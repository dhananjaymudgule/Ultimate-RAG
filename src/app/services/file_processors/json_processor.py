import json
from langchain_core.documents import Document  
from pathlib import Path

def convert_json_to_doc(file_path: Path):
    """
    Convert JSON file into LangChain Document objects with metadata.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)  

    # Ensure JSON is a list
    if not isinstance(json_data, list):
        raise ValueError("JSON file must contain a list of job profiles.")
    
    # Convert JSON data into LangChain document objects
    docs_with_metadata = [
        Document(
            page_content=json.dumps(job),
            metadata={
                "job_id": job.get("_id", {}).get("$oid"),
                "jobRole": job.get("jobRole"),
                "sector": job.get("sector"),
                "subSector": job.get("subSector"),
                "experienceLevel": job.get("experienceLevel"),
                "createdAt": (
                    job.get("createdAt", [{}])[0].get("$date") 
                    if isinstance(job.get("createdAt"), list) and job["createdAt"] 
                    else None
                ),
                "updatedAt": job.get("updatedAt", {}).get("$date"),
            }
        )
        for job in json_data
    ]

    return docs_with_metadata
