from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime
)

from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Knowledge(Base):

    __tablename__ = "knowledge"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    summary = Column(Text, nullable=False)

    category = Column(String, nullable=False)

    confidence = Column(Float, nullable=False)

    timestamp = Column(DateTime, nullable=False)

    employee_hash = Column(String, nullable=False)

    manager_hash = Column(String, nullable=True)

    vector_id = Column(String, unique=True, nullable=False)


class IdentityMapping(Base):

    __tablename__ = "identity_mapping"

    id = Column(Integer, primary_key=True, index=True)

    employee_hash = Column(String, unique=True, nullable=False)

    employee_id = Column(String, nullable=False)

    employee_name = Column(String, nullable=True)

    manager_hash = Column(String, nullable=True)

    manager_id = Column(String, nullable=True)

    manager_name = Column(String, nullable=True)