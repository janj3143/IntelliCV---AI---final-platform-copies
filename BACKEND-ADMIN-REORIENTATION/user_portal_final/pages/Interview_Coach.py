"""
Interview Coach - IntelliCV AI-Powered Interview Preparation System
==================================================================

This page consolidates interview preparation functionality from:
- frontend/interview_prep.py
- frontend/interview_simulator.py  
- frontend/interview_agent.py
- modules/career_coaching_assistant.py

Enhanced with integration to the new resume analysis system.
"""

import streamlit as st
import pandas as pd
import json
import datetime
from pathlib import Path
import random
import numpy as np

# Import shared components
try:
    from shared.components import render_section_header, check_authentication
    SHARED_COMPONENTS_AVAILABLE = True
except ImportError:
    SHARED_COMPONENTS_AVAILABLE = False
    
def check_authentication():
    """Fallback authentication check"""
    return st.session_state.get('user_authenticated', True)

def render_section_header(title, icon="💼"):
    """Fallback section header"""
    st.markdown(f"## {icon} {title}")

# Page Configuration
st.set_page_config(
    page_title="Interview Coach - IntelliCV",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication Check
if not check_authentication():
    st.error("🔒 Please log in to access Interview Coach.")
    st.stop()

# Page Header
st.markdown("""
<div style="display: flex; align-items: center; margin-bottom: 2rem;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1rem; border-radius: 10px; margin-right: 1rem;">
        <h1 style="color: white; margin: 0; font-size: 1.8rem;">
            💼 IntelliCV Interview Coach
        </h1>
        <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            AI-Powered Interview Preparation & Practice System
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize interview coaching data
if 'interview_data' not in st.session_state:
    st.session_state.interview_data = {
        'practice_sessions': [],
        'question_history': [],
        'performance_metrics': {},
        'custom_scenarios': []
    }

# Sidebar Navigation
st.sidebar.markdown("## 💼 Interview Coaching Hub")

interview_sections = {
    "🎯 Quick Prep": "quick_prep",
    "🤖 AI Interview Simulator": "simulator",
    "📚 Question Bank": "question_bank",
    "🎭 Role-Play Scenarios": "scenarios",
    "📊 Performance Analytics": "analytics",
    "🎪 Mock Interview": "mock_interview",
    "📝 STAR Method Coach": "star_method",
    "💡 Interview Tips": "tips"
}

selected_section = st.sidebar.radio(
    "Choose Coaching Mode:",
    options=list(interview_sections.keys()),
    index=0
)

section_key = interview_sections[selected_section]

# Integration with resume analysis
resume_data = st.session_state.get('resume_data', {})
spider_analysis = st.session_state.get('user_skill_adjustments', {})

if resume_data:
    st.sidebar.markdown("### 🔗 Resume Integration")
    st.sidebar.success("✅ Resume data connected")
    st.sidebar.metric("Career Level", resume_data.get('career_level', 'Unknown'))
    st.sidebar.metric("Key Skills", len(resume_data.get('keywords_extracted', [])))
else:
    st.sidebar.info("💡 Upload resume in Resume Analysis for personalized coaching")

# ==================== QUICK PREP SECTION ====================
if section_key == "quick_prep":
    render_section_header("Quick Interview Preparation", "🎯")
    
    st.markdown("""
    ### 🚀 Get Ready in 15 Minutes
    Fast-track interview preparation based on your resume and target role.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Target role input
        target_role = st.text_input(
            "🎯 Target Role",
            placeholder="e.g., Senior Software Engineer, Product Manager, Data Scientist"
        )
        
        company_name = st.text_input(
            "🏢 Company Name (Optional)",
            placeholder="e.g., Google, Microsoft, Amazon"
        )
        
        interview_type = st.selectbox(
            "📞 Interview Type",
            ["Technical Interview", "Behavioral Interview", "Case Study", "Panel Interview", "Phone Screen"]
        )
        
        if st.button("🚀 Generate Prep Plan", type="primary"):
            if target_role:
                with st.spinner("🤖 AI is creating your personalized prep plan..."):
                    # Generate personalized prep plan
                    prep_plan = {
                        "role": target_role,
                        "company": company_name,
                        "type": interview_type,
                        "generated_at": datetime.datetime.now().isoformat(),
                        "key_areas": [],
                        "likely_questions": [],
                        "your_strengths": [],
                        "areas_to_prepare": []
                    }
                    
                    # Analyze user's background from resume
                    if resume_data:
                        user_skills = resume_data.get('keywords_extracted', [])
                        prep_plan['your_strengths'] = user_skills[:5]
                        prep_plan['areas_to_prepare'] = [
                            "System design concepts",
                            "Leadership examples",
                            "Problem-solving scenarios"
                        ]
                    
                    # Generate role-specific questions
                    question_templates = {
                        "Technical Interview": [
                            f"How would you approach designing a {target_role.lower()} system?",
                            f"What's your experience with the core technologies used in {target_role.lower()} roles?",
                            f"Walk me through a challenging technical problem you solved.",
                            f"How do you ensure code quality in {target_role.lower()} projects?"
                        ],
                        "Behavioral Interview": [
                            "Tell me about a time you had to work with a difficult team member.",
                            "Describe a situation where you had to meet a tight deadline.",
                            "Give me an example of when you showed leadership.",
                            "How do you handle feedback and criticism?"
                        ]
                    }
                    
                    prep_plan['likely_questions'] = question_templates.get(interview_type, [
                        f"Why are you interested in this {target_role} position?",
                        f"What makes you a good fit for {target_role}?",
                        "What are your salary expectations?",
                        "Do you have any questions for me?"
                    ])
                    
                    st.session_state.current_prep_plan = prep_plan
                
                st.success("✅ Prep plan generated!")
                st.rerun()
            else:
                st.warning("Please enter a target role first.")
    
    with col2:
        st.markdown("### 💡 Quick Tips")
        st.info("""
        **Before You Start:**
        • Research the company & role
        • Review your resume thoroughly  
        • Prepare STAR method examples
        • Practice out loud
        
        **During Interview:**
        • Listen carefully to questions
        • Take a moment to think
        • Use specific examples
        • Ask thoughtful questions
        """)
    
    # Display generated prep plan
    if 'current_prep_plan' in st.session_state:
        plan = st.session_state.current_prep_plan
        
        st.markdown("### 📋 Your Personalized Prep Plan")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 💪 Your Strengths")
            for strength in plan['your_strengths']:
                st.success(f"✅ {strength}")
        
        with col2:
            st.markdown("#### 📚 Areas to Prepare")
            for area in plan['areas_to_prepare']:
                st.warning(f"📖 {area}")
        
        with col3:
            st.markdown("#### 🎯 Key Focus Areas")
            focus_areas = ["Technical depth", "Leadership examples", "Company alignment", "Questions to ask"]
            for area in focus_areas:
                st.info(f"🎯 {area}")
        
        st.markdown("#### ❓ Likely Questions")
        for i, question in enumerate(plan['likely_questions'], 1):
            with st.expander(f"Question {i}: {question}"):
                st.markdown("**💡 How to approach this question:**")
                st.write("• Use the STAR method (Situation, Task, Action, Result)")
                st.write("• Be specific with examples from your experience")
                st.write("• Highlight relevant skills and achievements")
                st.write("• Connect your answer to the role requirements")
                
                if st.button(f"🎤 Practice This Question", key=f"practice_{i}"):
                    st.info("Starting practice mode for this question...")

# ==================== AI INTERVIEW SIMULATOR ====================
elif section_key == "simulator":
    render_section_header("AI Interview Simulator", "🤖")
    
    st.markdown("""
    ### 🤖 Practice with AI Interviewer
    Realistic interview simulation with instant feedback and performance analysis.
    """)
    
    # Simulator settings
    col1, col2 = st.columns([3, 1])
    
    with col1:
        simulation_mode = st.selectbox(
            "🎭 Simulation Mode",
            ["Friendly Interviewer", "Technical Expert", "Behavioral Specialist", "Challenging Interviewer"]
        )
        
        difficulty_level = st.select_slider(
            "📈 Difficulty Level",
            options=["Beginner", "Intermediate", "Advanced", "Expert"],
            value="Intermediate"
        )
        
        session_length = st.selectbox(
            "⏱️ Session Length",
            ["Quick (5 questions)", "Standard (10 questions)", "Comprehensive (15 questions)", "Full Interview (30 minutes)"]
        )
    
    with col2:
        st.markdown("### 🎯 AI Features")
        st.info("""
        • **Real-time feedback**
        • **Speech analysis** 
        • **Confidence scoring**
        • **Answer quality assessment**
        • **Performance tracking**
        """)
    
    if st.button("🚀 Start AI Interview", type="primary"):
        st.markdown("### 🎤 Interview Session")
        
        # Mock interview questions based on user profile
        questions = [
            "Tell me about yourself and your background.",
            "Why are you interested in this position?",
            "What's your greatest professional achievement?",
            "Describe a challenging situation you faced at work.",
            "Where do you see yourself in 5 years?"
        ]
        
        if 'current_question_index' not in st.session_state:
            st.session_state.current_question_index = 0
        
        current_q = st.session_state.current_question_index
        
        if current_q < len(questions):
            st.markdown(f"#### Question {current_q + 1}: {questions[current_q]}")
            
            # Answer input
            user_answer = st.text_area(
                "Your Answer:",
                height=150,
                placeholder="Type your answer here... (In a real interview, you'd speak aloud)"
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("⏭️ Next Question"):
                    if user_answer:
                        # Simulate AI feedback
                        feedback = {
                            "answer": user_answer,
                            "question": questions[current_q],
                            "timestamp": datetime.datetime.now().isoformat(),
                            "ai_score": random.randint(75, 95),
                            "feedback": "Good use of specific examples. Consider adding more quantifiable results."
                        }
                        
                        if 'interview_session' not in st.session_state:
                            st.session_state.interview_session = []
                        st.session_state.interview_session.append(feedback)
                        
                        st.session_state.current_question_index = current_q + 1
                        st.rerun()
                    else:
                        st.warning("Please provide an answer first.")
            
            with col2:
                if st.button("🔄 Skip Question"):
                    st.session_state.current_question_index = current_q + 1
                    st.rerun()
            
            with col3:
                if st.button("🛑 End Session"):
                    st.session_state.current_question_index = len(questions)
                    st.rerun()
            
            # Real-time feedback simulation
            if user_answer:
                st.markdown("#### 🤖 AI Analysis (Real-time)")
                
                # Simulate AI analysis
                word_count = len(user_answer.split())
                sentiment_score = random.uniform(0.6, 0.9)
                confidence_score = random.randint(70, 90)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Word Count", word_count, delta=f"Target: 150-200")
                with col2:
                    st.metric("Confidence Score", f"{confidence_score}%")
                with col3:
                    st.metric("Sentiment", f"{sentiment_score:.0%}", delta="Positive")
                
                # Feedback suggestions
                suggestions = []
                if word_count < 50:
                    suggestions.append("💡 Consider providing more detail and specific examples")
                if word_count > 300:
                    suggestions.append("⚠️ Try to be more concise - aim for 1-2 minutes speaking time")
                if "I" in user_answer and user_answer.count("I") > 5:
                    suggestions.append("🎯 Good use of personal examples - keep it up!")
                
                if suggestions:
                    st.markdown("**💡 Real-time Suggestions:**")
                    for suggestion in suggestions:
                        st.write(suggestion)
        
        else:
            # Interview complete
            st.success("🎉 Interview simulation complete!")
            
            if 'interview_session' in st.session_state and st.session_state.interview_session:
                st.markdown("### 📊 Session Summary")
                
                session_data = st.session_state.interview_session
                avg_score = sum(q['ai_score'] for q in session_data) / len(session_data)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Overall Score", f"{avg_score:.0f}%")
                with col2:
                    st.metric("Questions Answered", len(session_data))
                with col3:
                    st.metric("Session Duration", "15 min") # Mock duration
                
                # Detailed feedback
                st.markdown("### 📝 Detailed Feedback")
                
                for i, q_data in enumerate(session_data, 1):
                    with st.expander(f"Question {i}: {q_data['question'][:50]}..."):
                        st.write(f"**Your Answer:** {q_data['answer'][:100]}...")
                        st.write(f"**AI Score:** {q_data['ai_score']}%")
                        st.write(f"**Feedback:** {q_data['feedback']}")
            
            if st.button("🔄 Start New Session"):
                st.session_state.current_question_index = 0
                if 'interview_session' in st.session_state:
                    del st.session_state.interview_session
                st.rerun()

# ==================== QUESTION BANK SECTION ====================
elif section_key == "question_bank":
    render_section_header("Interview Question Bank", "📚")
    
    st.markdown("""
    ### 📚 Comprehensive Question Database
    Browse, practice, and master common interview questions by category.
    """)
    
    # Question categories
    question_categories = {
        "👤 Behavioral": [
            "Tell me about yourself",
            "Why do you want to work here?",
            "What's your greatest strength?",
            "What's your biggest weakness?",
            "Describe a challenging situation you faced",
            "Tell me about a time you showed leadership",
            "How do you handle conflict?",
            "Why are you leaving your current job?"
        ],
        "💻 Technical": [
            "Explain your technical background",
            "How do you approach problem-solving?",
            "Describe your development process",
            "What's your experience with [specific technology]?",
            "How do you ensure code quality?",
            "Tell me about a technical challenge you solved",
            "How do you stay updated with technology trends?",
            "Explain a complex technical concept simply"
        ],
        "🎯 Situational": [
            "How would you handle a tight deadline?",
            "What would you do if you disagreed with your manager?",
            "How do you prioritize competing tasks?",
            "Tell me about a time you made a mistake",
            "How do you handle working with difficult people?",
            "Describe a time you had to learn something quickly",
            "How do you handle stress and pressure?",
            "What would you do in your first 90 days?"
        ],
        "🏢 Company-Specific": [
            "Why do you want to work for our company?",
            "What do you know about our products/services?",
            "How would you contribute to our team?",
            "What interests you about this role?",
            "How do you align with our company values?",
            "What questions do you have for us?",
            "What are your salary expectations?",
            "When can you start?"
        ]
    }
    
    selected_category = st.selectbox(
        "📂 Select Question Category",
        list(question_categories.keys())
    )
    
    category_questions = question_categories[selected_category]
    
    st.markdown(f"### {selected_category} Questions")
    
    for i, question in enumerate(category_questions, 1):
        with st.expander(f"{i}. {question}"):
            st.markdown("**💡 Approach Strategy:**")
            
            if "behavioral" in selected_category.lower():
                st.write("• Use the STAR method (Situation, Task, Action, Result)")
                st.write("• Choose examples that highlight your skills")
                st.write("• Be specific with metrics and outcomes")
            elif "technical" in selected_category.lower():
                st.write("• Demonstrate your technical depth")
                st.write("• Use specific examples from your experience")
                st.write("• Show your problem-solving process")
            elif "situational" in selected_category.lower():
                st.write("• Think through the scenario step-by-step")
                st.write("• Show your decision-making process")
                st.write("• Demonstrate relevant soft skills")
            else:
                st.write("• Research the company thoroughly")
                st.write("• Align your answer with company values")
                st.write("• Show genuine interest and enthusiasm")
            
            # Practice area
            st.markdown("**🎤 Practice Your Answer:**")
            practice_answer = st.text_area(
                "Your answer:",
                key=f"practice_{selected_category}_{i}",
                height=100,
                placeholder="Type your practice answer here..."
            )
            
            if practice_answer:
                # Simple analysis
                word_count = len(practice_answer.split())
                if word_count < 30:
                    st.info("💡 Consider adding more detail to your answer")
                elif word_count > 200:
                    st.warning("⚠️ Try to be more concise for better impact")
                else:
                    st.success("✅ Good answer length!")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"💾 Save Answer", key=f"save_{i}"):
                    st.success("Answer saved to your practice history!")
            with col2:
                if st.button(f"🎯 Get AI Feedback", key=f"feedback_{i}"):
                    if practice_answer:
                        st.info("🤖 AI Feedback: Good structure! Consider adding more specific metrics to strengthen your example.")
                    else:
                        st.warning("Please write an answer first to get feedback.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>💼 <strong>IntelliCV Interview Coach</strong> - AI-Powered Interview Preparation</p>
    <p>Practice makes perfect - prepare with confidence for your next opportunity</p>
</div>
""", unsafe_allow_html=True)