🛡️ AI Loss Prevention System

An AI-powered enterprise knowledge, privacy, and loss-prevention platform designed to protect organizational intelligence while making it accessible to authorized employees, managers, and HR teams.

📌 Table of Contents

Overview

Problem Statement

Solution

Core Objectives

Key Features

System Architecture

Application Flow

Role-Based Access

Employee Dashboard

Manager Dashboard

HR Dashboard

Knowledge System

RAG Pipeline

Privacy & Loss Prevention

AI Assistant

Data Sources

Authentication

Backend Architecture

Frontend Architecture

Project Structure

Technology Stack

Database Design

API Overview

Security Design

Negative RAG / Hallucination Prevention

Current Project Status

Future Enhancements

Installation

Running the Project

Development Credentials

Testing

GitHub Workflow

Production Considerations

Contributing

License

🚀 Overview

The AI Loss Prevention System is an enterprise-focused AI platform designed to reduce the loss of valuable organizational knowledge and prevent sensitive information from being unnecessarily exposed to AI systems.

Modern organizations generate huge amounts of knowledge through:

GitHub repositories

Slack conversations

Emails

Meetings

Project documentation

Tasks

Internal knowledge bases

Employee discussions

Technical decisions

A large portion of this information becomes difficult to discover, disconnected across tools, or unavailable when employees leave the organization.

At the same time, sending raw enterprise information directly into AI systems can introduce privacy and security risks.

This project combines:

Knowledge Preservation + Privacy Protection + Role-Based Access + RAG + AI Assistance

into a single platform.

🎯 Problem Statement

Organizations continuously create valuable knowledge, but that knowledge is often fragmented.

For example:

GitHub
   ├── Code
   ├── Pull Requests
   └── Technical Decisions

Slack
   ├── Discussions
   ├── Decisions
   └── Problem Solving

Email
   ├── Communication
   ├── Approvals
   └── Decisions

Meetings
   ├── Conversations
   ├── Decisions
   └── Action Items

This creates several problems.

1. Knowledge Loss

When employees leave or projects change teams, important knowledge can disappear.

2. Knowledge Fragmentation

Information is spread across multiple platforms.

3. Search Difficulty

Employees may know that information exists but not where it is stored.

4. Privacy Risk

Enterprise information may contain:

Personal information

Emails

Phone numbers

Credentials

Internal identifiers

Sensitive business information

5. AI Hallucination

If an AI system does not have sufficient evidence, it may generate an answer that sounds correct but is unsupported.

The AI Loss Prevention System addresses these challenges through a controlled knowledge pipeline.

💡 Solution

The system collects organizational knowledge, processes it through privacy-aware components, stores it in searchable representations, and allows authorized users to retrieve information through dashboards and an AI assistant.

High-level flow:

                    ORGANIZATIONAL DATA
                           │
          ┌────────────────┼────────────────┐
          │                │                │
       GitHub           Slack            Email
          │                │                │
          └────────────────┼────────────────┘
                           │
                        Meetings
                           │
                           ▼
                    Data Ingestion
                           │
                           ▼
                 Privacy / PII Layer
                           │
                           ▼
                    Knowledge Storage
                           │
                           ▼
                  Embedding / Vector DB
                           │
                           ▼
                       Retrieval
                           │
                    Permission Check
                           │
                           ▼
                    AI / RAG Layer
                           │
             ┌─────────────┼─────────────┐
             │             │             │
         Employee       Manager          HR
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                      AI Assistant

🎯 Core Objectives

The project focuses on five major objectives.

1. Preserve Organizational Knowledge

Convert scattered organizational information into structured, searchable knowledge.

2. Prevent Sensitive Information Leakage

Detect and protect sensitive information before it reaches downstream AI components.

3. Provide Role-Based Access

Different users should see only information appropriate for their role.

4. Enable Grounded AI Answers

Use retrieval-based AI instead of relying only on the language model's internal knowledge.

