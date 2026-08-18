from datetime import datetime

from backend_3_4.models import (
    Knowledge,
    Task,
    Project,
    ProjectEmployee,
    User
)

from fastapi import (
    FastAPI,
    File,
    Form,
    UploadFile,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

import hashlib
import hmac
import secrets

# ============================================================
# AGENT 5 : ANSWER AGENT
# ============================================================

from backend_56.agents.answer_agent import generate_answer


# ============================================================
# AGENT 2 : KNOWLEDGE AGENT
# ============================================================

from Agent2.agents.knowledge_agent import KnowledgeAgent


# ============================================================
# AGENT 3 : PRIVACY AGENT
# ============================================================

from backend_3_4.agents.privacy_agent import PrivacyAgent


# ============================================================
# AGENT 4 : STORAGE AGENT
# ============================================================

from backend_3_4.agents.storage_agent import StorageAgent


# ============================================================
# CONTRACTS
# ============================================================

from Agent2.shared.contracts import RawDocument

from backend_3_4.shared.contracts import KnowledgeCard


# ============================================================
# HASHING
# ============================================================

from backend_3_4.services.hashing_service import HashingService


# ============================================================
# DATABASE
# ============================================================

from backend_3_4.services.postgres_service import PostgresService


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="AI Loss Prevention System API",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class AskRequest(BaseModel):

    question: str


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password: str) -> str:

    salt = secrets.token_bytes(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        310000
    )

    return f"{salt.hex()}:{hashed.hex()}"


def verify_password(
    password: str,
    stored_hash: str
) -> bool:

    try:

        salt_hex, hash_hex = stored_hash.split(":", 1)

        salt = bytes.fromhex(salt_hex)

        expected_hash = bytes.fromhex(hash_hex)

        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            310000
        )

        return hmac.compare_digest(
            actual_hash,
            expected_hash
        )

    except Exception:

        return False

# ============================================================
# LOGIN REQUEST
# ============================================================

class LoginRequest(BaseModel):

    identifier: str

    password: str

    role: str

# ============================================================
# LOGIN
# ============================================================

@app.post("/auth/login")
def login(request: LoginRequest):

    identifier = request.identifier.strip()
    password = request.password
    role = request.role.strip().lower()

    allowed_roles = {
        "employee",
        "manager",
        "hr"
    }

    if role not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail="Invalid role."
        )

    if not identifier or not password:
        raise HTTPException(
            status_code=400,
            detail="ID and password are required."
        )

    session = PostgresService().get_session()

    try:

        user = (
            session.query(User)
            .filter(
                User.user_id == identifier,
                User.role == role
            )
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid ID, password or role."
            )

        if user.is_active != "true":
            raise HTTPException(
                status_code=403,
                detail="This account is inactive."
            )

        if not verify_password(
            password,
            user.password_hash
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid ID, password or role."
            )

        return {
            "success": True,
            "message": "Login successful.",
            "user": {
                "id": user.user_id,
                "role": user.role,
                "name": user.display_name,
                "email": user.email
            }
        }

    except HTTPException:
        raise

    except Exception as e:

        print(f"Login Error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Unable to process login."
        )

    finally:
        session.close()

# ============================================================
# CREATE DEVELOPMENT USERS
# ============================================================

@app.post("/auth/setup")
def setup_auth_users():

    session = PostgresService().get_session()

    try:

        # Make sure users table exists
        User.__table__.create(
            bind=session.get_bind(),
            checkfirst=True
        )

        development_users = [

            {
                "user_id": "EMP001",
                "role": "employee",
                "password": "Employee@123",
                "display_name": "Employee",
                "email": "emp001@company.local"
            },

            {
                "user_id": "MANAGER001",
                "role": "manager",
                "password": "Manager@123",
                "display_name": "Manager",
                "email": "manager001@company.local"
            },

            {
                "user_id": "HR001",
                "role": "hr",
                "password": "HR@123",
                "display_name": "HR",
                "email": "hr001@company.local"
            }
        ]

        created = []

        for item in development_users:

            existing = (
                session.query(User)
                .filter(
                    User.user_id == item["user_id"]
                )
                .first()
            )

            if existing:
                continue

            user = User(
                user_id=item["user_id"],
                role=item["role"],
                password_hash=hash_password(
                    item["password"]
                ),
                display_name=item["display_name"],
                email=item["email"],
                is_active="true"
            )

            session.add(user)
            created.append(item["user_id"])

        session.commit()

        return {
            "success": True,
            "message": "Authentication users are ready.",
            "created": created
        }

    except Exception as e:

        session.rollback()

        print(
            f"Auth Setup Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to create authentication users."
        )

    finally:

        session.close()

# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "ok",
        "system": "AI Loss Prevention System"
    }


# ============================================================
# ASK ENDPOINT
# ============================================================

@app.post("/ask")
def ask(
    request: AskRequest
):

    question = request.question.strip()

    if not question:

        return {
            "answer": "No question provided."
        }

    answer = generate_answer(
        question
    )

    return {
        "question": question,
        "answer": answer
    }


# ============================================================
# MY KNOWLEDGE
# ============================================================

@app.get("/knowledge")
def get_knowledge():

    session = PostgresService().get_session()

    try:

        knowledge_records = (
            session.query(Knowledge)
            .order_by(
                Knowledge.timestamp.desc()
            )
            .all()
        )

        results = []

        for knowledge in knowledge_records:

            results.append({

                "id": knowledge.id,

                "title": knowledge.title,

                "summary": knowledge.summary,

                "category": knowledge.category,

                "confidence": knowledge.confidence,

                "timestamp": (
                    knowledge.timestamp.isoformat()
                    if knowledge.timestamp
                    else None
                )

            })

        return {
            "count": len(results),
            "knowledge": results
        }

    except Exception as e:

        print(
            f"Knowledge API Error: {e}"
        )

        return {
            "count": 0,
            "knowledge": [],
            "error": "Unable to fetch knowledge."
        }

    finally:

        session.close()


