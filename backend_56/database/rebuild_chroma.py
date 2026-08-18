import chromadb

from backend_3_4.config.settings import settings
from backend_3_4.services.postgres_service import PostgresService
from backend_3_4.models import Knowledge
from backend_3_4.services.embedding_service import EmbeddingService


def main():

    # --------------------------------------------------
    # Chroma
    # --------------------------------------------------

    client = chromadb.PersistentClient(
        path=settings.CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name="knowledge"
    )


    # --------------------------------------------------
    # PostgreSQL
    # --------------------------------------------------

    postgres = PostgresService()

    session = postgres.get_session()


    embedding_service = EmbeddingService()


    try:

        records = (
            session
            .query(Knowledge)
            .all()
        )

        print(
            f"PostgreSQL records found: {len(records)}"
        )


        if not records:

            print(
                "No PostgreSQL knowledge found."
            )

            return


        stored = 0


        for record in records:

            searchable_text = (
                f"{record.title}\n"
                f"{record.summary}"
            )


            embedding = (
                embedding_service.generate(
                    searchable_text
                )
            )


            metadata = {

                "postgres_id": str(
                    record.id
                ),

                "category": (
                    record.category
                    or "Other"
                ),

                "timestamp": (
                    record.timestamp.isoformat()
                    if record.timestamp
                    else ""
                ),

                "source": (
                    getattr(
                        record,
                        "source",
                        ""
                    )
                    or ""
                )

            }


            collection.add(

                ids=[
                    record.vector_id
                ],

                documents=[
                    searchable_text
                ],

                embeddings=[
                    embedding
                ],

                metadatas=[
                    metadata
                ]

            )


            stored += 1


            print(
                f"Stored {stored}/{len(records)}: "
                f"{record.title}"
            )


        print(
            "\n======================================"
        )

        print(
            "CHROMA REBUILD COMPLETED"
        )

        print(
            "======================================"
        )

        print(
            "PostgreSQL records :",
            len(records)
        )

        print(
            "Chroma vectors     :",
            collection.count()
        )


    finally:

        session.close()


if __name__ == "__main__":

    main()