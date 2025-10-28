"""
🚀 IntelliCV-AI User Portal - Main Application
===========================================
Enhanced user portal with comprehensive authentication, 2FA, and security features
Main entry point for the Streamlit application
"""

import streamlit as st
import sys
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import authentication system
from enhanced_authentication import (
    get_authenticator, 
    check_authentication, 
    render_login_form, 
    render_user_menu,
    PasswordStrengthValidator,
    TwoFactorAuth
)

# Import token management
try:
    from token_management_system import TokenManager
    TOKEN_SYSTEM_AVAILABLE = True
except ImportError:
    TOKEN_SYSTEM_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="🚀 IntelliCV-AI Portal",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def render_sidebar_navigation():
    """Render sidebar navigation for authenticated users"""
    if not check_authentication():
        return
    
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        # User info display
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; color: white; margin-bottom: 20px;'>
            <h4 style='margin: 0; color: white;'>👋 {st.session_state.get('authenticated_full_name', 'User')}</h4>
            <p style='margin: 5px 0 0 0; opacity: 0.9;'>{st.session_state.get('authenticated_subscription_tier', 'Free')} Plan</p>
            <p style='margin: 5px 0 0 0; opacity: 0.9;'>🪙 {st.session_state.get('authenticated_tokens_remaining', 0)} tokens</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🏠 Dashboard", use_container_width=True):
            st.switch_page("pages/01_Dashboard.py")
        
        if st.button("📄 Resume Upload", use_container_width=True):
            st.switch_page("pages/09_Resume_Upload_Enhanced_Career_Intelligence.py")
        
        if st.button("👤 Profile", use_container_width=True):
            st.switch_page("pages/08_Profile_Complete.py")
        
        if st.button("💰 Pricing", use_container_width=True):
            st.switch_page("pages/06_Pricing.py")
        
        # Admin section
        if st.session_state.get('authenticated_is_admin', False):
            st.markdown("---")
            st.markdown("### 👑 Admin")
            if st.button("🔧 Admin Portal", use_container_width=True):
                st.info("Admin portal would open here")
        
        # Logout
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                if key.startswith('authenticated_'):
                    del st.session_state[key]
            st.session_state.authenticated_user = False
            st.rerun()

