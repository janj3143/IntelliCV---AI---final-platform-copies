"""
IntelliCV-AI Welcome & Home Page
==================================
Entry point to the IntelliCV-AI platform featuring:
- IntelliCV logo (60% width) - static on home, 30% on other pages
- Key USPs and product highlights  
- Four pricing tiers:
  • Free: Token-based with CV upload, limited chatbot, basic AI
  • Monthly $9.99: Enhanced options, no career/interview coach
  • Annual $149.99: Full suite including coaches & multi-CV
  • Super-User $299: Everything + 1-on-1 mentorship (mentor revenue share model)
- Login and Registration options
- Integration with admin payment system (Stripe, Google Pay, etc.)
- New registrations directed to Payment page (02_Payment.py)
"""

import streamlit as st
from pathlib import Path
import base64
import sys
import os
import time
from datetime import datetime
from typing import Dict, List, Optional

# Setup paths and imports
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

# Import utilities with fallbacks
try:
    from fragments.sidebar import show_sidebar
    SIDEBAR_AVAILABLE = True
except ImportError:
    SIDEBAR_AVAILABLE = False

try:
    from utils.error_handler import handle_exceptions, log_user_action, show_error, show_success
    ERROR_HANDLER_AVAILABLE = True
except ImportError:
    ERROR_HANDLER_AVAILABLE = False
    # Fallback functions
    def handle_exceptions(func):
        return func
    def log_user_action(action, details=None):
        pass
    def show_error(msg, details=None):
        st.error(f"❌ {msg}")
    def show_success(msg, details=None):
        st.success(f"✅ {msg}")

try:
    from auth.sandbox_secure_auth import SandboxUserAuthenticator
    ENHANCED_AUTH_AVAILABLE = True
except ImportError:
    ENHANCED_AUTH_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="🏠 IntelliCV-AI | Smart Resume Intelligence",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize sidebar if available
if SIDEBAR_AVAILABLE:
    try:
        show_sidebar()
    except Exception as e:
        pass

# Initialize session state
if 'page_visited' not in st.session_state:
    st.session_state.page_visited = 'home'
if 'selected_plan' not in st.session_state:
    st.session_state.selected_plan = None

# Load logo with error handling
@st.cache_data
def load_logo_b64() -> str:
    """Load and cache logo with error handling."""
    try:
        p = Path(__file__).parent.parent / "static" / "logo.png"
        if p.exists():
            return base64.b64encode(p.read_bytes()).decode()
        else:
            # Try alternative locations
            alt_paths = [
                Path(__file__).parent / "static" / "logo.png",
                Path(__file__).parent.parent / "assets" / "logo.png"
            ]
            for alt_p in alt_paths:
                if alt_p.exists():
                    return base64.b64encode(alt_p.read_bytes()).decode()
        return ""
    except Exception as e:
        if ERROR_HANDLER_AVAILABLE:
            log_user_action("missing_asset", {"asset": "logo.png", "error": str(e)})
        return ""

logo_b64 = load_logo_b64()

