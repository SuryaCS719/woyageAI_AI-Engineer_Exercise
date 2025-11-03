# Interview Follow-up Question Generator

A FastAPI-based backend service that uses OpenAI's GPT models to generate intelligent, context-aware follow-up questions for interviews in real-time.

## Overview

This application helps interviewers conduct better interviews by automatically generating relevant follow-up questions based on:
- The original interview question
- The candidate's response
- The role being interviewed for (optional)
- The type of interview (optional)

## Features

- **RESTful API** built with FastAPI
- **OpenAI Integration** using GPT-4o-mini for intelligent question generation
- **Input Validation** with Pydantic models
- **Safety Rails** to ensure professional, unbiased questions
- **Comprehensive Error Handling** for robust operation
- **Interactive API Documentation** via Swagger UI
- **Production-Ready** with proper logging and configuration management

## Requirements

- Python 3.8+
- OpenAI API Key

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SuryaCS719/woyageAI_AI-Engineer_Exercise.git
   cd woyageAI_AI-Engineer_Exercise
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

## Usage

### Starting the Server

Run the application using uvicorn:

```bash
python main.py
```

Or alternatively:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

### API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### API Endpoint

#### POST `/interview/generate-followups`

Generate a follow-up question based on interview context.

**Request Body:**

```json
{
  "question": "Tell me about a time you handled conflicting priorities.",
  "answer": "In my last role, we had two urgent client requests. I triaged by impact, aligned stakeholders, and delivered...",
  "role": "Senior Backend Engineer",
  "interview_type": "Behavioral interview"
}
```

**Parameters:**
- `question` (required): The interviewer's original question
- `answer` (required): The candidate's response
- `role` (optional): Target role/title for context
- `interview_type` (optional): Interview type for context

**Response (200 OK):**

```json
{
  "result": "success",
  "message": "Follow-up question generated.",
  "data": {
    "followup_question": "Looking back, what would you change about your triage approach?",
    "rationale": "This question helps assess the candidate's ability to reflect critically on their decisions and identify areas for improvement."
  }
}
```

**Error Response (4xx/5xx):**

```json
{
  "result": "error",
  "message": "Error description",
  "data": null
}
```

## Example Usage with cURL

```bash
curl -X POST "http://localhost:8000/interview/generate-followups" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Tell me about a time you handled conflicting priorities.",
    "answer": "In my last role, we had two urgent client requests. I triaged by impact, aligned stakeholders, and delivered the higher-impact feature first.",
    "role": "Senior Backend Engineer",
    "interview_type": "Behavioral interview"
  }'
```

## Example Usage with Python

```python
import requests

url = "http://localhost:8000/interview/generate-followups"
payload = {
    "question": "Tell me about a time you handled conflicting priorities.",
    "answer": "In my last role, we had two urgent client requests. I triaged by impact, aligned stakeholders, and delivered the higher-impact feature first.",
    "role": "Senior Backend Engineer",
    "interview_type": "Behavioral interview"
}

response = requests.post(url, json=payload)
print(response.json())
```

## Safety Features

The application includes several safety rails to ensure professional and unbiased question generation:

- Avoids questions about protected characteristics (age, race, religion, etc.)
- Prevents personal questions unrelated to job performance
- Ensures questions are open-ended and professional
- Focuses on behavioral patterns, decision-making, and job-relevant skills

## Project Structure

```
.
├── main.py              # FastAPI application with endpoint implementation
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Configuration

Environment variables (configure in `.env`):

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key (required) | - |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

## Error Handling

The API handles various error scenarios:

- **400 Bad Request**: Invalid input (empty fields, whitespace-only strings)
- **500 Internal Server Error**: Server configuration issues
- **503 Service Unavailable**: OpenAI API errors or unavailability

## Technical Implementation

### Key Technologies:
- **FastAPI**: Modern, high-performance web framework
- **Pydantic**: Data validation using Python type hints
- **OpenAI API**: GPT-4o-mini for question generation
- **python-dotenv**: Environment variable management

### Prompt Engineering:
The system uses carefully crafted prompts with:
- Clear role definition for the AI
- Specific output format requirements
- Safety guidelines and constraints
- Context-aware question generation

### API Design:
- RESTful endpoint design
- JSON request/response format
- Comprehensive validation
- Structured error responses

## Development

### Running Tests

You can test the endpoint using the interactive Swagger UI at `/docs` or programmatically using the examples above.

### Code Quality

The code follows Python best practices:
- Type hints for better code clarity
- Comprehensive docstrings
- Proper error handling
- Environment-based configuration
- Clean separation of concerns
---

**Submitted by:** Surya
