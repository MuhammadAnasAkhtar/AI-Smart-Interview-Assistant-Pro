// static/js/app.js
let currentSession = null;
let currentQuestionIndex = 0;
let totalQuestions = 0;
let timerInterval = null;
let seconds = 0;
let interviewConfig = {};

// Initialize question count slider
document.getElementById('question-count').addEventListener('input', function(e) {
    const value = e.target.value;
    document.getElementById('question-count-display').textContent = value;
});

function formatTime(secs) {
    const minutes = Math.floor(secs / 60);
    const seconds = secs % 60;
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

function startTimer() {
    seconds = 0;
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        seconds++;
        document.getElementById('timer').textContent = formatTime(seconds);
    }, 1000);
}

function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}

async function startInterview() {
    const jobRole = document.getElementById('job-role').value;
    const experienceLevel = document.getElementById('experience-level').value;
    const questionCount = parseInt(document.getElementById('question-count').value);

    interviewConfig = { jobRole, experienceLevel, questionCount };

    // Show loading section
    document.getElementById('setup-section').classList.add('hidden');
    document.getElementById('loading-section').classList.remove('hidden');
    document.getElementById('generating-for').textContent = 
        `${experienceLevel} ${jobRole} (${questionCount} questions)`;

    try {
        const response = await fetch('/start_interview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                job_role: jobRole,
                experience_level: experienceLevel,
                question_count: questionCount
            })
        });

        const data = await response.json();
        currentSession = data.session_id;
        
        // Poll for question generation completion
        checkQuestionGeneration();
        
    } catch (error) {
        console.error('Error starting interview:', error);
        alert('Error starting interview session');
        showSection('setup-section');
    }
}

async function checkQuestionGeneration() {
    if (!currentSession) return;

    try {
        const response = await fetch(`/interview_status/${currentSession}`);
        const data = await response.json();
        
        if (data.questions_ready) {
            // Questions are ready, start interview
            currentQuestionIndex = 0;
            totalQuestions = data.total_questions;
            
            showSection('interview-section');
            document.getElementById('current-question').textContent = data.first_question;
            updateProgress();
            updateInterviewInfo();
            startTimer();
            
        } else {
            // Continue polling
            setTimeout(checkQuestionGeneration, 2000);
        }
    } catch (error) {
        console.error('Error checking question status:', error);
        setTimeout(checkQuestionGeneration, 2000);
    }
}

function updateInterviewInfo() {
    document.getElementById('info-role').textContent = interviewConfig.jobRole;
    document.getElementById('info-level').textContent = interviewConfig.experienceLevel;
    document.getElementById('info-count').textContent = totalQuestions;
}

function updateProgress() {
    const progress = ((currentQuestionIndex) / totalQuestions) * 100;
    document.getElementById('progress-percentage').textContent = `${Math.round(progress)}%`;
    document.getElementById('progress-bar').style.width = `${progress}%`;
    document.getElementById('progress-text').textContent = 
        `Question ${currentQuestionIndex + 1} of ${totalQuestions}`;
    document.getElementById('current-q-number').textContent = currentQuestionIndex + 1;
}

async function submitAnswer() {
    const answer = document.getElementById('user-answer').value.trim();
    
    if (!answer) {
        alert('Please provide an answer before submitting.');
        return;
    }

    try {
        const response = await fetch('/submit_answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: currentSession,
                question_index: currentQuestionIndex,
                answer: answer
            })
        });

        const data = await response.json();
        
        // Display AI feedback
        displayAIFeedback(data.feedback);
        
        if (data.interview_complete) {
            showFinalResults(data);
        } else {
            // Move to next question
            currentQuestionIndex = data.current_question_index;
            document.getElementById('current-question').textContent = data.next_question;
            document.getElementById('user-answer').value = '';
            updateProgress();
            startTimer();
        }
        
    } catch (error) {
        console.error('Error submitting answer:', error);
        alert('Error submitting answer');
    }
}