5. Prevent Unsupported Answers

If sufficient knowledge is not available, the system should avoid inventing an answer.

✨ Key Features

🔐 Authentication

Employee login

Manager login

HR login

Password verification

Role validation

Secure password hashing

👥 Role-Based Dashboards

Dedicated interfaces for:

Employees

Managers

HR

📊 Project Management

Projects

Project members

Project status

Project employee counts

📋 Task Management

Task assignment

Task status

Priority

Due dates

Employee ownership

Manager ownership

🧠 Knowledge Management

Organizational knowledge

Knowledge categories

Confidence scores

Knowledge timestamps

Vector references

Employee/manager associations

🤖 AI Assistant

Natural-language questions

Knowledge retrieval

Context-based responses

Role-aware access

🛡️ Privacy Layer

PII detection

Anonymization

Hashing

Sensitive-data protection

🔎 RAG

Embedding generation

Vector storage

Similarity retrieval

Context injection

Grounded answering

📈 Activity Tracking

The system can surface activities such as:

Project creation

Employee assignment

Task assignment

Task updates

🏗️ System Architecture

The project is organized into multiple logical layers.

┌─────────────────────────────────────────────────────┐
│                    FRONTEND                         │
│                                                     │
│ Landing → Role Selection → Login → Dashboards      │
│                                                     │
│ Employee | Manager | HR                             │
└───────────────────────┬─────────────────────────────┘
                        │
                        │ HTTP / REST
                        ▼
┌─────────────────────────────────────────────────────┐
│                    API LAYER                        │
│                                                     │
│ Authentication                                      │
│ Employee APIs                                       │
│ Manager APIs                                        │
│ HR APIs                                             │
│ Knowledge APIs                                      │
│ Task APIs                                           │
│ Project APIs                                        │
│ AI / RAG APIs                                       │
└───────────────┬─────────────────┬───────────────────┘
                │                 │
                ▼                 ▼
       ┌────────────────┐   ┌────────────────┐
       │ PostgreSQL     │   │ Vector Store   │
       │                │   │                │
       │ Users          │   │ Embeddings     │
       │ Projects       │   │ Retrieval      │
       │ Tasks          │   │ RAG            │
       │ Knowledge      │   │                │
       └────────────────┘   └────────────────┘
                │                 │
                └────────┬────────┘
                         ▼
                ┌─────────────────┐
                │ AI / Agent Layer │
                │                 │
                │ Retrieval Agent │
                │ Answer Agent    │
                │ Knowledge Agent │
                │ Privacy Agent   │
                └─────────────────┘

🔄 Application Flow

1. Landing Page

The user first sees the system introduction.

/
│
├── Product introduction
├── Security information
├── AI capabilities
└── Get Started

2. Role Selection

The user selects:

Employee
Manager
HR

3. Login

The selected role determines the authentication context.

Example:

{
  "identifier": "EMP001",
  "password": "********",
  "role": "employee"
}

4. Authentication

The backend validates:

User ID
   +
Role
   +
Password

5. Dashboard

After successful authentication, the user reaches the appropriate dashboard.

👥 Role-Based Access

👨‍💻 Employee

Employees can work with their authorized:

Projects

Tasks

Knowledge

Activity

AI assistant

👔 Manager

Managers can work with:

Employees

Projects

Tasks

Team activity

Team knowledge

AI assistant

🧑‍💼 HR

HR receives organization-level functionality such as:

Employee overview

Project overview

Task overview

Organization activity

Knowledge overview

AI assistant

👨‍💻 Employee Dashboard

The employee dashboard provides a personalized view of the employee's work.

Typical information includes:

Employee
│
├── Projects
├── Tasks
├── Pending Tasks
├── Completed Tasks
├── Knowledge
└── AI Assistant

The dashboard uses backend APIs to retrieve employee-specific information.

👔 Manager Dashboard

