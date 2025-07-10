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
    
    .results-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .score-display {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .score-excellent {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
    }
    
    .score-good {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        color: #856404;
    }
    
    .score-needs-improvement {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
    }
    
    .info-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
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
    overlay.style.cssText = `
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
    `;
    
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
    },
    {
        "question": "Which programming language is known as the 'language of the web'?",
        "options": ["Python", "JavaScript", "Java", "C++"],
        "correct": 1,
        "explanation": "JavaScript enables interactive web pages and runs in browsers."
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
        "correct": 3,
        "explanation": "The Pacific Ocean covers about 46% of the water surface."
    },
    {
        "question": "Who developed the theory of relativity?",
        "options": ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Stephen Hawking"],
        "correct": 1,
        "explanation": "Einstein revolutionized our understanding of space and time."
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