# ============================================================
# MY TASKS
# ============================================================

@app.get("/tasks")
def get_tasks(
    employee_id: str = "EMP001"
):

    session = PostgresService().get_session()

    try:

        tasks = (
            session.query(Task)
            .filter(
                Task.employee_id == employee_id
            )
            .order_by(
                Task.due_date.asc()
            )
            .all()
        )

        results = []

        for task in tasks:

            results.append({

                "id": task.id,

                "title": task.title,

                "description": task.description,

                "priority": task.priority,

                "status": task.status,

                "due_date": (
                    task.due_date.isoformat()
                    if task.due_date
                    else None
                ),

                "employee_id": task.employee_id,

                "manager_id": task.manager_id,

                "created_at": (
                    task.created_at.isoformat()
                    if task.created_at
                    else None
                )

            })

        return {
            "count": len(results),
            "tasks": results
        }

    except Exception as e:

        print(
            f"Tasks API Error: {e}"
        )

        return {
            "count": 0,
            "tasks": [],
            "error": "Unable to fetch tasks."
        }

    finally:

        session.close()


# ============================================================
# CREATE TASK
# ============================================================

@app.post("/tasks")
def create_task(

    title: str = Form(...),

    description: str = Form(""),

    priority: str = Form("Medium"),

    status: str = Form("Pending"),

    due_date: str = Form(""),

    employee_id: str = Form(...),

    manager_id: str = Form("MANAGER001")

):

    session = PostgresService().get_session()

    try:

        parsed_due_date = None

        if due_date.strip():

            parsed_due_date = datetime.fromisoformat(
                due_date
            )

        task = Task(

            title=title,

            description=description,

            priority=priority,

            status=status,

            due_date=parsed_due_date,

            employee_id=employee_id,

            manager_id=manager_id

        )

        session.add(task)

        session.commit()

        session.refresh(task)

        return {

            "success": True,

            "message": "Task created successfully.",

            "task": {

                "id": task.id,

                "title": task.title,

                "description": task.description,

                "priority": task.priority,

                "status": task.status,

                "due_date": (
                    task.due_date.isoformat()
                    if task.due_date
                    else None
                ),

                "employee_id": task.employee_id,

                "manager_id": task.manager_id

            }

        }

    except Exception as e:

        session.rollback()

        print(
            f"Create Task Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to create task."
        )

    finally:

        session.close()


# ============================================================
# MANAGER : CREATE PROJECT
# ============================================================

@app.post("/manager/projects")
def create_project(

    name: str = Form(...),

    description: str = Form(""),

    manager_id: str = Form("MANAGER001")

):

    session = PostgresService().get_session()

    try:

        # ====================================================
        # PREVENT DUPLICATE PROJECT FOR SAME MANAGER
        # ====================================================

        existing_project = (
            session.query(Project)
            .filter(
                Project.manager_id == manager_id,
                Project.name == name
            )
            .first()
        )

        if existing_project:

            raise HTTPException(
                status_code=409,
                detail=(
                    f"Project '{name}' already exists."
                )
            )

        project = Project(

            name=name,

            description=description,

            manager_id=manager_id,

            status="active"

        )

        session.add(project)

        session.commit()

        session.refresh(project)

        return {

            "success": True,

            "message": "Project created successfully.",

            "project": {

                "id": project.id,

                "name": project.name,

                "description": project.description,

                "manager_id": project.manager_id,

                "status": project.status,

                "created_at": (
                    project.created_at.isoformat()
                    if project.created_at
                    else None
                )

            }

        }

    except Exception as e:

        session.rollback()

        print(
            f"Create Project Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to create project."
        )

    finally:

        session.close()


# ============================================================
# MANAGER : GET PROJECTS
# ============================================================

@app.get("/manager/projects")
def get_manager_projects(

    manager_id: str = "MANAGER001"

):

    session = PostgresService().get_session()

    try:

        projects = (
            session.query(Project)
            .filter(
                Project.manager_id == manager_id
            )
            .order_by(
                Project.created_at.desc()
            )
            .all()
        )

        results = []

        for project in projects:

            employee_count = (
                session.query(ProjectEmployee)
                .filter(
                    ProjectEmployee.project_id == project.id
                )
                .count()
            )

            results.append({

                "id": project.id,

                "name": project.name,

                "description": project.description,

                "manager_id": project.manager_id,

                "status": project.status,

                "employee_count": employee_count,

                "created_at": (
                    project.created_at.isoformat()
                    if project.created_at
                    else None
                )

            })

        return {

            "count": len(results),

            "projects": results

        }

    except Exception as e:

        print(
            f"Get Projects Error: {e}"
        )

        return {

            "count": 0,

            "projects": [],

            "error": "Unable to fetch projects."

        }

    finally:

        session.close()


# ============================================================
# MANAGER : GET PROJECT DETAILS
# ============================================================

