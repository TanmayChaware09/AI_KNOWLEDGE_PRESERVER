import json
import re

from backend_56.agents.retrieval_agent import retrieve
from Agent2.services.grok import GrokService


# ============================================================
# CONSTANTS
# ============================================================

FALLBACK = "No sufficient knowledge found."

PRIVACY_RESPONSE = (
    "The work or decision can be summarized, "
    "but individual employee identities are not disclosed."
)

VALID_ROLES = {
    "employee",
    "manager",
    "hr",
}


# ============================================================
# ROLE INSTRUCTIONS
# ============================================================

ROLE_INSTRUCTIONS = {

    "employee": """
You are answering for an employee.

Give useful team and project information.

The employee can know:
- project updates
- team progress
- technical changes
- pending work
- decisions
- meeting outcomes
- work performed by the team

Never reveal:
- employee names
- employee IDs
- email addresses
- usernames
- personal identifiers

Describe work without identifying who performed it.
""",

    "manager": """
You are answering for a manager.

Focus on:
- project progress
- team progress
- pending work
- blockers
- decisions
- technical changes
- meeting outcomes

Never reveal:
- employee names
- employee IDs
- email addresses
- usernames
- personal identifiers

Describe work at team/project level.
""",

    "hr": """
You are answering for HR.

Focus on:
- overall project status
- major updates
- pending work
- meeting summaries
- major decisions
- organization-level information

Never reveal:
- employee names
- employee IDs
- email addresses
- usernames
- personal identifiers

Keep information at an organization/project level.
"""
}


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_intent(query: str) -> str:

    text = query.lower().strip()

    # --------------------------------------------------------
    # MEETING
    # --------------------------------------------------------

    meeting_patterns = [
        "last meeting",
        "latest meeting",
        "recent meeting",
        "meeting summary",
        "summarize the meeting",
        "summarize last meeting",
        "what happened in the meeting",
        "what was discussed in the meeting",
        "meeting discussion",
        "meeting decision",
        "meeting decisions",
    ]

    if any(
        pattern in text
        for pattern in meeting_patterns
    ):
        return "meeting_summary"


    # --------------------------------------------------------
    # PENDING WORK
    # --------------------------------------------------------

    pending_patterns = [
        "what is pending",
        "what's pending",
        "whats pending",
        "pending work",
        "pending tasks",
        "what work is still pending",
        "what is still pending",
        "what remains",
        "what is remaining",
        "what's remaining",
        "remaining work",
        "unfinished work",
        "incomplete work",
        "what needs to be done",
        "what needs completion",
    ]

    if any(
        pattern in text
        for pattern in pending_patterns
    ):
        return "pending_work"


    # --------------------------------------------------------
    # RECENT UPDATES
    # --------------------------------------------------------

    recent_patterns = [
        "recent updates",
        "recent update",
        "latest updates",
        "latest update",
        "what happened recently",
        "what happened lately",
        "what changed recently",
        "recent changes",
        "latest changes",
        "recent activity",
        "latest activity",
        "what is happening",
        "what's happening",
        "what updates have happened",
    ]

    if any(
        pattern in text
        for pattern in recent_patterns
    ):
        return "recent_updates"


    # --------------------------------------------------------
    # PROJECT PROGRESS
    # --------------------------------------------------------

    progress_patterns = [
        "project progress",
        "project status",
        "how is the project",
        "how is the project going",
        "progress of the project",
        "current progress",
        "overall progress",
        "team progress",
        "how are we progressing",
    ]

    if any(
        pattern in text
        for pattern in progress_patterns
    ):
        return "project_progress"


    # --------------------------------------------------------
    # DECISIONS
    # --------------------------------------------------------

    decision_patterns = [
        "what decisions",
        "which decisions",
        "decisions made",
        "decisions taken",
        "what was decided",
        "what has been decided",
        "major decisions",
        "decision regarding",
        "decision about",
        "why was",
        "why did the team",
    ]

    if any(
        pattern in text
        for pattern in decision_patterns
    ):
        return "decisions"


    # --------------------------------------------------------
    # BLOCKERS
    # --------------------------------------------------------

    blocker_patterns = [
        "blockers",
        "blocked",
        "blocker",
        "what is blocking",
        "what's blocking",
        "current blockers",
        "project blockers",
    ]

    if any(
        pattern in text
        for pattern in blocker_patterns
    ):
        return "blockers"


    return "general"


# ============================================================
# IDENTITY QUESTION DETECTION
# ============================================================

def is_identity_question(
    query: str
) -> bool:

    text = query.lower().strip()

    identity_patterns = [

        "who ",
        "who?",
        "which employee",
        "which employees",
        "which person",
        "which people",
        "what employee",
        "whose work",
        "whose task",
        "whose update",
        "who completed",
        "who made",
        "who changed",
        "who updated",
        "who worked",
        "who sent",
        "who decided",
        "who created",
        "who fixed",
        "who implemented",
        "who wrote",
        "who added",
        "who removed",
        "who uploaded",
        "who performed",
        "who handled",
        "who was responsible",
        "responsible employee",
        "employee responsible",
    ]

    return any(
        pattern in text
        for pattern in identity_patterns
    )


