"""
🏠 User Dashboard - Your IntelliCV Command Center
===============================================
Post-login user dashboard with progress tracking and quick actions
"""

import streamlit as st
from pathlib import Path
import time
from datetime import datetime, timedelta
import json

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

# Import feature gating utilities
try:
    from utils.feature_gating import (
        check_feature_access,
        display_locked_feature_message,
        get_subscription_badge,
        get_usage_status,
        render_upgrade_prompt
    )
    FEATURE_GATING_AVAILABLE = True
except ImportError:
    FEATURE_GATING_AVAILABLE = False
    def check_feature_access(feature, plan=None): return True
    def display_locked_feature_message(feature, plan): st.warning(f"🔒 {feature} requires upgrade")
    def get_subscription_badge(plan=None): return ""
    def get_usage_status(limit_type, usage): return {'status': 'active', 'message': 'Active'}
    def render_upgrade_prompt(plan): pass

# Load logo with error handling
@st.cache_data
def load_logo_b64() -> str:
    """Load and cache logo with multiple fallback paths for 30% display"""
    try:
        import base64
        from pathlib import Path
        logo_paths = [
            Path(__file__).parent.parent / "static" / "logo.png",
            Path(__file__).parent.parent / "static" / "logo1.png",
            Path(__file__).parent.parent / "assets" / "logo.png",
            Path(__file__).parent / "static" / "logo.png"
        ]
        
        for logo_path in logo_paths:
            if logo_path.exists():
                return base64.b64encode(logo_path.read_bytes()).decode()
        
        return None
    except Exception as e:
        if ERROR_HANDLER_AVAILABLE:
            log_user_action("logo_load_error", {"error": str(e)})
        return None

