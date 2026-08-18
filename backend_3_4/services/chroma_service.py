import chromadb

from backend_3_4.config.settings import settings


class ChromaService:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name="knowledge"
        )


    def store(
        self,
        vector_id: str,
        text: str,
        embedding: list[float],
        metadata: dict | None = None
    ):

        self.collection.add(

            ids=[vector_id],

            documents=[text],

            embeddings=[embedding],

            metadatas=[
                metadata or {}
            ]

        )


    def get(
        self,
        vector_id: str
    ):

        return self.collection.get(
            ids=[vector_id]
        )


    def delete(
        self,
        vector_id: str
    ):

        self.collection.delete(
            ids=[vector_id]
        )