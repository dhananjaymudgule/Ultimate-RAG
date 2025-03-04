from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from typing import List
from src.app.core.config import settings  
from src.app.services.file_handler import process_uploaded_file  



router = APIRouter()

# Allowed file types
ALLOWED_EXTENSIONS = {
    "json", "pdf", "txt", "jpg", "jpeg", "png", "docx", "csv", "xls", "xlsx"
}

# Upload directory
UPLOAD_DIR = settings.UPLOAD_DIR  


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Uploads a single file and saves it in the uploads/ directory."""
    file_extension = file.filename.split(".")[-1].lower()

    # Validate file type
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_extension}")

    # Save the file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        processed_data = process_uploaded_file(file_path)
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "message": "File uploaded and processed successfully!",
            "processed_data": processed_data,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))

    # return {"filename": file.filename, "content_type": file.content_type, "message": "File uploaded successfully!"}

@router.post("/upload-multiple/")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """Uploads multiple files and saves them in the uploads/ directory."""
    uploaded_files = []
    
    for file in files:
        file_extension = file.filename.split(".")[-1].lower()

        # Validate file type
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")

        # Save the file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_files.append({"filename": file.filename, "content_type": file.content_type})

    
    try:
        processed_data = process_uploaded_file(file_path)
        uploaded_files.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "processed_data": processed_data,
        })
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))

    
    return {"message": "Files uploaded successfully!", "files": uploaded_files}