The manager dashboard provides team-level visibility.

Manager
│
├── Total Employees
├── Projects
├── Tasks
├── Pending Tasks
├── Completed Tasks
├── Team Knowledge
└── Recent Activity

Managers can view project and task relationships across their team.

🧑‍💼 HR Dashboard

The HR dashboard provides a higher-level organizational overview.

It can surface:

Total employees

Total projects

Total tasks

Pending tasks

Completed tasks

Team knowledge

Recent organizational activity

Example overview:

{
  "total_employees": 1,
  "total_projects": 2,
  "total_tasks": 4,
  "pending_tasks": 4,
  "completed_tasks": 0,
  "team_knowledge": 6
}

🧠 Knowledge System

The knowledge system is one of the central components of the platform.

Knowledge records contain fields such as:

ID
Title
Summary
Category
Confidence
Timestamp
Employee Hash
Manager Hash
Vector ID

This allows knowledge to be associated with:

People

Projects

Categories

Time

Confidence

Vector representations

🔎 RAG Pipeline

The Retrieval-Augmented Generation pipeline follows:

User Question
      │
      ▼
Query Processing
      │
      ▼
Embedding Generation
      │
      ▼
Vector Similarity Search
      │
      ▼
Relevant Knowledge
      │
      ▼
Permission / Privacy Filtering
      │
      ▼
Context Construction
      │
      ▼
Answer Generation
      │
      ▼
Grounded Answer

The key principle is:

The AI should answer using available organizational evidence rather than inventing information.

🚫 Negative RAG / Hallucination Prevention

A major evaluation scenario is when the user asks something that does not exist in the knowledge base.

Example:

Question:
"What was the decision regarding a technology that is not present
in our organizational knowledge?"

The expected behavior is:

No sufficient knowledge found.

rather than:

The team decided X because...

This makes the assistant more trustworthy for enterprise usage.

🛡️ Privacy & Loss Prevention

The privacy layer is designed to prevent unnecessary exposure of sensitive information.

Conceptually:

Raw Data
   │
   ▼
PII Detection
   │
   ▼
Sensitive Entity Identification
   │
   ▼
Anonymization / Hashing
   │
   ▼
Safe Knowledge Representation
   │
   ▼
Vector / Database Storage

The project contains privacy-oriented components such as:

PII detector

Presidio integration

Anonymizer

Hashing service

Entity merger

Privacy agent

Storage agent

🤖 AI Assistant

The AI assistant is designed as the natural-language interface to organizational knowledge.

Example:

User:
"Why was PostgreSQL retained instead of MongoDB?"

Pipeline:

Question
   ↓
Retrieval Agent
   ↓
Relevant organizational documents
   ↓
Context
   ↓
Answer Agent
   ↓
Grounded response

If the system does not have enough relevant evidence:

No sufficient knowledge found.

📥 Data Sources

The project contains collectors/connectors for organizational sources.

GitHub

Used for organizational technical knowledge such as:

Code-related information

Repository knowledge

Technical context

Slack

Used for organizational discussions and decisions.

Email

Used for relevant organizational communication.

Meetings

The meeting pipeline includes components for:

Meeting recordings

Transcripts

Speaker mapping

Knowledge extraction

Meeting summaries

Raw document generation

Google Drive

The project also contains a Google Drive connector.

🔐 Authentication

The current development authentication system uses:

User ID
Password
Role

Development users:

Role

ID

Employee

EMP001

Manager

MANAGER001

HR

HR001

Passwords are stored as password hashes rather than plaintext values.

The backend validates both:

User ID
+
Role

before accepting the login.

These credentials are for local development/testing only.

🧱 Backend Architecture

The repository currently contains multiple backend layers.

backend/

Handles data collection and external-source processing.

