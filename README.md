# 🚀 AI Smart Interview Assistant Pro

<div align="center">

![AI Interview Assistant](https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge&logo=ai)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green?style=for-the-badge&logo=fastapi)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-purple?style=for-the-badge&logo=openai)

**Revolutionize your interview preparation with AI-powered coaching, real-time analysis, and personalized feedback**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [API Documentation](#-api-documentation) • [Contributing](#-contributing)

</div>

## 📋 Table of Contents

- [🌟 Overview](#-overview)
- [🚀 Features](#-features)
- [🛠️ Installation](#️-installation)
- [⚡ Quick Start](#-quick-start)
- [🎯 Usage](#-usage)
- [🔧 API Documentation](#-api-documentation)
- [🤖 How It Works](#-how-it-works)
- [📁 Project Structure](#-project-structure)
- [🛠️ Configuration](#️-configuration)
- [🧪 Testing](#-testing)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 🌟 Overview

The **AI Smart Interview Assistant Pro** is a cutting-edge platform that transforms interview preparation through artificial intelligence. It provides realistic interview simulations with comprehensive feedback across technical knowledge, communication skills, and behavioral responses.

### 🎯 What Problem Does It Solve?

- ❌ **Generic Questions**: Traditional interview prep uses static questions
- ❌ **No Real Feedback**: You don't know how you're performing
- ❌ **No Personalization**: One-size-fits-all approach
- ❌ **Stress Management**: No help with interview anxiety
- ❌ **Technical Practice**: Limited coding interview practice

### ✅ Our Solution

- 🎯 **AI-Generated Questions**: Dynamic, role-specific questions
- 📊 **Instant Feedback**: Real-time scoring and improvement suggestions
- 🎤 **Voice Analysis**: Speech clarity, pace, and confidence scoring
- 😌 **Stress Detection**: Webcam-based stress level monitoring
- 💻 **Live Coding**: Real-time code execution and review
- 📈 **Progress Tracking**: Comprehensive analytics and performance metrics

## 🚀 Features

### 🎯 Core Features

#### 1. 🤖 AI-Powered Question Generation
**Get INSTANT Role-Specific Questions:**
```python
# AI generates questions based on your role and experience
questions = await generate_ai_questions("software engineer", "senior", 15)
```
- **Dynamic Question Bank**: 100+ questions per role
- **Experience Level Customization**: Entry to Principal level
- **Real-time Generation**: Fresh questions every session
- **Multiple Domains**: Technical, Behavioral, Situational

#### 2. 📊 Intelligent Response Analysis
**Get INSTANT AI Feedback:**
```python
feedback = await analyze_response_with_ai(question, answer, role, level)
# Returns: content_score, technical_score, communication_score, suggestions
```
- **Multi-dimensional Scoring**: 5 different scoring categories
- **Specific Improvement Suggestions**: Actionable feedback
- **STAR Method Evaluation**: Situation-Task-Action-Result analysis
- **Technical Depth Assessment**: Role-specific technical evaluation

#### 3. 🎤 AI Voice Coach
**Get INSTANT Voice Analysis:**
```python
voice_analysis = await voice_analyzer.analyze_voice_response(audio_data)
# Returns: clarity_score, pace_score, confidence_score, filler_words_count
```
- **Speech Clarity Scoring**: How clear and understandable you sound
- **Pace Analysis**: Optimal speaking speed detection
- **Confidence Measurement**: Vocal confidence indicators
- **Filler Word Detection**: "Um", "Ah" counter with reduction tips
- **Real-time Recording**: Web-based voice recording and analysis

#### 4. 😌 Stress Analyzer
**Get INSTANT Stress Detection:**
```python
stress_analysis = stress_analyzer.analyze_stress_from_image(webcam_image)
# Returns: stress_level, body_language_score, relaxation_tips
```
- **Webcam-based Analysis**: Real-time stress level monitoring
- **Body Language Scoring**: Posture and presence evaluation
- **Personalized Relaxation Tips**: Context-aware stress management
- **Confidence Indicators**: Non-verbal communication assessment

#### 5. 💻 Code Playground
**Get INSTANT Code Execution:**
```python
execution_result = await code_playground.execute_code(code, "python")
code_analysis = await analyze_code_quality(code, "python")
```
- **Multi-language Support**: Python, JavaScript
- **Real-time Execution**: Live code running with output
- **AI Code Review**: Readability, efficiency, best practices scoring
- **Safety First**: Secure code execution environment

### 🎨 Advanced Features

- **🔗 WebSocket Support**: Real-time feature updates
- **📈 Progress Analytics**: Session-wise performance tracking
- **🎯 Role-Specific Evaluation**: Custom scoring for different job roles
- **⚡ Fast Performance**: Optimized for quick response times
- 
## 🛠️ Installation

### Prerequisites

- Python 3.8+
- OpenAI API Key
- Modern web browser with microphone and webcam support

### Step-by-Step Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/ai-interview-assistant.git
cd ai-interview-assistant
```

2. **Create Virtual Environment**
```bash
python -m venv interview_env
source interview_env/bin/activate  # On Windows: interview_env\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
```bash
# Create .env file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

### Required Dependencies

```txt
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
openai==1.3.0
python-dotenv==1.0.0
speechrecognition==3.10.0
opencv-python==4.8.1.78
numpy==1.24.3
aiohttp==3.9.1
Pillow==10.0.1
python-multipart==0.0.6
jinja2==3.1.2
```

## ⚡ Quick Start

**Get INSTANT Setup:**
```bash
# 1. Install and setup
git clone https://github.com/yourusername/ai-interview-assistant.git
cd ai-interview-assistant
pip install -r requirements.txt

# 2. Configure environment
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# 3. Run the application
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 4. Open browser and navigate to:
# http://localhost:8000
```

## 🎯 Usage

### Starting an Interview Session

1. **Select Your Preferences**
   - Choose job role (Software Engineer, Data Scientist, etc.)
   - Select experience level (Entry to Principal)
   - Set number of questions (5-100)
   - Enable smart features (Voice Coach, Stress Analyzer, Code Playground)

2. **AI Question Generation**
   - Watch as AI generates personalized questions in real-time
   - Questions tailored to your specific role and level

3. **Answer Questions**
   - Type your responses or use voice recording
   - For technical roles: Use the code playground
   - Get real-time stress and voice feedback

4. **Receive Comprehensive Feedback**
   - Instant scoring across multiple dimensions
   - Specific improvement suggestions
   - Performance analytics and progress tracking

### Example Workflow

```python
# 1. Start interview session
response = await client.post("/start_interview", json={
    "job_role": "software engineer",
    "experience_level": "senior", 
    "question_count": 10,
    "features": ["voice", "stress", "coding"]
})

# 2. Submit answers and get feedback
feedback = await client.post("/submit_answer", json={
    "session_id": session_id,
    "question_index": 0,
    "answer": "My system design approach...",
    "answer_type": "text"
})

# 3. Get real-time analysis
# Voice analysis, stress monitoring, and AI feedback provided automatically
```

## 🔧 API Documentation

### Core Endpoints

#### 🚀 Start Interview
**POST** `/start_interview`
```python
{
    "job_role": "string",           # Required
    "experience_level": "string",   # Required: entry|junior|mid-level|senior|lead  
    "question_count": "integer",    # Optional: 5-100, default: 10
    "features": ["string"]          # Optional: voice|stress|coding
}
```

**Get INSTANT Response:**
```json
{
    "session_id": "uuid-string",
    "status": "generating_questions",
    "message": "AI is generating personalized questions...",
    "question_count": 10,
    "features_available": ["voice", "stress", "coding"]
}
```

#### 📤 Submit Answer
**POST** `/submit_answer`
```python
{
    "session_id": "string",         # Required
    "question_index": "integer",    # Required
    "answer": "string",             # Required
    "answer_type": "string"         # Optional: text|voice|code, default: text
}
```

**Get INSTANT Feedback:**
```json
{
    "session_id": "uuid-string",
    "feedback": {
        "scores": {
            "content_score": 8.5,
            "technical_score": 9.0,
            "communication_score": 7.5,
            "relevance_score": 8.0,
            "example_quality": 7.0,
            "overall_question_score": 8.0
        },
        "improvement_suggestions": [
            "Provide more specific examples",
            "Use STAR method for structure",
            "Include quantitative results"
        ],
        "overall_assessment": "Strong technical answer with good examples",
        "strengths": ["Technical depth", "Clear explanation"],
        "areas_for_improvement": ["More specific metrics", "Better structure"]
    },
    "next_question": "Describe your experience with...",
    "interview_complete": false
}
```

#### 🎤 Voice Analysis
**POST** `/submit_voice_response`
```python
{
    "session_id": "string",
    "question_index": "integer", 
    "answer": "string",
    "audio_data": "base64-string"
}
```

**Get INSTANT Voice Analysis:**
```json
{
    "voice_analysis": {
        "clarity_score": 8.2,
        "pace_score": 7.8,
        "confidence_score": 8.0,
        "articulation_score": 8.5,
        "energy_level": 7.5,
        "filler_words_count": 3,
        "pause_frequency": 2,
        "suggestions": [
            "Speak slightly slower for clarity",
            "Reduce filler words",
            "Maintain consistent volume"
        ],
        "overall_voice_score": 8.0
    }
}
```

#### 💻 Code Execution
**POST** `/execute_code`
```python
{
    "session_id": "string",
    "question_index": "integer",
    "code": "string",
    "language": "string"  # python|javascript
}
```

**Get INSTANT Code Feedback:**
```json
{
    "execution_result": {
        "success": true,
        "output": "Hello, World!",
        "error": "",
        "execution_time": 0.15
    },
    "code_analysis": {
        "readability_score": 8.5,
        "efficiency_score": 9.0,
        "best_practices_score": 8.0,
        "maintainability_score": 8.5,
        "robustness_score": 7.5,
        "improvement_suggestions": [
            "Add error handling",
            "Use more descriptive variable names"
        ],
        "overall_assessment": "Well-structured and efficient code"
    }
}
```

### WebSocket Endpoints

#### 🔗 Real-time Features
**WebSocket** `/ws/{session_id}`

**Supported Messages:**
```javascript
// Stress Analysis
{
    "type": "stress_analysis",
    "image_data": "base64-webcam-image"
}

// Voice Analysis  
{
    "type": "voice_analysis",
    "audio_data": "base64-audio-data"
}
```

## 🤖 How It Works

### Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI        │    │   OpenAI GPT    │
│   (React/HTML)  │◄──►│   Backend        │◄──►│   AI Models     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │ WebSocket             │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Webcam/Mic    │    │   Voice Analysis │    │   Code Exec     │
│   (Browser)     │    │   Stress Analysis│    │   Environment   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### AI-Powered Question Generation

**Get INSTANT AI Magic:**
```python
async def generate_ai_questions(role: str, level: str, count: int):
    prompt = f"""
    Generate {count} professional questions for {level} {role}.
    Include technical, behavioral, and situational questions.
    Return as JSON list.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)
```

### Intelligent Response Analysis

**Get INSTANT Multi-dimensional Scoring:**
```python
async def analyze_response_with_ai(question, answer, role, level):
    scoring_criteria = {
        "content_score": "Answer relevance and completeness",
        "technical_score": "Technical accuracy and depth", 
        "communication_score": "Clarity and structure",
        "relevance_score": "Role-specific relevance",
        "example_quality": "Use of specific examples"
    }
    # AI analyzes and scores each dimension
```

## 📁 Project Structure

```
ai-interview-assistant/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables
├── static/
│   └── js/
│       └── app.js         # Frontend JavaScript
├── templates/
│   └── index.html         # Main frontend template
└── README.md              # This file
```

### Key Components

- **`main.py`**: Core FastAPI application with all endpoints
- **`VoiceAnalyzer`**: Speech analysis and feedback
- **`StressAnalyzer`**: Webcam-based stress detection  
- **`CodePlayground`**: Safe code execution environment
- **`InterviewState`**: Session management and state tracking
- **Frontend**: Responsive UI with real-time features

## 🛠️ Configuration

### Environment Variables

```bash
# .env file
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional configurations
INTERVIEW_MAX_QUESTIONS=100
VOICE_ANALYSIS_TIMEOUT=30
CODE_EXECUTION_TIMEOUT=15
```

### Supported Job Roles

- Software Engineer
- DevOps Engineer  
- Data Engineer
- Data Analyst
- Data Scientist
- Product Manager

### Experience Levels

- **Entry Level** (0-2 years)
- **Junior** (2-4 years) 
- **Mid-Level** (4-7 years)
- **Senior** (7+ years)
- **Lead/Principal** (10+ years)

## 🧪 Testing

### Manual Testing

1. **Start the application**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. **Test endpoints**
```bash
# Test interview start
curl -X POST "http://localhost:8000/start_interview" \
     -H "Content-Type: application/json" \
     -d '{"job_role":"software engineer","experience_level":"mid-level","question_count":5}'

# Test answer submission
curl -X POST "http://localhost:8000/submit_answer" \
     -H "Content-Type: application/json" \
     -d '{"session_id":"your-session-id","question_index":0,"answer":"Test answer"}'
```

### Feature Testing Checklist

- [ ] AI question generation
- [ ] Response analysis and scoring
- [ ] Voice recording and analysis
- [ ] Webcam stress detection
- [ ] Code execution and review
- [ ] Real-time WebSocket features
- [ ] Session management
- [ ] Error handling

## 🤝 Contributing

We love contributions! Here's how you can help:

### 🐛 Reporting Bugs

1. Use GitHub Issues to report bugs
2. Include detailed reproduction steps
3. Provide environment information

### 💡 Feature Requests

1. Open an issue with "Feature Request" label
2. Describe the use case and benefits
3. Discuss implementation approach

### 🔧 Development

1. **Fork the repository**
2. **Create a feature branch**
```bash
git checkout -b feature/amazing-feature
```

3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Development Setup

```bash
# 1. Fork and clone
git clone [https://github.com/MuhammadAnasAkhtar/AI-Recipe-Generator-Nutrition-Analyzer.git]

# 2. Create development branch
git checkout -b dev

# 3. Install development dependencies
pip install -r requirements.txt

# 4. Make changes and test
# 5. Commit and push
git commit -m "Add amazing feature"
git push origin dev
```

### Coding Standards

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings for all functions
- Include type hints
- Write tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT models that power question generation and analysis
- **FastAPI** team for the excellent web framework
- **Contributors** who help improve this project
- **Users** who provide valuable feedback and feature requests


## 🚀 Future Enhancements

- [ ] Multi-language support (questions and interface)
- [ ] Video recording and playback
- [ ] Peer review system
- [ ] Company-specific question banks
- [ ] Advanced analytics dashboard
- [ ] Mobile app version
- [ ] Integration with job platforms

