import chromadb

from services.embedding import generate_embedding
from shared.config import CHROMA_PATH, COLLECTION_NAME

# Connect to ChromaDB
client = chromadb.PersistentClient(path=CHROMA_PATH)

# Get or create collection
collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


def retrieve(query: str, n_results: int = 3) -> dict:
    """
    Retrieve the most relevant knowledge cards from ChromaDB.

    Args:
        query (str): User query.
        n_results (int): Number of similar knowledge cards to retrieve.

    Returns:
        dict: Retrieved knowledge cards and metadata.
    """

    try:
        # Convert query to embedding
        query_embedding = generate_embedding(query)

        # Search similar vectors
        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )

        return results["documents"][0]

    except Exception as e:
        print(f"Retrieval Error: {e}")
        return {}


if __name__ == "__main__":

    user_query = "What is FastAPI?"

    results = retrieve(user_query, n_results=3)

    print(results)