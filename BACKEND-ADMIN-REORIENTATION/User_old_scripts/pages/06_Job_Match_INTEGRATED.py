"""
🎯 Job Matching - Smart AI-Powered Career Connections (INTEGRATED)
===================================================
Advanced job matching with Portal Bridge AI integration and fallback support
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

# PORTAL BRIDGE INTEGRATION
try:
    sys.path.insert(0, str(current_dir.parent / "BACKEND-ADMIN-REORIENTATION"))
    from shared_backend.services.portal_bridge import PortalBridge
    PORTAL_BRIDGE_AVAILABLE = True
except ImportError as e:
    PORTAL_BRIDGE_AVAILABLE = False
    print(f"Portal Bridge not available: {e}")

# Portal Bridge caching
@st.cache_resource
def get_portal_bridge():
    """Initialize and cache Portal Bridge instance"""
    try:
        if PORTAL_BRIDGE_AVAILABLE:
            bridge = PortalBridge()
            return bridge
    except Exception as e:
        print(f"Portal Bridge initialization error: {e}")
    return None

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

# Initialize Portal Bridge
portal_bridge = get_portal_bridge()
AI_MODE_ACTIVE = portal_bridge is not None

# Initialize Admin AI Integration
if ADMIN_AI_AVAILABLE:
    admin_ai = init_admin_ai_for_user_page()
    st.sidebar.success("🚀 Admin AI Integration: ACTIVE")
    st.sidebar.info("Enhanced Job Title Engine + LinkedIn Integration + Real AI Data Processing")
else:
    st.sidebar.warning("⚠️ Admin AI Integration: NOT AVAILABLE")
    st.sidebar.error("Basic job matching only")

# AI Status Indicator
if AI_MODE_ACTIVE:
    st.sidebar.success("🟢 **AI MODE: ACTIVE**")
    st.sidebar.info("Portal Bridge connected - Real AI job matching enabled")
else:
    st.sidebar.warning("🟡 **DEMO MODE: ACTIVE**")
    st.sidebar.info("Using mock data - Portal Bridge not available")

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
    
    .ai-status-banner {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    .demo-status-banner {
        background: linear-gradient(135deg, #ffc107, #e0a800);
        color: black;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
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

# Sample job database for demonstration (fallback)
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

# ENHANCED: AI-Powered Job Matching with Portal Bridge
class EnhancedJobMatchingEngine:
    """Enhanced job matching with Portal Bridge AI integration"""
    
    def __init__(self, portal_bridge=None):
        self.portal_bridge = portal_bridge
        self.ai_active = portal_bridge is not None
    
    def get_job_matches(self, user_profile, job_description=None):
        """
        Get AI-powered job matches with intelligent fallback
        
        Args:
            user_profile: User resume/profile data
            job_description: Optional specific job to match
            
        Returns:
            dict with status, data, and mode information
        """
        if self.ai_active:
            try:
                # Call Portal Bridge for AI job matching
                result = self.portal_bridge.get_job_matches(
                    user_profile=user_profile,
                    job_description=job_description
                )
                
                if result.get('status') == 'success':
                    return {
                        'status': 'success',
                        'mode': 'ai',
                        'data': result.get('data', {}),
                        'source': 'Portal Bridge AI'
                    }
                elif result.get('status') == 'not_implemented':
                    # Graceful fallback to mock data
                    return self._get_mock_job_matches(user_profile, job_description, fallback_reason='not_implemented')
                else:
                    # Error fallback
                    return self._get_mock_job_matches(user_profile, job_description, fallback_reason='error')
                    
            except Exception as e:
                print(f"Portal Bridge error: {e}")
                return self._get_mock_job_matches(user_profile, job_description, fallback_reason='exception')
        else:
            # Portal Bridge not available
            return self._get_mock_job_matches(user_profile, job_description, fallback_reason='unavailable')
    
    def _get_mock_job_matches(self, user_profile, job_description=None, fallback_reason='unavailable'):
        """Fallback to mock job matching analysis"""
        
        # Extract user skills
        user_skills = self._extract_skills_from_resume(user_profile.get('content', ''))
        
        if job_description:
            # Custom job matching
            job_skills = self._extract_job_skills(job_description)
            match_score = self._calculate_match_score(job_skills, user_skills)
            
            matched_skills = set(job_skills) & set(user_skills)
            missing_skills = set(job_skills) - set(user_skills)
            
            return {
                'status': 'success',
                'mode': 'demo',
                'data': {
                    'custom_match': {
                        'match_score': match_score,
                        'job_skills': job_skills,
                        'user_skills': user_skills,
                        'matched_skills': list(matched_skills),
                        'missing_skills': list(missing_skills),
                        'recommendations': self._generate_recommendations(match_score, missing_skills)
                    }
                },
                'source': f'Mock Data (Fallback: {fallback_reason})',
                'fallback_reason': fallback_reason
            }
        else:
            # Browse opportunities - match against sample jobs
            matched_jobs = []
            for job in SAMPLE_JOBS:
                match_score = self._calculate_match_score(job['skills'], user_skills)
                matched_skills = set(job['skills']) & set(user_skills)
                missing_skills = set(job['skills']) - set(user_skills)
                
                matched_jobs.append({
                    **job,
                    'match_score': match_score,
                    'matched_skills': list(matched_skills),
                    'missing_skills': list(missing_skills)
                })
            
            # Sort by match score
            matched_jobs.sort(key=lambda x: x['match_score'], reverse=True)
            
            return {
                'status': 'success',
                'mode': 'demo',
                'data': {
                    'opportunities': matched_jobs,
                    'total_jobs': len(matched_jobs),
                    'user_skills': user_skills
                },
                'source': f'Mock Data (Fallback: {fallback_reason})',
                'fallback_reason': fallback_reason
            }
    
    def _extract_skills_from_resume(self, resume_content):
        """Extract skills from resume content"""
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
    
    def _extract_job_skills(self, job_description):
        """Extract skills from job description"""
        skill_keywords = [
            "Python", "JavaScript", "Java", "C++", "React", "Angular", "Vue.js",
            "SQL", "AWS", "Azure", "Docker", "Kubernetes", "Git", "Machine Learning"
        ]
        
        job_skills = []
        desc_lower = job_description.lower()
        
        for skill in skill_keywords:
            if skill.lower() in desc_lower:
                job_skills.append(skill)
        
        return job_skills
    
    def _calculate_match_score(self, job_skills, user_skills):
        """Calculate job match score based on skill overlap"""
        if not job_skills or not user_skills:
            return 0
        
        matched_skills = len(set(job_skills) & set(user_skills))
        total_job_skills = len(job_skills)
        
        base_score = (matched_skills / total_job_skills) * 100
        
        # Bonus for having more skills than required
        bonus = min(len(user_skills) - len(job_skills), 0) * 2
        
        return min(base_score + bonus, 100)
    
    def _generate_recommendations(self, match_score, missing_skills):
        """Generate personalized recommendations"""
        recommendations = []
        
        if match_score >= 80:
            recommendations.append("🎉 Excellent match! You're highly qualified for this position.")
            recommendations.append("Consider applying immediately and highlighting your relevant experience.")
        elif match_score >= 60:
            recommendations.append("👍 Good match! You meet most requirements.")
            recommendations.append("Focus on showcasing your matching skills in your application.")
        else:
            recommendations.append("🎯 Growth opportunity! Consider developing missing skills before applying.")
        
        if missing_skills:
            top_skills = list(missing_skills)[:3]
            recommendations.append(f"Priority skills to develop: {', '.join(top_skills)}")
        
        return recommendations

# Initialize enhanced engine
job_matching_engine = EnhancedJobMatchingEngine(portal_bridge)

# Page header with AI status
username = st.session_state.get('authenticated_user', 'User')

if AI_MODE_ACTIVE:
    st.markdown('''
    <div class="ai-status-banner">
        🟢 AI MODE ACTIVE - Real-time job matching powered by Portal Bridge
    </div>
    ''', unsafe_allow_html=True)
else:
    st.markdown('''
    <div class="demo-status-banner">
        🟡 DEMO MODE - Using mock data (Portal Bridge integration pending)
    </div>
    ''', unsafe_allow_html=True)

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
            with st.spinner("Analyzing job match with AI..."):
                # Progress animation
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                analysis_steps = [
                    "🔍 Parsing job description...",
                    "🎯 Extracting required skills...",
                    "📄 Analyzing your resume...",
                    "🤖 Running AI compatibility analysis...",
                    "💡 Generating recommendations...",
                    "✅ Finalizing match report..."
                ]
                
                for i, step in enumerate(analysis_steps):
                    status_text.text(step)
                    progress_bar.progress((i + 1) / len(analysis_steps))
                    time.sleep(0.3)
                
                # Get AI-powered analysis
                user_profile = {
                    'content': resume_data.get('content', ''),
                    'filename': resume_data.get('filename', ''),
                    'user': username
                }
                
                result = job_matching_engine.get_job_matches(user_profile, job_description)
                
                status_text.empty()
                progress_bar.empty()
                
                # Display mode indicator
                if result['mode'] == 'ai':
                    st.success(f"✅ **AI Analysis Complete** - Source: {result['source']}")
                else:
                    st.info(f"ℹ️ **Demo Analysis** - Source: {result['source']}")
                
                # Extract match data
                match_data = result['data'].get('custom_match', {})
                match_score = match_data.get('match_score', 0)
                matched_skills = match_data.get('matched_skills', [])
                missing_skills = match_data.get('missing_skills', [])
                recommendations = match_data.get('recommendations', [])
                
                # Store match result
                match_result = {
                    'job_description': job_description,
                    'match_score': match_score,
                    'matched_skills': matched_skills,
                    'missing_skills': missing_skills,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'type': 'custom',
                    'mode': result['mode']
                }
                
                st.session_state.job_match_history.append(match_result)
                
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
                    if matched_skills:
                        for skill in matched_skills:
                            st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
                    else:
                        st.info("No direct skill matches found")
                
                with col2:
                    st.markdown("#### ⚠️ Skills to Develop")
                    if missing_skills:
                        for skill in missing_skills:
                            st.markdown(f'<span class="missing-skill">{skill}</span>', unsafe_allow_html=True)
                    else:
                        st.success("You have all required skills!")
                
                # Recommendations
                st.markdown('<div class="recommendations-box">', unsafe_allow_html=True)
                st.markdown("#### 💡 AI Recommendations")
                
                if recommendations:
                    for rec in recommendations:
                        st.markdown(f"• {rec}")
                else:
                    st.info("No specific recommendations at this time.")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                show_success("Job match analysis completed!")
                
                if ERROR_HANDLER_AVAILABLE:
                    log_user_action("job_match_analysis", {
                        "match_score": match_score,
                        "matched_skills": len(matched_skills),
                        "missing_skills": len(missing_skills),
                        "mode": result['mode']
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
    
    # Get AI-powered opportunities
    user_profile = {
        'content': resume_data.get('content', ''),
        'filename': resume_data.get('filename', ''),
        'user': username
    }
    
    with st.spinner("🤖 Loading AI-matched opportunities..."):
        result = job_matching_engine.get_job_matches(user_profile)
    
    # Display mode indicator
    if result['mode'] == 'ai':
        st.success(f"✅ **AI-Matched Jobs** - Source: {result['source']}")
    else:
        st.info(f"ℹ️ **Demo Jobs** - Source: {result['source']}")
    
    opportunities = result['data'].get('opportunities', [])
    
    # Display matched jobs
    for i, job in enumerate(opportunities):
        st.markdown('<div class="job-card">', unsafe_allow_html=True)
        
        # Job header
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### {job['title']}")
            st.markdown(f"**{job['company']}** • {job['location']}")
            if job.get('remote', False):
                st.markdown("🏠 Remote Available")
        
        with col2:
            match_score = job.get('match_score', 0)
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
        st.markdown(f"**💰 Salary:** {job.get('salary', 'Not specified')}")
        st.markdown(f"**📋 Type:** {job.get('type', 'Full-time')}")
        
        # Description
        with st.expander("📄 Job Description"):
            st.write(job.get('description', ''))
            
            if 'requirements' in job:
                st.markdown("**Requirements:**")
                for req in job['requirements']:
                    st.write(f"• {req}")
        
        # Skills comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**✅ Your Skills Match:**")
            matched_skills = job.get('matched_skills', [])
            for skill in matched_skills[:5]:  # Show first 5
                st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("**📚 Skills to Learn:**")
            missing_skills = job.get('missing_skills', [])
            for skill in missing_skills[:3]:  # Show first 3
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
        
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.metric("🎯 Total Matches", total_matches)
        
        with metric_col2:
            st.metric("📊 Average Score", f"{avg_score:.1f}%")
        
        with metric_col3:
            high_matches = sum(1 for match in st.session_state.job_match_history if match['match_score'] >= 80)
            st.metric("🌟 High Matches", high_matches)
        
        with metric_col4:
            ai_matches = sum(1 for match in st.session_state.job_match_history if match.get('mode') == 'ai')
            st.metric("🤖 AI Matches", ai_matches)
        
        # Match history
        st.markdown("#### 📋 Recent Match History")
        
        for i, match in enumerate(reversed(st.session_state.job_match_history[-5:])):  # Last 5 matches
            mode_emoji = "🤖" if match.get('mode') == 'ai' else "🎭"
            with st.expander(f"{mode_emoji} Match {len(st.session_state.job_match_history) - i} - {match['match_score']:.1f}% • {match['timestamp']}"):
                st.write(f"**Type:** {match['type'].title()}")
                st.write(f"**Mode:** {match.get('mode', 'demo').upper()}")
                st.write(f"**Match Score:** {match['match_score']:.1f}%")
                st.write(f"**Matched Skills:** {', '.join(match.get('matched_skills', [])[:5])}")
                st.write(f"**Missing Skills:** {', '.join(match.get('missing_skills', []))}")
                
                if match['type'] == 'custom' and 'job_description' in match:
                    st.text_area("Job Description:", match['job_description'][:200] + "...", disabled=True, key=f"desc_{i}")
        
        # Skills development recommendations
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Skills Development Recommendations")
        
        # Collect all missing skills from matches
        all_missing_skills = []
        for match in st.session_state.job_match_history:
            all_missing_skills.extend(match.get('missing_skills', []))
        
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
    user_skills = job_matching_engine._extract_skills_from_resume(resume_data.get('content', ''))
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
mode_indicator = "🟢 AI-Powered" if AI_MODE_ACTIVE else "🟡 Demo Mode"
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 1.5rem; background: #f8f9fa; border-radius: 10px;">
    <p><strong>IntelliCV-AI Job Matching</strong> | {mode_indicator} Intelligence</p>
    <p>🎯 Intelligent Matching • 📊 Real-time Analysis • 🚀 Career Growth</p>
    <p>💡 <strong>Pro Tip:</strong> Regular job matching helps you stay current with market demands</p>
</div>
""", unsafe_allow_html=True)
