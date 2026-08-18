from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    ForeignKey
)
from datetime import datetime

from sqlalchemy.orm import declarative_base


Base = declarative_base()


# ============================================================
# KNOWLEDGE
# ============================================================

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


# ============================================================
# TASK
# ============================================================

class Task(Base):

    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    priority = Column(
        String,
        nullable=False,
        default="Medium"
    )

    status = Column(
        String,
        nullable=False,
        default="Pending"
    )

    due_date = Column(
        DateTime,
        nullable=True
    )

    employee_id = Column(
        String,
        nullable=False
    )

    manager_id = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )


# ============================================================
# IDENTITY MAPPING
# ============================================================

class IdentityMapping(Base):

    __tablename__ = "identity_mapping"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    employee_hash = Column(
        String,
        unique=True,
        nullable=False
    )

    employee_id = Column(
        String,
        nullable=False
    )

    employee_name = Column(
        String,
        nullable=True
    )

    manager_hash = Column(
        String,
        nullable=True
    )

    manager_id = Column(
        String,
        nullable=True
    )

    manager_name = Column(
        String,
        nullable=True
    )


# ============================================================
# PROJECT
# ============================================================

class Project(Base):

    __tablename__ = "projects"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    manager_id = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="active"
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )


# ============================================================
# PROJECT EMPLOYEE
# ============================================================

class ProjectEmployee(Base):

    __tablename__ = "project_employees"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    employee_id = Column(
        String,
        nullable=False
    )

    added_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
# ============================================================
# USER / AUTHENTICATION
# ============================================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    role = Column(
        String,
        nullable=False
    )

    password_hash = Column(
        String,
        nullable=False
    )

    display_name = Column(
        String,
        nullable=True
    )

    email = Column(
        String,
        nullable=True,
        unique=True
    )

    is_active = Column(
        String,
        nullable=False,
        default="true"
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )