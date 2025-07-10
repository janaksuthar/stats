import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from datetime import datetime
import os
from typing import Dict, List, Any

# Configure page
st.set_page_config(
    page_title="Secure MCQ Exam System",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS for secure exam styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #dc3545 0%, #6f42c1 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .quiz-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border: 2px solid #dc3545;
    }
    
    .question-header {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #dc3545;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
    }
    
    .security-warning {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 3px solid #dc3545;
        border-radius: 10px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        color: #721c24;
        box-shadow: 0 4px 16px rgba(220, 53, 69, 0.3);
        text-align: center;
        font-weight: bold;
    }
    
    .lock-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.95);
        z-index: 10000;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: white;
        text-align: center;
    }
    
    .disabled-nav {
        opacity: 0.3;
        pointer-events: none;
        background: #6c757d !important;
    }
    
    .current-question {
        background: #dc3545 !important;
        color: white !important;
        border: 2px solid #dc3545 !important;
    }
    
    .future-question {
        background: #28a745 !important;
        color: white !important;
    }
    
    .no-reattempt-warning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 2px solid #ffc107;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
        color: #856404;
    }
    
    .exam-locked {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 3px solid #dc3545;
        padding: 3rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
    }
    
    .progress-bar-container {
        background: #e9ecef;
        border-radius: 10px;
        padding: 0.5rem;
        margin: 1rem 0;
    }
    
    .security-status {
        position: fixed;
        top: 10px;
        right: 10px;
        background: #dc3545;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-size: 0.9rem;
        font-weight: bold;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# Ultra-strict JavaScript for exam security
secure_exam_js = """
<script>
let tabSwitchCount = 0;
let isExamActive = true;
let examLocked = false;
let warningShown = false;

// Immediate tab switch detection and auto-submit
function handleTabSwitch() {
    if (isExamActive && !examLocked && !warningShown) {
        tabSwitchCount++;
        examLocked = true;
        warningShown = true;
        
        console.log('SECURITY BREACH: Tab switch detected!');
        
        // Show immediate warning
        showSecurityBreach();
        
        // Auto-submit immediately (no delay)
        setTimeout(() => {
            autoSubmitExam();
        }, 2000);
    }
}

// Security breach warning
function showSecurityBreach() {
    const overlay = document.createElement('div');
    overlay.className = 'lock-overlay';
    overlay.innerHTML = `
        <div style="background: white; padding: 3rem; border-radius: 15px; color: #dc3545; max-width: 500px;">
            <h1>🚨 SECURITY BREACH DETECTED!</h1>
            <h2>⚠️ TAB SWITCHING VIOLATION</h2>
            <p style="font-size: 1.2rem; margin: 2rem 0;">
                You have violated exam security protocols by switching tabs.
            </p>
            <div style="background: #f8d7da; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>EXAM WILL BE AUTO-SUBMITTED IN <span id="countdown">2</span> SECONDS</strong>
            </div>
            <p style="color: #721c24; font-weight: bold;">
                This incident has been logged and reported.
            </p>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    // Countdown
    let countdown = 2;
    const countdownElement = document.getElementById('countdown');
    const interval = setInterval(() => {
        countdown--;
        if (countdownElement) {
            countdownElement.textContent = countdown;
        }
        if (countdown <= 0) {
            clearInterval(interval);
        }
    }, 1000);
}

// Auto-submit exam function
function autoSubmitExam() {
    const url = new URL(window.location);
    url.searchParams.set('security_breach', 'true');
    url.searchParams.set('tab_switches', tabSwitchCount.toString());
    url.searchParams.set('timestamp', Date.now().toString());
    url.searchParams.set('auto_submit', 'true');
    
    // Force immediate submission
    window.location.href = url.toString();
}

// Enhanced event listeners for maximum security
document.addEventListener('visibilitychange', function() {
    if (document.hidden && isExamActive) {
        handleTabSwitch();
    }
});

window.addEventListener('blur', function() {
    if (isExamActive) {
        handleTabSwitch();
    }
});

window.addEventListener('focus', function() {
    if (examLocked) {
        handleTabSwitch();
    }
});

// Prevent browser back/forward navigation
history.pushState(null, null, document.URL);
window.addEventListener('popstate', function(event) {
    if (isExamActive) {
        history.pushState(null, null, document.URL);
        alert('Navigation is disabled during the exam!');
        handleTabSwitch();
    }
});

// Disable right-click completely
document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
    if (isExamActive) {
        alert('Right-click is disabled during the exam!');
    }
    return false;
});

// Disable all developer tools and shortcuts
document.addEventListener('keydown', function(e) {
    if (isExamActive) {
        // Disable F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+U, Ctrl+S, Ctrl+A, Ctrl+P
        if (e.keyCode === 123 || 
            (e.ctrlKey && e.shiftKey && (e.keyCode === 73 || e.keyCode === 74)) ||
            (e.ctrlKey && (e.keyCode === 85 || e.keyCode === 83 || e.keyCode === 65 || e.keyCode === 80)) ||
            e.keyCode === 116) { // F5 refresh
            e.preventDefault();
            alert('This action is disabled during the exam!');
            return false;
        }
    }
});

// Disable text selection
document.addEventListener('selectstart', function(e) {
    if (isExamActive) {
        e.preventDefault();
        return false;
    }
});

// Disable drag and drop
document.addEventListener('dragstart', function(e) {
    if (isExamActive) {
        e.preventDefault();
        return false;
    }
});

// Monitor for developer tools
let devtools = {open: false, orientation: null};
setInterval(function() {
    if (isExamActive && (window.outerHeight - window.innerHeight > 200 || window.outerWidth - window.innerWidth > 200)) {
        if (!devtools.open) {
            devtools.open = true;
            handleTabSwitch();
        }
    }
}, 500);

// Function to disable monitoring when exam is completed
function disableExamMonitoring() {
    isExamActive = false;
    console.log('Exam monitoring disabled');
}

// Make functions globally available
window.disableExamMonitoring = disableExamMonitoring;
window.isExamActive = isExamActive;

// Initialize security monitoring
if (isExamActive) {
    console.log('🔒 SECURE EXAM MODE ACTIVATED');
    console.log('⚠️ Tab switching will result in immediate auto-submission');
}

// Show security status
const securityStatus = document.createElement('div');
securityStatus.className = 'security-status';
securityStatus.innerHTML = '🔒 EXAM SECURED';
document.body.appendChild(securityStatus);
</script>
"""

# Enhanced quiz questions
QUIZ_QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct": 2,
        "explanation": "Paris is the capital and most populous city of France."
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct": 1,
        "explanation": "Mars appears red due to iron oxide on its surface."
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["African Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
        "correct": 1,
        "explanation": "Blue Whales can reach lengths of up to 100 feet."
    },
    {
        "question": "Who painted 'The Starry Night'?",
        "options": ["Picasso", "Van Gogh", "Da Vinci", "Monet"],
        "correct": 1,
        "explanation": "Painted by Vincent van Gogh in 1889."
    },
    {
        "question": "What is the chemical symbol for gold?",
        "options": ["Go", "Gd", "Au", "Ag"],
        "correct": 2,
        "explanation": "Au comes from the Latin word 'aurum'."
    }
]

