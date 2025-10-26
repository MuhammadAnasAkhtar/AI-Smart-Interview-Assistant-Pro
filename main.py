# main.py
from fastapi import FastAPI, HTTPException, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Optional, Any
from pydantic import BaseModel
import openai
import os
import uuid
import json
import asyncio
from dotenv import load_dotenv
import aiohttp

load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

class InterviewState(BaseModel):
    session_id: str
    job_role: str
    experience_level: str
    interview_questions: List[str]
    user_responses: List[Dict]
    feedback: List[Dict]
    current_question_index: int
    interview_complete: bool
    overall_score: float
    questions_generated: bool

class InterviewRequest(BaseModel):
    job_role: str
    experience_level: str
    question_count: int = 10  # Default to 10, can be up to 100

class UserResponse(BaseModel):
    session_id: str
    question_index: int
    answer: str

class FeedbackResponse(BaseModel):
    session_id: str
    feedback: Dict
    next_question: Optional[str]
    interview_complete: bool
    overall_score: Optional[float]

app = FastAPI(title="AI Smart Interview Assistant", version="2.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

interview_sessions = {}

async def generate_ai_questions(role: str, level: str, count: int = 10) -> List[str]:
    """Generate interview questions using OpenAI"""
    prompt = f"""
    Generate {count} professional interview questions for a {level} {role} position.
    Questions should cover:
    - Technical skills and knowledge
    - Behavioral and situational scenarios
    - Problem-solving approaches
    - Industry-specific challenges
    - Leadership and collaboration (for senior levels)
    
    Make questions specific, actionable, and relevant to real-world scenarios.
    Return only the questions as a JSON list.
    
    Role: {role}
    Level: {level}
    Count: {count}
    """
    
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert interview coach specializing in technical roles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        questions_text = response.choices[0].message.content
        # Parse the JSON response
        questions = json.loads(questions_text)
        return questions[:count]
        
    except Exception as e:
        print(f"OpenAI Error: {e}")
        # Fallback to template questions
        return await get_fallback_questions(role, level, count)

async def get_fallback_questions(role: str, level: str, count: int) -> List[str]:
    """Fallback question templates if OpenAI fails"""
    role_templates = {
        "devops engineer": [
            "Explain your experience with CI/CD pipeline implementation",
            "How do you handle infrastructure as code?",
            "Describe a production incident and how you resolved it",
            "What monitoring and alerting tools have you used?",
            "How do you ensure security in DevOps practices?",
            "Explain your experience with container orchestration",
            "Describe your approach to capacity planning",
            "How do you manage configuration across multiple environments?",
            "What's your experience with cloud platforms?",
            "How do you implement disaster recovery strategies?"
        ],
        "data engineer": [
            "Describe your experience with data pipeline architecture",
            "How do you ensure data quality and validation?",
            "Explain your ETL/ELT process design",
            "What's your experience with big data technologies?",
            "How do you handle data modeling and schema design?",
            "Describe your experience with data warehousing solutions",
            "How do you optimize query performance?",
            "What's your approach to data governance?",
            "Explain your experience with real-time data processing",
            "How do you handle data security and compliance?"
        ],
        "data analyst": [
            "Describe your data analysis process from raw data to insights",
            "What statistical methods do you commonly use?",
            "How do you ensure data accuracy in your reports?",
            "What visualization tools are you proficient with?",
            "Describe a complex analysis project you completed",
            "How do you handle missing or incomplete data?",
            "What's your experience with SQL and database querying?",
            "How do you communicate findings to non-technical stakeholders?",
            "Describe your experience with A/B testing analysis",
            "What metrics do you use to measure business impact?"
        ],
        "software engineer": [
            "Explain your system design approach for scalable applications",
            "How do you write maintainable and testable code?",
            "Describe your experience with different programming paradigms",
            "What's your approach to code reviews and technical feedback?",
            "How do you handle technical debt?",
            "Describe a challenging debugging experience",
            "What's your experience with microservices architecture?",
            "How do you ensure application security?",
            "Describe your testing strategy across different levels",
            "How do you stay updated with technology trends?"
        ],
        "data scientist": [
            "Describe your end-to-end machine learning project experience",
            "How do you validate and evaluate model performance?",
            "What's your approach to feature engineering?",
            "Explain your experience with different ML algorithms",
            "How do you handle imbalanced datasets?",
            "Describe your model deployment and monitoring process",
            "What's your experience with deep learning frameworks?",
            "How do you communicate model results to business stakeholders?",
            "What metrics do you use for model success?",
            "How do you ensure model fairness and ethics?"
        ]
    }
    
    questions = role_templates.get(role.lower(), [
        "Tell me about your experience and background",
        "What are your key strengths?",
        "Why are you interested in this position?",
        "Describe a challenging project you worked on",
        "How do you handle tight deadlines?",
        "What are your career goals?",
        "How do you approach problem-solving?",
        "Describe your experience working in teams",
        "How do you handle constructive criticism?",
        "What motivates you in your work?"
    ])
    
    # Repeat questions if needed to reach count
    while len(questions) < count:
        questions.extend(questions)
    
    return questions[:count]

async def analyze_response_with_ai(question: str, answer: str, role: str, level: str) -> Dict[str, Any]:
    """Analyze user response using OpenAI for detailed feedback"""
    prompt = f"""
    Analyze this interview response and provide detailed feedback.
    
    Job Role: {role} ({level} level)
    Question: {question}
    Candidate Answer: {answer}
    
    Provide feedback in the following format:
    - Content quality (0-10): How well does the answer address the question?
    - Technical depth (0-10): How technically accurate and detailed is the answer?
    - Communication (0-10): How clear, structured, and concise is the answer?
    - Relevance (0-10): How relevant is the answer to the specific role?
    
    Also provide 3-5 specific improvement suggestions and an overall assessment.
    
    Return as JSON with keys: content_score, technical_score, communication_score, 
    relevance_score, improvement_suggestions (list), overall_assessment (string).
    """
    
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert interview coach providing constructive feedback."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1500
        )
        
        feedback_text = response.choices[0].message.content
        feedback_data = json.loads(feedback_text)
        
        # Calculate overall score
        overall_score = (
            feedback_data["content_score"] + 
            feedback_data["technical_score"] + 
            feedback_data["communication_score"] + 
            feedback_data["relevance_score"]
        ) / 4
        
        return {
            "scores": {
                "content_score": round(feedback_data["content_score"], 1),
                "technical_score": round(feedback_data["technical_score"], 1),
                "communication_score": round(feedback_data["communication_score"], 1),
                "relevance_score": round(feedback_data["relevance_score"], 1),
                "overall_question_score": round(overall_score, 1)
            },
            "improvement_suggestions": feedback_data["improvement_suggestions"],
            "overall_assessment": feedback_data["overall_assessment"]
        }
        
    except Exception as e:
        print(f"OpenAI Analysis Error: {e}")
        return await get_fallback_feedback(question, answer)

