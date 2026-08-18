from sqlalchemy import create_engine

from backend_3_4.config.settings import settings
from backend_3_4.models import Base


DATABASE_URL = (
    f"postgresql://"
    f"{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)


def init_db():

    Base.metadata.create_all(bind=engine)

    print("Database Initialized")


if __name__ == "__main__":

    init_db()