@app.get("/manager/projects/{project_id}")
def get_project(

    project_id: int,

    manager_id: str = "MANAGER001"

):

    session = PostgresService().get_session()

    try:

        project = (
            session.query(Project)
            .filter(
                Project.id == project_id,
                Project.manager_id == manager_id
            )
            .first()
        )

        if not project:

            raise HTTPException(
                status_code=404,
                detail="Project not found."
            )

        members = (
            session.query(ProjectEmployee)
            .filter(
                ProjectEmployee.project_id == project_id
            )
            .all()
        )

        employees = []

        for member in members:

            employees.append({

                "employee_id": member.employee_id,

                "added_at": (
                    member.added_at.isoformat()
                    if member.added_at
                    else None
                )

            })

        return {

            "project": {

                "id": project.id,

                "name": project.name,

                "description": project.description,

                "manager_id": project.manager_id,

                "status": project.status,

                "created_at": (
                    project.created_at.isoformat()
                    if project.created_at
                    else None
                ),

                "employees": employees

            }

        }

    except HTTPException:

        raise

    except Exception as e:

        print(
            f"Get Project Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch project."
        )

    finally:

        session.close()


# ============================================================
# MANAGER : ADD EMPLOYEE TO PROJECT
# ============================================================

@app.post("/manager/projects/{project_id}/employees")
def add_employee_to_project(

    project_id: int,

    employee_id: str = Form(...),

    manager_id: str = Form("MANAGER001")

):

    session = PostgresService().get_session()

    try:

        project = (
            session.query(Project)
            .filter(
                Project.id == project_id,
                Project.manager_id == manager_id
            )
            .first()
        )

        if not project:

            raise HTTPException(
                status_code=404,
                detail="Project not found."
            )

        existing_member = (
            session.query(ProjectEmployee)
            .filter(
                ProjectEmployee.project_id == project_id,
                ProjectEmployee.employee_id == employee_id
            )
            .first()
        )

        if existing_member:

            raise HTTPException(
                status_code=400,
                detail="Employee is already assigned to this project."
            )

        member = ProjectEmployee(

            project_id=project_id,

            employee_id=employee_id

        )

        session.add(member)

        session.commit()

        session.refresh(member)

        return {

            "success": True,

            "message": "Employee added to project successfully.",

            "project_id": project_id,

            "employee_id": employee_id,

            "added_at": (
                member.added_at.isoformat()
                if member.added_at
                else None
            )

        }

    except HTTPException:

        raise

    except Exception as e:

        session.rollback()

        print(
            f"Add Employee Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to add employee to project."
        )

    finally:

        session.close()

# ============================================================
# MANAGER : DELETE PROJECT
# ============================================================

@app.delete("/manager/projects/{project_id}")
def delete_manager_project(

    project_id: int,

    manager_id: str = "MANAGER001"

):

    session = PostgresService().get_session()

    try:

        # ====================================================
        # CHECK PROJECT BELONGS TO MANAGER
        # ====================================================

        project = (
            session.query(Project)
            .filter(
                Project.id == project_id,
                Project.manager_id == manager_id
            )
            .first()
        )

        if not project:

            raise HTTPException(
                status_code=404,
                detail="Project not found."
            )

        # ====================================================
        # SAFETY CHECK
        #
        # A project with employees is protected.
        # The duplicate RAG Evaluation project has 0
        # employees, so it can be safely removed.
        # ====================================================

        employee_count = (
            session.query(ProjectEmployee)
            .filter(
                ProjectEmployee.project_id == project_id
            )
            .count()
        )

        if employee_count > 0:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Project cannot be deleted because "
                    "employees are assigned to it."
                )
            )

        # ====================================================
        # DELETE EMPTY PROJECT
        # ====================================================

        project_name = project.name

        session.delete(project)

        session.commit()

        return {

            "success": True,

            "message": (
                f"Project '{project_name}' "
                "deleted successfully."
            ),

            "project_id": project_id

        }

    except HTTPException:

        session.rollback()

        raise

    except Exception as e:

        session.rollback()

        print(
            f"Delete Project Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to delete project."
        )

    finally:

        session.close()


# ============================================================
# MANAGER : TEAM OVERVIEW
# ============================================================

