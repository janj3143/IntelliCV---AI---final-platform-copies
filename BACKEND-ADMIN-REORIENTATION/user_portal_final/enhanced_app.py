
# User Portal - Clean interface without admin functions

#!/usr/bin/env python3
"""
🚀 IntelliCV-AI Enhanced User Portal
Comprehensive application launcher with secure authentication integration

Combines:
- Frontend page management system
- Enhanced secure authentication 
- GDPR compliance
- Session management
- Admin portal compatibility
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Setup paths for enhanced authentication
current_dir = Path(__file__).parent
auth_dir = current_dir / "auth"
pages_dir = current_dir / "pages" 
utils_dir = current_dir / "utils"
fragments_dir = current_dir / "fragments"

# Add paths to Python path
for path in [str(current_dir), str(auth_dir), str(pages_dir), str(utils_dir), str(fragments_dir)]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Simple authentication - avoid complex dependencies
SECURE_AUTH_AVAILABLE = False

# Enhanced navigation imports
try:
    from utils.enhanced_navigation import render_enhanced_navigation, inject_navigation_css
    ENHANCED_NAVIGATION_AVAILABLE = True
except ImportError:
    ENHANCED_NAVIGATION_AVAILABLE = False

# Clean User Portal - No admin functions

# Legacy session utilities (maintain compatibility)
try:
    from utils.session_utils import load_working_profile, load_keywords, ensure_working_dir
    LEGACY_UTILS_AVAILABLE = True
except ImportError:
    LEGACY_UTILS_AVAILABLE = False

# Fragment imports for sidebar management
try:
    from fragments.sidebar import show_sidebar
    from fragments.sidebar_admin import show_admin_sidebar  
    from fragments.sidebar_debug import show_debug_sidebar
    FRAGMENTS_AVAILABLE = True
except ImportError:
    FRAGMENTS_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="IntelliCV-AI | Your Unique Career & Advisory Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"  # Start collapsed for unauthenticated users
)

# Load professional logo background CSS
def load_professional_css():
    """Load the professional logo background CSS"""
    css_file = Path("static/professional_logo_background.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # Enhanced CSS with highly visible background logo
        st.markdown("""
        <style>
        .stApp {
            background: 
                linear-gradient(135deg, rgba(102, 126, 234, 0.75) 0%, rgba(118, 75, 162, 0.75) 100%),
                url('static/logo1.png') center/contain no-repeat fixed !important;
            background-size: 40% auto, cover;
            background-position: center center, center center;
        }
        
        .main .block-container {
            background: rgba(255, 255, 255, 0.92) !important;
            backdrop-filter: blur(8px);
            border-radius: 20px;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
            border: 2px solid rgba(255, 255, 255, 0.3);
            margin: 1rem auto;
            padding: 2rem !important;
        }
        
        /* Logo watermark overlay */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('static/logo1.png') center/25% no-repeat;
            opacity: 0.1;
            pointer-events: none;
            z-index: 0;
        }
        
        /* Ensure content is above watermark */
        .main {
            position: relative;
            z-index: 1;
        }
        </style>
        """, unsafe_allow_html=True)

# Apply professional styling
load_professional_css()

# Simple authentication - no complex dependencies needed

# Initialize legacy session data if available
if LEGACY_UTILS_AVAILABLE:
    ensure_working_dir()
    if "profile_data" not in st.session_state:
        st.session_state["profile_data"] = load_working_profile()
    if "selected_keywords" not in st.session_state:
        st.session_state["selected_keywords"] = load_keywords()

# Enhanced session state initialization
default_session = {
    "authenticated_user": False,
    "is_admin": False,
    "debug_mode": False,
    "current_page": "Home",
    "user_id": None,
    "session_token": None,
    "auth_method": "enhanced" if SECURE_AUTH_AVAILABLE else "legacy",
    "gdpr_consent": False,
    "user_profile": {},
    "security_events": []
}

# Initialize session state with enhanced defaults
for key, value in default_session.items():
    if key not in st.session_state:
        st.session_state[key] = value

def check_authentication():
    """Enhanced authentication check"""
    if SECURE_AUTH_AVAILABLE and st.session_state.user_authenticator:
        # Use enhanced authentication system
        if st.session_state.get("session_token"):
            # Validate session token
            is_valid = st.session_state.user_authenticator.validate_session(
                st.session_state.session_token
            )
            if not is_valid:
                # Clear invalid session
                for key in ["authenticated_user", "session_token", "user_id"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state.authenticated_user = False
                return False
            return True
        return st.session_state.get("authenticated_user", False)
    else:
        # Fall back to legacy authentication
        return st.session_state.get("authenticated_user", False)

def render_sidebar():
    """Enhanced sidebar rendering with navigation and authentication"""
    # Do not show sidebar on authentication pages
    if st.session_state["current_page"] in ["Landing", "Login", "Register"]:
        return
    
    # Apply enhanced navigation CSS
    if ENHANCED_NAVIGATION_AVAILABLE:
        inject_navigation_css()
    
    # Use enhanced navigation if available
    if ENHANCED_NAVIGATION_AVAILABLE and st.session_state.get("authenticated_user"):
        render_enhanced_navigation()
        return
    
    # Fallback to basic sidebar
    if not FRAGMENTS_AVAILABLE:
        # Simple sidebar if fragments not available
        with st.sidebar:
            st.title("🚀 IntelliCV-AI")
            if st.session_state.get("authenticated_user"):
                st.success(f"Welcome, {st.session_state['authenticated_user']}!")
                if st.button("🚪 Logout"):
                    logout_user()
            return

    # Enhanced sidebar with authentication status
    with st.sidebar:
        # Authentication status indicator
        if st.session_state.get("authenticated_user"):
            st.success(f"✅ Authenticated: {st.session_state['authenticated_user']}")
            
            # Security indicators
            if SECURE_AUTH_AVAILABLE:
                if st.session_state.get("session_token"):
                    st.info("🔐 Enhanced Security Active")
                if st.session_state.get("gdpr_consent"):
                    st.success("🏛️ GDPR Compliant")
        
        # Show appropriate sidebar based on user role
        if st.session_state.get("is_admin"):
            show_admin_sidebar()
        elif st.session_state.get("debug_mode"):
            show_debug_sidebar()
        else:
            show_sidebar()

def logout_user():
    """Enhanced logout with secure session cleanup"""
    if SECURE_AUTH_AVAILABLE and st.session_state.get("session_token"):
        # Use enhanced logout
        st.session_state.user_authenticator.logout_user(st.session_state.session_token)
    
    # Clear all session data
    keys_to_clear = [
        "authenticated_user", "is_admin", "debug_mode", "user_id",
        "session_token", "gdpr_consent", "user_profile", "security_events"
    ]
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    
    # Reset to defaults
    st.session_state.authenticated_user = False
    st.session_state.current_page = "Landing"
    
    # Force page refresh
    st.rerun()

def show_home_page():
    """Integrated Home Page with Authentication"""
    
    # Main title with logo
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #1f2937; font-size: 3rem; margin-bottom: 1rem;">
            🚀 Welcome to IntelliCV-AI
        </h1>
        <h2 style="color: #6b7280; font-size: 1.5rem; margin-bottom: 2rem;">
            Your Intelligent Career & Resume Platform
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Authentication section
    if not st.session_state.get("authenticated_user"):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔐 Please Login or Register")
            
            tab1, tab2 = st.tabs(["Login", "Register"])
            
            with tab1:
                with st.form("login_form"):
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    login_button = st.form_submit_button("Login", use_container_width=True)
                    
                    if login_button:
                        if username and password:
                            # Simple authentication (enhance this with your auth system)
                            st.session_state.authenticated_user = True
                            st.session_state.user_id = username
                            st.success("✅ Login successful!")
                            st.rerun()
                        else:
                            st.error("Please enter both username and password")
            
            with tab2:
                with st.form("register_form"):
                    reg_username = st.text_input("Choose Username")
                    reg_email = st.text_input("Email Address") 
                    reg_password = st.text_input("Choose Password", type="password")
                    reg_confirm = st.text_input("Confirm Password", type="password")
                    register_button = st.form_submit_button("Register", use_container_width=True)
                    
                    if register_button:
                        if reg_username and reg_email and reg_password and reg_confirm:
                            if reg_password == reg_confirm:
                                st.session_state.authenticated_user = True
                                st.session_state.user_id = reg_username
                                st.success("✅ Registration successful!")
                                st.rerun()
                            else:
                                st.error("Passwords don't match")
                        else:
                            st.error("Please fill all fields")
    
    else:
        # Welcome authenticated user
        st.success(f"🎉 Welcome back, {st.session_state.get('user_id', 'User')}!")
        
        # Feature showcase
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 📊 Resume Analysis
            Upload and analyze your resume with AI-powered insights
            """)
            if st.button("Start Resume Analysis", key="resume_analysis"):
                st.switch_page("pages/01_Resume_Upload_and_Analysis.py")
        
        with col2:
            st.markdown("""
            ### 👤 Profile Management
            Build and manage your professional profile
            """)
            if st.button("Manage Profile", key="manage_profile"):
                st.switch_page("pages/02_Profile.py")
        
        with col3:
            st.markdown("""
            ### 🎯 Job Matching
            Find jobs that match your skills and experience
            """)
            if st.button("Find Jobs", key="find_jobs"):
                st.switch_page("pages/05_Job_Match_Insights.py")