backend/
├── collectors/
│   ├── email.py
│   ├── github.py
│   ├── meeting.py
│   └── slack.py
│
├── connectors/
│   └── google_drive.py
│
├── meeting/
│   ├── knowledge_extractor.py
│   ├── meeting_llm.py
│   ├── raw_document_generator.py
│   └── speaker_mapper.py
│
└── main.py

backend_3_4/

Contains privacy, storage, database and knowledge-related services.

backend_3_4/
├── agents/
│   ├── privacy_agent.py
│   └── storage_agent.py
│
├── services/
│   ├── anonymizer.py
│   ├── chroma_service.py
│   ├── embedding_service.py
│   ├── entity_merger.py
│   ├── grok_service.py
│   ├── hashing_service.py
│   ├── pii_detector.py
│   ├── postgres_service.py
│   └── presidio_service.py
│
├── models.py
└── main.py

backend_56/

Contains the API and RAG components.

backend_56/
├── agents/
│   ├── answer_agent.py
│   └── retrieval_agent.py
│
├── database/
│   ├── chroma_db.py
│   └── rebuild_chroma.py
│
├── services/
│   └── embedding.py
│
├── shared/
│   └── config.py
│
└── api.py

🎨 Frontend Architecture

The frontend is built using React and Vite.

frontend/
├── src/
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   │
│   └── pages/
│       ├── LandingPage.jsx
│       ├── LandingPage.css
│       ├── RoleSelection.jsx
│       ├── RoleSelection.css
│       ├── Login.jsx
│       ├── Login.css
│       ├── EmployeeDashboard.jsx
│       ├── EmployeeDashboard.css
│       ├── ManagerDashboard.jsx
│       ├── ManagerDashboard.css
│       ├── HRDashboard.jsx
│       └── HRDashboard.css
│
├── package.json
├── package-lock.json
└── vite.config.js

📁 Project Structure

AI_PRE_LOSS_SYSTEM/
│
├── Agent2/
│   ├── agents/
│   ├── prompts/
│   ├── services/
│   └── shared/
│
├── backend/
│   ├── collectors/
│   ├── connectors/
│   ├── meeting/
│   ├── shared/
│   └── main.py
│
├── backend_3_4/
│   ├── agents/
│   ├── config/
│   ├── services/
│   ├── shared/
│   ├── tests/
│   ├── models.py
│   └── main.py
│
├── backend_56/
│   ├── agents/
│   ├── database/
│   ├── services/
│   ├── shared/
│   └── api.py
│
├── chroma_db/
│
├── frontend/
│   ├── public/
│   └── src/
│
└── .gitignore

🧰 Technology Stack

Frontend

React

Vite

JavaScript / JSX

CSS

Lucide React icons

Backend

Python

FastAPI

SQLAlchemy

Pydantic

Database

PostgreSQL

Vector Search

ChromaDB

AI / LLM

Grok-based services

Retrieval Agent

Answer Agent

Knowledge Agent

Privacy

Microsoft Presidio

PII detection

Anonymization

Hashing

Integrations

GitHub

Slack

Email

Google Drive

Meeting processing

🗄️ Database Design

The current database model contains important entities such as:

Knowledge

knowledge
├── id
├── title
├── summary
├── category
├── confidence
├── timestamp
├── employee_hash
├── manager_hash
└── vector_id

Tasks

tasks
├── id
├── title
├── description
├── priority
├── status
├── due_date
├── employee_id
├── manager_id
└── created_at

Projects

projects
├── id
├── name
├── description
├── manager_id
├── status
└── created_at

Project Employees

project_employees
├── id
├── project_id
├── employee_id
└── added_at

Identity Mapping

Used to associate hashed identities with authorized organizational identities.

Users

The authentication model contains:

users
├── id
├── user_id
├── role
├── password_hash
├── display_name
├── email
├── is_active
└── created_at

🔌 API Overview

The backend provides APIs for several functional areas.

Authentication

POST /auth/setup
POST /auth/login

Employee

Examples include endpoints for:

