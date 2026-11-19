from fastapi import APIRouter, HTTPException
from uuid import uuid4

from app.schemas.interview import (
    StartInterviewRequest,
    AnswerRequest
)

from app.api.resumes import resume_store

from app.services.interview_service import generate_question

router = APIRouter(
    prefix="/api/interviews",
    tags=["Interviews"]
)

# Temporary demo storage.
# Use PostgreSQL for real interview sessions.
sessions = {}


@router.post("/start")
def start_interview(
    request: StartInterviewRequest
):

    resume_id = str(request.resume_id)

    if resume_id not in resume_store:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    session_id = str(uuid4())

    question = generate_question(
        resume_id=resume_id,
        job_role=request.job_role
    )

    sessions[session_id] = {
        "resume_id": resume_id,
        "job_role": request.job_role,
        "current_question": question,
        "history": [],
        "status": "active"
    }

    return {
        "session_id": session_id,
        "question": question,
        "status": "active"
    }


@router.post("/answer")
def submit_answer(
    request: AnswerRequest
):

    session_id = str(request.session_id)

    session = sessions.get(session_id)

    if not session or session["status"] != "active":
        raise HTTPException(
            status_code=404,
            detail="Active interview not found"
        )

    previous_question = session["current_question"]

    session["history"].append({
        "question": previous_question,
        "answer": request.answer
    })

    next_question = generate_question(
        resume_id=session["resume_id"],
        job_role=session["job_role"],
        previous_question=previous_question,
        previous_answer=request.answer
    )

    session["current_question"] = next_question

    return {
        "session_id": session_id,
        "question": next_question
    }


@router.post("/{session_id}/end")
def end_interview(session_id: str):

    session = sessions.get(session_id)

    if not session or session["status"] != "active":
        raise HTTPException(
            status_code=404,
            detail="Active interview not found"
        )

    session["status"] = "completed"

    return {
        "session_id": session_id,
        "status": "completed",
        "responses": len(session["history"])
    }