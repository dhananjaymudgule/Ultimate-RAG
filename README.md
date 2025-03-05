# Ultimate-RAG

## 📌 Overview
Ultimate-RAG is a **Retrieval-Augmented Generation (RAG) system** that enables intelligent document processing and query answering using **LLMs (Large Language Models)**. It allows users to **upload documents, embed them using Google’s text embedding model, store embeddings in a vector database (Pinecone), retrieve relevant documents, and generate responses** dynamically using different LLMs.

## 🚀 Features
- 📂 **File Uploading**: Supports various file types (JSON, PDF, CSV, etc.).
- 🏗 **Document Embedding**: Converts document content into vector embeddings for efficient retrieval.
- 🔎 **Document Retrieval**: Uses vector search (Pinecone, FAISS, Chroma) to find relevant content.
- 🧠 **AI-Powered Answers**: Uses LLMs like **Gemini, OpenAI, etc.** to generate responses.
- ✅ **Modular & Scalable**: Supports multiple embedding models and vector stores dynamically.
- 🌍 **Web UI**: Interactive frontend using **Streamlit**.

## 🏗 Directory Structure
```
ULTIMATE-RAG/
│── src/
│   │── app/
│   │   │── api/               # ✅ API routes
│   │   │   │── routes/
│   │   │   │   │── upload.py  # Handles file uploads
│   │   │   │   │── query.py   # Handles LLM queries
│   │   │   │── dependencies.py  # Dependency injection (if needed)
│   │   │── core/              # ✅ Core configurations
│   │   │   │── config.py      # App settings & environment variables
│   │   │── services/          # ✅ Business logic
│   │   │   │── vector_store.py # Vector database management
│   │   │   │── retrieval_service.py # Retrieval logic from Pinecone
│   │   │   │── query_service.py  # Query processing logic
│   │   │   │── file_processors/  # ✅ Handles file-specific processing
│   │   │   │   │── json_processor.py  # JSON processing logic
│   │   │   │   │── pdf_processor.py   # (Future) PDF processing logic
│   │   │   │── file_handler.py  # ✅ Detects file types & calls processors
│   │   │── prompts/            # ✅ Stores LLM prompts
│   │   │   │── prompt_templates.py # Defines system & human prompts
│   │   │── utils/              # ✅ Utility functions (if needed)
│   │── uploads/                # ✅ Stores uploaded files
│── streamlit_app/              # ✅ Frontend UI (Streamlit)
│   │── app.py                  # Streamlit interface
│── ultimate/                   # Virtual environment
│── .env                        # ✅ Environment variables
│── requirements.txt            # Dependencies
│── README.md                   # Project documentation
│── LICENSE                     # License file
│── .gitignore                  # Ignore unnecessary files
```

## 📦 Installation & Setup
### **1️⃣ Create Virtual Environment**
```bash
python -m venv ultimate
ultimate\Scripts\activate  # On Windows
source ultimate/bin/activate  # On Mac/Linux
```

### **2️⃣ Install Dependencies**
```bash
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

### **3️⃣ Set Up Environment Variables**
Create a `.env` file in the project root:
```
PINECONE_API_KEY=your_pinecone_api_key
GEMINI_API_KEY=your_google_gemini_api_key
EMBEDDING_MODEL_NAME=models/text-embedding-004
```

## 🏃‍♂️ Running the Project
### **1️⃣ Start FastAPI Backend**
```bash
uvicorn src.app.main:app --reload
```
- **Swagger UI (API Docs)** → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc UI** → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Health Check** → [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### **2️⃣ Start Streamlit Frontend**
```bash
cd streamlit_app
streamlit run app.py
```

## 🛠 API Endpoints
### **1️⃣ File Upload API** (`upload.py`)
| Method | Endpoint         | Description                  |
|--------|-----------------|------------------------------|
| `POST` | `/files/upload/` | Upload a single file         |
| `POST` | `/files/upload-multiple/` | Upload multiple files |

### **2️⃣ Query API** (`query.py`)
| Method | Endpoint      | Description               |
|--------|--------------|---------------------------|
| `POST` | `/query/ask` | Ask a question to the LLM |

## 🏗 Project Architecture
### **🔹 1️⃣ API Layer (`api/routes/`)**
- **`upload.py`** → Handles file uploads
- **`query.py`** → Processes user queries via LLM

### **🔹 2️⃣ Business Logic (`services/`)**
- **`query_service.py`** → Manages query processing & LLM calls
- **`retrieval_service.py`** → Fetches documents from vector DB
- **`vector_store.py`** → Handles storage/retrieval of embeddings

### **🔹 3️⃣ File Handling (`file_processors/`)**
- **`json_processor.py`** → Parses JSON files & extracts data
- **`pdf_processor.py`** → (Future) Extracts text from PDFs
- **`file_handler.py`** → Detects file type & calls processor

### **🔹 4️⃣ Prompt Management (`prompts/`)**
- **`prompt_templates.py`** → Stores system & human prompts

### **🔹 5️⃣ Utilities (`utils/`)**
- **`logger.py`** → Logs system activity
- **`dependencies.py`** → Handles dependency injection

## 🎯 Future Enhancements
- ✅ Add support for **PDF, CSV, and DOCX file processing**
- ✅ Implement **multi-vector database support (Weaviate, Qdrant, Milvus)**
- ✅ Support **multiple LLMs dynamically (OpenAI, Gemini, Cohere, etc.)**
- ✅ Improve **retrieval with advanced ranking algorithms (BM25, Hybrid Search)**