def render_welcome_dashboard():
    """Render welcome dashboard for authenticated users"""
    st.markdown("""
    <div style='text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0; font-size: 3em;'>🚀 Welcome to IntelliCV-AI</h1>
        <p style='color: white; margin: 10px 0 0 0; font-size: 1.2em;'>Your AI-Powered Career Intelligence Hub</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;'>
            <h3 style='color: #667eea; margin-bottom: 15px;'>📄 Resume Intelligence</h3>
            <p>Upload your resume and get instant analysis with peer group comparisons and job title overlap visualization.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Resume Analysis", key="resume_btn", use_container_width=True):
            st.switch_page("pages/09_Resume_Upload_Enhanced_Career_Intelligence.py")
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;'>
            <h3 style='color: #764ba2; margin-bottom: 15px;'>👤 Profile Setup</h3>
            <p>Complete your professional profile with our AI chatbot that asks whimsical questions about your career aspirations.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✨ Complete Profile", key="profile_btn", use_container_width=True):
            st.switch_page("pages/08_Profile_Complete.py")
    
    with col3:
        st.markdown("""
        <div style='background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;'>
            <h3 style='color: #667eea; margin-bottom: 15px;'>🎯 Job Matching</h3>
            <p>Find your perfect job match with our AI-powered job matching engine and career intelligence tools.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔍 Find Jobs", key="jobs_btn", use_container_width=True):
            st.switch_page("pages/16_Job_Match.py")
    
    # User stats
    st.markdown("---")
    st.markdown("### 📊 Your Account Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Subscription Plan",
            st.session_state.get('authenticated_subscription_tier', 'Free')
        )
    
    with col2:
        st.metric(
            "Tokens Remaining",
            st.session_state.get('authenticated_tokens_remaining', 0)
        )
    
    with col3:
        st.metric(
            "Account Type",
            "Admin 👑" if st.session_state.get('authenticated_is_admin', False) else "User"
        )
    
    with col4:
        st.metric(
            "2FA Status",
            "Enabled 🔐" if st.session_state.get('authenticated_2fa_enabled', False) else "Disabled"
        )
    
    # Recent activity placeholder
    st.markdown("### 📈 Quick Start Guide")
    
    with st.expander("🔰 Getting Started with IntelliCV-AI", expanded=True):
        st.markdown("""
        **Welcome! Here's how to get the most out of your IntelliCV-AI experience:**
        
        1. **📄 Upload Your Resume** - Start with our Enhanced Career Intelligence Hub
           - Get professional précis generation
           - See peer group word cloud analysis
           - View job title overlap visualization
           - Receive career optimization recommendations
        
        2. **👤 Complete Your Profile** - Use our AI chatbot for profile setup
           - Answer whimsical questions about your career
           - Get enthusiasm and creativity scoring
           - Build comprehensive career insights
        
        3. **🎯 Explore Job Matching** - Find your perfect career fit
           - AI-powered job recommendations
           - Skill gap analysis
           - Market intelligence insights
        
        4. **🔐 Secure Your Account** - Enable two-factor authentication
           - Enhanced security with TOTP codes
           - Backup codes for emergency access
           - Account lockout protection
        """)
    
    # Token usage guidance
    if TOKEN_SYSTEM_AVAILABLE:
        with st.expander("🪙 Token Usage Guide"):
            st.markdown("""
            **Your token balance determines which features you can access:**
            
            - **FREE (0 tokens):** Basic navigation, account management, pricing info
            - **BASIC (1-2 tokens):** Profile setup, application tracking, resume history
            - **STANDARD (3-5 tokens):** Resume upload, job matching, feedback tools
            - **ADVANCED (6-10 tokens):** AI-enhanced features, interview coaching
            - **PREMIUM (11-20 tokens):** Advanced career tools, AI insights
            - **ENTERPRISE (21-50 tokens):** Mentorship hub, marketplace access
            
            💡 **Tip:** Start with our Enhanced Resume Upload (7 tokens) for comprehensive career intelligence!
            """)

def render_security_features_demo():
    """Render security features demonstration"""
    st.markdown("### 🔐 Security Features Demo")
    
    with st.expander("🛡️ Password Strength Tester", expanded=False):
        st.markdown("Test our real-time password strength indicator:")
        
        test_password = st.text_input(
            "Enter a test password:",
            type="password",
            placeholder="Try different passwords to see strength indication",
            key="test_password"
        )
        
        if test_password:
            from enhanced_authentication import PasswordStrengthValidator
            strength_data = PasswordStrengthValidator.check_password_strength(test_password)
            
            # Progress bar
            st.markdown(f"""
            <div style='margin: 10px 0;'>
                <div style='background: #f0f0f0; border-radius: 10px; height: 12px; overflow: hidden;'>
                    <div style='background: {strength_data["color"]}; height: 100%; width: {strength_data["percentage"]}%; transition: all 0.3s ease;'></div>
                </div>
                <div style='display: flex; justify-content: space-between; margin-top: 8px;'>
                    <span style='color: {strength_data["color"]}; font-weight: bold; font-size: 1.1em;'>{strength_data["strength"]}</span>
                    <span style='color: #666; font-size: 1em;'>{strength_data["score"]}/{strength_data["max_score"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if strength_data['feedback']:
                st.info("💡 **Suggestions to improve password strength:**")
                for tip in strength_data['feedback']:
                    st.write(f"   • {tip}")
    
    with st.expander("📱 Two-Factor Authentication Info", expanded=False):
        st.markdown("""
        **IntelliCV-AI supports robust 2FA options:**
        
        - **📱 TOTP Authenticator Apps:** Google Authenticator, Authy, Microsoft Authenticator
        - **🔑 Manual Key Entry:** For apps that don't support QR codes
        - **🔒 Backup Codes:** 8 single-use codes for emergency access
        - **⏰ Time-based Tokens:** 30-second rotating codes for security
        - **🛡️ Backup Protection:** Multiple recovery options
        
        **Setup Process:**
        1. Click "Setup 2FA" on the login page
        2. Scan QR code with your authenticator app
        3. Enter verification code to confirm
        4. Save backup codes securely
        5. 2FA is now active for your account!
        """)

def main():
    """Main application logic"""
    # Initialize session state
    if 'authenticated_user' not in st.session_state:
        st.session_state.authenticated_user = False
    
    # Initialize authenticator
    authenticator = get_authenticator()
    
    # Render navigation
    render_sidebar_navigation()
    
    # Main content based on authentication status
    if check_authentication():
        # Authenticated user dashboard
        render_welcome_dashboard()
        
        # Show security features for demo
        if st.session_state.get('authenticated_email') == 'janatmainswood@gmail.com':
            st.markdown("---")
            render_security_features_demo()
        
    else:
        # Login form for unauthenticated users
        render_login_form(authenticator)
        
        # Show demo credentials
        st.markdown("---")
        with st.expander("🔑 Demo Credentials", expanded=True):
            st.info("""
            **Test the login system with these credentials:**
            
            📧 **Email:** janatmainswood@gmail.com  
            🔒 **Password:** JanJ3143@?  
            
            **Features to test:**
            - Real-time password strength indicator
            - Account lockout protection (5 failed attempts)
            - Two-factor authentication setup
            - Session management and security
            - Admin privileges and token management
            """)

if __name__ == "__main__":
    main()