# Professional CSS styling
def load_professional_css():
    """Load comprehensive professional CSS"""
    css = f'''
    <style>
    /* Main App Background - Clean gradient only */
    .stApp {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.5) 0%, rgba(118, 75, 162, 0.5) 100%);
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* Main Container */
    .main .block-container {{
        background: rgba(255,255,255,0.97) !important;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        margin-top: 1rem;
        backdrop-filter: blur(10px);
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
    }}
    
    /* Welcome Header */
    .welcome-header {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }}
    
    .welcome-header h1 {{
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    
    .welcome-header p {{
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }}
    
    /* Feature Cards */
    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }}
    
    .feature-card {{
        background: white;
        padding: 1.8rem;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-left-color: #764ba2;
    }}
    
    .feature-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        opacity: 0;
        transition: opacity 0.3s ease;
    }}
    
    .feature-card:hover::before {{
        opacity: 1;
    }}
    
    /* USP Scrollable List */
    .usp-list {{
        max-height: 35vh;
        overflow-y: auto;
        background: #fff;
        padding: 1.5rem;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        color: #111;
        font-size: 1.1rem;
        scrollbar-width: thin;
        scrollbar-color: #667eea #f1f1f1;
    }}
    
    .usp-list::-webkit-scrollbar {{
        width: 8px;
    }}
    
    .usp-list::-webkit-scrollbar-track {{
        background: #f1f1f1;
        border-radius: 4px;
    }}
    
    .usp-list::-webkit-scrollbar-thumb {{
        background: #667eea;
        border-radius: 4px;
    }}
    
    .usp-list::-webkit-scrollbar-thumb:hover {{
        background: #764ba2;
    }}
    
    /* Login Card */
    .login-card {{
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }}
    
    /* Pricing Cards - Updated for three column layout */
    .pricing-card {{
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
    }}
    
    .pricing-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }}
    
    .pricing-card.featured {{
        border-color: #667eea;
        transform: scale(1.02);
    }}
    
    .pricing-card.featured::before {{
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
    }}
    
    .pricing-card.featured h3 {{
        margin-top: 2rem;
    }}
    
    .price {{
        font-size: 2.2rem;
        font-weight: bold;
        color: #667eea;
        margin: 1rem 0;
    }}
    
    .price-period {{
        font-size: 1rem;
        color: #666;
        font-weight: normal;
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }}
    
    /* Input Fields */
    .stTextInput > div > div > input {{
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s ease;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab"] {{
        background: #f8f9fa;
        border-radius: 8px 8px 0 0;
        padding: 0.75rem 1.5rem;
        margin-right: 0.5rem;
        font-weight: 600;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }}
    
    /* Status Messages */
    .stSuccess, .stError, .stWarning, .stInfo {{
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }}
    
    /* Hide Streamlit Elements */
    #MainMenu, footer, header {{
        visibility: hidden;
    }}
    
    /* Logo column styling */
    .logo-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 300px;
        background: rgba(255,255,255,0.9);
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding: 1rem;
        }}
        
        .welcome-header {{
            padding: 1.5rem;
        }}
        
        .welcome-header h1 {{
            font-size: 2rem;
        }}
        
        .feature-grid {{
            grid-template-columns: 1fr;
        }}
        
        .login-card {{
            padding: 1.5rem;
        }}
        
        .logo-container {{
            height: 200px;
        }}
    }}
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

# Load CSS
load_professional_css()

# Log page access
if ERROR_HANDLER_AVAILABLE:
    log_user_action("page_view", {"page": "home", "timestamp": datetime.now().isoformat()})

# Welcome Header
st.markdown('''
<div class="welcome-header">
    <h1>🚀 Welcome to IntelliCV-AI</h1>
    <p>Transform Your Career with Intelligent Resume Technology</p>
</div>
''', unsafe_allow_html=True)

# HERO SECTION - Dominating logo display
st.markdown('<div style="text-align: center; margin: 2rem 0 3rem 0;">', unsafe_allow_html=True)
if logo_b64:
    st.markdown(f'''
    <div class="hero-logo-container" style="text-align: center; padding: 1rem;">
        <img src="data:image/png;base64,{logo_b64}" 
             style="width: 85%; max-width: 900px; height: auto; object-fit: contain; margin: 0 auto;" 
             alt="IntelliCV-AI - AI-Powered Career Platform">
    </div>
    ''', unsafe_allow_html=True)
else:
    st.markdown('''
    <div class="hero-logo-fallback" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; text-align: center; padding: 4rem 2rem; border-radius: 30px; margin: 0 auto; max-width: 900px;">
        <div>
            <h1 style="font-size: 6rem; margin: 0;">🚀</h1>
            <h2 style="font-size: 3.5rem; margin: 1rem 0; font-weight: 700;">IntelliCV-AI</h2>
            <p style="font-size: 1.8rem; opacity: 0.9;">AI-Powered Career Intelligence Platform</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Main content layout - Content left, Login right (logo now above)
content_col, login_col = st.columns([2.5, 1.5], gap="large")