async def get_fallback_feedback(question: str, answer: str) -> Dict[str, Any]:
    """Fallback feedback generation"""
    answer_length = len(answer.split())
    technical_terms = sum(1 for term in ["system", "design", "algorithm", "framework", "database", 
                                       "api", "microservices", "pipeline", "infrastructure", "model"] 
                         if term in answer.lower())
    
    return {
        "scores": {
            "content_score": min(10, answer_length / 20 + 5),
            "technical_score": min(10, technical_terms * 2 + 4),
            "communication_score": min(10, max(4, answer_length / 25 + 5)),
            "relevance_score": 7.0,
            "overall_question_score": 7.0
        },
        "improvement_suggestions": [
            "Provide more specific examples from your experience",
            "Use the STAR method (Situation, Task, Action, Result) to structure your answer",
            "Include quantitative results or metrics when possible",
            "Explain the technical concepts more clearly"
        ],
        "overall_assessment": "Good answer with room for improvement in providing specific examples and technical details."
    }

@app.post("/start_interview")
async def start_interview(request: InterviewRequest, background_tasks: BackgroundTasks):
    """Start a new interview session with AI-generated questions"""
    session_id = str(uuid.uuid4())
    
    initial_state = InterviewState(
        session_id=session_id,
        job_role=request.job_role,
        experience_level=request.experience_level,
        interview_questions=[],
        user_responses=[],
        feedback=[],
        current_question_index=0,
        interview_complete=False,
        overall_score=0.0,
        questions_generated=False
    )
    
    # Store session immediately
    interview_sessions[session_id] = initial_state
    
    # Generate questions in background
    background_tasks.add_task(
        generate_questions_for_session, 
        session_id, 
        request.job_role, 
        request.experience_level, 
        min(request.question_count, 100)  # Cap at 100 questions
    )
    
    return {
        "session_id": session_id,
        "status": "generating_questions",
        "message": "AI is generating personalized interview questions...",
        "question_count": min(request.question_count, 100)
    }

