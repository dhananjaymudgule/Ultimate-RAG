# Ultimate-RAG


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