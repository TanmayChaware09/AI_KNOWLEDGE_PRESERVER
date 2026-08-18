🛡️ AI Loss Prevention System

Intelligent Enterprise Knowledge • Privacy • RAG • AI Assistant

Protect organizational knowledge. Prevent sensitive data loss. Give every team the right intelligence.








📌 Table of Contents

Overview

Problem

Solution

Features

Architecture

User Flow

Role-Based Experience

AI and RAG

Negative RAG

Privacy and Loss Prevention

Knowledge Sources

Database

Project Structure

Technology Stack

Quick Start

Authentication

Testing

Current Status

Roadmap

Security

Future Enhancements

Project Vision

🎯 Overview

AI Loss Prevention System is an enterprise knowledge platform that combines:

Organizational knowledge preservation

Privacy protection

Role-based access

Retrieval-Augmented Generation

AI-powered knowledge assistance

Organizations create valuable information every day across GitHub, Slack, Email, meetings, projects, and internal documentation.

The problem is that this knowledge becomes fragmented, difficult to search, or completely lost when people change teams or leave an organization.

At the same time, sending raw enterprise information directly to an AI system can create privacy and security risks.

This project addresses both problems.

Core idea

GitHub ─────┐
Slack ──────┤
Email ──────┤
Meetings ───┤
Projects ───┤
Knowledge ──┘
      │
      ▼
Data Ingestion
      │
      ▼
Privacy / PII Protection
      │
      ▼
Knowledge Storage
      │
      ▼
Embeddings + Vector Search
      │
      ▼
RAG Retrieval
      │
      ▼
Permission Check
      │
      ▼
AI Assistant
      │
 ┌────┼────┐
 ▼    ▼    ▼
EMP  MGR   HR

💡 Problem

Modern organizations face several knowledge-management problems.

1. Knowledge Loss

Important technical and business decisions often exist only in individual employees' memory.

2. Knowledge Fragmentation

Information is distributed across:

GitHub

Slack

Email

Meetings

Documents

Project systems

3. Difficult Discovery

Employees may know that information exists but not where it is stored.

4. Privacy Risk

Enterprise information may contain:

Personal information

Emails

Phone numbers

Internal identifiers

Credentials

Sensitive business information

5. AI Hallucination

An AI assistant may generate a confident answer even when the organization has no supporting information.

🚀 Solution

The AI Loss Prevention System creates a controlled organizational knowledge layer.

                    COMPANY DATA
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
                  DATA INGESTION
                         │
                         ▼
                 PRIVACY / PII
                         │
                         ▼
                 KNOWLEDGE MEMORY
                         │
                         ▼
                VECTOR REPRESENTATION
                         │
                         ▼
                     RETRIEVAL
                         │
                         ▼
                 AUTHORIZATION
                         │
                         ▼
                   AI ASSISTANT

The system aims to make organizational knowledge:

Discoverable

Useful

Private

Permission-aware

Grounded

Preserved

✨ Features

Feature

Description

🏠 Landing Page

Product introduction and entry point

👥 Role Selection

Employee, Manager and HR workflows

🔐 Authentication

User ID, password and role verification

👨‍💻 Employee Dashboard

Personal projects, tasks and knowledge

👔 Manager Dashboard

Team, projects, tasks and activity

🧑‍💼 HR Dashboard

Organization-level overview

📋 Task Management

Assignment, priority, status and due dates

📁 Project Management

Projects, members and status

🧠 Knowledge Management

Structured organizational knowledge

🤖 AI Assistant

Natural-language enterprise knowledge access

🔎 RAG

Retrieval-grounded AI responses

🛡️ PII Protection

Privacy-aware processing

🔒 Role-Based Access

Authorized information access

📊 Activity Tracking

Project and task activity

🔌 Data Collectors

GitHub, Slack, Email and Meetings

🏗️ Architecture

High-Level Architecture

┌───────────────────────────────────────────────────────────┐
│                       FRONTEND                            │
│                                                           │
│ Landing → Role Selection → Login → Dashboard             │
│                                                           │
│ Employee        Manager              HR                   │
└─────────────────────────────┬─────────────────────────────┘
                              │
                              │ REST / HTTP
                              ▼
