"""
👤 IntelliCV-AI Profile Setup
============================
Step 3: Complete Your Profile
"""

import streamlit as st
from pathlib import Path
import sys
import time
from datetime import datetime

# Setup paths and imports
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

# Import utilities with fallbacks
try:
    from utils.error_handler import handle_exceptions, log_user_action, show_error, show_success
    ERROR_HANDLER_AVAILABLE = True
except ImportError:
    ERROR_HANDLER_AVAILABLE = False
    def handle_exceptions(func):
        return func
    def log_user_action(action, details=None):
        pass
    def show_error(msg, details=None):
        st.error(f"❌ {msg}")
    def show_success(msg, details=None):
        st.success(f"✅ {msg}")

# Page configuration
st.set_page_config(
    page_title="👤 Profile Setup | IntelliCV-AI",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Check if user is authenticated
if not st.session_state.get('authenticated_user'):
    st.error("❌ Please complete registration and payment first")
    if st.button("🔙 Go to Home"):
        st.switch_page("pages/00_Home.py")
    st.stop()

# Professional CSS styling
def load_profile_css():
    """Load profile setup page specific CSS"""
    css = '''
    <style>
    /* Clean background */
    .stApp {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
    }
    
    /* Main Container */
    .main .block-container {
        background: rgba(255,255,255,0.97) !important;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        margin-top: 1rem;
        backdrop-filter: blur(10px);
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Header styling */
    .profile-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    .profile-header h1 {
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Section cards */
    .profile-section {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    
    /* Progress bar */
    .progress-container {
        background: #f0f0f0;
        border-radius: 10px;
        height: 20px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #28a745, #20c997);
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Progress steps */
    .progress-steps {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }
    
    .step {
        padding: 0.5rem 1rem;
        margin: 0 0.5rem;
        background: #f8f9fa;
        border-radius: 20px;
        font-weight: 600;
    }
    
    .step.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .step.completed {
        background: #28a745;
        color: white;
    }
    
    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .section-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
    }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

# Load CSS
load_profile_css()

# Log page access
if ERROR_HANDLER_AVAILABLE:
    log_user_action("page_view", {"page": "profile_setup", "timestamp": datetime.now().isoformat()})

# Progress steps
st.markdown('''
<div class="progress-steps">
    <div class="step completed">1. Registration</div>
    <div class="step completed">2. Payment</div>
    <div class="step active">3. Profile Setup</div>
</div>
''', unsafe_allow_html=True)

# Header
username = st.session_state.get('authenticated_user', 'User')
plan = st.session_state.get('subscription_plan', 'free')
plan_names = {'free': 'Free Trial', 'monthly': 'Monthly Pro', 'annual': 'Annual Pro'}

st.markdown(f'''
<div class="profile-header">
    <h1>🎉 Welcome to IntelliCV-AI, {username}!</h1>
    <p>Complete your profile to get the most out of your {plan_names.get(plan, 'Free Trial')} experience</p>
</div>
''', unsafe_allow_html=True)

# Calculate completion percentage
profile_sections = ['personal', 'professional', 'contact', 'preferences', 'aspirational']
completed_sections = [s for s in profile_sections if st.session_state.get(f'profile_{s}_complete', False)]
completion_percentage = len(completed_sections) / len(profile_sections) * 100

# Progress bar
st.markdown(f"### 📊 Profile Completion: {completion_percentage:.0f}%")
st.markdown(f'''
<div class="progress-container">
    <div class="progress-bar" style="width: {completion_percentage}%"></div>
</div>
''', unsafe_allow_html=True)

# Sidebar with quick actions
with st.sidebar:
    st.markdown("### 🚀 Quick Actions")
    
    if completion_percentage >= 50:
        if st.button("📄 Upload Resume", use_container_width=True, type="primary"):
            st.switch_page("pages/01_Resume_Upload_and_Analysis.py")
    
    if completion_percentage >= 75:
        if st.button("🎯 Find Jobs", use_container_width=True):
            show_success("Job matching will be available after profile completion!")
    
    st.markdown("---")
    st.markdown("### 📋 Profile Sections")
    for i, section in enumerate(profile_sections):
        icon = "✅" if st.session_state.get(f'profile_{section}_complete', False) else "⏳"
        section_names = {
            'personal': 'Personal Info', 
            'professional': 'Professional', 
            'contact': 'Contact', 
            'preferences': 'Preferences',
            'aspirational': 'Career Aspirations'
        }
        st.markdown(f"{icon} {section_names.get(section, section.title())}")
    
    st.markdown("---")
    if st.button("🏠 Go to Dashboard", use_container_width=True):
        st.switch_page("pages/00_Home.py")

# Main content - Profile sections
col1, col2 = st.columns(2, gap="large")

with col1:
    # Personal Information Section
    st.markdown('<div class="profile-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><span class="section-icon">👤</span><span class="section-title">Personal Information</span></div>', unsafe_allow_html=True)
    
    with st.form("personal_info"):
        # Get existing registration data
        reg_data = st.session_state.get('registration_data', {})
        
        col_a, col_b = st.columns(2)
        with col_a:
            first_name = st.text_input("First Name", value=reg_data.get('first_name', ''))
            date_of_birth = st.date_input("Date of Birth", value=None)
            
        with col_b:
            last_name = st.text_input("Last Name", value=reg_data.get('last_name', ''))
            location = st.text_input("Location", placeholder="City, Country")
        
        phone = st.text_input("Phone Number", placeholder="+1 (555) 123-4567")
        bio = st.text_area("Professional Bio", placeholder="Brief description of your professional background...")
        
        if st.form_submit_button("💾 Save Personal Info", use_container_width=True):
            if first_name and last_name:
                st.session_state['profile_personal'] = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'date_of_birth': str(date_of_birth) if date_of_birth else '',
                    'location': location,
                    'phone': phone,
                    'bio': bio
                }
                st.session_state['profile_personal_complete'] = True
                show_success("✅ Personal information saved!")
                st.rerun()
            else:
                show_error("Please fill in required fields (First Name, Last Name)")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Professional Experience Section
    st.markdown('<div class="profile-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><span class="section-icon">💼</span><span class="section-title">Professional Experience</span></div>', unsafe_allow_html=True)
    
    with st.form("professional_info"):
        current_job_title = st.text_input("Current Job Title", placeholder="e.g., Software Engineer")
        current_company = st.text_input("Current Company", placeholder="e.g., Tech Corp")
        
        col_c, col_d = st.columns(2)
        with col_c:
            years_experience = st.selectbox("Years of Experience", [
                "0-1 years", "1-3 years", "3-5 years", "5-10 years", "10+ years"
            ])
            industry = st.selectbox("Industry", [
                "Technology", "Healthcare", "Finance", "Education", "Marketing", 
                "Sales", "Engineering", "Design", "Management", "Other"
            ], index=0 if not reg_data.get('industry') else ["Technology", "Healthcare", "Finance", "Education", "Marketing", "Sales", "Engineering", "Design", "Management", "Other"].index(reg_data.get('industry', 'Technology')))
        
        with col_d:
            salary_range = st.selectbox("Salary Range (USD)", [
                "Under $30k", "$30k-$50k", "$50k-$75k", "$75k-$100k", 
                "$100k-$150k", "$150k-$200k", "$200k+"
            ])
            employment_type = st.selectbox("Employment Type", [
                "Full-time", "Part-time", "Contract", "Freelance", "Seeking Employment"
            ])
        
        key_skills = st.text_area("Key Skills", placeholder="e.g., Python, Project Management, Data Analysis...")
        career_goals = st.text_area("Career Goals", placeholder="What are your professional aspirations?")
        
        if st.form_submit_button("💾 Save Professional Info", use_container_width=True):
            st.session_state['profile_professional'] = {
                'current_job_title': current_job_title,
                'current_company': current_company,
                'years_experience': years_experience,
                'industry': industry,
                'salary_range': salary_range,
                'employment_type': employment_type,
                'key_skills': key_skills,
                'career_goals': career_goals
            }
            st.session_state['profile_professional_complete'] = True
            show_success("✅ Professional information saved!")
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Contact & Social Section
    st.markdown('<div class="profile-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><span class="section-icon">📧</span><span class="section-title">Contact & Social</span></div>', unsafe_allow_html=True)
    
    with st.form("contact_info"):
        email = st.text_input("Email", value=reg_data.get('email', ''), disabled=True)
        linkedin_url = st.text_input("LinkedIn Profile", placeholder="https://linkedin.com/in/yourprofile")
        github_url = st.text_input("GitHub Profile", placeholder="https://github.com/yourusername")
        portfolio_url = st.text_input("Portfolio Website", placeholder="https://yourportfolio.com")
        
        # Communication preferences
        st.markdown("**Communication Preferences:**")
        col_e, col_f = st.columns(2)
        with col_e:
            email_notifications = st.checkbox("📧 Email Notifications", value=reg_data.get('notifications', False))
            job_alerts = st.checkbox("🔔 Job Alerts", value=True)
        
        with col_f:
            newsletter = st.checkbox("📰 Newsletter", value=reg_data.get('newsletter', False))
            marketing_emails = st.checkbox("📢 Marketing Updates")
        
        if st.form_submit_button("💾 Save Contact Info", use_container_width=True):
            st.session_state['profile_contact'] = {
                'email': email,
                'linkedin_url': linkedin_url,
                'github_url': github_url,
                'portfolio_url': portfolio_url,
                'email_notifications': email_notifications,
                'job_alerts': job_alerts,
                'newsletter': newsletter,
                'marketing_emails': marketing_emails
            }
            st.session_state['profile_contact_complete'] = True
            show_success("✅ Contact information saved!")
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Job Search Preferences Section
    st.markdown('<div class="profile-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><span class="section-icon">🎯</span><span class="section-title">Job Search Preferences</span></div>', unsafe_allow_html=True)
    
    with st.form("preferences_info"):
        job_types = st.multiselect("Preferred Job Types", [
            "Full-time", "Part-time", "Contract", "Freelance", "Internship", "Remote"
        ], default=["Full-time"])
        
        preferred_locations = st.text_input("Preferred Locations", placeholder="e.g., New York, Remote, San Francisco")
        
        col_g, col_h = st.columns(2)
        with col_g:
            min_salary = st.number_input("Minimum Salary (USD)", min_value=0, step=5000, value=50000)
            notice_period = st.selectbox("Notice Period", [
                "Immediate", "2 weeks", "1 month", "2 months", "3+ months"
            ])
        
        with col_h:
            remote_preference = st.selectbox("Remote Work", [
                "Remote only", "Hybrid preferred", "On-site preferred", "No preference"
            ])
            travel_willingness = st.selectbox("Travel Willingness", [
                "No travel", "Occasional travel", "Regular travel", "Extensive travel"
            ])
        
        job_interests = st.text_area("Areas of Interest", placeholder="What type of roles or industries interest you?")
        
        if st.form_submit_button("💾 Save Preferences", use_container_width=True):
            st.session_state['profile_preferences'] = {
                'job_types': job_types,
                'preferred_locations': preferred_locations,
                'min_salary': min_salary,
                'notice_period': notice_period,
                'remote_preference': remote_preference,
                'travel_willingness': travel_willingness,
                'job_interests': job_interests
            }
            st.session_state['profile_preferences_complete'] = True
            show_success("✅ Job preferences saved!")
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# NEW: Aspirational Career Section - Free-form AI context
st.markdown("---")
st.markdown('<div class="profile-section">', unsafe_allow_html=True)
st.markdown('<div class="section-header"><span class="section-icon">🚀</span><span class="section-title">Tell Us About Your Aspirations</span></div>', unsafe_allow_html=True)

st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
    <strong>💡 Help our AI understand you better!</strong><br>
    Share your career dreams, preferred lifestyle, and aspirations. The more context you provide, 
    the better our AI can match you with opportunities that align with YOUR unique goals.
</div>
""", unsafe_allow_html=True)

with st.form("aspirational_profile"):
    st.markdown("**🎯 Career Aspirations**")
    career_aspirations = st.text_area(
        "What roles are you aiming for?",
        placeholder="e.g., I want to become a Senior Software Engineer at a tech startup, leading a team of developers...",
        height=100,
        help="Be specific about job titles, seniority levels, and types of companies"
    )
    
    st.markdown("**🌍 Preferred Locations & Lifestyle**")
    location_aspirations = st.text_area(
        "Where do you want to live and work?",
        placeholder="e.g., I prefer working remotely from Austin, TX, but open to relocating to San Francisco for the right opportunity...",
        height=80,
        help="Include cities, countries, remote preferences, and lifestyle considerations"
    )
    
    st.markdown("**💼 Target Companies & Industries**")
    target_companies = st.text_area(
        "What types of companies interest you?",
        placeholder="e.g., Fast-growing SaaS startups, Fortune 500 tech companies, fintech innovators...",
        height=80,
        help="Describe company size, culture, industry, stage, or specific companies"
    )
    
    st.markdown("**🎨 Work Style & Environment**")
    work_style = st.text_area(
        "How do you like to work?",
        placeholder="e.g., I thrive in collaborative environments, prefer flexible hours, enjoy mentoring junior developers...",
        height=80,
        help="Share your preferred work culture, team dynamics, and work-life balance priorities"
    )
    
    st.markdown("**🎓 Growth & Development Goals**")
    growth_goals = st.text_area(
        "What skills or experiences are you seeking?",
        placeholder="e.g., I want to gain leadership experience, learn cloud architecture, work with cutting-edge AI/ML technologies...",
        height=80,
        help="Include skills you want to learn, certifications to earn, or experiences to gain"
    )
    
    st.markdown("**🌟 Unique Context**")
    unique_context = st.text_area(
        "Anything else that makes your career journey unique?",
        placeholder="e.g., Career changer from teaching, military veteran, returning to workforce after parenting, seeking visa sponsorship...",
        height=80,
        help="Share any unique circumstances, constraints, or opportunities that affect your job search"
    )
    
    if st.form_submit_button("💾 Save Aspirational Profile", use_container_width=True):
        aspirational_data = {
            'career_aspirations': career_aspirations,
            'location_aspirations': location_aspirations,
            'target_companies': target_companies,
            'work_style': work_style,
            'growth_goals': growth_goals,
            'unique_context': unique_context,
            'completed': bool(career_aspirations or location_aspirations),  # At least one field filled
            'last_updated': datetime.now().isoformat()
        }
        
        st.session_state['profile_aspirational'] = aspirational_data
        st.session_state['profile_aspirational_complete'] = bool(career_aspirations or location_aspirations)
        
        show_success("✅ Aspirational profile saved! Our AI will use this to find better matches for you.")
        
        # Log to admin AI for enrichment
        if ERROR_HANDLER_AVAILABLE:
            log_user_action("aspirational_profile_saved", {
                "username": username,
                "has_career_aspirations": bool(career_aspirations),
                "has_location_pref": bool(location_aspirations),
                "has_unique_context": bool(unique_context)
            })
        
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Interactive Chatbot Section
if not st.session_state.get('chatbot_completed', False):
    st.markdown("---")
    st.markdown('<div class="profile-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><span class="section-icon">🤖</span><span class="section-title">Quick Profile Builder (AI Assistant)</span></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #e8eaf6; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
        💬 <strong>Prefer a conversation?</strong> Our AI assistant can help you complete your profile 
        through a quick Q&A session instead of filling out forms.
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Start Quick Profile Builder", use_container_width=True, type="primary"):
        st.session_state['show_chatbot'] = True
    
    # Chatbot interface
    if st.session_state.get('show_chatbot', False):
        st.markdown("---")
        
        # Initialize chatbot session
        if 'chatbot_step' not in st.session_state:
            st.session_state['chatbot_step'] = 0
            st.session_state['chatbot_responses'] = {}
        
        chatbot_questions = [
            ("🎯 Career Aspirations", "What role are you aiming for in your career? (e.g., Senior Data Scientist, Product Manager)", "career_goal"),
            ("🌍 Location Preference", "Where would you like to work? (City, remote, flexible?)", "location_pref"),
            ("💼 Target Industry", "Which industries interest you most? (e.g., Tech, Healthcare, Finance)", "industry_pref"),
            ("🎨 Work Style", "How do you prefer to work? (e.g., Team-based, independent, fast-paced)", "work_style_pref"),
            ("⏰ Work-Life Balance", "What's important to you in work-life balance? (e.g., Flexible hours, remote work)", "work_life_pref")
        ]
        
        current_step = st.session_state['chatbot_step']
        
        if current_step < len(chatbot_questions):
            icon, question, key = chatbot_questions[current_step]
            
            st.markdown(f"### {icon} Question {current_step + 1}/{len(chatbot_questions)}")
            st.markdown(f"**{question}**")
            
            user_response = st.text_input("Your answer:", key=f"chatbot_q_{current_step}", 
                                         placeholder="Type your answer here...")
            
            col_prev, col_next, col_skip = st.columns([1, 1, 1])
            
            with col_prev:
                if current_step > 0:
                    if st.button("⬅️ Previous", use_container_width=True):
                        st.session_state['chatbot_step'] -= 1
                        st.rerun()
            
            with col_next:
                if st.button("Next ➡️", use_container_width=True, type="primary"):
                    if user_response:
                        st.session_state['chatbot_responses'][key] = user_response
                    st.session_state['chatbot_step'] += 1
                    st.rerun()
            
            with col_skip:
                if st.button("Skip ⏭️", use_container_width=True):
                    st.session_state['chatbot_step'] += 1
                    st.rerun()
        
        else:
            # Chatbot complete - save responses
            st.success("🎉 Quick profile builder complete!")
            st.markdown("**Here's what you told us:**")
            
            for key, value in st.session_state['chatbot_responses'].items():
                st.markdown(f"- **{key.replace('_', ' ').title()}:** {value}")
            
            if st.button("💾 Save Chatbot Responses", use_container_width=True, type="primary"):
                # Merge chatbot responses into aspirational profile
                existing_aspirational = st.session_state.get('profile_aspirational', {})
                existing_aspirational.update({
                    'chatbot_responses': st.session_state['chatbot_responses'],
                    'chatbot_completed': True,
                    'last_updated': datetime.now().isoformat()
                })
                st.session_state['profile_aspirational'] = existing_aspirational
                st.session_state['chatbot_completed'] = True
                st.session_state['show_chatbot'] = False
                
                show_success("✅ Chatbot responses saved to your profile!")
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Completion actions
if completion_percentage == 100:
    st.markdown("---")
    st.markdown("## 🎉 Profile Complete!")
    st.success("Congratulations! Your profile is 100% complete. You're ready to start using IntelliCV-AI!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Upload Your Resume", use_container_width=True, type="primary"):
            st.switch_page("pages/01_Resume_Upload_and_Analysis.py")
    
    with col2:
        if st.button("🎯 Find Matching Jobs", use_container_width=True):
            show_success("Job matching feature coming soon!")
    
    with col3:
        if st.button("🏠 Go to Dashboard", use_container_width=True):
            st.switch_page("pages/00_Home.py")
    
    # Log profile completion
    if ERROR_HANDLER_AVAILABLE:
        log_user_action("profile_completed", {
            "username": username,
            "completion_percentage": completion_percentage,
            "plan": plan
        })

elif completion_percentage >= 50:
    st.markdown("---")
    st.info(f"📊 Your profile is {completion_percentage:.0f}% complete. Complete remaining sections to unlock all features!")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>IntelliCV-AI</strong> | Profile Setup Complete</p>
    <p>👤 {username} • 📊 {completion_percentage:.0f}% Complete • 🎯 {plan_names.get(plan, 'Free Trial')}</p>
</div>
""", unsafe_allow_html=True)
