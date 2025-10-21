#!/usr/bin/env python3
"""
🏠 Enhanced Landing Page with Secure Authentication Integration
Combines the best of both landing page systems with enhanced security
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Import the secure authentication system
try:
    from auth.secure_auth import UserAuthenticator, GDPRCompliance
    SECURE_AUTH_AVAILABLE = True
except ImportError:
    SECURE_AUTH_AVAILABLE = False

def main():
    """Main landing page with enhanced authentication"""
    
    # Initialize authenticator if available
    if SECURE_AUTH_AVAILABLE:
        if "user_authenticator" not in st.session_state:
            st.session_state.user_authenticator = UserAuthenticator()
        if "gdpr_compliance" not in st.session_state:
            st.session_state.gdpr_compliance = GDPRCompliance()
    
    # Custom CSS for enhanced styling with professional background
    st.markdown("""
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stAppHeader {display: none;}
    
    /* Global Streamlit app background with professional logo */
    .stApp {
        background: 
            linear-gradient(135deg, rgba(102, 126, 234, 0.85) 0%, rgba(118, 75, 162, 0.85) 100%),
            url('static/logo1.png') center/cover no-repeat fixed !important;
    }
    
    /* Main container styling with background logo */
    .main-container {
        background: 
            linear-gradient(135deg, rgba(102, 126, 234, 0.85) 0%, rgba(118, 75, 162, 0.85) 100%),
            url('static/logo1.png') center/cover no-repeat fixed;
        min-height: 100vh;
        padding: 0;
        margin: 0;
        position: relative;
    }
    
    /* Background overlay for better text readability */
    .main-container::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.1);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Enhanced header */
    .header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 1rem 2rem;
        box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border-radius: 0 0 20px 20px;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 15px;
        justify-content: center;
    }
    
    .logo-icon {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 15px;
        font-size: 2rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .logo-text {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .tagline {
        font-size: 1.1rem;
        color: #666;
        font-weight: 500;
        margin-top: 5px;
    }
    
    /* USP Banner */
    .usp-banner {
        background: linear-gradient(90deg, #2d3748 0%, #4a5568 50%, #2d3748 100%);
        color: white;
        padding: 15px 0;
        margin-bottom: 3rem;
        overflow: hidden;
        white-space: nowrap;
        border-radius: 10px;
        margin: 2rem 0;
    }
    
    .usp-scroll {
        display: inline-block;
        padding-left: 100%;
        animation: scroll-left 45s linear infinite;
        font-size: 1.2rem;
        font-weight: 500;
    }
    
    @keyframes scroll-left {
        0% { transform: translate3d(100%, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }
    
    .usp-item {
        margin-right: 3rem;
        color: #90cdf4;
    }
    
    .usp-item::before {
        content: "✨";
        margin-right: 8px;
        color: #ffd700;
    }
    
    /* Authentication cards */
    .auth-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .auth-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        min-width: 350px;
        max-width: 400px;
    }
    
    .welcome-section {
        text-align: center;
        padding: 3rem 2rem;
        color: white;
    }
    
    .welcome-title {
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    }
    
    .welcome-subtitle {
        font-size: 1.5rem;
        margin-bottom: 2rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Status indicators */
    .status-indicator {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        margin: 0.5rem;
        display: inline-block;
    }
    
    .status-secure {
        background: rgba(34, 197, 94, 0.2);
        color: #16a34a;
        border: 1px solid #16a34a;
    }
    
    .status-gdpr {
        background: rgba(59, 130, 246, 0.2);
        color: #2563eb;
        border: 1px solid #2563eb;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with branding
    st.markdown("""
    <div class="header">
        <div class="logo-container">
            <div class="logo-icon">🤖</div>
            <div>
                <div class="logo-text">IntelliCV-AI</div>
                <div class="tagline">Your Unique Career & Advisory Platform</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # USP Banner
    st.markdown("""
    <div class="usp-banner">
        <div class="usp-scroll">
            <span class="usp-item">AI-Powered CV Analysis & Enhancement</span>
            <span class="usp-item">Real-Time Job Market Intelligence</span>
            <span class="usp-item">Personalized Career Path Recommendations</span>
            <span class="usp-item">Advanced Skill Gap Analysis</span>
            <span class="usp-item">Interview Preparation with AI Coaching</span>
            <span class="usp-item">Salary Negotiation Insights</span>
            <span class="usp-item">Industry Trend Predictions</span>
            <span class="usp-item">Professional Network Expansion</span>
            <span class="usp-item">Resume ATS Optimization</span>
            <span class="usp-item">Career Milestone Tracking</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome Section
    st.markdown("""
    <div class="welcome-section">
        <h1 class="welcome-title">Welcome to IntelliCV-AI</h1>
        <p class="welcome-subtitle">Transform your career with AI-powered insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # System status indicators
    if SECURE_AUTH_AVAILABLE:
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <span class="status-indicator status-secure">🔐 Enhanced Security Active</span>
            <span class="status-indicator status-gdpr">🏛️ GDPR Compliant</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Check if user is already authenticated
    if st.session_state.get("authenticated_user"):
        st.success(f"✅ Welcome back, {st.session_state['authenticated_user']}!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📄 Resume Upload", use_container_width=True):
                st.session_state.current_page = "Resume_Upload"
                st.rerun()
        with col2:
            if st.button("👤 Profile", use_container_width=True):
                st.session_state.current_page = "Profile"
                st.rerun()
        with col3:
            if st.button("🚪 Logout", use_container_width=True):
                logout_user()
        return
    
    # Authentication interface
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Login")
        
        if SECURE_AUTH_AVAILABLE:
            render_enhanced_login()
        else:
            render_basic_login()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Register")
        
        if SECURE_AUTH_AVAILABLE:
            render_enhanced_registration()
        else:
            render_basic_registration()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_enhanced_login():
    """Enhanced login form with secure authentication"""
    with st.form("enhanced_login_form"):
        email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
        password = st.text_input("🔒 Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            remember_me = st.checkbox("Remember me", value=True)
        with col2:
            totp_code = st.text_input("🔐 2FA Code (if enabled)", placeholder="123456", max_chars=6)
        
        submitted = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
        
        if submitted:
            if not email or not password:
                st.error("❌ Please enter both email and password")
                return
            
            try:
                # Use enhanced authentication
                result = st.session_state.user_authenticator.login_user(
                    email, password, totp_code if totp_code else None
                )
                
                if result['success']:
                    st.session_state.authenticated_user = result['user']['email']
                    st.session_state.user_id = result['user']['user_id']
                    st.session_state.session_token = result['session_token']
                    st.session_state.user_profile = result['user']
                    
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")
                    
            except Exception as e:
                st.error(f"❌ Login error: {str(e)}")
    
    # Additional options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 Forgot Password?", use_container_width=True):
            st.info("Password reset functionality available - contact support")
    with col2:
        if st.button("🧪 Demo Login", use_container_width=True):
            # Demo login for testing
            st.session_state.authenticated_user = "demo@intellicv.ai"
            st.session_state.user_id = "demo_user"
            st.success("✅ Demo login successful!")
            st.rerun()

def render_enhanced_registration():
    """Enhanced registration form with secure authentication"""
    with st.form("enhanced_registration_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("👤 First Name")
        with col2:
            last_name = st.text_input("👤 Last Name")
        
        email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
        password = st.text_input("🔒 Password", type="password")
        confirm_password = st.text_input("🔒 Confirm Password", type="password")
        
        # Password strength indicator
        if password:
            strength = calculate_password_strength(password)
            if strength >= 4:
                st.success(f"🔒 Password Strength: Strong ({strength}/5)")
            elif strength >= 3:
                st.warning(f"🔒 Password Strength: Good ({strength}/5)")
            else:
                st.error(f"🔒 Password Strength: Weak ({strength}/5)")
        
        enable_2fa = st.checkbox("🔐 Enable Two-Factor Authentication (Recommended)", value=True)
        
        # GDPR Compliance
        if SECURE_AUTH_AVAILABLE:
            gdpr_consent = st.checkbox("🏛️ I agree to the privacy policy and data processing terms", value=False)
            marketing_consent = st.checkbox("📧 I consent to receive marketing communications (optional)", value=False)
        
        submitted = st.form_submit_button("📧 Create Account", use_container_width=True, type="primary")
        
        if submitted:
            # Validation
            if not all([first_name, last_name, email, password, confirm_password]):
                st.error("❌ Please fill in all required fields")
                return
            
            if password != confirm_password:
                st.error("❌ Passwords do not match")
                return
            
            if SECURE_AUTH_AVAILABLE and not gdpr_consent:
                st.error("❌ Privacy policy consent is required")
                return
            
            try:
                # Use enhanced registration
                result = st.session_state.user_authenticator.register_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    enable_2fa=enable_2fa
                )
                
                if result['success']:
                    # Record GDPR consent
                    if SECURE_AUTH_AVAILABLE:
                        st.session_state.gdpr_compliance.record_consent(
                            result['user']['user_id'],
                            'registration',
                            {
                                'privacy_policy': True,
                                'marketing': marketing_consent,
                                'data_processing': True
                            }
                        )
                    
                    st.success("✅ Registration successful! Please check your email for verification.")
                    
                    # Show 2FA setup if enabled
                    if enable_2fa and 'qr_code' in result:
                        st.info("📱 Scan this QR code with your authenticator app:")
                        st.image(result['qr_code'])
                else:
                    st.error(f"❌ {result['message']}")
                    
            except Exception as e:
                st.error(f"❌ Registration error: {str(e)}")

def render_basic_login():
    """Basic login form (fallback)"""
    with st.form("basic_login_form"):
        username = st.text_input("👤 Username", value="demo")
        password = st.text_input("🔒 Password", type="password", value="demo123")
        
        submitted = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
        
        if submitted and username and password:
            st.session_state.authenticated_user = username
            st.success("✅ Login successful!")
            st.rerun()

def render_basic_registration():
    """Basic registration form (fallback)"""
    with st.form("basic_registration_form"):
        username = st.text_input("👤 Username")
        email = st.text_input("📧 Email")
        password = st.text_input("🔒 Password", type="password")
        
        submitted = st.form_submit_button("📧 Register", use_container_width=True, type="primary")
        
        if submitted and username and email and password:
            st.session_state.authenticated_user = username
            st.success("✅ Registration successful!")
            st.rerun()

def calculate_password_strength(password):
    """Calculate password strength score"""
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
    return score

def logout_user():
    """Logout user and clear session"""
    if SECURE_AUTH_AVAILABLE and st.session_state.get("session_token"):
        st.session_state.user_authenticator.logout_user(st.session_state.session_token)
    
    # Clear session
    keys_to_clear = ["authenticated_user", "user_id", "session_token", "user_profile"]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    
    st.session_state.current_page = "Landing"
    st.rerun()

if __name__ == "__main__":
    main()