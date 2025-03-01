from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from typing import List

router = APIRouter()

# Allowed file types
ALLOWED_EXTENSIONS = {
    "json", "pdf", "txt", "jpg", "jpeg", "png", "docx", "csv", "xls", "xlsx"
}

# Upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure upload directory exists

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

    return {"filename": file.filename, "content_type": file.content_type, "message": "File uploaded successfully!"}

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

    return {"message": "Files uploaded successfully!", "files": uploaded_files}