@app.get("/manager/overview")
def get_manager_overview(

    manager_id: str = "MANAGER001"

):

    session = PostgresService().get_session()

    try:

        # ====================================================
        # PROJECTS
        # ====================================================

        projects = (
            session.query(Project)
            .filter(
                Project.manager_id == manager_id
            )
            .all()
        )

        project_ids = [
            project.id
            for project in projects
        ]


        # ====================================================
        # TEAM MEMBERS
        # ====================================================

        team_members = 0

        if project_ids:

            team_members = (
                session.query(ProjectEmployee)
                .filter(
                    ProjectEmployee.project_id.in_(
                        project_ids
                    )
                )
                .distinct(
                    ProjectEmployee.employee_id
                )
                .count()
            )


        # ====================================================
        # TASKS
        # ====================================================

        tasks = (
            session.query(Task)
            .filter(
                Task.manager_id == manager_id
            )
            .all()
        )

        total_tasks = len(tasks)

        pending_tasks = sum(
            1
            for task in tasks
            if task.status.lower() == "pending"
        )

        completed_tasks = sum(
            1
            for task in tasks
            if task.status.lower() == "completed"
        )


        # ====================================================
        # TEAM KNOWLEDGE
        # ====================================================

        team_knowledge = 0

        employee_ids = []

        if project_ids:

            employee_ids = [
                member.employee_id
                for member in (
                    session.query(ProjectEmployee)
                    .filter(
                        ProjectEmployee.project_id.in_(project_ids)
                    )
                    .all()
                )
            ]

        employee_ids = list(set(employee_ids))

        if employee_ids:

            hasher = HashingService()

            employee_hashes = [
                hasher.hash(employee_id)
                for employee_id in employee_ids
            ]

            team_knowledge = (
                session.query(Knowledge)
                .filter(
                    Knowledge.employee_hash.in_(
                        employee_hashes
                    )
                )
                .count()
            )


        # ====================================================
        # PROJECT LIST
        # ====================================================

        projects_list = []

        for project in projects:

            employee_count = (
                session.query(ProjectEmployee)
                .filter(
                    ProjectEmployee.project_id == project.id
                )
                .count()
            )

            projects_list.append({

                "id": project.id,

                "name": project.name,

                "description": project.description,

                "status": project.status,

                "employee_count": employee_count,

                "created_at": (
                    project.created_at.isoformat()
                    if project.created_at
                    else None
                )

            })


        # ====================================================
        # RECENT TASKS
        # ====================================================

        recent_tasks = (
            session.query(Task)
            .filter(
                Task.manager_id == manager_id
            )
            .order_by(
                Task.created_at.desc()
            )
            .limit(10)
            .all()
        )

        recent_tasks_list = []

        for task in recent_tasks:

            recent_tasks_list.append({

                "id": task.id,

                "title": task.title,

                "employee_id": task.employee_id,

                "priority": task.priority,

                "status": task.status,

                "due_date": (
                    task.due_date.isoformat()
                    if task.due_date
                    else None
                ),

                "created_at": (
                    task.created_at.isoformat()
                    if task.created_at
                    else None
                )

            })


        # ====================================================
        # FINAL RESPONSE
        # ====================================================

        return {

            "manager_id": manager_id,

            "team_members": team_members,

            "projects": len(projects),

            "total_tasks": total_tasks,

            "pending_tasks": pending_tasks,

            "completed_tasks": completed_tasks,

            "team_knowledge": team_knowledge,

            "projects_list": projects_list,

            "recent_tasks": recent_tasks_list

        }


    except Exception as e:

        print(
            f"Manager Overview Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch manager overview."
        )


    finally:

        session.close()


# ============================================================
# MANAGER : TEAM KNOWLEDGE
# ============================================================

@app.get("/manager/knowledge")
def get_manager_knowledge(
    manager_id: str = "MANAGER001"
):

    session = PostgresService().get_session()

    try:

        # ----------------------------------------------------
        # GET MANAGER PROJECTS
        # ----------------------------------------------------

        projects = (
            session.query(Project)
            .filter(
                Project.manager_id == manager_id
            )
            .all()
        )

        project_ids = [
            project.id
            for project in projects
        ]

        if not project_ids:

            return {
                "manager_id": manager_id,
                "count": 0,
                "knowledge": []
            }

        # ----------------------------------------------------
        # GET TEAM EMPLOYEES
        # ----------------------------------------------------

        employee_ids = [
            member.employee_id
            for member in (
                session.query(ProjectEmployee)
                .filter(
                    ProjectEmployee.project_id.in_(
                        project_ids
                    )
                )
                .all()
            )
        ]

        employee_ids = list(
            set(employee_ids)
        )

        if not employee_ids:

            return {
                "manager_id": manager_id,
                "count": 0,
                "knowledge": []
            }

        # ----------------------------------------------------
        # HASH EMPLOYEE IDs
        # ----------------------------------------------------

        hasher = HashingService()

        employee_hashes = [
            hasher.hash(employee_id)
            for employee_id in employee_ids
        ]

        # ----------------------------------------------------
        # GET TEAM KNOWLEDGE
        # ----------------------------------------------------

        records = (
            session.query(Knowledge)
            .filter(
                Knowledge.employee_hash.in_(
                    employee_hashes
                )
            )
            .order_by(
                Knowledge.timestamp.desc()
            )
            .all()
        )

        results = []

        # ----------------------------------------------------
        # BUILD RESPONSE
        # ----------------------------------------------------

        for knowledge in records:

            results.append({

                "id": knowledge.id,

                "title": knowledge.title,

                "summary": knowledge.summary,

                "category": knowledge.category,

                "confidence": knowledge.confidence,

                "timestamp": (
                    knowledge.timestamp.isoformat()
                    if knowledge.timestamp
                    else None
                )

            })

        return {

            "manager_id": manager_id,

            "count": len(results),

            "knowledge": results

        }

    except Exception as e:

        print(
            f"Manager Knowledge Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch team knowledge."
        )

    finally:

        session.close()


# ============================================================
# MANAGER : CREATE TASK
# ============================================================

