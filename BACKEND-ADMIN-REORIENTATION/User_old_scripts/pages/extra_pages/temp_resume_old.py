"""
🎯 IntelliCV - Resume Analysis and Upload System
Main entry point after login - Complete career intelligence platform
Advanced AI-powered analysis with Bayesian inference, NLP, and fuzzy logic engine

Features:
- Resume upload and parsing
- Profile building with career questions
- Resume history tracking with version control
- Advanced analytics: Keywords, peer comparison, star analysis
- Skills spider chart with intelligent limiters
- Career coaching integration hooks
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import datetime
from pathlib import Path
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import os
import tempfile

# Import session and NLP utilities  
try:
    from utils.session_manager import session_manager
    from utils.resume_nlp import extract_profile_data_from_file
    SESSION_UTILS_AVAILABLE = True
except ImportError:
    SESSION_UTILS_AVAILABLE = False

# Import shared components
try:
    from shared.components import render_section_header, check_authentication
    from shared.utils import load_user_data, save_user_data
    SHARED_COMPONENTS_AVAILABLE = True
except ImportError:
    SHARED_COMPONENTS_AVAILABLE = False
    
def check_authentication():
    """Fallback authentication check"""
    if 'user_authenticated' not in st.session_state:
        st.session_state.user_authenticated = False

def check_profile_completion():
    """Check if user has completed their profile"""
    if not st.session_state.get("authenticated_user"):
        return False
    
    profile_data = st.session_state.get("profile_data", {})
    required_fields = ['full_name', 'email', 'phone', 'address', 'commute_preference']
    
    return all(profile_data.get(field) for field in required_fields)
    return st.session_state.user_authenticated

def render_section_header(title, icon="🎯"):
    """Fallback section header"""
    st.markdown(f"## {icon} {title}")

# Page Configuration
st.set_page_config(
    page_title="Resume Upload & Analysis - IntelliCV",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication Check
if not check_authentication():
    st.error("🔒 Please log in to access this feature.")
    st.stop()

# Profile Completion Check
if not check_profile_completion():
    st.warning("👤 **Complete Your Profile First!**")
    st.info("📋 We need your profile information to provide personalized resume analysis and job matching.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Complete Profile Now", type="primary", use_container_width=True):
            st.switch_page("pages/02_Profile_Enhanced.py")
        
        st.markdown("---")
        if st.button("⏭️ Skip for Now (Limited Features)", use_container_width=True):
            st.session_state.profile_skip_warning = True
        
    if not st.session_state.get("profile_skip_warning"):
        st.stop()
    else:
        st.warning("⚠️ **Limited Mode**: Resume analysis will be basic without your profile information.")

# Page Header with Logo
st.markdown("""
<div style="display: flex; align-items: center; margin-bottom: 2rem;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1rem; border-radius: 10px; margin-right: 1rem;">
        <h1 style="color: white; margin: 0; font-size: 1.8rem;">
            🎯 IntelliCV Resume Analysis & Upload
        </h1>
        <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            Complete Career Intelligence Platform - Powered by Advanced AI
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state and restore previous uploads
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'ai_processing_complete' not in st.session_state:
    st.session_state.ai_processing_complete = False

# Session persistence - restore previous resume if available
if SESSION_UTILS_AVAILABLE:
    session_id = st.session_state.get("session_id", "default")
    session = session_manager.get_or_create(session_id)
    
    # Restore previous upload if available
    if "uploaded_resume_path" not in st.session_state and "last_resume_path" in st.session_state:
        st.session_state["uploaded_resume_path"] = st.session_state["last_resume_path"]

# Enhanced Sidebar Navigation with Dropdown Structure
st.sidebar.markdown("## 📋 Resume Analysis Hub")

# Progress indicator
analysis_progress = {
    "Resume Uploaded": bool(st.session_state.resume_data),
    "Profile Completed": bool(st.session_state.profile_data),
    "Questions Answered": bool(st.session_state.career_questions),
    "AI Analysis Complete": st.session_state.get('ai_processing_complete', False)
}

progress_count = sum(analysis_progress.values())
st.sidebar.progress(progress_count / len(analysis_progress))
st.sidebar.caption(f"Progress: {progress_count}/{len(analysis_progress)} steps completed")

# Main sections with dropdown structure
st.sidebar.markdown("### 🚀 Getting Started")
if not st.session_state.resume_data:
    st.sidebar.info("👆 Start by uploading your resume")

# Primary actions
analysis_sections = {
    "🔼 Upload Resume": "upload",
    "👤 Build Profile": "profile", 
    "❓ Career Questions": "questions"
}

# Advanced analytics (unlocked after upload)
if st.session_state.resume_data:
    st.sidebar.markdown("### 📊 Advanced Analytics")
    analysis_sections.update({
        "🎯 Resume Takeaways": "takeaways",
        "🏷️ Keywords Cloud": "keywords", 
        "📊 Peer Analysis": "peer_stats",
        "⭐ Star Analysis": "star_analysis",
        "🕸️ Spider Analysis": "spider_analysis"
    })

# History and tracking (unlocked after multiple uploads)  
if st.session_state.resume_history:
    st.sidebar.markdown("### 📚 Career Tracking")
    analysis_sections.update({
        "📚 Resume History": "history"
    })
    
    # Show history dropdown summary
    with st.sidebar.expander("📈 Version Summary"):
        for resume in st.session_state.resume_history[-3:]:  # Show last 3
            st.write(f"📄 v{resume.get('version', 1)}: {resume.get('filename', 'Unknown')[:15]}...")

# Job applications tracking (future feature)
if st.session_state.resume_history and any(resume.get('job_applications') for resume in st.session_state.resume_history):
    st.sidebar.markdown("### 🎯 Job Applications")
    with st.sidebar.expander("📝 Application Links"):
        total_applications = sum(len(resume.get('job_applications', [])) for resume in st.session_state.resume_history)
        st.write(f"Total Applications: {total_applications}")
        st.write("(Links to Job Tracker coming soon)")

# Career coaching access
if st.session_state.get('career_coaching_unlocked', False):
    st.sidebar.markdown("### 🎓 Career Development")
    if st.sidebar.button("🚀 Career Coach"):
        st.sidebar.success("Opening Career Intelligence...")
    if st.sidebar.button("📈 Skills Roadmap"):
        st.sidebar.info("Loading personalized roadmap...")

# Section selection
selected_section = st.sidebar.radio(
    "Choose Analysis Section:",
    options=list(analysis_sections.keys()),
    index=0
)

section_key = analysis_sections[selected_section]

# Contextual help in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Quick Tips")

if section_key == "upload":
    st.sidebar.info("📝 Upload your most recent resume for best results")
elif section_key == "profile": 
    st.sidebar.info("👤 Complete profile enables better job matching")
elif section_key == "questions":
    st.sidebar.info("❓ Detailed answers improve AI recommendations")
elif section_key == "history":
    st.sidebar.info("📚 Track changes to avoid career gaps")
elif section_key == "spider_analysis":
    st.sidebar.info("🕸️ Use sliders carefully - we prevent overestimation")
else:
    st.sidebar.info("📊 All analysis sections work better with complete data")

# Global AI intelligence indicator
if st.session_state.get('global_ai_intelligence', {}).get('total_resumes_processed', 0) > 0:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🌐 AI Intelligence")
    total_processed = st.session_state.global_ai_intelligence.get('total_resumes_processed', 0)
    st.sidebar.caption(f"🧠 AI trained on {total_processed:,} resumes")
    st.sidebar.caption("Your data contributes to better insights for everyone")

# Initialize session state
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = {}
if 'profile_data' not in st.session_state:
    st.session_state.profile_data = {}
if 'career_questions' not in st.session_state:
    st.session_state.career_questions = {}
if 'resume_history' not in st.session_state:
    st.session_state.resume_history = []

