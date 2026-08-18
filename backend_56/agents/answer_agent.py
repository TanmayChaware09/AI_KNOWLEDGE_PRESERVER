import json

from backend_56.agents.retrieval_agent import retrieve
from Agent2.services.grok import GrokService


# ============================================================
# CONSTANTS
# ============================================================

FALLBACK = "No sufficient knowledge found."


class AnswerAgent:

    def __init__(self):
        self.llm = GrokService()

    # ========================================================
    # BUILD CONTEXT
    # ========================================================

    def _build_context(self, documents: list) -> str:

        context_parts = []

        for i, document in enumerate(
            documents,
            start=1
        ):
            context_parts.append(
                f"[Knowledge {i}]\n"
                f"{document}"
            )

        return "\n\n".join(context_parts)

    # ========================================================
    # CLEAN LLM RESPONSE
    # ========================================================

    def _clean_response(self, response: str) -> str:

        if not response:
            return FALLBACK

        response = response.strip()

        # ----------------------------------------------------
        # Remove markdown fences
        # ----------------------------------------------------

        if response.startswith("```json"):
            response = response[7:].strip()

        elif response.startswith("```"):
            response = response[3:].strip()

        if response.endswith("```"):
            response = response[:-3].strip()

        # ----------------------------------------------------
        # Try to parse JSON
        # ----------------------------------------------------

        try:

            parsed = json.loads(response)

            if isinstance(parsed, dict):

                # --------------------------------------------
                # Standard answer fields
                # --------------------------------------------

                standard_fields = [
                    "answer",
                    "response",
                    "summary",
                    "statement",
                    "decision"
                ]

                for field in standard_fields:

                    value = parsed.get(field)

                    if value:

                        response = str(
                            value
                        ).strip()

                        break

                else:

                    # ----------------------------------------
                    # Single arbitrary key
                    #
                    # Example:
                    #
                    # {
                    #   "Analytics AWS Account Strategy":
                    #   "AWS account strategy remains..."
                    # }
                    # ----------------------------------------

                    if len(parsed) == 1:

                        value = next(
                            iter(
                                parsed.values()
                            )
                        )

                        if isinstance(
                            value,
                            str
                        ):

                            response = value.strip()

                        elif value is not None:

                            response = str(
                                value
                            ).strip()

                        else:

                            response = FALLBACK

                    else:

                        # ------------------------------------
                        # Multiple unknown JSON fields.
                        #
                        # Do not guess which field is the
                        # actual answer.
                        # ------------------------------------

                        response = FALLBACK

        except (
            json.JSONDecodeError,
            TypeError
        ):

            # Normal plain-text response.
            pass

        # ----------------------------------------------------
        # Empty response
        # ----------------------------------------------------

        if not response:
            return FALLBACK

        # ----------------------------------------------------
        # Normalize fallback variants
        # ----------------------------------------------------

        lowered = response.lower()

        fallback_phrases = [
            "no sufficient knowledge found",
            "not enough information",
            "insufficient information",
            "there is not enough information",
            "cannot be determined from the context",
            "cannot answer from the provided context"
        ]

        for phrase in fallback_phrases:

            if phrase in lowered:
                return FALLBACK

        return response

    # ========================================================
    # ANSWER GENERATION
    # ========================================================

    def generate_answer(self, query: str) -> str:

        # ====================================================
        # AGENT 5 : RETRIEVE KNOWLEDGE
        # ====================================================

        documents = retrieve(
            query,
            n_results=5
        )

        if not documents:
            return FALLBACK

        # ====================================================
        # BUILD CONTEXT
        # ====================================================

        context = self._build_context(
            documents
        )

        # ====================================================
        # STRICT RAG PROMPT
        # ====================================================

        prompt = f"""
You are the final Answer Agent of an AI Loss Prevention
System.

Your job is to answer the user's question using ONLY the
knowledge provided in the KNOWLEDGE CONTEXT.

Do not use outside knowledge.

Do not use general knowledge.

Do not guess.

Do not invent facts.

============================================================
GROUNDING RULES
============================================================

1. Every factual statement must be directly supported by
   the knowledge context.

2. Use only knowledge that is relevant to the user's question.

3. Multiple knowledge entries may be combined when they
   describe the same decision or workflow and do not
   contradict each other.

4. Do not combine unrelated knowledge entries.

5. You may rewrite the knowledge in clear natural language,
   but do not change its meaning.

6. Do not invent people, dates, technologies, decisions,
   reasons, permissions, workflows, or requirements.

7. If the context does not contain enough information to
   answer the question, return exactly:

No sufficient knowledge found.

8. If only part of the question is supported, answer only
   the supported part.

============================================================
IMPORTANT WORKFLOW EXAMPLE
============================================================

Knowledge:

"The LLM does not have direct database-write permission."

Knowledge:

"The LLM must pass through the Checker before the Fixer
can execute an approved and validated correction."

Question:

"What is the Checker and Fixer workflow for LLM database
operations?"

Valid answer:

"The LLM does not have direct database-write permission.
Its output must pass through the Checker before the Fixer
can execute an approved and validated correction."

============================================================
ANSWER FORMAT
============================================================

Return ONLY a normal plain-text answer.

DO NOT return JSON.

DO NOT return a JSON object.

DO NOT return key-value pairs.

DO NOT return field names.

DO NOT return markdown code blocks.

DO NOT mention retrieval, embeddings, Chroma, agents,
prompts, distances, or internal system details.

Keep the answer concise and direct.

============================================================
USER QUESTION
============================================================

{query}

============================================================
KNOWLEDGE CONTEXT
============================================================

{context}

============================================================
FINAL CHECK
============================================================

Before answering:

- Is the answer supported by the knowledge?
- Did I avoid outside knowledge?
- Did I avoid guessing?
- Did I avoid unrelated information?
- Did I preserve the meaning?

If yes, return the plain-text answer.

If no, return exactly:

No sufficient knowledge found.

============================================================
FINAL RESPONSE
============================================================
"""

        # ====================================================
        # CALL LLM
        # ====================================================

        try:

            response = self.llm.generate(
                prompt
            )

            response = self._clean_response(
                response
            )

            return response

        except Exception as e:

            print(
                f"Answer Generation Error: {e}"
            )

            return FALLBACK


# ============================================================
# PUBLIC FUNCTION
# ============================================================

def generate_answer(query: str) -> str:

    agent = AnswerAgent()

    return agent.generate_answer(
        query
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    query = input(
        "Ask a question: "
    )

    response = generate_answer(
        query
    )

    print(
        "\nAnswer:\n"
    )

    print(
        response
    )