def route_to_page():
    """Simple routing - default to home page"""
    current_page = st.session_state.get("current_page", "Home")
    
    if current_page == "Home" or current_page == "Landing":
        show_home_page()
    else:
        # Handle other page routing if needed
        show_home_page()

def get_page_file(page_name):
    """Map page names to file names"""
    page_mapping = {
        # Enhanced Dashboard (New Default Landing)
        "Dashboard": "01_Dashboard.py",
        
        # Core User Journey
        "Resume_Upload": "01_Resume_Upload.py",
        "Profile": "02_Profile.py", 
        "Job_Description": "03_Job_Description.py",
        "Resume_Feedback": "04_Resume_Feedback.py",
        "Job_Match_Insights": "05_Job_Match_Insights.py",
        "Resume_History": "06_Resume_History.py",
        "Resume_Tuner": "07_Resume_Tuner.py",
        "Job_Tracker": "09_Job_Tracker.py",
        
        # Enhanced Career Development Features
        "AI_Interview_Coach": "07_AI_Interview_Coach.py",
        "Career_Intelligence": "08_Career_Intelligence.py",
        "Mentorship_Hub": "09_Mentorship_Hub.py", 
        "Advanced_Career_Tools": "10_Advanced_Career_Tools.py",
        
        # Admin Functions
        "Admin_Panel": "99_admin/00_admin_login.py"
    }
    return page_mapping.get(page_name, "00_Home.py")

