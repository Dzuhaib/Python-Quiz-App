import streamlit as st

quiz_data = [
    {"question": "What is the correct syntax to define a function in Python?",
     "options": ["def function_name():", "function function_name():", "define function_name():", "fn function_name():"],
     "correct_answer": "def function_name():"},

    {"question": "Which of the following is used to create a loop in Python?",
     "options": ["for", "while", "Both for and while", "loop"],
     "correct_answer": "Both for and while"},

    {"question": "What is the output of print(2 ** 3) in Python?",
     "options": ["6", "8", "9", "16"],
     "correct_answer": "8"},

    {"question": "Which keyword is used to handle exceptions in Python?",
     "options": ["try", "catch", "handle", "except"],
     "correct_answer": "try"},

    {"question": "Which of the following data types is **immutable** in Python?",
     "options": ["List", "Dictionary", "Tuple", "Set"],
     "correct_answer": "Tuple"}
]

# Initialize session state at the beginning
if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(quiz_data)
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = 0  # Fix: Initialize `current_question`

# Function to handle quiz logic
def run_quiz():
    st.sidebar.title("📌 Python Quiz Navigation")
    st.sidebar.markdown("Navigate through the quiz and check your score!")

    # Progress Bar
    progress = (st.session_state.current_question + 1) / len(quiz_data)
    st.sidebar.progress(progress)

    if st.session_state.submitted:
        st.sidebar.subheader("📊 Your Results")
        st.sidebar.write(f"Your score: **{st.session_state.score} / {len(quiz_data)}** 🎯")

    st.title("🐍Python Quiz")

    # Display question
    q_index = st.session_state.current_question
    question = quiz_data[q_index]
    st.subheader(f"Question {q_index + 1}: {question['question']}")

    # Display radio buttons for options
    selected_answer = st.radio(
        "Select an answer",
        question["options"],
        index=question["options"].index(st.session_state.answers[q_index]) if st.session_state.answers[q_index] else None,
        key=f"q{q_index}"
    )

    # Store the selected answer
    st.session_state.answers[q_index] = selected_answer

    # Navigation Buttons
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.session_state.current_question > 0:
            if st.button("⬅️ Previous Question"):
                st.session_state.current_question -= 1
                st.rerun()  # Fix: rerun the app properly

    with col2:
        if st.session_state.current_question < len(quiz_data) - 1:
            if st.button("➡️ Next Question"):
                st.session_state.current_question += 1
                st.rerun()  # Fix: rerun the app properly

    # Submit Quiz
    if st.session_state.current_question == len(quiz_data) - 1 and st.button("✅ Submit Answers"):
        st.session_state.submitted = True
        st.session_state.score = sum(
            1 for i, q in enumerate(quiz_data) if st.session_state.answers[i] == q["correct_answer"]
        )
        st.rerun()  # Fix: rerun after submitting

    # Display results after submission
    if st.session_state.submitted:
        st.write("---")
        st.subheader("📊 Your Results")
        st.write(f"Your score: **{st.session_state.score} / {len(quiz_data)}** 🎯")

        # Provide feedback on each question
        for i, q in enumerate(quiz_data):
            st.write(f"**Q{i + 1}: {q['question']}**")
            st.write(f"Your answer: `{st.session_state.answers[i]}`")
            st.write(f"Correct answer: `{q['correct_answer']}`")
            if st.session_state.answers[i] == q["correct_answer"]:
                st.success("✅ Correct!")
            else:
                st.error("❌ Incorrect.")

        # Reset Quiz Button
        if st.button("🔄 Reset Quiz"):
            st.session_state.answers = [None] * len(quiz_data)
            st.session_state.score = 0
            st.session_state.submitted = False
            st.session_state.current_question = 0
            st.rerun()  # Fix: rerun after resetting


if __name__ == "__main__":
    run_quiz()
