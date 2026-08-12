from sentence_transformers import SentenceTransformer
from shared.config import EMBEDDING_MODEL
# Load the embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text):
    """
    Convert text into an embedding vector.
    """
    return model.encode(text)
 
# Test the function
if __name__ == "__main__":
    sample_text = "How do I deploy FastAPI?"
    embedding = generate_embedding(sample_text)

    print("Original Text:")
    print(sample_text)

    print("\nEmbedding Dimension:", len(embedding))

    print("\nFirst 10 values:")
    print(embedding[:10])