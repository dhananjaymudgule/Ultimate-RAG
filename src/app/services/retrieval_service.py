# src/app/services/retrieval_service.py

from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from typing import List, Dict, Optional

from src.app.services.vector_store import pc_vector_store  
from src.app.core.config import settings
from src.app.utils.logger import logger

# get the correct retriever 
def get_retriever(retriever_name: str):
    
    try:
        if retriever_name == "pinecone":
            return pc_vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            )
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