@app.post("/manager/tasks")
def manager_create_task(

    title: str = Form(...),

    description: str = Form(""),

    priority: str = Form("Medium"),

    due_date: str = Form(""),

    employee_id: str = Form(...),

    project_id: int = Form(...),

    manager_id: str = Form("MANAGER001")

):

    session = PostgresService().get_session()

    try:

        # ====================================================
        # CLEAN INPUT
        # ====================================================

        title = title.strip()

        description = description.strip()

        priority = priority.strip()

        employee_id = employee_id.strip()

        manager_id = manager_id.strip()


        # ====================================================
        # BASIC VALIDATION
        # ====================================================

        if not title:

            raise HTTPException(

                status_code=400,

                detail="Task title is required."

            )


        if not employee_id:

            raise HTTPException(

                status_code=400,

                detail="Employee ID is required."

            )


        # ====================================================
        # CHECK PROJECT BELONGS TO MANAGER
        # ====================================================

        project = (

            session.query(Project)

            .filter(

                Project.id == project_id,

                Project.manager_id == manager_id

            )

            .first()

        )


        if not project:

            raise HTTPException(

                status_code=404,

                detail="Project not found."

            )


        # ====================================================
        # CHECK EMPLOYEE BELONGS TO PROJECT
        # ====================================================

        member = (

            session.query(ProjectEmployee)

            .filter(

                ProjectEmployee.project_id == project_id,

                ProjectEmployee.employee_id == employee_id

            )

            .first()

        )


        if not member:

            raise HTTPException(

                status_code=400,

                detail=(
                    "Employee is not assigned "
                    "to this project."
                )

            )


        # ====================================================
        # CHECK DUPLICATE ACTIVE TASK
        # ====================================================
        #
        # Prevent the same manager from assigning
        # the same active task to the same employee.
        #
        # Existing completed tasks are allowed again.
        #
        # ====================================================

        existing_task = (

            session.query(Task)

            .filter(

                Task.title == title,

                Task.employee_id == employee_id,

                Task.manager_id == manager_id,

                Task.status.in_([

                    "Pending",

                    "pending",

                    "In Progress",

                    "in progress"

                ])

            )

            .first()

        )


        if existing_task:

            raise HTTPException(

                status_code=409,

                detail=(
                    f"Task '{title}' is already "
                    f"assigned to {employee_id}."
                )

            )


        # ====================================================
        # PARSE DUE DATE
        # ====================================================

        parsed_due_date = None


        if due_date.strip():

            try:

                parsed_due_date = (
                    datetime.fromisoformat(
                        due_date
                    )
                )

            except ValueError:

                raise HTTPException(

                    status_code=400,

                    detail=(
                        "Invalid due date format."
                    )

                )


        # ====================================================
        # CREATE TASK
        # ====================================================

        task = Task(

            title=title,

            description=description,

            priority=priority,

            status="Pending",

            due_date=parsed_due_date,

            employee_id=employee_id,

            manager_id=manager_id

        )


        session.add(task)

        session.commit()

        session.refresh(task)


        # ====================================================
        # SUCCESS RESPONSE
        # ====================================================

        return {

            "success": True,

            "message": "Task assigned successfully.",

            "task": {

                "id": task.id,

                "title": task.title,

                "description": task.description,

                "priority": task.priority,

                "status": task.status,

                "due_date": (

                    task.due_date.isoformat()

                    if task.due_date

                    else None

                ),

                "employee_id": task.employee_id,

                "manager_id": task.manager_id,

                "project_id": project_id

            }

        }


    # ========================================================
    # HTTP EXCEPTIONS
    # ========================================================

    except HTTPException:

        session.rollback()

        raise


    # ========================================================
    # UNEXPECTED ERROR
    # ========================================================

    except Exception as e:

        session.rollback()

        print(
            f"Manager Create Task Error: {e}"
        )

        raise HTTPException(

            status_code=500,

            detail="Unable to assign task."

        )


    # ========================================================
    # CLOSE SESSION
    # ========================================================

    finally:

        session.close()

# ============================================================
# MANAGER : GET TEAM TASKS
# ============================================================

@app.get("/manager/tasks")
def get_manager_tasks(

    manager_id: str = "MANAGER001"

):

    session = PostgresService().get_session()

    try:

        tasks = (
            session.query(Task)
            .filter(
                Task.manager_id == manager_id
            )
            .order_by(
                Task.created_at.desc()
            )
            .all()
        )


        results = []


        for task in tasks:

            results.append({

                "id": task.id,

                "title": task.title,

                "description": task.description,

                "priority": task.priority,

                "status": task.status,

                "due_date": (
                    task.due_date.isoformat()
                    if task.due_date
                    else None
                ),

                "employee_id": task.employee_id,

                "manager_id": task.manager_id,

                "created_at": (
                    task.created_at.isoformat()
                    if task.created_at
                    else None
                )

            })


        return {

            "count": len(results),

            "tasks": results

        }


    except Exception as e:

        print(
            f"Manager Tasks Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch team tasks."
        )


    finally:

        session.close()

# ============================================================
# MANAGER : TEAM ACTIVITY
# ============================================================

