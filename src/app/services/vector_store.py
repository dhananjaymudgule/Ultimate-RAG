import os
import time
from uuid import uuid4
from pathlib import Path
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from src.app.core.config import settings
from src.app.utils.logger import logger

#  Initialize Pinecone
pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index_name = "career-advisory-service"

#  Ensure the index exists
existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)



#  Initialize Embedding Model # 768
gemini_embedding_model = GoogleGenerativeAIEmbeddings(
    model=settings.GEMINI_EMBEDDING_MODEL_NAME,
    google_api_key=settings.GEMINI_API_KEY
)

#  Connect to Pinecone
index = pc.Index(index_name)
pc_vector_store = PineconeVectorStore(index=index, embedding=gemini_embedding_model)



def store_document_embeddings(docs_with_metadata):
    """
    Extracts text from the document, generates embeddings, and stores them in Pinecone.
    """
    try:
        #  Generate unique UUIDs for each document
        uuids = [str(uuid4()) for _ in range(len(docs_with_metadata))]

        #  Store in Pinecone
        embedding_result = pc_vector_store.add_documents(documents=docs_with_metadata, ids=uuids)
        
        return {"message": "Embeddings stored successfully!", "total_docs": len(docs_with_metadata),
                "embedding_result":embedding_result}
    except Exception as e:
        logger.error(f"Error  : {str(e)}", exc_info=True)

        return {"error": str(e)}
    
