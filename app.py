import os
import streamlit as st
import google.generativeai as genai
import json  

API_KEY = "AIzaSyAMPjH7RwRrOOCZQBO9JjJd9zt_cpSs8tM"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.0-flash')

st.sidebar.title("Quiz Settings")
difficulty = st.sidebar.radio('Select difficulty:', ['Easy', 'Medium', 'Hard'])

def get_questions(difficulty):
    prompt = f"""
    Generate 5 **completely different** Python multiple-choice questions **each time** in JSON format.
    
    ⚠️ **DO NOT REPEAT** previous questions.
    ⚠️ **DO NOT INCLUDE** explanations or markdown.
    
    **Strict JSON Format:**
    {{
        "questions": [
            {{
                "question": "What is the correct way to open a file in Python for reading?",
                "options": ["open('file.txt', 'w')", "open('file.txt', 'r')", "open('file.txt', 'a')", "open('file.txt', 'x')"],
                "answer": "open('file.txt', 'r')"
            }},
            {{
                "question": "Which data type is immutable in Python?",
                "options": ["List", "Set", "Dictionary", "Tuple"],
                "answer": "Tuple"
            }},
            ...
        ]
    }}

    📌 **Rules for Generation**:
    - **Generate random questions each time.**
    - **Ensure JSON format without any extra text.**
    - **Only Python-related questions.**
    
    Topic: General Python  
    Difficulty: {difficulty}
    """

    try:
        response = model.generate_content(prompt)

        print("Raw AI Response:", response.text)

        json_start = response.text.find("{")
        json_end = response.text.rfind("}") + 1

        if json_start == -1 or json_end == 0:
            raise ValueError("No valid JSON found in AI response")
        clean_json = response.text[json_start:json_end]

        question_data = json.loads(clean_json)
        return question_data["questions"] 
    
    except json.JSONDecodeError:
        st.error("❌ Failed to parse the AI response as JSON.")
        return None
    except Exception as e:
        st.error(f"Error fetching questions: {e}")
        return None
    

if "quiz_data" not in st.session_state or st.sidebar.button("Generate New Quiz"):
    st.session_state.quiz_data = get_questions(difficulty)
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.selected_answers = [None] * 5

if st.session_state.quiz_data:
    total_questions = len(st.session_state.quiz_data)
    current_q_index = st.session_state.current_question
    
    if current_q_index < total_questions:
        question_data = st.session_state.quiz_data[current_q_index]
        st.write(f"**Q{current_q_index + 1}: {question_data['question']}**")

        selected_answer = st.radio(
            "Choose your answer:",
            question_data['options'],
            key=f"q{current_q_index}"
        )

        st.session_state.selected_answers[current_q_index] = selected_answer

        # Next Question Button
        if st.button("Next Question"):
            if selected_answer == question_data["answer"]:
                st.session_state.score += 1 
            st.session_state.current_question += 1
            st.rerun()
    else:
        st.subheader("Quiz Completed! 🎉")
        st.write(f"Your Final Score: **{st.session_state.score} / {total_questions}**")

        if st.button("Restart Quiz"):
            st.session_state.quiz_data = get_questions(difficulty)
            st.session_state.current_question = 0
            st.session_state.score = 0 
            st.session_state.selected_answers = [None] * 5
            st.rerun()