@app.get("/manager/activity")
def get_manager_activity(
    manager_id: str = "MANAGER001"
):

    session = PostgresService().get_session()

    try:

        activities = []

        # ====================================================
        # MANAGER PROJECTS
        # ====================================================

        projects = (
            session.query(Project)
            .filter(
                Project.manager_id == manager_id
            )
            .all()
        )

        project_ids = [
            project.id
            for project in projects
        ]

        # ====================================================
        # PROJECT ACTIVITY
        # ====================================================

        for project in projects:

            activities.append({

                "type": "project",

                "title": "Project created",

                "description": (
                    f"{project.name} project was created."
                ),

                "project_name": project.name,

                "employee_id": None,

                "timestamp": (
                    project.created_at.isoformat()
                    if project.created_at
                    else None
                )

            })

        # ====================================================
        # EMPLOYEE PROJECT MEMBERSHIP
        # ====================================================

        if project_ids:

            members = (
                session.query(ProjectEmployee)
                .filter(
                    ProjectEmployee.project_id.in_(
                        project_ids
                    )
                )
                .all()
            )

            project_name_map = {
                project.id: project.name
                for project in projects
            }

            for member in members:

                activities.append({

                    "type": "employee",

                    "title": "Employee added",

                    "description": (
                        f"{member.employee_id} "
                        f"was added to "
                        f"{project_name_map.get(member.project_id, 'project')}."
                    ),

                    "project_name": (
                        project_name_map.get(
                            member.project_id
                        )
                    ),

                    "employee_id": member.employee_id,

                    "timestamp": (
                        member.added_at.isoformat()
                        if member.added_at
                        else None
                    )

                })

        # ====================================================
        # TASK ACTIVITY
        # ====================================================

        tasks = (
            session.query(Task)
            .filter(
                Task.manager_id == manager_id
            )
            .all()
        )

        for task in tasks:

            activities.append({

                "type": "task",

                "title": "Task assigned",

                "description": (
                    f"{task.title} assigned to "
                    f"{task.employee_id}."
                ),

                "project_name": None,

                "employee_id": task.employee_id,

                "status": task.status,

                "priority": task.priority,

                "timestamp": (
                    task.created_at.isoformat()
                    if task.created_at
                    else None
                )

            })

        # ====================================================
        # TEAM KNOWLEDGE ACTIVITY
        # ====================================================

        employee_ids = []

        if project_ids:

            employee_ids = list(set([
                member.employee_id
                for member in (
                    session.query(ProjectEmployee)
                    .filter(
                        ProjectEmployee.project_id.in_(
                            project_ids
                        )
                    )
                    .all()
                )
            ]))

        if employee_ids:

            hasher = HashingService()

            employee_hashes = [
                hasher.hash(employee_id)
                for employee_id in employee_ids
            ]

            knowledge_records = (
                session.query(Knowledge)
                .filter(
                    Knowledge.employee_hash.in_(
                        employee_hashes
                    )
                )
                .all()
            )

            hash_to_employee = dict(
                zip(
                    employee_hashes,
                    employee_ids
                )
            )

            for knowledge in knowledge_records:

                activities.append({

                    "type": "knowledge",

                    "title": "Knowledge added",

                    "description": (
                        f"{knowledge.title} "
                        "was added to team knowledge."
                    ),

                    "project_name": None,

                    "employee_id": (
                        hash_to_employee.get(
                            knowledge.employee_hash
                        )
                    ),

                    "category": knowledge.category,

                    "timestamp": (
                        knowledge.timestamp.isoformat()
                        if knowledge.timestamp
                        else None
                    )

                })

        # ====================================================
        # SORT NEWEST FIRST
        # ====================================================

        activities.sort(
            key=lambda item: (
                item.get("timestamp") or ""
            ),
            reverse=True
        )

        # ====================================================
        # LIMIT
        # ====================================================

        activities = activities[:30]

        return {

            "manager_id": manager_id,

            "count": len(activities),

            "activities": activities

        }

    except Exception as e:

        print(
            f"Manager Activity Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch team activity."
        )

    finally:

        session.close()

# ============================================================
# HR : ORGANIZATION OVERVIEW
# ============================================================

@app.get("/hr/overview")
def get_hr_overview():

    session = PostgresService().get_session()

    try:

        # ====================================================
        # PROJECTS
        # ====================================================

        projects = (
            session.query(Project)
            .order_by(
                Project.created_at.desc()
            )
            .all()
        )

        project_ids = [
            project.id
            for project in projects
        ]


        # ====================================================
        # EMPLOYEES
        # ====================================================

        employee_rows = []

        if project_ids:

            employee_rows = (
                session.query(ProjectEmployee.employee_id)
                .filter(
                    ProjectEmployee.project_id.in_(
                        project_ids
                    )
                )
                .all()
            )

        employee_ids = list(
            set(
                row[0]
                for row in employee_rows
            )
        )


        # ====================================================
        # TASKS
        # ====================================================

        tasks = (
            session.query(Task)
            .all()
        )

        total_tasks = len(tasks)

        pending_tasks = sum(
            1
            for task in tasks
            if (task.status or "").lower()
            == "pending"
        )

        completed_tasks = sum(
            1
            for task in tasks
            if (task.status or "").lower()
            == "completed"
        )


        # ====================================================
        # KNOWLEDGE
        # ====================================================

        team_knowledge = 0

        if employee_ids:

            hasher = HashingService()

            employee_hashes = [
                hasher.hash(employee_id)
                for employee_id in employee_ids
            ]

            team_knowledge = (
                session.query(Knowledge)
                .filter(
                    Knowledge.employee_hash.in_(
                        employee_hashes
                    )
                )
                .count()
            )


        # ====================================================
        # PROJECT SUMMARY
        # ====================================================

        project_list = []

        for project in projects:

            employee_count = (
                session.query(ProjectEmployee)
                .filter(
                    ProjectEmployee.project_id
                    == project.id
                )
                .count()
            )

            project_list.append({

                "id": project.id,

                "name": project.name,

                "description": project.description,

                "manager_id": project.manager_id,

                "status": project.status,

                "employee_count":
                    employee_count,

                "created_at": (
                    project.created_at.isoformat()
                    if project.created_at
                    else None
                )

            })


        # ====================================================
        # RESPONSE
        # ====================================================

        return {

            "total_employees":
                len(employee_ids),

            "total_projects":
                len(projects),

            "total_tasks":
                total_tasks,

            "pending_tasks":
                pending_tasks,

            "completed_tasks":
                completed_tasks,

            "team_knowledge":
                team_knowledge,

            "projects":
                project_list

        }


    except Exception as e:

        print(
            f"HR Overview Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch HR overview."
        )


    finally:

        session.close()


# ============================================================
# HR : EMPLOYEES
# ============================================================