┌───────────────────────────────────────────────────────────┐
│                        API LAYER                           │
│                                                           │
│ Auth │ Employee │ Manager │ HR │ Projects │ Tasks │ AI   │
└───────────────┬──────────────────────────┬────────────────┘
                │                          │
                ▼                          ▼
      ┌──────────────────┐        ┌──────────────────┐
      │   PostgreSQL     │        │     ChromaDB     │
      │                  │        │                  │
      │ Users            │        │ Embeddings       │
      │ Projects         │        │ Vector Search    │
      │ Tasks            │        │ Retrieval        │
      │ Knowledge        │        │ RAG              │
      └──────────────────┘        └─────────┬────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │   AI AGENTS     │
                                  │                 │
                                  │ Retrieval Agent │
                                  │ Answer Agent    │
                                  │ Knowledge Agent │
                                  │ Privacy Agent   │
                                  └─────────────────┘

🔄 User Flow

Landing Page
     │
     ▼
Role Selection
     │
 ┌───┼───────────┐
 ▼   ▼           ▼
EMP MGR          HR
 │   │           │
 └───┼───────────┘
     ▼
   Login
     │
     ▼
Authentication
     │
     ▼
Authorized Dashboard

👥 Role-Based Experience

👨‍💻 Employee

Employee
   │
   ├── Projects
   ├── Tasks
   ├── Knowledge
   ├── Activity
   └── AI Assistant

Employees receive a personalized view of their authorized work and knowledge.

👔 Manager

Manager
   │
   ├── Employees
   ├── Projects
   ├── Tasks
   ├── Team Knowledge
   ├── Activity
   └── AI Assistant

Managers receive team and project-level visibility.

🧑‍💼 HR

HR
 │
 ├── Employee Overview
 ├── Project Overview
 ├── Task Overview
 ├── Organization Activity
 ├── Knowledge Overview
 └── AI Assistant

🤖 AI and RAG

The AI layer uses Retrieval-Augmented Generation.

Instead of asking an LLM to answer entirely from its internal knowledge, the system first retrieves relevant organizational information.

User Question
      │
      ▼
Query Processing
      │
      ▼
Embedding
      │
      ▼
Vector Search
      │
      ▼
Relevant Knowledge
      │
      ▼
Permission / Privacy Filter
      │
      ▼
Context
      │
      ▼
LLM
      │
      ▼
Grounded Answer

Example

User:
"Why was PostgreSQL retained instead of MongoDB?"

        ↓

Retrieval Agent

        ↓

Relevant organizational decisions

        ↓

Answer Agent

        ↓

Grounded response

🚫 Negative RAG

A critical requirement is handling questions where the knowledge base does not contain enough information.

Without negative RAG

User Question
      ↓
No relevant knowledge
      ↓
LLM guesses
      ↓
❌ Hallucinated answer

With negative RAG

User Question
      ↓
Retrieval
      ↓
Is sufficient evidence available?
      │
 ┌────┴────┐
 │         │
YES       NO
 │         │
 ▼         ▼
Answer   "No sufficient
         knowledge found."

This makes the assistant safer and more trustworthy for enterprise use.

🛡️ Privacy and Loss Prevention

Privacy is implemented as a separate processing layer.

RAW DATA
   │
   ▼
PII DETECTION
   │
   ▼
SENSITIVE ENTITY CHECK
   │
   ▼
ANONYMIZATION / HASHING
   │
   ▼
SAFE REPRESENTATION
   │
   ▼
STORAGE
   │
   ▼
RETRIEVAL
   │
   ▼
AUTHORIZATION CHECK
   │
   ▼
AI

Privacy-related components include:

PII Detector

Presidio Service

Anonymizer

Hashing Service

Entity Merger

Privacy Agent

Storage Agent

🔐 Security Model

The intended security flow is:

Authentication
      │
      ▼
Role Validation
      │
      ▼
Authorization
      │
      ▼
Privacy Filtering
      │
      ▼
