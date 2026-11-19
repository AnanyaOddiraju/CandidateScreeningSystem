from openai import OpenAI
from app.core.config import settings
from app.services.rag_service import ResumeRAG


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

rag = ResumeRAG()


def generate_question(
    resume_id: str,
    job_role: str,
    previous_question: str | None = None,
    previous_answer: str | None = None
):

    query = (
        f"Generate a relevant interview question "
        f"for a {job_role} candidate."
    )

    if previous_answer:
        query += (
            f" Consider this previous answer: "
            f"{previous_answer}"
        )

    context = rag.retrieve(
        resume_id=resume_id,
        query=query
    )

    prompt = f"""
    You are an AI interview assistant.

    Job role: {job_role}

    Relevant resume context:
    {context}

    Previous question:
    {previous_question or "None"}

    Previous answer:
    {previous_answer or "None"}

    Instructions:
    1. Ask one clear question at a time.
    2. Focus on job-relevant skills and experience.
    3. Ask about projects and technologies mentioned
       in the resume.
    4. Do not assume skills that are not evidenced.
    5. Use follow-up questions when clarification
       would be useful.
    6. Do not ask about protected personal characteristics.
    7. Do not make hiring decisions.

    Return only the interview question.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",

        messages=[
            {
                "role": "system",
                "content": "You conduct structured, job-relevant interviews."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.4,

        max_tokens=200
    )

    return response.choices[0].message.content