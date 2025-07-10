import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import os

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
        box-shadow: 0 8px 32px rgba(0, 0极兔, 0.1);
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
        background: linear-gradient(135极, #fff3cd 0%, #ffeaa7 100%);
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
    
    .correct-answer {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(40, 167, 69, 0.1);
    }
    
    .incorrect-answer {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 5px solid #dc3545;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(220, 53, 69, 0.1);
    }
    
    .progress-section {
        background: #e9ecef;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .warning-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        color: #dc3545;
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

function handleTabSwitch() {
    if (isExamActive && !examLocked && !warningShown) {
        tabSwitchCount++;
        examLocked = true;
        warning极own = true;
        
        showSecurityBreach();
        
        // Auto-submit after 2 seconds
        setTimeout(() => {
            autoSubmitExam();
        }, 2000);
    }
}

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
            <div class="warning-icon">🚨</div>
            <h1>SECURITY BREACH DETECTED!</h1>
            <h2>TAB SWITCHING VIOLATION</h2>
            <p style="font-size: 1.2rem; margin: 2rem 0;">
                You have violated exam security protocols by switching windows/tabs.
            </p>
            <div style="background: #f8d7da; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong style="font-size: 1.3rem;">EXAM WILL BE AUTO-SUBMITTED IN <span id="countdown">2</span> SECONDS</strong>
            </div>
            <p style="color: #721c24; font-weight: bold;">
                This incident has been logged in the exam record.
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

function autoSubmitExam() {
    const url = new URL(window.location);
    url.searchParams.set('security_breach', 'true');
    url.searchParams.set('tab_switches', tabSwitchCount.toString());
    url.searchParams.set('timestamp', Date.now().toString());
    极rl.searchParams.set('auto_submit', 'true');
    
    window.location.href = url.toString();
}

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

history.pushState(null, null, document.URL);
window.addEventListener('popstate', function(event) {
    if (isExamActive) {
        history.pushState(null, null, document.URL);
        alert('Navigation is disabled during the exam!');
        handleTabSwitch();
    }
});

document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
    return false;
});

document.addEventListener('keydown', function(e) {
    if (isExamActive) {
        if (e.keyCode === 123 ||  // F12
            (e.ctrlKey && e.shiftKey && (e.keyCode === 73 || e.keyCode === 74)) ||  // Ctrl+Shift+I/J
            (e.ctrlKey && (e.keyCode === 85 || e.keyCode === 83 || e.keyCode === 65 || e.keyCode === 80)) ||  // Ctrl+U/S/A/P
            e.keyCode === 116) {  // F5
            e.preventDefault();
            alert('This action is disabled during the exam!');
            return false;
        }
    }
});

document.addEventListener('selectstart', function(e) {
    if (isExamActive) {
        e.preventDefault();
        return false;
    }
});

document.addEventListener('dragstart', function(e) {
    if (isExamActive) {
        e.preventDefault();
        return false;
    }
});

let devtools = {open: false, orientation: null};
setInterval(function() {
    if (isExamActive && (window.outerHeight - window.innerHeight > 200 || window.outerWidth - window.innerWidth > 200)) {
        if (!devtools.open) {
            devtools.open = true;
            handleTabSwitch();
        }
    }
}, 500);

function disableExamMonitoring() {
    isExamActive = false;
}

window.disableExamMonitoring = disableExamMonitoring;

