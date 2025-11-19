import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import pandas as pd

# 1. CONFIGURATION
# ----------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="Tutor Buddy", page_icon="🎓", layout="wide")

if not api_key:
    st.error("❌ API Key not found!")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# 2. DATA
# -------
SUBJECTS_LIST = [
    "Python Programming", "Data Structures & Algorithms", "DBMS", 
    "Operating Systems", "Computer Networks", "Web Development", 
    "Software Engineering", "C++ Programming", "Java", "AI Basics"
]

# 3. AGENT FUNCTIONS
# ------------------

def get_syllabus(subject):
    prompt = f"Create a 6-topic syllabus for {subject}. Return JSON list of strings."
    try:
        text = model.generate_content(prompt).text.strip().replace("```json", "").replace("```", "")
        return json.loads(text)
    except:
        return ["Basics", "Intermediate Concepts", "Advanced Topics", "Best Practices", "Case Studies", "Summary"]

def teach_topic(subject, topic, level):
    # Personality instructions
    if level == "Beginner":
        tone = "You are a friendly kindergarten teacher. Use simple analogies. No complex jargon."
    elif level == "Intermediate":
        tone = "You are a University Professor. Balance theory and code."
    else: 
        tone = "You are a Senior Staff Engineer at Google. Deep dive into optimization and edge cases."

    prompt = f"""
    Subject: {subject}
    Topic: {topic}
    Target Audience: {level}
    
    INSTRUCTIONS:
    {tone}
    Structure your response with Markdown headers.
    """
    return model.generate_content(prompt).text

def generate_quiz(subject, topic):
    prompt = f"""
    Create 3 multiple-choice questions for {subject}: {topic}.
    Return strictly valid JSON format:
    [
      {{"question": "Q1", "options": ["A. x", "B. y", "C. z", "D. w"], "correct": "A"}},
      ...
    ]
    """
    try:
        text = model.generate_content(prompt).text.strip().replace("```json", "").replace("```", "")
        return json.loads(text)
    except:
        return []

# 4. SESSION STATE
# ----------------
if 'step' not in st.session_state: st.session_state.step = 1
if 'selected_subject' not in st.session_state: st.session_state.selected_subject = None
if 'topic_list' not in st.session_state: st.session_state.topic_list = []
if 'generated_level' not in st.session_state: st.session_state.generated_level = None

# 5. UI
# -----
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=100)
    st.title("🎓 Tutor Profile")
    level = st.select_slider("Expertise Level", options=["Beginner", "Intermediate", "Expert"])
    
    st.divider()
    if st.button("🔄 Reset App"):
        st.session_state.clear()
        st.rerun()

st.title("🤖 AI Tutor Buddy")

# STEP 1: SUBJECT SELECTION
if st.session_state.step == 1:
    st.header("1️⃣ Select Subject")
    st.write("Pick a subject to generate your custom syllabus.")
    
    subj = st.selectbox("Choose your subject:", SUBJECTS_LIST)
    
    if st.button("Load Syllabus 🚀"):
        st.session_state.selected_subject = subj
        st.session_state.topic_list = get_syllabus(subj)
        st.session_state.step = 2
        st.rerun()

# STEP 2: TOPIC SELECTION
elif st.session_state.step == 2:
    st.header(f"2️⃣ Syllabus: {st.session_state.selected_subject}")
    
    df_t = pd.DataFrame(st.session_state.topic_list, columns=["Modules"])
    st.table(df_t)
    
    topic = st.radio("Select Module:", st.session_state.topic_list)
    
    if st.button("Start Class 🎓"):
        st.session_state.selected_topic = topic
        st.session_state.step = 3
        if 'lecture_content' in st.session_state: del st.session_state.lecture_content
        st.rerun()
    
    if st.button("⬅️ Back"):
        st.session_state.step = 1
        st.rerun()

# STEP 3: LEARNING
elif st.session_state.step == 3:
    st.header(f"📖 {st.session_state.selected_topic}")
    st.caption(f"Current Level: **{level}**")

    # Auto-refresh if slider changes
    if 'generated_level' in st.session_state and st.session_state.generated_level != level:
        if 'lecture_content' in st.session_state:
            del st.session_state.lecture_content
    
    if 'lecture_content' not in st.session_state:
        with st.spinner(f"Writing {level} level notes..."):
            st.session_state.lecture_content = teach_topic(
                st.session_state.selected_subject, 
                st.session_state.selected_topic, 
                level
            )
            st.session_state.generated_level = level
    
    st.markdown(st.session_state.lecture_content)
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Take Quiz 📝"):
            st.session_state.quiz_questions = generate_quiz(st.session_state.selected_subject, st.session_state.selected_topic)
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("⬅️ Topics"):
            st.session_state.step = 2
            st.rerun()

# STEP 4: QUIZ
elif st.session_state.step == 4:
    st.header("📝 Knowledge Check")
    
    if 'quiz_questions' not in st.session_state or not st.session_state.quiz_questions:
         st.error("Quiz generation failed. Try again.")
         if st.button("Back"):
             st.session_state.step = 3
             st.rerun()
    else:
        with st.form("quiz_form"):
            for i, q in enumerate(st.session_state.quiz_questions):
                st.subheader(f"Q{i+1}: {q['question']}")
                st.radio("Select:", q['options'], key=f"q{i}", index=None)
            
            if st.form_submit_button("Submit Answers"):
                score = 0
                for i, q in enumerate(st.session_state.quiz_questions):
                    user_ans = st.session_state.get(f"q{i}")
                    correct = q['correct']
                    if user_ans and (user_ans.startswith(correct + ".") or user_ans.startswith(correct + ")") or user_ans == correct):
                        score += 1
                
                if score == 3:
                    st.balloons() # <--- ADDED IT BACK HERE! 🎈
                    st.success(f"Perfect! 3/3 🎉")
                elif score > 0: 
                    st.info(f"Score: {score}/3")
                else: 
                    st.warning(f"Score: {score}/3")
        
        if st.button("⬅️ Back to Notes"):
            st.session_state.step = 3
            st.rerun()