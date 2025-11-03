"""
FastAPI application for generating interview follow-up questions using OpenAI.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from openai import OpenAI, OpenAIError
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Interview Follow-up Question Generator",
    description="Generate intelligent follow-up questions for interviews using AI",
    version="1.0.0"
)

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


# Request/Response Models
class InterviewRequest(BaseModel):
    """Request model for interview follow-up generation."""
    question: str = Field(..., min_length=1, description="The interviewer's original question")
    answer: str = Field(..., min_length=1, description="The candidate's response")
    role: Optional[str] = Field(None, description="Target role/title for context")
    interview_type: Optional[str] = Field(None, description="Interview type for context")

    @validator('question', 'answer')
    def validate_not_empty(cls, v):
        """Ensure strings are not just whitespace."""
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or contain only whitespace")
        return v.strip()


class FollowUpData(BaseModel):
    """Data model for follow-up question."""
    followup_question: str


class InterviewResponse(BaseModel):
    """Response model for successful follow-up generation."""
    result: str = "success"
    message: str = "Follow-up question generated."
    data: FollowUpData


class ErrorResponse(BaseModel):
    """Response model for errors."""
    result: str = "error"
    message: str
    data: Optional[dict] = None


def create_system_prompt() -> str:
    """Create the system prompt with safety rails for OpenAI."""
    return """You are an expert interview coach helping interviewers ask better follow-up questions.

Your role:
- Generate ONE concise, relevant follow-up question based on the candidate's answer
- The question should dig deeper, probe for specifics, or explore related competencies
- Keep questions professional, respectful, and focused on job-relevant insights
- Questions should be open-ended and encourage detailed responses

Safety rails:
- Do NOT generate questions about protected characteristics (age, race, religion, etc.)
- Do NOT ask personal questions unrelated to job performance
- Do NOT be adversarial or trick the candidate
- Focus on behavioral patterns, decision-making, problem-solving, and technical skills

Output format:
Return ONLY the follow-up question text, nothing else. No explanations, no rationale, just the question."""


def create_user_prompt(request: InterviewRequest) -> str:
    """Create the user prompt with interview context."""
    context_parts = []

    if request.role:
        context_parts.append(f"Role: {request.role}")
    if request.interview_type:
        context_parts.append(f"Interview Type: {request.interview_type}")

    context = "\n".join(context_parts) if context_parts else "No additional context provided."

    return f"""Context:
{context}

Original Question:
{request.question}

Candidate's Answer:
{request.answer}

Generate one insightful follow-up question for the interviewer to ask next."""


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Interview Follow-up Question Generator",
        "version": "1.0.0"
    }


@app.post(
    "/interview/generate-followups",
    response_model=InterviewResponse,
    status_code=status.HTTP_200_OK,
    tags=["Interview"],
    responses={
        200: {"model": InterviewResponse, "description": "Follow-up question generated successfully"},
        400: {"model": ErrorResponse, "description": "Invalid input"},
        500: {"model": ErrorResponse, "description": "Server error"},
        503: {"model": ErrorResponse, "description": "OpenAI API unavailable"}
    }
)
async def generate_followup_questions(request: InterviewRequest):
    """
    Generate intelligent follow-up questions for interview conversations.

    This endpoint accepts an original interview question and the candidate's answer,
    then uses OpenAI to generate a relevant, insightful follow-up question.
    """
    try:
        # Validate OpenAI API key is configured
        if not os.getenv("OPENAI_API_KEY"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OpenAI API key not configured"
            )

        # Create prompts
        system_prompt = create_system_prompt()
        user_prompt = create_user_prompt(request)

        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.3,
            presence_penalty=0.3
        )

        # Extract the generated follow-up question
        followup_question = response.choices[0].message.content.strip()

        # Validate we got a meaningful response
        if not followup_question:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate follow-up question"
            )

        # Return successful response
        return InterviewResponse(
            result="success",
            message="Follow-up question generated.",
            data=FollowUpData(followup_question=followup_question)
        )

    except OpenAIError as e:
        # Handle OpenAI-specific errors
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "result": "error",
                "message": f"OpenAI API error: {str(e)}",
                "data": None
            }
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        # Handle unexpected errors
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "result": "error",
                "message": f"Unexpected error: {str(e)}",
                "data": None
            }
        )


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    uvicorn.run("main:app", host=host, port=port, reload=True)
