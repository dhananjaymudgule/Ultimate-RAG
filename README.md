# Ultimate-RAG



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
│── .gitignore                   # Ignore unnecessary files


python -m venv ultimate 

ultimate\Scripts\activate  

python.exe -m pip install --upgrade pip

pip install -r requirements.txt

# RUN FastAPI 
uvicorn src.app.main:app --reload


Swagger UI (API Docs) → Open http://127.0.0.1:8000/docs
Redoc UI → Open http://127.0.0.1:8000/redoc
Health Check → Visit http://127.0.0.1:8000/

streamlit run app.py  







---

## **📌  Directory Structure**
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
│── .gitignore                   # Ignore unnecessary files
```

---

## **🔹 overview**
### **1️⃣ Keep API Routes Inside `api/routes/`**
- **`upload.py`** → Handles file uploads  
- **`query.py`** → Handles queries  
- Keeps the **REST API layer clean**.

### **2️⃣ Use `services/` for Business Logic**
- **`query_service.py`** → Manages LLM queries  
- **`retrieval_service.py`** → Handles document retrieval  
- **`vector_store.py`** → Manages Pinecone vector database  
- **`file_handler.py`** → Determines file type and delegates processing  
- **`file_processors/`** → Stores different file processing logic (JSON, PDF, etc.)

### **3️⃣ Store LLM Prompts Separately in `prompts/`**
- **`prompt_templates.py`** → Keeps prompt structures separate from logic  
- Allows easy **customization** without modifying code.

### **4️⃣ Keep Configurations in `core/config.py`**
- Centralized environment variables like **API keys, database settings**  
- Avoids hardcoding values throughout the project.

---



