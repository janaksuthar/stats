import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from datetime import datetime
import os
from typing import Dict, List, Any

# Configure page
st.set_page_config(
    page_title="MCQ Quiz Assessment v6",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        border: 1px solid #e1e8ed;
    }
    
    .question-header {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 2px solid #ffc107;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        color: #856404;
        box-shadow: 0 4px 16px rgba(255, 193, 7, 0.2);
    }
    
    .results-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
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
    
    .version-tag {
        position: absolute;
        top: 10px;
        right: 10px;
        background: #667eea;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced JavaScript for tab switching detection
tab_monitor_js = """
<script>
let tabSwitchCount = 0;
let isQuizActive = true;
let warningShown = false;

// Function to handle visibility change
function handleVisibilityChange() {
    if (document.hidden && isQuizActive && !warningShown) {
        tabSwitchCount++;
        warningShown = true;
        
        console.log('Tab switch detected! Count:', tabSwitchCount);
        
        // Show warning with countdown
        showWarningDialog();
        
        // Trigger auto-submission after delay
        setTimeout(() => {
            submitQuiz();
        }, 3000);
    }
}

// Enhanced warning dialog
function showWarningDialog() {
    // Create warning overlay
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        z-index: 10000;
        display: flex;
        align-items: center;
        justify-content: center;
    `;
    
    const modal = document.createElement('div');
    modal.style.cssText = `
        background: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        max-width: 400px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    `;
    
    modal.innerHTML = `
        <h2 style="color: #dc3545; margin-bottom: 1rem;">⚠️ Tab Switch Detected!</h2>
        <p style="margin-bottom: 1rem;">You switched away from the quiz window.</p>
        <p style="margin-bottom: 1rem; font-weight: bold;">Quiz will be auto-submitted in <span id="countdown">3</span> seconds...</p>
        <div style="background: #f8d7da; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <strong>Tab switches detected: ${tabSwitchCount}</strong>
        </div>
    `;
    
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
    
    // Countdown timer
    let countdown = 3;
    const countdownElement = document.getElementById('countdown');
    const countdownInterval = setInterval(() => {
        countdown--;
        if (countdownElement) {
            countdownElement.textContent = countdown;
        }
        if (countdown <= 0) {
            clearInterval(countdownInterval);
        }
    }, 1000);
}

// Submit quiz function
function submitQuiz() {
    const url = new URL(window.location);
    url.searchParams.set('auto_submit', 'true');
    url.searchParams.set('tab_switches', tabSwitchCount.toString());
    url.searchParams.set('timestamp', Date.now().toString());
    
    // Force page reload to trigger submission
    window.location.href = url.toString();
}

// Add event listeners
document.addEventListener('visibilitychange', handleVisibilityChange);

// Enhanced window blur detection
window.addEventListener('blur', function() {
    if (isQuizActive && !document.hidden) {
        setTimeout(() => {
            if (document.hidden) {
                handleVisibilityChange();
            }
        }, 100);
    }
});

// Prevent right-click context menu
document.addEventListener('contextmenu', function(e) {
    if (isQuizActive) {
        e.preventDefault();
        return false;
    }
});

// Prevent common cheating key combinations
document.addEventListener('keydown', function(e) {
    if (isQuizActive) {
        // Prevent F12, Ctrl+Shift+I, Ctrl+U, Ctrl+S
        if (e.keyCode === 123 || 
            (e.ctrlKey && e.shiftKey && e.keyCode === 73) ||
            (e.ctrlKey && e.keyCode === 85) ||
            (e.ctrlKey && e.keyCode === 83)) {
            e.preventDefault();
            return false;
        }
    }
});

// Function to disable monitoring when quiz is completed
function disableTabMonitoring() {
    isQuizActive = false;
    console.log('Quiz tab monitoring disabled');
}

// Make functions globally available
window.disableTabMonitoring = disableTabMonitoring;
window.tabSwitchCount = tabSwitchCount;

// Initialize monitoring
if (isQuizActive) {
    console.log('MCQ Quiz v6 - Tab monitoring active');
}
</script>
"""

# Enhanced quiz questions with better content
QUIZ_QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct": 2,
        "explanation": "Paris is the capital and most populous city of France, located on the Seine River in northern France."
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct": 1,
        "explanation": "Mars is called the Red Planet due to its reddish appearance caused by iron oxide (rust) on its surface."
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["African Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
        "correct": 1,
        "explanation": "The Blue Whale is the largest animal ever known to have lived on Earth, reaching lengths of up to 100 feet."
    },
    {
        "question": "Who painted the famous artwork 'The Starry Night'?",
        "options": ["Pablo Picasso", "Vincent van Gogh", "Leonardo da Vinci", "Claude Monet"],
        "correct": 1,
        "explanation": "The Starry Night was painted by Vincent van Gogh in 1889 while he was a patient at the Saint-Paul-de-Mausole asylum."
    },
    {
        "question": "What is the chemical symbol for gold?",
        "options": ["Go", "Gd", "Au", "Ag"],
        "correct": 2,
        "explanation": "Au is the chemical symbol for gold, derived from the Latin word 'aurum' meaning 'shining dawn'."
    },
    {
        "question": "Which programming language is known as the 'language of the web'?",
        "options": ["Python", "JavaScript", "Java", "C++"],
        "correct": 1,
        "explanation": "JavaScript is widely known as the 'language of the web' because it runs in web browsers and enables interactive web pages."
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
        "correct": 3,
        "explanation": "The Pacific Ocean is the largest ocean on Earth, covering about 46% of the water surface and 32% of the total surface area."
    },
    {
        "question": "Who developed the theory of relativity?",
        "options": ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Stephen Hawking"],
        "correct": 1,
        "explanation": "Albert Einstein developed both the special and general theories of relativity, revolutionizing our understanding of space and time."
    }
]