# Content column (middle)
with content_col:
    st.markdown("### 💡 Why IntelliCV-AI is Unlike Anything Else")
    
    # POWERFUL USPs - highlighting unique 8-factor AI and real human mentorship
    key_usps = [
        "🧠 **8-Factor AI Engine** - Our proprietary AI analyzes your career from 8 unique dimensions. No one else does this. We craft and shape your resume with unmatched precision to dramatically improve your chances of landing your next role.",
        
        "📊 **Peer Benchmarking & Gap Analysis** - See exactly how you stack up against your peers. Identify what you need to get ahead and get actionable steps to close the gap.",
        
        "🎯 **Optimized Career Coaching** - Not just AI, but REAL PEOPLE. Executive-level mentors who've seen it, done it, across ALL sectors and job levels. They're incentivized to help YOU succeed.",
        
        "💼 **Flexible Mentorship Programs** - Your mentor, your deal. They set their rates, you negotiate. Pay only for the time you need. No one else offers this level of personalized, human connection.",
        
        "💎 **Become a Mentor & Earn Equity** - We reward YOU too! Join as a mentor and earn through our unique development program. Offer new ideas and we don't just pay for them - we offer **fractional shares of the entire platform**. Imagine we go public and you helped us become the #1 industry leader. Your input becomes worth real money. But don't hesitate - those fractional shares get diluted as we grow. Early contributors earn the biggest rewards!",
        
        "🗺️ **Location & Industry Mapping** - Find companies, jobs, and crossover functions you never knew existed. Flip your career trajectory with intelligent geographic and role mapping.",
        
        "🎤 **Interview Coaching That Works** - Real preparation from people who've conducted thousands of interviews. Not generic tips - specific, role-based, industry-specific coaching.",
        
        "🔗 **Smart Integrations** - Yes, we integrate with LinkedIn and major platforms. But unlike others, we USE that data to give you optimized career tips, not just import it.",
        
        "🔒 **Enterprise Security & Privacy** - Your data is yours. Bank-level encryption, GDPR compliant, with complete control over who sees what."
    ]
    
    # Display USPs with better formatting
    st.markdown('<div class="usp-list" style="line-height: 1.8;">', unsafe_allow_html=True)
    for usp in key_usps:
        st.markdown(f"{usp}")
        st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)  # Small spacer
    st.markdown("</div>", unsafe_allow_html=True)

# Login column (right)
with login_col:
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # Check authentication status
    if st.session_state.get('authenticated_user'):
        st.success(f"✅ Welcome back, **{st.session_state['authenticated_user']}**!")
        
        # Quick action buttons
        st.markdown("### 🚀 Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📄 Upload Resume", use_container_width=True):
                try:
                    st.switch_page("pages/01_Resume_Upload_and_Analysis.py")
                except:
                    show_error("Upload page not available")
                    
        with col2:
            if st.button("🎯 Job Match", use_container_width=True):
                try:
                    st.switch_page("pages/05_Job_Match_Insights.py") 
                except:
                    show_error("Job Match page not available")
            
        # Small visual spacer (no line)
        st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)
        
        # User info and logout
        user_role = st.session_state.get('user_role', 'user')
        st.info(f"👤 **Role:** {user_role.title()}")
        
        if st.button("🚪 Logout", use_container_width=True):
            # Clear session
            keys_to_clear = ['authenticated_user', 'user_role', 'session_token', 'user_email']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            
            if ERROR_HANDLER_AVAILABLE:
                log_user_action("user_logout", {"page": "home"})
            
            show_success("Successfully logged out!")
            time.sleep(1)
            st.rerun()
    
    else:
        # Simple Login/Register buttons
        st.markdown("### 🔐 Access Your Account")
        
        # Main action buttons
        if st.button("🔑 Login", use_container_width=True, type="primary"):
            st.session_state['show_login'] = True
            st.session_state['show_register'] = False
            st.rerun()
            
        if st.button("🆕 Create Account", use_container_width=True):
            # Redirect to registration page
            st.switch_page("01_Registration.py")
        
        # Login form (dropdown)
        if st.session_state.get('show_login', False):
            with st.expander("🔐 Login Form", expanded=True):
                with st.form("login_form"):
                    username = st.text_input("Username", placeholder="Enter your username")
                    password = st.text_input("Password", type="password", placeholder="Enter your password")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("🔑 Login", use_container_width=True):
                            if username and password:
                                # Demo credentials check
                                if username == "admin" and password == "admin123":
                                    st.session_state['authenticated_user'] = username
                                    st.session_state['user_role'] = 'admin'
                                    st.session_state['user_email'] = 'admin@intellicv.ai'
                                elif username == "Janatmainswood@gmail.com" and password == "janj@3143@?":
                                    st.session_state['authenticated_user'] = "Jan Atmainswood"
                                    st.session_state['user_role'] = 'user'
                                    st.session_state['user_email'] = username
                                else:
                                    st.session_state['authenticated_user'] = username
                                    st.session_state['user_role'] = 'user'
                                    st.session_state['user_email'] = username
                                
                                st.session_state['session_token'] = f"token_{int(time.time())}"
                                st.session_state['is_new_user'] = False
                                st.session_state['show_login'] = False
                                
                                show_success("Login successful! Redirecting...")
                                if ERROR_HANDLER_AVAILABLE:
                                    log_user_action("user_login", {"username": username})
                                time.sleep(1)
                                st.switch_page("pages/03_Profile_Setup.py")
                            else:
                                show_error("Please enter both username and password")
                    
                    with col2:
                        if st.form_submit_button("❌ Cancel", use_container_width=True):
                            st.session_state['show_login'] = False
                            st.rerun()
                
                # Demo info
                st.info("💡 **Demo Login:**\n- Admin: 'admin' / 'admin123'\n- User: 'Janatmainswood@gmail.com' / 'janj@3143@?'\n- Or use any username/password for generic user access")

    
    st.markdown('</div>', unsafe_allow_html=True)