function displayAIFeedback(feedback) {
    const feedbackContent = document.getElementById('feedback-content');
    const scores = feedback.scores;
    
    feedbackContent.innerHTML = `
        <div class="space-y-6">
            <!-- Score Grid -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="bg-blue-50 p-4 rounded-xl text-center border-2 border-blue-100">
                    <div class="text-2xl font-bold text-blue-600">${scores.content_score}</div>
                    <div class="text-sm font-semibold text-blue-800 mt-1">Content</div>
                    <div class="text-xs text-blue-600 mt-1">Quality</div>
                </div>
                <div class="bg-purple-50 p-4 rounded-xl text-center border-2 border-purple-100">
                    <div class="text-2xl font-bold text-purple-600">${scores.technical_score}</div>
                    <div class="text-sm font-semibold text-purple-800 mt-1">Technical</div>
                    <div class="text-xs text-purple-600 mt-1">Depth</div>
                </div>
                <div class="bg-green-50 p-4 rounded-xl text-center border-2 border-green-100">
                    <div class="text-2xl font-bold text-green-600">${scores.communication_score}</div>
                    <div class="text-sm font-semibold text-green-800 mt-1">Communication</div>
                    <div class="text-xs text-green-600 mt-1">Clarity</div>
                </div>
                <div class="bg-orange-50 p-4 rounded-xl text-center border-2 border-orange-100">
                    <div class="text-2xl font-bold text-orange-600">${scores.relevance_score}</div>
                    <div class="text-sm font-semibold text-orange-800 mt-1">Relevance</div>
                    <div class="text-xs text-orange-600 mt-1">To Role</div>
                </div>
            </div>
            
            <!-- Overall Score -->
            <div class="bg-gradient-to-r from-blue-500 to-purple-500 p-4 rounded-xl text-white text-center">
                <div class="text-sm font-semibold mb-1">OVERALL QUESTION SCORE</div>
                <div class="text-4xl font-bold">${scores.overall_question_score}/10</div>
            </div>
            
            <!-- AI Assessment -->
            <div class="bg-gray-50 border-l-4 border-gray-400 p-4 rounded-lg">
                <h4 class="font-semibold text-gray-800 mb-2 flex items-center">
                    <i class="fas fa-robot mr-2"></i>AI Assessment
                </h4>
                <p class="text-gray-700">${feedback.overall_assessment}</p>
            </div>
            
            <!-- Improvement Suggestions -->
            <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-lg">
                <h4 class="font-semibold text-yellow-800 mb-3 flex items-center">
                    <i class="fas fa-lightbulb mr-2"></i>Improvement Suggestions
                </h4>
                <ul class="list-disc list-inside space-y-2 text-yellow-700">
                    ${feedback.improvement_suggestions.map(suggestion => 
                        `<li class="flex items-start">
                            <i class="fas fa-chevron-right text-yellow-500 mt-1 mr-2 text-xs"></i>
                            ${suggestion}
                         </li>`
                    ).join('')}
                </ul>
            </div>
        </div>
    `;
}

function showFinalResults(data) {
    stopTimer();
    showSection('results-section');
    
    const finalResults = document.getElementById('final-results');
    
    finalResults.innerHTML = `
        <!-- Overall Score -->
        <div class="text-center mb-8">
            <div class="text-6xl font-bold text-green-600 mb-2">${data.overall_score}/10</div>
            <div class="text-2xl text-gray-600">Overall Interview Score</div>
        </div>
        
        <!-- Category Scores -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div class="bg-blue-50 p-4 rounded-xl text-center border-2 border-blue-200">
                <div class="text-2xl font-bold text-blue-600">${data.category_scores.content_score}</div>
                <div class="text-sm font-semibold text-blue-800 mt-1">Content</div>
            </div>
            <div class="bg-purple-50 p-4 rounded-xl text-center border-2 border-purple-200">
                <div class="text-2xl font-bold text-purple-600">${data.category_scores.technical_score}</div>
                <div class="text-sm font-semibold text-purple-800 mt-1">Technical</div>
            </div>
            <div class="bg-green-50 p-4 rounded-xl text-center border-2 border-green-200">
                <div class="text-2xl font-bold text-green-600">${data.category_scores.communication_score}</div>
                <div class="text-sm font-semibold text-green-800 mt-1">Communication</div>
            </div>
            <div class="bg-orange-50 p-4 rounded-xl text-center border-2 border-orange-200">
                <div class="text-2xl font-bold text-orange-600">${data.category_scores.relevance_score}</div>
                <div class="text-sm font-semibold text-orange-800 mt-1">Relevance</div>
            </div>
        </div>
        
        <!-- Performance Feedback -->
        <div class="bg-gradient-to-r from-blue-500 to-purple-500 p-6 rounded-2xl text-white">
            <h3 class="text-xl font-bold mb-4 text-center">Performance Summary</h3>
            <div class="space-y-3">
                ${data.performance_feedback.map(feedback => `
                    <div class="flex items-start">
                        <i class="fas fa-star text-yellow-300 mt-1 mr-3"></i>
                        <span class="text-lg">${feedback}</span>
                    </div>
                `).join('')}
            </div>
        </div>
        
        <!-- Stats -->
        <div class="text-center text-gray-600 bg-gray-50 p-4 rounded-xl">
            <i class="fas fa-chart-bar mr-2"></i>
            You completed ${data.total_questions} AI-generated questions in this interview session.
        </div>
    `;
}

function showSection(sectionId) {
    // Hide all sections
    document.getElementById('setup-section').classList.add('hidden');
    document.getElementById('loading-section').classList.add('hidden');
    document.getElementById('interview-section').classList.add('hidden');
    document.getElementById('results-section').classList.add('hidden');
    
    // Show target section
    document.getElementById(sectionId).classList.remove('hidden');
}

function restartInterview() {
    currentSession = null;
    currentQuestionIndex = 0;
    totalQuestions = 0;
    stopTimer();
    
    showSection('setup-section');
    
    // Reset feedback content
    document.getElementById('feedback-content').innerHTML = `
        <div class="text-center text-gray-500 py-8">
            <i class="fas fa-robot text-4xl mb-3 opacity-50"></i>
            <p class="text-lg">Your AI-powered feedback will appear here</p>
            <p class="text-sm mt-2">After you submit your first answer</p>
        </div>
    `;
}