Knowledge Retrieval
      │
      ▼
AI Response

A key design principle is:

Authentication does not automatically grant access to every piece of organizational knowledge.

📥 Knowledge Sources

🐙 GitHub

Used for technical and repository-related knowledge.

Examples:

Technical decisions

Repository information

Engineering context

💬 Slack

Used for:

Discussions

Decisions

Problem solving

Team communication

📧 Email

Used for:

Organizational communication

Approvals

Decisions

Relevant business context

🎙️ Meetings

The meeting pipeline can process:

Recording
   ↓
Transcript
   ↓
Speaker Mapping
   ↓
Knowledge Extraction
   ↓
Meeting Summary
   ↓
Knowledge Representation

☁️ Google Drive

A Google Drive connector is included for document-based organizational knowledge.

🧠 Knowledge Model

Knowledge records contain fields such as:

┌────────────────────────────┐
│         KNOWLEDGE          │
├────────────────────────────┤
│ ID                         │
│ Title                      │
│ Summary                    │
│ Category                   │
│ Confidence                 │
│ Timestamp                  │
│ Employee Hash              │
│ Manager Hash               │
│ Vector ID                  │
└────────────────────────────┘

🗄️ Database

The project uses PostgreSQL for structured application data.

Core entities

Users
  │
  ├──────────────┐
  │              │
Projects       Tasks
  │              │
  │              │
  └──── Project Employees

Knowledge
   │
   └── Identity Mapping

Main tables

Table

Purpose

users

Authentication and roles

knowledge

Organizational knowledge

tasks

Task assignments and status

projects

Project information

project_employees

Project membership

identity_mapping

Identity/hash relationships

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
│   │   ├── email.py
│   │   ├── github.py
│   │   ├── meeting.py
│   │   └── slack.py
│   │
│   ├── connectors/
│   │   └── google_drive.py
│   │
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

🧰 Technology Stack

Layer

Technologies

Frontend

React, Vite, JSX, CSS

Backend

Python, FastAPI, SQLAlchemy, Pydantic

Database

PostgreSQL

Vector DB

ChromaDB

AI

RAG, Embeddings, AI Agents

Privacy

Presidio, PII Detection, Anonymization, Hashing

Integrations

GitHub, Slack, Email, Google Drive, Meetings

⚡ Quick Start

1. Clone

git clone <YOUR_REPOSITORY_URL>
cd AI_PRE_LOSS_SYSTEM

2. Frontend

cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173

3. Backend

Create a Python environment:

python -m venv venv

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r backend/requirements.txt

Run the configured API:

python -m backend_56.api

Swagger:

http://127.0.0.1:8000/docs

🔑 Development Authentication

⚠️ LOCAL DEVELOPMENT ONLY

Role

ID

👨‍💻 Employee

EMP001

👔 Manager

MANAGER001

🧑‍💼 HR

HR001

Passwords should remain local and must never be committed to GitHub.

Production should use secure company authentication such as SSO/OAuth.

🧪 Testing

Authentication

Employee login

Manager login

HR login

Password verification

Role validation

JWT/session

Token expiration

Protected routes

Logout

Dashboards

Employee dashboard

Manager dashboard

HR dashboard

Projects

Tasks

Activity

Knowledge information

AI

Retrieval Agent

Answer Agent

Vector search components

Final dashboard assistant integration

Full negative-RAG evaluation

Retrieval quality evaluation

Privacy

PII detection component

Presidio integration

Anonymization component

Hashing service

End-to-end privacy validation

📊 Current Status

Product Foundation

Module

Status

Landing Page

✅ Complete

Role Selection

✅ Complete

Basic Authentication

✅ Complete

Employee Dashboard

✅ Complete

Manager Dashboard

✅ Complete

HR Dashboard

✅ Complete

Backend APIs

🟡 In Progress

Database

✅ Complete

Project Management

✅ Complete

Task Management

✅ Complete

AI and Security

Module

Status

Retrieval Agent

✅ Implemented

Answer Agent

✅ Implemented

Vector Search

✅ Implemented

AI Assistant Integration

🟡 In Progress

