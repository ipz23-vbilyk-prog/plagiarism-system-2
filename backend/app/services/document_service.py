import os
import json
import shutil
from uuid import uuid4

from fastapi import UploadFile

from backend.app.services.text_extractor import extract_text
from backend.app.services.matching import check_plagiarism


UPLOAD_DIR = "uploads"
DB_FILE = "documents.json"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def load_db():
    if not os.path.exists(DB_FILE):
        return {}

    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


async def save_file(file: UploadFile):
    unique_name = f"{uuid4()}_{file.filename}"

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_name
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return file_path


async def process_document(
    file: UploadFile,
    username: str
):
    documents_db = load_db()

    file_path = await save_file(file)

    text = extract_text(file_path)

    if username not in documents_db:
        documents_db[username] = []

    user_documents = documents_db[username]

    result = check_plagiarism(
        new_text=text,
        existing_documents=user_documents
    )

    document = {
        "id": len(user_documents) + 1,
        "filename": file.filename,
        "filepath": file_path,
        "text": text,
        "similarity": result.get("similarity", 0),
        "level": result.get("level", "low")
    }

    user_documents.append(document)

    save_db(documents_db)

    return {
        "id": document["id"],
        "filename": document["filename"],
        "similarity": document["similarity"],
        "level": document["level"],
        "matches": result.get("matches", [])
    }


def get_history(username: str):
    documents_db = load_db()

    return documents_db.get(
        username,
        []
    )


def get_document_by_id(
    username: str,
    document_id: int
):
    documents_db = load_db()

    user_documents = documents_db.get(
        username,
        []
    )

    for doc in user_documents:
        if doc["id"] == document_id:
            return doc

    return None

def delete_document(
    username: str,
    document_id: int
):
    documents_db = load_db()

    user_documents = documents_db.get(
        username,
        []
    )

    for doc in user_documents:

        if doc["id"] == document_id:

            if os.path.exists(
                doc["filepath"]
            ):
                os.remove(
                    doc["filepath"]
                )

            user_documents.remove(doc)

            save_db(documents_db)

            return True

    return False