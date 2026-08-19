

# 🛡️ AI Loss Prevention System

**Intelligent Enterprise Knowledge • Privacy • RAG • AI Assistant**

*Protect organizational knowledge. Prevent sensitive data loss. Give every team the right intelligence.*





## 📌 Table of Contents

- [Overview](#-overview)
- [Problem](#-problem)
- [Solution](#-solution)
- [Features](#-features)
- [Architecture](#️-architecture)
- [User Flow](#-user-flow)
- [Role-Based Experience](#-role-based-experience)
- [AI and RAG](#-ai-and-rag)
- [Negative RAG](#-negative-rag)
- [Privacy and Loss Prevention](#️-privacy-and-loss-prevention)
- [Knowledge Sources](#-knowledge-sources)
- [Database](#️-database)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Quick Start](#-quick-start)
- [Authentication](#-development-authentication)
- [Testing](#-testing)
- [Current Status](#-current-status)
- [Roadmap](#️-roadmap)
- [Security](#-git-and-secrets)
- [Future Enhancements](#-future-enhancements)
- [Project Vision](#-project-vision)

---

## 🎯 Overview

**AI Loss Prevention System** is an enterprise knowledge platform that combines:

- 🧠 Organizational knowledge preservation
- 🛡️ Privacy protection
- 🔒 Role-based access
- 🔎 Retrieval-Augmented Generation (RAG)
- 🤖 AI-powered knowledge assistance

Organizations create valuable information every day across GitHub, Slack, Email, meetings, projects, and internal documentation. That knowledge becomes fragmented, hard to search, or lost entirely when people change teams or leave. At the same time, sending raw enterprise data directly into an AI system creates real privacy and security risk.

**This project solves both problems at once.**

```
GitHub ─────┐
Slack ──────┤
Email ──────┤
Meetings ───┤
Projects ───┤
Knowledge ──┘
      │
      ▼
Data Ingestion → Privacy / PII Protection → Knowledge Storage
      │
      ▼
Embeddings + Vector Search → RAG Retrieval → Permission Check
      │
      ▼
                AI Assistant
                     │
            ┌────────┼────────┐
            ▼        ▼        ▼
          EMP       MGR       HR
```

---

## 💡 Problem

| # | Problem | Description |
|---|---------|--------------|
| 1 | **Knowledge Loss** | Important technical and business decisions often live only in employees' memory. |
| 2 | **Knowledge Fragmentation** | Information is scattered across GitHub, Slack, Email, meetings, documents, and project systems. |
| 3 | **Difficult Discovery** | People know information exists but can't find where it's stored. |
| 4 | **Privacy Risk** | Enterprise data may contain PII, emails, phone numbers, internal identifiers, credentials, and sensitive business information. |
| 5 | **AI Hallucination** | An AI assistant may confidently answer even when the organization has no supporting evidence. |

---

## 🚀 Solution

The **AI Loss Prevention System** creates a controlled organizational knowledge layer that makes knowledge:

`Discoverable` · `Useful` · `Private` · `Permission-aware` · `Grounded` · `Preserved`

```
COMPANY DATA (GitHub / Slack / Email / Meetings)
      │
      ▼
DATA INGESTION → PRIVACY / PII → KNOWLEDGE MEMORY
      │
      ▼
VECTOR REPRESENTATION → RETRIEVAL → AUTHORIZATION
      │
      ▼
                AI ASSISTANT
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏠 **Landing Page** | Product introduction and entry point |
| 👥 **Role Selection** | Employee, Manager, and HR workflows |
| 🔐 **Authentication** | User ID, password, and role verification |
| 👨‍💻 **Employee Dashboard** | Personal projects, tasks, and knowledge |
| 👔 **Manager Dashboard** | Team, projects, tasks, and activity |
| 🧑‍💼 **HR Dashboard** | Organization-level overview |
| 📋 **Task Management** | Assignment, priority, status, due dates |
| 📁 **Project Management** | Projects, members, and status |
| 🧠 **Knowledge Management** | Structured organizational knowledge |
| 🤖 **AI Assistant** | Natural-language enterprise knowledge access |
| 🔎 **RAG** | Retrieval-grounded AI responses |
| 🛡️ **PII Protection** | Privacy-aware processing |
| 🔒 **Role-Based Access** | Authorized information access only |
| 📊 **Activity Tracking** | Project and task activity |
| 🔌 **Data Collectors** | GitHub, Slack, Email, and Meetings |

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
      │  Users · Projects   │    │  Embeddings         │
      │  Tasks · Knowledge  │    │  Vector Search / RAG │
      └────────────────────┘    └──────────┬──────────┘
                                            ▼
                                 ┌───────────────────┐
                                 │     AI AGENTS      │
                                 │ Retrieval Agent    │
                                 │ Answer Agent       │
                                 │ Knowledge Agent    │
                                 │ Privacy Agent      │
                                 └───────────────────┘
```

---

## 🔄 User Flow

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
- Tasks
- Knowledge
- Activity
- AI Assistant

</td>
<td>

- Employees
- Projects
- Tasks
- Team Knowledge
- Activity
- AI Assistant

</td>
<td>

- Employee Overview
- Project Overview
- Task Overview
- Organization Activity
- Knowledge Overview
- AI Assistant

</td>
</tr>
</table>

---

## 🤖 AI and RAG

The AI layer uses **Retrieval-Augmented Generation** — instead of answering purely from internal model knowledge, the system first retrieves relevant organizational information.

```
User Question → Query Processing → Embedding → Vector Search
      │
      ▼
Relevant Knowledge → Permission / Privacy Filter → Context
      │
      ▼
                  LLM → Grounded Answer
```

**Example**

> **User:** "Why was PostgreSQL retained instead of MongoDB?"
>
> `Retrieval Agent` → relevant organizational decisions → `Answer Agent` → grounded response

---

## 🚫 Negative RAG

A critical requirement: gracefully handle questions the knowledge base can't answer.

| Without Negative RAG | With Negative RAG |
|---|---|
| Question → no relevant knowledge → LLM guesses → ❌ **Hallucinated answer** | Question → retrieval → evidence sufficient? → ✅ **Answer** or 🚫 **"No sufficient knowledge found."** |

This makes the assistant safer and more trustworthy for enterprise use.

---

## 🛡️ Privacy and Loss Prevention

Privacy is implemented as a dedicated processing layer:

```
RAW DATA → PII DETECTION → SENSITIVE ENTITY CHECK → ANONYMIZATION / HASHING
      │
      ▼
SAFE REPRESENTATION → STORAGE → RETRIEVAL → AUTHORIZATION CHECK → AI
```

**Privacy components:** PII Detector · Presidio Service · Anonymizer · Hashing Service · Entity Merger · Privacy Agent · Storage Agent

### 🔐 Security Model

```
Authentication → Role Validation → Authorization → Privacy Filtering → Knowledge Retrieval → AI Response
```

> **Key principle:** Authentication does not automatically grant access to every piece of organizational knowledge.

---

## 📥 Knowledge Sources

| Source | Used For |
|---|---|
| 🐙 **GitHub** | Technical decisions, repository info, engineering context |
| 💬 **Slack** | Discussions, decisions, problem solving, team communication |
| 📧 **Email** | Organizational communication, approvals, decisions, business context |
| 🎙️ **Meetings** | Recording → Transcript → Speaker Mapping → Knowledge Extraction → Summary |
| ☁️ **Google Drive** | Document-based organizational knowledge |

**Knowledge record fields:** `ID` · `Title` · `Summary` · `Category` · `Confidence` · `Timestamp` · `Employee Hash` · `Manager Hash` · `Vector ID`

---

## 🗄️ Database

PostgreSQL powers structured application data.

| Table | Purpose |
|---|---|
| `users` | Authentication and roles |
| `knowledge` | Organizational knowledge |
| `tasks` | Task assignments and status |
| `projects` | Project information |
| `project_employees` | Project membership |
| `identity_mapping` | Identity/hash relationships |

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
│   │   ├── email.py
│   │   ├── github.py
│   │   ├── meeting.py
│   │   └── slack.py
│   ├── connectors/
│   │   └── google_drive.py
│   ├── meeting/
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
│   │   ├── answer_agent.py
│   │   └── retrieval_agent.py
│   ├── database/
│   ├── services/
│   ├── shared/
│   └── api.py
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── App.jsx
│       └── pages/
│           ├── LandingPage.jsx
│           ├── RoleSelection.jsx
│           ├── Login.jsx
│           ├── EmployeeDashboard.jsx
│           ├── ManagerDashboard.jsx
│           └── HRDashboard.jsx
│
├── .gitignore
└── README.md
```

---

## 🧰 Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React, Vite, JSX, CSS |
| **Backend** | Python, FastAPI, SQLAlchemy, Pydantic |
| **Database** | PostgreSQL |
| **Vector DB** | ChromaDB |
| **AI** | RAG, Embeddings, AI Agents |
| **Privacy** | Presidio, PII Detection, Anonymization, Hashing |
| **Integrations** | GitHub, Slack, Email, Google Drive, Meetings |

---

## ⚡ Quick Start

### 1. Clone

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

Frontend runs at: **http://localhost:5173**

### 3. Backend

Create a Python environment:

```bash
python -m venv venv
```

Activate it (Windows):

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Run the configured API:

```bash
python -m backend_56.api
```

Swagger docs: **http://127.0.0.1:8000/docs**

---

## 🔑 Development Authentication

> ⚠️ **LOCAL DEVELOPMENT ONLY**

| Role | ID |
|---|---|
| 👨‍💻 Employee | `EMP001` |
| 👔 Manager | `MANAGER001` |
| 🧑‍💼 HR | `HR001` |

Passwords should remain local and must **never** be committed to GitHub. Production should use secure company authentication such as SSO/OAuth.

---

## 🧪 Testing

<details>
<summary><strong>Authentication</strong></summary>

- Employee / Manager / HR login
- Password verification
- Role validation
- JWT/session
- Token expiration
- Protected routes
- Logout

</details>

<details>
<summary><strong>Dashboards</strong></summary>

- Employee, Manager, HR dashboards
- Projects, Tasks, Activity
- Knowledge information

</details>

<details>
<summary><strong>AI</strong></summary>

- Retrieval Agent, Answer Agent
- Vector search components
- Final dashboard assistant integration
- Full negative-RAG evaluation
- Retrieval quality evaluation

</details>

<details>
<summary><strong>Privacy</strong></summary>

- PII detection component
- Presidio integration
- Anonymization component
- Hashing service
- End-to-end privacy validation

</details>

---

## 📊 Current Status

### Product Foundation

| Module | Status |
|---|---|
| Landing Page | ✅ Complete |
| Role Selection | ✅ Complete |
| Basic Authentication | ✅ Complete |
| Employee Dashboard | ✅ Complete |
| Manager Dashboard | ✅ Complete |
| HR Dashboard | ✅ Complete |
| Backend APIs | 🟡 In Progress |
| Database | ✅ Complete |
| Project Management | ✅ Complete |
| Task Management | ✅ Complete |

### AI and Security

| Module | Status |
|---|---|
| Retrieval Agent | ✅ Implemented |
| Answer Agent | ✅ Implemented |
| Vector Search | ✅ Implemented |
| AI Assistant Integration | 🟡 In Progress |
| RAG Finalization | 🟡 In Progress |
| Negative RAG | 🟡 In Progress |
| Privacy Pipeline | 🟡 In Progress |
| JWT Security | ⏳ Next |
| Protected Routes | ⏳ Next |
| Logout | ⏳ Next |
| Full Testing | ⏳ Pending |

---

## 🛣️ Roadmap

- [x] **Phase 1 — Product Foundation:** Landing Page · Role Selection · Login · Employee/Manager/HR Dashboards
- [x] **Phase 2 — Core Backend:** PostgreSQL · Projects · Tasks · Activity · Knowledge APIs · Authentication API
- [ ] **Phase 3 — AI Knowledge:** Retrieval Agent · Answer Agent · Embeddings · Vector database · Final RAG evaluation · Negative RAG hardening
- [ ] **Phase 4 — Security:** Password hashing · Role validation · PII detection · Anonymization · JWT · Protected routes · Logout · Full authorization testing
- [ ] **Phase 5 — Enterprise Intelligence:** GitHub/Slack/Email collectors · Meeting pipeline · Google Drive connector · Ingestion orchestration · Permission-aware retrieval
- [ ] **Phase 6 — Production:** Company SSO · OAuth · Secret management · HTTPS · Monitoring · Production deployment

---

## 🔒 Git and Secrets

Sensitive files are intentionally excluded from version control:

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

**Never commit:** ❌ API keys · ❌ Passwords · ❌ OAuth secrets · ❌ Access tokens · ❌ Private certificates · ❌ Production credentials · ❌ Private company data

### 🚨 Enterprise Security (Production)

```
Company Identity Provider → SSO / OAuth → JWT / Session
      │
      ▼
Role-Based Authorization → Privacy Filtering → RAG / Retrieval → AI Assistant
```

Additional production requirements: HTTPS · Secure secret management · Database migrations · Monitoring · Logging · Rate limiting · Access auditing · Backup strategy · Strong authentication · MFA where appropriate.

---

## 🔮 Future Enhancements

- **🧠 Knowledge Graph** — relationships between Employee ↔ Project ↔ Task ↔ Decision ↔ Document ↔ Meeting
- **📊 Advanced RAG Evaluation** — retrieval recall/precision, context relevance, answer faithfulness, hallucination rate, citation accuracy
- **🚨 Knowledge Loss Alerts** — undocumented decisions, repeated questions, missing documentation, critical knowledge gaps
- **🤝 Knowledge Transfer** — when an employee changes role or leaves: `Employee Knowledge → Extraction → Privacy Filtering → Validation → Organizational Memory`

---

## 🌟 Why This Project?

This isn't just another chatbot. It combines **Privacy**, **Retrieval**, and **Access** into one secure AI assistant.

**Key principles:**

1. Knowledge should not be lost.
2. Sensitive information should not be exposed unnecessarily.
3. AI should answer from evidence.
4. Users should only access authorized information.
5. When evidence is missing, the system should say so.

---

## 🏁 Project Vision

> Build an organization's **AI-powered knowledge memory** — grounded, private, and permission-aware — serving Employees, Managers, and HR alike.

---

<div align="center">

### 💬 Preserve Knowledge. Protect Privacy. Empower Teams.

**⭐ Current milestone:** Core platform + dashboards + knowledge/RAG foundation completed.
**➡️ Next milestone:** JWT security → Protected routes → Logout → Final AI assistant → RAG hardening → Privacy validation → Complete testing.

**🛡️ AI Loss Prevention System** — *Intelligent Enterprise Knowledge Management*

</div>