def render_page_logo():
    """Render 30% logo for non-home pages"""
    logo_b64 = load_logo_b64()
    
    if logo_b64:
        st.markdown(f'''
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 1.5rem;">
            <img src="data:image/png;base64,{logo_b64}" 
                 alt="IntelliCV-AI Logo" 
                 style="width: 30%; max-width: 300px; height: auto; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));">
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 1.5rem;">
            <div style="font-size: 2.5rem; color: #667eea;">🚀</div>
            <h3 style="color: #667eea; margin: 0.5rem 0;">IntelliCV-AI</h3>
        </div>
        ''', unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="🏠 Dashboard | IntelliCV-AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication check
if not st.session_state.get('authenticated_user'):
    st.error("🔒 Please log in to access your dashboard")
    if st.button("🏠 Return to Home"):
        st.switch_page("pages/00_Home.py")
    st.stop()

# Initialize Admin AI Integration
if ADMIN_AI_AVAILABLE:
    admin_ai = init_admin_ai_for_user_page()
    st.sidebar.success("🚀 Admin AI Integration: ACTIVE")
    st.sidebar.info("Enhanced dashboard metrics with admin statistical tools and real-time data processing")
else:
    st.sidebar.warning("⚠️ Admin AI Integration: NOT AVAILABLE")
    st.sidebar.error("Basic dashboard metrics only")

# Professional CSS styling
def load_dashboard_css():
    css = '''
    <style>
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .quick-action-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border-top: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .quick-action-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .progress-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .recent-activity {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .status-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .status-complete { background: #d4edda; color: #155724; }
    .status-pending { background: #fff3cd; color: #856404; }
    .status-missing { background: #f8d7da; color: #721c24; }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

# Load CSS
load_dashboard_css()

# Render 30% logo
render_page_logo()

# Initialize user data
username = st.session_state.get('authenticated_user', 'User')
user_role = st.session_state.get('user_role', 'user')
login_time = st.session_state.get('login_time', datetime.now())

# Initialize session data if not exists
if 'profile_data' not in st.session_state:
    st.session_state.profile_data = {}
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = {}
if 'recent_activities' not in st.session_state:
    st.session_state.recent_activities = []

# Dashboard header with user welcome
current_time = datetime.now()
if current_time.hour < 12:
    greeting = "Good Morning"
elif current_time.hour < 17:
    greeting = "Good Afternoon"
else:
    greeting = "Good Evening"

# Get subscription badge
subscription_badge = get_subscription_badge() if FEATURE_GATING_AVAILABLE else ""

st.markdown(f'''
<div class="dashboard-header">
    <h1>🏠 {greeting}, {username}! {subscription_badge}</h1>
    <p>Welcome to your IntelliCV-AI Dashboard</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">Last login: {login_time.strftime("%B %d, %Y at %I:%M %p")}</p>
</div>
''', unsafe_allow_html=True)

# Calculate completion metrics
profile_data = st.session_state.profile_data
resume_data = st.session_state.resume_data

# Profile completion
required_profile_fields = ['full_name', 'email', 'phone', 'location', 'current_title', 'experience_level']
completed_profile_fields = sum(1 for field in required_profile_fields if profile_data.get(field))
profile_completion = (completed_profile_fields / len(required_profile_fields)) * 100

# Resume status
has_resume = bool(resume_data.get('content') or resume_data.get('filename'))
resume_upload_status = "✅ Uploaded" if has_resume else "❌ Not Uploaded"

# Job applications (simulated for now)
job_applications = st.session_state.get('job_applications', [])
total_applications = len(job_applications)

# Recent activity count
recent_activities = st.session_state.get('recent_activities', [])
activity_count = len(recent_activities)

# Admin AI Enhanced Metrics
dashboard_user_data = {
    'user_id': st.session_state.get('user_id', username),
    'profile_data': profile_data,
    'resume_data': resume_data,
    'profile_completion': profile_completion,
    'total_applications': total_applications,
    'activity_count': activity_count,
    'session_data': {
        'login_time': login_time.isoformat(),
        'user_role': user_role
    }
}

# Process dashboard metrics with admin AI
if ADMIN_AI_AVAILABLE and admin_ai.is_admin_ai_available():
    with st.spinner("🧠 Processing dashboard with admin AI systems..."):
        dashboard_result = process_user_action_with_admin_ai('dashboard_metrics', dashboard_user_data)
        enhanced_metrics = dashboard_result.get('enhanced_data', {})
else:
    enhanced_metrics = {}

# Metrics Dashboard
if ADMIN_AI_AVAILABLE and enhanced_metrics:
    st.markdown("## 📊 Your Progress Overview (Enhanced with Admin AI)")
else:
    st.markdown("## 📊 Your Progress Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="Profile Completion",
        value=f"{profile_completion:.0f}%",
        delta=f"{completed_profile_fields}/{len(required_profile_fields)} fields"
    )
    if profile_completion >= 80:
        st.markdown('<span class="status-badge status-complete">Complete</span>', unsafe_allow_html=True)
    elif profile_completion >= 50:
        st.markdown('<span class="status-badge status-pending">In Progress</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-missing">Needs Attention</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="Resume Status",
        value=resume_upload_status,
        delta="Ready for optimization" if has_resume else "Upload needed"
    )
    if has_resume:
        st.markdown('<span class="status-badge status-complete">Active</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-missing">Missing</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="Job Applications",
        value=total_applications,
        delta="Active applications"
    )
    if total_applications > 0:
        st.markdown('<span class="status-badge status-complete">Active</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-pending">Getting Started</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="Recent Activities",
        value=activity_count,
        delta="This week"
    )
    if activity_count > 5:
        st.markdown('<span class="status-badge status-complete">Very Active</span>', unsafe_allow_html=True)
    elif activity_count > 0:
        st.markdown('<span class="status-badge status-pending">Active</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-missing">New User</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Quick Actions Section
st.markdown("---")
st.markdown("## 🚀 Quick Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    st.markdown('<div class="quick-action-card">', unsafe_allow_html=True)
    st.markdown("### 👤 Profile Management")
    
    if profile_completion < 100:
        st.warning(f"Profile is {profile_completion:.0f}% complete")
        if st.button("✏️ Complete Profile", use_container_width=True, type="primary"):
            st.switch_page("pages/02_Profile.py")
    else:
        st.success("Profile is complete!")
        if st.button("✏️ Edit Profile", use_container_width=True):
            st.switch_page("pages/02_Profile.py")
    
    if st.button("📊 View Profile Summary", use_container_width=True):
        st.switch_page("pages/02_Profile.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

with action_col2:
    st.markdown('<div class="quick-action-card">', unsafe_allow_html=True)
    st.markdown("### 📄 Resume Center")
    
    if not has_resume:
        st.info("No resume uploaded yet")
        if st.button("📤 Upload Resume", use_container_width=True, type="primary"):
            try:
                st.switch_page("pages/05_Resume_Upload.py")
            except:
                show_error("Resume upload page not yet available")
    else:
        st.success("Resume is uploaded!")
        if st.button("🔍 Analyze Resume", use_container_width=True):
            try:
                st.switch_page("pages/01_Resume_Upload_and_Analysis.py")
            except:
                show_error("Resume analysis page not available")
    
    # Premium feature: Resume history tracking
    if FEATURE_GATING_AVAILABLE and check_feature_access('resume_upload_unlimited'):
        if st.button("📈 Resume History", use_container_width=True):
            st.info("Coming soon - Resume version tracking")
    else:
        st.button("📈 Resume History 🔒", disabled=True, use_container_width=True, 
                 help="Upgrade to Monthly Pro for resume version tracking")
    
    st.markdown('</div>', unsafe_allow_html=True)

with action_col3:
    st.markdown('<div class="quick-action-card">', unsafe_allow_html=True)
    st.markdown("### 💼 Job Search")
    
    if profile_completion >= 50 and has_resume:
        # Check advanced AI matching access
        has_advanced_matching = FEATURE_GATING_AVAILABLE and check_feature_access('advanced_ai_matching')
        button_label = "🎯 Find Job Matches" + (" (AI Enhanced)" if has_advanced_matching else "")
        
        if st.button(button_label, use_container_width=True, type="primary"):
            try:
                st.switch_page("pages/06_Job_Match.py")
            except:
                show_error("Job matching page not yet available")
        
        # Premium feature: Application tracking
        if FEATURE_GATING_AVAILABLE and check_feature_access('application_tracking'):
            if st.button("📝 Track Applications", use_container_width=True):
                st.info("Coming soon - Application tracking")
        else:
            st.button("📝 Track Applications 🔒", disabled=True, use_container_width=True,
                     help="Upgrade to Monthly Pro for application tracking")
    else:
        st.warning("Complete profile & upload resume first")
        st.button("🎯 Find Job Matches", disabled=True, use_container_width=True)
        st.button("📝 Track Applications", disabled=True, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Progress Section
st.markdown("---")
st.markdown("## 📈 Your Journey Progress")

progress_col1, progress_col2 = st.columns([2, 1])

with progress_col1:
    st.markdown('<div class="progress-section">', unsafe_allow_html=True)
    st.markdown("### 🛤️ Getting Started Checklist")
    
    checklist_items = [
        ("Create Account", True, "✅"),
        ("Complete Profile", profile_completion >= 80, "✅" if profile_completion >= 80 else "⏳"),
        ("Upload Resume", has_resume, "✅" if has_resume else "❌"),
        ("Find Job Matches", total_applications > 0, "✅" if total_applications > 0 else "🎯"),
        ("Submit Applications", total_applications > 0, "✅" if total_applications > 0 else "📝"),
        ("Track Progress", activity_count > 5, "✅" if activity_count > 5 else "📊")
    ]
    
    for item, completed, icon in checklist_items:
        status_class = "status-complete" if completed else "status-pending"
        st.markdown(f'{icon} **{item}** <span class="status-badge {status_class}">{"Done" if completed else "To Do"}</span>', 
                   unsafe_allow_html=True)
    
    # Overall progress bar
    completed_items = sum(1 for _, completed, _ in checklist_items if completed)
    overall_progress = (completed_items / len(checklist_items)) * 100
    
    st.progress(overall_progress / 100)
    st.caption(f"Overall Progress: {overall_progress:.0f}% ({completed_items}/{len(checklist_items)} steps)")
    
    st.markdown('</div>', unsafe_allow_html=True)

with progress_col2:
    st.markdown("### 🎯 Next Steps")
    
    # Personalized recommendations
    if profile_completion < 80:
        st.info("📝 Complete your profile to unlock job matching")
    elif not has_resume:
        st.info("📄 Upload your resume to start getting matches")
    elif total_applications == 0:
        st.success("🎯 You're ready! Start finding job matches")
    else:
        st.success("🚀 Keep tracking your applications and opportunities")
    
    # Quick stats
    st.markdown("### 📊 Quick Stats")
    days_since_login = (datetime.now() - login_time).days
    st.metric("Days Active", max(1, days_since_login))
    st.metric("Account Type", user_role.title())
    
    # Motivational message
    motivational_messages = [
        "🌟 Every expert was once a beginner!",
        "💪 Your dream job is one application away!",
        "🎯 Consistency is key to job search success!",
        "🚀 You're building momentum - keep going!",
        "✨ Great profiles attract great opportunities!"
    ]
    
    import random
    random.seed(hash(username))  # Consistent message per user
    daily_motivation = random.choice(motivational_messages)
    st.info(daily_motivation)

# Recent Activity Section (if any activities exist)
if recent_activities:
    st.markdown("---")
    st.markdown("## 📅 Recent Activity")
    
    for activity in recent_activities[-5:]:  # Show last 5 activities
        activity_time = activity.get('timestamp', datetime.now())
        activity_type = activity.get('type', 'general')
        activity_description = activity.get('description', 'Activity logged')
        
        st.markdown(f'''
        <div class="recent-activity">
            <strong>{activity_type.replace('_', ' ').title()}</strong><br>
            {activity_description}<br>
            <small style="color: #666;">{activity_time.strftime("%B %d, %Y at %I:%M %p")}</small>
        </div>
        ''', unsafe_allow_html=True)
    
    if len(recent_activities) > 5:
        st.info(f"And {len(recent_activities) - 5} more activities...")

# Footer with additional navigation
st.markdown("---")
st.markdown("## 🧭 Explore More Features")

footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)

with footer_col1:
    # Check if user has access to AI Career Coach
    has_career_coach_access = FEATURE_GATING_AVAILABLE and check_feature_access('career_insights')
    button_label = "🤖 AI Career Coach" + ("" if has_career_coach_access else " 🔒")
    
    if st.button(button_label, use_container_width=True, disabled=not has_career_coach_access,
                help="Upgrade to Monthly Pro" if not has_career_coach_access else None):
        try:
            st.switch_page("pages/07_AI_Interview_Coach.py")
        except:
            show_error("AI Coach not yet available")

with footer_col2:
    has_intelligence_access = FEATURE_GATING_AVAILABLE and check_feature_access('career_insights')
    button_label = "🧠 Career Intelligence" + ("" if has_intelligence_access else " 🔒")
    
    if st.button(button_label, use_container_width=True, disabled=not has_intelligence_access,
                help="Upgrade to Monthly Pro" if not has_intelligence_access else None):
        try:
            st.switch_page("pages/08_Career_Intelligence.py")
        except:
            show_error("Career Intelligence not yet available")

with footer_col3:
    has_mentorship_access = FEATURE_GATING_AVAILABLE and check_feature_access('mentorship_access')
    button_label = "👥 Mentorship Hub" + ("" if has_mentorship_access else " 🔒")
    
    if st.button(button_label, use_container_width=True, disabled=not has_mentorship_access,
                help="Upgrade to Super-User for mentorship access" if not has_mentorship_access else None):
        try:
            st.switch_page("pages/09_Mentorship_Hub.py")
        except:
            show_error("Mentorship Hub not yet available")

with footer_col4:
    has_advanced_tools_access = FEATURE_GATING_AVAILABLE and check_feature_access('advanced_analytics')
    button_label = "🔧 Advanced Tools" + ("" if has_advanced_tools_access else " 🔒")
    
    if st.button(button_label, use_container_width=True, disabled=not has_advanced_tools_access,
                help="Upgrade to Annual Pro for advanced tools" if not has_advanced_tools_access else None):
        try:
            st.switch_page("pages/10_Advanced_Career_Tools.py")
        except:
            show_error("Advanced Tools not yet available")

# Show upgrade prompt if user is on free plan
if FEATURE_GATING_AVAILABLE:
    user_plan = st.session_state.get('subscription_plan', 'free')
    if user_plan == 'free':
        render_upgrade_prompt(user_plan)

# Add activity log for page visit
if ERROR_HANDLER_AVAILABLE:
    log_user_action("dashboard_visit", {
        "profile_completion": profile_completion,
        "has_resume": has_resume,
        "total_applications": total_applications
    })

# Add this visit to recent activities
new_activity = {
    'timestamp': datetime.now(),
    'type': 'dashboard_visit',
    'description': 'Visited dashboard'
}

if 'recent_activities' not in st.session_state:
    st.session_state.recent_activities = []

st.session_state.recent_activities.append(new_activity)

# Keep only last 20 activities
if len(st.session_state.recent_activities) > 20:
    st.session_state.recent_activities = st.session_state.recent_activities[-20:]

# Final footer
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem; margin-top: 2rem; background: #f8f9fa; border-radius: 10px;">
    <p><strong>IntelliCV-AI Dashboard</strong> | Your Career Command Center</p>
    <p>🎯 Keep building your profile • 📄 Upload quality resumes • 💼 Apply strategically</p>
</div>
""", unsafe_allow_html=True)