# ============================================================
# INTENT INSTRUCTIONS
# ============================================================

INTENT_INSTRUCTIONS = {

    "meeting_summary": """
Summarize the meeting using the provided knowledge.

Focus on:
- topics
- decisions
- outcomes
- updates
- pending work

Do not identify participants.
""",

    "pending_work": """
Identify only work that is explicitly pending,
unfinished, remaining, unresolved, or required
according to the provided knowledge.

Do not invent pending tasks.
Do not identify employees.
""",

    "recent_updates": """
Summarize the recent project/team updates contained
in the provided knowledge.

Combine information from all relevant knowledge items.

Do not identify employees.
""",

    "project_progress": """
Summarize project progress using only the provided
knowledge.

Focus on completed/current/pending work and blockers.
Do not identify employees.
""",

    "decisions": """
Explain decisions and their reasons only when they
are explicitly supported by the knowledge.

Do not identify who made the decision.
""",

    "blockers": """
Summarize blockers and unresolved issues supported
by the knowledge.

Do not identify employees.
""",

    "general": """
Answer directly using only the provided knowledge.
"""
}


# ============================================================
# ANSWER AGENT
# ============================================================

class AnswerAgent:

    def __init__(self):

        self.llm = GrokService()


    # ========================================================
    # BUILD CONTEXT
    # ========================================================

    def _build_context(
        self,
        documents: list
    ) -> str:

        if not documents:
            return ""

        context_parts = []

        for index, document in enumerate(
            documents,
            start=1
        ):

            context_parts.append(
                f"Knowledge {index}:\n{document}"
            )

        return "\n\n".join(
            context_parts
        )


    # ========================================================
    # IDENTITY SANITIZATION
    # ========================================================

    def _sanitize_identity(
        self,
        text: str
    ) -> str:

        if not text:
            return text

        sanitized = text

        # Employee IDs
        sanitized = re.sub(
            r"\bEMP[-_]?\d+\b",
            "a team member",
            sanitized,
            flags=re.IGNORECASE
        )

        # Manager IDs
        sanitized = re.sub(
            r"\bMANAGER[-_]?\d+\b",
            "a manager",
            sanitized,
            flags=re.IGNORECASE
        )

        # HR IDs
        sanitized = re.sub(
            r"\bHR[-_]?\d+\b",
            "HR",
            sanitized,
            flags=re.IGNORECASE
        )

        # Email addresses
        sanitized = re.sub(
            r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
            "a team member",
            sanitized,
            flags=re.IGNORECASE
        )

        return sanitized


    # ========================================================
    # REMOVE COMMON ATTRIBUTION
    # ========================================================

    def _remove_attribution(
        self,
        text: str
    ) -> str:

        if not text:
            return text

        sanitized = text

        patterns = [

            (
                r"\b[A-Z][a-z]+\s+completed\b",
                "The team completed"
            ),

            (
                r"\b[A-Z][a-z]+\s+implemented\b",
                "The team implemented"
            ),

            (
                r"\b[A-Z][a-z]+\s+updated\b",
                "The team updated"
            ),

            (
                r"\b[A-Z][a-z]+\s+fixed\b",
                "The team fixed"
            ),

            (
                r"\b[A-Z][a-z]+\s+created\b",
                "The team created"
            ),

            (
                r"\b[A-Z][a-z]+\s+changed\b",
                "The team changed"
            ),

            (
                r"\b[A-Z][a-z]+\s+added\b",
                "The team added"
            ),

            (
                r"\b[A-Z][a-z]+\s+removed\b",
                "The team removed"
            ),

            (
                r"\b[A-Z][a-z]+\s+worked\b",
                "The team worked"
            ),

            (
                r"\b[A-Z][a-z]+\s+decided\b",
                "The team decided"
            ),
        ]

        for pattern, replacement in patterns:

            sanitized = re.sub(
                pattern,
                replacement,
                sanitized
            )

        return sanitized


    # ========================================================
    # PRIVACY CLEANUP
    # ========================================================

    def _privacy_cleanup(
        self,
        text: str
    ) -> str:

        text = self._sanitize_identity(
            text
        )

        text = self._remove_attribution(
            text
        )

        return text.strip()


    # ========================================================
    # CLEAN RESPONSE
    # ========================================================

    def _clean_response(
        self,
        response: str
    ) -> str:

        if not response:
            return FALLBACK

        response = response.strip()

        # ----------------------------------------------------
        # Remove markdown fences
        # ----------------------------------------------------

        if response.startswith(
            "```json"
        ):

            response = response[7:].strip()

        elif response.startswith(
            "```"
        ):

            response = response[3:].strip()

        if response.endswith(
            "```"
        ):

            response = response[:-3].strip()


        # ----------------------------------------------------
        # JSON response handling
        # ----------------------------------------------------

        try:

            parsed = json.loads(
                response
            )

            if isinstance(
                parsed,
                dict
            ):

                for field in [
                    "answer",
                    "response",
                    "summary",
                    "statement",
                    "decision",
                ]:

                    value = parsed.get(
                        field
                    )

                    if value:

                        response = str(
                            value
                        ).strip()

                        break

        except (
            json.JSONDecodeError,
            TypeError
        ):

            pass


        if not response:

            return FALLBACK


        # ----------------------------------------------------
        # Fallback detection
        # ----------------------------------------------------

        lowered = response.lower()

        fallback_phrases = [
            "no sufficient knowledge found",
            "not enough information",
            "insufficient information",
            "there is not enough information",
            "cannot be determined from the context",
            "cannot answer from the provided context",
        ]

        if any(
            phrase in lowered
            for phrase in fallback_phrases
        ):

            return FALLBACK


        return response


    # ========================================================
    # GENERATE ANSWER
    # ========================================================

    def generate_answer(
        self,
        query: str,
        role: str,
        user_id: str
    ) -> str:

        role = (
            role or ""
        ).strip().lower()

        query = (
            query or ""
        ).strip()


        # ----------------------------------------------------
        # Validate
        # ----------------------------------------------------

        if role not in VALID_ROLES:

            print(
                f"Invalid RAG role: {role}"
            )

            return FALLBACK


        if not query:

            return FALLBACK


        # ----------------------------------------------------
        # Intent
        # ----------------------------------------------------

        intent = detect_intent(
            query
        )

        print(
            f"\nRAG Role: {role}"
        )

        print(
            f"RAG Intent: {intent}"
        )


        # ----------------------------------------------------
        # Identity protection
        # ----------------------------------------------------

        if is_identity_question(
            query
        ):

            return PRIVACY_RESPONSE


        # ----------------------------------------------------
        # Retrieval
        # ----------------------------------------------------

        documents = retrieve(
            query,
            n_results=8
        )


        print(
            f"Answer Agent received "
            f"{len(documents)} documents."
        )


        # ----------------------------------------------------
        # No knowledge
        # ----------------------------------------------------

        if not documents:

            print(
                "Answer Agent: no relevant knowledge."
            )

            return FALLBACK


        # ----------------------------------------------------
        # Context
        # ----------------------------------------------------

        context = self._build_context(
            documents
        )


        if not context:

            return FALLBACK


        print(
            "\nAnswer Agent Context:"
        )

        for index, document in enumerate(
            documents,
            start=1
        ):

            print(
                f"{index}. {document[:150]}"
            )


        # ----------------------------------------------------
        # Instructions
        # ----------------------------------------------------

        role_instruction = (
            ROLE_INSTRUCTIONS[role]
        )

        intent_instruction = (
            INTENT_INSTRUCTIONS[intent]
        )


        # ----------------------------------------------------
        # Prompt
        # ----------------------------------------------------

        prompt = f"""
You are the Answer Agent for an internal AI knowledge
system.

Your ONLY source of factual information is the KNOWLEDGE
CONTEXT below.

Do not use your pretrained/world knowledge.

Do not guess.

Do not invent information.

Do not add facts that are not present in the context.

============================================================
USER ROLE
============================================================

{role}

============================================================
ROLE RULES
============================================================

{role_instruction}

============================================================
QUERY INTENT
============================================================

{intent}

{intent_instruction}

============================================================
PRIVACY
============================================================

Never reveal:
- employee names
- employee IDs
- email addresses
- usernames
- personal identifiers

Never say who performed an action.

Describe actions using team/project wording.

============================================================
IMPORTANT ANSWERING RULE
============================================================

Use ALL relevant knowledge items when answering.

If multiple knowledge items are relevant, synthesize them
into ONE useful answer.

Do NOT simply return the title of a knowledge item.

For example, do NOT answer:

"Decision"

Instead explain the actual supported information.

============================================================
GROUNDING
============================================================

If the knowledge context does not contain enough information
to answer the question, return exactly:

No sufficient knowledge found.

============================================================
USER QUESTION
============================================================

{query}

============================================================
KNOWLEDGE CONTEXT
============================================================

{context}

============================================================
FINAL ANSWER
============================================================
"""


        # ----------------------------------------------------
        # LLM
        # ----------------------------------------------------

        try:

            response = self.llm.generate(
                prompt
            )

            print(
                "\nRaw LLM response:"
            )

            print(
                response
            )


            response = self._clean_response(
                response
            )


            if response == FALLBACK:

                return FALLBACK


            response = self._privacy_cleanup(
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

def generate_answer(
    query=None,
    role=None,
    user_id=None,
    question=None
) -> str:

    """
    Supports BOTH:

        generate_answer(
            query=...
        )

    and:

        generate_answer(
            question=...
        )

    This prevents an API parameter-name mismatch.
    """

    if not query:

        query = question


    agent = AnswerAgent()


    return agent.generate_answer(
        query=query,
        role=role,
        user_id=user_id
    )


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    question = input(
        "Ask a question: "
    )


    role = input(
        "Role (employee/manager/hr): "
    ).strip().lower()


    user_id = input(
        "User ID: "
    ).strip()


    response = generate_answer(
        question=question,
        role=role,
        user_id=user_id
    )


    print(
        "\nAnswer:\n"
    )

    print(
        response
    )