"""
🎯 Job Matching - Smart AI-Powered Career Connections
===================================================
Advanced job matching with resume analysis and compatibility scoring
"""

import streamlit as st
from pathlib import Path
import time
from datetime import datetime
import json
import re

# Setup paths and imports
current_dir = Path(__file__).parent.parent
import sys
sys.path.insert(0, str(current_dir))

# Import admin AI integration
try:
    from user_portal_admin_integration import process_user_action_with_admin_ai, init_admin_ai_for_user_page
    ADMIN_AI_AVAILABLE = True
except ImportError:
    ADMIN_AI_AVAILABLE = False

# Import utilities with fallbacks
try:
    from utils.error_handler import log_user_action, show_error, show_success, show_warning
    ERROR_HANDLER_AVAILABLE = True
except ImportError:
    ERROR_HANDLER_AVAILABLE = False
    def log_user_action(action, details=None): pass
    def show_error(msg): st.error(f"❌ {msg}")
    def show_success(msg): st.success(f"✅ {msg}")
    def show_warning(msg): st.warning(f"⚠️ {msg}")

# Page configuration
st.set_page_config(
    page_title="🎯 Job Matching | IntelliCV-AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication check
if not st.session_state.get('authenticated_user'):
    st.error("🔒 Please log in to access job matching")
    if st.button("🏠 Return to Home"):
        st.switch_page("pages/00_Home.py")
    st.stop()

# Initialize Admin AI Integration
if ADMIN_AI_AVAILABLE:
    admin_ai = init_admin_ai_for_user_page()
    st.sidebar.success("🚀 Admin AI Integration: ACTIVE")
    st.sidebar.info("Enhanced Job Title Engine + LinkedIn Integration + Real AI Data Processing")
else:
    st.sidebar.warning("⚠️ Admin AI Integration: NOT AVAILABLE")
    st.sidebar.error("Basic job matching only")

# Check resume upload
resume_data = st.session_state.get('resume_data', {})
if not resume_data.get('processed'):
    st.warning("📄 Please upload your resume first")
    if st.button("📤 Upload Resume"):
        st.switch_page("pages/05_Resume_Upload.py")
    st.stop()

# Professional CSS styling
def load_job_match_css():
    css = '''
    <style>
    .job-match-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    .input-section {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border-left: 5px solid #667eea;
    }
    
    .job-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
    }
    
    .job-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .match-score-excellent {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .match-score-good {
        background: linear-gradient(135deg, #007bff, #0056b3);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .match-score-fair {
        background: linear-gradient(135deg, #ffc107, #e0a800);
        color: black;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .skill-tag {
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    
    .missing-skill {
        background: #ffebee;
        color: #d32f2f;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    
    .analysis-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .comparison-table {
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .recommendations-box {
        background: linear-gradient(135deg, #e3f2fd, #f3e5f5);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #2196f3;
        margin: 1rem 0;
    }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

# Load CSS
load_job_match_css()

# Initialize job matching data
if 'job_matches' not in st.session_state:
    st.session_state.job_matches = []

if 'job_match_history' not in st.session_state:
    st.session_state.job_match_history = []

# Sample job database for demonstration
SAMPLE_JOBS = [
    {
        "title": "Senior Software Engineer",
        "company": "TechCorp Inc.",
        "location": "San Francisco, CA",
        "salary": "$120,000 - $160,000",
        "type": "Full-time",
        "remote": True,
        "description": "We are seeking a Senior Software Engineer to join our dynamic team. You will be responsible for developing scalable web applications, mentoring junior developers, and contributing to architectural decisions.",
        "requirements": [
            "5+ years of software development experience",
            "Proficiency in Python, JavaScript, and React",
            "Experience with cloud platforms (AWS, Azure)",
            "Strong problem-solving skills",
            "Bachelor's degree in Computer Science or related field"
        ],
        "skills": ["Python", "JavaScript", "React", "AWS", "Git", "Docker", "SQL", "REST APIs"]
    },
    {
        "title": "Data Scientist",
        "company": "DataCorp Analytics",
        "location": "New York, NY",
        "salary": "$100,000 - $140,000",
        "type": "Full-time",
        "remote": False,
        "description": "Join our data science team to build predictive models and extract insights from large datasets. You'll work on machine learning projects that drive business decisions.",
        "requirements": [
            "3+ years of data science experience",
            "Strong Python and R programming skills",
            "Experience with machine learning frameworks",
            "Statistical analysis expertise",
            "Master's degree preferred"
        ],
        "skills": ["Python", "R", "Machine Learning", "SQL", "Pandas", "Scikit-learn", "TensorFlow", "Statistics"]
    },
    {
        "title": "Frontend Developer",
        "company": "WebSolutions Ltd",
        "location": "Austin, TX",
        "salary": "$80,000 - $110,000",
        "type": "Full-time",
        "remote": True,
        "description": "We're looking for a creative Frontend Developer to build beautiful, responsive user interfaces. You'll work closely with designers and backend developers to create exceptional user experiences.",
        "requirements": [
            "3+ years of frontend development experience",
            "Expert-level JavaScript, HTML, CSS",
            "Experience with React or Vue.js",
            "Understanding of responsive design",
            "Portfolio of web applications"
        ],
        "skills": ["JavaScript", "HTML", "CSS", "React", "Vue.js", "Sass", "Webpack", "Git"]
    },
    {
        "title": "DevOps Engineer",
        "company": "CloudTech Systems",
        "location": "Seattle, WA",
        "salary": "$110,000 - $145,000",
        "type": "Full-time",
        "remote": True,
        "description": "Help us build and maintain our cloud infrastructure. You'll automate deployments, monitor systems, and ensure our applications scale efficiently.",
        "requirements": [
            "4+ years of DevOps experience",
            "Experience with Kubernetes and Docker",
            "Cloud platform expertise (AWS, GCP, Azure)",
            "Infrastructure as Code (Terraform, CloudFormation)",
            "CI/CD pipeline development"
        ],
        "skills": ["Kubernetes", "Docker", "AWS", "Terraform", "Jenkins", "Python", "Linux", "Git"]
    }
]

# Mock resume analysis for skill matching
def extract_skills_from_resume(resume_content):
    """Extract skills from resume content"""
    # Common technical skills to look for
    common_skills = [
        "Python", "JavaScript", "Java", "C++", "React", "Angular", "Vue.js",
        "Node.js", "HTML", "CSS", "SQL", "MongoDB", "PostgreSQL", "MySQL",
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Git", "Jenkins",
        "Machine Learning", "Data Science", "TensorFlow", "PyTorch",
        "REST APIs", "GraphQL", "Microservices", "Agile", "Scrum"
    ]
    
    found_skills = []
    content_lower = resume_content.lower()
    
    for skill in common_skills:
        if skill.lower() in content_lower:
            found_skills.append(skill)
    
    return found_skills

def calculate_match_score(job_skills, user_skills):
    """Calculate job match score based on skill overlap"""
    if not job_skills or not user_skills:
        return 0
    
    matched_skills = len(set(job_skills) & set(user_skills))
    total_job_skills = len(job_skills)
    
    base_score = (matched_skills / total_job_skills) * 100
    
    # Bonus for having more skills than required
    bonus = min(len(user_skills) - len(job_skills), 0) * 2
    
    return min(base_score + bonus, 100)

# Page header
username = st.session_state.get('authenticated_user', 'User')
st.markdown(f'''
<div class="job-match-header">
    <h1>🎯 AI-Powered Job Matching</h1>
    <p>Welcome, {username}! Find your perfect career match with intelligent analysis</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">Upload a job description or browse our curated opportunities</p>
</div>
''', unsafe_allow_html=True)

# Main matching interface
st.markdown("## 🔍 Find Your Perfect Match")

tab1, tab2, tab3 = st.tabs(["🎯 Custom Job Match", "💼 Browse Opportunities", "📊 Match Analysis"])

with tab1:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("### 📝 Enter Job Description")
    
    job_description = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="Copy and paste the complete job description you want to match against your resume...",
        help="Include job title, requirements, responsibilities, and desired skills for best matching results"
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("🚀 Analyze Match", type="primary", use_container_width=True) and job_description:
            with st.spinner("Analyzing job match..."):
                # Simulate AI analysis
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                analysis_steps = [
                    "Parsing job description...",
                    "Extracting required skills...",
                    "Analyzing your resume...",
                    "Calculating compatibility...",
                    "Generating recommendations...",
                    "Finalizing match report..."
                ]
                
                for i, step in enumerate(analysis_steps):
                    status_text.text(step)
                    progress_bar.progress((i + 1) / len(analysis_steps))
                    time.sleep(0.3)
                
                # Extract user skills from resume
                user_skills = extract_skills_from_resume(resume_data.get('content', ''))
                
                # Extract job skills (simple keyword matching)
                job_skills = []
                skill_keywords = ["Python", "JavaScript", "React", "SQL", "AWS", "Docker", "Git"]
                for skill in skill_keywords:
                    if skill.lower() in job_description.lower():
                        job_skills.append(skill)
                
                # Calculate match score
                match_score = calculate_match_score(job_skills, user_skills)
                
                # Store match result
                match_result = {
                    'job_description': job_description,
                    'job_skills': job_skills,
                    'user_skills': user_skills,
                    'match_score': match_score,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'type': 'custom'
                }
                
                st.session_state.job_match_history.append(match_result)
                
                status_text.empty()
                progress_bar.empty()
                
                # Display results
                st.markdown("### 🎯 Match Analysis Results")
                
                # Match score display
                if match_score >= 80:
                    score_class = "match-score-excellent"
                    score_emoji = "🎉"
                    score_text = "Excellent Match!"
                elif match_score >= 60:
                    score_class = "match-score-good"
                    score_emoji = "👍"
                    score_text = "Good Match!"
                else:
                    score_class = "match-score-fair"
                    score_emoji = "🤔"
                    score_text = "Fair Match"
                
                st.markdown(f'''
                <div style="text-align: center; margin: 2rem 0;">
                    <div class="{score_class}">
                        {score_emoji} {score_text} - {match_score:.1f}% Compatible
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Skills analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### ✅ Your Matching Skills")
                    matched_skills = set(job_skills) & set(user_skills)
                    if matched_skills:
                        for skill in matched_skills:
                            st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
                    else:
                        st.info("No direct skill matches found")
                
                with col2:
                    st.markdown("#### ⚠️ Skills to Develop")
                    missing_skills = set(job_skills) - set(user_skills)
                    if missing_skills:
                        for skill in missing_skills:
                            st.markdown(f'<span class="missing-skill">{skill}</span>', unsafe_allow_html=True)
                    else:
                        st.success("You have all required skills!")
                
                # Recommendations
                st.markdown('<div class="recommendations-box">', unsafe_allow_html=True)
                st.markdown("#### 💡 Recommendations")
                
                if match_score >= 80:
                    st.markdown("🎉 **Excellent match!** You're highly qualified for this position. Consider applying immediately.")
                elif match_score >= 60:
                    st.markdown("👍 **Good match!** You meet most requirements. Consider highlighting your relevant experience.")
                else:
                    st.markdown("🎯 **Growth opportunity!** Consider developing the missing skills before applying.")
                
                if missing_skills:
                    st.markdown(f"**Priority skills to develop:** {', '.join(list(missing_skills)[:3])}")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                show_success("Job match analysis completed!")
                
                if ERROR_HANDLER_AVAILABLE:
                    log_user_action("job_match_analysis", {
                        "match_score": match_score,
                        "matched_skills": len(matched_skills),
                        "missing_skills": len(missing_skills)
                    })
    
    with col2:
        st.markdown("**💡 Tips:**")
        st.markdown("""
        - Include full job posting
        - Copy all requirements
        - Include desired skills
        - Add company info
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### 💼 Curated Job Opportunities")
    st.info("🤖 These positions are automatically matched to your profile and skills")
    
    # Extract user skills for matching
    user_skills = extract_skills_from_resume(resume_data.get('content', ''))
    
    # Calculate matches for sample jobs
    for i, job in enumerate(SAMPLE_JOBS):
        match_score = calculate_match_score(job['skills'], user_skills)
        
        st.markdown('<div class="job-card">', unsafe_allow_html=True)
        
        # Job header
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### {job['title']}")
            st.markdown(f"**{job['company']}** • {job['location']}")
            if job['remote']:
                st.markdown("🏠 Remote Available")
        
        with col2:
            if match_score >= 80:
                score_class = "match-score-excellent"
                score_emoji = "🎉"
            elif match_score >= 60:
                score_class = "match-score-good"
                score_emoji = "👍"
            else:
                score_class = "match-score-fair"
                score_emoji = "🤔"
            
            st.markdown(f'''
            <div class="{score_class}" style="text-align: center;">
                {score_emoji} {match_score:.0f}% Match
            </div>
            ''', unsafe_allow_html=True)
        
        # Job details
        st.markdown(f"**💰 Salary:** {job['salary']}")
        st.markdown(f"**📋 Type:** {job['type']}")
        
        # Description
        with st.expander("📄 Job Description"):
            st.write(job['description'])
            
            st.markdown("**Requirements:**")
            for req in job['requirements']:
                st.write(f"• {req}")
        
        # Skills comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**✅ Your Skills Match:**")
            matched_skills = set(job['skills']) & set(user_skills)
            for skill in list(matched_skills)[:5]:  # Show first 5
                st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("**📚 Skills to Learn:**")
            missing_skills = set(job['skills']) - set(user_skills)
            for skill in list(missing_skills)[:3]:  # Show first 3
                st.markdown(f'<span class="missing-skill">{skill}</span>', unsafe_allow_html=True)
        
        # Action buttons
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button(f"📄 View Details", key=f"details_{i}"):
                st.info("Job details view coming soon!")
        
        with action_col2:
            if st.button(f"💾 Save Job", key=f"save_{i}"):
                show_success("Job saved to your favorites!")
        
        with action_col3:
            if st.button(f"🚀 Apply", key=f"apply_{i}"):
                st.info("External application link coming soon!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")

with tab3:
    st.markdown("### 📊 Your Match History & Analytics")
    
    if st.session_state.job_match_history:
        # Analytics overview
        total_matches = len(st.session_state.job_match_history)
        avg_score = sum(match['match_score'] for match in st.session_state.job_match_history) / total_matches
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric("🎯 Total Matches", total_matches)
        
        with metric_col2:
            st.metric("📊 Average Score", f"{avg_score:.1f}%")
        
        with metric_col3:
            high_matches = sum(1 for match in st.session_state.job_match_history if match['match_score'] >= 80)
            st.metric("🌟 High Matches", high_matches)
        
        # Match history
        st.markdown("#### 📋 Recent Match History")
        
        for i, match in enumerate(reversed(st.session_state.job_match_history[-5:])):  # Last 5 matches
            with st.expander(f"Match {len(st.session_state.job_match_history) - i} - {match['match_score']:.1f}% • {match['timestamp']}"):
                st.write(f"**Type:** {match['type'].title()}")
                st.write(f"**Match Score:** {match['match_score']:.1f}%")
                st.write(f"**Matched Skills:** {', '.join(match.get('user_skills', [])[:5])}")
                st.write(f"**Job Skills:** {', '.join(match.get('job_skills', []))}")
                
                if match['type'] == 'custom':
                    st.text_area("Job Description:", match['job_description'][:200] + "...", disabled=True)
        
        # Skills development recommendations
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Skills Development Recommendations")
        
        # Collect all missing skills from matches
        all_missing_skills = []
        for match in st.session_state.job_match_history:
            missing = set(match.get('job_skills', [])) - set(match.get('user_skills', []))
            all_missing_skills.extend(missing)
        
        # Count frequency of missing skills
        skill_frequency = {}
        for skill in all_missing_skills:
            skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
        
        # Show top missing skills
        if skill_frequency:
            sorted_skills = sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)
            st.markdown("**Most Requested Skills You Should Learn:**")
            
            for skill, count in sorted_skills[:5]:
                st.write(f"• **{skill}** - Appeared in {count} job{'s' if count > 1 else ''}")
        else:
            st.success("Great! You're well-matched for the positions you've analyzed.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.info("No match history yet. Try analyzing some job descriptions above!")

# Quick actions sidebar
st.sidebar.markdown("### 🚀 Quick Actions")

if st.sidebar.button("📤 Upload New Resume", use_container_width=True):
    st.switch_page("pages/05_Resume_Upload.py")

if st.sidebar.button("👤 Update Profile", use_container_width=True):
    st.switch_page("pages/02_Profile.py")

if st.sidebar.button("📊 View Dashboard", use_container_width=True):
    st.switch_page("pages/04_Dashboard.py")

# Resume status in sidebar
st.sidebar.markdown("### 📄 Resume Status")
if resume_data.get('filename'):
    st.sidebar.success(f"✅ {resume_data['filename']}")
    st.sidebar.write(f"Uploaded: {resume_data.get('upload_date', 'Unknown')}")
    
    # Show user skills
    user_skills = extract_skills_from_resume(resume_data.get('content', ''))
    if user_skills:
        st.sidebar.markdown("**Your Skills:**")
        for skill in user_skills[:5]:  # Show first 5
            st.sidebar.markdown(f"• {skill}")
        if len(user_skills) > 5:
            st.sidebar.markdown(f"• +{len(user_skills) - 5} more...")

# Career insights
st.sidebar.markdown("### 💡 Career Insights")
st.sidebar.info("""
**Tip of the Day:**
Companies value candidates who show continuous learning. Consider adding the top missing skills to your development plan!
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1.5rem; background: #f8f9fa; border-radius: 10px;">
    <p><strong>IntelliCV-AI Job Matching</strong> | AI-Powered Career Intelligence</p>
    <p>🎯 Intelligent Matching • 📊 Real-time Analysis • 🚀 Career Growth</p>
    <p>💡 <strong>Pro Tip:</strong> Regular job matching helps you stay current with market demands</p>
</div>
""", unsafe_allow_html=True)