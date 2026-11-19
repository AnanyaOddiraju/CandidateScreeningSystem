from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4

from app.services.resume_parser import extract_resume
from app.services.rag_service import ResumeRAG

router = APIRouter(prefix="/api/resumes", tags=["Resumes"])

# Temporary demo storage.
# Replace with PostgreSQL and private object storage.
resume_store = {}


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...)
):

    if file.size and file.size > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Resume exceeds 5 MB"
        )

    try:

        content = await file.read(5 * 1024 * 1024 + 1)

        if len(content) > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="Resume exceeds 5 MB"
            )

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Filename is required"
            )

        text = extract_resume(
            content,
            file.filename
        )

        resume_id = str(uuid4())

        rag.index_resume(
            resume_id,
            text
        )

        resume_store[resume_id] = {
            "filename": file.filename,
            "status": "processed"
        }

        return {
            "resume_id": resume_id,
            "filename": file.filename,
            "status": "processed"
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    finally:
        await file.close()