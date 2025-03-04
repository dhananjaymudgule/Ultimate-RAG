# file_handler.py

from pathlib import Path
from src.app.services.file_processors.json_processor import convert_json_to_doc

def process_uploaded_file(file_path: Path):
    """
    Detects the file type and processes it accordingly.
    """
    file_path = Path(file_path)  # ✅ Convert string to Path object
    file_extension = file_path.suffix.lower()

    file_extension = file_path.suffix.lower()

    if file_extension == ".json":
        return convert_json_to_doc(file_path)
    elif file_extension == ".pdf":
        raise NotImplementedError("PDF processing not implemented yet.")
    elif file_extension == ".csv":
        raise NotImplementedError("CSV processing not implemented yet.")
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")
