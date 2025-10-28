""""""

🏠 IntelliCV-AI Welcome & Home Page🏠 IntelliCV-AI Welcome & Home Page

====================================================================

Complete welcome experience with:Complete welcome experience with:

- IntelliCV logo (60% width)- IntelliCV logo (60% width)

- Key USPs and product highlights  - Key USPs and product highlights  

- Payment plans: Free → Monthly ($9.99) → Annual ($149.99) → Super-User ($299)- Payment plans: Free → Monthly ($9.99) → Annual ($149.99) → Super-User ($299)

- Login and Registration options- Login and Registration options

- Links to admin payment system (Stripe, Google Pay, etc.)- Professional design with admin AI integration

""""""



import streamlit as stimport streamlit as st

from pathlib import Pathfrom pathlib import Path

import base64import base64

import sysimport sys

import osimport os

import timeimport time

from datetime import datetimefrom datetime import datetime

from typing import Dict, List, Optionalfrom typing import Dict, List, Optional



# Setup paths and imports# Setup paths and imports

current_dir = Path(__file__).parent.parentcurrent_dir = Path(__file__).parent.parent

sys.path.insert(0, str(current_dir))sys.path.insert(0, str(current_dir))



# Import utilities with fallbacks# Import utilities with fallbacks

try:try:

    from utils.error_handler import handle_exceptions, log_user_action, show_error, show_success    from fragments.sidebar import show_sidebar

    ERROR_HANDLER_AVAILABLE = True    SIDEBAR_AVAILABLE = True

except ImportError:except ImportError:

    ERROR_HANDLER_AVAILABLE = False    SIDEBAR_AVAILABLE = False

    def handle_exceptions(func):

        return functry:

    def log_user_action(action, details=None):    from utils.error_handler import handle_exceptions, log_user_action, show_error, show_success

        pass    ERROR_HANDLER_AVAILABLE = True

    def show_error(msg, details=None):except ImportError:

        st.error(f"❌ {msg}")    ERROR_HANDLER_AVAILABLE = False

    def show_success(msg, details=None):    # Fallback functions

        st.success(f"✅ {msg}")    def handle_exceptions(func):

        return func

try:    def log_user_action(action, details=None):

    from shared_infrastructure_final.admin_ai_integration import init_admin_ai_for_user_page        pass

    ADMIN_AI_AVAILABLE = True    def show_error(msg, details=None):

except ImportError:        st.error(f"❌ {msg}")

    ADMIN_AI_AVAILABLE = False    def show_success(msg, details=None):

        st.success(f"✅ {msg}")

# Page configuration