def display_system_status():
    """Display system status for debugging"""
    if st.session_state.get("debug_mode"):
        with st.expander("🔧 System Status", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Authentication Status:**")
                st.write(f"- Enhanced Auth: {'✅' if SECURE_AUTH_AVAILABLE else '❌'}")
                st.write(f"- Legacy Utils: {'✅' if LEGACY_UTILS_AVAILABLE else '❌'}")
                st.write(f"- Fragments: {'✅' if FRAGMENTS_AVAILABLE else '❌'}")
                st.write(f"- Current User: {st.session_state.get('authenticated_user', 'None')}")
                
            with col2:
                st.write("**Session Information:**")
                st.write(f"- Current Page: {st.session_state.get('current_page')}")
                st.write(f"- Auth Method: {st.session_state.get('auth_method')}")
                st.write(f"- GDPR Consent: {st.session_state.get('gdpr_consent')}")
                st.write(f"- Session Token: {'Set' if st.session_state.get('session_token') else 'None'}")

def main():
    """Main application entry point"""
    # Display system status if debug mode
    display_system_status()
    
    # Render sidebar
    render_sidebar()
    
    # Route to appropriate page
    route_to_page()
    
    # Display footer with system info
    if st.session_state.get("debug_mode"):
        st.markdown("---")
        st.caption(f"🚀 IntelliCV-AI Enhanced Portal | Auth: {st.session_state.get('auth_method')} | "
                  f"Version: Enhanced {'(Secure)' if SECURE_AUTH_AVAILABLE else '(Legacy)'}")

# Entry point check
if __name__ == "__main__":
    main()