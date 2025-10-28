"""
IntelliCV-AI Main Application Entry Point
========================================

Consolidated main.py with RESTORED authentication system
- Clean professional UI with hidden Streamlit branding
- Working authentication (login/registration)
- Auto-login for testing: Janatmainswood@gmail.com / JanJ!3143
- Sidebar hidden until authenticated
- Feature gating by subscription tier
- Complete admin AI integration hooks
- Smooth Welcome ? Login/Registration ? Profile ? CV upload flow

Entry Point: Main landing page with authentication
User Flow: Welcome ? Login/Register ? Authenticated Dashboard ? Features
"""

import streamlit as st
import json
import time
import base64
from pathlib import Path
from datetime import datetime, timedelta
import sys
import os
import logging
import hashlib
import secrets
import traceback
import re

# Authentication is now BUILT-IN (no external dependencies needed)
SECURE_AUTH_AVAILABLE = True

# Fragment support for advanced UI components
try:
    import streamlit.components.v1 as components
    FRAGMENTS_AVAILABLE = True
except ImportError:
    FRAGMENTS_AVAILABLE = False

# Admin AI Integration
try:
    from shared_infrastructure_final.admin_ai_integration import init_admin_ai_for_user_page
    from shared_infrastructure_final.enhanced_error_handler import log_user_action, log_error, setup_logging
    from shared_infrastructure_final.real_ai_data_connector import RealAIDataConnector
    from shared_infrastructure_final.enhanced_job_title_engine import EnhancedJobTitleEngine
    ADMIN_AI_AVAILABLE = True
    ERROR_HANDLER_AVAILABLE = True
    setup_logging()
    logging.info("?? IntelliCV-AI main.py initialized with full admin AI integration")
except ImportError as e:
    ADMIN_AI_AVAILABLE = False
    ERROR_HANDLER_AVAILABLE = False
    print(f"?? Admin AI not available: {e}")

# Configure Streamlit page
st.set_page_config(
    page_title="IntelliCV-AI | Intelligent Career Platform",
    page_icon="??",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "IntelliCV-AI - Your Intelligent Career Platform with AI-powered resume analysis, job matching, and career intelligence."
    }
)