Employee overview
Employee projects
Employee tasks
Employee knowledge
Employee activity

Manager

Examples include:

Manager overview
Employees
Projects
Tasks
Activity

HR

Examples include:

HR overview
Employees
Projects
Tasks
Activity

AI

POST /ask

Knowledge Upload

POST /upload

The exact endpoint set can evolve as the platform is developed.

🔒 Security Design

The system follows a defense-in-depth approach.

Authentication
      ↓
Role Validation
      ↓
Authorization
      ↓
Privacy Filtering
      ↓
Knowledge Retrieval
      ↓
AI Generation

This is important because authentication alone does not guarantee that a user should see every piece of organizational knowledge.

🧪 Testing Strategy

Testing is divided into several layers.

Authentication Tests

Correct ID + Password       → PASS
Wrong Password              → DENY
Wrong Role                  → DENY
Unknown User                → DENY
Inactive User               → DENY

Authorization Tests

Employee → Employee data   → PASS
Employee → HR data         → DENY

Manager → Team data        → PASS
Manager → Restricted HR    → DENY

RAG Tests

Known question
    ↓
Relevant knowledge
    ↓
Grounded answer

Negative case:

Unknown question
    ↓
No sufficient knowledge

Privacy Tests

Sensitive information should be detected and protected before being exposed to downstream AI components.

📊 Current Project Status

Completed

Project architecture

React frontend

Landing page

Role selection

Login UI

Employee dashboard

Manager dashboard

HR dashboard

PostgreSQL integration

Project APIs

Task APIs

Activity APIs

Knowledge APIs

Development authentication

Password hashing

Employee authentication test

Manager authentication test

HR authentication test

RAG components

Retrieval agent

Answer agent

Privacy components

PII detection components

Anonymization components

GitHub/email/Slack/meeting collectors

Google Drive connector

GitHub repository backup

🚧 Remaining Development

The following features are planned for completion:

Authentication Security

JWT access tokens

Token expiration

Protected frontend routes

Role-based route guards

Logout/session cleanup

AI Assistant

Final dashboard integration

Role-aware assistant context

Knowledge permission filtering

Improved response validation

RAG

Final retrieval pipeline

Retrieval evaluation

Negative RAG testing

Hallucination prevention

Retrieval quality improvements

Privacy

Final end-to-end privacy pipeline

PII evaluation

Sensitive information access tests

Privacy-aware retrieval

Testing

Full end-to-end testing

Permission testing

Security testing

RAG evaluation

Negative test suite

Production deployment, company OAuth configuration, and production credentials are intentionally treated as a later phase.

⚙️ Installation

1. Clone the repository

git clone <YOUR_REPOSITORY_URL>
cd AI_PRE_LOSS_SYSTEM

2. Frontend

cd frontend
npm install

3. Backend

Create the required Python environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies according to the backend requirements.

For the main backend:

pip install -r backend/requirements.txt

Additional backend components may have their own dependency requirements.

▶️ Running the Project

Start Frontend

cd frontend
npm run dev

The Vite development server will normally be available at:

http://localhost:5173

Start Backend

Use the project's configured Python entry point.

For example:

python -m backend_56.api

The API documentation can then be accessed through FastAPI's Swagger UI:

http://127.0.0.1:8000/docs

🧪 Development Credentials

For local development only:

Role

ID

Password

👨‍💻 Employee

EMP001

Employee@123

👔 Manager

MANAGER001

Manager@123

🧑‍💼 HR

HR001

HR@123

⚠️ Important

These credentials are development credentials only.

Do not use them in production.

Production authentication should use:

Company identity provider

Secure password policies

OAuth / SSO

JWT/session management

Secret management

MFA where appropriate

🔄 Development Workflow

Recommended workflow:

1. Create feature
      ↓
2. Test locally
      ↓
3. Check git status
      ↓
4. Add safe files
      ↓
