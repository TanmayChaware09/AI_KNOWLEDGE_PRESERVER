from backend_3_4.services.embedding_service import EmbeddingService


# Load the same embedding model used by Agent 4
_embedding_service = EmbeddingService()


def generate_embedding(text: str) -> list[float]:
    """
    Generate an embedding using the same
    embedding service used by Agent 4.
    """

    return _embedding_service.generate(text)


# Test
if __name__ == "__main__":

    sample_text = "How do I deploy FastAPI?"

    embedding = generate_embedding(
        sample_text
    )

    print("Original Text:")
    print(sample_text)

    print(
        "\nEmbedding Dimension:",
        len(embedding)
    )

    print("\nFirst 10 values:")
    print(embedding[:10])