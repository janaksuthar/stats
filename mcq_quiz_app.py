<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MCQ Quiz Assessment</title>
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
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>MCQ Quiz Assessment</h1>
            <p>Test your knowledge with this interactive quiz</p>
        </div>
        
        <div id="student-info" class="quiz-container">
            <h2>Student Information</h2>
            <div class="form-group">
                <label for="name">Full Name *</label>
                <input type="text" id="name" class="form-control" placeholder="Enter your full name" required>
            </div>
            
            <div class="warning-box">
                <h3>⚠️ Important Quiz Instructions:</h3>
                <ul>
                    <li><strong>Don't switch tabs/windows</strong> - Quiz will be auto-submitted if you do</li>
                    <li>Read each question carefully before answering</li>
                    <li>Your answers are saved automatically</li>
                    <li>No going back to previous questions</li>
                </ul>
            </div>
            
            <button id="start-quiz" class="start-btn">Start Quiz</button>
        </div>
        
        <div id="quiz-content" class="hidden">
            <div id="quiz-question" class="quiz-container">
                <div class="question" id="question-text"></div>
                <div class="options" id="options-container"></div>
                
                <div class="navigation">
                    <button id="next-btn" class="next">Next Question</button>
                    <button id="submit-btn" class="submit hidden">Submit Quiz</button>
                </div>
            </div>
            
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress" id="progress-bar"></div>
                </div>
                <div class="progress-text" id="progress-text"></div>
            </div>
        </div>
        
        <div id="quiz-results" class="hidden">
            <div class="quiz-container">
                <h2>Quiz Results</h2>
                
                <div id="score-display" class="score-display score-excellent">
                    <h3 id="score-text"></h3>
                    <p id="grade-text"></p>
                </div>
                
                <div id="results-container"></div>
            </div>
        </div>
    </div>
    
    <script>
        // Quiz questions
        const quizQuestions = [
            {
                question: "What is the capital of France?",
                options: ["London", "Berlin", "Paris", "Madrid"],
                correct: 2,
                explanation: "Paris is the capital and most populous city of France."
            },
            {
                question: "Which planet is known as the Red Planet?",
                options: ["Venus", "Mars", "Jupiter", "Saturn"],
                correct: 1,
                explanation: "Mars appears red due to iron oxide (rust) on its surface."
            },
            {
                question: "What is the largest mammal in the world?",
                options: ["African Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
                correct: 1,
                explanation: "The Blue Whale is the largest animal ever known to have lived on Earth."
            },
            {
                question: "Who painted the famous artwork 'The Starry Night'?",
                options: ["Pablo Picasso", "Vincent van Gogh", "Leonardo da Vinci", "Claude Monet"],
                correct: 1,
                explanation: "Vincent van Gogh painted The Starry Night in 1889."
            },
            {
                question: "What is the chemical symbol for gold?",
                options: ["Go", "Gd", "Au", "Ag"],
                correct: 2,
                explanation: "Au is the chemical symbol for gold, from the Latin 'aurum'."
            }
        ];
        
        // Quiz state
        let currentQuestion = 0;
        let userAnswers = [];
        let tabSwitches = 0;
        let quizStarted = false;
        let quizCompleted = false;
        let studentName = "";
        
        // DOM elements
        const studentInfoSection = document.getElementById('student-info');
        const quizContentSection = document.getElementById('quiz-content');
        const quizResultsSection = document.getElementById('quiz-results');
        const questionText = document.getElementById('question-text');
        const optionsContainer = document.getElementById('options-container');
        const nextBtn = document.getElementById('next-btn');
        const submitBtn = document.getElementById('submit-btn');
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        const scoreDisplay = document.getElementById('score-display');
        const scoreText = document.getElementById('score-text');
        const gradeText = document.getElementById('grade-text');
        const resultsContainer = document.getElementById('results-container');
        const startBtn = document.getElementById('start-quiz');
        const nameInput = document.getElementById('name');
        
        // Tab switching detection
        function handleVisibilityChange() {
            if (document.hidden && quizStarted && !quizCompleted) {
                tabSwitches++;
                alert("Warning: You switched tabs! Quiz will be auto-submitted.");
                submitQuiz();
            }
        }
        
        document.addEventListener('visibilitychange', handleVisibilityChange);
        
        // Start quiz
        startBtn.addEventListener('click', () => {
            studentName = nameInput.value.trim();
            
            if (studentName === "") {
                alert("Please enter your name to start the quiz.");
                return;
            }
            
            quizStarted = true;
            studentInfoSection.classList.add('hidden');
            quizContentSection.classList.remove('hidden');
            loadQuestion();
            recordStartTime();
            
            // Disable right-click
            document.addEventListener('contextmenu', (e) => {
                e.preventDefault();
            });
        });
        
        // Load question
        function loadQuestion() {
            const question = quizQuestions[currentQuestion];
            questionText.textContent = `Question ${currentQuestion + 1}: ${question.question}`;
            
            optionsContainer.innerHTML = "";
            
            question.options.forEach((option, index) => {
                const optionElement = document.createElement('div');
                optionElement.classList.add('option');
                
                if (userAnswers[currentQuestion] === index) {
                    optionElement.classList.add('selected');
                }
                
                optionElement.textContent = `${String.fromCharCode(65 + index)}. ${option}`;
                
                optionElement.addEventListener('click', () => {
                    // Remove selected class from all options
                    document.querySelectorAll('.option').forEach(opt => {
                        opt.classList.remove('selected');
                    });
                    
                    // Add selected class to clicked option
                    optionElement.classList.add('selected');
                    
                    // Save answer
                    userAnswers[currentQuestion] = index;
                });
                
                optionsContainer.appendChild(optionElement);
            });
            
            // Update progress
            const progress = ((currentQuestion) / quizQuestions.length) * 100;
            progressBar.style.width = `${progress}%`;
            progressText.textContent = `Completed: ${currentQuestion} of ${quizQuestions.length} questions`;
            
            // Show/hide submit button
            if (currentQuestion === quizQuestions.length - 1) {
                nextBtn.classList.add('hidden');
                submitBtn.classList.remove('hidden');
            } else {
                nextBtn.classList.remove('hidden');
                submitBtn.classList.add('hidden');
            }
        }
        
        // Next question
        nextBtn.addEventListener('click', () => {
            if (userAnswers[currentQuestion] === undefined) {
                alert("Please select an answer before proceeding.");
                return;
            }
            
            currentQuestion++;
            loadQuestion();
        });
        
        // Submit quiz
        submitBtn.addEventListener('click', () => {
            submitQuiz();
        });
        
        function submitQuiz() {
            quizCompleted = true;
            
            // Calculate score
            let correctAnswers = 0;
            let totalQuestions = quizQuestions.length;
            
            for (let i = 0; i < totalQuestions; i++) {
                if (userAnswers[i] === quizQuestions[i].correct) {
                    correctAnswers++;
                }
            }
            
            const percentage = (correctAnswers / totalQuestions) * 100;
            let grade = getGrade(percentage);
            
            // Display results
            scoreText.textContent = `Score: ${correctAnswers}/${totalQuestions} (${percentage.toFixed(1)}%)`;
            gradeText.textContent = `Grade: ${grade}`;
            
            if (percentage >= 80) {
                scoreDisplay.classList.add('score-excellent');
                scoreDisplay.classList.remove('score-good');
                scoreDisplay.classList.remove('score-needs-improvement');
            } else if (percentage >= 60) {
                scoreDisplay.classList.remove('score-excellent');
                scoreDisplay.classList.add('score-good');
                scoreDisplay.classList.remove('score-needs-improvement');
            } else {
                scoreDisplay.classList.remove('score-excellent');
                scoreDisplay.classList.remove('score-good');
                scoreDisplay.classList.add('score-needs-improvement');
            }
            
            // Render detailed results
            resultsContainer.innerHTML = "";
            
            quizQuestions.forEach((question, index) => {
                const resultItem = document.createElement('div');
                resultItem.classList.add('result-item');
                
                if (userAnswers[index] === question.correct) {
                    resultItem.classList.add('correct');
                } else {
                    resultItem.classList.add('incorrect');
                }
                
                const userAnswer = userAnswers[index] !== undefined ? 
                    `${String.fromCharCode(65 + userAnswers[index])}. ${question.options[userAnswers[index]]}` : 
                    "Not answered";
                
                const correctAnswer = `${String.fromCharCode(65 + question.correct)}. ${question.options[question.correct]}`;
                
                resultItem.innerHTML = `
                    <p><strong>Question ${index + 1}:</strong> ${question.question}</p>
                    <p><strong>Your answer:</strong> ${userAnswer}</p>
                    <p><strong>Correct answer:</strong> ${correctAnswer}</p>
                    <p><em>${question.explanation}</em></p>
                `;
                
                resultsContainer.appendChild(resultItem);
            });
            
            quizContentSection.classList.add('hidden');
            quizResultsSection.classList.remove('hidden');
            
            // Record completion time
            recordCompletionTime();
        }
        
        function getGrade(percentage) {
            if (percentage >= 90) return "A+";
            if (percentage >= 85) return "A";
            if (percentage >= 80) return "B+";
            if (percentage >= 75) return "B";
            if (percentage >= 70) return "C+";
            if (percentage >= 65) return "C";
            if (percentage >= 60) return "D";
            return "F";
        }
        
        function recordStartTime() {
            localStorage.setItem('quizStartTime', new Date().toISOString());
        }
        
        function recordCompletionTime() {
            localStorage.setItem('quizCompletionTime', new Date().toISOString());
            localStorage.setItem('tabSwitches', tabSwitches);
        }
        
        // Prevent cheating shortcuts
        document.addEventListener('keydown', (e) => {
            if (quizStarted && !quizCompleted) {
                // Disable F12
                if (e.keyCode === 123) {
                    e.preventDefault();
                }
                
                // Disable Ctrl+Shift+I and Ctrl+Shift+J
                if (e.ctrlKey && e.shiftKey && (e.keyCode === 73 || e.keyCode === 74)) {
                    e.preventDefault();
                }
                
                // Disable Ctrl+U
                if (e.ctrlKey && e.keyCode === 85) {
                    e.preventDefault();
                }
            }
        });
    </script>
</body>
</html>