5. Commit
      ↓
6. Push
      ↓
7. Continue next feature

Example:

git status
git add -A
git commit -m "Add authentication security"
git push

🔐 Git & Secrets

The repository intentionally excludes sensitive local files through .gitignore.

Examples:

.env
*.env
client_secret.json
drive_token.json
token.json
__pycache__/
*.pyc
chroma_db/

Never commit:

API keys

Passwords

OAuth client secrets

Access tokens

Private certificates

Production credentials

Private company data

🌐 Production Considerations

Production deployment is a later phase.

When deployed for a real organization, the system should introduce:

Company Identity Provider
          ↓
       SSO/OAuth
          ↓
      JWT/Session
          ↓
 Role-Based Authorization
          ↓
 Privacy Layer
          ↓
 Knowledge/RAG

Production deployment should also include:

HTTPS

Secure secret storage

Database migrations

Monitoring

Logging

Rate limiting

Backup strategy

Access auditing

Strong authentication

Company-approved OAuth scopes

🔮 Future Enhancements

Potential future improvements include:

Enterprise SSO

Integrate with:

Microsoft Entra ID

Google Workspace

Okta

Other company identity providers

Advanced Knowledge Graph

Build relationships between:

Employee
   ↕
Project
   ↕
Task
   ↕
Decision
   ↕
Document
   ↕
Meeting

Better RAG Evaluation

Track:

Recall

Precision

Retrieval relevance

Context quality

Answer faithfulness

Citation accuracy

Intelligent Alerts

Detect:

Missing documentation

Repeated knowledge

Important undocumented decisions

Potential knowledge loss

Sensitive information exposure

Employee Knowledge Transfer

Before an employee leaves:

Employee Knowledge
        ↓
Knowledge Extraction
        ↓
Validation
        ↓
Structured Knowledge
        ↓
Organizational Knowledge Base

This directly supports the project's loss-prevention objective.

🧠 Why This Project Matters

Traditional enterprise systems store information.

This system focuses on:

Understanding, preserving, protecting, and retrieving organizational knowledge.

The goal is not simply to build another chatbot.

The goal is to build a controlled organizational intelligence layer where:

Knowledge
   +
Privacy
   +
Authorization
   +
Retrieval
   +
AI

work together.

🏁 Project Vision

The long-term vision is:

                 COMPANY KNOWLEDGE
                        │
        ┌───────────────┼────────────────┐
        │               │                │
      GitHub          Slack            Email
        │               │                │
        └───────────────┼────────────────┘
                        │
                     Meetings
                        │
                        ▼
                KNOWLEDGE INGESTION
                        │
                        ▼
                 PRIVACY ENGINE
                        │
                        ▼
                KNOWLEDGE MEMORY
                        │
                        ▼
                  RAG / RETRIEVAL
                        │
                        ▼
                 AI KNOWLEDGE AGENT
                        │
        ┌───────────────┼────────────────┐
        │               │                │
    EMPLOYEE         MANAGER             HR
        │               │                │
        └───────────────┼────────────────┘
                        ▼
                 SECURE AI ASSISTANT

The system aims to make organizational knowledge:

Discoverable.

Useful.

Private.

Permission-aware.

Grounded.

Preserved.

👨‍💻 Project Development

This project is being developed as an end-to-end AI system combining:

Full-stack development

Backend APIs

Database engineering

AI agents

Retrieval-Augmented Generation

Vector search

Privacy engineering

PII detection

Enterprise integrations

Role-based access control

📄 License

This project is currently intended for educational, development, and demonstration purposes.

Add an appropriate open-source license before publicly distributing or commercializing the project.

⭐ Final Note

AI Loss Prevention is designed around a simple principle:

Enterprise knowledge should not be lost, and it should not be exposed without authorization.

The platform brings organizational data, privacy protection, retrieval, and AI assistance together to create a safer and more useful enterprise knowledge system.
