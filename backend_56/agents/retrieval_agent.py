import re
from datetime import datetime, timezone

import chromadb

from backend_56.services.embedding import generate_embedding
from backend_56.shared.config import (
    CHROMA_PATH,
    COLLECTION_NAME,
)


# ============================================================
# CHROMA
# ============================================================

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


# ============================================================
# INTENT KEYWORDS
# ============================================================

INTENT_KEYWORDS = {
    "recent_updates": {
        "recent",
        "recently",
        "latest",
        "update",
        "updates",
        "updated",
        "changed",
        "changes",
        "activity",
        "happened",
        "new",
    },

    "pending_work": {
        "pending",
        "remaining",
        "unfinished",
        "incomplete",
        "todo",
        "blocker",
        "blocked",
        "unresolved",
        "needs",
        "complete",
        "completion",
        "task",
        "tasks",
        "work",
    },

    "meeting_summary": {
        "meeting",
        "meetings",
        "discussion",
        "discussed",
        "summary",
        "summarize",
        "agenda",
        "minutes",
        "outcome",
        "outcomes",
    },

    "project_progress": {
        "project",
        "progress",
        "status",
        "completed",
        "completion",
        "development",
        "work",
    },

    "decisions": {
        "decision",
        "decisions",
        "decided",
        "chosen",
        "choice",
        "architecture",
        "retained",
        "selected",
    },

    "blockers": {
        "blocker",
        "blockers",
        "blocked",
        "issue",
        "issues",
        "problem",
        "problems",
        "dependency",
        "dependencies",
        "unresolved",
    },
}


# ============================================================
# STOP WORDS
# ============================================================

