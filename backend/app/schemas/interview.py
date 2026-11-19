from pydantic import BaseModel, Field
from uuid import UUID


class StartInterviewRequest(BaseModel):
    resume_id: UUID
    job_role: str = Field(min_length=2, max_length=100)


class AnswerRequest(BaseModel):
    session_id: UUID
    answer: str = Field(min_length=1, max_length=10000)


class InterviewResponse(BaseModel):
    session_id: UUID
    question: str