if (isExamActive) {
    const securityStatus = document.createElement('div');
    securityStatus.style.cssText = `
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
    `;
    securityStatus.innerHTML = '🔒 EXAM SECURED';
    document.body.appendChild(securityStatus);
}
</script>
"""

# Quiz questions
QUIZ_QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct": 2,
        "explanation": "Paris is the capital and most populous city of France, located on the Seine River."
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct": 1,
        "explanation": "Mars appears red due to iron oxide prevalent on its surface."
    },
    {
        "question": "What is the largest mammal?",
        "options": ["African Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
        "correct": 1,
        "explanation": "Blue Whales can reach lengths of up to 100 feet and weigh up to 200 tons."
    },
    {
        "question": "Who painted 'The Starry Night'?",
        "options": ["Pablo Picasso", "Vincent van Gogh", "Leonardo da Vinci", "Claude Monet"],
        "correct": 1,
        "explanation": "Vincent van Gogh painted 'The Starry Night' in 1889 during his stay at an asylum."
    },
    {
        "question": "What is the chemical symbol for gold?",
        "options": ["Go", "Gd", "Au", "Ag"],
        "correct": 2,
        "explanation": "The symbol Au comes from the Latin word 'aurum' meaning 'shining dawn'."
    }
]

def initialize_session_state():
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
    if st.session_state.exam_completed:
        return
    
    st.session_state.exam_completed = True
    st.session_state.attempt_made = True
    st.session_state.end_time = datetime.now()
    
    # Calculate score
    correct_answers = 0
    for i, question in enumerate(QUIZ_QUESTIONS):
        if i in st.session_state.user_answers:
            if st.session_state.user_answers[i] == question['correct']:
                correct_answers += 1
    
    st.session_state.score = correct_answers
    st.session_state.total_questions = len(QUIZ_QUESTIONS)
    st.session_state.percentage = (correct_answers / len(QUIZ_QUESTIONS)) * 100
    
    save_results_to_csv()

def save_results_to_csv():
    try:
        duration = (st.session_state.end_time - st.session_state.start_time).total_seconds() / 60
        
        result_data = {
            'Student Name': st.session_state.student_name,
            'Student ID': st.session_state.student_id,
            'Start Time': st.session_state.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'End Time': st.session_state.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'Duration (min)': round(duration, 2),
            'Score': st.session_state.score,
            'Total Questions': st.session_state.total_questions,
            'Percentage': round(st.session_state.percentage, 2),
            'Security Breaches': st.session_state.security_breaches,
            'Auto Submitted': st.session_state.auto_submitted,
            'Submission Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add question-level detail
        for i, question in enumerate(QUIZ_QUESTIONS):
            user_answer = st.session_state.user_answers.get(i, -1)
            correct_answer = question['correct']
            result_data[f'Q{i+1}_User'] = question['options'][user_answer] if user_answer >= 0 else 'Not Answered'
            result_data[f'Q{i+1}_Correct'] = question['options'][correct_answer]
            result_data[f'Q{i+1}_Status'] = user_answer == correct_answer
        
        # Create and save DataFrame
        df = pd.DataFrame([result_data])
        csv_filename = 'secure_exam_results.csv'
        
        if os.path.exists(csv_filename):
            df.to_csv(csv_filename, mode='a', header=False, index=False)
        else:
            df.to_csv(csv_filename, index=False)
        
        st.session_state.csv_saved = True
    except Exception as e:
        st.error(f"Error saving results: {str(e)}")
        st.session_state.csv_saved = False

def get_grade(percentage):
    if percentage >= 90: return "A+"
    elif percentage >= 80: return "A"
    elif percentage >= 70: return "B"
    elif percentage >= 60: return "C"
    elif percentage >= 50: return "D"
    else: return "F"

def display_results():
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    
    st.subheader("📊 Exam Results Summary")
    
    # Score with grade and color coding
    score_class = "score-excellent" if st.session_state.percentage >= 80 else "score-good" if st.session_state.percentage >= 60 else "score-needs-improvement"
    grade = get_grade(st.session_state.percentage)
    
    st.markdown(f'''
    <div class="score-display {score_class}">
        Final Score: {st.session_state.score}/{st.session_state.total_questions}<br>
        Percentage: {st.session_state.percentage:.1f}%<br>
        Grade: {grade}
    </div>
    ''', unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.metric("🛡️ Security Breaches", st.session_state.security_breaches)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        duration = (st.session_state.end_time - st.session_state.start_time).total_seconds() / 60
        st.metric("⏱️ Duration (min)", f"{duration:.1f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.metric("⚡ Auto Submitted", "Yes" if st.session_state.auto_submitted else "No")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Question review
    st.subheader("📝 Question Review")
    for i, question in enumerate(QUIZ_QUESTIONS):
        user_answer = st.session_state.user_answers.get(i, -1)
        correct = user_answer == question['correct']
        
        with st.expander(f"Question {i+1}: {question['question']}", expanded=True):
            st.write(f"**Your answer:** {question['options'][user_answer] if user_answer >= 0 else 'Not answered'}")
            st.write(f"**Correct answer:** {question['options'][question['correct']]}")
            
            if correct:
                st.markdown('<div class="correct-answer">✅ Correct!</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="incorrect-answer">❌ Incorrect</div>', unsafe_allow_html=True)
            
            st.info(f"**Explanation:** {question['explanation']}")
    
    # Warning about re-attempts
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="no-reattempt-warning">', unsafe_allow_html=True)
    st.warning("🚨 RE-ATTEMPTS ARE NOT ALLOWED FOR THIS SECURE EXAM")
    st.write("For security reasons, each student can only take this exam once.")
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    initialize_session_state()
    check_security_breach()
    
    st.markdown('''
    <div class="main-header">
        <h1>🔒 Secure MCQ Exam System</h1>
        <p>Advanced Security Protocols | Automatic Violation Detection | No Re-Attempts</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Exam locked due to security breach
    if st.session_state.exam_locked:
        st.markdown('<div class="exam-locked">', unsafe_allow_html=True)
        st.error("🚨 YOUR EXAM HAS BEEN LOCKED DUE TO SECURITY VIOLATIONS")
        st.write("Reason: Tab switching detected during exam")
        st.write("Your exam has been automatically submitted with penalties applied")
        
        if st.button("View Results Now"):
            st.session_state.exam_completed = True
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # View results after completion
    if st.session_state.exam_completed:
        # Disable security scripts
        components.html("<script>if(window.disableExamMonitoring){window.disableExamMonitoring();}</script>", height=0)
        
        display_results()
        
        if st.session_state.auto_submitted:
            st.error("Your exam was automatically submitted due to security violations")
        return
    
    # Registration form
    if not st.session_state.exam_started:
        with st.container():
            st.subheader("🧾 Student Registration")
            col1, col2 = st.columns(2)
            with col1:
                student_name = st.text_input("Full Name *", placeholder="Enter your full name")
            with col2:
                student_id = st.text_input("Student ID", placeholder="Enter student ID")
            
            # Important security warning
            st.markdown('<div class="security-warning">', unsafe_allow_html=True)
            st.subheader("⚠️ IMPORTANT SECURITY NOTICE")
            st.write("1. Tab switching will result in immediate automatic submission")
            st.write("2. Exam cannot be re-attempted")
            st.write("3. Right-click and developer tools are disabled")
            st.write("4. Navigation buttons are disabled")
            st.write("5. Screenshots and screen recording are prohibited")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Start Secure Exam", type="primary", use_container_width=True):
                if not student_name:
                    st.error("Please enter your full name to start the exam")
                else:
                    st.session_state.student_name = student_name
                    st.session_state.student_id = student_id
                    st.session_state.exam_started = True
                    st.session_state.start_time = datetime.now()
                    st.rerun()
        return
    
    # Active exam interface
    components.html(secure_exam_js, height=0)
    
    with st.container():
        # Visual progress bar
        progress = (st.session_state.current_question + 1) / len(QUIZ_QUESTIONS)
        st.subheader(f"Progress: Question {st.session_state.current_question + 1} of {len(QUIZ_QUESTIONS)}")
        st.progress(progress)
        
        # Current question
        q_index = st.session_state.current_question
        question = QUIZ_QUESTIONS[q_index]
        
        st.markdown('<div class="question-header">', unsafe_allow_html=True)
        st.subheader(f"Question {q_index + 1}")
        st.write(f"**{question['question']}**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Answer selection
        current_answer = st.session_state.user_answers.get(q_index, -1)
        with st.container():
            selected_option = st.radio(
                "Select your answer:",
                options=list(range(len(question['options']))),
                format_func=lambda i: f"{chr(65 + i)}. {question['options'][i]}",
                index=current_answer if current_answer >= 0 else None,
                key=f"q{q_index}",
                horizontal=True
            )
        
        # Save answer
        if selected_option is not None:
            st.session_state.user_answers[q_index] = selected_option
        
        # Navigation
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.session_state.current_question > 0:
                if st.button("⬅️ Previous Question"):
                    st.session_state.current_question -= 1
                    st.rerun()
            else:
                st.write("")  # Spacer
                
        with col2:
            if st.session_state.current_question < len(QUIZ_QUESTIONS) - 1:
                if st.button(f"Next Question ➡️ (Q{q_index+2})", type="primary"):
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.button("✅ Submit Final Answers", type="primary", use_container_width=True):
                    submit_exam()
                    st.rerun()
        
        # Warning about previous questions
        st.markdown("---")
        st.warning("⚠️ SECURITY NOTICE: You cannot return to previous questions after submission. Ensure your answer is final before moving ahead.")

if __name__ == "__main__":
    main()