RAG Finalization

🟡 In Progress

Negative RAG

🟡 In Progress

Privacy Pipeline

🟡 In Progress

JWT Security

⏳ Next

Protected Routes

⏳ Next

Logout

⏳ Next

Full Testing

⏳ Pending

🛣️ Roadmap

Phase 1 — Product Foundation

Frontend

Landing Page

Role Selection

Login

Employee Dashboard

Manager Dashboard

HR Dashboard

Phase 2 — Core Backend

PostgreSQL

Projects

Tasks

Activity

Knowledge APIs

Authentication API

Phase 3 — AI Knowledge

Retrieval Agent

Answer Agent

Embedding components

Vector database

Final RAG evaluation

Negative RAG hardening

Phase 4 — Security

Password hashing

Role validation

PII detection components

Anonymization components

JWT

Protected routes

Logout

Complete authorization testing

Phase 5 — Enterprise Intelligence

GitHub collector

Slack collector

Email collector

Meeting pipeline

Google Drive connector

Final ingestion orchestration

Permission-aware retrieval

Phase 6 — Production

Company SSO

OAuth configuration

Secret management

HTTPS

Monitoring

Production deployment

🔒 Git and Secrets

Sensitive files are intentionally excluded from version control.

Examples:

.env
*.env
client_secret.json
drive_token.json
token.json
__pycache__/
*.pyc
chroma_db/
local state
local meeting data

Never commit

❌ API keys
❌ Passwords
❌ OAuth secrets
❌ Access tokens
❌ Private certificates
❌ Production credentials
❌ Private company data

🚨 Enterprise Security

Production deployment should introduce:

Company Identity Provider
          │
          ▼
       SSO / OAuth
          │
          ▼
     JWT / Session
          │
          ▼
 Role-Based Authorization
          │
          ▼
    Privacy Filtering
          │
          ▼
     RAG / Retrieval
          │
          ▼
      AI Assistant

Additional production requirements:

HTTPS

Secure secret management

Database migrations

Monitoring

Logging

Rate limiting

Access auditing

Backup strategy

Strong authentication

MFA where appropriate

🔮 Future Enhancements

🧠 Knowledge Graph

Create relationships between:

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

📊 Advanced RAG Evaluation

Measure:

Retrieval recall

Retrieval precision

Context relevance

Answer faithfulness

Hallucination rate

Citation accuracy

🚨 Knowledge Loss Alerts

Detect:

Undocumented decisions

Repeated questions

Missing project documentation

Critical employee knowledge

Knowledge gaps

🤝 Knowledge Transfer

When an employee changes role or leaves:

Employee Knowledge
        ↓
Knowledge Extraction
        ↓
Privacy Filtering
        ↓
Validation
        ↓
Organizational Memory

🌟 Why This Project?

This is not simply another chatbot.

The system combines:

             ORGANIZATIONAL KNOWLEDGE
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
          Privacy   Retrieval  Access
             │         │         │
             └─────────┼─────────┘
                       ▼
                  AI ASSISTANT

Key principles

Knowledge should not be lost.

Sensitive information should not be exposed unnecessarily.

AI should answer from evidence.

Users should only access authorized information.

When evidence is missing, the system should say so.

🏁 Project Vision

The long-term goal is to create an organization's AI-powered knowledge memory.

                 COMPANY KNOWLEDGE
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
                    Privacy
                         │
                         ▼
                 Knowledge Memory
                         │
                         ▼
                   Vector Search
                         │
                         ▼
                      RAG
                         │
                         ▼
                  Secure AI Agent
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
          Employee     Manager      HR

💬 Final Thought

Preserve Knowledge. Protect Privacy. Empower Teams.

The AI Loss Prevention System brings enterprise data, privacy engineering, retrieval, authorization, and AI together into one intelligent platform.

⭐ Project Status

Current milestone: Core platform + dashboards + knowledge/RAG foundation completed.

Next milestone: JWT security → protected routes → logout → final AI assistant → RAG hardening → privacy validation → complete testing.

🛡️ AI Loss Prevention System

Intelligent Enterprise Knowledge Management
