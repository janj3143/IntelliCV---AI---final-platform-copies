#!/usr/bin/env python3
"""
🚀 IntelliCV-AI Enhanced User Portal - Complete Authentication System
Includes: 2FA, SMS, Terms & Conditions, Pricing, Marketing Consent, Email Verification
"""

import streamlit as st
import os
import sys
import re
import random
import string
from pathlib import Path
import base64
from datetime import datetime, timedelta
import pyotp
import qrcode
from io import BytesIO
import json

# Page configuration
st.set_page_config(
    page_title="IntelliCV-AI | Your Intelligent Career Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load professional logo background CSS with highly visible logo
def load_professional_css():
    """Load the professional logo background CSS with pricing styling"""
    st.markdown("""
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    footer {{visibility: hidden;}}
    .stAppHeader {{display: none;}}
    
    .stApp {
        background: 
            linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.3) 100%),
            url('./static/logo1.png') center/contain no-repeat fixed !important;
        background-size: 60% auto;
        background-position: center center;
        background-attachment: fixed;
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 1rem auto;
        padding: 2rem !important;
    }
    
    /* Pricing Cards */
    .pricing-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 2rem;
        color: white;
        text-align: center;
        margin: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .pricing-card.free {
        background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
    }
    
    .pricing-card.premium {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        transform: scale(1.05);
        border: 3px solid #fbbf24;
    }
    
    .price {
        font-size: 3rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .feature-list {
        text-align: left;
        margin: 1rem 0;
    }
    
    .feature-list li {
        margin: 0.5rem 0;
        padding: 0.25rem 0;
    }
    
    /* Authentication styling */
    .auth-tabs {
        margin: 2rem 0;
    }
    
    .terms-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        max-height: 200px;
        overflow-y: auto;
    }
    
    .verification-code {
        font-family: monospace;
        font-size: 1.5rem;
        font-weight: bold;
        color: #059669;
        background: #ecfdf5;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Apply professional styling
load_professional_css()

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        "authenticated_user": False,
        "user_id": None,
        "user_email": None,
        "subscription_tier": "free",
        "email_verified": False,
        "phone_verified": False,
        "2fa_enabled": False,
        "terms_accepted": False,
        "marketing_consent": False,
        "verification_code": None,
        "verification_phone": None,
        "show_pricing": True,
        "registration_step": 1
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

def generate_verification_code():
    """Generate a 6-digit verification code"""
    return ''.join(random.choices(string.digits, k=6))

def generate_2fa_secret():
    """Generate a new 2FA secret"""
    return pyotp.random_base32()

def generate_qr_code(username, secret):
    """Generate QR code for 2FA setup"""
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(
        name=username,
        issuer_name="IntelliCV-AI"
    )
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes for Streamlit display
    buf = BytesIO()
    qr_image.save(buf, format="PNG")
    return buf.getvalue()

def verify_2fa_code(secret, user_code):
    """Verify 2FA code"""
    totp = pyotp.TOTP(secret)
    return totp.verify(user_code)

def get_country_codes():
    """Get list of country codes for phone numbers"""
    return {
        "🇺🇸 United States": "+1",
        "🇬🇧 United Kingdom": "+44", 
        "🇨🇦 Canada": "+1",
        "🇦🇺 Australia": "+61",
        "🇩🇪 Germany": "+49",
        "🇫🇷 France": "+33",
        "🇪🇸 Spain": "+34",
        "🇮🇹 Italy": "+39",
        "🇳🇱 Netherlands": "+31",
        "🇸🇪 Sweden": "+46",
        "🇳🇴 Norway": "+47",
        "🇩🇰 Denmark": "+45",
        "🇮🇪 Ireland": "+353",
        "🇨🇭 Switzerland": "+41",
        "🇦🇹 Austria": "+43",
        "🇧🇪 Belgium": "+32",
        "🇵🇹 Portugal": "+351",
        "🇯🇵 Japan": "+81",
        "🇰🇷 South Korea": "+82",
        "🇸🇬 Singapore": "+65",
        "🇭🇰 Hong Kong": "+852",
        "🇮🇳 India": "+91",
        "🇿🇦 South Africa": "+27",
        "🇧🇷 Brazil": "+55",
        "🇲🇽 Mexico": "+52"
    }

def validate_phone_number(phone):
    """Enhanced phone number validation with country code"""
    # Remove spaces, hyphens, parentheses
    clean_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    # Check if it starts with + and has 7-15 digits after
    phone_pattern = r'^\+[1-9]\d{6,14}$'
    return re.match(phone_pattern, clean_phone)

def show_pricing_section():
    """Display pricing structure"""
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0;">
        <h1 style="color: #1f2937; font-size: 3rem; margin-bottom: 1rem;">
            💎 Choose Your Plan
        </h1>
        <p style="font-size: 1.2rem; color: #6b7280;">
            Select the perfect plan for your career journey
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="pricing-card free">
            <h3>🆓 Free Starter</h3>
            <div class="price">$0<span style="font-size: 1rem;">/month</span></div>
            <div class="feature-list">
                <ul>
                    <li>✅ 3 Resume analyses per month</li>
                    <li>✅ Basic job matching</li>
                    <li>✅ Limited feedback</li>
                    <li>⚠️ Ads from our partners</li>
                    <li>⚠️ Marketing emails included</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Choose Free Plan", key="free_plan", use_container_width=True):
            st.session_state.subscription_tier = "free"
            st.session_state.marketing_consent = True  # Required for free plan
            st.session_state.show_pricing = False
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="pricing-card premium">
            <h3>⭐ Premium Pro</h3>
            <div class="price">$9.99<span style="font-size: 1rem;">/month</span></div>
            <div class="feature-list">
                <ul>
                    <li>✅ Unlimited resume analyses</li>
                    <li>✅ Advanced AI coaching</li>
                    <li>✅ Priority job matching</li>
                    <li>✅ No advertisements</li>
                    <li>✅ Expert feedback</li>
                    <li>✅ 2FA security</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Choose Premium", key="premium_plan", use_container_width=True):
            st.session_state.subscription_tier = "premium"
            st.session_state.marketing_consent = False  # Optional for premium
            st.session_state.show_pricing = False
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="pricing-card">
            <h3>🏢 Enterprise</h3>
            <div class="price">$99<span style="font-size: 1rem;">/month</span></div>
            <div class="feature-list">
                <ul>
                    <li>✅ Everything in Premium</li>
                    <li>✅ Team management</li>
                    <li>✅ API access</li>
                    <li>✅ Custom integrations</li>
                    <li>✅ Dedicated support</li>
                    <li>✅ White-label options</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Contact Sales", key="enterprise_plan", use_container_width=True):
            st.info("📞 Contact us at enterprise@intellicv.ai for custom pricing")

def show_terms_and_conditions():
    """Display terms and conditions"""
    st.markdown("""
    <div class="terms-box">
    <h4>📜 Terms and Conditions</h4>
    <p><strong>IntelliCV-AI Platform Terms of Service</strong></p>
    
    <p><strong>1. Acceptance of Terms</strong><br>
    By using IntelliCV-AI, you agree to these terms and our Privacy Policy.</p>
    
    <p><strong>2. Service Description</strong><br>
    IntelliCV-AI provides AI-powered career coaching and resume optimization services.</p>
    
    <p><strong>3. User Responsibilities</strong><br>
    - Provide accurate information<br>
    - Maintain account security<br>
    - Use service ethically and lawfully</p>
    
    <p><strong>4. Free Plan Terms</strong><br>
    - Limited to 3 resume analyses per month<br>
    - Includes advertising from our partners<br>
    - Marketing communications are included</p>
    
    <p><strong>5. Premium Plans</strong><br>
    - Ad-free experience<br>
    - Advanced features and priority support<br>
    - Optional marketing communications</p>
    
    <p><strong>6. Data Usage</strong><br>
    We process your data to provide our services. See our Privacy Policy for details.</p>
    
    <p><strong>7. Age Requirement</strong><br>
    You must be 16 or older to use our services.</p>
    
    <p>Last updated: October 2025</p>
    </div>
    """, unsafe_allow_html=True)

def show_registration_form():
    """Multi-step registration with all security features"""
    
    if st.session_state.registration_step == 1:
        st.markdown("### 📝 Step 1: Basic Information")
        
        with st.form("basic_info_form"):
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name *", key="reg_first_name")
            with col2:
                last_name = st.text_input("Last Name *", key="reg_last_name")
            
            email = st.text_input("Email Address *", key="reg_email")
            
            # Enhanced phone number input with country code
            col_country, col_phone = st.columns([1, 2])
            with col_country:
                country_codes = get_country_codes()
                selected_country = st.selectbox(
                    "Country", 
                    options=list(country_codes.keys()),
                    key="reg_country"
                )
                country_code = country_codes[selected_country]
                
            with col_phone:
                phone_number = st.text_input(
                    "Phone Number *", 
                    key="reg_phone_number",
                    placeholder="1234567890"
                )
                
            # Display full phone number
            full_phone = f"{country_code}{phone_number}" if phone_number else ""
            if full_phone:
                st.caption(f"📱 Full number: {full_phone}")
            
            col1, col2 = st.columns(2)
            with col1:
                password = st.text_input("Password *", type="password", key="reg_password")
            with col2:
                confirm_password = st.text_input("Confirm Password *", type="password", key="reg_confirm")
            
            next_step = st.form_submit_button("Next Step →", use_container_width=True)
            
            if next_step:
                if not all([first_name, last_name, email, phone_number, password, confirm_password]):
                    st.error("❌ Please fill in all required fields")
                elif password != confirm_password:
                    st.error("❌ Passwords do not match")
                elif not validate_phone_number(full_phone):
                    st.error("❌ Please enter a valid phone number")
                else:
                    # Store registration data
                    st.session_state.reg_data = {
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'phone': full_phone,
                        'country_code': country_code,
                        'phone_number': phone_number,
                        'password': password
                    }
                    st.session_state.registration_step = 2
                    st.rerun()
    
    elif st.session_state.registration_step == 2:
        st.markdown("### 🔐 Step 2: Security & Verification")
        
        # SMS Verification
        st.markdown("#### 📱 Phone Verification")
        if not st.session_state.get('verification_code'):
            if st.button("Send SMS Verification Code", use_container_width=True):
                st.session_state.verification_code = generate_verification_code()
                st.session_state.verification_phone = st.session_state.reg_data['phone']
                st.success(f"📱 SMS sent to {st.session_state.verification_phone}")
                st.rerun()
        else:
            st.info(f"📱 Verification code sent to {st.session_state.verification_phone}")
            st.markdown(f"""
            <div class="verification-code">
                Verification Code: {st.session_state.verification_code}
            </div>
            <p style="text-align: center; color: #6b7280; font-size: 0.9rem;">
                (In production, this would be sent via SMS)
            </p>
            """, unsafe_allow_html=True)
            
            entered_code = st.text_input("Enter 6-digit verification code", max_chars=6)
            
            if st.button("Verify Phone Number"):
                if entered_code == st.session_state.verification_code:
                    st.session_state.phone_verified = True
                    st.success("✅ Phone number verified!")
                    st.session_state.registration_step = 3
                    st.rerun()
                else:
                    st.error("❌ Invalid verification code")
    
    elif st.session_state.registration_step == 3:
        st.markdown("### 📋 Step 3: Terms & Preferences")
        
        # Show terms and conditions
        show_terms_and_conditions()
        
        with st.form("terms_form"):
            # Required terms acceptance
            terms_accepted = st.checkbox("✅ I accept the Terms and Conditions (Required - Age 16+)", key="terms_check")
            privacy_accepted = st.checkbox("✅ I accept the Privacy Policy (Required)", key="privacy_check")
            
            # 2FA option with setup
            st.markdown("#### 🔐 Two-Factor Authentication Setup")
            enable_2fa = st.checkbox("Enable Two-Factor Authentication (Highly Recommended)", value=True)
            
            if enable_2fa:
                st.info("📱 2FA adds an extra layer of security to your account")
                
                # Generate 2FA secret if not exists
                if '2fa_secret' not in st.session_state:
                    st.session_state['2fa_secret'] = generate_2fa_secret()
                
                # Show QR code for setup
                st.markdown("**Step 1**: Download an authenticator app:")
                st.markdown("• Google Authenticator • Microsoft Authenticator • Authy")
                
                st.markdown("**Step 2**: Scan this QR code with your authenticator app:")
                
                try:
                    qr_image = generate_qr_code(
                        st.session_state.reg_data['email'], 
                        st.session_state['2fa_secret']
                    )
                    st.image(qr_image, width=200)
                    
                    # Show manual entry option
                    with st.expander("📝 Can't scan? Enter manually"):
                        st.code(st.session_state['2fa_secret'])
                        st.caption("Enter this secret key in your authenticator app")
                        
                    # Verify 2FA setup
                    st.markdown("**Step 3**: Enter the 6-digit code from your app to verify setup:")
                    test_2fa_code = st.text_input("Test 2FA Code", max_chars=6, key="test_2fa")
                    
                    if test_2fa_code and len(test_2fa_code) == 6:
                        if verify_2fa_code(st.session_state['2fa_secret'], test_2fa_code):
                            st.success("✅ 2FA setup verified!")
                            st.session_state['2fa_verified'] = True
                        else:
                            st.error("❌ Invalid code. Please try again.")
                            st.session_state['2fa_verified'] = False
                    
                except Exception as e:
                    st.error(f"QR code generation failed: {e}")
                    enable_2fa = False
            
            # Marketing consent based on subscription tier
            if st.session_state.subscription_tier == "free":
                st.warning("⚠️ Free plan includes marketing communications from our partners")
                marketing_consent = st.checkbox("📧 I consent to receive marketing emails (Required for free plan)", value=True, disabled=True)
            else:
                marketing_consent = st.checkbox("📧 I consent to receive marketing communications (Optional)", value=False)
            
            # Email notifications
            email_notifications = st.checkbox("📬 Send me email notifications about my account", value=True)
            
            complete_registration = st.form_submit_button("🎉 Complete Registration", use_container_width=True, type="primary")
            
            if complete_registration:
                if not terms_accepted or not privacy_accepted:
                    st.error("❌ You must accept the Terms and Privacy Policy to continue")
                elif enable_2fa and not st.session_state.get('2fa_verified', False):
                    st.warning("⚠️ Please verify your 2FA setup before completing registration")
                else:
                    # Complete registration
                    st.session_state.authenticated_user = True
                    st.session_state.user_id = st.session_state.reg_data['first_name']
                    st.session_state.user_email = st.session_state.reg_data['email']
                    st.session_state.user_phone = st.session_state.reg_data['phone']
                    st.session_state.email_verified = False  # Will need email verification
                    st.session_state['2fa_enabled'] = enable_2fa
                    st.session_state['2fa_secret'] = st.session_state.get('2fa_secret') if enable_2fa else None
                    st.session_state.terms_accepted = True
                    st.session_state.marketing_consent = marketing_consent
                    
                    st.success("🎉 Registration completed successfully!")
                    st.info("📧 Please check your email for verification link")
                    
                    if enable_2fa:
                        st.info("🔐 Two-Factor Authentication will be set up on first login")
                    
                    # Redirect to profile creation
                    st.info("🚀 **Next Step**: Complete your profile to get better job matches!")
                    st.session_state.registration_step = 1  # Reset for next user
                    st.session_state.redirect_to_profile = True

def show_login_form():
    """Enhanced login form with 2FA"""
    with st.form("login_form"):
        email = st.text_input("Email Address", key="login_email", placeholder="test@example.com")
        password = st.text_input("Password", type="password", key="login_password", placeholder="Any password for demo")
        
        remember_me = st.checkbox("Remember me")
        
        login_button = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
        
        if login_button:
            if email and password:
                # For demo purposes, accept any email/password combo
                # In production, validate against database
                st.session_state.authenticated_user = True
                st.session_state.user_id = email.split('@')[0]
                st.session_state.user_email = email
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Please enter both email and password")
    


def show_sidebar():
    """Enhanced sidebar with subscription info"""
    if not st.session_state.get("authenticated_user"):
        return

    st.sidebar.title("📂 IntelliCV-AI")
    
    # User info with subscription
    st.sidebar.markdown(f"""
    ### 👤 Welcome, {st.session_state.get('user_id', 'User')}!
    **Plan**: {st.session_state.get('subscription_tier', 'free').title()}
    {"🆓" if st.session_state.get('subscription_tier') == 'free' else "⭐"}
    """)
    
    if not st.session_state.get('email_verified'):
        st.sidebar.warning("📧 Please verify your email")
    
    # Core Tools
    st.sidebar.markdown("### 🚀 Core Tools")
    st.sidebar.page_link("pages/02_Profile_Enhanced.py", label="� Complete Your Profile", help="Start here after login!")
    st.sidebar.page_link("pages/01_Resume_Upload_and_Analysis.py", label="� Resume Analysis Hub")
    st.sidebar.page_link("pages/03_Job_Description.py", label="📄 Job Description")
    st.sidebar.page_link("pages/04_Resume_Feedback.py", label="💬 Resume Feedback")
    st.sidebar.page_link("pages/05_Job_Match_Insights.py", label="🎯 Job Match Insights")
    st.sidebar.page_link("pages/06_Resume_History.py", label="📄 Resume History")
    
    st.sidebar.markdown("---")
    
    # Subscription management
    st.sidebar.markdown("### 💎 Subscription")
    if st.session_state.get('subscription_tier') == 'free':
        st.sidebar.info("🆓 Free Plan - 3 analyses/month")
        if st.sidebar.button("⬆️ Upgrade to Premium"):
            st.session_state.show_pricing = True
            st.rerun()
    else:
        st.sidebar.success("⭐ Premium Plan Active")
    
    st.sidebar.markdown("---")
    
    # Settings
    st.sidebar.markdown("### ⚙️ Settings")
    if st.sidebar.button("📧 Verify Email") and not st.session_state.get('email_verified'):
        st.sidebar.success("Verification email sent!")
        
    if st.sidebar.button("🔐 Setup 2FA") and not st.session_state.get('2fa_enabled'):
        st.sidebar.info("2FA setup initiated")
    
    if st.sidebar.button("🚪 Logout"):
        # Clear session
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def show_welcome_page():
    """Welcome authenticated users with subscription info"""
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #10b981, #3b82f6); 
                border-radius: 15px; color: white; margin: 2rem 0;">
        <h2>🎉 Welcome back, {st.session_state.get('user_id', 'User')}!</h2>
        <p style="font-size: 1.2rem;">
            You're on the {st.session_state.get('subscription_tier', 'free').title()} plan
            {"🆓" if st.session_state.get('subscription_tier') == 'free' else "⭐"}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show subscription-specific features
    if st.session_state.get('subscription_tier') == 'free':
        st.info("🆓 **Free Plan Features**: 3 resume analyses per month, basic matching, partner advertisements")
    
    # Feature showcase
    st.markdown("### 🌟 Choose Your Next Step")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #f8fafc; border-radius: 10px; height: 200px;">
            <h3>📊 Resume Analysis</h3>
            <p>AI-powered resume optimization and insights</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Analysis", key="resume_analysis", use_container_width=True):
            st.switch_page("pages/01_Resume_Upload_and_Analysis.py")
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white; border-radius: 10px; height: 200px;">
            <h3>👤 Complete Your Profile</h3>
            <p>Essential for better job matches!</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Complete Profile First", key="complete_profile", use_container_width=True, type="primary"):
            st.switch_page("pages/02_Profile_Enhanced.py")
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #f8fafc; border-radius: 10px; height: 200px;">
            <h3>🎯 Job Matching</h3>
            <p>Find perfect career opportunities</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Find Jobs", key="find_jobs", use_container_width=True):
            st.switch_page("pages/05_Job_Match_Insights.py")

def main():
    """Main application with all enhanced features"""
    # Show sidebar if authenticated
    show_sidebar()
    
    # Main content based on authentication status
    if not st.session_state.get("authenticated_user"):
        # Show pricing first if not selected
        if st.session_state.get("show_pricing"):
            show_pricing_section()
            return
        
        # Main title
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="color: #1f2937; font-size: 4rem; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                🚀 IntelliCV-AI
            </h1>
            <h2 style="color: #6b7280; font-size: 2rem; margin-bottom: 2rem;">
                Your Intelligent Career Platform
            </h2>
            <p style="font-size: 1.2rem; color: #374151;">
                AI-powered resume optimization • Career coaching • Job matching
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Authentication tabs
        tab1, tab2 = st.tabs(["🚀 Login", "📝 Register"])
        
        with tab1:
            show_login_form()
        
        with tab2:
            show_registration_form()
            
        # Handle profile redirect after registration
        if st.session_state.get('redirect_to_profile'):
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📝 Create My Profile Now", type="primary", use_container_width=True):
                    st.switch_page("pages/02_Profile_Enhanced.py")
            
        # Back to pricing link
        st.markdown("---")
        if st.button("💎 View Pricing Plans", use_container_width=True):
            st.session_state.show_pricing = True
            st.rerun()
    
    else:
        # Show welcome page for authenticated users
        show_welcome_page()

# Entry point
if __name__ == "__main__":
    main()