@app.get("/hr/employees")
def get_hr_employees():

    session = PostgresService().get_session()

    try:

        projects = (
            session.query(Project)
            .all()
        )

        project_ids = [
            project.id
            for project in projects
        ]

        project_map = {
            project.id: project
            for project in projects
        }


        # ====================================================
        # PROJECT MEMBERS
        # ====================================================

        members = []

        if project_ids:

            members = (
                session.query(ProjectEmployee)
                .filter(
                    ProjectEmployee.project_id.in_(
                        project_ids
                    )
                )
                .all()
            )


        # ====================================================
        # BUILD EMPLOYEE MAP
        # ====================================================

        employee_map = {}

        for member in members:

            employee_id = member.employee_id

            if employee_id not in employee_map:

                employee_map[employee_id] = {

                    "employee_id":
                        employee_id,

                    "projects": [],

                    "project_count":
                        0,

                    "task_count":
                        0,

                    "pending_tasks":
                        0,

                    "completed_tasks":
                        0,

                    "knowledge_count":
                        0

                }


            project = project_map.get(
                member.project_id
            )

            if project:

                employee_map[
                    employee_id
                ]["projects"].append({

                    "id":
                        project.id,

                    "name":
                        project.name,

                    "status":
                        project.status

                })


        # ====================================================
        # TASK COUNTS
        # ====================================================

        tasks = (
            session.query(Task)
            .all()
        )

        for task in tasks:

            employee_id = task.employee_id

            if employee_id not in employee_map:

                employee_map[employee_id] = {

                    "employee_id":
                        employee_id,

                    "projects": [],

                    "project_count":
                        0,

                    "task_count":
                        0,

                    "pending_tasks":
                        0,

                    "completed_tasks":
                        0,

                    "knowledge_count":
                        0

                }


            employee_map[
                employee_id
            ]["task_count"] += 1


            status = (
                task.status or ""
            ).lower()


            if status == "pending":

                employee_map[
                    employee_id
                ]["pending_tasks"] += 1


            if status == "completed":

                employee_map[
                    employee_id
                ]["completed_tasks"] += 1


        # ====================================================
        # KNOWLEDGE COUNTS
        # ====================================================

        hasher = HashingService()

        for employee_id in employee_map:

            employee_hash = hasher.hash(
                employee_id
            )

            employee_map[
                employee_id
            ]["knowledge_count"] = (
                session.query(Knowledge)
                .filter(
                    Knowledge.employee_hash
                    == employee_hash
                )
                .count()
            )


            employee_map[
                employee_id
            ]["project_count"] = len(
                employee_map[
                    employee_id
                ]["projects"]
            )


        # ====================================================
        # RESPONSE
        # ====================================================

        employees = list(
            employee_map.values()
        )

        employees.sort(
            key=lambda employee:
                employee["employee_id"]
        )


        return {

            "count":
                len(employees),

            "employees":
                employees

        }


    except Exception as e:

        print(
            f"HR Employees Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch employees."
        )


    finally:

        session.close()


# ============================================================
# HR : ALL PROJECTS
# ============================================================

@app.get("/hr/projects")
def get_hr_projects():

    session = PostgresService().get_session()

    try:

        projects = (
            session.query(Project)
            .order_by(
                Project.created_at.desc()
            )
            .all()
        )

        results = []


        for project in projects:

            members = (
                session.query(ProjectEmployee)
                .filter(
                    ProjectEmployee.project_id
                    == project.id
                )
                .all()
            )


            tasks = (
                session.query(Task)
                .filter(
                    Task.manager_id
                    == project.manager_id
                )
                .all()
            )


            results.append({

                "id":
                    project.id,

                "name":
                    project.name,

                "description":
                    project.description,

                "manager_id":
                    project.manager_id,

                "status":
                    project.status,

                "employee_count":
                    len(members),

                "employees": [
                    member.employee_id
                    for member in members
                ],

                "task_count":
                    len(tasks),

                "created_at": (
                    project.created_at.isoformat()
                    if project.created_at
                    else None
                )

            })


        return {

            "count":
                len(results),

            "projects":
                results

        }


    except Exception as e:

        print(
            f"HR Projects Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch HR projects."
        )


    finally:

        session.close()


# ============================================================
# HR : ALL TASKS
# ============================================================

@app.get("/hr/tasks")
def get_hr_tasks():

    session = PostgresService().get_session()

    try:

        tasks = (
            session.query(Task)
            .order_by(
                Task.created_at.desc()
            )
            .all()
        )

        results = []


        for task in tasks:

            results.append({

                "id":
                    task.id,

                "title":
                    task.title,

                "description":
                    task.description,

                "priority":
                    task.priority,

                "status":
                    task.status,

                "employee_id":
                    task.employee_id,

                "manager_id":
                    task.manager_id,

                "due_date": (
                    task.due_date.isoformat()
                    if task.due_date
                    else None
                ),

                "created_at": (
                    task.created_at.isoformat()
                    if task.created_at
                    else None
                )

            })


        return {

            "count":
                len(results),

            "tasks":
                results

        }


    except Exception as e:

        print(
            f"HR Tasks Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch HR tasks."
        )


    finally:

        session.close()


# ============================================================
# HR : RECENT ACTIVITY
# ============================================================

