# IntelliCRM – AI-Powered HCP Relationship Management System

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent_Framework-purple.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue.svg)
![Groq](https://img.shields.io/badge/Groq-LLM_API-orange.svg)

## Overview

**IntelliCRM** is an AI-powered Healthcare Professional (HCP) Relationship Management System designed to help pharmaceutical teams efficiently manage interactions, conversations, and insights related to healthcare professionals.

The system combines **Large Language Models (LLMs)**, **agent workflows**, and **structured data management** to create an intelligent assistant capable of understanding HCP interactions and providing meaningful insights.

The project uses **LangGraph** to build an AI agent workflow, **FastAPI** for backend APIs, **PostgreSQL** for persistent data storage, and **Groq-powered LLM inference** for fast AI responses.

---

## Key Features

### 🤖 AI-Powered Assistant

* Intelligent conversational assistant powered by LLMs
* Uses LangGraph for structured AI agent workflows
* Context-aware responses based on stored information

### 🏥 HCP Relationship Management

* Manage healthcare professional interactions
* Store and retrieve relationship data
* Maintain structured HCP information

### ⚡ Fast Backend APIs

* Built using FastAPI
* Modular backend architecture
* RESTful API design

### 🧠 Agent-Based Architecture

* LangGraph-based AI workflow
* Separation of AI logic and API layers
* Extensible agent pipeline

### 🗄️ Persistent Database

* PostgreSQL database integration
* Environment-based configuration
* Scalable data storage design

---

## System Architecture

```
                User
                 |
                 |
            FastAPI Backend
                 |
                 |
        ---------------------
        |                   |
   LangGraph Agent       PostgreSQL
        |
        |
     ChatGroq LLM
```

---

## Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn

### AI / LLM

* LangGraph
* LangChain
* ChatGroq
* Groq LLM API

### Database

* PostgreSQL

### Configuration

* Environment variables
* Python dotenv

---

## Project Structure

```
pharma-ai-assistant/

├── backend/
│   |
│   ├── app/
│   │   |
│   │   ├── agent/
│   │   │   ├── graph.py
│   │   │   ├── llm.py
│   │   │   └── ...
│   │   |
│   │   ├── routes/
│   │   |
│   │   └── main.py
│   |
│   ├── requirements.txt
│   └── .env
│
├── README.md
└── .gitignore
```

---

# Installation and Setup

## 1. Clone Repository

```bash
git clone https://github.com/<your-username>/pharma-ai-assistant.git

cd pharma-ai-assistant
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file inside the backend directory:

```env
GROQ_API_KEY=your_groq_api_key

DATABASE_URL=postgresql://username:password@localhost:5432/hcp_crm
```

---

## 5. Setup PostgreSQL Database

Create database:

```sql
CREATE DATABASE hcp_crm;
```

Update your database credentials inside `.env`.

---

## 6. Run Application

Navigate to backend:

```bash
cd backend
```

Start FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

API documentation:

```
http://127.0.0.1:8000/docs
```

---

# API Overview

| Endpoint | Method | Description               |
| -------- | ------ | ------------------------- |
| `/`      | GET    | Health check              |
| `/docs`  | GET    | Swagger API documentation |

(More endpoints will be added as the system evolves.)

---

# AI Workflow

The AI assistant follows an agent-based workflow:

1. User sends a query
2. FastAPI receives request
3. LangGraph manages the reasoning flow
4. ChatGroq generates AI response
5. PostgreSQL stores required information
6. Response is returned to the user

---

# Future Improvements

Planned enhancements:

* [ ] HCP profile management
* [ ] Interaction history tracking
* [ ] AI-generated relationship summaries
* [ ] Document/RAG-based knowledge retrieval
* [ ] Authentication and authorization
* [ ] Frontend dashboard
* [ ] Analytics and reporting
* [ ] Cloud deployment

---

# Security Notes

* API keys are stored using environment variables
* Sensitive credentials are excluded from GitHub
* `.env` files should never be committed

---

# Author

**Alina Iram**

Computer Science Engineering Graduate
AI/ML & Cloud Computing Enthusiast
