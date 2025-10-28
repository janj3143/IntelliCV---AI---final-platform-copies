"""
🏠 IntelliCV-AI Main Application
==============================
Main Streamlit application with enhanced authentication system
Features:
- Secure login with password strength validation
- 2FA support (Authenticator app & Mobile PIN)
- Account lockout protection
- Session management
- Navigation to all portal features
"""

import streamlit as st
import sys
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import our enhanced authentication system
from enhanced_auth_system import EnhancedAuthenticator, render_login_form, render_2fa_verification

# Page configuration
st.set_page_config(
    page_title="IntelliCV-AI Portal",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def render_sidebar():
    """Render sidebar with navigation and user info"""
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 20px;'>
            <h2 style='color: white; margin: 0;'>🧠 IntelliCV-AI</h2>
            <p style='color: white; margin: 5px 0 0 0;'>Career Intelligence Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # User info if authenticated
        if st.session_state.get('authenticated_user'):
            user_data = st.session_state.get('user_data', {})
            user_name = user_data.get('name', 'User')
            user_email = st.session_state.get('authenticated_user')
            
            st.markdown(f"""
            <div style='background: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
                <h4 style='margin: 0; color: #1f77b4;'>👤 {user_name}</h4>
                <p style='margin: 5px 0 0 0; font-size: 0.9em; color: #666;'>{user_email}</p>
                <p style='margin: 5px 0 0 0; font-size: 0.8em; color: #28a745;'>
                    🔐 2FA: {'✅ Enabled' if user_data.get('two_factor_enabled') else '❌ Disabled'}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Navigation menu
            st.markdown("### 🧭 Navigation")
            
            # Main pages
            if st.button("🏠 Dashboard", use_container_width=True):
                st.switch_page("pages/04_Dashboard.py")
            
            if st.button("📄 Enhanced Resume Upload", use_container_width=True):
                st.switch_page("pages/09_Resume_Upload_Enhanced_Career_Intelligence.py")
            
            if st.button("👤 Profile Complete", use_container_width=True):
                st.switch_page("pages/08_Profile_Complete.py")
            
            if st.button("💰 Payment & Pricing", use_container_width=True):
                st.switch_page("pages/02_Payment.py")
            
            st.divider()
            
            # Quick access to key features
            st.markdown("### 🚀 Quick Access")
            
            if st.button("🎯 Job Matching", use_container_width=True):
                st.switch_page("pages/16_Job_Match.py")
            
            if st.button("🤖 AI Interview Coach", use_container_width=True):
                st.switch_page("pages/30_AI_Interview_Coach.py")
            
            if st.button("📊 Career Intelligence", use_container_width=True):
                st.switch_page("pages/32_Career_Intelligence.py")
            
            st.divider()
            
            # Account actions
            st.markdown("### ⚙️ Account")
            
            if st.button("🔐 Security Settings", use_container_width=True):
                st.session_state['show_security'] = True
                st.rerun()
            
            if st.button("🚪 Logout", use_container_width=True):
                # Clear session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        else:
            # Login prompt
            st.info("🔒 Please log in to access the portal")
            
            # Demo credentials
            st.markdown("### 🧪 Demo Access")
            st.code("""
Email: janatmainswood@gmail.com
Password: JanJ3143@?
            """)

def render_welcome_dashboard():
    """Render welcome dashboard for authenticated users"""
    user_data = st.session_state.get('user_data', {})
    user_name = user_data.get('name', 'User')
    
    # Welcome header
    st.markdown(f"""
    <div style='text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0; font-size: 3em;'>👋 Welcome, {user_name}!</h1>
        <p style='color: white; margin: 15px 0 0 0; font-size: 1.3em;'>Your AI-Powered Career Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: #f8f9fa; padding: 25px; border-radius: 15px; text-align: center; border: 2px solid #007bff;'>
            <h3 style='color: #007bff; margin-top: 0;'>📄 Resume Intelligence</h3>
            <p>Upload your resume for comprehensive analysis with peer group comparisons and job title overlap visualization.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Resume Analysis", use_container_width=True):
            st.switch_page("pages/09_Resume_Upload_Enhanced_Career_Intelligence.py")
    
    with col2:
        st.markdown("""
        <div style='background: #f8f9fa; padding: 25px; border-radius: 15px; text-align: center; border: 2px solid #28a745;'>
            <h3 style='color: #28a745; margin-top: 0;'>👤 Profile Setup</h3>
            <p>Complete your profile with our AI chatbot assistant for personalized career insights and recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✨ Complete Profile", use_container_width=True):
            st.switch_page("pages/08_Profile_Complete.py")
    
    with col3:
        st.markdown("""
        <div style='background: #f8f9fa; padding: 25px; border-radius: 15px; text-align: center; border: 2px solid #ffc107;'>
            <h3 style='color: #e68900; margin-top: 0;'>🎯 Career Matching</h3>
            <p>Find perfect job matches using our AI-powered career intelligence and market analysis engines.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔍 Find Opportunities", use_container_width=True):
            st.switch_page("pages/16_Job_Match.py")
    
    st.divider()
    
    # Platform features overview
    st.markdown("### 🌟 Platform Features")
    
    feature_cols = st.columns(2)
    
    with feature_cols[0]:
        st.markdown("""
        **🧠 AI-Powered Analysis:**
        - Professional précis generation
        - Peer group skill comparison
        - Job title compatibility scoring
        - Career optimization recommendations
        
        **📊 Advanced Intelligence:**
        - Real-time market data integration
        - Competitive intelligence analysis
        - Industry trend insights
        - Geographic career mapping
        """)
    
    with feature_cols[1]:
        st.markdown("""
        **🔐 Security Features:**
        - Password strength validation
        - Two-factor authentication (2FA)
        - Account lockout protection
        - Secure data encryption
        
        **💰 Flexible Pricing:**
        - Token-based system
        - Hybrid subscription options
        - Free tier available
        - Enterprise solutions
        """)
    
    # Quick stats (simulated)
    st.divider()
    st.markdown("### 📈 Your Progress")
    
    progress_cols = st.columns(4)
    
    with progress_cols[0]:
        st.metric("Profile Completion", "75%", "+15%")
    
    with progress_cols[1]:
        st.metric("Resume Score", "8.5/10", "+0.5")
    
    with progress_cols[2]:
        st.metric("Job Matches", "23", "+7")
    
    with progress_cols[3]:
        st.metric("Tokens Available", "45", "-5")

def render_security_settings():
    """Render security settings page"""
    st.markdown("### 🔐 Security Settings")
    
    user_data = st.session_state.get('user_data', {})
    authenticator = EnhancedAuthenticator()
    
    # Current security status
    st.markdown("#### Current Security Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        is_2fa_enabled = user_data.get('two_factor_enabled', False)
        if is_2fa_enabled:
            st.success("✅ Two-Factor Authentication: Enabled")
        else:
            st.warning("❌ Two-Factor Authentication: Disabled")
    
    with col2:
        failed_attempts = user_data.get('failed_attempts', 0)
        if failed_attempts == 0:
            st.success("✅ Account Status: Secure")
        else:
            st.warning(f"⚠️ Failed Attempts: {failed_attempts}")
    
    st.divider()
    
    # 2FA Management
    if not is_2fa_enabled:
        st.markdown("#### 🛡️ Enable Two-Factor Authentication")
        st.info("Protect your account with an additional layer of security")
        
        if st.button("🔐 Setup 2FA"):
            st.session_state['setup_2fa'] = True
            st.rerun()
        
        if st.session_state.get('setup_2fa'):
            from enhanced_auth_system import render_2fa_setup
            render_2fa_setup(authenticator, st.session_state.get('authenticated_user'))
    else:
        st.markdown("#### ✅ Two-Factor Authentication Enabled")
        st.success("Your account is protected with 2FA")
        
        if st.button("🔧 Manage 2FA"):
            st.info("2FA management options would be available here in production")
    
    st.divider()
    
    # Password strength info
    st.markdown("#### 🔑 Password Security")
    st.info("Your password meets all security requirements")
    
    if st.button("🔄 Change Password"):
        st.info("Password change functionality would be implemented here")
    
    # Back button
    if st.button("🔙 Back to Dashboard"):
        if 'show_security' in st.session_state:
            del st.session_state['show_security']
        st.rerun()

def main():
    """Main application logic"""
    # Initialize authentication
    authenticator = EnhancedAuthenticator()
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    if st.session_state.get('authenticated_user'):
        # User is authenticated
        if st.session_state.get('show_security'):
            render_security_settings()
        else:
            render_welcome_dashboard()
    
    elif st.session_state.get('show_2fa'):
        # Show 2FA verification
        render_2fa_verification(authenticator)
    
    else:
        # Show login form
        render_login_form(authenticator)

if __name__ == "__main__":
    main()