async def generate_questions_for_session(session_id: str, role: str, level: str, count: int):
    """Generate questions for a session and update state"""
    try:
        questions = await generate_ai_questions(role, level, count)
        
        if session_id in interview_sessions:
            interview_sessions[session_id].interview_questions = questions
            interview_sessions[session_id].questions_generated = True
            
    except Exception as e:
        print(f"Error generating questions for session {session_id}: {e}")

@app.get("/interview_status/{session_id}")
async def get_interview_status(session_id: str):
    """Get current interview status including question generation progress"""
    if session_id not in interview_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    state = interview_sessions[session_id]
    
    if not state.questions_generated:
        return {
            "status": "generating_questions",
            "message": "AI is still generating questions...",
            "questions_ready": False
        }
    
    return {
        "status": "ready",
        "questions_ready": True,
        "current_question_index": state.current_question_index,
        "total_questions": len(state.interview_questions),
        "interview_complete": state.interview_complete,
        "overall_score": state.overall_score,
        "first_question": state.interview_questions[0] if state.interview_questions else None
    }

@app.post("/submit_answer")
async def submit_answer(response: UserResponse):
    """Submit answer and get AI-powered feedback"""
    session_id = response.session_id
    
    if session_id not in interview_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    state = interview_sessions[session_id]
    
    if not state.questions_generated:
        raise HTTPException(status_code=400, detail="Questions are still being generated")
    
    # Store user response
    current_question = state.interview_questions[response.question_index]
    state.user_responses.append({
        "question_index": response.question_index,
        "question": current_question,
        "answer": response.answer
    })
    
    # Analyze response with AI
    ai_feedback = await analyze_response_with_ai(
        current_question, 
        response.answer, 
        state.job_role, 
        state.experience_level
    )
    
    # Store feedback
    feedback_entry = {
        "question": current_question,
        "user_answer": response.answer,
        **ai_feedback
    }
    state.feedback.append(feedback_entry)
    
    # Update question index
    state.current_question_index += 1
    
    # Check if interview is complete
    if state.current_question_index >= len(state.interview_questions):
        state.interview_complete = True
        # Calculate final scores
        final_scores = calculate_final_scores(state)
        state.overall_score = final_scores["overall_score"]
        
        return {
            "session_id": session_id,
            "feedback": feedback_entry,
            "interview_complete": True,
            **final_scores
        }
    else:
        next_question = state.interview_questions[state.current_question_index]
        return {
            "session_id": session_id,
            "feedback": feedback_entry,
            "next_question": next_question,
            "interview_complete": False,
            "current_question_index": state.current_question_index,
            "total_questions": len(state.interview_questions)
        }

def calculate_final_scores(state: InterviewState) -> Dict[str, Any]:
    """Calculate comprehensive final scores"""
    if not state.feedback:
        return {
            "overall_score": 0.0,
            "category_scores": {},
            "performance_feedback": ["No feedback available"],
            "total_questions": 0
        }
    
    # Calculate averages for each category
    categories = ["content_score", "technical_score", "communication_score", "relevance_score"]
    category_scores = {}
    
    for category in categories:
        scores = [feedback["scores"][category] for feedback in state.feedback]
        category_scores[category] = round(sum(scores) / len(scores), 1)
    
    overall_score = round(sum(category_scores.values()) / len(category_scores), 1)
    
    # Generate performance feedback
    performance_feedback = generate_performance_feedback(overall_score, category_scores)
    
    return {
        "overall_score": overall_score,
        "category_scores": category_scores,
        "performance_feedback": performance_feedback,
        "total_questions": len(state.feedback)
    }

def generate_performance_feedback(overall_score: float, category_scores: Dict[str, float]) -> List[str]:
    """Generate performance feedback based on scores"""
    feedback = []
    
    if overall_score >= 9:
        feedback.append("Outstanding performance! You demonstrate excellent expertise and communication skills.")
    elif overall_score >= 8:
        feedback.append("Strong performance with well-developed skills across all areas.")
    elif overall_score >= 7:
        feedback.append("Good performance with solid fundamentals and some standout areas.")
    elif overall_score >= 6:
        feedback.append("Satisfactory performance with clear areas for improvement.")
    else:
        feedback.append("Needs significant improvement in multiple areas.")
    
    # Category-specific feedback
    weakest_category = min(category_scores, key=category_scores.get)
    if category_scores[weakest_category] < 7:
        category_names = {
            "content_score": "content quality",
            "technical_score": "technical depth", 
            "communication_score": "communication skills",
            "relevance_score": "answer relevance"
        }
        feedback.append(f"Focus on improving your {category_names[weakest_category]}.")
    
    return feedback

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)