def initialize_session_state():
    """Initialize session state variables"""
    if 'exam_started' not in st.session_state:
        st.session_state.exam_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'exam_completed' not in st.session_state:
        st.session_state.exam_completed = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'student_name' not in st.session_state:
        st.session_state.student_name = ""
    if 'student_id' not in st.session_state:
        st.session_state.student_id = ""
    if 'security_breaches' not in st.session_state:
        st.session_state.security_breaches = 0
    if 'auto_submitted' not in st.session_state:
        st.session_state.auto_submitted = False
    if 'exam_locked' not in st.session_state:
        st.session_state.exam_locked = False
    if 'attempt_made' not in st.session_state:
        st.session_state.attempt_made = False

def check_security_breach():
    """Check for security breaches and auto-submit"""
    try:
        query_params = st.query_params
        if query_params.get('security_breach') == 'true':
            if not st.session_state.exam_completed:
                st.session_state.auto_submitted = True
                st.session_state.security_breaches = int(query_params.get('tab_switches', '1'))
                st.session_state.exam_locked = True
                submit_exam()
                st.query_params.clear()
    except:
        pass

def submit_exam():
    """Submit the exam and calculate results"""
    if st.session_state.exam_completed:
        return
    
    st.session_state.exam_completed = True
    st.session_state.attempt_made = True
    st.session_state.end_time = datetime.now()
    
    # Calculate score
    correct_answers = 0
    total_questions = len(QUIZ_QUESTIONS)
    
    for i, question in enumerate(QUIZ_QUESTIONS):
        if i in st.session_state.user_answers:
            if st.session_state.user_answers[i] == question['correct']:
                correct_answers += 1
    
    st.session_state.score = correct_answers
    st.session_state.total_questions = total_questions
    st.session_state.percentage = (correct_answers / total_questions) * 100
    
    save_results_to_csv()

def save_results_to_csv():
    """Save exam results to CSV file"""
    try:
        duration = (st.session_state.end_time - st.session_state.start_time).total_seconds() / 60
        
        result_data = {
            'Student Name': st.session_state.student_name,
            'Student ID': st.session_state.student_id,
            'Start Time': st.session_state.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'End Time': st.session_state.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'Duration (minutes)': round(duration, 2),
            'Score': st.session_state.score,
            'Total Questions': st.session_state.total_questions,
            'Percentage': round(st.session_state.percentage, 2),
            'Security Breaches': st.session