@app.get("/hr/activity")
def get_hr_activity():

    session = PostgresService().get_session()

    try:

        activities = []


        # ====================================================
        # PROJECTS
        # ====================================================

        projects = (
            session.query(Project)
            .all()
        )

        for project in projects:

            activities.append({

                "type":
                    "project",

                "title":
                    "Project created",

                "description":
                    f"{project.name} project was created.",

                "timestamp": (
                    project.created_at.isoformat()
                    if project.created_at
                    else None
                )

            })


        # ====================================================
        # EMPLOYEES
        # ====================================================

        members = (
            session.query(ProjectEmployee)
            .all()
        )

        project_map = {
            project.id:
                project.name
            for project in projects
        }


        for member in members:

            activities.append({

                "type":
                    "employee",

                "title":
                    "Employee added",

                "description":
                    (
                        f"{member.employee_id} "
                        f"was added to "
                        f"{project_map.get(member.project_id, 'project')}."
                    ),

                "employee_id":
                    member.employee_id,

                "timestamp": (
                    member.added_at.isoformat()
                    if member.added_at
                    else None
                )

            })


        # ====================================================
        # TASKS
        # ====================================================

        tasks = (
            session.query(Task)
            .all()
        )

        for task in tasks:

            activities.append({

                "type":
                    "task",

                "title":
                    "Task assigned",

                "description":
                    (
                        f"{task.title} "
                        f"assigned to "
                        f"{task.employee_id}."
                    ),

                "employee_id":
                    task.employee_id,

                "status":
                    task.status,

                "priority":
                    task.priority,

                "timestamp": (
                    task.created_at.isoformat()
                    if task.created_at
                    else None
                )

            })


        # ====================================================
        # SORT
        # ====================================================

        activities.sort(
            key=lambda item:
                item.get("timestamp") or "",
            reverse=True
        )


        return {

            "count":
                len(activities),

            "activities":
                activities[:50]

        }


    except Exception as e:

        print(
            f"HR Activity Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch HR activity."
        )


    finally:

        session.close()


# ============================================================
# UPLOAD KNOWLEDGE
# ============================================================

@app.post("/upload")
async def upload_knowledge(

    file: UploadFile = File(...),

    employee_id: str = Form(...),

    employee_name: str = Form(...),

    department: str = Form(...)

):

    # ========================================================
    # VALIDATE FILE
    # ========================================================

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    # --------------------------------------------------------
    # Currently support TXT only
    # --------------------------------------------------------

    if not file.filename.lower().endswith(".txt"):

        raise HTTPException(
            status_code=400,
            detail="Only .txt files are supported currently."
        )

    # ========================================================
    # READ FILE
    # ========================================================

    try:

        file_bytes = await file.read()

        content = file_bytes.decode(
            "utf-8"
        )

    except UnicodeDecodeError:

        raise HTTPException(
            status_code=400,
            detail="Unable to read file. Please upload a UTF-8 text file."
        )

    if not content.strip():

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # ========================================================
    # CREATE RAW DOCUMENT
    # ========================================================

    timestamp = datetime.now()

    raw_document = RawDocument(

        source="employee_upload",

        employee_name=employee_name,

        employee_id=employee_id,

        department=department,

        timestamp=timestamp,

        url=file.filename,

        content=content

    )

    print(
        "\n=================================================="
    )

    print(
        "EMPLOYEE KNOWLEDGE UPLOAD"
    )

    print(
        "=================================================="
    )

    print(
        f"File       : {file.filename}"
    )

    print(
        f"Employee   : {employee_name}"
    )

    print(
        f"Employee ID: {employee_id}"
    )

    # ========================================================
    # AGENT 2 : KNOWLEDGE EXTRACTION
    # ========================================================

    try:

        knowledge_agent = KnowledgeAgent()

        extracted_cards = (
            knowledge_agent.extract(
                raw_document
            )
        )

    except Exception as e:

        print(
            f"Knowledge Extraction Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Knowledge extraction failed."
        )

    # ========================================================
    # NO KNOWLEDGE FOUND
    # ========================================================

    if not extracted_cards:

        return {

            "success": False,

            "message": (
                "No valuable knowledge was found "
                "in the uploaded document."
            ),

            "file": file.filename,

            "stored": 0

        }

    # ========================================================
    # AGENT 3 : PRIVACY
    # ========================================================

    privacy_agent = PrivacyAgent()

    # ========================================================
    # AGENT 4 : STORAGE
    # ========================================================

    storage_agent = StorageAgent()

    # ========================================================
    # HASH EMPLOYEE ID
    # ========================================================

    hasher = HashingService()

    employee_hash = hasher.hash(
        employee_id
    )

    stored_items = []

    # ========================================================
    # PROCESS EACH KNOWLEDGE CARD
    # ========================================================

    for extracted_card in extracted_cards:

        try:

            # ------------------------------------------------
            # CONVERT Agent2 KnowledgeCard
            # INTO backend_3_4 KnowledgeCard
            # ------------------------------------------------

            knowledge_card = KnowledgeCard(

                title=extracted_card.title,

                summary=extracted_card.summary,

                category=extracted_card.category,

                confidence=extracted_card.confidence,

                source=extracted_card.source,

                employee_id=extracted_card.employee_id,

                timestamp=extracted_card.timestamp

            )

            # ------------------------------------------------
            # PRIVACY AGENT
            # ------------------------------------------------

            safe_card = privacy_agent.process(
                knowledge_card
            )

            # ------------------------------------------------
            # STORAGE AGENT
            #
            # SafeKnowledgeCard goes to:
            # PostgreSQL + Chroma
            #
            # Therefore raw PII does NOT enter RAG storage.
            # ------------------------------------------------

            stored = storage_agent.store(

                card=safe_card,

                employee_hash=employee_hash

            )

            stored_items.append({

                "title": safe_card.title,

                "postgres_id": stored.postgres_id,

                "vector_id": stored.vector_id,

                "stored": stored.stored

            })

        except Exception as e:

            print(
                f"Knowledge Storage Error: {e}"
            )

            continue

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    successful_count = len(
        stored_items
    )

    print(
        "\n=================================================="
    )

    print(
        "UPLOAD COMPLETED"
    )

    print(
        f"Knowledge Cards : {successful_count}"
    )

    print(
        "=================================================="
    )

    return {

        "success": successful_count > 0,

        "message": (
            "Knowledge uploaded and processed successfully."
            if successful_count > 0
            else "No knowledge cards could be stored."
        ),

        "file": file.filename,

        "stored": successful_count,

        "items": stored_items

    }