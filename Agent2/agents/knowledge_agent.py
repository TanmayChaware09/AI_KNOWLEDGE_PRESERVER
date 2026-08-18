import json
import re
from pathlib import Path

from Agent2.shared.contracts import (
    RawDocument,
    KnowledgeCard
)

from Agent2.services.grok import GrokService


class KnowledgeAgent:

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self):

        self.llm = GrokService()

        prompt_path = (
            Path(__file__).resolve().parent.parent
            / "prompts"
            / "knowledge_prompt.txt"
        )

        with open(
            prompt_path,
            "r",
            encoding="utf-8"
        ) as f:

            self.prompt_template = f.read()


    # ========================================================
    # CATEGORY NORMALIZATION
    # ========================================================

    def _normalize_category(
        self,
        category
    ) -> str:

        if category is None:
            return "Other"

        category = str(
            category
        ).strip()

        if "." in category:

            category = category.split(
                "."
            )[-1]

        category = (
            category
            .replace("_", " ")
            .strip()
        )

        allowed_categories = {

            "decision": "Decision",

            "best practice": "Best Practice",

            "architecture": "Architecture",

            "bug fix": "Bug Fix",

            "workflow": "Workflow",

            "other": "Other"

        }

        normalized = allowed_categories.get(
            category.lower()
        )

        if normalized:

            return normalized


        # Fallback matching

        for key, value in allowed_categories.items():

            if key in category.lower():

                return value


        return "Other"


    # ========================================================
    # CONFIDENCE NORMALIZATION
    # ========================================================

    def _normalize_confidence(
        self,
        confidence
    ) -> float:

        try:

            confidence = float(
                confidence
            )

        except (
            TypeError,
            ValueError
        ):

            confidence = 0.0


        confidence = max(
            0.0,
            min(
                1.0,
                confidence
            )
        )


        # Avoid blindly trusting 1.0

        if confidence >= 1.0:

            confidence = 0.95


        return confidence


    # ========================================================
    # EXTRACT JSON OBJECT
    # ========================================================

    def _extract_json_text(
        self,
        response: str
    ) -> str:

        response = response.strip()


        # ----------------------------------------------------
        # Remove Markdown fences
        # ----------------------------------------------------

        response = re.sub(
            r"^```(?:json)?\s*",
            "",
            response,
            flags=re.IGNORECASE
        )

        response = re.sub(
            r"\s*```$",
            "",
            response
        )

        response = response.strip()


        # ----------------------------------------------------
        # Find first JSON object
        # ----------------------------------------------------

        start = response.find(
            "{"
        )

        if start == -1:

            raise ValueError(
                "No JSON object found in LLM response."
            )


        # ----------------------------------------------------
        # Find matching closing brace
        # ----------------------------------------------------

        depth = 0

        in_string = False

        escaped = False

        end = -1


        for i in range(
            start,
            len(response)
        ):

            char = response[i]


            if escaped:

                escaped = False

                continue


            if char == "\\" and in_string:

                escaped = True

                continue


            if char == '"':

                in_string = not in_string

                continue


            if in_string:

                continue


            if char == "{":

                depth += 1


            elif char == "}":

                depth -= 1


                if depth == 0:

                    end = i

                    break


        if end == -1:

            raise ValueError(
                "JSON object was not properly closed."
            )


        return response[
            start:end + 1
        ]


    # ========================================================
    # CLEAN COMMON JSON ERRORS
    # ========================================================

    def _clean_json(
        self,
        json_text: str
    ) -> str:

        cleaned = (
            json_text
            .replace("“", '"')
            .replace("”", '"')
            .replace("‘", "'")
            .replace("’", "'")
        )


        cleaned = cleaned.replace(
            "\\_",
            "_"
        )


        # ----------------------------------------------------
        # Remove comments outside strings
        # ----------------------------------------------------

        result = []

        in_string = False

        escaped = False

        i = 0


        while i < len(cleaned):

            char = cleaned[i]


            if escaped:

                result.append(
                    char
                )

                escaped = False

                i += 1

                continue


            if char == "\\" and in_string:

                result.append(
                    char
                )

                escaped = True

                i += 1

                continue


            if char == '"':

                in_string = not in_string

                result.append(
                    char
                )

                i += 1

                continue


            # Python-style comment

            if char == "#" and not in_string:

                while (
                    i < len(cleaned)
                    and cleaned[i] != "\n"
                ):

                    i += 1

                continue


            result.append(
                char
            )

            i += 1


        cleaned = "".join(
            result
        )


        # ----------------------------------------------------
        # Remove trailing commas
        # ----------------------------------------------------

        cleaned = re.sub(
            r",\s*}",
            "}",
            cleaned
        )

        cleaned = re.sub(
            r",\s*]",
            "]",
            cleaned
        )


        return cleaned.strip()


    # ========================================================
    # PARSE JSON
    # ========================================================

    def _parse_json(
        self,
        response: str
    ) -> dict:

        json_text = self._extract_json_text(
            response
        )

        cleaned = self._clean_json(
            json_text
        )


        try:

            data = json.loads(
                cleaned
            )

        except json.JSONDecodeError as e:

            raise ValueError(
                "Invalid JSON returned by LLM:\n"
                f"{response}"
            ) from e


        if not isinstance(
            data,
            dict
        ):

            raise ValueError(
                "LLM response must be a JSON object."
            )


        return data


    # ========================================================
    # JSON REPAIR
    # ========================================================

    def _repair_response(
        self,
        response: str
    ) -> dict:

        repair_prompt = f"""
You are a JSON repair engine.

Your ONLY task is to repair the JSON structure of the response.

Do NOT create new information.

Do NOT add facts.

Do NOT remove valid facts.

Do NOT reinterpret the knowledge.

Do NOT improve the content.

Do NOT create new knowledge cards.

Do NOT create duplicate knowledge cards.

Return ONLY valid JSON.

Required structure:

{{
  "knowledge_cards": [
    {{
      "title": "string",
      "summary": "string",
      "category": "Decision",
      "confidence": 0.90
    }}
  ]
}}

Allowed categories:

Decision
Best Practice
Architecture
Bug Fix
Workflow
Other

Rules:

1. Preserve the original meaning.
2. Repair malformed JSON syntax only.
3. Use double quotes.
4. Remove comments.
5. Remove trailing commas.
6. Do not add source.
7. Do not add employee_id.
8. Do not add timestamp.
9. Do not invent facts.
10. Do not create missing information.
11. Return an empty knowledge_cards list if the original response
    contains no safely recoverable knowledge.

MALFORMED RESPONSE:

{response}
"""


        repaired = self.llm.generate(
            repair_prompt
        )


        return self._parse_json(
            repaired
        )


    # ========================================================
    # SAFE LLM CALL
    # ========================================================

    def _call_and_parse(
    self,
    prompt: str
    ) -> dict:

        response = self.llm.generate(
        prompt
        )

        try:

            data = self._parse_json(
            response
            )

            print(
                "\n========== PARSED LLM JSON =========="
            )

            print(
                json.dumps(
                data,
                indent=2
                )
            )

            print(
                "====================================="
            )

            return data

        except ValueError as e:

            print(
            "\n========== RAW LLM RESPONSE =========="
        )

        print(response)

        print(
            "========== PARSER ERROR =========="
        )

        print(e)

        print(
            "====================================="
        )

        print(
            "Attempting automatic JSON repair..."
        )

        try:

            repaired = self._repair_response(
                response
            )

            print(
                "✓ JSON repair successful."
            )

            return repaired

        except ValueError as repair_error:

            print(
                "\n========== REPAIR ERROR =========="
            )

            print(
                repair_error
            )

            print(
                "================================="
            )

            return {
                "knowledge_cards": []
            }

    # ========================================================
    # GET RAW CARDS
    # ========================================================

    def _get_raw_cards(
        self,
        data: dict
    ) -> list:

        # ----------------------------------------------------
        # Preferred format
        # ----------------------------------------------------

        cards = data.get(
            "knowledge_cards"
        )


        if isinstance(
            cards,
            list
        ):

            return cards


        # ----------------------------------------------------
        # Also support a single card
        # ----------------------------------------------------

        if (
            "title" in data
            and "summary" in data
        ):

            return [
                data
            ]


        return []


    # ========================================================
    # BUILD KNOWLEDGE CARD
    # ========================================================

    def _build_card(
        self,
        card_data: dict,
        document: RawDocument
    ):

        if not isinstance(
            card_data,
            dict
        ):

            return None


        title = str(
            card_data.get(
                "title",
                ""
            )
        ).strip()


        summary = str(
            card_data.get(
                "summary",
                ""
            )
        ).strip()


        # ----------------------------------------------------
        # Required fields
        # ----------------------------------------------------

        if not title or not summary:

            return None


        # ----------------------------------------------------
        # No valuable knowledge
        # ----------------------------------------------------

        if title.lower() == (
            "no valuable knowledge"
        ):

            return None


        # ----------------------------------------------------
        # Reject obvious hallucinated placeholders
        # ----------------------------------------------------

        if summary.lower() in {
            "none",
            "n/a",
            "unknown",
            "not available"
        }:

            return None


        # ----------------------------------------------------
        # Category
        # ----------------------------------------------------

        category = self._normalize_category(
            card_data.get(
                "category",
                "Other"
            )
        )


        # ----------------------------------------------------
        # Confidence
        # ----------------------------------------------------

        confidence = (
            self._normalize_confidence(
                card_data.get(
                    "confidence",
                    0.0
                )
            )
        )


        # ----------------------------------------------------
        # Metadata MUST come from RawDocument
        # ----------------------------------------------------

        normalized = {

            "title": title,

            "summary": summary,

            "category": category,

            "confidence": confidence,

            "source": document.source,

            "employee_id": document.employee_id,

            "timestamp": document.timestamp

        }


        try:

            return KnowledgeCard(
                **normalized
            )

        except Exception as e:

            print(
                f"⚠ Invalid KnowledgeCard skipped: {title}"
            )

            print(
                f"  Error: {e}"
            )

            return None


    # ========================================================
    # NORMALIZE TEXT
    # ========================================================

    def _normalize_text(
        self,
        text: str
    ) -> str:

        return re.sub(
            r"[^a-z0-9]+",
            " ",
            text.lower()
        ).strip()


    # ========================================================
    # DUPLICATE DETECTION
    # ========================================================

    def _is_duplicate(
        self,
        card: KnowledgeCard,
        existing_cards: list
    ) -> bool:

        title = self._normalize_text(
            card.title
        )

        summary = self._normalize_text(
            card.summary
        )


        title_words = set(
            title.split()
        )

        summary_words = set(
            summary.split()
        )


        for existing in existing_cards:

            existing_title = (
                self._normalize_text(
                    existing.title
                )
            )

            existing_summary = (
                self._normalize_text(
                    existing.summary
                )
            )


            existing_title_words = set(
                existing_title.split()
            )

            existing_summary_words = set(
                existing_summary.split()
            )


            # ------------------------------------------------
            # Exact title
            # ------------------------------------------------

            if title == existing_title:

                return True


            # ------------------------------------------------
            # Exact summary
            # ------------------------------------------------

            if summary == existing_summary:

                return True


            # ------------------------------------------------
            # Strong title overlap
            # ------------------------------------------------

            if (
                title_words
                and existing_title_words
            ):

                intersection = (
                    title_words
                    & existing_title_words
                )

                union = (
                    title_words
                    | existing_title_words
                )


                similarity = (
                    len(intersection)
                    /
                    len(union)
                )


                if similarity >= 0.75:

                    return True


            # ------------------------------------------------
            # Strong summary overlap
            # ------------------------------------------------

            if (
                summary_words
                and existing_summary_words
            ):

                intersection = (
                    summary_words
                    & existing_summary_words
                )

                union = (
                    summary_words
                    |
                    existing_summary_words
                )


                similarity = (
                    len(intersection)
                    /
                    len(union)
                )


                if similarity >= 0.85:

                    return True


        return False


    # ========================================================
    # SINGLE EXTRACTION PASS
    # ========================================================

    def _first_pass(
        self,
        document: RawDocument
    ) -> list:

        prompt = self.prompt_template.replace(
            "{document}",
            document.model_dump_json()
        )


        data = self._call_and_parse(
            prompt
        )


        return self._get_raw_cards(
            data
        )


    # ========================================================
    # MAIN EXTRACTION
    # ========================================================

    def extract(
        self,
        document: RawDocument
    ) -> list[KnowledgeCard]:

        print(
            "\nAgent 2 : Knowledge extraction..."
        )


        # ----------------------------------------------------
        # ONLY ONE LLM EXTRACTION PASS
        # ----------------------------------------------------

        raw_cards = self._first_pass(
            document
        )


        final_cards = []


        for card_data in raw_cards:

            card = self._build_card(
                card_data,
                document
            )


            if card is None:

                continue


            # ------------------------------------------------
            # Remove duplicates
            # ------------------------------------------------

            if self._is_duplicate(
                card,
                final_cards
            ):

                continue


            final_cards.append(
                card
            )


        print(
            f"  Final cards: {len(final_cards)}"
        )


        return final_cards


