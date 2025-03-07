# src/app/services/retrieval_service.py

from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from typing import List, Dict, Optional

from src.app.services.vector_store import pc_vector_store  
from src.app.core.config import settings
from src.app.utils.logger import logger

search_type = "similarity"


import json
from pathlib import Path

CONFIG_JSON_PATH = Path("D:/Dhananjay/Pro/MyIdea/Ultimate-RAG/streamlit_app/config.json")

def load_config():
    if CONFIG_JSON_PATH.exists():
        with open(CONFIG_JSON_PATH, "r") as f:
            return json.load(f)
    return {"top_k": 2, "similarity_threshold": 0.75}  # Default values

# Load parameters
config = load_config()

# Use them in your retrieval/generation process
top_k = config["top_k"]
similarity_threshold = config["similarity_threshold"]

logger.info(f"Using Top-K: {top_k}, Similarity Threshold: {similarity_threshold}")


# get the correct retriever 
def get_retriever(retriever_name: str):
    
    try:
        if retriever_name == "pinecone":
            if search_type == "similarity_score_threshold":
                retriever = pc_vector_store.as_retriever(
                    search_type="similarity_score_threshold",
                    search_kwargs={'score_threshold': similarity_threshold, "k": top_k}
                    )
            else:
                retriever = pc_vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            )
            return retriever
        
        elif retriever_name == "chroma":
            chroma_vector_db = Chroma(
                collection_name="career_advisory",
                embedding_function=settings.EMBEDDING_MODEL
            )
            return chroma_vector_db.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            )
        elif retriever_name == "faiss":
            faiss_vector_db = FAISS.load_local("faiss_index", settings.EMBEDDING_MODEL)
            return faiss_vector_db.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            )
        
    except Exception as e:
        logger.error(f"Error retrieving : {str(e)}", exc_info=True)
        raise ValueError(f"Retriever `{retriever_name}` not supported")



#  `retrieve_documents()` function
def retrieve_documents(question: str, 
                       filters: Optional[Dict] = None, 
                       retriever_name: str = "pinecone") -> List[Document]:
    """
    Retrieves relevant documents from the specified vector store.
    """
    try:
        retriever = get_retriever(retriever_name)
        retrieved_docs = retriever.invoke(question, filter=filters if filters else {})
        return retrieved_docs
    except Exception as e:
        logger.error(f"Error retrieving documents '{question}': {str(e)}", exc_info=True)

        return f"Error retrieving documents: {str(e)}"


# retriever = vector_store.as_retriever(
#     search_type="mmr",
#     search_kwargs={"k": 1, "fetch_k": 2, "lambda_mult": 0.5},
# )
# retriever.invoke("thud")

# # Only retrieve documents that have a relevance score
# Above a certain threshold