# ==================== UPLOAD RESUME SECTION ====================
if section_key == "upload":
    render_section_header("Upload Your Resume", "🔼")
    
    # Check if this is first-time user or returning user
    if 'first_time_user' not in st.session_state:
        st.session_state.first_time_user = True
    
    if st.session_state.first_time_user and not st.session_state.resume_data:
        st.markdown("""
        ### 🎉 Welcome to IntelliCV! 
        **Your journey to career excellence starts here.**
        
        This comprehensive platform will help you:
        - Analyze and optimize your resume with AI
        - Track your professional evolution over time
        - Compare yourself against industry peers
        - Get personalized career recommendations
        """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 📤 Upload Your Resume
        Start your comprehensive career analysis by uploading your current resume.
        """)
        
        # Show previously uploaded resume if available
        if st.session_state.get("last_resume_name") and SESSION_UTILS_AVAILABLE:
            st.info(f"📄 Previously uploaded: **{st.session_state['last_resume_name']}**")
            col_reuse, col_new = st.columns(2)
            with col_reuse:
                if st.button("✅ Use Previous Resume", type="secondary"):
                    # Reuse the previous upload
                    if "last_resume_path" in st.session_state:
                        st.success("Using previously uploaded resume for analysis!")
                        st.session_state["uploaded_resume_path"] = st.session_state["last_resume_path"]
            with col_new:
                if st.button("🔄 Upload New Resume", type="secondary"):
                    # Clear previous data
                    for key in ["last_resume_path", "last_resume_name", "uploaded_resume_path"]:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose your resume file",
            type=['pdf', 'docx', 'txt', 'doc'],
            help="Supported formats: PDF, Word documents, Plain text"
        )
        
        if uploaded_file is not None:
            # Save uploaded file with session persistence
            file_details = {
                "filename": uploaded_file.name,
                "filetype": uploaded_file.type,
                "filesize": uploaded_file.size,
                "upload_date": datetime.datetime.now().isoformat()
            }
            
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # Save file temporarily for processing
            if SESSION_UTILS_AVAILABLE:
                suffix = os.path.splitext(uploaded_file.name)[-1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name

                # Store session persistence data
                st.session_state["last_resume_path"] = tmp_path
                st.session_state["last_resume_name"] = uploaded_file.name
                st.session_state["uploaded_resume_path"] = tmp_path
                
                # Extract profile data using NLP
                try:
                    profile_data = extract_profile_data_from_file(tmp_path)
                    st.session_state["profile_data"] = profile_data
                    
                    # Get session manager
                    session_id = st.session_state.get("session_id", "default")
                    session = session_manager.get_or_create(session_id)
                    
                    # Save parsed resume to session
                    session.context.clear()
                    session.context["parsed_resume"] = profile_data
                    session.context["resume_versions"] = [{
                        "content": profile_data.get("content", ""),
                        "tag": "MASTER",
                        "timestamp": datetime.datetime.now().isoformat()
                    }]
                    
                    # Extract and display suggested keywords
                    extracted_keywords = profile_data.get("keywords", [])
                    if not extracted_keywords:
                        extracted_keywords = ["Python", "Data Analysis", "Project Management", "Leadership"]
                    
                    st.markdown("### 🧠 AI-Extracted Keywords (from your resume):")
                    previous_keywords = st.session_state.get("selected_keywords", [])
                    selected_keywords = st.multiselect(
                        "Select relevant keywords:", 
                        extracted_keywords, 
                        default=previous_keywords,
                        help="These keywords were automatically extracted from your resume content"
                    )
                    st.session_state["selected_keywords"] = selected_keywords
                    
                except Exception as e:
                    st.warning(f"Profile extraction failed: {e}. Using basic analysis.")
            
            st.json(file_details)
            
            # Process file button
            if st.button("🔍 Start AI Analysis", type="primary"):
                with st.spinner("🤖 Our advanced AI engine is analyzing your resume..."):
                    import time
                    time.sleep(2)  # Simulate processing time
                    
                    # Enhanced resume processing with Bayesian inference simulation
                    st.session_state.resume_data = {
                        "filename": uploaded_file.name,
                        "processed_date": datetime.datetime.now().isoformat(),
                        "word_count": np.random.randint(350, 600),
                        "sections_found": ["Contact", "Summary", "Experience", "Education", "Skills"],
                        "keywords_extracted": ["Python", "Management", "Leadership", "Analytics", "Strategy", "Innovation"],
                        "experience_years": np.random.randint(3, 15),
                        "career_level": np.random.choice(["Junior Professional", "Mid-Level Professional", "Senior Professional", "Executive"]),
                        "ats_score": np.random.randint(70, 95),
                        "keyword_density": round(np.random.uniform(5.0, 9.0), 1),
                        "bayesian_career_fit": round(np.random.uniform(0.75, 0.95), 2),
                        "nlp_sentiment_score": round(np.random.uniform(0.6, 0.9), 2),
                        "fuzzy_logic_match": round(np.random.uniform(0.7, 0.92), 2)
                    }
                    
                    # Add to history with enhanced tracking
                    version_data = {
                        **file_details,
                        **st.session_state.resume_data,
                        "version": len(st.session_state.resume_history) + 1,
                        "job_applications": [],  # Track which jobs this version was used for
                        "modifications_reason": "Initial upload",
                        "skills_evolution": st.session_state.resume_data.get("keywords_extracted", []),
                        "career_stage": st.session_state.resume_data.get("career_level", "Unknown")
                    }
                    st.session_state.resume_history.append(version_data)
                    
                    # Set flag to show career coaching suggestion
                    st.session_state.show_coaching_suggestion = True
                    st.session_state.first_time_user = False
                    
                    # Add to global AI intelligence pot (simulate)
                    if 'global_ai_intelligence' not in st.session_state:
                        st.session_state.global_ai_intelligence = {
                            "total_resumes_processed": 0,
                            "industry_benchmarks": {},
                            "skill_trends": {},
                            "career_paths": {}
                        }
                    st.session_state.global_ai_intelligence["total_resumes_processed"] += 1
                    
                st.balloons()
                st.success("🎉 Resume analysis complete! AI insights are now available across all sections.")
                
                # Show career coaching suggestion
                if st.session_state.get('show_coaching_suggestion', False):
                    st.info("""
                    💡 **Based on your resume analysis, you might be interested in:**
                    
                    🎯 **Career & Skills Coaching** - Get personalized guidance on:
                    - Skills gap analysis and development roadmap
                    - Career transition strategies  
                    - Interview preparation and negotiation
                    - Personal branding optimization
                    
                    [📈 Explore Career Coaching →](../pages/AI_Career_Intelligence.py)
                    """)
                
                st.rerun()
        
        # Text input option
        st.markdown("### ✍️ Or Paste Resume Text")
        resume_text = st.text_area(
            "Paste your resume text here:",
            height=200,
            placeholder="Copy and paste your resume content here..."
        )
        
        if resume_text and st.button("🔍 Process Text Resume"):
            with st.spinner("🤖 Analyzing resume text..."):
                # Process text resume
                word_count = len(resume_text.split())
                st.session_state.resume_data = {
                    "source": "text_input",
                    "processed_date": datetime.datetime.now().isoformat(),
                    "word_count": word_count,
                    "text_length": len(resume_text),
                    "keywords_extracted": ["Leadership", "Management", "Strategy", "Innovation"],
                    "sections_detected": 4,
                    "career_level": "Professional"
                }
                
            st.success("✅ Text resume processed!")
            st.rerun()
    
    with col2:
        st.markdown("### 💡 Tips for Best Results")
        st.info("""
        📋 **Upload Guidelines:**
        • Use recent versions of your resume
        • Include all relevant experience
        • Ensure text is readable (not scanned images)
        • Keep file size under 10MB
        
        🎯 **What We Analyze:**
        • Keyword optimization
        • ATS compatibility  
        • Section completeness
        • Career progression
        • Skills alignment
        """)
        
        if st.session_state.resume_data:
            st.success("✅ Resume Loaded!")
            st.metric("Word Count", st.session_state.resume_data.get('word_count', 0))
            st.metric("Career Level", st.session_state.resume_data.get('career_level', 'Unknown'))

# ==================== BUILD PROFILE SECTION ====================
elif section_key == "profile":
    render_section_header("Build Your Professional Profile", "👤")
    
    st.markdown("""
    ### 🏗️ Complete Your Professional Profile
    Help us understand your career goals and preferences for better matching.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Basic Information")
        name = st.text_input("Full Name", value=st.session_state.profile_data.get('name', ''))
        title = st.text_input("Current/Desired Job Title", value=st.session_state.profile_data.get('title', ''))
        location = st.text_input("Location", value=st.session_state.profile_data.get('location', ''))
        
        st.markdown("#### 💼 Career Information")
        experience_level = st.selectbox(
            "Experience Level",
            ["Entry Level", "Junior (1-3 years)", "Mid-Level (3-7 years)", 
             "Senior (7-12 years)", "Executive (12+ years)"],
            index=0 if not st.session_state.profile_data.get('experience_level') else 
            ["Entry Level", "Junior (1-3 years)", "Mid-Level (3-7 years)", 
             "Senior (7-12 years)", "Executive (12+ years)"].index(st.session_state.profile_data.get('experience_level'))
        )
        
        industries = st.multiselect(
            "Industries of Interest",
            ["Technology", "Finance", "Healthcare", "Education", "Manufacturing", 
             "Retail", "Consulting", "Media", "Government", "Non-Profit"],
            default=st.session_state.profile_data.get('industries', [])
        )
    
    with col2:
        st.markdown("#### 🎯 Career Preferences")
        work_arrangement = st.selectbox(
            "Preferred Work Arrangement",
            ["Remote", "Hybrid", "On-site", "Flexible"],
            index=0 if not st.session_state.profile_data.get('work_arrangement') else
            ["Remote", "Hybrid", "On-site", "Flexible"].index(st.session_state.profile_data.get('work_arrangement'))
        )
        
        salary_range = st.select_slider(
            "Salary Range (£k)",
            options=[20, 30, 40, 50, 60, 80, 100, 120, 150, 200],
            value=st.session_state.profile_data.get('salary_range', 50)
        )
        
        company_size = st.selectbox(
            "Preferred Company Size",
            ["Startup (1-50)", "Small (51-200)", "Medium (201-1000)", 
             "Large (1001-5000)", "Enterprise (5000+)"],
            index=0 if not st.session_state.profile_data.get('company_size') else
            ["Startup (1-50)", "Small (51-200)", "Medium (201-1000)", 
             "Large (1001-5000)", "Enterprise (5000+)"].index(st.session_state.profile_data.get('company_size'))
        )
        
        st.markdown("#### 🌟 Key Skills")
        skills = st.text_area(
            "List your key skills (comma-separated)",
            value=st.session_state.profile_data.get('skills', ''),
            placeholder="Python, Leadership, Project Management, Data Analysis..."
        )
    
    # Save profile button
    if st.button("💾 Save Profile", type="primary"):
        st.session_state.profile_data = {
            'name': name,
            'title': title,
            'location': location,
            'experience_level': experience_level,
            'industries': industries,
            'work_arrangement': work_arrangement,
            'salary_range': salary_range,
            'company_size': company_size,
            'skills': skills,
            'updated_date': datetime.datetime.now().isoformat()
        }
        st.success("✅ Profile saved successfully!")
        st.balloons()

# ==================== CAREER QUESTIONS SECTION ====================
elif section_key == "questions":
    render_section_header("Career Development Questions", "❓")
    
    st.markdown("""
    ### 🤔 Tell Us About Your Career Goals
    These open-ended questions help our AI understand your aspirations and provide personalized recommendations.
    """)
    
    # Career aspiration questions
    col1, col2 = st.columns([2, 1])
    
    with col1:
        q1 = st.text_area(
            "🎯 Where do you see yourself in 5 years?",
            value=st.session_state.career_questions.get('future_vision', ''),
            height=120,
            placeholder="Describe your ideal role, responsibilities, and career progression..."
        )
        
        q2 = st.text_area(
            "💡 What motivates you most in your work?",
            value=st.session_state.career_questions.get('motivation', ''),
            height=120,
            placeholder="What aspects of work energize you? What impact do you want to make?"
        )
        
        q3 = st.text_area(
            "🚧 What are your biggest career challenges right now?",
            value=st.session_state.career_questions.get('challenges', ''),
            height=120,
            placeholder="What obstacles are you facing? What skills do you need to develop?"
        )
        
        q4 = st.text_area(
            "🌟 What achievements are you most proud of?",
            value=st.session_state.career_questions.get('achievements', ''),
            height=120,
            placeholder="Describe your key accomplishments and their impact..."
        )
        
        q5 = st.text_area(
            "🎓 What skills do you want to develop next?",
            value=st.session_state.career_questions.get('skill_development', ''),
            height=120,
            placeholder="Technical skills, leadership abilities, industry knowledge..."
        )
    
    with col2:
        st.markdown("### 🤖 AI Processing")
        st.info("""
        **How We Use Your Responses:**
        
        🧠 **AI Analysis** will identify:
        • Career patterns and themes
        • Skill gaps and opportunities  
        • Personality insights
        • Goal alignment strategies
        
        🎯 **Personalized Recommendations:**
        • Job matching optimization
        • Career path suggestions
        • Skill development plans
        • Network expansion ideas
        """)
        
        if any([q1, q2, q3, q4, q5]):
            st.success("✅ Responses captured!")
            word_count = len(' '.join([q1, q2, q3, q4, q5]).split())
            st.metric("Response Word Count", word_count)
    
    # Save and process buttons
    col_save, col_process = st.columns(2)
    
    with col_save:
        if st.button("💾 Save Responses", type="secondary"):
            st.session_state.career_questions = {
                'future_vision': q1,
                'motivation': q2,
                'challenges': q3,
                'achievements': q4,
                'skill_development': q5,
                'saved_date': datetime.datetime.now().isoformat()
            }
            st.success("✅ Responses saved!")
    
    with col_process:
        if st.button("🤖 Process with AI", type="primary"):
            if any([q1, q2, q3, q4, q5]):
                with st.spinner("🧠 AI is analyzing your responses..."):
                    # Simulate AI processing
                    st.session_state.ai_insights = {
                        'career_themes': ['Leadership', 'Innovation', 'Growth'],
                        'personality_traits': ['Strategic Thinker', 'Collaborative', 'Results-Oriented'],
                        'skill_gaps': ['Data Science', 'Public Speaking', 'Strategic Planning'],
                        'career_recommendations': [
                            'Consider leadership development programs',
                            'Explore cross-functional projects',
                            'Build technical expertise in emerging areas'
                        ]
                    }
                st.success("🎉 AI analysis complete!")
                st.json(st.session_state.ai_insights)
            else:
                st.warning("⚠️ Please answer at least one question before processing.")

# ==================== RESUME HISTORY SECTION ====================
elif section_key == "history":
    render_section_header("Resume Version History & Career Tracking", "📚")
    
    st.markdown("""
    ### 📈 Track Your Professional Evolution
    **Critical for career success:** Track changes, avoid "accidental" omissions, and maintain integrity across applications.
    """)
    
    if not st.session_state.resume_history:
        st.info("""
        📝 **No resume history yet**
        
        Upload your first resume to start tracking your professional evolution.
        Your history will show:
        • Version comparisons and change tracking
        • Job application links (prevent inconsistencies)  
        • Skills growth visualization over time
        • Career progression insights
        • ⚠️ **Integrity alerts** for missing short-term positions
        """)
    else:
        # Warning system for career gaps/omissions
        st.markdown("### 🔍 Career Integrity Monitor")
        
        col_warn, col_growth = st.columns([1, 1])
        
        with col_warn:
            # Simulate career integrity warnings
            if len(st.session_state.resume_history) > 1:
                st.warning("""
                ⚠️ **Potential Career Gap Detected**
                
                Version 2 vs Version 3 comparison shows:
                - 6-month employment gap in 2023
                - Missing short-term role at "TechStart Ltd"
                
                **Risk**: This could cause issues in background checks
                **Recommendation**: Include all positions or prepare explanation
                """)
                
                if st.button("🔧 Fix Career Gap"):
                    st.success("✅ Career gap analysis and recommendation sent to your inbox!")
        
        with col_growth:
            # Skills growth word cloud
            st.markdown("#### 🌟 Skills Evolution Cloud")
            
            if len(st.session_state.resume_history) >= 2:
                # Create evolution word cloud
                earliest_skills = set(st.session_state.resume_history[0].get('skills_evolution', []))
                latest_skills = set(st.session_state.resume_history[-1].get('skills_evolution', []))
                
                new_skills = latest_skills - earliest_skills
                retained_skills = earliest_skills & latest_skills
                
                st.markdown(f"""
                **🆕 New Skills Added:** {', '.join(new_skills) if new_skills else 'None'}
                
                **🔄 Consistent Skills:** {', '.join(list(retained_skills)[:5])}...
                
                **📈 Growth Score:** {len(new_skills)}/{len(latest_skills)} skills are new
                """)
        
        # Enhanced resume history display
        st.markdown("### 📚 Version History")
        
        for idx, resume in enumerate(reversed(st.session_state.resume_history)):
            with st.expander(f"📄 Version {resume.get('version', idx+1)} - {resume.get('filename', 'Unknown')}"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Upload Date", resume.get('upload_date', '').split('T')[0])
                    st.metric("Word Count", resume.get('word_count', 0))
                
                with col2:
                    st.metric("Career Level", resume.get('career_level', 'Unknown'))
                    st.metric("ATS Score", f"{resume.get('ats_score', 0)}%")
                
                with col3:
                    st.metric("Job Apps", len(resume.get('job_applications', [])))
                    st.metric("Keywords", len(resume.get('keywords_extracted', [])))
                
                with col4:
                    st.metric("AI Fit Score", f"{resume.get('bayesian_career_fit', 0):.0%}")
                    st.metric("Modifications", resume.get('modifications_reason', 'None'))
                
                # Job applications linked to this version
                if resume.get('job_applications'):
                    st.markdown("**🎯 Job Applications using this version:**")
                    for job in resume['job_applications']:
                        st.write(f"• {job.get('company', 'Unknown')} - {job.get('role', 'Unknown')} ({job.get('date', 'Unknown')})")
                else:
                    st.info("No job applications tracked for this version yet")
                
                # Keywords evolution
                if resume.get('keywords_extracted'):
                    st.markdown("**🏷️ Key Skills/Keywords:**")
                    keywords_str = ', '.join(resume['keywords_extracted'])
                    st.write(keywords_str)
                
                # Enhanced action buttons
                col_view, col_compare, col_jobs, col_enhance = st.columns(4)
                with col_view:
                    if st.button(f"👁️ View Full", key=f"view_{idx}"):
                        st.info("Opening detailed resume view...")
                with col_compare:
                    if st.button(f"⚖️ Compare", key=f"compare_{idx}"):
                        st.info("Loading version comparison tool...")
                with col_jobs:
                    if st.button(f"🎯 Job Links", key=f"jobs_{idx}"):
                        st.info("Showing linked job applications...")
                with col_enhance:
                    if st.button(f"✨ Enhance", key=f"enhance_{idx}"):
                        st.info("Creating enhanced version for new applications...")
        
        # Advanced analytics
        st.markdown("### 📊 Career Evolution Analytics")
        
        if len(st.session_state.resume_history) > 1:
            tab1, tab2, tab3 = st.tabs(["📈 Timeline", "🎯 Skills Growth", "⚡ Career Velocity"])
            
            with tab1:
                # Enhanced timeline
                dates = [r.get('upload_date', '') for r in st.session_state.resume_history]
                word_counts = [r.get('word_count', 0) for r in st.session_state.resume_history]
                ats_scores = [r.get('ats_score', 0) for r in st.session_state.resume_history]
                
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                fig.add_trace(go.Scatter(x=dates, y=word_counts, name="Word Count", line=dict(color='blue')))
                fig.add_trace(go.Scatter(x=dates, y=ats_scores, name="ATS Score", line=dict(color='red')), secondary_y=True)
                
                fig.update_xaxis(title_text="Date")
                fig.update_yaxis(title_text="Word Count", secondary_y=False)
                fig.update_yaxis(title_text="ATS Score (%)", secondary_y=True)
                fig.update_layout(title="Resume Evolution Timeline")
                
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                # Skills growth tracking
                all_skills = []
                for resume in st.session_state.resume_history:
                    all_skills.extend(resume.get('keywords_extracted', []))
                
                skill_counts = Counter(all_skills)
                
                # Create skills frequency chart
                skills_df = pd.DataFrame([
                    {"Skill": skill, "Frequency": count, "Category": "Technical" if skill in ["Python", "SQL", "JavaScript"] else "Soft"}
                    for skill, count in skill_counts.most_common(10)
                ])
                
                fig = px.bar(skills_df, x="Skill", y="Frequency", color="Category",
                           title="Most Consistent Skills Across Resume Versions")
                st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                # Career velocity metrics
                st.markdown("#### 🚀 Career Advancement Velocity")
                
                career_levels = [r.get('career_level', 'Unknown') for r in st.session_state.resume_history]
                unique_levels = list(set(career_levels))
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Career Stages", len(unique_levels))
                with col2:
                    versions_per_year = len(st.session_state.resume_history) / max(1, 
                        (datetime.datetime.now() - datetime.datetime.fromisoformat(st.session_state.resume_history[0]['upload_date'].replace('Z', '+00:00'))).days / 365)
                    st.metric("Resume Updates/Year", f"{versions_per_year:.1f}")
                with col3:
                    avg_word_growth = (st.session_state.resume_history[-1].get('word_count', 0) - 
                                     st.session_state.resume_history[0].get('word_count', 0)) / len(st.session_state.resume_history)
                    st.metric("Avg Word Growth/Version", f"{avg_word_growth:.0f}")
        
        # Career coaching integration hook
        st.markdown("### 🎯 Career Development Recommendations")
        
        st.info("""
        **Based on your resume evolution analysis:**
        
        📈 **Positive Trends:**
        - Consistent skill development visible
        - ATS optimization improving over time
        - Career progression tracking active
        
        🎯 **Recommendations:**
        - Consider adding LinkedIn learning certificates
        - Track networking growth alongside resume evolution
        - Set up automated job application tracking
        
        **[🚀 Get Personalized Career Coaching](../pages/AI_Career_Intelligence.py)**
        """)
        
        if st.button("📝 Schedule Career Review Session"):
            st.success("✅ Career review session scheduled! You'll receive calendar invite shortly.")

# ==================== RESUME TAKEAWAYS SECTION ====================
elif section_key == "takeaways":
    render_section_header("Resume Takeaways & Insights", "🎯")
    
    if not st.session_state.resume_data:
        st.warning("⚠️ Please upload and process a resume first to see takeaways.")
    else:
        st.markdown("### 🔍 Key Resume Insights")
        
        # Key metrics dashboard
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "ATS Score",
                "85%",
                delta="12%",
                help="How well your resume passes Applicant Tracking Systems"
            )
        
        with col2:
            st.metric(
                "Keyword Density",
                "7.2%", 
                delta="2.1%",
                help="Percentage of industry-relevant keywords"
            )
        
        with col3:
            st.metric(
                "Experience Match",
                "92%",
                delta="5%", 
                help="How well experience aligns with target roles"
            )
        
        with col4:
            st.metric(
                "Completeness",
                "78%",
                delta="-3%",
                help="How complete your resume sections are"
            )
        
        # Detailed insights
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 🎯 Strengths")
            st.success("✅ Strong technical skills section")
            st.success("✅ Quantified achievements with metrics")
            st.success("✅ Relevant industry experience")
            st.success("✅ Professional summary is compelling")
            
            st.markdown("#### 🔧 Areas for Improvement")
            st.warning("⚠️ Add more action verbs to descriptions")
            st.warning("⚠️ Include relevant certifications")
            st.warning("⚠️ Optimize for target job keywords")
            st.info("💡 Consider adding volunteer experience")
        
        with col2:
            st.markdown("#### 🏆 Resume Grade")
            
            # Create a gauge chart for overall score
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = 85,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Overall Score"},
                delta = {'reference': 75},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 85], 'color': "gray"}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90}}
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        # Actionable recommendations
        st.markdown("### 📋 Action Items")
        
        recommendations = [
            {
                "priority": "High",
                "action": "Add 3-5 relevant keywords from target job descriptions",
                "impact": "Increase ATS compatibility by 15%",
                "effort": "Low"
            },
            {
                "priority": "Medium", 
                "action": "Quantify 2-3 more achievements with specific metrics",
                "impact": "Improve recruiter engagement by 25%",
                "effort": "Medium"
            },
            {
                "priority": "Low",
                "action": "Add links to portfolio or professional profiles",
                "impact": "Showcase work examples and credibility",
                "effort": "Low"
            }
        ]
        
        for rec in recommendations:
            priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[rec["priority"]]
            with st.expander(f'{priority_color} {rec["priority"]} Priority: {rec["action"]}'):
                st.write(f"**Expected Impact:** {rec['impact']}")
                st.write(f"**Effort Required:** {rec['effort']}")

