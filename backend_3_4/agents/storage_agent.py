import uuid

from backend_3_4.shared.contracts import (
    SafeKnowledgeCard,
    StoredKnowledge
)

from backend_3_4.models import Knowledge

from backend_3_4.services.postgres_service import PostgresService
from backend_3_4.services.embedding_service import EmbeddingService
from backend_3_4.services.chroma_service import ChromaService


class StorageAgent:

    def __init__(self):

        self.postgres = PostgresService()

        self.embedding = EmbeddingService()

        self.chroma = ChromaService()

    def store(

        self,

        card: SafeKnowledgeCard,

        employee_hash: str,

        manager_hash: str | None = None

    ) -> StoredKnowledge:

        session = self.postgres.get_session()

        try:

            searchable_text = (
                f"{card.title}\n"
                f"{card.summary}"
            )

            embedding = self.embedding.generate(
                searchable_text
            )

            vector_id = str(
                uuid.uuid4()
            )

            self.chroma.store(

                vector_id=vector_id,

                text=searchable_text,

                embedding=embedding,

                metadata={
                    "source": card.source,
                    "category": card.category,
                    "timestamp": card.timestamp.isoformat()
                }

            )   

            knowledge = Knowledge(

                title=card.title,

                summary=card.summary,

                category=card.category,

                confidence=card.confidence,

                timestamp=card.timestamp,

                employee_hash=employee_hash,

                manager_hash=manager_hash,

                vector_id=vector_id

            )

            session.add(
                knowledge
            )

            session.commit()

            session.refresh(
                knowledge
            )

            return StoredKnowledge(

                postgres_id=knowledge.id,

                vector_id=vector_id,

                stored=True

            )

        except Exception:

            session.rollback()

            raise

        finally:

            session.close()