st.set_page_config(try:

    page_title="🏠 IntelliCV-AI | AI-Powered Career Intelligence Platform",    from auth.sandbox_secure_auth import SandboxUserAuthenticator

    page_icon="🚀",    ENHANCED_AUTH_AVAILABLE = True

    layout="wide",except ImportError:

    initial_sidebar_state="collapsed",    ENHANCED_AUTH_AVAILABLE = False

    menu_items={

        'Get Help': None,# Page configuration

        'Report a bug': None,st.set_page_config(

        'About': "IntelliCV-AI - Transform your career with AI-powered intelligence and professional mentorship."    page_title="🏠 IntelliCV-AI | Smart Resume Intelligence",

    }    page_icon="🏠",

)    layout="wide",

    initial_sidebar_state="expanded"

# Initialize session state)

if 'page_visited' not in st.session_state:

    st.session_state.page_visited = 'home'# Initialize sidebar if available

if 'selected_plan' not in st.session_state:if SIDEBAR_AVAILABLE:

    st.session_state.selected_plan = None    try:

        show_sidebar()

# Load logo with error handling    except Exception as e:

@st.cache_data        pass

def load_logo_b64() -> str:

    """Load and cache logo with multiple fallback paths"""# Load logo with error handling

    try:@st.cache_data

        logo_paths = [def load_logo_b64() -> str:

            Path(__file__).parent.parent / "static" / "logo.png",    """Load and cache logo with error handling."""

            Path(__file__).parent.parent / "static" / "logo1.png",    try:

            Path(__file__).parent.parent / "assets" / "logo.png",        p = Path(__file__).parent.parent / "static" / "logo.png"

            Path(__file__).parent / "static" / "logo.png"        if p.exists():

        ]            return base64.b64encode(p.read_bytes()).decode()

                else:

        for logo_path in logo_paths:            # Try alternative locations

            if logo_path.exists():            alt_paths = [

                return base64.b64encode(logo_path.read_bytes()).decode()                Path(__file__).parent / "static" / "logo.png",

                        Path(__file__).parent.parent / "assets" / "logo.png"

        return None            ]

    except Exception as e:            for alt_p in alt_paths:

        if ERROR_HANDLER_AVAILABLE:                if alt_p.exists():

            log_user_action("logo_load_error", {"error": str(e)})                    return base64.b64encode(alt_p.read_bytes()).decode()

        return None        return ""

    except Exception as e:

def load_welcome_css():        if ERROR_HANDLER_AVAILABLE:

    """Load comprehensive CSS for welcome page"""            log_user_action("missing_asset", {"asset": "logo.png", "error": str(e)})

    css = '''        return ""

    <style>

    /* =================================logo_b64 = load_logo_b64()

       HIDE STREAMLIT ELEMENTS

       ================================= */# Professional CSS styling

    #MainMenu {visibility: hidden;}def load_professional_css():

    .stDeployButton {display: none;}    """Load comprehensive professional CSS"""

    footer {visibility: hidden;}    css = f'''

    .stAppHeader {display: none;}    <style>

    header[data-testid="stHeader"] {display: none;}    /* Main App Background - Clean gradient only */

        .stApp {{

    /* =================================        background: linear-gradient(135deg, rgba(102, 126, 234, 0.5) 0%, rgba(118, 75, 162, 0.5) 100%);

       MAIN APP BACKGROUND        background-size: cover;

       ================================= */        background-position: center;

    .stApp {        background-repeat: no-repeat;

        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);        background-attachment: fixed;

    }    }}

        

    .main .block-container {    /* Main Container */

        padding-top: 1rem;    .main .block-container {{

        max-width: 1400px;        background: rgba(255,255,255,0.97) !important;

        margin: 0 auto;        padding: 2rem;

    }        border-radius: 12px;

            box-shadow: 0 8px 24px rgba(0,0,0,0.15);

    /* =================================        margin-top: 1rem;

       LOGO CONTAINER (60% WIDTH)        backdrop-filter: blur(10px);

       ================================= */        max-width: 1200px;

    .logo-container {        margin-left: auto;

        text-align: center;        margin-right: auto;

        padding: 3rem 2rem;    }}

        margin-bottom: 2rem;    

        background: white;    /* Welcome Header */

        border-radius: 20px;    .welcome-header {{

        box-shadow: 0 10px 40px rgba(0,0,0,0.1);        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

    }        color: white;

            padding: 2.5rem;

    .logo-container img {        border-radius: 12px;

        width: 60%;        text-align: center;

        max-width: 500px;        margin-bottom: 2rem;

        height: auto;        box-shadow: 0 6px 20px rgba(0,0,0,0.2);

        margin-bottom: 1.5rem;    }}

        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));    

    }    .welcome-header h1 {{

            font-size: 2.5rem;

    .logo-container h1 {        margin-bottom: 0.5rem;

        color: #667eea;        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);

        font-size: 3rem;    }}

        margin: 1rem 0;    

        font-weight: 700;    .welcome-header p {{

        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);        font-size: 1.2rem;

        -webkit-background-clip: text;        opacity: 0.9;

        -webkit-text-fill-color: transparent;        margin: 0;

        background-clip: text;    }}

    }    

        /* Feature Cards */

    .logo-container .tagline {    .feature-grid {{

        color: #666;        display: grid;

        font-size: 1.4rem;        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));

        margin: 1rem 0;        gap: 1.5rem;

        font-weight: 300;        margin: 2rem 0;

    }    }}

        

    .logo-container .subtitle {    .feature-card {{

        color: #888;        background: white;

        font-size: 1rem;        padding: 1.8rem;

        margin: 0;        border-radius: 12px;

    }        border-left: 5px solid #667eea;

            box-shadow: 0 4px 16px rgba(0,0,0,0.1);

    /* =================================        transition: all 0.3s ease;

       USP SECTION        position: relative;

       ================================= */        overflow: hidden;

    .usp-header {    }}

        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);    

        color: white;    .feature-card:hover {{

        padding: 3rem 2rem;        transform: translateY(-5px);

        border-radius: 20px;        box-shadow: 0 8px 25px rgba(0,0,0,0.15);

        text-align: center;        border-left-color: #764ba2;

        margin: 3rem 0;    }}

        box-shadow: 0 10px 40px rgba(0,0,0,0.2);    

    }    .feature-card::before {{

            content: '';

    .usp-header h2 {        position: absolute;

        font-size: 2.5rem;        top: 0;

        margin-bottom: 1rem;        left: 0;

        font-weight: 700;        right: 0;

    }        height: 3px;

            background: linear-gradient(90deg, #667eea, #764ba2);

    .usp-header p {        opacity: 0;

        font-size: 1.2rem;        transition: opacity 0.3s ease;

        opacity: 0.9;    }}

        margin: 0;    

    }    .feature-card:hover::before {{

            opacity: 1;

    .usp-grid {    }}

        display: grid;    

        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));    /* USP Scrollable List */

        gap: 2rem;    .usp-list {{

        margin: 3rem 0;        max-height: 35vh;

    }        overflow-y: auto;

            background: #fff;

    .usp-card {        padding: 1.5rem;

        background: white;        border: 1px solid #e0e0e0;

        padding: 2rem;        border-radius: 10px;

        border-radius: 15px;        box-shadow: 0 4px 12px rgba(0,0,0,0.08);

        box-shadow: 0 8px 30px rgba(0,0,0,0.1);        color: #111;

        border-left: 6px solid #667eea;        font-size: 1.1rem;

        transition: all 0.3s ease;        scrollbar-width: thin;

        position: relative;        scrollbar-color: #667eea #f1f1f1;

        overflow: hidden;    }}

    }    

        .usp-list::-webkit-scrollbar {{

    .usp-card:hover {        width: 8px;

        transform: translateY(-5px);    }}

        box-shadow: 0 15px 50px rgba(0,0,0,0.15);    

    }    .usp-list::-webkit-scrollbar-track {{

            background: #f1f1f1;

    .usp-card::before {        border-radius: 4px;

        content: '';    }}

        position: absolute;    

        top: 0;    .usp-list::-webkit-scrollbar-thumb {{

        right: 0;        background: #667eea;

        width: 100px;        border-radius: 4px;

        height: 100px;    }}

        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));    

        border-radius: 0 15px 0 100px;    .usp-list::-webkit-scrollbar-thumb:hover {{

    }        background: #764ba2;

        }}

    .usp-card h3 {    

        color: #667eea;    /* Login Card */

        margin-bottom: 1rem;    .login-card {{

        font-size: 1.4rem;        background: white;

        font-weight: 600;        padding: 2rem;

        position: relative;        border-radius: 12px;

        z-index: 1;        box-shadow: 0 6px 20px rgba(0,0,0,0.1);

    }        border: 1px solid #e0e0e0;

        }}

    .usp-card p {    

        color: #555;    /* Pricing Cards - Updated for three column layout */

        line-height: 1.7;    .pricing-card {{

        margin: 0;        background: white;

        position: relative;        padding: 1.5rem;

        z-index: 1;        border-radius: 12px;

    }        text-align: center;

            box-shadow: 0 4px 16px rgba(0,0,0,0.1);

    /* =================================        border: 2px solid #e0e0e0;

       PAYMENT PLANS SECTION        transition: all 0.3s ease;

       ================================= */        position: relative;

    .pricing-section {        overflow: hidden;

        background: #f8f9fa;        height: 100%;

        padding: 4rem 2rem;        min-height: 300px;

        border-radius: 20px;    }}

        margin: 4rem 0;    

        box-shadow: 0 10px 40px rgba(0,0,0,0.05);    .pricing-card:hover {{

    }        transform: translateY(-5px);

            box-shadow: 0 8px 25px rgba(0,0,0,0.15);

    .pricing-header {    }}

        text-align: center;    

        margin-bottom: 4rem;    .pricing-card.featured {{

    }        border-color: #667eea;

            transform: scale(1.02);

    .pricing-header h2 {    }}

        color: #333;    

        font-size: 2.5rem;    .pricing-card.featured::before {{

        margin-bottom: 1rem;        content: 'MOST POPULAR';

        font-weight: 700;        position: absolute;

    }        top: 0;

            left: 0;

    .pricing-header p {        right: 0;

        color: #666;        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

        font-size: 1.2rem;        color: white;

        margin: 0;        padding: 0.5rem;

    }        font-size: 0.8rem;

            font-weight: bold;

    .pricing-grid {    }}

        display: grid;    

        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));    .pricing-card.featured h3 {{

        gap: 2.5rem;        margin-top: 2rem;

        max-width: 1300px;    }}

        margin: 0 auto;    

    }    .price {{

            font-size: 2.2rem;

    .pricing-card {        font-weight: bold;

        background: white;        color: #667eea;

        border-radius: 20px;        margin: 1rem 0;

        padding: 2.5rem;    }}

        text-align: center;    

        box-shadow: 0 10px 40px rgba(0,0,0,0.1);    .price-period {{

        border: 3px solid transparent;        font-size: 1rem;

        transition: all 0.4s ease;        color: #666;

        position: relative;        font-weight: normal;

        overflow: hidden;    }}

    }    

        /* Buttons */

    .pricing-card:hover {    .stButton > button {{

        transform: translateY(-8px);        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

        box-shadow: 0 20px 60px rgba(0,0,0,0.15);        color: white;

    }        border: none;

            border-radius: 8px;

    .pricing-card.popular {        padding: 0.75rem 1.5rem;

        border-color: #667eea;        font-weight: 600;

        transform: scale(1.05);        transition: all 0.3s ease;

        background: linear-gradient(135deg, #f8f9ff 0%, #fff 100%);        box-shadow: 0 3px 10px rgba(0,0,0,0.2);

        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.2);    }}

    }    

        .stButton > button:hover {{

    .pricing-card.premium {        transform: translateY(-2px);

        border-color: #ffd700;        box-shadow: 0 5px 15px rgba(0,0,0,0.3);

        background: linear-gradient(135deg, #fffbf0 0%, #fff 100%);    }}

        box-shadow: 0 15px 50px rgba(255, 215, 0, 0.2);    

    }    /* Input Fields */

        .stTextInput > div > div > input {{

    .popular-badge, .premium-badge {        border-radius: 8px;

        position: absolute;        border: 2px solid #e0e0e0;

        top: -15px;        transition: border-color 0.3s ease;

        left: 50%;    }}

        transform: translateX(-50%);    

        padding: 0.7rem 1.5rem;    .stTextInput > div > div > input:focus {{

        border-radius: 25px;        border-color: #667eea;

        font-size: 0.9rem;        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);

        font-weight: bold;    }}

        box-shadow: 0 4px 15px rgba(0,0,0,0.2);    

    }    /* Tabs */

        .stTabs [data-baseweb="tab"] {{

    .popular-badge {        background: #f8f9fa;

        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);        border-radius: 8px 8px 0 0;

        color: white;        padding: 0.75rem 1.5rem;

    }        margin-right: 0.5rem;

            font-weight: 600;

    .premium-badge {    }}

        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);    

        color: #333;    .stTabs [aria-selected="true"] {{

    }        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

            color: white;

    .plan-name {    }}

        font-size: 1.6rem;    

        font-weight: bold;    /* Status Messages */

        color: #333;    .stSuccess, .stError, .stWarning, .stInfo {{

        margin-bottom: 1rem;        border-radius: 8px;

    }        padding: 1rem;

            margin: 1rem 0;

    .plan-price {    }}

        font-size: 3rem;    

        font-weight: bold;    /* Hide Streamlit Elements */

        color: #667eea;    #MainMenu, footer, header {{

        margin-bottom: 0.5rem;        visibility: hidden;

    }    }}

        

    .plan-price.premium-price {    /* Logo column styling */

        color: #ffd700;    .logo-container {{

    }        display: flex;

            justify-content: center;

    .plan-period {        align-items: center;

        font-size: 1rem;        height: 300px;

        color: #666;        background: rgba(255,255,255,0.9);

        margin-bottom: 2rem;        border-radius: 12px;

    }        box-shadow: 0 4px 16px rgba(0,0,0,0.1);

            margin-bottom: 1rem;

    .plan-features {    }}

        text-align: left;    

        margin: 2rem 0;    /* Responsive Design */

        min-height: 250px;    @media (max-width: 768px) {{

    }        .main .block-container {{

                padding: 1rem;

    .plan-features ul {        }}

        list-style: none;        

        padding: 0;        .welcome-header {{

        margin: 0;            padding: 1.5rem;

    }        }}

            

    .plan-features li {        .welcome-header h1 {{

        padding: 0.7rem 0;            font-size: 2rem;

        border-bottom: 1px solid #f0f0f0;        }}

        color: #555;        

        font-size: 0.95rem;        .feature-grid {{

    }            grid-template-columns: 1fr;

            }}

    .plan-features li:last-child {        

        border-bottom: none;        .login-card {{

    }            padding: 1.5rem;

            }}

    .plan-features .highlight {        

        color: #667eea;        .logo-container {{

        font-weight: 600;            height: 200px;

    }        }}

        }}

    .plan-features .exclusive {    </style>

        color: #ffd700;    '''

        font-weight: 600;    st.markdown(css, unsafe_allow_html=True)

    }

    # Load CSS

    .mentorship-info {load_professional_css()

        background: linear-gradient(135deg, #e8f5e8 0%, #f0fff0 100%);

        padding: 2rem;# Log page access

        border-radius: 15px;if ERROR_HANDLER_AVAILABLE:

        margin: 3rem 0;    log_user_action("page_view", {"page": "home", "timestamp": datetime.now().isoformat()})

        border-left: 6px solid #28a745;

        text-align: center;# Welcome Header

    }st.markdown('''

    <div class="welcome-header">

    .mentorship-info h4 {    <h1>🚀 Welcome to IntelliCV-AI</h1>

        color: #28a745;    <p>Transform Your Career with Intelligent Resume Technology</p>

        margin-bottom: 1rem;</div>

        font-size: 1.3rem;''', unsafe_allow_html=True)

    }

    # Main content layout - Logo left, content center, login right

    .mentorship-info p {logo_col, content_col, login_col = st.columns([1, 2, 1.2], gap="medium")

        color: #555;

        margin: 0.5rem 0;# Logo column (left)

    }with logo_col:

        if logo_b64:

    .payment-methods {        st.markdown(f'''

        background: white;        <div class="logo-container">

        padding: 2rem;            <img src="data:image/png;base64,{logo_b64}" 

        border-radius: 15px;                 style="max-width: 90%; max-height: 250px; object-fit: contain;" 

        margin: 2rem 0;                 alt="IntelliCV-AI Logo">

        box-shadow: 0 8px 30px rgba(0,0,0,0.1);        </div>

        text-align: center;        ''', unsafe_allow_html=True)

    }    else:

            st.markdown('''

    /* =================================        <div class="logo-container" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 

       AUTH SECTION                    color: white; text-align: center;">

       ================================= */            <div>

    .auth-section {                <h2>🚀</h2>

        background: white;                <h3>IntelliCV-AI</h3>

        padding: 3rem 2rem;                <p>AI-Powered</p>

        border-radius: 20px;            </div>

        box-shadow: 0 10px 40px rgba(0,0,0,0.1);        </div>

        margin: 3rem 0;        ''', unsafe_allow_html=True)

    }

    # Content column (middle)

    .auth-header {with content_col:

        text-align: center;    st.markdown("### 💡 Why Choose IntelliCV-AI?")

        margin-bottom: 2rem;    

    }    # Enhanced USP list with comprehensive features

        comprehensive_usps = [

    .auth-header h2 {        "🚀 **Smart Resume Builder** - Create targeted resumes instantly with AI guidance",

        color: #667eea;        "📈 **AI Job Matching** - See compatibility scores with transparent AI analysis",  

        font-size: 2rem;        "🧠 **Real-Time Feedback** - Get actionable improvement suggestions, not just scores",

        margin-bottom: 1rem;        "🌟 **STAR Story Generator** - Transform experiences into compelling recruiter stories",

    }        "📊 **Visual Resume Insights** - Understand keyword strength and recruiter perspective",

            "🛠️ **One-Click Optimization** - Export perfectly tailored resume versions",

    /* =================================        "📬 **Application Tracker** - Monitor your applications and their status",

       RESPONSIVE DESIGN        "🔗 **LinkedIn Integration** - Import and enhance your existing profile",

       ================================= */        "🎯 **Keyword Discovery** - Find and integrate in-demand industry terms",

    @media (max-width: 768px) {        "📁 **Career Workbook** - Auto-generate personalized career development guides",

        .main .block-container {        "🧩 **Industry Glossary** - Access built-in terminology and skill databases",

            padding: 1rem 0.5rem;        "🌐 **ATS Optimization** - Ensure compatibility with applicant tracking systems",

        }        "📱 **Mobile Responsive** - Access your tools anywhere, anytime",

                "🔒 **Secure & Private** - Your data protected with enterprise-grade security",

        .logo-container img {        "🎨 **Professional Templates** - Choose from industry-specific design options"

            width: 80%;    ]

        }    

            # Scrollable USP container

        .logo-container h1 {    st.markdown('<div class="usp-list">', unsafe_allow_html=True)

            font-size: 2.2rem;    for usp in comprehensive_usps:

        }        st.markdown(f"• {usp}")

            st.markdown("</div>", unsafe_allow_html=True)

        .pricing-card.popular {

            transform: none;# Login column (right)

        }with login_col:

            st.markdown('<div class="login-card">', unsafe_allow_html=True)

        .plan-price {    

            font-size: 2.2rem;    # Check authentication status

        }    if st.session_state.get('authenticated_user'):

                st.success(f"✅ Welcome back, **{st.session_state['authenticated_user']}**!")

        .usp-header h2 {        

            font-size: 2rem;        # Quick action buttons

        }        st.markdown("### 🚀 Quick Actions")

                

        .pricing-header h2 {        col1, col2 = st.columns(2)

            font-size: 2rem;        with col1:

        }            if st.button("📄 Upload Resume", use_container_width=True):

    }                try:

    </style>                    st.switch_page("pages/01_Resume_Upload_and_Analysis.py")

    '''                except:

    st.markdown(css, unsafe_allow_html=True)                    show_error("Upload page not available")

                    

# Load CSS        with col2:

load_welcome_css()            if st.button("🎯 Job Match", use_container_width=True):

                try:

def render_logo_section():                    st.switch_page("pages/05_Job_Match_Insights.py") 

    """Render the main logo section (60% width)"""                except:

    logo_b64 = load_logo_b64()                    show_error("Job Match page not available")

            

    if logo_b64:        st.markdown("---")

        st.markdown(f'''        

        <div class="logo-container">        # User info and logout

            <img src="data:image/png;base64,{logo_b64}" alt="IntelliCV-AI Logo">        user_role = st.session_state.get('user_role', 'user')

            <h1>IntelliCV-AI</h1>        st.info(f"👤 **Role:** {user_role.title()}")

            <p class="tagline">AI-Powered Career Intelligence Platform</p>        

            <p class="subtitle">Transform your career with intelligent automation</p>        if st.button("🚪 Logout", use_container_width=True):

        </div>            # Clear session

        ''', unsafe_allow_html=True)            keys_to_clear = ['authenticated_user', 'user_role', 'session_token', 'user_email']

    else:            for key in keys_to_clear:

        st.markdown('''                if key in st.session_state:

        <div class="logo-container">                    del st.session_state[key]

            <div style="font-size: 4rem; margin-bottom: 1rem;">🚀</div>            

            <h1>IntelliCV-AI</h1>            if ERROR_HANDLER_AVAILABLE:

            <p class="tagline">AI-Powered Career Intelligence Platform</p>                log_user_action("user_logout", {"page": "home"})

            <p class="subtitle">Transform your career with intelligent automation</p>            

        </div>            show_success("Successfully logged out!")

        ''', unsafe_allow_html=True)            time.sleep(1)

            st.rerun()

def render_usp_section():    

    """Render key USPs and product highlights"""    else:

    st.markdown('''        # Simple Login/Register buttons

    <div class="usp-header">        st.markdown("### 🔐 Access Your Account")

        <h2>🌟 Transform Your Career with AI Intelligence</h2>        

        <p>Join thousands of professionals who've advanced their careers with our comprehensive AI-powered platform</p>        # Main action buttons

    </div>        if st.button("� Login", use_container_width=True, type="primary"):

    ''', unsafe_allow_html=True)            st.session_state['show_login'] = True

                st.session_state['show_register'] = False

    # USP Grid            st.rerun()

    st.markdown('''            

    <div class="usp-grid">        if st.button("🆕 Create Account", use_container_width=True):

        <div class="usp-card">            # Redirect to registration page

            <h3>🧠 Advanced 6-System AI</h3>            st.switch_page("01_Registration.py")

            <p>Our proprietary AI coordination combines NLP, Bayesian analysis, LLM processing, Neural networks, Expert systems, and Statistical modeling for unmatched career intelligence and resume optimization.</p>        

        </div>        # Login form (dropdown)

                if st.session_state.get('show_login', False):

        <div class="usp-card">            with st.expander("🔐 Login Form", expanded=True):

            <h3>📄 Enhanced Job Title Engine</h3>                with st.form("login_form"):

            <p>422 lines of sophisticated LinkedIn integration creates industry-perfect resumes that get noticed by recruiters, ATS systems, and hiring managers across all sectors.</p>                    username = st.text_input("Username", placeholder="Enter your username")

        </div>                    password = st.text_input("Password", type="password", placeholder="Enter your password")

                            

        <div class="usp-card">                    col1, col2 = st.columns(2)

            <h3>📊 Real AI Data Connector</h3>                    with col1:

            <p>Live processing of 3,418+ JSON data sources provides current salary insights, skill trends, market intelligence, and competitive positioning for informed career decisions.</p>                        if st.form_submit_button("🔑 Login", use_container_width=True):

        </div>                            if username and password:

                                        # Demo credentials check

        <div class="usp-card">                                if username == "admin" and password == "admin123":

            <h3>🎯 Intelligent Career Positioning</h3>                                    st.session_state['authenticated_user'] = username

            <p>Get personalized career analysis, skill gap identification, and growth recommendations based on real-time market data and industry-specific intelligence.</p>                                    st.session_state['user_role'] = 'admin'

        </div>                                else:

                                            st.session_state['authenticated_user'] = username

        <div class="usp-card">                                    st.session_state['user_role'] = 'user'

            <h3>🚀 Profile Optimization Suite</h3>                                

            <p>Transform your professional presence with AI-powered suggestions, keyword optimization, and industry-specific enhancements that maximize your visibility.</p>                                st.session_state['session_token'] = f"token_{int(time.time())}"

        </div>                                st.session_state['is_new_user'] = False

                                        st.session_state['show_login'] = False

        <div class="usp-card">                                

            <h3>🤝 Expert Mentorship Network</h3>                                show_success("Login successful! Redirecting...")

            <p>Connect with verified industry professionals for personalized guidance, interview coaching, career strategy, and networking opportunities at the highest levels.</p>                                if ERROR_HANDLER_AVAILABLE:

        </div>                                    log_user_action("user_login", {"username": username})

    </div>                                time.sleep(1)

    ''', unsafe_allow_html=True)                                st.switch_page("pages/03_Profile_Setup.py")

                            else:

def render_pricing_section():                                show_error("Please enter both username and password")

    """Render payment plans: Free → Monthly ($9.99) → Annual ($149.99) → Super-User ($299)"""                    

                        with col2:

    st.markdown('''                        if st.form_submit_button("❌ Cancel", use_container_width=True):

    <div class="pricing-section">                            st.session_state['show_login'] = False

        <div class="pricing-header">                            st.rerun()

            <h2>💰 Choose Your Career Intelligence Plan</h2>                

            <p>Start free, scale as your career grows, unlock premium mentorship</p>                # Demo info

        </div>                st.info("💡 **Demo:** Use 'admin'/'admin123' for admin access, or any username/password for user access")

                

        <div class="pricing-grid">

            <!-- FREE PLAN -->    

            <div class="pricing-card">    st.markdown('</div>', unsafe_allow_html=True)

                <div class="plan-name">🆓 Free Starter</div>

                <div class="plan-price">FREE</div># Pricing Section - Three plans side by side underneath main content

