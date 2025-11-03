Here is the extracted text from the PDF, neatly formatted for prompt use with an LLM:

***

**Woyage AI - AI Engineer Exercise**

**Exercise 1**

**Task:**  
Build a FastAPI backend endpoint that accepts:
- the original interview question
- the candidate’s answer (text)

Then calls the OpenAI API to generate high-quality follow-up questions the interviewer can use immediately in the conversation.

**Objective:**  
Implement a POST API following the below standards. The endpoint should validate input, call OpenAI with a clear system prompt and safety rails, and return one or more concise, relevant follow-up questions with brief rationales.

**Request:**  
- Method: **POST**
- Path: **/interview/generate-followups**
- Content-Type: **application/json**

**Request Body (JSON):**
```json
{
  "question": "Tell me about a time you handled conflicting priorities.",
  "answer": "In my last role, we had two urgent client requests. I triaged by impact, aligned stakeholders, and delivered...",
  "role": "Senior Backend Engineer",
  "interview_type": "Behavioral interview"
}
```

- **question** (string, required): the interviewer’s original question.
- **answer** (string, required): the candidate’s response.
- **role** (string, optional): target role/title for context.
- **interview_type** (string, optional): interview type for context.

**Response:**  
- Status: **200 OK** on success
- Content-Type: **application/json**

**Response Body (JSON):**
```json
{
  "result": "success",
  "message": "Follow-up question generated.",
  "data": {
    "followup_question": "Looking back, what would you change about your triage approach?"
  }
}
```

**Deliverables:**  
- A professionally written code should be made available on GitHub. (No code by email.)

