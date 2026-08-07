from sentence_transformers import SentenceTransformer

from config.settings import settings


class EmbeddingService:

    def __init__(self):

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

    def generate(
        self,
        text: str
    ) -> list[float]:

        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()