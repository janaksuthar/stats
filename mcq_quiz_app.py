# Custom CSS for professional styling
st.markdown("""
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f5f7fa;
        margin: 0;
        padding: 0;
        color: #333;
    }
    
    .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .header {
        text-align: center;
        margin-bottom: 30px;
        padding: 20px;
        background-color: #667eea;
        color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .quiz-container {
        background-color: white;
        border-radius: 10px;
        padding: 25px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    .question {
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 15px;
    }
    
    .options {
        margin: 20px 0;
    }
    
    .option {
        display: block;
        margin: 10px 0;
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .option:hover {
        background-color: #e9ecef;
    }
    
    .option.selected {
        background-color: #d4edda;
    }
    
    .navigation {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
    }
    
    button {
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.2s;
    }
    
    button.next {
        background-color: #667eea;
        color: white;
    }
    
    button.next:hover {
        background-color: #5a67d8;
    }
    
    button.submit {
        background-color: #38a169;
        color: white;
    }
    
    button.submit:hover {
        background-color: #2f855a;
    }
    
    .progress-container {
        margin-top: 30px;
    }
    
    .progress-bar {
        height: 10px;
        background-color: #e2e8f0;
        border-radius: 5px;
        margin-bottom: 10px;
        overflow: hidden;
    }
    
    .progress {
        height: 100%;
        background-color: #667eea;
        transition: width 0.3s;
    }
    
    .progress-text {
        text-align: center;
        font-size: 0.9em;
        color: #718096;
    }
    
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 5px;
    }
    
    .quiz-started {
        text-align: center;
        padding: 20px;
    }
    
    .start-btn {
        background-color: #667eea;
        color: white;
        padding: 12px 25px;
        font-size: 1.1em;
        margin-top: 20px;
    }
    
    .score-display {
        text-align: center;
        padding: 30px;
        border-radius: 10px;
        margin: 20px 0;
    }
    
    .score-excellent {
        background-color: #d4edda;
        color: #155724;
    }
    
    .result-item {
        margin-bottom: 15px;
        padding: 15px;
        border-radius: 5px;
        background-color: #f8f9fa;
    }
    
    .correct {
        background-color: #d4edda;
    }
    
    .incorrect {
        background-color: #f8d7da;
    }
    
    .hidden {
        display: none;
    }
</style>
""", unsafe_allow_html=True)
