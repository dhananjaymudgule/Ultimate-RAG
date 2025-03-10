# src/app/services/retrieval_service.py


from src.app.services.embedding_service import get_embedding_model
from src.app.core.config import settings
from src.app.utils.logger import logger

import json
from pathlib import Path
from uuid import uuid4
from typing import List, Dict, Optional

from langchain_core.documents import Document
from langchain_chroma import Chroma

google_embedding_model = get_embedding_model()


def intitialise_vector_store():

    chroma_vector_store = Chroma(
        collection_name="career_advisory_service",
        embedding_function=google_embedding_model,
        persist_directory=str(settings.CHROMA_DB_PATH),  
    )

    return chroma_vector_store

# initialise vector db
chroma_vector_db = intitialise_vector_store()

# get the correct retriever 
def get_retriever():
    """vector store retirival"""
    chroma_retriver =  chroma_vector_db.as_retriever(
                search_type="similarity",
                search_kwargs={"k": settings.TOP_K}
                )

    logger.info(f" Using Top-K: {settings.TOP_K}")
                
    return chroma_retriver


# store documents embeddings to vector db
def store_document_embeddings(docs_with_metadata):
    """
    Extracts text from the document, generates embeddings, and stores them in Pinecone.
    """
    try:
        #  Generate unique UUIDs for each document
        uuids = [str(uuid4()) for _ in range(len(docs_with_metadata))]

        #  Store in Pinecone
        embedding_result = chroma_vector_db.add_documents(documents=docs_with_metadata, ids=uuids)
        
        return {"message": "Embeddings stored successfully!", "total_docs": len(docs_with_metadata),
                "embedding_result":embedding_result}
    except Exception as e:
        logger.error(f"Error  : {str(e)}", exc_info=True)

        return {"error": str(e)}
    


# Retrive Docuements
def retrieve_documents(question: str, 
                       filters: Optional[Dict] = None) -> List[Document]:
    """
    Retrieves relevant documents from the specified vector store.
    """
    try:
        retriever = get_retriever()
        retrieved_docs = retriever.invoke(question)
        return retrieved_docs
    except Exception as e:
        logger.error(f"Error retrieving documents '{question}': {str(e)}", exc_info=True)

        return f"Error retrieving documents: {str(e)}"





if __name__ == "__main__":
    
    retriever = get_retriever()
    print(retriever)