STOP_WORDS = {
    "what",
    "was",
    "were",
    "is",
    "are",
    "the",
    "a",
    "an",
    "about",
    "for",
    "from",
    "in",
    "on",
    "of",
    "to",
    "and",
    "or",
    "did",
    "does",
    "do",
    "how",
    "why",
    "which",
    "who",
    "current",
    "currently",
    "please",
    "tell",
    "me",
    "show",
    "give",
    "can",
    "you",
    "could",
    "would",
    "should",
    "have",
    "has",
    "been",
    "it",
    "this",
    "that",
    "we",
    "our",
    "their",
    "they",
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:

    return re.sub(
        r"[^a-z0-9]+",
        " ",
        str(text).lower()
    ).strip()


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_intent(query: str) -> str:

    text = normalize_text(query)

    # --------------------------------------------------------
    # MEETING
    # --------------------------------------------------------

    if (
        "last meeting" in text
        or "latest meeting" in text
        or "recent meeting" in text
        or "meeting summary" in text
        or "summarize meeting" in text
        or "what was discussed" in text
    ):
        return "meeting_summary"


    # --------------------------------------------------------
    # PENDING WORK
    # --------------------------------------------------------

    if (
        "what is pending" in text
        or "whats pending" in text
        or "pending work" in text
        or "pending tasks" in text
        or "remaining work" in text
        or "what remains" in text
        or "what needs to be done" in text
        or "unfinished work" in text
        or "incomplete work" in text
    ):
        return "pending_work"


    # --------------------------------------------------------
    # RECENT UPDATES
    # --------------------------------------------------------

    if (
        "recent updates" in text
        or "recent update" in text
        or "latest updates" in text
        or "latest update" in text
        or "what happened recently" in text
        or "recent changes" in text
        or "recent activity" in text
        or "what happened lately" in text
    ):
        return "recent_updates"


    # --------------------------------------------------------
    # KEYWORD SCORING
    # --------------------------------------------------------

    words = set(
        text.split()
    )

    scores = {}

    for intent, keywords in INTENT_KEYWORDS.items():

        scores[intent] = len(
            words.intersection(
                keywords
            )
        )


    best_intent = max(
        scores,
        key=scores.get
    )


    if scores[best_intent] > 0:

        return best_intent


    return "general"


# ============================================================
# KEYWORD EXTRACTION
# ============================================================

def extract_keywords(text: str):

    words = normalize_text(
        text
    ).split()

    return {
        word
        for word in words
        if (
            len(word) >= 3
            and word not in STOP_WORDS
        )
    }


# ============================================================
# KEYWORD SCORE
# ============================================================

def keyword_score(
    query_keywords,
    document
):

    if not query_keywords:
        return 0.0


    document_words = set(
        normalize_text(
            document
        ).split()
    )


    matches = (
        query_keywords
        &
        document_words
    )


    return (
        len(matches)
        /
        len(query_keywords)
    )


# ============================================================
# INTENT SCORE
# ============================================================

def intent_score(
    intent,
    document
):

    if intent == "general":
        return 0.0


    document_words = set(
        normalize_text(
            document
        ).split()
    )


    intent_words = INTENT_KEYWORDS.get(
        intent,
        set()
    )


    if not intent_words:
        return 0.0


    matches = (
        document_words
        &
        intent_words
    )


    return (
        len(matches)
        /
        len(intent_words)
    )


# ============================================================
# RECENCY SCORE
# ============================================================

def recency_score(
    timestamp
):

    if not timestamp:
        return 0.0


    try:

        timestamp_text = str(
            timestamp
        ).strip()


        # ----------------------------------------------------
        # Handle timestamps ending with Z
        # ----------------------------------------------------

        if timestamp_text.endswith(
            "Z"
        ):

            timestamp_text = (
                timestamp_text[:-1]
                + "+00:00"
            )


        dt = datetime.fromisoformat(
            timestamp_text
        )


        # ----------------------------------------------------
        # Make timezone aware
        # ----------------------------------------------------

        if dt.tzinfo is None:

            dt = dt.replace(
                tzinfo=timezone.utc
            )


        now = datetime.now(
            timezone.utc
        )


        age_hours = (
            now - dt
        ).total_seconds() / 3600


        # ----------------------------------------------------
        # Protect against future timestamps
        # ----------------------------------------------------

        age_hours = max(
            0.0,
            age_hours
        )


        # ----------------------------------------------------
        # Recency decay
        #
        # 0 hours  -> 1.00
        # 24 hours -> ~0.50
        # 48 hours -> ~0.33
        # 72 hours -> ~0.25
        #
        # This gives recent knowledge a stronger ranking
        # without completely ignoring older knowledge.
        # ----------------------------------------------------

        return 1.0 / (
            1.0
            +
            age_hours / 24.0
        )


    except Exception:

        return 0.0


# ============================================================
# MAIN RETRIEVAL
# ============================================================

def retrieve(
    query: str,
    n_results: int = 5
) -> list:

    try:

        if not query.strip():

            return []


        # ====================================================
        # QUERY ANALYSIS
        # ====================================================

        intent = detect_intent(
            query
        )

        query_keywords = extract_keywords(
            query
        )


        print(
            "\n================================================"
        )

        print(
            "RAG RETRIEVAL"
        )

        print(
            "================================================"
        )

        print(
            f"Original query : {query}"
        )

        print(
            f"Detected intent: {intent}"
        )

        print(
            f"Keywords       : "
            f"{sorted(query_keywords)}"
        )


        # ====================================================
        # COLLECTION CHECK
        # ====================================================

        total_records = collection.count()


        print(
            f"Knowledge count: {total_records}"
        )


        if total_records == 0:

            print(
                "Knowledge collection is empty."
            )

            return []


        # ====================================================
        # QUERY EMBEDDING
        # ====================================================

        query_embedding = generate_embedding(
            query
        )


        # ====================================================
        # SEMANTIC SEARCH
        # ====================================================

        candidate_count = min(
            max(
                10,
                n_results * 5
            ),
            total_records
        )


        results = collection.query(

            query_embeddings=[
                query_embedding
            ],

            n_results=candidate_count,

            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )


        documents = (
            results.get(
                "documents",
                [[]]
            )[0]
        )


        metadatas = (
            results.get(
                "metadatas",
                [[]]
            )[0]
        )


        distances = (
            results.get(
                "distances",
                [[]]
            )[0]
        )


        print(
            f"Semantic candidates: "
            f"{len(documents)}"
        )


        # ====================================================
        # RANKING
        # ====================================================

        ranked = []


        for index, document in enumerate(
            documents
        ):

            if not document:
                continue


            metadata = (
                metadatas[index]
                if index < len(metadatas)
                else {}
            )


            distance = (
                distances[index]
                if index < len(distances)
                else 1.0
            )


            # ------------------------------------------------
            # Semantic score
            # ------------------------------------------------

            semantic = max(
                0.0,
                1.0 - float(distance)
            )


            # ------------------------------------------------
            # Keyword score
            # ------------------------------------------------

            lexical = keyword_score(
                query_keywords,
                document
            )


            # ------------------------------------------------
            # Intent score
            # ------------------------------------------------

            intent_match = intent_score(
                intent,
                document
            )


            # ------------------------------------------------
            # Timestamp
            # ------------------------------------------------

            timestamp = metadata.get(
                "timestamp"
            )


            # ------------------------------------------------
            # Recency
            # ------------------------------------------------

            recent = recency_score(
                timestamp
            )


            # ------------------------------------------------
            # Final score
            #
            # NORMAL:
            # semantic + keyword + intent
            #
            # RECENT/PENDING:
            # semantic + keyword + intent + recency
            #
            # Recency is NOT allowed to make an unrelated
            # document relevant by itself.
            # ------------------------------------------------

            if intent in {
                "recent_updates",
                "pending_work",
            }:

                final_score = (

                    0.50
                    * semantic

                    +

                    0.25
                    * lexical

                    +

                    0.10
                    * intent_match

                    +

                    0.15
                    * recent

                )

            else:

                final_score = (

                    0.65
                    * semantic

                    +

                    0.25
                    * lexical

                    +

                    0.10
                    * intent_match

                )


            ranked.append({

                "document": document,

                "metadata": metadata,

                "distance": float(distance),

                "semantic_score": semantic,

                "keyword_score": lexical,

                "intent_score": intent_match,

                "recency_score": recent,

                "final_score": final_score,

            })


        # ====================================================
        # SORT
        # ====================================================

        ranked.sort(
            key=lambda item:
                item["final_score"],
            reverse=True
        )


        # ====================================================
        # DEBUG
        # ====================================================

        print(
            "\nRetrieval candidates:"
        )


        for candidate in ranked[:10]:

            print(

                f"Score: "
                f"{candidate['final_score']:.4f} | "

                f"Semantic: "
                f"{candidate['semantic_score']:.4f} | "

                f"Keyword: "
                f"{candidate['keyword_score']:.4f} | "

                f"Intent: "
                f"{candidate['intent_score']:.4f} | "

                f"Recency: "
                f"{candidate['recency_score']:.4f} | "

                f"{candidate['document'][:120]}"

            )


        # ====================================================
        # RELEVANCE GATE
        # ====================================================
        #
        # IMPORTANT:
        #
        # Recency alone can NEVER make an unrelated document
        # relevant.
        #
        # This protects negative RAG.
        #
        # ----------------------------------------------------
        #
        # Strong semantic:
        #     semantic >= 0.45
        #
        # OR meaningful keyword overlap:
        #     keyword >= 0.20
        #
        # For recent/pending queries we also allow a moderately
        # relevant document when it has both:
        #
        #     semantic >= 0.20
        #     AND
        #     (keyword >= 0.20 OR intent >= 0.09)
        #
        # ====================================================

        relevant_items = []


        for item in ranked:

            semantic = (
                item["semantic_score"]
            )

            lexical = (
                item["keyword_score"]
            )

            intent_match = (
                item["intent_score"]
            )


            # ------------------------------------------------
            # Strong semantic match
            # ------------------------------------------------

            if semantic >= 0.45:

                relevant_items.append(
                    item
                )

                continue


            # ------------------------------------------------
            # Strong keyword match
            # ------------------------------------------------

            if lexical >= 0.20:

                relevant_items.append(
                    item
                )

                continue


            # ------------------------------------------------
            # Moderate project/update relevance
            #
            # Only for the intents where recency matters.
            # ------------------------------------------------

            if intent in {
                "recent_updates",
                "pending_work",
            }:

                if (
                    semantic >= 0.20
                    and
                    (
                        lexical >= 0.20
                        or
                        intent_match >= 0.09
                    )
                ):

                    relevant_items.append(
                        item
                    )


        # ====================================================
        # REMOVE DUPLICATES
        # ====================================================

        unique_documents = []

        seen = set()


        for item in relevant_items:

            document = item[
                "document"
            ]


            normalized_document = (
                normalize_text(
                    document
                )
            )


            if normalized_document in seen:

                continue


            seen.add(
                normalized_document
            )


            unique_documents.append(
                document
            )


            if len(
                unique_documents
            ) >= n_results:

                break


        # ====================================================
        # FINAL RESULT
        # ====================================================

        print(
            f"\nRelevant documents: "
            f"{len(unique_documents)}"
        )

        print(
            f"Retrieved documents: "
            f"{len(unique_documents)}"
        )

        print(
            "================================================\n"
        )


        return unique_documents


    except Exception as e:

        print(
            f"Semantic retrieval error: {e}"
        )

        return []


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    query = input(
        "Ask a question: "
    )


    results = retrieve(
        query,
        n_results=5
    )


    print(
        "\nRetrieved Knowledge:\n"
    )


    if not results:

        print(
            "No sufficient knowledge found."
        )

    else:

        for index, result in enumerate(
            results,
            start=1
        ):

            print(
                f"\n{index}. {result}"
            )