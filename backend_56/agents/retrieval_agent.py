import re

import chromadb

from backend_56.services.embedding import generate_embedding
from backend_56.shared.config import (
    CHROMA_PATH,
    COLLECTION_NAME
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
# SOURCE ALIASES
# ============================================================

SOURCE_ALIASES = {
    "slack": "slack",
    "email": "gmail",
    "gmail": "gmail",
    "github": "github",
    "git hub": "github",
    "meeting": "meeting",
    "meetings": "meeting"
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
    "me"
}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(
    text: str
) -> str:

    return re.sub(
        r"[^a-z0-9]+",
        " ",
        str(text).lower()
    ).strip()


# ============================================================
# SOURCE DETECTION
# ============================================================

def detect_source(
    query: str
):

    normalized = normalize_text(
        query
    )

    for phrase, source in SOURCE_ALIASES.items():

        if phrase in normalized:

            return source

    return None


# ============================================================
# KEYWORD EXTRACTION
# ============================================================

def extract_keywords(
    text: str
):

    words = normalize_text(
        text
    ).split()

    return {
        word
        for word in words
        if (
            len(word) >= 3
            and word not in STOP_WORDS
            and word not in SOURCE_ALIASES
        )
    }


# ============================================================
# KEYWORD SCORE
# ============================================================

def keyword_score(
    query_keywords,
    document
):

    document_words = set(
        normalize_text(
            document
        ).split()
    )

    if not query_keywords:

        return 0.0

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
# GET ALL DOCUMENTS FROM SOURCE
# ============================================================

def get_source_documents(
    source: str
):

    try:

        results = collection.get(

            where={
                "source": source
            },

            include=[
                "documents",
                "metadatas"
            ]

        )

        return list(
            zip(
                results.get(
                    "documents",
                    []
                ),
                results.get(
                    "metadatas",
                    []
                )
            )
        )

    except Exception as e:

        print(
            f"Source retrieval error: {e}"
        )

        return []


# ============================================================
# SEMANTIC SEARCH
# ============================================================

def semantic_search(
    query_embedding,
    n_results: int
):

    try:

        results = collection.query(

            query_embeddings=[
                query_embedding
            ],

            n_results=n_results,

            include=[
                "documents",
                "metadatas",
                "distances"
            ]

        )

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]

        return list(
            zip(
                documents,
                metadatas,
                distances
            )
        )

    except Exception as e:

        print(
            f"Semantic retrieval error: {e}"
        )

        return []


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

        requested_source = detect_source(
            query
        )

        query_keywords = extract_keywords(
            query
        )


        print(
            "\nQuery analysis:"
        )

        print(
            f"Original query : {query}"
        )

        print(
            f"Detected source : "
            f"{requested_source or 'none'}"
        )

        print(
            f"Keywords       : "
            f"{sorted(query_keywords)}"
        )


        # ====================================================
        # GENERATE QUERY EMBEDDING
        # ====================================================

        query_embedding = generate_embedding(
            query
        )


        # ====================================================
        # SEMANTIC SEARCH
        # ====================================================

        total_records = collection.count()

        candidate_count = min(
            max(
                20,
                n_results * 10
            ),
            total_records
        )


        semantic_results = semantic_search(
            query_embedding,
            candidate_count
        )


        # ====================================================
        # CANDIDATE STORAGE
        # ====================================================

        candidates = {}


        # ====================================================
        # ADD SEMANTIC CANDIDATES
        # ====================================================

        for (
            document,
            metadata,
            distance
        ) in semantic_results:

            if not document:

                continue


            metadata = (
                metadata
                or {}
            )


            source = str(
                metadata.get(
                    "source",
                    ""
                )
            ).lower().strip()


            # ------------------------------------------------
            # HARD SOURCE FILTER
            # ------------------------------------------------

            if (
                requested_source
                and source != requested_source
            ):

                continue


            key = (
                document,
                str(metadata)
            )


            candidates[key] = {

                "document": document,

                "metadata": metadata,

                "distance": float(
                    distance
                ),

                "semantic_score": max(
                    0.0,
                    1.0 - float(
                        distance
                    )
                )

            }


        # ====================================================
        # ADD ALL DOCUMENTS FROM REQUESTED SOURCE
        # ====================================================

        if requested_source:

            source_documents = get_source_documents(
                requested_source
            )


            print(
                f"Source documents found: "
                f"{len(source_documents)}"
            )


            for (
                document,
                metadata
            ) in source_documents:

                if not document:

                    continue


                metadata = (
                    metadata
                    or {}
                )


                key = (
                    document,
                    str(metadata)
                )


                if key not in candidates:

                    candidates[key] = {

                        "document": document,

                        "metadata": metadata,

                        "distance": 1.0,

                        "semantic_score": 0.0

                    }


        # ====================================================
        # HYBRID RANKING
        # ====================================================

        ranked = []


        for candidate in candidates.values():

            document = candidate[
                "document"
            ]

            semantic_score = candidate[
                "semantic_score"
            ]


            lexical_score = keyword_score(
                query_keywords,
                document
            )


            final_score = (

                0.45
                * semantic_score

                +

                0.55
                * lexical_score

            )


            candidate[
                "keyword_score"
            ] = lexical_score


            candidate[
                "final_score"
            ] = final_score


            ranked.append(
                candidate
            )


        # ====================================================
        # SORT
        # ====================================================

        ranked.sort(

            key=lambda item:
                item["final_score"],

            reverse=True

        )


        # ====================================================
        # DEBUG OUTPUT
        # ====================================================

        print(
            "\nRetrieval candidates:"
        )


        for candidate in ranked:

            print(

                f"Score: "
                f"{candidate['final_score']:.4f} | "

                f"Semantic: "
                f"{candidate['semantic_score']:.4f} | "

                f"Keywords: "
                f"{candidate['keyword_score']:.4f} | "

                f"Source: "
                f"{candidate['metadata'].get('source', 'unknown')} | "

                f"{candidate['document'][:120]}"

            )


        # ====================================================
        # RELEVANCE FILTER
        # ====================================================

        retrieved = []


        if ranked:

            best_score = (
                ranked[0]["final_score"]
            )

        else:

            best_score = 0.0


        for candidate in ranked:

            score = (
                candidate["final_score"]
            )

            keyword = (
                candidate["keyword_score"]
            )

            semantic = (
                candidate["semantic_score"]
            )


            # ------------------------------------------------
            # STRONG MATCH MODE
            # ------------------------------------------------
            #
            # If the best document is very strong,
            # only keep documents reasonably close to it.
            #
            # This prevents generic documents from being
            # passed to the Answer Agent.
            # ------------------------------------------------

            if best_score >= 0.75:

                relevant = (
                    score
                    >=
                    best_score * 0.75
                )

            else:

                relevant = (
                    keyword >= 0.50
                    and
                    score >= best_score * 0.70
                )


            if not relevant:

                continue


            retrieved.append(
                candidate["document"]
            )


            if len(retrieved) >= n_results:

                break


        # ====================================================
        # FINAL RESULT
        # ====================================================

        print(
            f"\nRetrieved documents: "
            f"{len(retrieved)}"
        )


        return retrieved


    except Exception as e:

        print(
            f"Retrieval Error: {e}"
        )

        return []


# ============================================================
# TEST
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


    for i, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\n{i}. {result}"
        )