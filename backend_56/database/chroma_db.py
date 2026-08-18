import chromadb
from services.embedding import generate_embedding
from shared.config import CHROMA_PATH, COLLECTION_NAME

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)



def store_knowledge_card(card_id, text, metadata=None):
    """
    Store a knowledge card in ChromaDB.
    """

    embedding = generate_embedding(text)

    collection.add(
        ids=[card_id],
        documents=[text],
        embeddings=[embedding.tolist()],
        metadatas=[metadata or {}]
    )

    print(f"Stored: {card_id}")


if __name__ == "__main__":

    store_knowledge_card(
        card_id="1",
        text="FastAPI is a modern Python web framework.",
        metadata={"source": "Documentation"}
    )