# ============================================================
# PUBLIC FUNCTION
# ============================================================

def extract_knowledge(
    document: RawDocument
) -> list[KnowledgeCard]:

    agent = KnowledgeAgent()

    return agent.extract(
        document
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    from datetime import datetime


    test_document = RawDocument(

        source="slack",

        employee_name="Test User",

        employee_id="TEST001",

        department="Engineering",

        timestamp=datetime.now(),

        url="test",

        content="""
        PostgreSQL is used for analytics because reporting
        relies on complex relational joins.

        Analytics currently remains in the same AWS account,
        while moving it to a separate account is a pending proposal.

        The LLM has no database-write permission.
        LLM output must pass through a Checker before the Fixer
        can execute an approved and validated operation.
        """

    )


    cards = extract_knowledge(
        test_document
    )


    print(
        "\n======================================"
    )

    print(
        "KNOWLEDGE EXTRACTION TEST"
    )

    print(
        "======================================"
    )


    print(
        f"\nCards extracted: {len(cards)}"
    )


    for i, card in enumerate(
        cards,
        start=1
    ):

        print(
            f"\nKnowledge Card {i}"
        )

        print(
            "--------------------------------------"
        )

        print(
            f"Title      : {card.title}"
        )

        print(
            f"Summary    : {card.summary}"
        )

        print(
            f"Category   : {card.category}"
        )

        print(
            f"Confidence : {card.confidence}"
        )

        print(
            f"Source     : {card.source}"
        )

        print(
            f"Employee ID: {card.employee_id}"
        )

        print(
            f"Timestamp  : {card.timestamp}"
        )