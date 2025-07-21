Sure! Here's your content formatted as a professional and clean `README.md` file for your GitHub repository:

# 📚 Knowledge Assistant  
A Django-based application for uploading PDF documents, processing them into a searchable knowledge base, answering questions using a language model (Google Gemini API) and ChromaDB, and reading document text in various voices with pause/resume functionality across sessions.

## 🧭 Table of Contents

- [📘 Project Overview](#-project-overview)  
- [✨ Features](#-features)  
- [📁 Project Structure](#-project-structure)  
- [🛠️ Prerequisites](#️-prerequisites)  
- [⚙️ Setup Instructions](#-setup-instructions)  
- [🔗 API Endpoints](#-api-endpoints)  
- [📄 API Documentation (Swagger)](#-api-documentation-swagger)  
- [🔐 Authentication](#-authentication)  
- [📝 Logging](#-logging)  
- [🛡️ Security and Rate Limiting](#️-security-and-rate-limiting)  
- [🧯 Troubleshooting](#️-troubleshooting)  

## 📘 Project Overview

**Knowledge Assistant** is a web application built with **Django** and **Django REST Framework** that enables authenticated users to:

- Upload PDF documents (max 10MB).
- Convert PDFs into embeddings stored in **ChromaDB**.
- Ask questions in natural language powered by **Google Gemini API**.
- Read document text in various voices using TTS with session-persistent pause/resume.
- Log all interactions for auditing and debugging.

🔒 Built with performance, security, and usability in mind.

## ✨ Features

- ✅ PDF Upload via token-authenticated API  
- 💬 Natural Language Q&A from PDF content  
- 🔊 Text-to-Speech with multiple voice options and session-persistent pause/resume  
- 🧠 ChromaDB Integration for semantic retrieval  
- 🔐 Token Authentication via Django admin  
- 🚫 Rate Limiting (uploads/questions per IP)  
- 🧾 Logging of all requests/responses  
- 🧪 Unit Testing for endpoints  
- 💻 Swagger UI for API docs  
- 🔒 Security-first configurations  

## 📁 Project Structure

```
pdf-qa-app
├── .venv/                    # Virtual environment
├── .env                      # Environment config
├── .gitignore
├── db.sqlite3
├── manage.py
├── requirements.txt
├── api/                      # API logic
│   ├── admin.py
│   ├── apps.py
│   ├── llm.py                # Google Gemini API integration
│   ├── models.py             # Document, InteractionLog models
│   ├── serializers.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py               # API routes
│   ├── utils.py              # PDF + ChromaDB + TTS utilities
│   ├── views.py              # API views
│   ├── __init__.py
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_interactionlog.py
│   │   ├── 0003_alter_interactionlog_user.py
│   │   ├── 0004_rename_created_at_interactionlog_timestamp_and_more.py
│   │   ├── __init__.py
├── chroma/                   # ChromaDB storage
│   ├── chroma.sqlite3
│   ├── c575fc4a-f2c4-4683-a736-5f7e933db530/
│   │   ├── data_level0.bin
│   │   ├── header.bin
│   │   ├── length.bin
│   │   ├── link_lists.bin
├── knowledge_assistant/       # Django project
│   ├── asgi.py
│   ├── settings.py           # Security, logging, Swagger
│   ├── urls.py               # Routing
│   ├── wsgi.py
│   ├── __init__.py
│   ├── chroma/
│   │   ├── chroma.sqlite3
│   │   ├── 1f198ee0-3a70-474b-9ca1-2d8748391bdb/
│   │   │   ├── data_level0.bin
│   │   │   ├── header.bin
│   │   │   ├── length.bin
│   │   │   ├── link_lists.bin
├── media/                    # PDF storage
│   ├── documents/
│   │   ├── Introduction-to-MS-Office.pdf
├── sample/                   # Sample PDFs
│   ├── Introduction-to-MS-Office.pdf
├── static/                   # Static files
│   ├── index.html
├── logs/                     # Application logs
│   ├── django.log
└── README.md
```

## 🛠️ Prerequisites

- Python 3.8+  
- ChromaDB server listening at `localhost:8000`  
- Google Gemini API key  
- Virtual environment setup  
- Django superuser access  
- Web browser with TTS support  

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Vaibhav-crux/pdf-qa-app.git
cd pdf-qa-app
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Configure `.env`

Create a `.env` file in the root:

```ini
GOOGLE_API_KEY=your_google_api_key
DJANGO_SECRET_KEY=your_django_secret
HF_HUB_DISABLE_SYMLINKS_WARNING=true
```

### 5. Create Necessary Directories

```bash
mkdir -p media/documents logs static
```

### 6. Run Database Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Start ChromaDB Server

```bash
chroma run --host localhost --port 8000
```

### 9. Run Django App

```bash
python manage.py runserver
```

Visit: [http://localhost:8000/](http://localhost:8000/)

## 🔗 API Endpoints

All endpoints require **Token Authentication** and are **rate-limited**.

### 1. Upload Document

- **POST** `/api/upload-document/`  
- **Auth:** Required  
- **Limit:** 5 requests/min/IP  

**Sample cURL:**

```bash
curl -X POST http://localhost:8000/api/upload-document/ \
  -H "Authorization: Token " \
  -F "file_name=MyDoc.pdf" \
  -F "file=@/path/to/MyDoc.pdf"
```

### 2. Ask a Question

- **POST** `/api/ask-question/`  
- **Auth:** Required  
- **Limit:** 10 requests/min/IP  

**Sample cURL:**

```bash
curl -X POST http://localhost:8000/api/ask-question/ \
  -H "Authorization: Token " \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the use of mitochondria?"}'
```

### 3. Read Document Text (TTS)

- **POST** `/api/read-document/`  
- **Auth:** Required  
- **Limit:** 10 requests/min/IP  

**Sample cURL:**

```bash
curl -X POST http://localhost:8000/api/read-document/ \
  -H "Authorization: Token " \
  -H "Content-Type: application/json" \
  -d '{"file_name": "MyDoc.pdf", "voice": "en-US-male", "start_page": 1, "resume": false}'
```

📌 **Note:**
- Supported TTS Voices: `en-US-male`, `en-US-female` (depends on browser)
- TTS progress persists across sessions (resume from last read point)

## 📄 API Documentation (Swagger)

- **Swagger UI:** [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)  
- **OpenAPI Schema:** [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

> Use the **Authorize** button in Swagger UI to add your Token.

## 🔐 Authentication

### Token Creation

Go to Django Admin:
```
http://localhost:8000/admin/
```

Navigate to:
```text
authtoken > tokens
```

Generate and copy your token:  
`Authorization: Token `

## 📝 Logging

Log File: `logs/django.log`  
Includes:
- Uploaded document details  
- Reading session data  
- Question and answer logs  
- Error stack traces  

**Example:**

```
INFO 2025-07-21 23:29:37 api Document reading started for MyDoc.pdf in en-US-male voice
```

## 🛡️ Security and Rate Limiting

- **Authentication:** Token required for major endpoints  
- **Rate Limits:**
  - Upload Document: 5/min/IP
  - Ask Question: 10/min/IP
  - Read Document: 10/min/IP
- **Environment Variables:** Secure keys in `.env`
- **CSRF:** Disabled for API calls (for backend API usage)
- **Use HTTPS in production!**

## 🧯 Troubleshooting

| Issue                 | Solution                                                                 |
|-----------------------|--------------------------------------------------------------------------|
| Auth Errors           | Ensure Authorization token is generated from admin panel                |
| Timeout Issues        | Check logs, consider reducing `max_chunks` in `utils.py`                 |
| 400 Bad Request       | Ensure payload and all request parameters are passed                     |
| ChromaDB Connection   | Make sure `chroma run` server is active on port `8000`                   |
| 429 Too Many Requests | Wait and retry after 1 minute                                            |
| Swagger Not Loading   | Ensure `drf-spectacular` is installed and configured properly            |
| TTS Not Working       | Ensure valid voice and supported browser used (e.g., Chrome, Edge)       |
| Resume Broken         | Ensure database is connected; check read tracking logic on resume        |