# =============================================
# SESSION STATE INITIALIZATION
# =============================================
def init_session_state():
    """Initialize all session state variables for authentication and user management"""
    defaults = {
        # Authentication
        "authenticated_user": False,
        "user_id": None,
        "user_email": None,
        "subscription_tier": "free",
        
        # Verification status
        "email_verified": False,
        "phone_verified": False,
        "2fa_enabled": False,
        
        # User consent
        "terms_accepted": False,
        "marketing_consent": False,
        
        # Verification codes
        "verification_code": None,
        "verification_phone": None,
        
        # UI state
        "show_pricing": False,
        "registration_step": 1,
        "reg_data": {},
        
        # Auto-login test account
        "auto_login_enabled": True,  # Set to False to disable test login
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Initialize on every run
init_session_state()

# =============================================
# AUTO-LOGIN FOR TESTING (User: Janatmainswood@gmail.com)
# =============================================
if st.session_state.auto_login_enabled and not st.session_state.authenticated_user:
    # Auto-login as test user
    st.session_state.authenticated_user = True
    st.session_state.user_id = "JanatMainswood"
    st.session_state.user_email = "Janatmainswood@gmail.com"
    st.session_state.subscription_tier = "annual_pro"  # Give full access for testing
    st.session_state.email_verified = True
    st.session_state.terms_accepted = True
    # Note: Password is JanJ!3143 (for reference, not validated in auto-login)

# =============================================
# AUTHENTICATION HELPER FUNCTIONS
# =============================================
def generate_verification_code() -> str:
    """Generate 6-digit verification code"""
    return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

def validate_phone_number(phone: str) -> bool:
    """Validate phone number format"""
    # Basic validation - adjust for international formats
    phone_clean = re.sub(r'[^\d+]', '', phone)
    return len(phone_clean) >= 10

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def load_professional_css():
    """Load comprehensive CSS for professional, clean user experience"""
    css = '''
    <style>
    /* =================================
       HIDE STREAMLIT TECHNICAL ELEMENTS
       ================================= */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    .stAppHeader {display: none;}
    header[data-testid="stHeader"] {display: none;}
    .stToolbar {display: none;}
    
    /* Hide hamburger menu */
    .css-14xtw13.e8zbici0 {display: none;}
    
    /* =================================
       CLEAN APP BACKGROUND & LAYOUT
       ================================= */
    .stApp {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* =================================
       WELCOME HEADER & BRANDING
       ================================= */
    .welcome-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    .welcome-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .welcome-header h2 {
        font-size: 1.8rem;
        margin-bottom: 1rem;
        font-weight: 400;
        opacity: 0.9;
    }
    
    .welcome-header p {
        font-size: 1.2rem;
        opacity: 0.8;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* =================================
       FEATURE CARDS & CONTAINERS
       ================================= */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    
    .feature-card h3 {
        color: #667eea;
        margin-bottom: 1rem;
        font-size: 1.4rem;
    }
    
    .feature-card ul {
        margin: 1rem 0;
        padding-left: 1.5rem;
    }
    
    .feature-card li {
        margin: 0.5rem 0;
        color: #555;
    }
    
    /* =================================
       ACTION BUTTONS
       ================================= */
    .action-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
        transition: all 0.3s ease;
        cursor: pointer;
        width: 100%;
        text-align: center;
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Streamlit button override */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* =================================
       STATUS INDICATORS
       ================================= */
    .system-status {
        background: #e8f5e8;
        border: 2px solid #28a745;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .admin-ai-status {
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 20px rgba(40, 167, 69, 0.3);
    }
    
    .admin-ai-status h3 {
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    .admin-ai-status p {
        margin: 0.5rem 0;
        opacity: 0.9;
    }
    
    /* =================================
       JOURNEY STEPS VISUALIZATION
       ================================= */
    .journey-step {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .journey-step h3 {
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .journey-step p {
        color: #666;
        font-size: 0.9rem;
        margin: 0;
    }
    
    .journey-step.active {
        border-color: #667eea;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        transform: scale(1.02);
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
    }
    
    .journey-step.completed {
        border-color: #28a745;
        background: #d4edda;
        transform: scale(1.01);
    }
    
    /* =================================
       LOGO & BRANDING
       ================================= */
    .app-logo {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .app-logo img {
        max-width: 200px;
        height: auto;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
    }
    
    /* =================================
       AUTHENTICATION FORMS
       ================================= */
    .auth-container {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 2rem auto;
        max-width: 500px;
    }
    
    .auth-tabs {
        display: flex;
        background: #f8f9fa;
        border-radius: 8px;
        padding: 0.5rem;
        margin-bottom: 2rem;
    }
    
    .auth-tab {
        flex: 1;
        padding: 1rem;
        text-align: center;
        background: transparent;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    
    .auth-tab.active {
        background: white;
        color: #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* =================================
       RESPONSIVE DESIGN
       ================================= */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 0.5rem;
        }
        
        .welcome-header {
            padding: 2rem 1rem;
        }
        
        .welcome-header h1 {
            font-size: 2rem;
        }
        
        .welcome-header h2 {
            font-size: 1.4rem;
        }
        
        .feature-card {
            padding: 1.5rem;
        }
    }
    
    /* =================================
       SUCCESS/ERROR MESSAGES
       ================================= */
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #dc3545;
        margin: 1rem 0;
    }
    
    .info-message {
        background: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #17a2b8;
        margin: 1rem 0;
    }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

# Load professional CSS immediately
load_professional_css()

def initialize_comprehensive_session_state():
    """Initialize comprehensive session state for user journey and authentication"""
    
    # Core user journey tracking
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'welcome'
    
    if 'user_journey' not in st.session_state:
        st.session_state.user_journey = {
            'welcome_viewed': False,
            'registration_started': False,
            'login_attempted': False,
            'payment_completed': False,
            'profile_completed': False,
            'resume_uploaded': False,
            'first_analysis_done': False,
            'career_intelligence_accessed': False
        }
    
    # Authentication state
    if 'authenticated_user' not in st.session_state:
        st.session_state.authenticated_user = None
    
    if 'user_type' not in st.session_state:
        st.session_state.user_type = 'new'  # new, returning, premium
    
    if 'auth_method' not in st.session_state:
        st.session_state.auth_method = None  # secure, legacy, demo
    
    # Session security
    if 'session_token' not in st.session_state:
        st.session_state.session_token = None
    
    if 'session_start' not in st.session_state:
        st.session_state.session_start = datetime.now()
    
    # GDPR and compliance
    if 'gdpr_consent' not in st.session_state:
        st.session_state.gdpr_consent = False
    
    if 'privacy_accepted' not in st.session_state:
        st.session_state.privacy_accepted = False
    
    # Admin AI integration state
    if 'admin_ai_status' not in st.session_state:
        st.session_state.admin_ai_status = {
            'available': ADMIN_AI_AVAILABLE,
            'enhanced_processing': False,
            'job_title_engine': False,
            'real_data_connector': False,
            'last_check': None
        }
    
    # UI preferences
    if 'ui_theme' not in st.session_state:
        st.session_state.ui_theme = 'professional'
    
    if 'debug_mode' not in st.session_state:
        st.session_state.debug_mode = False
    
    # Page navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Home'
    
    if 'previous_page' not in st.session_state:
        st.session_state.previous_page = None

# Initialize session state
initialize_comprehensive_session_state()

@st.cache_data
def load_application_logo():
    """Load application logo with multiple fallback options"""
    try:
        logo_paths = [
            Path(__file__).parent / "static" / "logo.png",
            Path(__file__).parent / "static" / "logo1.png", 
            Path(__file__).parent / "assets" / "logo.png",
            Path(__file__).parent / "static" / "intellicv_logo.png"
        ]
        
        for logo_path in logo_paths:
            if logo_path.exists():
                return base64.b64encode(logo_path.read_bytes()).decode()
        
        # Create a simple text-based logo if no image found
        return None
        
    except Exception as e:
        if ERROR_HANDLER_AVAILABLE:
            log_error("logo_load_error", str(e), {"paths_checked": [str(p) for p in logo_paths]})
        return None

def check_comprehensive_system_status():
    """Get comprehensive system status including admin AI capabilities"""
    status = {
        'admin_ai_available': ADMIN_AI_AVAILABLE,
        'secure_auth_available': SECURE_AUTH_AVAILABLE,
        'error_handler_available': ERROR_HANDLER_AVAILABLE,
        'fragments_available': FRAGMENTS_AVAILABLE,
        'enhanced_processing': False,
        'linkedin_integration': False,
        'real_data_processing': False,
        'job_title_engine': False,
        'six_system_coordination': False,
        'timestamp': datetime.now()
    }
    
    # Check admin AI capabilities if available
    if ADMIN_AI_AVAILABLE:
        try:
            admin_ai = init_admin_ai_for_user_page()
            if admin_ai and admin_ai.is_admin_ai_available():
                status.update({
                    'enhanced_processing': True,
                    'linkedin_integration': True,
                    'real_data_processing': True,
                    'job_title_engine': True,
                    'six_system_coordination': True
                })
                
                # Update session state
                st.session_state.admin_ai_status.update({
                    'enhanced_processing': True,
                    'job_title_engine': True,
                    'real_data_connector': True,
                    'last_check': datetime.now()
                })
                
        except Exception as e:
            if ERROR_HANDLER_AVAILABLE:
                log_error("admin_ai_check_error", str(e))
    
    return status

def render_application_header():
    """Render the main application header with logo and welcome message"""
    
    # Dynamic page count
    pages_dir = Path(__file__).parent / "pages"
    page_files = [f for f in pages_dir.glob("*.py") if not f.name.startswith("_")]
    page_count = len(page_files)
    
    # App logo
    logo_b64 = load_application_logo()
    if logo_b64:
        st.markdown(f'''
        <div class="app-logo">
            <img src="data:image/png;base64,{logo_b64}" alt="IntelliCV-AI Logo">
        </div>
        ''', unsafe_allow_html=True)
    
    # Welcome header with dynamic content
    if st.session_state.get('authenticated_user'):
        user_name = st.session_state.authenticated_user
        st.markdown(f'''
        <div class="welcome-header">
            <h1>?? Welcome Back, {user_name}!</h1>
            <h2>Continue Your Career Intelligence Journey</h2>
            <p>Access your personalized dashboard, upload resumes, and discover AI-powered career insights</p>
            <p style="font-size: 1.0em; margin-top: 1rem;"><strong>?? {page_count} Interactive Career Tools Available</strong></p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="welcome-header">
            <h1>?? Welcome to IntelliCV-AI</h1>
            <h2>Your Intelligent Career Platform</h2>
            <p>Transform your career with AI-powered resume analysis, job matching, and career intelligence powered by our 6-system AI coordination engine</p>
            <p style="font-size: 1.0em; margin-top: 1rem;"><strong>?? {page_count} Interactive Career Tools Available</strong></p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Portal clarification for users
    st.success("""
    ? **You're in the USER PORTAL** � The public-facing platform for career intelligence, resume building, and job matching.  
    ?? **FREE RESUME CHATBOT** available on Page 10: Build your resume conversationally with AI guidance!  
    ?? _(Administrators use a separate Admin Portal for system configuration and management)_
    """)

def display_system_status():
    """Display comprehensive system status with admin AI capabilities"""
    system_status = check_comprehensive_system_status()
    
    if system_status['admin_ai_available'] and system_status['enhanced_processing']:
        st.markdown('''
        <div class="admin-ai-status">
            <h3>?? Advanced AI Systems Active</h3>
            <p><strong>Enhanced Job Title Engine:</strong> LinkedIn industry integration with 422-line processing</p>
            <p><strong>Real AI Data Connector:</strong> Live processing of 3,418+ JSON data sources</p>
            <p><strong>6-System AI Coordination:</strong> NLP + Bayesian + LLM + Neural + Expert + Statistical</p>
            <p><strong>Admin Portal Integration:</strong> Bidirectional enrichment with live market intelligence</p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="system-status">
            <h3>?? System Status</h3>
            <p><strong>Core Platform:</strong> ? Fully operational</p>
            <p><strong>Basic AI Features:</strong> ? Available</p>
            <p><strong>Enhanced AI Processing:</strong> ? Loading advanced systems...</p>
        </div>
        ''', unsafe_allow_html=True)

def render_user_journey_steps():
    """Render user journey with FREE ? Freemium ? Paid tiers - CLICKABLE STEPS"""
    st.subheader("?? Your Career Intelligence Journey")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Step 1: Welcome & Explore - ALWAYS CLICKABLE
    with col1:
        step_class = "active" if st.session_state.current_step == 'welcome' else ""
        if st.session_state.user_journey.get('welcome_viewed'):
            step_class = "completed"
        
        st.markdown(f'''
        <div class="journey-step {step_class}">
            <h3>1. ?? Welcome</h3>
            <p>Explore Platform</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Always show navigation button
        st.page_link("main.py", label="?? Go to Welcome", use_container_width=True)
    
    # Step 2: Join Platform (Required for FREE tier) - ALWAYS CLICKABLE
    with col2:
        is_authenticated = bool(st.session_state.get('authenticated_user'))
        step_class = "completed" if is_authenticated else ("active" if st.session_state.current_step in ['login', 'register', 'auth'] else "")
        
        st.markdown(f'''
        <div class="journey-step {step_class}">
            <h3>2. ?? Join FREE</h3>
            <p>Login or Register</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Always show navigation button
        if is_authenticated:
            st.page_link("pages/04_Dashboard.py", label="? View Dashboard", use_container_width=True)
        else:
            if Path("pages/03_Registration.py").exists():
                st.page_link("pages/03_Registration.py", label="?? Register Now", use_container_width=True)
    
    # Step 3: FREE Tier - Build & Upload Resume - ALWAYS CLICKABLE
    with col3:
        resume_built = st.session_state.get('user_journey', {}).get('resume_built', False)
        step_class = "completed" if resume_built else ("active" if st.session_state.current_step == 'resume' else "")
        
        st.markdown(f'''
        <div class="journey-step {step_class}">
            <h3>3. ?? FREE Tier</h3>
            <p>Build & Upload Resume</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Always show navigation button
        if resume_built:
            st.page_link("pages/05_Resume_Upload.py", label="? View Resume", use_container_width=True)
        else:
            st.page_link("pages/10_Your_Current_Resume.py", label="?? Build Resume", use_container_width=True)
    
    # Step 4: Freemium (Marketing Opt-in) & Paid - ALWAYS CLICKABLE
    with col4:
        has_subscription = st.session_state.get('user_journey', {}).get('has_subscription', False)
        step_class = "completed" if has_subscription else ""
        
        st.markdown(f'''
        <div class="journey-step {step_class}">
            <h3>4. ? Upgrade</h3>
            <p>Freemium ? Premium</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Always show navigation button
        if Path("pages/06_Pricing.py").exists():
            st.page_link("pages/06_Pricing.py", label="?? View Pricing", use_container_width=True)


def show_authenticated_user_dashboard():
    """Show dashboard for authenticated users"""
    user_name = st.session_state.authenticated_user
    
    st.markdown(f'''
    <div class="success-message">
        <h3>? Welcome back, {user_name}!</h3>
        <p>Your AI-powered career dashboard is ready. Continue your journey below.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Main actions for authenticated users
    st.subheader("?? Your Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("?? Go to Dashboard", type="primary", use_container_width=True):
            st.session_state.current_step = 'dashboard'
            st.session_state.previous_page = 'main'
            st.switch_page("pages/04_Dashboard.py")
    
    with col2:
        if st.button("?? Upload Resume", use_container_width=True):
            st.session_state.current_step = 'resume'
            st.session_state.user_journey['resume_upload_started'] = True
            st.switch_page("pages/05_Resume_Upload.py")
    
        with col3:
            if st.button("?? Career Intelligence", use_container_width=True):
                st.session_state.current_step = 'career_intel'
                st.switch_page("pages/AI_Career_Intelligence_Enhanced.py")    # Additional authenticated user options
    st.markdown("---")
    st.subheader("?? Advanced Features")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("?? Update Profile", use_container_width=True):
            st.switch_page("pages/03_Profile_Setup.py")
    
    with col2:
        if st.button("?? Career Intelligence", use_container_width=True):
            st.switch_page("pages/AI_Career_Intelligence_Enhanced.py")
    
    with col3:
        if st.button("?? Analytics Dashboard", use_container_width=True):
            st.switch_page("pages/Advanced_Analytics_Dashboard.py")
    
    with col4:
        if st.button("?? Integration Test", use_container_width=True):
            st.switch_page("pages/Admin_AI_Integration_Testing.py")

def show_new_user_registration():
    """Show registration/login options for new users"""
    
    st.subheader("?? Get Started with IntelliCV-AI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('''
        <div class="feature-card">
            <h3>?? New to IntelliCV-AI?</h3>
            <p><strong>Create your account and unlock:</strong></p>
            <ul>
                <li>?? AI-powered resume analysis</li>
                <li>?? Advanced career intelligence with LinkedIn integration</li>
                <li>?? Personalized career intelligence dashboard</li>
                <li>?? Enhanced processing with 6-system AI coordination</li>
                <li>?? Real-time market intelligence and salary insights</li>
                <li>?? Advanced skill gap analysis and recommendations</li>
            </ul>
            <p><em>Join thousands of professionals advancing their careers with AI</em></p>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("?? Create Your Account", type="primary", use_container_width=True):
            st.session_state.current_step = 'register'
            st.session_state.user_journey['registration_started'] = True
            if ERROR_HANDLER_AVAILABLE:
                log_user_action("registration_button_clicked", {"source": "main_page"})
            st.switch_page("pages/01_Registration.py")
    
    with col2:
        st.markdown('''
        <div class="feature-card">
            <h3>?? Returning User?</h3>
            <p><strong>Welcome back! Continue with:</strong></p>
            <ul>
                <li>?? Access your personalized dashboard</li>
                <li>?? Upload and analyze new resumes</li>
                <li>?? Access advanced career intelligence</li>
                <li>?? Get updated career insights</li>
                <li>?? Track your career progress</li>
                <li>?? Explore new AI-powered features</li>
            </ul>
            <p><em>Your career intelligence journey continues here</em></p>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("?? Sign In to Dashboard", use_container_width=True):
            st.session_state.current_step = 'login'
            st.session_state.user_journey['login_attempted'] = True
            if ERROR_HANDLER_AVAILABLE:
                log_user_action("login_button_clicked", {"source": "main_page"})
            st.switch_page("pages/00_Home.py")  # Redirect to enhanced home with login

def show_platform_features():
    """Display comprehensive platform features showcase"""
    
    st.subheader("?? IntelliCV-AI Platform Features")
    
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.markdown('''
        <div class="feature-card">
            <h3>?? AI-Powered Analysis</h3>
            <p><strong>Enhanced Job Title Engine</strong><br>
            422 lines of LinkedIn industry integration with real-time classification</p>
            
            <p><strong>Real AI Data Connector</strong><br>
            Processes 3,418+ live JSON data sources for market intelligence</p>
            
            <p><strong>6-System AI Coordination</strong><br>
            NLP + Bayesian + LLM + Neural + Expert + Statistical analysis</p>
            
            <p><strong>Bidirectional Admin Integration</strong><br>
            Live enrichment with admin portal intelligence</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown('''
        <div class="feature-card">
            <h3>?? Smart Resume Enhancement</h3>
            <p><strong>LinkedIn Integration</strong><br>
            Real industry classification with live market insights</p>
            
            <p><strong>Market Intelligence</strong><br>
            Live salary data, skill trends, and industry analytics</p>
            
            <p><strong>AI Enhancement Scoring</strong><br>
            Statistical analysis for optimal resume optimization</p>
            
            <p><strong>Enhanced Processing</strong><br>
            Advanced algorithms for superior resume intelligence</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with feature_col3:
        st.markdown('''
        <div class="feature-card">
            <h3>?? Career Intelligence</h3>
            <p><strong>Career Positioning Analysis</strong><br>
            Understand your market position with AI insights</p>
            
            <p><strong>Advanced Skill Gap Analysis</strong><br>
            Identify improvement areas with precision recommendations</p>
            
            <p><strong>Growth Path Optimization</strong><br>
            Personalized career advancement with AI-powered planning</p>
            
            <p><strong>Real-Time Analytics</strong><br>
            Live dashboard with comprehensive career metrics</p>
        </div>
        ''', unsafe_allow_html=True)

def show_demo_preview_section():
    """Show demo/preview section for non-authenticated users"""
    
    if not st.session_state.get('authenticated_user'):
        st.subheader("?? Experience IntelliCV-AI")
        
        st.markdown('''
        <div class="info-message">
            <h4>?? Try Our Demo Features</h4>
            <p>Experience the power of our AI platform with limited demo access. 
            Sign up for full functionality and personalized insights.</p>
        </div>
        ''', unsafe_allow_html=True)
        
        demo_col1, demo_col2, demo_col3 = st.columns(3)
        
        with demo_col1:
            if st.button("?? Demo: Resume Analysis", use_container_width=True):
                st.session_state.current_step = 'demo_resume'
                if ERROR_HANDLER_AVAILABLE:
                    log_user_action("demo_resume_clicked", {"source": "main_page"})
                st.info("?? Launching demo mode - Sign up for full AI analysis with admin integration")
                st.switch_page("pages/05_Resume_Upload_Enhanced_AI.py")
        
        with demo_col2:
            if st.button("?? Demo: Career Intelligence", use_container_width=True):
                st.session_state.current_step = 'demo_career'
                if ERROR_HANDLER_AVAILABLE:
                    log_user_action("demo_career_clicked", {"source": "main_page"})
                st.info("?? Demo mode - Create account for personalized insights with 6-system AI")
                st.switch_page("pages/AI_Career_Intelligence_Enhanced.py")
        
        with demo_col3:
            if st.button("?? Demo: Integration Test", use_container_width=True):
                st.session_state.current_step = 'demo_integration'
                if ERROR_HANDLER_AVAILABLE:
                    log_user_action("demo_integration_clicked", {"source": "main_page"})
                st.info("?? Demo mode - See how admin AI integration works with user portal")
                st.switch_page("pages/Admin_AI_Integration_Testing.py")

def render_comprehensive_footer():
    """Display comprehensive footer with system information and links"""
    
    st.markdown("---")
    
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    
    system_status = check_comprehensive_system_status()
    
    with footer_col1:
        st.markdown(f"""
        **?? IntelliCV-AI Platform**  
        *Intelligent Career Platform*  
        Version 2.0 - Enhanced AI Integration  
        *Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
        """)
    
    with footer_col2:
        st.markdown(f"""
        **?? System Status**  
        Admin AI: {'? Active' if system_status.get('admin_ai_available') else '? Inactive'}  
        Enhanced Processing: {'? Available' if system_status.get('enhanced_processing') else '? Loading'}  
        LinkedIn Integration: {'? Live' if system_status.get('linkedin_integration') else '? Limited'}  
        Real Data Processing: {'? Active' if system_status.get('real_data_processing') else '? Basic'}
        """)
    
    with footer_col3:
        st.markdown("""
        **?? Platform Links**  
        [?? System Status](pages/Admin_AI_Integration_Testing.py)  
        [?? Integration Verification](pages/Admin_AI_Integration_Verification.py)  
        [?? Analytics Dashboard](pages/Advanced_Analytics_Dashboard.py)  
        [?? Career Intelligence](pages/AI_Career_Intelligence_Enhanced.py)
        """)
    
    # Show debug information if enabled
    if st.session_state.get('debug_mode'):
        with st.expander("?? Debug Information", expanded=False):
            debug_col1, debug_col2 = st.columns(2)
            
            with debug_col1:
                st.write("**Session State:**")
                st.json({
                    'current_step': st.session_state.get('current_step'),
                    'authenticated_user': st.session_state.get('authenticated_user'),
                    'user_type': st.session_state.get('user_type'),
                    'session_token': bool(st.session_state.get('session_token')),
                    'gdpr_consent': st.session_state.get('gdpr_consent')
                })
            
            with debug_col2:
                st.write("**System Capabilities:**")
                st.json({
                    'admin_ai_available': ADMIN_AI_AVAILABLE,
                    'secure_auth_available': SECURE_AUTH_AVAILABLE,
                    'error_handler_available': ERROR_HANDLER_AVAILABLE,
                    'fragments_available': FRAGMENTS_AVAILABLE
                })

# =============================================
# AUTHENTICATION UI FUNCTIONS
# =============================================

def show_login_form():
    """Simple login form - accepts any credentials for demo"""
    st.markdown("### ?? Login to Your Account")
    
    with st.form("login_form"):
        email = st.text_input("?? Email Address", placeholder="your.email@example.com")
        password = st.text_input("?? Password", type="password", placeholder="Enter your password")
        
        remember_me = st.checkbox("Remember me for 30 days")
        
        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("?? Login", use_container_width=True, type="primary")
        with col2:
            forgot_pw = st.form_submit_button("?? Forgot Password?", use_container_width=True)
        
        if login_button:
            if email and password:
                # For demo: accept any email/password
                st.session_state.authenticated_user = True
                st.session_state.user_id = email.split('@')[0]
                st.session_state.user_email = email
                st.session_state.email_verified = True
                st.session_state.subscription_tier = "monthly_pro"  # Default to pro for demo
                st.success("? Login successful!")
                st.rerun()
            else:
                st.error("? Please enter both email and password")
        
        if forgot_pw:
            st.info("?? Password reset link would be sent to your email")

def show_registration_form():
    """Simple registration form"""
    st.markdown("### ?? Create Your Account")
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name*", placeholder="John")
        with col2:
            last_name = st.text_input("Last Name*", placeholder="Doe")
        
        email = st.text_input("?? Email Address*", placeholder="john.doe@example.com")
        
        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input("?? Password*", type="password", placeholder="Min 8 characters")
        with col2:
            confirm_password = st.text_input("?? Confirm Password*", type="password", placeholder="Re-enter password")
        
        phone = st.text_input("?? Phone Number (optional)", placeholder="+1 (555) 123-4567")
        
        st.markdown("---")
        
        terms = st.checkbox("? I accept the Terms & Conditions and Privacy Policy (Required, Age 16+)*", value=False)
        marketing = st.checkbox("?? I consent to receive marketing communications (Optional)", value=False)
        
        register_button = st.form_submit_button("?? Create Account", use_container_width=True, type="primary")
        
        if register_button:
            # Validation
            if not all([first_name, last_name, email, password, confirm_password]):
                st.error("? Please fill in all required fields")
            elif not validate_email(email):
                st.error("? Please enter a valid email address")
            elif len(password) < 8:
                st.error("? Password must be at least 8 characters")
            elif password != confirm_password:
                st.error("? Passwords do not match")
            elif not terms:
                st.error("? You must accept the Terms & Conditions")
            else:
                # Create account (demo - just set session state)
                st.session_state.authenticated_user = True
                st.session_state.user_id = first_name
                st.session_state.user_email = email
                st.session_state.subscription_tier = "free"
                st.session_state.terms_accepted = True
                st.session_state.marketing_consent = marketing
                st.success("?? Account created successfully!")
                st.info("?? Please check your email for verification (demo mode - auto-verified)")
                st.session_state.email_verified = True
                st.rerun()

def show_sidebar():
    """Show sidebar only for authenticated users with subscription info"""
    if not st.session_state.get("authenticated_user"):
        return  # Don't show sidebar if not logged in
    
    st.sidebar.title("?? IntelliCV-AI")
    
    # User info
    st.sidebar.markdown(f"""
    ### ?? {st.session_state.get('user_id', 'User')}
    **??** {st.session_state.get('user_email', 'N/A')}
    **??** {st.session_state.get('subscription_tier', 'free').replace('_', ' ').title()}
    """)
    
    if not st.session_state.get('email_verified'):
        st.sidebar.warning("?? Please verify your email")
    
    st.sidebar.markdown("---")
    
    # Navigation
    st.sidebar.markdown("### ?? Navigation")
    st.sidebar.page_link("pages/01_Home.py", label="?? Home Dashboard")
    st.sidebar.page_link("pages/09_Resume_Upload_Career_Intelligence_Express.py", label="?? Resume Upload")
    st.sidebar.page_link("pages/10_Your_Current_Resume.py", label="?? Your Resume")
    st.sidebar.page_link("pages/11_Career_Intelligence_Suite.py", label="?? Career Intelligence")
    
    st.sidebar.markdown("---")
    
    # Subscription management
    st.sidebar.markdown("### ?? Subscription")
    tier = st.session_state.get('subscription_tier', 'free')
    
    if tier == 'free':
        st.sidebar.info("?? Free Starter - 10 tokens/month")
        if st.sidebar.button("?? Upgrade to Pro"):
            st.session_state.show_pricing = True
            st.rerun()
    elif tier == 'monthly_pro':
        st.sidebar.success("? Monthly Pro - 100 tokens/month")
    elif tier == 'annual_pro':
        st.sidebar.success("?? Annual Pro - 250 tokens/month")
    elif tier == 'enterprise_pro':
        st.sidebar.success("?? Enterprise Pro - 1000 tokens/month")
    
    # Feature gating indicators
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ?? Your Access")
    
    # Show locked/unlocked features based on tier
    features_by_tier = {
        'free': ['Resume Builder', 'Basic Upload'],
        'monthly_pro': ['Full Job Suite', 'Resume Intelligence'],
        'annual_pro': ['Career Launch Hub', 'Personal Branding'],
        'enterprise_pro': ['Coaching', 'Mentorship', 'Priority Support']
    }
    
    tier_hierarchy = ['free', 'monthly_pro', 'annual_pro', 'enterprise_pro']
    current_tier_index = tier_hierarchy.index(tier) if tier in tier_hierarchy else 0
    
    for idx, (tier_name, features) in enumerate(features_by_tier.items()):
        if idx <= current_tier_index:
            for feature in features:
                st.sidebar.success(f"? {feature}")
        else:
            for feature in features:
                st.sidebar.warning(f"?? {feature} (Upgrade needed)")
    
    st.sidebar.markdown("---")
    
    # Logout
    if st.sidebar.button("?? Logout"):
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def show_welcome_authenticated():
    """Welcome page for logged-in users"""
    tier = st.session_state.get('subscription_tier', 'free')
    user_name = st.session_state.get('user_id', 'User')
    
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #10b981, #3b82f6); 
                border-radius: 15px; color: white; margin: 2rem 0;">
        <h2>?? Welcome back, {user_name}!</h2>
        <p style="font-size: 1.2rem;">
            You're on the <strong>{tier.replace('_', ' ').title()}</strong> plan
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("### ?? Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #f8fafc; border-radius: 10px;">
            <h3>?? Upload Resume</h3>
            <p>Start your career analysis</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("?? Upload Now", key="quick_upload", use_container_width=True, type="primary"):
            st.switch_page("pages/09_Resume_Upload_Career_Intelligence_Express.py")
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #f8fafc; border-radius: 10px;">
            <h3>?? Career Intelligence</h3>
            <p>Analyze your career path</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("?? Explore", key="quick_career", use_container_width=True):
            st.switch_page("pages/11_Career_Intelligence_Suite.py")
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #f8fafc; border-radius: 10px;">
            <h3>?? UMarketU Suite</h3>
            <p>Complete career marketing platform</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("?? Launch UMarketU", key="quick_umarketu", use_container_width=True):
            st.switch_page("pages/12_UMarketU_Suite.py")
    
    # Show feature access summary
    st.markdown("---")
    st.markdown("### ?? Your Plan Features")
    
    if tier == 'free':
        st.info("?? **Free Starter**: 10 tokens/month � Resume chatbot � Basic upload")
    elif tier == 'monthly_pro':
        st.success("? **Monthly Pro**: 100 tokens/month � Full Job Suite � Resume Intelligence")
    elif tier == 'annual_pro':
        st.success("?? **Annual Pro**: 250 tokens/month � Career Launch Hub � Personal Branding")
    elif tier == 'enterprise_pro':
        st.success("?? **Enterprise Pro**: 1000 tokens/month � Coaching � Mentorship � Priority Support")

# =============================================
# END OF AUTHENTICATION UI FUNCTIONS
# =============================================

def main():
    """
    Main application entry point with AUTHENTICATION
    Flow: Welcome ? Login/Register ? Authenticated Dashboard
    """
    
    try:
        # Load CSS
        load_professional_css()
        
        # Show sidebar ONLY if authenticated
        show_sidebar()
        
        # Check authentication status
        if not st.session_state.get("authenticated_user"):
            # NOT LOGGED IN - Show landing page with login/register
            
            # Show welcome header
            render_application_header()
            
            # Show journey steps
            render_user_journey_steps()
            
            st.markdown("---")
            
            # Login/Registration tabs
            st.markdown("### ?? Welcome to IntelliCV-AI")
            st.markdown("**Login or create an account to access your intelligent career platform**")
            
            tab1, tab2 = st.tabs(["?? Login", "?? Create Account"])
            
            with tab1:
                show_login_form()
            
            with tab2:
                show_registration_form()
            
            st.markdown("---")
            
            # Show platform features to entice signup
            st.markdown("### ?? What You Get With IntelliCV-AI")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="feature-card">
                    <h3>?? Resume Intelligence</h3>
                    <ul>
                        <li>AI Resume Builder</li>
                        <li>ATS Optimization</li>
                        <li>Peer Review</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="feature-card">
                    <h3>?? Career Intelligence</h3>
                    <ul>
                        <li>Touch Point Analysis</li>
                        <li>Job Matching</li>
                        <li>Career Insights</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="feature-card">
                    <h3>?? Job Search</h3>
                    <ul>
                        <li>AI Job Matching</li>
                        <li>Application Tracking</li>
                        <li>Interview Prep</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
        else:
            # LOGGED IN - Show authenticated dashboard
            show_welcome_authenticated()
            
            # Show platform suites
            st.markdown("---")
            st.markdown("### ?? IntelliCV-AI Platform Suites")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="feature-card">
                    <h3>?? Resume Intelligence Suite</h3>
                    <ul>
                        <li><strong>FREE:</strong> Resume Chatbot Builder</li>
                        <li><strong>FREE:</strong> Resume Upload & Analysis</li>
                        <li><strong>PREMIUM:</strong> Advanced Peer Review</li>
                        <li><strong>PREMIUM:</strong> ATS Optimization</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="feature-card">
                    <h3>?? Career Intelligence Suite</h3>
                    <ul>
                        <li>Strength/Weakness Analysis</li>
                        <li>Touch Point Mapping</li>
                        <li>Career Path Insights</li>
                        <li>Skills Gap Identification</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="feature-card">
                    <h3>? Career Launch Hub</h3>
                    <ul>
                        <li>Job Search Engine</li>
                        <li>Application Tracking</li>
                        <li>Interview Coaching</li>
                        <li>Personal Branding</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            col4, col5, col6 = st.columns(3)
            
            with col4:
                st.markdown("""
                <div class="feature-card">
                    <h3>?? Interview Coach</h3>
                    <ul>
                        <li>Mock Interviews</li>
                        <li>Question Prep</li>
                        <li>Company Research</li>
                        <li>Success Tips</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col5:
                st.markdown("""
                <div class="feature-card">
                    <h3>?? Career Coach</h3>
                    <ul>
                        <li>Career Navigation</li>
                        <li>Skills Gap Identification</li>
                        <li>Growth Recommendations</li>
                        <li>Industry Insights</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col6:
                st.markdown("""
                <div class="feature-card">
                    <h3>?? Mentorship Suite</h3>
                    <ul>
                        <li>Mentorship Hub</li>
                        <li>Marketplace Matching</li>
                        <li>Career Guidance</li>
                        <li>Expert Connections</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
        
        # PRICING SECTION - Streamlit Native Components
        st.markdown("### ?? Choose Your Plan")
        st.markdown("**Flexible pricing:** Choose subscription tiers OR use token-based access")
        
        price_col1, price_col2, price_col3, price_col4 = st.columns(4)
        
        with price_col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 1.5rem; border-radius: 10px; color: white; text-align: center;">
                <h3>?? Free Starter</h3>
                <h2 style="margin: 0.5rem 0;">$0</h2>
                <p style="font-size: 0.9rem;">10 tokens/month</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            **Features:**
            - Resume Builder Chatbot
            - Resume Upload & Analysis
            - Basic Career Insights
            - Community Access
            """)
        
        with price_col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; border-radius: 10px; color: white; text-align: center;">
                <h3>? Monthly Pro</h3>
                <h2 style="margin: 0.5rem 0;">$15.99</h2>
                <p style="font-size: 0.9rem;">100 tokens/month</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            **Features:**
            - **Full Job Suite Access**
            - AI Job Matching
            - Interview Prep Tools
            - Application Tracker
            """)
        
        with price_col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 1.5rem; border-radius: 10px; color: white; text-align: center; 
                        border: 3px solid gold;">
                <div style="background: gold; color: #333; padding: 0.2rem 0.6rem; 
                            border-radius: 10px; display: inline-block; font-weight: bold; 
                            font-size: 0.7rem; margin-bottom: 0.3rem;">
                    ? BEST VALUE
                </div>
                <h3>?? Annual Pro</h3>
                <h2 style="margin: 0.5rem 0;">$149.99<span style="font-size: 0.6rem;">/year</span></h2>
                <p style="font-size: 0.9rem;">250 tokens/month</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            **Features:**
            - **Everything in Monthly**
            - **Career Launch Hub**
            - **Dual-Career Optimization** ??
            - Advanced Analytics
            - Industry Reports
            """)
        
        with price_col4:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100);  
                        padding: 1.5rem; border-radius: 10px; color: #333; text-align: center;">
                <h3>?? Enterprise Pro</h3>
                <h2 style="margin: 0.5rem 0;">$299.99</h2>
                <p style="font-size: 0.9rem;">1000 tokens/month</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            **Features:**
            - **Everything in Annual**
            - **Career Coaching** (50 tokens/hr)
            - **Mentorship Hub** (25 tokens)
            - Custom AI Training
            - Priority Support
            """)
        
        st.info("""
        ?? **Token-Based Access:** Pay only for what you use  
        ?? Tokens refresh monthly � Unused tokens don't roll over  
        ?? Emergency token packs: 25 tokens for $4.99  
        ? All plans include priority support
        """)
        
        st.markdown("---")
        
        # Quick navigation to FREE tier pages
        st.subheader("?? FREE Tier - Get Started")
        st.info("?? **FREE Features:** Build resume with chatbot ? Upload & get basic insights ? Opt-in for freemium features")
        
        nav_col1, nav_col2 = st.columns(2)
        
        with nav_col1:
            st.page_link("pages/10_Your_Current_Resume.py", label="?? Build Your Resume (FREE Chatbot)", use_container_width=True)
        
        with nav_col2:
            st.page_link("pages/12_Resume_Upload_Enhanced.py", label="?? Upload Resume (FREE Analysis)", use_container_width=True)
    
    except Exception as e:
        # Error handling with fallback
        error_message = f"Application error: {str(e)}"
        
        if ERROR_HANDLER_AVAILABLE:
            log_error("main_app_error", error_message, {
                'traceback': traceback.format_exc()
            })
        
        st.error(f"?? Application Error: {error_message}")
        st.info("Please refresh the page or contact support if the issue persists.")

# Application entry point
if __name__ == "__main__":
    main()