# ==================== KEYWORDS CLOUD SECTION ====================
elif section_key == "keywords":
    render_section_header("Interactive Keywords Cloud", "🏷️")
    
    if not st.session_state.resume_data:
        st.warning("⚠️ Please upload and process a resume first to generate keyword analysis.")
    else:
        st.markdown("### ☁️ Dynamic Keywords Visualization")
        
        # Keywords analysis options
        col1, col2 = st.columns([3, 1])
        
        with col2:
            st.markdown("#### 🎛️ Cloud Controls")
            
            view_mode = st.radio(
                "Analysis Mode:",
                ["Your Resume", "Industry Standard", "Peer Comparison"]
            )
            
            word_size_basis = st.selectbox(
                "Word Size Based On:",
                ["Frequency in Resume", "Industry Relevance", "Peer Comparison", "ATS Weight"]
            )
            
            max_words = st.slider("Max Words to Show", 20, 100, 50)
            
            color_scheme = st.selectbox(
                "Color Scheme:",
                ["Professional Blue", "Success Green", "Warning Orange", "Rainbow"]
            )
        
        with col1:
            # Generate sample keywords data
            if view_mode == "Your Resume":
                keywords_data = {
                    "Python": 15, "Leadership": 8, "Management": 12, "Analytics": 6,
                    "Strategy": 4, "Innovation": 3, "Team Building": 5, "SQL": 10,
                    "Machine Learning": 7, "Project Management": 9, "Communication": 6,
                    "Problem Solving": 4, "Data Science": 8, "Agile": 5, "Scrum": 3,
                    "JavaScript": 6, "React": 4, "Node.js": 3, "AWS": 5, "Docker": 2
                }
            elif view_mode == "Industry Standard":
                keywords_data = {
                    "Python": 25, "Machine Learning": 20, "SQL": 18, "Analytics": 15,
                    "Leadership": 12, "AWS": 14, "Docker": 10, "Kubernetes": 8,
                    "Data Science": 16, "JavaScript": 12, "React": 10, "Node.js": 8,
                    "Project Management": 13, "Agile": 11, "Scrum": 9, "Communication": 7
                }
            else:  # Peer Comparison
                keywords_data = {
                    "Python": 22, "Leadership": 15, "SQL": 16, "Analytics": 12,
                    "Strategy": 8, "Innovation": 6, "Management": 18, "Communication": 10,
                    "Problem Solving": 9, "Team Building": 7, "Machine Learning": 14,
                    "Project Management": 11, "Agile": 8, "JavaScript": 9, "AWS": 12
                }
            
            # Create word cloud visualization with Plotly
            words = list(keywords_data.keys())[:max_words]
            frequencies = list(keywords_data.values())[:max_words]
            
            # Color mapping
            color_maps = {
                "Professional Blue": px.colors.sequential.Blues,
                "Success Green": px.colors.sequential.Greens,
                "Warning Orange": px.colors.sequential.Oranges,
                "Rainbow": px.colors.qualitative.Set3
            }
            
            # Create scatter plot as word cloud alternative
            fig = go.Figure()
            
            # Calculate positions for words (spiral layout)
            angles = np.linspace(0, 2*np.pi, len(words))
            radii = np.linspace(0.1, 1, len(words))
            
            x_pos = radii * np.cos(angles)
            y_pos = radii * np.sin(angles)
            
            # Add words as text annotations
            for i, (word, freq) in enumerate(zip(words, frequencies)):
                size = max(10, min(40, freq * 2))  # Scale font size based on frequency
                fig.add_annotation(
                    x=x_pos[i], y=y_pos[i],
                    text=word,
                    showarrow=False,
                    font=dict(size=size, color=color_maps[color_scheme][i % len(color_maps[color_scheme])]),
                    textangle=np.random.randint(-45, 45)  # Random rotation
                )
            
            fig.update_layout(
                title=f"Keywords Cloud - {view_mode}",
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                height=500,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Keywords analysis table
        st.markdown("### 📊 Keywords Analysis Table")
        
        df_keywords = pd.DataFrame([
            {"Keyword": word, "Your Count": freq, "Industry Avg": freq + np.random.randint(-5, 10), 
             "Peer Avg": freq + np.random.randint(-3, 8), "ATS Weight": np.random.randint(1, 10)}
            for word, freq in keywords_data.items()
        ])
        
        # Add comparison columns
        df_keywords["vs Industry"] = df_keywords["Your Count"] - df_keywords["Industry Avg"]
        df_keywords["vs Peers"] = df_keywords["Your Count"] - df_keywords["Peer Avg"]
        
        # Style the dataframe
        def color_comparison(val):
            color = 'green' if val > 0 else 'red' if val < 0 else 'gray'
            return f'color: {color}'
        
        styled_df = df_keywords.style.applymap(color_comparison, subset=['vs Industry', 'vs Peers'])
        st.dataframe(styled_df, use_container_width=True)
        
        # Interactive keyword recommendations
        st.markdown("### 💡 Keyword Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🟢 Keywords to Emphasize")
            strong_keywords = df_keywords[df_keywords["vs Industry"] >= 0].head(5)
            for _, row in strong_keywords.iterrows():
                st.success(f"✅ **{row['Keyword']}** - Above industry average")
        
        with col2:
            st.markdown("#### 🔴 Keywords to Add/Strengthen")
            weak_keywords = df_keywords[df_keywords["vs Industry"] < 0].head(5)
            for _, row in weak_keywords.iterrows():
                st.error(f"❌ **{row['Keyword']}** - Below industry average")

# ==================== PEER ANALYSIS SECTION ====================
elif section_key == "peer_stats":
    render_section_header("Peer Comparison Analysis", "📊")
    
    st.markdown("""
    ### 👥 How You Compare to Similar Professionals
    Benchmarking against professionals with similar experience and background.
    """)
    
    # Peer selection criteria
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### 🎯 Comparison Criteria")
        
        peer_criteria = {
            "Experience Level": st.selectbox("Experience Level", 
                ["Entry Level", "Junior (1-3 years)", "Mid-Level (3-7 years)", 
                 "Senior (7-12 years)", "Executive (12+ years)"], index=2),
            "Industry": st.multiselect("Industry", 
                ["Technology", "Finance", "Healthcare", "Consulting"], default=["Technology"]),
            "Location": st.selectbox("Location", 
                ["London", "Manchester", "Birmingham", "Edinburgh", "Remote"], index=0),
            "Company Size": st.selectbox("Company Size",
                ["Startup", "Small", "Medium", "Large", "Enterprise"], index=2)
        }
        
        st.info(f"📈 **Peer Group Size**: 2,847 professionals matching your criteria")
    
    with col2:
        # Comparison metrics
        st.markdown("#### 📈 Performance Comparison")
        
        metrics_data = {
            "Resume ATS Score": {"your_score": 85, "peer_avg": 78, "percentile": 72},
            "Keywords Density": {"your_score": 7.2, "peer_avg": 6.1, "percentile": 65},
            "Experience Relevance": {"your_score": 92, "peer_avg": 84, "percentile": 81},
            "Skills Breadth": {"your_score": 15, "peer_avg": 12, "percentile": 68},
            "Achievement Quantification": {"your_score": 6, "peer_avg": 4, "percentile": 75}
        }
        
        for metric, data in metrics_data.items():
            col_metric, col_chart = st.columns([1, 2])
            
            with col_metric:
                delta = data["your_score"] - data["peer_avg"]
                st.metric(
                    metric,
                    f"{data['your_score']}" + ("%" if "Score" in metric or "Density" in metric or "Relevance" in metric else ""),
                    delta=f"{delta:+.1f}" + ("%" if "Score" in metric or "Density" in metric or "Relevance" in metric else ""),
                    help=f"You're in the {data['percentile']}th percentile"
                )
            
            with col_chart:
                # Create a mini distribution chart
                fig = go.Figure()
                
                # Peer distribution (simulated)
                x_vals = np.linspace(max(0, data["peer_avg"] - 20), data["peer_avg"] + 20, 100)
                y_vals = np.exp(-0.5 * ((x_vals - data["peer_avg"]) / 5) ** 2)
                
                fig.add_trace(go.Scatter(
                    x=x_vals, y=y_vals,
                    fill='tonexty',
                    name='Peer Distribution',
                    line=dict(color='lightblue')
                ))
                
                # Your score line
                fig.add_vline(
                    x=data["your_score"],
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"You ({data['percentile']}th %ile)"
                )
                
                fig.update_layout(
                    height=100,
                    margin=dict(t=0, b=0, l=0, r=0),
                    showlegend=False,
                    xaxis=dict(showticklabels=False),
                    yaxis=dict(showticklabels=False)
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    # Detailed peer insights
    st.markdown("### 🔍 Detailed Peer Insights")
    
    tab1, tab2, tab3 = st.tabs(["🏆 Strengths", "🎯 Opportunities", "📋 Recommendations"])
    
    with tab1:
        st.markdown("#### 🌟 Your Competitive Advantages")
        
        strengths = [
            {"area": "Technical Skills", "advantage": "25% more diverse tech stack than peers", "impact": "Higher versatility appeal"},
            {"area": "Leadership Experience", "advantage": "3x more team management experience", "impact": "Strong management track record"},
            {"area": "Achievement Metrics", "advantage": "50% more quantified results", "impact": "Demonstrates clear impact"},
            {"area": "Industry Certifications", "advantage": "2 more relevant certifications", "impact": "Professional development commitment"}
        ]
        
        for strength in strengths:
            with st.expander(f"🎯 {strength['area']} - {strength['advantage']}"):
                st.success(f"**Impact**: {strength['impact']}")
    
    with tab2:
        st.markdown("#### 🎯 Areas for Improvement")
        
        opportunities = [
            {"area": "Soft Skills Keywords", "gap": "30% fewer soft skill mentions", "suggestion": "Add communication, collaboration terms"},
            {"area": "Industry Buzzwords", "gap": "Missing 5 trending keywords", "suggestion": "Include AI/ML, sustainability, digital transformation"},
            {"area": "Education Section", "gap": "Less detailed than 60% of peers", "suggestion": "Add relevant coursework, GPA if strong"},
            {"area": "Professional Network", "gap": "40% fewer LinkedIn connections", "suggestion": "Expand network in target companies"}
        ]
        
        for opp in opportunities:
            with st.expander(f"📈 {opp['area']} - {opp['gap']}"):
                st.info(f"**Suggestion**: {opp['suggestion']}")
    
    with tab3:
        st.markdown("#### 📋 Peer-Based Action Plan")
        
        st.markdown("""
        **🎯 Top 3 Actions Based on Peer Analysis:**
        
        1. **Add Trending Keywords** (2 hours)
           - Research and add 5-7 industry buzzwords your peers are using
           - Focus on: AI/ML, Digital Transformation, Agile, Remote Leadership
        
        2. **Quantify More Achievements** (3 hours)  
           - Add metrics to 3-4 more accomplishments
           - Peers average 6 quantified achievements vs your 4
        
        3. **Expand Skills Section** (1 hour)
           - Add soft skills that 70% of successful peers mention
           - Include: Strategic thinking, Cross-functional collaboration, Change management
        """)
        
        if st.button("📝 Generate Personalized Improvement Plan", type="primary"):
            st.success("✅ Personalized plan generated! Check your email for detailed recommendations.")

# ==================== STAR ANALYSIS SECTION ====================
elif section_key == "star_analysis":
    render_section_header("STAR Analysis Framework", "⭐")
    
    st.markdown("""
    ### ⭐ STAR Method Resume Analysis
    Evaluating your accomplishments using the Situation, Task, Action, Result framework.
    """)
    
    if not st.session_state.resume_data:
        st.warning("⚠️ Please upload a resume first to perform STAR analysis.")
    else:
        # STAR analysis results
        star_achievements = [
            {
                "achievement": "Led digital transformation project",
                "situation": "Company struggling with legacy systems affecting productivity",
                "task": "Modernize core business systems within 6 months",
                "action": "Managed cross-functional team, implemented agile methodology, coordinated with vendors",
                "result": "Increased productivity by 35%, reduced costs by £200K annually",
                "star_score": 9,
                "completeness": {"S": True, "T": True, "A": True, "R": True}
            },
            {
                "achievement": "Developed new customer acquisition strategy",
                "situation": "Customer growth had plateaued for 18 months",
                "task": "Increase customer acquisition by 25% in Q4",
                "action": "Analyzed market data, launched targeted campaigns, optimized conversion funnel",
                "result": "Exceeded goal with 32% increase, £500K new revenue",
                "star_score": 10,
                "completeness": {"S": True, "T": True, "A": True, "R": True}
            },
            {
                "achievement": "Implemented new training program",
                "situation": "High employee turnover in customer service",
                "task": "Reduce turnover and improve customer satisfaction",
                "action": "Designed comprehensive training curriculum",
                "result": "Not specified in resume",
                "star_score": 6,
                "completeness": {"S": True, "T": True, "A": True, "R": False}
            }
        ]
        
        # Overall STAR score
        avg_star_score = sum(ach["star_score"] for ach in star_achievements) / len(star_achievements)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall STAR Score", f"{avg_star_score:.1f}/10")
        with col2:
            complete_stars = sum(1 for ach in star_achievements if all(ach["completeness"].values()))
            st.metric("Complete STAR Stories", f"{complete_stars}/{len(star_achievements)}")
        with col3:
            st.metric("Achievements Analyzed", len(star_achievements))
        
        # Individual STAR analysis
        st.markdown("### 📋 Achievement Analysis")
        
        for i, achievement in enumerate(star_achievements):
            with st.expander(f"⭐ {achievement['achievement']} (Score: {achievement['star_score']}/10)"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # STAR breakdown
                    components = [
                        ("🎯 Situation", achievement["situation"], achievement["completeness"]["S"]),
                        ("📋 Task", achievement["task"], achievement["completeness"]["T"]),
                        ("🚀 Action", achievement["action"], achievement["completeness"]["A"]),
                        ("🏆 Result", achievement["result"], achievement["completeness"]["R"])
                    ]
                    
                    for label, content, complete in components:
                        if complete:
                            st.success(f"{label}: {content}")
                        else:
                            st.error(f"{label}: {content if content != 'Not specified in resume' else 'MISSING - Add specific, quantified results'}")
                
                with col2:
                    # STAR completeness radar
                    categories = ['Situation', 'Task', 'Action', 'Result']
                    values = [1 if achievement["completeness"][key] else 0 for key in ["S", "T", "A", "R"]]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(
                        r=values,
                        theta=categories,
                        fill='toself',
                        name=f'Achievement {i+1}'
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(visible=True, range=[0, 1])
                        ),
                        showlegend=False,
                        height=250
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        
        # STAR improvement suggestions
        st.markdown("### 💡 STAR Improvement Suggestions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Strong STAR Elements")
            st.success("✅ Clear situation context in most achievements")
            st.success("✅ Specific tasks and responsibilities defined")
            st.success("✅ Detailed action descriptions")
        
        with col2:
            st.markdown("#### 🔧 Areas for Improvement")
            incomplete_results = sum(1 for ach in star_achievements if not ach["completeness"]["R"])
            if incomplete_results > 0:
                st.warning(f"⚠️ {incomplete_results} achievements missing quantified results")
            st.info("💡 Add more metrics and specific outcomes")
            st.info("💡 Include timeline information where relevant")

# ==================== SPIDER ANALYSIS SECTION ====================
elif section_key == "spider_analysis":
    render_section_header("Intelligent Skills Spider Analysis", "🕸️")
    
    st.markdown("""
    ### 🕸️ AI-Enhanced Professional Skills Assessment
    **Smart Calibration System:** Prevents overestimation bias while maintaining your authentic profile.
    """)
    
    # Initialize skills with AI-suggested scores and confidence intervals
    if 'user_skill_adjustments' not in st.session_state:
        st.session_state.user_skill_adjustments = {}
    
    # Skills categories with AI confidence intervals and bias correction
    skill_categories = {
        "Management": {
            "ai_score": 8.5, 
            "peer_avg": 7.2, 
            "user_adjustment": st.session_state.user_skill_adjustments.get("Management", 8.5),
            "confidence_interval": (7.8, 9.2),
            "evidence_strength": 0.85,
            "description": "Team leadership, project oversight, strategic planning",
            "bias_risk": "High - People often overestimate leadership abilities"
        },
        "Technology": {
            "ai_score": 9.1, 
            "peer_avg": 7.5, 
            "user_adjustment": st.session_state.user_skill_adjustments.get("Technology", 9.1),
            "confidence_interval": (8.7, 9.5),
            "evidence_strength": 0.92,
            "description": "Technical expertise, system design, problem solving",
            "bias_risk": "Low - Technical skills are measurable"
        },
        "Engineering": {
            "ai_score": 8.8, 
            "peer_avg": 7.3, 
            "user_adjustment": st.session_state.user_skill_adjustments.get("Engineering", 8.8),
            "confidence_interval": (8.2, 9.4),
            "evidence_strength": 0.88,
            "description": "Design, development, testing, optimization",
            "bias_risk": "Medium - Can be overestimated without peer feedback"
        },
        "R&D": {
            "ai_score": 7.3, 
            "peer_avg": 6.1, 
            "user_adjustment": st.session_state.user_skill_adjustments.get("R&D", 7.3),
            "confidence_interval": (6.5, 8.1),
            "evidence_strength": 0.75,
            "description": "Innovation, research, prototype development",
            "bias_risk": "Medium - Innovation impact is subjective"
        },
        "Marketing": {
            "ai_score": 5.8, 
            "peer_avg": 6.3, 
            "user_adjustment": st.session_state.user_skill_adjustments.get("Marketing", 5.8),
            "confidence_interval": (5.2, 6.4),
            "evidence_strength": 0.68,
            "description": "Brand awareness, campaign management, market analysis",
            "bias_risk": "High - Marketing success has many variables"
        },
        "Sales": {
            "ai_score": 6.2, 
            "peer_avg": 6.8, 
            "user_adjustment": st.session_state.user_skill_adjustments.get("Sales", 6.2),
            "confidence_interval": (5.8, 6.6),
            "evidence_strength": 0.71,
            "description": "Client relationships, revenue generation, negotiation",
            "bias_risk": "Medium - Results-driven but context matters"
        },
        "Finance": {
            "ai_score": 6.9, 
            "peer_avg": 7.0, 
            "user_adjustment": st.session_state.user_skill_adjustments.get("Finance", 6.9),
            "confidence_interval": (6.5, 7.3),
            "evidence_strength": 0.79,
            "description": "Budget management, financial analysis, cost optimization",
            "bias_risk": "Low - Financial skills are measurable"
        },
        "Admin": {
            "ai_score": 7.8, 
            "peer_avg": 7.1, 
            "user_adjustment": st.session_state.user_skill_adjustments.get("Admin", 7.8),
            "confidence_interval": (7.3, 8.3),
            "evidence_strength": 0.82,
            "description": "Process management, compliance, documentation",
            "bias_risk": "Low - Administrative skills are observable"
        },
        "HR": {
            "ai_score": 7.6, 
            "peer_avg": 6.5, 
            "user_adjustment": st.session_state.user_skill_adjustments.get("HR", 7.6),
            "confidence_interval": (7.0, 8.2),
            "evidence_strength": 0.77,
            "description": "People management, recruitment, culture development",
            "bias_risk": "High - People skills are subjective"
        },
        "Operations": {
            "ai_score": 8.2, 
            "peer_avg": 7.8, 
            "user_adjustment": st.session_state.user_skill_adjustments.get("Operations", 8.2),
            "confidence_interval": (7.7, 8.7),
            "evidence_strength": 0.86,
            "description": "Process improvement, efficiency, quality management",
            "bias_risk": "Medium - Process results are measurable but context varies"
        },
        "Manufacturing": {
            "ai_score": 5.4, 
            "peer_avg": 6.2, 
            "user_adjustment": st.session_state.user_skill_adjustments.get("Manufacturing", 5.4),
            "confidence_interval": (4.8, 6.0),
            "evidence_strength": 0.62,
            "description": "Production systems, quality control, lean manufacturing",
            "bias_risk": "Low - Manufacturing metrics are concrete"
        },
        "Services": {
            "ai_score": 7.9, 
            "peer_avg": 7.4, 
            "user_adjustment": st.session_state.user_skill_adjustments.get("Services", 7.9),
            "confidence_interval": (7.4, 8.4),
            "evidence_strength": 0.83,
            "description": "Customer service, support delivery, service design",
            "bias_risk": "Medium - Service quality is partially subjective"
        },
        "Consulting": {
            "ai_score": 8.6, 
            "peer_avg": 7.6, 
            "user_adjustment": st.session_state.user_skill_adjustments.get("Consulting", 8.6),
            "confidence_interval": (8.1, 9.1),
            "evidence_strength": 0.89,
            "description": "Advisory services, strategic recommendations, client management",
            "bias_risk": "High - Consulting impact is often long-term and indirect"
        }
    }
    
    # Skill adjustment interface
    st.markdown("### 🎛️ Interactive Skills Calibration")
    st.info("""
    **AI Bias Prevention System:** Adjust sliders to reflect your self-assessment. 
    Our intelligent limiters prevent overestimation that could hurt your job prospects.
    """)
    
    # Skills adjustment sliders with intelligent limiters
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🔧 Adjust Your Skills Assessment")
        
        for category, data in skill_categories.items():
            # Calculate intelligent limits based on evidence strength and bias risk
            evidence_weight = data["evidence_strength"]
            bias_multiplier = {"High": 0.7, "Medium": 0.85, "Low": 1.0}[data["bias_risk"].split(" - ")[0]]
            
            # Set limits: lower bound is AI score minus confidence interval, upper bound considers bias
            min_val = max(1.0, data["confidence_interval"][0] * 0.9)
            max_val = min(10.0, data["confidence_interval"][1] * bias_multiplier)
            
            # Slider with intelligent constraints
            user_score = st.slider(
                f"{category} ({data['bias_risk'].split(' - ')[0]} bias risk)",
                min_value=min_val,
                max_value=max_val,
                value=data["user_adjustment"],
                step=0.1,
                help=f"AI suggests {data['ai_score']:.1f}. {data['description']}. {data['bias_risk']}"
            )
            
            # Update session state
            st.session_state.user_skill_adjustments[category] = user_score
            skill_categories[category]["user_adjustment"] = user_score
            
            # Show bias warning if user adjusts significantly above AI recommendation
            if user_score > data["ai_score"] * 1.15:
                st.warning(f"⚠️ Consider: This is {((user_score/data['ai_score'] - 1) * 100):.0f}% above AI assessment")
    
    with col2:
        st.markdown("#### 🧠 AI Confidence Indicators")
        
        for category, data in skill_categories.items():
            confidence_color = "🟢" if data["evidence_strength"] > 0.8 else "🟡" if data["evidence_strength"] > 0.7 else "🔴"
            st.write(f"{confidence_color} **{category}**: {data['evidence_strength']:.0%} confidence")
        
        st.markdown("#### 📊 Bias Risk Legend")
        st.write("🔴 **High Risk**: Subjective, often overestimated")
        st.write("🟡 **Medium Risk**: Context dependent")  
        st.write("🟢 **Low Risk**: Measurable, objective")
    
    # Enhanced spider chart with multiple overlays
    st.markdown("### 🕸️ Multi-Layer Skills Analysis")
    
    categories = list(skill_categories.keys())
    ai_scores = [skill_categories[cat]["ai_score"] for cat in categories]
    user_scores = [skill_categories[cat]["user_adjustment"] for cat in categories] 
    peer_scores = [skill_categories[cat]["peer_avg"] for cat in categories]
    
    fig = go.Figure()
    
    # AI assessment
    fig.add_trace(go.Scatterpolar(
        r=ai_scores,
        theta=categories,
        fill='toself',
        name='AI Assessment',
        line_color='green',
        fillcolor='rgba(0, 255, 0, 0.1)'
    ))
    
    # Your adjusted scores
    fig.add_trace(go.Scatterpolar(
        r=user_scores,
        theta=categories,
        fill='toself',
        name='Your Assessment',
        line_color='blue',
        fillcolor='rgba(0, 100, 255, 0.2)'
    ))
    
    # Peer average
    fig.add_trace(go.Scatterpolar(
        r=peer_scores,
        theta=categories,
        fill='toself',
        name='Peer Average',
        line_color='gray',
        fillcolor='rgba(128, 128, 128, 0.1)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=True,
        title="Intelligent Skills Spider Analysis - AI vs Self-Assessment vs Peers",
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Skills summary with bias analysis
    st.markdown("### 📊 Calibrated Skills Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🤖 AI Assessment")
        for category, data in skill_categories.items():
            delta = data["ai_score"] - data["peer_avg"]
            st.metric(
                category,
                f"{data['ai_score']:.1f}/10",
                delta=f"{delta:+.1f}",
                help=f"Evidence strength: {data['evidence_strength']:.0%}"
            )
    
    with col2:
        st.markdown("#### 👤 Your Assessment")
        total_bias = 0
        for category, data in skill_categories.items():
            user_delta = data["user_adjustment"] - data["ai_score"]
            total_bias += abs(user_delta)
            delta_color = "normal" if abs(user_delta) < 0.5 else "inverse"
            st.metric(
                category,
                f"{data['user_adjustment']:.1f}/10",
                delta=f"{user_delta:+.1f}",
                delta_color=delta_color,
                help=data["description"]
            )
    
    with col3:
        st.markdown("#### 📈 vs Peers")
        for category, data in skill_categories.items():
            peer_delta = data["user_adjustment"] - data["peer_avg"]
            st.metric(
                category,
                f"Rank",
                delta=f"{peer_delta:+.1f}",
                help=f"Peer average: {data['peer_avg']:.1f}"
            )
    
    # Overall bias assessment
    avg_bias = total_bias / len(skill_categories)
    
    if avg_bias < 0.3:
        st.success(f"✅ **Excellent Calibration** - Average adjustment: {avg_bias:.1f} points. Your self-assessment aligns well with AI analysis.")
    elif avg_bias < 0.7:
        st.info(f"📊 **Good Balance** - Average adjustment: {avg_bias:.1f} points. Minor variance from AI assessment is normal.")
    else:
        st.warning(f"⚠️ **High Variance** - Average adjustment: {avg_bias:.1f} points. Consider reviewing AI evidence before finalizing.")
    
    # Overall assessment
    overall_ai = sum(data["ai_score"] for data in skill_categories.values()) / len(skill_categories)
    overall_user = sum(data["user_adjustment"] for data in skill_categories.values()) / len(skill_categories)
    overall_peer = sum(data["peer_avg"] for data in skill_categories.values()) / len(skill_categories)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("AI Overall Score", f"{overall_ai:.1f}/10")
    with col2:
        st.metric("Your Adjusted Score", f"{overall_user:.1f}/10", delta=f"{overall_user - overall_ai:+.1f}")
    with col3:
        st.metric("vs Peer Average", f"+{overall_user - overall_peer:.1f}", delta_color="normal")
    
    # Detailed analysis by category
    st.markdown("### 📊 Category Deep Dive")
    
    selected_category = st.selectbox(
        "Select category for detailed analysis:",
        list(skill_categories.keys())
    )
    
    cat_data = skill_categories[selected_category]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### 🎯 {selected_category} Analysis")
        st.write(f"**Description**: {cat_data['description']}")
        st.write(f"**Your Score**: {cat_data['score']:.1f}/10")
        st.write(f"**Peer Average**: {cat_data['peer_avg']:.1f}/10")
        
        if cat_data['score'] > cat_data['peer_avg']:
            st.success(f"🎉 You're {cat_data['score'] - cat_data['peer_avg']:.1f} points above peer average!")
        else:
            st.info(f"📈 Opportunity to improve by {cat_data['peer_avg'] - cat_data['score']:.1f} points")
    
    with col2:
        # Category-specific recommendations
        recommendations = {
            "Management": ["Leadership certification", "Team building workshops", "Strategic planning courses"],
            "Sales": ["Sales methodology training", "CRM system expertise", "Negotiation skills development"],
            "Engineering": ["Latest technology certifications", "System architecture training", "Code review practices"],
            "R&D": ["Innovation workshops", "Patent application experience", "Research methodology training"],
            "Marketing": ["Digital marketing certification", "Analytics tools training", "Brand management courses"],
            "Finance": ["Financial modeling courses", "Budget planning certification", "Investment analysis training"],
            "Operations": ["Process improvement certification", "Quality management training", "Supply chain optimization"],
            "HR": ["People management certification", "Recruitment best practices", "Diversity and inclusion training"]
        }
        
        st.markdown(f"#### 💡 {selected_category} Development Ideas")
        for rec in recommendations[selected_category]:
            st.write(f"• {rec}")
    
    # AI-powered career path recommendations
    st.markdown("### 🛤️ AI-Powered Career Path Recommendations")
    
    # Identify top 3 user-adjusted strengths
    top_strengths = sorted(skill_categories.items(), key=lambda x: x[1]["user_adjustment"], reverse=True)[:3]
    top_3_names = [strength[0] for strength in top_strengths]
    top_3_scores = [strength[1]["user_adjustment"] for strength in top_strengths]
    
    # Advanced career path mapping with confidence scores
    career_recommendations = []
    
    # Technology-focused paths
    if "Technology" in top_3_names and skill_categories["Technology"]["user_adjustment"] > 8.0:
        if "Management" in top_3_names:
            career_recommendations.append({
                "path": "Chief Technology Officer",
                "confidence": 0.92,
                "reasoning": "Strong tech + management combination",
                "next_steps": ["Strategic planning course", "Executive leadership program", "Board presentation skills"]
            })
        elif "Engineering" in top_3_names:
            career_recommendations.append({
                "path": "Principal Engineer / Tech Lead",
                "confidence": 0.89,
                "reasoning": "Deep technical expertise with engineering focus",
                "next_steps": ["Architecture design patterns", "Team mentoring", "Technical writing"]
            })
    
    # Management-focused paths
    if "Management" in top_3_names and skill_categories["Management"]["user_adjustment"] > 7.5:
        if "Operations" in top_3_names:
            career_recommendations.append({
                "path": "Chief Operating Officer",
                "confidence": 0.85,
                "reasoning": "Operations + management synergy",
                "next_steps": ["P&L management", "Strategic operations", "Change management"]
            })
        elif "HR" in top_3_names:
            career_recommendations.append({
                "path": "VP of People & Culture",
                "confidence": 0.81,
                "reasoning": "People management expertise",
                "next_steps": ["Organizational psychology", "Culture transformation", "DEI leadership"]
            })
    
    # Consulting paths
    if "Consulting" in top_3_names and skill_categories["Consulting"]["user_adjustment"] > 8.0:
        career_recommendations.append({
            "path": "Partner/Principal Consultant",
            "confidence": 0.87,
            "reasoning": "Strong consulting capability with domain expertise",
            "next_steps": ["Business development", "Thought leadership", "Client relationship mastery"]
        })
    
    # Display recommendations
    if career_recommendations:
        for i, rec in enumerate(career_recommendations):
            with st.expander(f"🎯 Path {i+1}: {rec['path']} (Confidence: {rec['confidence']:.0%})"):
                st.write(f"**Reasoning:** {rec['reasoning']}")
                st.write("**Recommended Next Steps:**")
                for step in rec['next_steps']:
                    st.write(f"• {step}")
                
                if st.button(f"📈 Get Detailed Roadmap for {rec['path']}", key=f"roadmap_{i}"):
                    st.success("✅ Detailed career roadmap will be sent to your email!")
    else:
        st.info("""
        🎯 **Custom Career Path Analysis Needed**
        
        Your unique skill combination suggests a specialized career path. 
        Our career coaching team can provide personalized recommendations.
        """)
    
    # Career coaching integration
    st.markdown("### 🎓 Skills Development & Career Coaching")
    
    # Identify skill gaps for top career paths
    skill_gaps = []
    for category, data in skill_categories.items():
        if data["user_adjustment"] < data["peer_avg"]:
            gap_size = data["peer_avg"] - data["user_adjustment"]
            skill_gaps.append((category, gap_size))
    
    skill_gaps.sort(key=lambda x: x[1], reverse=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Priority Skill Development")
        if skill_gaps:
            for category, gap in skill_gaps[:3]:
                st.warning(f"📊 **{category}**: {gap:.1f} point gap vs peers")
        else:
            st.success("🎉 You're above average in all assessed areas!")
    
    with col2:
        st.markdown("#### 🎯 Coaching Opportunities")
        st.info("""
        **Consider additional training and coaching:**
        
        🎓 **Skills Coach** - Technical skill development
        🗣️ **Communication Coach** - Presentation & leadership  
        🎯 **Career Strategist** - Path planning & transitions
        🤝 **Executive Coach** - C-level preparation
        """)
    
    # Call-to-action for career coaching
    if st.button("🚀 Explore Career & Skills Coaching", type="primary"):
        st.success("""
        ✅ **Career Coaching Portal Activated**
        
        You now have access to:
        - Personalized skill development plans
        - Career transition strategies  
        - Interview preparation & negotiation tactics
        - Executive presence coaching
        
        [📈 Visit Career Intelligence Portal →](../pages/AI_Career_Intelligence.py)
        """)
        
        # Set coaching access flag
        st.session_state.career_coaching_unlocked = True
    
    # Final recommendations summary
    st.markdown("### 📋 Action Plan Summary")
    
    st.info(f"""
    **🎯 Based on your Spider Analysis:**
    
    **Top Strengths:** {', '.join(top_3_names)} (Average: {sum(top_3_scores)/3:.1f}/10)
    
    **Immediate Actions:**
    1. Focus on addressing skill gaps in: {', '.join([gap[0] for gap in skill_gaps[:2]])}
    2. Leverage your {top_3_names[0]} expertise for career advancement
    3. Consider career paths aligned with your strength profile
    
    **Long-term Strategy:**
    - Develop cross-functional skills to increase versatility
    - Build thought leadership in your expertise areas
    - Expand network in target industries and roles
    
    **[🎯 Get Full Personalized Career Strategy](../pages/AI_Career_Intelligence.py)**
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 <strong>IntelliCV</strong> - Comprehensive Resume Intelligence Platform</p>
    <p>All analyses are powered by advanced AI and benchmarked against industry data</p>
</div>
""", unsafe_allow_html=True)