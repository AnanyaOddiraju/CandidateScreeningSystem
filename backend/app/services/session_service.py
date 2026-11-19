from sqlalchemy.orm import Session
from uuid import UUID

from app.models import (
    InterviewSession,
    InterviewQuestion,
    InterviewAnswer,
    Resume,
    JobRole,
    Candidate,
    utc_now
)

from app.services.interview_service import generate_question


def create_interview(
    db: Session,
    candidate_id: UUID,
    resume_id: UUID,
    job_role_id: UUID
):

    # Validate candidate and resume ownership
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.candidate_id == candidate_id,
        Resume.processing_status == "processed"
    ).first()

    if not resume:
        raise ValueError("Resume not found or not processed")

    role = db.get(JobRole, job_role_id)

    if not role:
        raise ValueError("Job role not found")

    candidate = db.get(Candidate, candidate_id)

    if not candidate:
        raise ValueError("Candidate not found")

    try:

        session = InterviewSession(
            candidate_id=candidate_id,
            resume_id=resume_id,
            job_role_id=job_role_id,
            status="active",
            started_at=utc_now()
        )

        db.add(session)
        db.flush()

        # Generate first question
        question_text = generate_question(
            resume_id=str(resume_id),
            job_role=role.title
        )

        question = InterviewQuestion(
            session_id=session.id,
            sequence_number=1,
            question_text=question_text
        )

        db.add(question)

        db.commit()
        db.refresh(session)

        return session, question

    except Exception:
        db.rollback()
        raise