# Pricing Section - Four plans side by side underneath main content
st.markdown('<div style="height: 3rem;"></div>', unsafe_allow_html=True)  # Spacer instead of line
st.markdown("## 💰 Choose Your Plan")
st.markdown("Select the plan that best fits your career goals:")

# Four column pricing layout
price_col1, price_col2, price_col3, price_col4 = st.columns(4, gap="small")

with price_col1:
    st.markdown('''
    <div class="pricing-card">
        <h3>🆓 Free</h3>
        <div class="price">FREE</div>
        <p style="text-align: center; color: #666; font-size: 0.85rem;">Limited Token-Based Access</p>
        <ul style="text-align: left; padding-left: 1rem; margin: 1rem 0; font-size: 0.85rem;">
            <li>Upload CV (we want that data!)</li>
            <li>Profile access</li>
            <li>Limited Chatbot</li>
            <li>Basic AI from Career Intelligence Suite</li>
            <li>Truncated career options</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("🚀 Start Free", key="free_plan", use_container_width=True):
        st.session_state['selected_plan'] = 'free'
        st.switch_page("pages/02_Payment.py")

with price_col2:
    st.markdown('''
    <div class="pricing-card">
        <h3>⭐ Monthly</h3>
        <div class="price">$9.99<span class="price-period">/mo</span></div>
        <p style="text-align: center; color: #666; font-size: 0.85rem;">Enhanced Career Tools</p>
        <ul style="text-align: left; padding-left: 1rem; margin: 1rem 0; font-size: 0.85rem;">
            <li>All Free features</li>
            <li>Increased AI options</li>
            <li>More career intelligence</li>
            <li>❌ No Career Coach</li>
            <li>❌ No Interview Coach</li>
            <li>❌ No Multi-CV autogenerate</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("⭐ Choose Monthly", key="monthly_plan", use_container_width=True):
        st.session_state['selected_plan'] = 'monthly'
        st.switch_page("pages/02_Payment.py")

with price_col3:
    st.markdown('''
    <div class="pricing-card featured">
        <h3>🏆 Annual</h3>
        <div class="price">$149.99<span class="price-period">/yr</span></div>
        <p style="text-align: center; color: #666; font-size: 0.85rem;">Complete Career Suite</p>
        <ul style="text-align: left; padding-left: 1rem; margin: 1rem 0; font-size: 0.85rem;">
            <li>All Monthly features</li>
            <li>✅ Career Coach</li>
            <li>✅ Interview Coach</li>
            <li>✅ Multi-CV autogenerate & send</li>
            <li>✅ Full Career Intelligence</li>
            <li>❌ No Mentorship Support</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("🏆 Choose Annual", key="annual_plan", use_container_width=True, type="primary"):
        st.session_state['selected_plan'] = 'annual'
        st.switch_page("pages/02_Payment.py")

with price_col4:
    st.markdown('''
    <div class="pricing-card">
        <h3>👑 Super-User</h3>
        <div class="price">$299<span class="price-period">/yr</span></div>
        <p style="text-align: center; color: #666; font-size: 0.85rem;">Premium + Mentorship</p>
        <ul style="text-align: left; padding-left: 1rem; margin: 1rem 0; font-size: 0.85rem;">
            <li>Everything in Annual</li>
            <li>✅ <strong>1-on-1 Mentorship Access</strong></li>
            <li>✅ Connect with industry mentors</li>
            <li>✅ Personalized career guidance</li>
            <li>💡 Mentors earn revenue share</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("👑 Choose Super-User", key="superuser_plan", use_container_width=True):
        st.session_state['selected_plan'] = 'superuser'
        st.switch_page("pages/02_Payment.py")

# Footer section
st.markdown('<div style="height: 3rem;"></div>', unsafe_allow_html=True)  # Spacer instead of line
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>IntelliCV-AI</strong> | Powered by Advanced AI Technology</p>
    <p>🔒 Your data is secure • 🌍 Available worldwide • 📞 24/7 Support</p>
    <p style="font-size: 0.85rem; margin-top: 1rem;">Payment powered by Stripe, Google Pay, and more | Admin portal integration</p>
</div>
""", unsafe_allow_html=True)