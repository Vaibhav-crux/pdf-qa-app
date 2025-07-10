# 📚 Knowledge Assistant

A Django-based application for uploading PDF documents, processing them into a searchable knowledge base, and answering questions using a language model (Google Gemini API) and ChromaDB.

---

## 🧭 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [API Documentation (Swagger)](#api-documentation-swagger)
- [Authentication](#authentication)
- [Logging](#logging)
- [Security and Rate Limiting](#security-and-rate-limiting)
- [Troubleshooting](#troubleshooting)

---

## 📘 Project Overview

Knowledge Assistant is a web application built with **Django** and **Django REST Framework** that enables authenticated users to:

- Upload PDF documents (max 10MB).
- Convert PDFs into embeddings stored in **ChromaDB**.
- Ask questions in natural language powered by **Google’s Gemini API**.
- Log all interactions for auditing and debugging.

Optimized for performance and built with best practices in mind (auth, rate limiting, Swagger docs, etc.).

---

## ✨ Features

- **PDF Upload** via token-authenticated API
- **Natural Language Q&A** from PDF content
- **ChromaDB Integration** for semantic retrieval
- **Token Authentication** via Django admin
- **Rate Limiting** (uploads/questions per IP)
- **Logging** of all requests/responses
- **Unit Testing** for endpoints
- **Swagger UI** for API docs
- **Security-first** configurations

---

## 📁 Project Structure

```

pdf-qa-app
├── .venv/                    # Virtual environment
├── knowledge\_assistant/      # Django project
│   ├── settings.py           # Security, logging, Swagger
│   ├── urls.py               # Routing
│   ├── wsgi.py
├── api/                      # API logic
│   ├── models.py             # Document, InteractionLog models
│   ├── views.py              # API views
│   ├── urls.py               # API routes
│   ├── serializers.py
│   ├── llm.py                # Google Gemini API integration
│   ├── utils.py              # PDF + ChromaDB utilities
│   ├── signals.py
├── media/documents/          # PDF storage
├── logs/django.log           # Application logs
├── tests/                    # Unit tests
├── .env                      # Environment config
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md

````

---

## 🛠️ Prerequisites

- Python 3.8+
- ChromaDB server running on `localhost:8000`
- Google Gemini API key
- Virtual environment setup
- Django admin access

---

## ⚙️ Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Vaibhav-crux/pdf-qa-app.git
   cd pdf-qa-app
   ```

2. **Create and Activate Virtual Environment**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate     # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file:

   ```env
   GOOGLE_API_KEY=your_google_api_key
   DJANGO_SECRET_KEY=your_django_secret
   HF_HUB_DISABLE_SYMLINKS_WARNING=true
   ```

5. **Create Required Directories**

   ```bash
   mkdir -p media/documents logs
   ```

6. **Run Migrations**

   ```bash
   python manage.py migrate
   ```

7. **Create Superuser**

   ```bash
   python manage.py createsuperuser
   ```

8. **Start ChromaDB Server**
   In a separate terminal:

   ```bash
   chroma run --host localhost --port 8000
   ```

9. **Start Django Server**

   ```bash
   python manage.py runserver
   ```

> Visit: [http://localhost:8000/](http://localhost:8000/)

---

## 🔗 API Endpoints

All API endpoints require **Token Authentication** and are **rate-limited**.

### 1. Upload Document

* **POST** `/api/upload-document/`
* **Auth Required**: Yes
* **Rate Limit**: 5 requests/min/IP
* **Request (form-data)**:

  * `file_name`: String
  * `file`: PDF (max 10MB)

**Example**:

```bash
curl -X POST http://localhost:8000/api/upload-document/ \
-H "Authorization: Token <your-token>" \
-F "file_name=MyDoc.pdf" \
-F "file=@/path/to/MyDoc.pdf"
```

**Success**:

```json
{
  "message": "Document uploaded and processed successfully",
  "file_name": "MyDoc.pdf"
}
```

---

### 2. Ask Question

* **POST** `/api/ask-question/`
* **Auth Required**: Yes
* **Rate Limit**: 10 requests/min/IP
* **Request (JSON)**:

  * `question`: String

**Example**:

```bash
curl -X POST http://localhost:8000/api/ask-question/ \
-H "Authorization: Token <your-token>" \
-H "Content-Type: application/json" \
-d '{"question": "What is the use of mitochondria?"}'
```

**Success**:

```json
{
  "answer": "The mitochondria is known as the powerhouse of the cell...",
  "sources": ["Science_Class_IX.pdf - Page 3"]
}
```

---

## 📄 API Documentation (Swagger)

* URL: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
* OpenAPI Schema: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

Use Swagger UI to:

* Explore endpoints
* Test with input
* Use the `Authorize` button to add your token

---

## 🔐 Authentication

1. **Generate Token**

   * Visit: `http://localhost:8000/admin/`
   * Navigate to: `authtoken > tokens`
   * Copy your token (e.g., `9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`)

2. **Usage**

   * Use in header:

     ```
     Authorization: Token <your-token>
     ```

---

## 📝 Logging

* Logs saved in `logs/django.log`
* Includes request info, response times, and errors

**Example Log**:

```
INFO 2025-07-11 12:46:37 api Document processing completed in 15.23 seconds
```

---

## 🛡️ Security and Rate Limiting

* **Token Auth**: All sensitive endpoints
* **Rate Limits**:

  * Uploads: 5/min/IP
  * Questions: 10/min/IP
* **.env**: Sensitive configs like `GOOGLE_API_KEY`, `DJANGO_SECRET_KEY`
* **CSRF**: Disabled for API endpoints
* **Secure settings**: Production-ready flags are included (e.g., `SECURE_SSL_REDIRECT`)

---

## 🧯 Troubleshooting

| Issue                | Solution                                                      |
| -------------------- | ------------------------------------------------------------- |
| **Auth Errors**      | Ensure `Authorization` header has valid token                 |
| **Timeout**          | Check logs, reduce `max_chunks` in `utils.py`                 |
| **Bad Request**      | Ensure `file_name`, `file`, or `question` fields are provided |
| **ChromaDB Errors**  | Ensure server is running at port 8000                         |
| **Rate Limit (429)** | Wait 1 minute or adjust in `settings.py`                      |
| **Swagger Issues**   | Ensure `drf-spectacular` is installed and running             |

---