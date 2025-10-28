"""
🆕 IntelliCV-AI Registration Page
================================
Step 1: Account Creation + Plan Selection
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

# Load logo with error handling
@st.cache_data
def load_logo_b64() -> str:
    """Load and cache logo with multiple fallback paths for 30% display"""
    try:
        import base64
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
    page_title="🆕 Registration | IntelliCV-AI",
    page_icon="🆕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS styling
def load_registration_css():
    """Load registration page specific CSS"""
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
        max-width: 1000px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Header styling */
    .registration-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    .registration-header h1 {
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Registration form card */
    .registration-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    
    /* Pricing Cards */
    .pricing-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        height: 100%;
        min-height: 300px;
    }
    
    .pricing-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .pricing-card.featured {
        border-color: #667eea;
        transform: scale(1.02);
    }
    
    .pricing-card.featured::before {
        content: 'MOST POPULAR';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .pricing-card.featured h3 {
        margin-top: 2rem;
    }
    
    .pricing-card.selected {
        border-color: #28a745;
        background: rgba(40, 167, 69, 0.05);
    }
    
    .price {
        font-size: 2.2rem;
        font-weight: bold;
        color: #667eea;
        margin: 1rem 0;
    }
    
    .price-period {
        font-size: 1rem;
        color: #666;
        font-weight: normal;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
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
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

# Load CSS
load_registration_css()

# Render 30% logo
render_page_logo()

# Log page access
if ERROR_HANDLER_AVAILABLE:
    log_user_action("page_view", {"page": "registration", "timestamp": datetime.now().isoformat()})

# Progress steps
st.markdown('''
<div class="progress-steps">
    <div class="step active">1. Registration</div>
    <div class="step">2. Payment</div>
    <div class="step">3. Profile Setup</div>
</div>
''', unsafe_allow_html=True)

# Header
st.markdown('''
<div class="registration-header">
    <h1>🚀 Join IntelliCV-AI</h1>
    <p>Create your account and choose your plan to get started</p>
</div>
''', unsafe_allow_html=True)

# Back to home button in sidebar
with st.sidebar:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("pages/00_Home.py")
    
    st.markdown("---")
    st.markdown("### 📋 Registration Steps")
    st.markdown("""
    1. **Create Account** - Fill in your details
    2. **Choose Plan** - Select your subscription
    3. **Payment** - Complete your purchase
    4. **Profile Setup** - Customize your experience
    """)

# Main registration content
col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.markdown('<div class="registration-card">', unsafe_allow_html=True)
    st.markdown("### 👤 Create Your Account")
    
    with st.form("registration_form"):
        # Personal information
        st.markdown("**Personal Information**")
        col_a, col_b = st.columns(2)
        
        with col_a:
            first_name = st.text_input("First Name *", placeholder="John")
            username = st.text_input("Username *", max_chars=30, placeholder="Choose username")
            
        with col_b:
            last_name = st.text_input("Last Name *", placeholder="Doe")
            email = st.text_input("Email *", max_chars=100, placeholder="john@example.com")
        
        st.markdown("**Security**")
        col_c, col_d = st.columns(2)
        
        with col_c:
            password = st.text_input("Password *", type="password", max_chars=100, placeholder="Secure password (6+ chars)")
            
        with col_d:
            confirm_pass = st.text_input("Confirm Password *", type="password", max_chars=100, placeholder="Confirm password")
        
        st.markdown("**Preferences**")
        col_e, col_f = st.columns(2)
        
        with col_e:
            industry = st.selectbox("Industry", [
                "Technology", "Healthcare", "Finance", "Education", "Marketing", 
                "Sales", "Engineering", "Design", "Management", "Other"
            ])
            newsletter = st.checkbox("📧 Career Tips Newsletter")
            
        with col_f:
            experience_level = st.selectbox("Experience Level", [
                "Entry Level (0-2 years)", "Mid Level (3-5 years)", 
                "Senior Level (6-10 years)", "Executive (10+ years)"
            ])
            notifications = st.checkbox("🔔 Job Match Alerts")
        
        # Terms and conditions
        st.markdown("---")
        agree_terms = st.checkbox("✅ I agree to the Terms of Service and Privacy Policy *", value=False)
        
        # Form submission
        col_submit, col_cancel = st.columns(2)
        
        with col_submit:
            submitted = st.form_submit_button("🚀 Create Account & Continue", use_container_width=True, type="primary")
            
        with col_cancel:
            if st.form_submit_button("❌ Cancel", use_container_width=True):
                st.switch_page("pages/00_Home.py")
        
        # Form validation and processing
        if submitted:
            # Validation
            required_fields = [first_name, last_name, username, email, password, confirm_pass]
            if not all(required_fields):
                show_error("Please fill in all required fields marked with *")
            elif password != confirm_pass:
                show_error("Passwords don't match")
            elif len(password) < 6:
                show_error("Password must be at least 6 characters")
            elif not agree_terms:
                show_error("Please accept Terms of Service and Privacy Policy")
            elif "@" not in email or "." not in email:
                show_error("Please enter a valid email address")
            else:
                # Store registration data in session
                st.session_state['registration_data'] = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username,
                    'email': email,
                    'password': password,
                    'industry': industry,
                    'experience_level': experience_level,
                    'newsletter': newsletter,
                    'notifications': notifications,
                    'timestamp': datetime.now().isoformat()
                }
                
                show_success("✅ Account details validated! Now choose your plan below...")
                if ERROR_HANDLER_AVAILABLE:
                    log_user_action("registration_step1_completed", {"username": username, "email": email})
                
                # Enable plan selection
                st.session_state['registration_step1_complete'] = True
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Quick stats or benefits
    st.markdown("### 🌟 Why Join IntelliCV-AI?")
    
    benefits = [
        "🎯 **AI-Powered Matching** - Get matched with relevant jobs instantly",
        "📄 **Smart Resume Builder** - Create compelling resumes in minutes", 
        "📊 **Career Analytics** - Track your job search progress",
        "🚀 **Interview Prep** - AI-powered interview coaching",
        "🔒 **Secure & Private** - Your data is protected and encrypted",
        "📱 **Mobile Ready** - Access from anywhere, anytime"
    ]
    
    for benefit in benefits:
        st.markdown(f"• {benefit}")
    
    st.markdown("---")
    st.markdown("### 📞 Need Help?")
    st.info("Questions about registration? Contact our support team at support@intellicv-ai.com")

# Plan selection section (only show if step 1 is complete)
if st.session_state.get('registration_step1_complete', False):
    st.markdown("---")
    st.markdown("## 💰 Choose Your Plan")
    st.markdown("Select the plan that best fits your career goals:")
    
    # Three column pricing layout
    price_col1, price_col2, price_col3 = st.columns(3, gap="medium")
    
    selected_plan = st.session_state.get('selected_plan', None)
    
    with price_col1:
        card_class = "pricing-card selected" if selected_plan == 'free' else "pricing-card"
        st.markdown(f'''
        <div class="{card_class}">
            <h3>🆓 Free Trial</h3>
            <div class="price">FREE</div>
            <p style="text-align: center; color: #666;">Perfect for testing our platform</p>
            <ul style="text-align: left; padding-left: 1rem; margin: 1rem 0;">
                <li>3 Resume generations</li>
                <li>Basic job matching</li>
                <li>Standard templates</li>
                <li>Email support</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("🚀 Select Free Trial", key="select_free", use_container_width=True):
            st.session_state['selected_plan'] = 'free'
            st.session_state['plan_price'] = 0
            st.rerun()
    
    with price_col2:
        card_class = "pricing-card featured selected" if selected_plan == 'monthly' else "pricing-card featured"
        st.markdown(f'''
        <div class="{card_class}">
            <h3>⭐ Monthly Pro</h3>
            <div class="price">$9.99<span class="price-period">/month</span></div>
            <p style="text-align: center; color: #666;">Most popular choice for job seekers</p>
            <ul style="text-align: left; padding-left: 1rem; margin: 1rem 0; min-height: 120px;">
                <li>Unlimited resume generations</li>
                <li>Advanced AI job matching</li>
                <li>Premium templates</li>
                <li>Priority support</li>
                <li>LinkedIn integration</li>
                <li>Application tracking</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("⭐ Select Monthly Pro", key="select_monthly", use_container_width=True, type="primary"):
            st.session_state['selected_plan'] = 'monthly'
            st.session_state['plan_price'] = 9.99
            st.rerun()
    
    with price_col3:
        card_class = "pricing-card selected" if selected_plan == 'annual' else "pricing-card"
        st.markdown(f'''
        <div class="{card_class}">
            <h3>🏆 Annual Pro</h3>
            <div class="price">$89.99<span class="price-period">/year</span></div>
            <p style="text-align: center; color: #666;">Best value - Save $30!</p>
            <ul style="text-align: left; padding-left: 1rem; margin: 1rem 0; min-height: 120px;">
                <li>Everything in Monthly Pro</li>
                <li>Career workbook generator</li>
                <li>Industry insights</li>
                <li>1-on-1 career consultation</li>
                <li>Early access to new features</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("🏆 Select Annual Pro", key="select_annual", use_container_width=True):
            st.session_state['selected_plan'] = 'annual'
            st.session_state['plan_price'] = 89.99
            st.rerun()
    
    # Proceed to payment button
    if selected_plan:
        st.markdown("---")
        plan_names = {'free': 'Free Trial', 'monthly': 'Monthly Pro ($9.99/month)', 'annual': 'Annual Pro ($89.99/year)'}
        st.success(f"✅ Selected: **{plan_names[selected_plan]}**")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("💳 Proceed to Payment", use_container_width=True, type="primary"):
                # Store final selection
                st.session_state['registration_data']['selected_plan'] = selected_plan
                st.session_state['registration_data']['plan_price'] = st.session_state.get('plan_price', 0)
                
                if ERROR_HANDLER_AVAILABLE:
                    log_user_action("plan_selected", {"plan": selected_plan, "price": st.session_state.get('plan_price', 0)})
                
                # Redirect to payment page
                st.switch_page("pages/02_Payment.py")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>IntelliCV-AI</strong> | Secure Registration Process</p>
    <p>🔒 Your data is encrypted • 📞 24/7 Support • 💳 Secure Payment Processing</p>
</div>
""", unsafe_allow_html=True)