# Pricing Section - Clean implementation
st.markdown("---")
st.markdown("## 💰 Choose Your Plan")
st.markdown("Select the plan that best fits your career goals:")

# Pricing toggle - Payment Plans vs Token Plans
col_toggle1, col_toggle2, col_toggle3 = st.columns([1, 2, 1])
with col_toggle2:
    pricing_mode = st.toggle("🔄 Switch to Token-Based Pricing", key="pricing_toggle")
    if pricing_mode:
        st.info("💡 **Token Mode**: Pay for exactly what you use - perfect for power users!")
    else:
        st.info("📅 **Subscription Mode**: Predictable monthly/annual billing - most popular!")

# Three column pricing layout
price_col1, price_col2, price_col3 = st.columns(3, gap="medium")

with price_col1:

    if not pricing_mode:
        # SUBSCRIPTION MODE - Traditional Payment Plans
        st.markdown('''
        <div class="pricing-card">
            <h3>🆓 Free Starter</h3>
            <div class="price">FREE</div>
            <p style="text-align: center; color: #666;">Limited access • We value your data!</p>
            <ul style="text-align: left; padding-left: 1rem; margin: 1rem 0;">
                <li>✅ Upload 1 CV (Get resume précis)</li>
                <li>✅ Upload 1 Job Application (See peer comparison)</li>
                <li>✅ View Job Adverts (Required for job uploads)</li>
                <li>✅ Basic Career Insights</li>
                <li>✅ Community Access</li>
                <li>❌ Multiple CV generations</li>
                <li>❌ Full Job Suite access</li>
                <li>❌ Personal Branding Suite</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    else:
        # TOKEN MODE - Flexible Usage-Based
        st.markdown('''
        <div class="pricing-card">
            <h3>🆓 Free Starter</h3>
            <div class="price">FREE</div>
            <div class="token-badge" style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.9rem; margin: 0.5rem 0;">10 Tokens/Month</div>
            <p style="text-align: center; color: #666;">Limited access • We value your data!</p>
            <ul style="text-align: left; padding-left: 1rem; margin: 1rem 0;">
                <li>✅ CV Analysis (3 tokens)</li>
                <li>✅ Job Comparison (5 tokens)</li>
                <li>✅ Career Insights (2 tokens)</li>
                <li>✅ Community Access (Free)</li>
                <li>❌ Advanced AI features</li>
                <li>❌ Personal Branding Suite</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    
    if st.button("🚀 Start Free Trial", key="free_trial", use_container_width=True):
        st.session_state['selected_plan'] = 'free'
        st.session_state['pricing_mode'] = 'tokens' if pricing_mode else 'subscription'
        st.switch_page("pages/01_Registration.py")

with price_col2:

    if not pricing_mode:
        # SUBSCRIPTION MODE - Traditional Payment Plans  
        st.markdown('''
        <div class="pricing-card featured" style="border: 2px solid #667eea; transform: scale(1.05);">
            <div style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 0.3rem 0.8rem; border-radius: 15px 15px 0 0; margin: -1rem -1rem 1rem -1rem; text-align: center; font-weight: bold;">⭐ MOST POPULAR</div>
            <h3>⭐ Monthly Pro</h3>
            <div class="price">$15.99<span class="price-period">/month</span></div>
            <p style="text-align: center; color: #666;">Full Job Suite access (no Personal Branding)</p>
            <ul style="text-align: left; padding-left: 1rem; margin: 1rem 0;">
                <li>✅ Everything in Free Starter</li>
                <li>✅ Unlimited CV uploads & analysis</li>
                <li>✅ Advanced AI job matching</li>
                <li>✅ LinkedIn integration</li>
                <li>✅ Application tracking</li>
                <li>✅ Interview preparation tools</li>
                <li>❌ Personal Branding Suite</li>
                <li>❌ Career Coaching</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    else:
        # TOKEN MODE - Flexible Usage-Based
        st.markdown('''
        <div class="pricing-card featured" style="border: 2px solid #667eea; transform: scale(1.05);">
            <div style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 0.3rem 0.8rem; border-radius: 15px 15px 0 0; margin: -1rem -1rem 1rem -1rem; text-align: center; font-weight: bold;">⭐ MOST POPULAR</div>
            <h3>⭐ Monthly Pro</h3>
            <div class="price">$15.99<span class="price-period">/month</span></div>
            <div class="token-badge" style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.9rem; margin: 0.5rem 0;">100 Tokens/Month</div>
            <p style="text-align: center; color: #666;">Full Job Suite • No Personal Branding</p>
            <ul style="text-align: left; padding-left: 1rem; margin: 1rem 0;">
                <li>✅ CV Analysis (2 tokens each)</li>
                <li>✅ AI Job Matching (5 tokens/search)</li>
                <li>✅ LinkedIn Sync (3 tokens)</li>
                <li>✅ Interview Prep (5 tokens/session)</li>
                <li>✅ Application Tracking (1 token/app)</li>
                <li>❌ Personal Branding (10+ tokens)</li>
                <li>❌ Career Coaching (50+ tokens)</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    
    if st.button("⭐ Choose Monthly Pro", key="monthly_pro", use_container_width=True, type="primary"):
        st.session_state['selected_plan'] = 'monthly'
        st.session_state['pricing_mode'] = 'tokens' if pricing_mode else 'subscription'
        st.switch_page("pages/01_Registration.py")

with price_col3:

    if not pricing_mode:
        # SUBSCRIPTION MODE - Traditional Payment Plans
        st.markdown('''
        <div class="pricing-card">
            <h3>🏆 Annual Pro</h3>
            <div class="price">$149.99<span class="price-period">/year</span></div>
            <p style="text-align: center; color: #666;">Everything + Personal Branding Suite</p>
            <ul style="text-align: left; padding-left: 1rem; margin: 1rem 0;">
                <li>✅ Everything in Monthly Pro</li>
                <li>✅ <strong>Personal Branding Suite</strong></li>
                <li>✅ LinkedIn profile optimization</li>
                <li>✅ Personal website builder</li>
                <li>✅ Content calendar creation</li>
                <li>✅ Advanced analytics dashboard</li>
                <li>✅ Industry intelligence reports</li>
                <li>❌ Career Coaching & Mentorship</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    else:
        # TOKEN MODE - Flexible Usage-Based
        st.markdown('''
        <div class="pricing-card">
            <h3>🏆 Annual Pro</h3>
            <div class="price">$149.99<span class="price-period">/year</span></div>
            <div class="token-badge" style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.9rem; margin: 0.5rem 0;">250 Tokens/Month</div>
            <p style="text-align: center; color: #666;">All features + Personal Branding Suite</p>
            <ul style="text-align: left; padding-left: 1rem; margin: 1rem 0;">
                <li>✅ Everything from Monthly Pro</li>
                <li>✅ Personal Brand Analysis (10 tokens)</li>
                <li>✅ LinkedIn Optimization (8 tokens)</li>
                <li>✅ Website Builder (15 tokens)</li>
                <li>✅ Content Calendar (5 tokens)</li>
                <li>✅ Analytics Reports (5 tokens)</li>
                <li>❌ Career Coaching (50+ tokens)</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    
    if st.button("🏆 Choose Annual Pro", key="annual_pro", use_container_width=True):
        st.session_state['selected_plan'] = 'annual'
        st.session_state['pricing_mode'] = 'tokens' if pricing_mode else 'subscription'
        st.switch_page("pages/01_Registration.py")

# Add fourth column for Enterprise (optional)
st.markdown("---")
enterprise_col1, enterprise_col2, enterprise_col3 = st.columns([1, 2, 1])
with enterprise_col2:

                if st.button("🏆 Choose Annual Pro", key="annual_pro", use_container_width=True):

            <!-- SUPER-USER PLAN -->        st.session_state['selected_plan'] = 'annual'

            <div class="pricing-card premium">        st.switch_page("pages/01_Registration.py")

                <div class="premium-badge">Premium Elite</div>

                <div class="plan-name">🌟 Super-User</div># Enhanced App Content - Only show for new users

                <div class="plan-price premium-price">$299</div>if st.session_state.get('is_new_user', False) and not st.session_state.get('authenticated_user'):

                <div class="plan-period">per year • Full platform access + Revenue</div>    st.markdown("---")

                <div class="plan-features">    st.markdown("### 🌟 Enhanced Features for New Users")

                    <ul>    

                        <li>✅ <strong>Everything in Annual Pro</strong></li>    # Feature cards for new users

                        <li>✅ <span class="exclusive">Personal Mentorship Support</span></li>    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)

                        <li>✅ <span class="exclusive">1-on-1 Career Coaching</span></li>    

                        <li>✅ <span class="exclusive">Interview Coaching Sessions</span></li>    features = [

                        <li>✅ <span class="exclusive">Direct Mentor Access</span></li>        {

                        <li>✅ <span class="exclusive">Become a Mentor</span> (Earn revenue!)</li>            "icon": "🎯",

                        <li>✅ <span class="exclusive">80% Revenue Share</span></li>            "title": "Smart Targeting",

                        <li>✅ <span class="exclusive">White-glove Service</span></li>            "description": "AI analyzes job descriptions and optimizes your resume for maximum impact"

                        <li>✅ <span class="exclusive">Custom AI Training</span></li>        },

                        <li>✅ <span class="exclusive">VIP Support Channel</span></li>        {

                    </ul>            "icon": "⚡",

                </div>            "title": "Lightning Fast",

            </div>            "description": "Generate professional resumes in seconds, not hours"

        </div>        },

                {

        <div class="mentorship-info">            "icon": "📊", 

            <h4>🎯 Super-User Mentorship Revenue Model</h4>            "title": "Data-Driven",

            <p><strong>Earn while you help others advance their careers!</strong></p>            "description": "Make informed decisions with comprehensive analytics and insights"

            <p>• Become a verified mentor and charge for your services</p>        },

            <p>• Keep 80% of all mentorship fees (we take 20% platform fee)</p>        {

            <p>• Set your own rates for premium consulting</p>            "icon": "🔧",

            <p>• Access to mentor-only revenue opportunities</p>            "title": "Fully Customizable", 

            <p>• All mentorship services vetted by our platform for quality assurance</p>            "description": "Tailor every aspect to match your industry and personal brand"

        </div>        }

    </div>    ]

    ''', unsafe_allow_html=True)    

        for feature in features:

    # Payment plan selection buttons        st.markdown(f'''

    st.markdown("### 🚀 Select Your Plan & Get Started")        <div class="feature-card">

                <h3>{feature["icon"]} {feature["title"]}</h3>

    col1, col2, col3, col4 = st.columns(4)            <p>{feature["description"]}</p>

            </div>

    with col1:        ''', unsafe_allow_html=True)

        if st.button("🆓 Start Free Now", use_container_width=True, type="secondary"):    

            st.session_state['selected_plan'] = 'free'    st.markdown('</div>', unsafe_allow_html=True)

            st.session_state['plan_price'] = 0.00    

            st.session_state['plan_name'] = 'Free Starter'    # New user onboarding info

            if ERROR_HANDLER_AVAILABLE:    st.info("👋 Welcome to IntelliCV-AI! Complete your registration above to unlock all these features.")

                log_user_action("plan_selected", {"plan": "free", "price": 0.00})

            st.success("Free plan selected! Creating your account...")# Footer section

            time.sleep(1)st.markdown("---")

            st.switch_page("pages/01_Registration.py")st.markdown("""

    <div style="text-align: center; color: #666; padding: 1rem;">

    with col2:    <p><strong>IntelliCV-AI</strong> | Powered by Advanced AI Technology</p>

        if st.button("⭐ Choose Monthly Pro", use_container_width=True, type="primary"):    <p>🔒 Your data is secure • 🌍 Available worldwide • 📞 24/7 Support</p>

            st.session_state['selected_plan'] = 'monthly'</div>

            st.session_state['plan_price'] = 9.99""", unsafe_allow_html=True)

            st.session_state['plan_name'] = 'Monthly Pro'

            if ERROR_HANDLER_AVAILABLE:# Debug information (development only)

                log_user_action("plan_selected", {"plan": "monthly", "price": 9.99})if st.sidebar.checkbox("🔧 Debug Info", value=False):

            st.success("Monthly Pro selected! Proceeding to registration...")    with st.sidebar.expander("System Status"):

            time.sleep(1)        st.write("**Module Status:**")

            st.switch_page("pages/01_Registration.py")        st.write(f"• Sidebar: {'✅' if SIDEBAR_AVAILABLE else '❌'}")

            st.write(f"• Error Handler: {'✅' if ERROR_HANDLER_AVAILABLE else '❌'}")

    with col3:        st.write(f"• Enhanced Auth: {'✅' if ENHANCED_AUTH_AVAILABLE else '❌'}")

        if st.button("🏆 Choose Annual Pro", use_container_width=True):        st.write(f"• Logo: {'✅' if logo_b64 else '❌'}")

            st.session_state['selected_plan'] = 'annual'        

            st.session_state['plan_price'] = 149.99        st.write("**Session State:**")

            st.session_state['plan_name'] = 'Annual Pro'        for key, value in st.session_state.items():

            if ERROR_HANDLER_AVAILABLE:            if not key.startswith('_'):

                log_user_action("plan_selected", {"plan": "annual", "price": 149.99})                st.write(f"• {key}: {str(value)[:50]}...")

            st.success("Annual Pro selected! Great choice - you save $70!")
            time.sleep(1)
            st.switch_page("pages/01_Registration.py")
    
    with col4:
        if st.button("🌟 Go Super-User", use_container_width=True):
            st.session_state['selected_plan'] = 'super_user'
            st.session_state['plan_price'] = 299.00
            st.session_state['plan_name'] = 'Super-User Elite'
            if ERROR_HANDLER_AVAILABLE:
                log_user_action("plan_selected", {"plan": "super_user", "price": 299.00})
            st.success("Super-User Elite selected! Welcome to our premium tier!")
            time.sleep(1)
            st.switch_page("pages/01_Registration.py")
    
    # Payment methods info
    st.markdown('''
    <div class="payment-methods">
        <h4 style="color: #667eea; margin-bottom: 1rem;">💳 Secure Payment Options Available</h4>
        <p>We support all major payment methods through our admin payment system:</p>
        <div style="display: flex; justify-content: center; gap: 2rem; margin: 1rem 0; flex-wrap: wrap;">
            <span>💳 Credit Cards</span>
            <span>🏦 Bank Transfer</span>
            <span>📱 Google Pay</span>
            <span>🛡️ Stripe</span>
            <span>💰 PayPal</span>
        </div>
        <p style="color: #666; font-size: 0.9rem; margin: 1rem 0 0 0;">
            All payments processed securely through our admin portal • Enterprise-grade security • Cancel anytime
        </p>
    </div>
    ''', unsafe_allow_html=True)

def render_auth_section():
    """Render login and registration options"""
    
    # Check if user is already authenticated
    if st.session_state.get('authenticated_user'):
        st.markdown('''
        <div class="auth-section">
            <div class="auth-header">
                <h2>✅ Welcome Back!</h2>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.success(f"Welcome back, **{st.session_state['authenticated_user']}**!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Go to Dashboard", use_container_width=True, type="primary"):
                st.switch_page("pages/04_Dashboard.py")
        
        with col2:
            if st.button("📄 Upload Resume", use_container_width=True):
                st.switch_page("pages/05_Resume_Upload.py")
        
        with col3:
            if st.button("🚪 Logout", use_container_width=True):
                # Clear session
                for key in ['authenticated_user', 'user_role', 'session_token', 'selected_plan']:
                    if key in st.session_state:
                        del st.session_state[key]
                
                if ERROR_HANDLER_AVAILABLE:
                    log_user_action("user_logout", {"page": "home"})
                
                show_success("Successfully logged out!")
                time.sleep(1)
                st.rerun()
        
        return
    
    # Authentication section for non-logged-in users
    st.markdown('''
    <div class="auth-section">
        <div class="auth-header">
            <h2>🔐 Access Your IntelliCV-AI Account</h2>
            <p style="color: #666;">Login to your existing account or create a new one to get started</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Auth tabs
    tab1, tab2 = st.tabs(["🔑 Login to Account", "🆕 Create New Account"])
    
    with tab1:
        # Login form
        st.subheader("Welcome Back to IntelliCV-AI!")
        
        with st.form("login_form"):
            username = st.text_input("Username or Email", placeholder="Enter your username or email address")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            remember_me = st.checkbox("Remember me for 30 days")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("🔑 Login Now", use_container_width=True, type="primary"):
                    if username and password:
                        # Simple demo authentication
                        st.session_state['authenticated_user'] = username
                        st.session_state['user_role'] = 'admin' if username.lower() == 'admin' else 'user'
                        st.session_state['session_token'] = f"token_{int(time.time())}"
                        st.session_state['remember_me'] = remember_me
                        
                        if ERROR_HANDLER_AVAILABLE:
                            log_user_action("user_login", {
                                "username": username, 
                                "page": "home",
                                "remember_me": remember_me
                            })
                        
                        show_success("Login successful! Welcome back to IntelliCV-AI")
                        time.sleep(1)
                        st.rerun()
                    else:
                        show_error("Please enter both username and password")
            
            with col2:
                if st.form_submit_button("🔄 Reset Password", use_container_width=True):
                    st.info("Password reset link will be sent to your email address")
        
        st.info("💡 **Demo Access:** Use any username/password to explore the platform features")
        
        # Social login options
        st.markdown("---")
        st.markdown("**Or continue with:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔗 LinkedIn", use_container_width=True):
                st.info("LinkedIn OAuth integration coming soon!")
        
        with col2:
            if st.button("🔍 Google", use_container_width=True):
                st.info("Google OAuth integration coming soon!")
        
        with col3:
            if st.button("📧 Microsoft", use_container_width=True):
                st.info("Microsoft OAuth integration coming soon!")
    
    with tab2:
        # Registration redirect
        st.subheader("Join IntelliCV-AI Today!")
        st.write("Create your account and transform your career with AI-powered intelligence.")
        
        # Selected plan display
        if st.session_state.get('selected_plan'):
            plan_name = st.session_state.get('plan_name', 'Selected Plan')
            plan_price = st.session_state.get('plan_price', 0)
            
            if plan_price > 0:
                st.success(f"✅ Plan Selected: **{plan_name}** - ${plan_price}")
            else:
                st.success(f"✅ Plan Selected: **{plan_name}** - FREE")
        
        if st.button("🚀 Create Your Account", use_container_width=True, type="primary"):
            if ERROR_HANDLER_AVAILABLE:
                log_user_action("registration_redirect", {"source": "home_page"})
            st.switch_page("pages/01_Registration.py")
        
        st.markdown("**✨ What you get with an account:**")
        st.markdown("""
        • 🧠 **AI-Powered Career Analysis** - Advanced 6-system coordination
        • 📄 **Smart Resume Building** - LinkedIn-integrated job title engine  
        • 📊 **Real-Time Market Intelligence** - Live data from 3,418+ sources
        • 🎯 **Personalized Recommendations** - Career positioning & skill gaps
        • 🤝 **Professional Mentorship** - Connect with industry experts
        • 🚀 **Profile Optimization** - Maximize your professional visibility
        """)

def render_system_status():
    """Display system status for admin AI integration"""
    if ADMIN_AI_AVAILABLE:
        st.markdown('''
        <div style="background: linear-gradient(45deg, #28a745, #20c997); color: white; padding: 1.5rem; border-radius: 12px; text-align: center; margin: 2rem 0; box-shadow: 0 8px 30px rgba(40, 167, 69, 0.3);">
            <h4 style="margin-bottom: 1rem;">🧠 AI Systems: Fully Operational</h4>
            <p style="margin: 0.5rem 0;">Enhanced Job Title Engine • Real AI Data Connector • 6-System Coordination</p>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">Admin Portal Integration Active • Enhanced Processing Available</p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div style="background: linear-gradient(45deg, #ffc107, #ff8c00); color: #333; padding: 1.5rem; border-radius: 12px; text-align: center; margin: 2rem 0; box-shadow: 0 8px 30px rgba(255, 193, 7, 0.3);">
            <h4 style="margin-bottom: 1rem;">⚡ AI Systems: Initializing</h4>
            <p style="margin: 0.5rem 0;">Core functionality available • Enhanced features loading</p>
            <p style="margin: 0; font-size: 0.9rem;">Admin integration coming online • Full system activation pending</p>
        </div>
        ''', unsafe_allow_html=True)

def main():
    """Main welcome page function"""
    
    # Log page access
    if ERROR_HANDLER_AVAILABLE:
        log_user_action("home_page_accessed", {
            'timestamp': datetime.now().isoformat(),
            'admin_ai_available': ADMIN_AI_AVAILABLE,
            'user_authenticated': bool(st.session_state.get('authenticated_user')),
            'selected_plan': st.session_state.get('selected_plan')
        })
    
    # Render main sections
    render_logo_section()
    render_system_status() 
    render_usp_section()
    render_pricing_section()
    
    st.markdown("---")
    
    render_auth_section()
    
    # Footer
    st.markdown("""
    ---
    
    <div style="text-align: center; padding: 2rem; color: #666;">
        <h3 style="color: #667eea; margin-bottom: 1rem;">🚀 IntelliCV-AI</h3>
        <p><strong>Transforming careers with AI-powered intelligence</strong></p>
        <p style="margin: 1rem 0;">Secure • Private • Powered by Advanced AI • Trusted by Professionals Worldwide</p>
        <p style="font-size: 0.9rem;">© 2025 IntelliCV-AI. All rights reserved. | 
        <a href="#" style="color: #667eea;">Privacy Policy</a> | 
        <a href="#" style="color: #667eea;">Terms of Service</a> | 
        <a href="#" style="color: #667eea;">Contact Support</a></p>
    </div>
    """, unsafe_allow_html=True)

# Run the main function
if __name__ == "__main__":
    main()