def initialize_session_state():
    """Initialize session state variables"""
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'student_name' not in st.session_state:
        st.session_state.student_name = ""
    if 'student_id' not in st.session_state:
        st.session_state.student_id = ""
    if 'tab_switches' not in st.session_state:
        st.session_state.tab_switches = 0
    if 'auto_submitted' not in st.session_state:
        st.session_state.auto_submitted = False
    if 'quiz_version' not in st.session_state:
        st.session_state.quiz_version = "v6"

def check_auto_submit():
    """Check if quiz should be auto-submitted due to tab switching"""
    try:
        query_params = st.query_params
        if query_params.get('auto_submit') == 'true':
            if not st.session_state.quiz_completed:
                st.session_state.auto_submitted = True
                st.session_state.tab_switches = int(query_params.get('tab_switches', '0'))
                submit_quiz()
                # Clear the URL parameters
                st.query_params.clear()
    except Exception as e:
        pass

def submit_quiz():
    """Submit the quiz and calculate results"""
    if st.session_state.quiz_completed:
        return
    
    st.session_state.quiz_completed = True
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
    
    # Save results to CSV
    save_results_to_csv()

def save_results_to_csv():
    """Save quiz results to CSV file"""
    try:
        # Prepare data for CSV
        duration = (st.session_state.end_time - st.session_state.start_time).total_seconds() / 60
        
        result_data = {
            'Quiz Version': st.session_state.quiz_version,
            'Student Name': st.session_state.student_name,
            'Student ID': st.session_state.student_id,
            'Start Time': st.session_state.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'End Time': st.session_state.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'Duration (minutes)': round(duration, 2),
            'Score': st.session_state.score,
            'Total Questions': st.session_state.total_questions,
            'Percentage': round(st.session_state.percentage, 2),
            'Grade': get_grade(st.session_state.percentage),
            'Tab Switches': st.session_state.tab_switches,
            'Auto Submitted': st.session_state.auto_submitted,
            'Submission Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add individual question responses
        for i, question in enumerate(QUIZ_QUESTIONS):
            user_answer = st.session_state.user_answers.get(i, -1)
            correct_answer = question['correct']
            result_data[f'Q{i+1}_User_Answer'] = user_answer
            result_data[f'Q{i+1}_Correct_Answer'] = correct_answer
            result_data[f'Q{i+1}_Correct'] = user_answer == correct_answer
        
        # Create DataFrame
        df = pd.DataFrame([result_data])
        
        # Save to CSV
        csv_filename = 'mcq_quiz_results.csv'
        if os.path.exists(csv_filename):
            df.to_csv(csv_filename, mode='a', header=False, index=False)
        else:
            df.to_csv(csv_filename, index=False)
        
        st.session_state.csv_saved = True
        
    except Exception as e:
        st.error(f"Error saving results to CSV: {str(e)}")
        st.session_state.csv_saved = False

def get_grade(percentage):
    """Convert percentage to letter grade"""
    if percentage >= 90:
        return "A+"
    elif percentage >= 85:
        return "A"
    elif percentage >= 80:
        return "B+"
    elif percentage >= 75:
        return "B"
    elif percentage >= 70:
        return "C+"
    elif percentage >= 65:
        return "C"
    elif percentage >= 60:
        return "D"
    else:
        return "F"

def display_results():
    """Display quiz results with enhanced formatting"""
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    
    # Score display with enhanced styling
    score_class = "score-excellent" if st.session_state.percentage >= 80 else "score-good" if st.session_state.percentage >= 60 else "score-needs-improvement"
    grade = get_grade(st.session_state.percentage)
    
    st.markdown(f'''
    <div class="score-display {score_class}">
        🎯 Final Score: {st.session_state.score}/{st.session_state.total_questions}<br>
        📊 Percentage: {st.session_state.percentage:.1f}%<br>
        🎓 Grade: {grade}
    </div>
    ''', unsafe_allow_html=True)
    
    # Quiz summary with enhanced metrics
    duration = (st.session_state.end_time - st.session_state.start_time).total_seconds() / 60
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.metric("⏱️ Time Taken", f"{duration:.1f} min")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.metric("👀 Tab Switches", st.session_state.tab_switches)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.metric("🤖 Auto Submit", "Yes" if st.session_state.auto_submitted else "No")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.metric("✅ Accuracy", f"{st.session_state.percentage:.0f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed results
    st.subheader("📋 Detailed Question Analysis")
    
    for i, question in enumerate(QUIZ_QUESTIONS):
        user_answer = st.session_state.user_answers.get(i, -1)
        correct_answer = question['correct']
        is_correct = user_answer == correct_answer
        
        with st.expander(f"Question {i+1}: {question['question']}", expanded=False):
            st.write(f"**Your Answer:** {question['options'][user_answer] if user_answer != -1 else 'Not answered'}")
            st.write(f"**Correct Answer:** {question['options'][correct_answer]}")
            
            if is_correct:
                st.markdown('<div class="correct-answer">✅ Correct! Well done!</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="incorrect-answer">❌ Incorrect</div>', unsafe_allow_html=True)
            
            st.info(f"💡 **Explanation:** {question['explanation']}")
    
    # Performance summary
    st.subheader("📈 Performance Summary")
    
    correct_count = st.session_state.score
    incorrect_count = st.session_state.total_questions - correct_count
    
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"✅ Correct Answers: {correct_count}")
    with col2:
        st.error(f"❌ Incorrect Answers: {incorrect_count}")
    
    # CSV save status
    if hasattr(st.session_state, 'csv_saved'):
        if st.session_state.csv_saved:
            st.success("📄 Results saved to mcq_quiz_results.csv")
        else:
            st.warning("⚠️ Could not save results to CSV file")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application function"""
    initialize_session_state()
    check_auto_submit()
    
    # Header with version tag
    st.markdown('''
    <div class="main-header">
        <div class="version-tag">v6</div>
        <h1>📝 MCQ Quiz Assessment</h1>
        <p>Advanced quiz system with tab monitoring and integrity tracking</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Show results if quiz is completed
    if st.session_state.quiz_completed:
        # Disable tab monitoring when quiz is completed
        components.html("""
        <script>
        if (window.disableTabMonitoring) {
            window.disableTabMonitoring();
        }
        </script>
        """, height=0)
        
        if st.session_state.auto_submitted:
            st.error("🚨 Quiz was automatically submitted due to tab switching!")
        else:
            st.success("🎉 Quiz completed successfully!")
        
        display_results()
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Start New Quiz", type="primary"):
                # Reset session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button("📊 View Results Summary", type="secondary"):
                if os.path.exists('mcq_quiz_results.csv'):
                    df = pd.read_csv('mcq_quiz_results.csv')
                    st.dataframe(df.tail(10))
                else:
                    st.warning("No results file found.")
        
        return
    
    # Student information input (if not started)
    if not st.session_state.quiz_started:
        st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
        st.subheader("👤 Student Information")
        
        col1, col2 = st.columns(2)
        with col1:
            student_name = st.text_input("📝 Full Name *", value=st.session_state.student_name, placeholder="Enter your full name")
        with col2:
            student_id = st.text_input("🆔 Student ID", value=st.session_state.student_id, placeholder="Enter your student ID (optional)")
        
        if student_name:
            st.session_state.student_name = student_name
            st.session_state.student_id = student_id
            
            # Quiz instructions
            st.markdown('''
            <div class="warning-box">
                <h4>⚠️ Important Quiz Instructions:</h4>
                <ul>
                    <li><strong>🚫 Do not switch tabs</strong> or minimize the browser window during the quiz</li>
                    <li><strong>⚡ Auto-submission:</strong> The quiz will automatically submit if you leave this page</li>
                    <li><strong>⏰ Time limit:</strong> No time limit, but work efficiently</li>
                    <li><strong>🔍 Read carefully:</strong> Each question before selecting your answer</li>
                    <li><strong>🔄 Navigation:</strong> Use Previous/Next buttons to move between questions</li>
                    <li><strong>💾 Auto-save:</strong> Your answers are automatically saved</li>
                    <li><strong>🛡️ Security:</strong> Right-click and developer tools are disabled</li>
                </ul>
            </div>
            ''', unsafe_allow_html=True)
            
            # Quiz preview
            st.info(f"📚 This quiz contains {len(QUIZ_QUESTIONS)} multiple-choice questions covering various topics.")
            
            if st.button("🚀 Start Quiz", type="primary", use_container_width=True):
                st.session_state.quiz_started = True
                st.session_state.start_time = datetime.now()
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Inject JavaScript for tab monitoring
    components.html(tab_monitor_js, height=0)
    
    # Quiz interface
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    
    # Progress bar with enhanced styling
    progress = (st.session_state.current_question + 1) / len(QUIZ_QUESTIONS)
    st.progress(progress)
    
    # Quiz header info
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"**👤 Student:** {st.session_state.student_name}")
        if st.session_state.student_id:
            st.write(f"**🆔 ID:** {st.session_state.student_id}")
    with col2:
        st.write(f"**📍 Question:** {st.session_state.current_question + 1}/{len(QUIZ_QUESTIONS)}")
    with col3:
        answered = len(st.session_state.user_answers)
        st.write(f"**✅ Answered:** {answered}/{len(QUIZ_QUESTIONS)}")
    
    # Current question display
    current_q = QUIZ_QUESTIONS[st.session_state.current_question]
    
    st.markdown(f'''
    <div class="question-header">
        <h3>Question {st.session_state.current_question + 1}</h3>
        <p style="font-size: 1.1em; margin-top: 1rem;">{current_q["question"]}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Answer options with enhanced styling
    current_answer = st.session_state.user_answers.get(st.session_state.current_question, None)
    
    selected_option = st.radio(
        "Select your answer:",
        options=list(range(len(current_q["options"]))),
        format_func=lambda x: f"{chr(65 + x)}. {current_q['options'][x]}",
        index=current_answer,
        key=f"q_{st.session_state.current_question}"
    )
    
    # Save answer
    if selected_option is not None:
        st.session_state.user_answers[st.session_state.current_question] = selected_option
    
    # Navigation buttons with enhanced styling
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_question > 0:
            if st.button("⬅️ Previous", type="secondary", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col2:
        # Progress indicator
        st.write(f"**Progress:** {answered}/{len(QUIZ_QUESTIONS)} questions answered")
        progress_percentage = (answered / len(QUIZ_QUESTIONS)) * 100
        st.progress(progress_percentage / 100)
    
    with col3:
        if st.session_state.current_question < len(QUIZ_QUESTIONS) - 1:
            if st.button("Next ➡️", type="secondary", use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("✅ Submit Quiz", type="primary", use_container_width=True):
                submit_quiz()
                st.rerun()
    
    # Quick navigation (question overview)
    st.markdown("---")
    st.write("**🎯 Quick Navigation:**")
    
    # Create question navigation buttons
    nav_cols = st.columns(min(8, len(QUIZ_QUESTIONS)))
    for i in range(len(QUIZ_QUESTIONS)):
        col_idx = i % len(nav_cols)
        with nav_cols[col_idx]:
            status = "✅" if i in st.session_state.user_answers else "⭕"
            button_type = "primary" if i == st.session_state.current_question else "secondary"
            if st.button(f"{status} {i+1}", type=button_type, key=f"nav_{i}"):
                st.session_state.current_question = i
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
