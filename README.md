# 🛡️ AI Loss Prevention System

**Intelligent Enterprise Knowledge • Privacy • RAG • AI Assistant**

*Protect organizational knowledge. Prevent sensitive data loss. Give every team the right intelligence.*

An AI-powered enterprise knowledge, privacy, and loss-prevention platform designed to protect organizational intelligence while making it accessible to authorized employees, managers, and HR teams.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem](#-problem)
- [Solution](#-solution)
- [Core Objectives](#-core-objectives)
- [Features](#-features)
- [Architecture](#️-architecture)
- [User Flow](#-user-flow)
- [Role-Based Experience](#-role-based-experience)
- [Knowledge System](#-knowledge-system)
- [AI and RAG](#-ai-and-rag)
- [Negative RAG / Hallucination Prevention](#-negative-rag--hallucination-prevention)
- [Privacy and Loss Prevention](#️-privacy-and-loss-prevention)
- [Knowledge Sources](#-knowledge-sources)
- [Authentication](#-development-authentication)
- [Backend Architecture](#-backend-architecture)
- [Frontend Architecture](#-frontend-architecture)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Database Design](#️-database-design)
- [API Overview](#-api-overview)
- [Security Design](#-security-design)
- [Testing Strategy](#-testing-strategy)
- [Current Status](#-current-status)
- [Roadmap](#️-roadmap)
- [Quick Start](#-quick-start)
- [Git and Secrets](#-git-and-secrets)
- [Production Considerations](#-production-considerations)
- [Future Enhancements](#-future-enhancements)
- [Why This Project Matters](#-why-this-project-matters)
- [Project Vision](#-project-vision)
- [License](#-license)

---

## 🎯 Overview

**AI Loss Prevention System** is an enterprise knowledge platform that combines:

- 🧠 Organizational knowledge preservation
- 🛡️ Privacy protection
- 🔒 Role-based access
- 🔎 Retrieval-Augmented Generation (RAG)
- 🤖 AI-powered knowledge assistance

Modern organizations generate huge amounts of knowledge through GitHub repositories, Slack conversations, emails, meetings, project documentation, tasks, and internal discussions. A large portion of this knowledge becomes difficult to discover, disconnected across tools, or lost entirely when employees leave. At the same time, sending raw enterprise data directly into an AI system introduces real privacy and security risk.

**This project solves both problems at once**, combining Knowledge Preservation + Privacy Protection + Role-Based Access + RAG + AI Assistance into a single platform.

---

## 🎯 Problem

Organizations continuously create valuable knowledge, but that knowledge is often fragmented:

```
GitHub    → Code, Pull Requests, Technical Decisions
Slack     → Discussions, Decisions, Problem Solving
Email     → Communication, Approvals, Decisions
Meetings  → Conversations, Decisions, Action Items
```

| # | Problem | Description |
|---|---------|--------------|
| 1 | **Knowledge Loss** | Important decisions often live only in employees' memory and disappear when they leave or change teams. |
| 2 | **Knowledge Fragmentation** | Information is scattered across GitHub, Slack, Email, meetings, and project systems. |
| 3 | **Difficult Discovery** | Employees may know information exists but not where it's stored. |
| 4 | **Privacy Risk** | Enterprise data may contain PII, emails, phone numbers, credentials, internal identifiers, and sensitive business information. |
| 5 | **AI Hallucination** | Without sufficient evidence, an AI system may confidently generate an answer that sounds correct but is unsupported. |

The AI Loss Prevention System addresses these challenges through a controlled knowledge pipeline.

---

## 🚀 Solution

The system collects organizational knowledge, processes it through privacy-aware components, stores it in searchable representations, and allows authorized users to retrieve information through dashboards and an AI assistant — making knowledge:

`Discoverable` · `Useful` · `Private` · `Permission-aware` · `Grounded` · `Preserved`

```
ORGANIZATIONAL DATA (GitHub / Slack / Email / Meetings)
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
      ▼             ▼             ▼
  Employee       Manager          HR
      │             │             │
      └─────────────┼─────────────┘
                    ▼
              AI Assistant
```

---

## 🎯 Core Objectives

1. **Preserve Organizational Knowledge** — convert scattered information into structured, searchable knowledge.
2. **Prevent Sensitive Information Leakage** — detect and protect sensitive data before it reaches downstream AI components.
3. **Provide Role-Based Access** — different users see only information appropriate for their role.
4. **Enable Grounded AI Answers** — use retrieval-based AI instead of relying solely on the model's internal knowledge.
5. **Prevent Unsupported Answers** — if sufficient knowledge isn't available, the system avoids inventing one.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏠 **Landing Page** | Product introduction and entry point |
| 👥 **Role Selection** | Employee, Manager, and HR workflows |
| 🔐 **Authentication** | User ID, password, and role verification with secure hashing |
| 👨‍💻 **Employee Dashboard** | Personal projects, tasks, and knowledge |
| 👔 **Manager Dashboard** | Team, projects, tasks, and activity |
| 🧑‍💼 **HR Dashboard** | Organization-level overview |
| 📋 **Task Management** | Assignment, priority, status, due dates, employee/manager ownership |
| 📁 **Project Management** | Projects, members, status, employee counts |
| 🧠 **Knowledge Management** | Categories, confidence scores, timestamps, vector references |
| 🤖 **AI Assistant** | Natural-language, context-based, role-aware enterprise knowledge access |
| 🔎 **RAG** | Embedding generation, vector storage, similarity retrieval, grounded answering |
| 🛡️ **Privacy Layer** | PII detection, anonymization, hashing, sensitive-data protection |
| 🔒 **Role-Based Access** | Authorized information access only |
| 📈 **Activity Tracking** | Project creation, employee/task assignment, task updates |
| 🔌 **Data Collectors** | GitHub, Slack, Email, Meetings, Google Drive |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        FRONTEND                          │
│   Landing → Role Selection → Login → Dashboard           │
│      Employee        Manager          HR                 │
└───────────────────────────┬───────────────────────────────┘
                             │ REST / HTTP
                             ▼
┌─────────────────────────────────────────────────────────┐
│                         API LAYER                        │
│  Auth │ Employee │ Manager │ HR │ Projects │ Tasks │ AI  │
└───────────────┬─────────────────────────┬─────────────────┘
                 ▼                         ▼
      ┌────────────────────┐    ┌────────────────────┐
      │     PostgreSQL      │    │      ChromaDB       │
      │  Users · Projects   │    │  Embeddings          │
      │  Tasks · Knowledge  │    │  Vector Search / RAG │
      └────────────────────┘    └──────────┬──────────┘
                                            ▼
                                 ┌───────────────────┐
                                 │     AI AGENTS       │
                                 │ Retrieval Agent     │
                                 │ Answer Agent        │
                                 │ Knowledge Agent     │
                                 │ Privacy Agent       │
                                 └───────────────────┘
```

---

## 🔄 User Flow

**1. Landing Page** — product introduction, security information, AI capabilities, "Get Started."

**2. Role Selection** — Employee, Manager, or HR.

**3. Login** — the selected role determines the authentication context:

```json
{
  "identifier": "EMP001",
  "password": "********",
  "role": "employee"
}
```

**4. Authentication** — the backend validates `User ID + Role + Password`.

**5. Dashboard** — after successful authentication, the user reaches their role-appropriate dashboard.

```
Landing Page → Role Selection → Login → Authentication → Authorized Dashboard
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
        EMP        MGR        HR
```

---

## 👥 Role-Based Experience

<table>
<tr>
<th>👨‍💻 Employee</th>
<th>👔 Manager</th>
<th>🧑‍💼 HR</th>
</tr>
<tr>
<td>

- Projects
- Tasks / Pending / Completed
- Knowledge
- Activity
- AI Assistant

</td>
<td>

- Total Employees
- Projects & Tasks
- Team Knowledge
- Recent Activity
- AI Assistant

</td>
<td>

- Employee Overview
- Project & Task Overview
- Organization Activity
- Knowledge Overview
- AI Assistant

</td>
</tr>
</table>

**Example HR overview:**

```json
{
  "total_employees": 1,
  "total_projects": 2,
  "total_tasks": 4,
  "pending_tasks": 4,
  "completed_tasks": 0,
  "team_knowledge": 6
}
```

---

## 🧠 Knowledge System

Knowledge records are the central data unit of the platform, containing:

`ID` · `Title` · `Summary` · `Category` · `Confidence` · `Timestamp` · `Employee Hash` · `Manager Hash` · `Vector ID`

This allows knowledge to be associated with people, projects, categories, time, confidence, and vector representations.

---

## 🤖 AI and RAG

The AI layer uses **Retrieval-Augmented Generation** — instead of answering purely from internal model knowledge, the system first retrieves relevant organizational information, so the AI answers from evidence rather than inventing it.

```
User Question → Query Processing → Embedding Generation → Vector Similarity Search
      │
      ▼
Relevant Knowledge → Permission / Privacy Filtering → Context Construction
      │
      ▼
             Answer Generation → Grounded Answer
```

**Example**

> **User:** "Why was PostgreSQL retained instead of MongoDB?"
>
> `Retrieval Agent` → relevant organizational documents → `Context` → `Answer Agent` → grounded response

---

## 🚫 Negative RAG / Hallucination Prevention

A major evaluation scenario is when a user asks something that doesn't exist in the knowledge base.

| Without Negative RAG | With Negative RAG |
|---|---|
| Question → no relevant knowledge → LLM guesses → ❌ **Hallucinated answer** ("The team decided X because…") | Question → retrieval → evidence sufficient? → ✅ **Answer** or 🚫 **"No sufficient knowledge found."** |

This makes the assistant considerably more trustworthy for enterprise usage.

---

## 🛡️ Privacy and Loss Prevention

Privacy is implemented as a dedicated processing layer, designed to prevent unnecessary exposure of sensitive information:

```
Raw Data → PII Detection → Sensitive Entity Identification → Anonymization / Hashing
      │
      ▼
Safe Knowledge Representation → Vector / Database Storage
```

**Privacy components:** PII Detector · Presidio Integration · Anonymizer · Hashing Service · Entity Merger · Privacy Agent · Storage Agent

### 🔐 Security Model

```
Authentication → Role Validation → Authorization → Privacy Filtering → Knowledge Retrieval → AI Generation
```

> **Key principle:** authentication alone does not guarantee a user should see every piece of organizational knowledge.

---

## 📥 Knowledge Sources

| Source | Used For |
|---|---|
| 🐙 **GitHub** | Code-related information, repository knowledge, technical decisions |
| 💬 **Slack** | Organizational discussions, decisions, problem solving |
| 📧 **Email** | Relevant organizational communication and approvals |
| 🎙️ **Meetings** | Recording → Transcript → Speaker Mapping → Knowledge Extraction → Summary → Raw Document Generation |
| ☁️ **Google Drive** | Document-based organizational knowledge |

---

## 🔐 Development Authentication

> ⚠️ **For local development / testing only — never use in production.**

| Role | ID | Password |
|---|---|---|
| 👨‍💻 Employee | `EMP001` | `Employee@123` |
| 👔 Manager | `MANAGER001` | `Manager@123` |
| 🧑‍💼 HR | `HR001` | `HR@123` |

Passwords are stored as password hashes rather than plaintext. The backend validates both **User ID** and **Role** before accepting a login. Production authentication should use a company identity provider, secure password policies, OAuth/SSO, JWT/session management, secret management, and MFA where appropriate.

---

## 🧱 Backend Architecture

The repository currently contains multiple backend layers.

**`backend/`** — data collection and external-source processing

```
backend/
├── collectors/
│   ├── email.py
│   ├── github.py
│   ├── meeting.py
│   └── slack.py
├── connectors/
│   └── google_drive.py
├── meeting/
│   ├── knowledge_extractor.py
│   ├── meeting_llm.py
│   ├── raw_document_generator.py
│   └── speaker_mapper.py
└── main.py
```

**`backend_3_4/`** — privacy, storage, database, and knowledge services

```
backend_3_4/
├── agents/
│   ├── privacy_agent.py
│   └── storage_agent.py
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
├── models.py
└── main.py
```

**`backend_56/`** — API and RAG components

```
backend_56/
├── agents/
│   ├── answer_agent.py
│   └── retrieval_agent.py
├── database/
│   ├── chroma_db.py
│   └── rebuild_chroma.py
├── services/
│   └── embedding.py
├── shared/
│   └── config.py
└── api.py
```

---

## 🎨 Frontend Architecture

Built with **React** and **Vite**.

```
frontend/
├── src/
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── pages/
│       ├── LandingPage.jsx / .css
│       ├── RoleSelection.jsx / .css
│       ├── Login.jsx / .css
│       ├── EmployeeDashboard.jsx / .css
│       ├── ManagerDashboard.jsx / .css
│       └── HRDashboard.jsx / .css
├── package.json
├── package-lock.json
└── vite.config.js
```

---

## 📁 Project Structure

```
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
```

---

## 🧰 Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React, Vite, JavaScript/JSX, CSS, Lucide React icons |
| **Backend** | Python, FastAPI, SQLAlchemy, Pydantic |
| **Database** | PostgreSQL |
| **Vector Search** | ChromaDB |
| **AI / LLM** | Grok-based services, Retrieval Agent, Answer Agent, Knowledge Agent |
| **Privacy** | Microsoft Presidio, PII detection, Anonymization, Hashing |
| **Integrations** | GitHub, Slack, Email, Google Drive, Meeting processing |

---

## 🗄️ Database Design

**Knowledge**
```
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
```

**Tasks**
```
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
```

**Projects**
```
projects
├── id
├── name
├── description
├── manager_id
├── status
└── created_at
```

**Project Employees**
```
project_employees
├── id
├── project_id
├── employee_id
└── added_at
```

**Users**
```
users
├── id
├── user_id
├── role
├── password_hash
├── display_name
├── email
├── is_active
└── created_at
```

**Identity Mapping** — associates hashed identities with authorized organizational identities.

---

## 🔌 API Overview

| Area | Endpoints |
|---|---|
| **Authentication** | `POST /auth/setup`, `POST /auth/login` |
| **Employee** | Overview, projects, tasks, knowledge, activity |
| **Manager** | Overview, employees, projects, tasks, activity |
| **HR** | Overview, employees, projects, tasks, activity |
| **AI** | `POST /ask` |
| **Knowledge Upload** | `POST /upload` |

*The exact endpoint set can evolve as the platform is developed.*

---

## 🔒 Security Design

```
Authentication → Role Validation → Authorization → Privacy Filtering → Knowledge Retrieval → AI Generation
```

Authentication alone does not guarantee that a user should see every piece of organizational knowledge — the system follows a defense-in-depth approach.

---

## 🧪 Testing Strategy

<details>
<summary><strong>Authentication Tests</strong></summary>

```
Correct ID + Password       → PASS
Wrong Password               → DENY
Wrong Role                   → DENY
Unknown User                 → DENY
Inactive User                → DENY
```
</details>

<details>
<summary><strong>Authorization Tests</strong></summary>

```
Employee → Employee data     → PASS
Employee → HR data           → DENY
Manager  → Team data         → PASS
Manager  → Restricted HR     → DENY
```
</details>

<details>
<summary><strong>RAG Tests</strong></summary>

```
Known question → Relevant knowledge → Grounded answer
Unknown question → No sufficient knowledge
```
</details>

<details>
<summary><strong>Privacy Tests</strong></summary>

Sensitive information should be detected and protected before being exposed to downstream AI components.
</details>

---

## 📊 Current Status

### Product Foundation

| Module | Status |
|---|---|
| Landing Page | ✅ Complete |
| Role Selection | ✅ Complete |
| Login UI | ✅ Complete |
| Employee Dashboard | ✅ Complete |
| Manager Dashboard | ✅ Complete |
| HR Dashboard | ✅ Complete |
| PostgreSQL Integration | ✅ Complete |
| Project APIs | ✅ Complete |
| Task APIs | ✅ Complete |
| Activity APIs | ✅ Complete |
| Knowledge APIs | ✅ Complete |
| Development Authentication | ✅ Complete |
| Password Hashing | ✅ Complete |

### AI, RAG & Privacy

| Module | Status |
|---|---|
| Retrieval Agent | ✅ Implemented |
| Answer Agent | ✅ Implemented |
| Vector Search | ✅ Implemented |
| PII Detection Components | ✅ Implemented |
| Anonymization Components | ✅ Implemented |
| GitHub / Email / Slack / Meeting Collectors | ✅ Implemented |
| Google Drive Connector | ✅ Implemented |
| AI Assistant Dashboard Integration | 🟡 In Progress |
| RAG Finalization | 🟡 In Progress |
| Negative RAG Testing | 🟡 In Progress |
| Privacy End-to-End Pipeline | 🟡 In Progress |
| JWT Security | ⏳ Next |
| Protected Routes | ⏳ Next |
| Logout / Session Cleanup | ⏳ Next |
| Full End-to-End Testing | ⏳ Pending |

---

## 🛣️ Roadmap

- [x] **Phase 1 — Product Foundation:** Landing Page · Role Selection · Login · Employee/Manager/HR Dashboards
- [x] **Phase 2 — Core Backend:** PostgreSQL · Projects · Tasks · Activity · Knowledge APIs · Authentication API
- [ ] **Phase 3 — AI Knowledge:** Retrieval Agent · Answer Agent · Embeddings · Vector database · Final RAG evaluation · Negative RAG hardening
- [ ] **Phase 4 — Security:** JWT tokens · Token expiration · Protected frontend routes · Role-based route guards · Logout/session cleanup · Full authorization testing
- [ ] **Phase 5 — Enterprise Intelligence:** GitHub/Slack/Email collectors · Meeting pipeline · Google Drive connector · Ingestion orchestration · Permission-aware retrieval
- [ ] **Phase 6 — Production:** Company SSO · OAuth · Secret management · HTTPS · Monitoring · Production deployment

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd AI_PRE_LOSS_SYSTEM
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs at: **http://localhost:5173**

### 3. Backend

Create and activate a Python environment:

```bash
python -m venv venv
venv\Scripts\activate    # Windows
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

*Additional backend components (`backend_3_4`, `backend_56`) may have their own dependency requirements.*

Run the API:

```bash
python -m backend_56.api
```

Swagger docs: **http://127.0.0.1:8000/docs**

---

## 🔄 Development Workflow

```
1. Create feature → 2. Test locally → 3. Check git status
      → 4. Add safe files → 5. Commit → 6. Push → 7. Continue next feature
```

```bash
git status
git add -A
git commit -m "Add authentication security"
git push
```

---

## 🔒 Git and Secrets

The repository intentionally excludes sensitive local files via `.gitignore`:

```
.env
*.env
client_secret.json
drive_token.json
token.json
__pycache__/
*.pyc
chroma_db/
```

**Never commit:** ❌ API keys · ❌ Passwords · ❌ OAuth client secrets · ❌ Access tokens · ❌ Private certificates · ❌ Production credentials · ❌ Private company data

---

## 🌐 Production Considerations

Production deployment, company OAuth configuration, and production credentials are intentionally treated as a later phase.

```
Company Identity Provider → SSO / OAuth → JWT / Session
      │
      ▼
Role-Based Authorization → Privacy Layer → Knowledge / RAG
```

Production deployment should also include: HTTPS · Secure secret storage · Database migrations · Monitoring · Logging · Rate limiting · Backup strategy · Access auditing · Strong authentication · Company-approved OAuth scopes.

---

## 🔮 Future Enhancements

- **🔐 Enterprise SSO** — Microsoft Entra ID, Google Workspace, Okta, and other identity providers
- **🧠 Advanced Knowledge Graph** — relationships between Employee ↔ Project ↔ Task ↔ Decision ↔ Document ↔ Meeting
- **📊 Better RAG Evaluation** — recall, precision, retrieval relevance, context quality, answer faithfulness, citation accuracy
- **🚨 Intelligent Alerts** — missing documentation, repeated knowledge, undocumented decisions, potential knowledge loss, sensitive information exposure
- **🤝 Employee Knowledge Transfer** — before an employee leaves: `Employee Knowledge → Extraction → Validation → Structured Knowledge → Organizational Knowledge Base`

---

## 🧠 Why This Project Matters

Traditional enterprise systems store information. This system focuses on **understanding, preserving, protecting, and retrieving** organizational knowledge.

The goal isn't simply to build another chatbot — it's to build a controlled organizational intelligence layer where:

`Knowledge + Privacy + Authorization + Retrieval + AI` work together.

**Key principles:**

1. Knowledge should not be lost.
2. Sensitive information should not be exposed unnecessarily.
3. AI should answer from evidence.
4. Users should only access authorized information.
5. When evidence is missing, the system should say so.

---

## 🏁 Project Vision

```
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
```

The system aims to make organizational knowledge **discoverable, useful, private, permission-aware, grounded, and preserved.**

This project is being developed as an end-to-end AI system combining full-stack development, backend APIs, database engineering, AI agents, Retrieval-Augmented Generation, vector search, privacy engineering, PII detection, enterprise integrations, and role-based access control.

---

## 📄 License

This project is currently intended for educational, development, and demonstration purposes. Add an appropriate open-source license before publicly distributing or commercializing the project.

---

<div align="center">

### 💬 Preserve Knowledge. Protect Privacy. Empower Teams.

**⭐ Current milestone:** Core platform + dashboards + knowledge/RAG foundation completed.
**➡️ Next milestone:** JWT security → Protected routes → Logout → Final AI assistant → RAG hardening → Privacy validation → Complete testing.

**🛡️ AI Loss Prevention System** — *Intelligent Enterprise Knowledge Management*

</div>
