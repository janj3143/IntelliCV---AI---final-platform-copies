""""""""""""

Profile Management - Complete User Profile System

"""👤 User Profile Management - Complete Profile System



import streamlit as st==================================================👤 User Profile - Complete Your IntelliCV Journey👤 User Profile - Complete Your IntelliCV Journey

from pathlib import Path

import timeComprehensive profile management with enhanced features and validation

from datetime import datetime

"""================================================================================================

# Setup paths and imports

current_dir = Path(__file__).parent.parent

import sys

sys.path.insert(0, str(current_dir))import streamlit as stProfile completion and management pageProfile completion and management page



# Import utilities with fallbacksfrom pathlib import Path

try:

    from utils.error_handler import log_user_action, show_error, show_success, show_warningimport time""""""

    ERROR_HANDLER_AVAILABLE = True

except ImportError:from datetime import datetime

    ERROR_HANDLER_AVAILABLE = False

    def log_user_action(action, details=None): passimport json

    def show_error(msg): st.error(f"❌ {msg}")

    def show_success(msg): st.success(f"✅ {msg}")

    def show_warning(msg): st.warning(f"⚠️ {msg}")

# Setup paths and importsimport streamlit as stimport streamlit as st

# Page configuration

st.set_page_config(current_dir = Path(__file__).parent.parent

    page_title="👤 Profile Management | IntelliCV-AI",

    page_icon="👤",import sysfrom pathlib import Pathfrom pathlib import Path

    layout="wide",

    initial_sidebar_state="expanded"sys.path.insert(0, str(current_dir))

)

import timeimport time

# Authentication check

if not st.session_state.get('authenticated_user'):# Import utilities with fallbacks

    st.error("🔒 Please log in to access your profile")

    if st.button("🏠 Return to Home"):try:from datetime import datetimefrom datetime import datetime

        st.switch_page("pages/00_Home.py")

    st.stop()    from utils.error_handler import log_user_action, show_error, show_success, show_warning



# Professional CSS styling    ERROR_HANDLER_AVAILABLE = True

def load_profile_css():

    css = '''except ImportError:

    <style>

    .profile-header {    ERROR_HANDLER_AVAILABLE = False# Setup paths and imports# Setup paths and imports

        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

        color: white;    def log_user_action(action, details=None): pass

        padding: 2.5rem;

        border-radius: 12px;    def show_error(msg): st.error(f"❌ {msg}")current_dir = Path(__file__).parent.parentcurrent_dir = Path(__file__).parent.parent

        text-align: center;

        margin-bottom: 2rem;    def show_success(msg): st.success(f"✅ {msg}")

        box-shadow: 0 6px 20px rgba(0,0,0,0.2);

    }    def show_warning(msg): st.warning(f"⚠️ {msg}")import sysimport sys

    

    .profile-section {

        background: white;

        padding: 2rem;# Page configurationsys.path.insert(0, str(current_dir))sys.path.insert(0, str(current_dir))

        border-radius: 12px;

        box-shadow: 0 4px 16px rgba(0,0,0,0.1);st.set_page_config(

        margin-bottom: 2rem;

        border-left: 5px solid #667eea;    page_title="👤 Profile Management | IntelliCV-AI",

    }

        page_icon="👤",

    .completion-bar {

        background: #e9ecef;    layout="wide",# Import utilities with fallbacks# Import utilities with fallbacks

        border-radius: 10px;

        padding: 0.5rem;    initial_sidebar_state="expanded"

        margin: 1rem 0;

    })try:try:

    

    .completion-fill {

        background: linear-gradient(135deg, #28a745, #20c997);

        height: 20px;# Authentication check    from utils.error_handler import log_user_action, show_error, show_success, show_warning    from utils.error_handler import log_user_action, show_error, show_success, show_warning

        border-radius: 8px;

        transition: width 0.3s ease;if not st.session_state.get('authenticated_user'):

        display: flex;

        align-items: center;    st.error("🔒 Please log in to access your profile")    ERROR_HANDLER_AVAILABLE = True    ERROR_HANDLER_AVAILABLE = True

        justify-content: center;

        color: white;    if st.button("🏠 Return to Home"):

        font-weight: bold;

        font-size: 0.8rem;        st.switch_page("pages/00_Home.py")except ImportError:except ImportError:

    }

        st.stop()

    .field-group {

        background: #f8f9fa;    ERROR_HANDLER_AVAILABLE = False    ERROR_HANDLER_AVAILABLE = False

        padding: 1.5rem;

        border-radius: 10px;# Professional CSS styling

        margin: 1rem 0;

        border: 1px solid #e9ecef;def load_profile_css():    def log_user_action(action, details=None): pass    def log_user_action(action, details=None): pass

    }

        css = '''

    .skill-tag {

        background: #e3f2fd;    <style>    def show_error(msg): st.error(f"❌ {msg}")    def show_error(msg): st.error(f"❌ {msg}")

        color: #1976d2;

        padding: 0.3rem 0.8rem;    .profile-header {

        border-radius: 15px;

        font-size: 0.8rem;        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);    def show_success(msg): st.success(f"✅ {msg}")    def show_success(msg): st.success(f"✅ {msg}")

        margin: 0.2rem;

        display: inline-block;        color: white;

    }

    </style>        padding: 2.5rem;    def show_warning(msg): st.warning(f"⚠️ {msg}")    def show_warning(msg): st.warning(f"⚠️ {msg}")

    '''

    st.markdown(css, unsafe_allow_html=True)        border-radius: 12px;



# Load CSS        text-align: center;

load_profile_css()

        margin-bottom: 2rem;

# Initialize profile data

if 'profile_data' not in st.session_state:        box-shadow: 0 6px 20px rgba(0,0,0,0.2);# Page configuration# Page configuration

    st.session_state.profile_data = {}

    }

# Define profile fields

PROFILE_FIELDS = {    st.set_page_config(st.set_page_config(

    'basic_info': {

        'title': 'Basic Information',    .profile-section {

        'fields': {

            'full_name': {'label': 'Full Name', 'type': 'text', 'required': True},        background: white;    page_title="👤 Your Profile | IntelliCV",    page_title="👤 Your Profile | IntelliCV",

            'email': {'label': 'Email Address', 'type': 'email', 'required': True},

            'phone': {'label': 'Phone Number', 'type': 'text', 'required': True},        padding: 2rem;

            'location': {'label': 'Location (City, State)', 'type': 'text', 'required': True},

            'linkedin_url': {'label': 'LinkedIn Profile', 'type': 'url', 'required': False},        border-radius: 12px;    page_icon="👤",    page_icon="👤",

        }

    },        box-shadow: 0 4px 16px rgba(0,0,0,0.1);

    'professional_info': {

        'title': 'Professional Information',        margin-bottom: 2rem;    layout="wide",    layout="wide",

        'fields': {

            'current_title': {'label': 'Current Job Title', 'type': 'text', 'required': True},        border-left: 5px solid #667eea;

            'current_company': {'label': 'Current Company', 'type': 'text', 'required': False},

            'industry': {'label': 'Industry', 'type': 'selectbox', 'required': True,    }    initial_sidebar_state="expanded"    initial_sidebar_state="expanded"

                        'options': ['Technology', 'Healthcare', 'Finance', 'Education', 'Manufacturing', 

                                  'Retail', 'Consulting', 'Government', 'Non-profit', 'Other']},    

            'experience_level': {'label': 'Experience Level', 'type': 'selectbox', 'required': True,

                               'options': ['Entry Level (0-2 years)', 'Mid Level (3-5 years)',     .completion-bar {))

                                         'Senior Level (6-10 years)', 'Executive (10+ years)']},

        }        background: #e9ecef;

    }

}        border-radius: 10px;



def calculate_completion_percentage():        padding: 0.5rem;

    """Calculate profile completion percentage"""

    total_required = 0        margin: 1rem 0;# Authentication check# Authentication check

    completed_required = 0

        }

    for section in PROFILE_FIELDS.values():

        for field_key, field_config in section['fields'].items():    if not st.session_state.get('authenticated_user'):if not st.session_state.get('authenticated_user'):

            if field_config['required']:

                total_required += 1    .completion-fill {

                if st.session_state.profile_data.get(field_key):

                    completed_required += 1        background: linear-gradient(135deg, #28a745, #20c997);    st.error("🔒 Please log in to access your profile")    st.error("🔒 Please log in to access your profile")

    

    return (completed_required / total_required * 100) if total_required > 0 else 0        height: 20px;



# Page header        border-radius: 8px;    if st.button("🏠 Return to Home"):    if st.button("🏠 Return to Home"):

username = st.session_state.get('authenticated_user', 'User')

completion_pct = calculate_completion_percentage()        transition: width 0.3s ease;



st.markdown(f'''        display: flex;        st.switch_page("pages/00_Home.py")        st.switch_page("pages/00_Home.py")

<div class="profile-header">

    <h1>👤 Profile Management</h1>        align-items: center;

    <p>Welcome, {username}! Complete your profile to unlock all features</p>

    <div class="completion-bar">        justify-content: center;    st.stop()    st.stop()

        <div class="completion-fill" style="width: {completion_pct}%;">

            {completion_pct:.0f}% Complete        color: white;

        </div>

    </div>        font-weight: bold;

</div>

''', unsafe_allow_html=True)        font-size: 0.8rem;



# Progress indicators    }# Professional CSS styling# Professional CSS styling

st.markdown("## 📊 Profile Status")

col1, col2 = st.columns(2)    



with col1:    .field-group {def load_profile_css():def load_profile_css():

    st.metric("Profile Completion", f"{completion_pct:.0f}%")

        background: #f8f9fa;

with col2:

    status = "🌟 Complete!" if completion_pct >= 80 else "🎯 In Progress"        padding: 1.5rem;    css = '''    css = '''

    st.metric("Status", status)

        border-radius: 10px;

# Profile editing form

st.markdown("---")        margin: 1rem 0;    <style>    <style>

st.markdown("## ✏️ Edit Profile Information")

        border: 1px solid #e9ecef;

# Create tabs for different sections

tabs = st.tabs([section['title'] for section in PROFILE_FIELDS.values()])    }    .profile-header {    .profile-header {



for i, (section_key, section_config) in enumerate(PROFILE_FIELDS.items()):    

    with tabs[i]:

        st.markdown('<div class="profile-section">', unsafe_allow_html=True)    .skill-tag {        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

        

        for field_key, field_config in section_config['fields'].items():        background: #e3f2fd;

            label = field_config['label']

            field_type = field_config['type']        color: #1976d2;        color: white;        color: white;

            required = field_config['required']

            current_value = st.session_state.profile_data.get(field_key, '')        padding: 0.3rem 0.8rem;

            

            # Add required indicator        border-radius: 15px;        padding: 2rem;        padding: 2rem;

            display_label = f"{label} {'*' if required else ''}"

                    font-size: 0.8rem;

            # Render appropriate input field

            if field_type == 'text' or field_type == 'email' or field_type == 'url':        margin: 0.2rem;        border-radius: 12px;        border-radius: 12px;

                new_value = st.text_input(display_label, value=current_value, key=f"input_{field_key}")

            elif field_type == 'selectbox':        display: inline-block;

                options = field_config.get('options', [])

                if not required and '' not in options:    }        text-align: center;

                    options = [''] + options

                    

                current_index = 0

                if current_value and current_value in options:    .progress-indicator {        margin-bottom: 2rem;        text-align: center;        text-align: center;

                    current_index = options.index(current_value)

                        background: white;

                new_value = st.selectbox(display_label, options, index=current_index, key=f"input_{field_key}")

            else:        padding: 1.5rem;        box-shadow: 0 6px 20px rgba(0,0,0,0.2);

                new_value = current_value

                    border-radius: 10px;

            # Update session state if value changed

            if new_value != current_value:        box-shadow: 0 2px 8px rgba(0,0,0,0.1);    }        margin-bottom: 2rem;        margin-bottom: 2rem;

                st.session_state.profile_data[field_key] = new_value

                margin: 1rem 0;

        st.markdown('</div>', unsafe_allow_html=True)

    }    

# Action buttons

st.markdown("---")    

col1, col2, col3 = st.columns(3)

    .achievement-badge {    .profile-card {        box-shadow: 0 6px 20px rgba(0,0,0,0.2);        box-shadow: 0 6px 20px rgba(0,0,0,0.2);

with col1:

    if st.button("💾 Save Profile", type="primary", use_container_width=True):        background: linear-gradient(135deg, #ffc107, #e0a800);

        # Add save timestamp

        st.session_state.profile_data['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")        color: black;        background: white;

        

        # Add to activity log        padding: 0.5rem 1rem;

        if 'recent_activities' not in st.session_state:

            st.session_state.recent_activities = []        border-radius: 20px;        padding: 2rem;    }    }

        

        st.session_state.recent_activities.append({        font-weight: bold;

            'timestamp': datetime.now(),

            'type': 'profile_update',        display: inline-block;        border-radius: 12px;

            'description': 'Profile information updated'

        })        margin: 0.2rem;

        

        show_success("Profile saved successfully!")    }        box-shadow: 0 4px 16px rgba(0,0,0,0.1);        

        

        if ERROR_HANDLER_AVAILABLE:    

            log_user_action("profile_saved", {"completion_percentage": completion_pct})

            .alert-success {        margin-bottom: 1.5rem;

        time.sleep(1)

        background: #d4edda;

with col2:

    if st.button("🏠 Back to Dashboard", use_container_width=True):        color: #155724;        border-left: 5px solid #667eea;    .profile-section {    .profile-section {

        st.switch_page("pages/04_Dashboard.py")

        padding: 1rem;

with col3:

    if st.button("📄 Upload Resume", use_container_width=True):        border-radius: 8px;    }

        st.switch_page("pages/05_Resume_Upload.py")

        border-left: 4px solid #28a745;

# Profile preview

if completion_pct > 30:        margin: 1rem 0;            background: white;        background: white;

    st.markdown("---")

    st.markdown("## 👀 Profile Preview")    }

    

    with st.expander("View Profile Summary"):        .skill-tag {

        st.markdown('<div class="field-group">', unsafe_allow_html=True)

            .alert-warning {

        if st.session_state.profile_data.get('full_name'):

            st.markdown(f"### {st.session_state.profile_data['full_name']}")        background: #fff3cd;        background: linear-gradient(135deg, #667eea, #764ba2);        padding: 2rem;        padding: 2rem;

        

        if st.session_state.profile_data.get('current_title'):        color: #856404;

            st.markdown(f"**{st.session_state.profile_data['current_title']}**")

                padding: 1rem;        color: white;

        if st.session_state.profile_data.get('current_company'):

            st.markdown(f"at {st.session_state.profile_data['current_company']}")        border-radius: 8px;

        

        if st.session_state.profile_data.get('location'):        border-left: 4px solid #ffc107;        padding: 0.5rem 1rem;        border-radius: 12px;        border-radius: 12px;

            st.markdown(f"📍 {st.session_state.profile_data['location']}")

                margin: 1rem 0;

        st.markdown('</div>', unsafe_allow_html=True)

    }        border-radius: 20px;

# Sidebar navigation

st.sidebar.markdown("### 🚀 Quick Actions")    </style>



if st.sidebar.button("📊 View Dashboard", use_container_width=True):    '''        margin: 0.2rem;        box-shadow: 0 4px 16px rgba(0,0,0,0.1);        box-shadow: 0 4px 16px rgba(0,0,0,0.1);

    st.switch_page("pages/04_Dashboard.py")

    st.markdown(css, unsafe_allow_html=True)

if st.sidebar.button("📄 Resume Upload", use_container_width=True):

    st.switch_page("pages/05_Resume_Upload.py")        font-size: 0.9rem;



if st.sidebar.button("🎯 Find Jobs", use_container_width=True):# Load CSS

    st.switch_page("pages/06_Job_Match.py")

load_profile_css()        display: inline-block;        margin-bottom: 2rem;        margin-bottom: 2rem;

# Footer

st.markdown("---")

st.markdown("""

<div style="text-align: center; color: #666; padding: 1.5rem; background: #f8f9fa; border-radius: 10px;"># Initialize profile data    }

    <p><strong>IntelliCV-AI Profile Management</strong> | Your Professional Identity</p>

    <p>🔒 Secure & Private • ✏️ Always Editable • 🚀 AI-Optimized</p>if 'profile_data' not in st.session_state:

</div>

""", unsafe_allow_html=True)    st.session_state.profile_data = {}    </style>        border-left: 5px solid #667eea;        border-left: 5px solid #667eea;



# Define profile fields and validation    '''

PROFILE_FIELDS = {

    'basic_info': {    st.markdown(css, unsafe_allow_html=True)    }    }

        'title': 'Basic Information',

        'fields': {

            'full_name': {'label': 'Full Name', 'type': 'text', 'required': True},

            'email': {'label': 'Email Address', 'type': 'email', 'required': True},# Load CSS        

            'phone': {'label': 'Phone Number', 'type': 'text', 'required': True},

            'location': {'label': 'Location (City, State)', 'type': 'text', 'required': True},load_profile_css()

            'linkedin_url': {'label': 'LinkedIn Profile', 'type': 'url', 'required': False},

            'portfolio_url': {'label': 'Portfolio/Website', 'type': 'url', 'required': False}    .progress-bar {    .progress-bar {

        }

    },# Initialize profile data

    'professional_info': {

        'title': 'Professional Information',if 'profile_data' not in st.session_state:        background: #e0e0e0;        background: #e0e0e0;

        'fields': {

            'current_title': {'label': 'Current Job Title', 'type': 'text', 'required': True},    st.session_state.profile_data = {

            'current_company': {'label': 'Current Company', 'type': 'text', 'required': False},

            'industry': {'label': 'Industry', 'type': 'selectbox', 'required': True,        'full_name': '',        border-radius: 10px;        border-radius: 10px;

                        'options': ['Technology', 'Healthcare', 'Finance', 'Education', 'Manufacturing', 

                                  'Retail', 'Consulting', 'Government', 'Non-profit', 'Other']},        'email': '',

            'experience_level': {'label': 'Experience Level', 'type': 'selectbox', 'required': True,

                               'options': ['Entry Level (0-2 years)', 'Mid Level (3-5 years)',         'phone': '',        overflow: hidden;        overflow: hidden;

                                         'Senior Level (6-10 years)', 'Executive (10+ years)']},

            'work_preference': {'label': 'Work Preference', 'type': 'selectbox', 'required': True,        'location': '',

                              'options': ['Remote', 'On-site', 'Hybrid', 'No Preference']}

        }        'current_title': '',        margin: 1rem 0;        margin: 1rem 0;

    },

    'career_goals': {        'experience_level': '',

        'title': 'Career Goals & Preferences',

        'fields': {        'skills': [],    }    }

            'target_roles': {'label': 'Target Job Titles (comma-separated)', 'type': 'text_area', 'required': False},

            'salary_range': {'label': 'Desired Salary Range', 'type': 'selectbox', 'required': False,        'bio': '',

                           'options': ['Under $50k', '$50k-$75k', '$75k-$100k', '$100k-$125k', 

                                     '$125k-$150k', '$150k-$200k', 'Over $200k', 'Prefer not to say']},        'linkedin': '',        

            'career_stage': {'label': 'Career Stage', 'type': 'selectbox', 'required': False,

                           'options': ['Exploring Options', 'Actively Job Searching', 'Passively Looking',         'github': '',

                                     'Career Advancement', 'Career Change', 'Skill Building']},

            'key_skills': {'label': 'Key Skills (comma-separated)', 'type': 'text_area', 'required': False}        'portfolio': '',    .progress-fill {    .progress-fill {

        }

    }        'salary_expectation': '',

}

        'availability': '',        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

def calculate_completion_percentage():

    """Calculate profile completion percentage"""        'work_preference': ''

    total_required = 0

    completed_required = 0    }        height: 20px;        height: 20px;

    total_optional = 0

    completed_optional = 0

    

    for section in PROFILE_FIELDS.values():# Profile header        border-radius: 10px;        border-radius: 10px;

        for field_key, field_config in section['fields'].items():

            field_value = st.session_state.profile_data.get(field_key, '')username = st.session_state.get('authenticated_user', 'User')

            

            if field_config['required']:st.markdown(f'''        transition: width 0.3s ease;        transition: width 0.3s ease;

                total_required += 1

                if field_value:<div class="profile-header">

                    completed_required += 1

            else:    <h1>👤 Welcome, {username}!</h1>        display: flex;        display: flex;

                total_optional += 1

                if field_value:    <p>Complete your profile to unlock all IntelliCV features</p>

                    completed_optional += 1

    </div>        align-items: center;        align-items: center;

    # Weight required fields more heavily (70% for required, 30% for optional)

    required_percentage = (completed_required / total_required * 100) if total_required > 0 else 0''', unsafe_allow_html=True)

    optional_percentage = (completed_optional / total_optional * 100) if total_optional > 0 else 0

            justify-content: center;        justify-content: center;

    overall_completion = (required_percentage * 0.7) + (optional_percentage * 0.3)

    # Calculate profile completion

    return overall_completion, completed_required, total_required, completed_optional, total_optional

profile_data = st.session_state.profile_data        color: white;        color: white;

# Page header

username = st.session_state.get('authenticated_user', 'User')required_fields = ['full_name', 'email', 'phone', 'location', 'current_title', 'experience_level']

completion_pct, req_completed, req_total, opt_completed, opt_total = calculate_completion_percentage()

completed_fields = sum(1 for field in required_fields if profile_data.get(field))        font-weight: bold;        font-weight: bold;

st.markdown(f'''

<div class="profile-header">completion_percentage = (completed_fields / len(required_fields)) * 100

    <h1>👤 Profile Management</h1>

    <p>Welcome, {username}! Complete your profile to unlock all features</p>        font-size: 0.8rem;        font-size: 0.8rem;

    <div class="completion-bar">

        <div class="completion-fill" style="width: {completion_pct}%;"># Progress indicator

            {completion_pct:.0f}% Complete

        </div>col1, col2, col3 = st.columns([2, 1, 1])    }    }

    </div>

</div>with col1:

''', unsafe_allow_html=True)

    st.progress(completion_percentage / 100)    </style>    </style>

# Progress indicators

st.markdown("## 📊 Profile Status")    st.caption(f"Profile Completion: {completion_percentage:.0f}%")



col1, col2, col3, col4 = st.columns(4)with col2:    '''    '''



with col1:    st.metric("Fields Complete", f"{completed_fields}/{len(required_fields)}")

    st.metric("Overall Progress", f"{completion_pct:.0f}%")

with col3:    st.markdown(css, unsafe_allow_html=True)    st.markdown(css, unsafe_allow_html=True)

with col2:

    st.metric("Required Fields", f"{req_completed}/{req_total}")    if completion_percentage >= 80:



with col3:        st.success("🎉 Almost Done!")

    st.metric("Optional Fields", f"{opt_completed}/{opt_total}")

    elif completion_percentage >= 50:

with col4:

    badge_text = "🌟 Complete!" if completion_pct >= 80 else "🎯 In Progress"        st.warning("⚡ Keep Going!")load_profile_css()load_profile_css()

    st.metric("Status", badge_text)

    else:

# Profile completion recommendations

if completion_pct < 100:        st.info("🚀 Get Started!")

    missing_required = []

    missing_optional = []

    

    for section in PROFILE_FIELDS.values():# Tab structure# Get user info# Get user info

        for field_key, field_config in section['fields'].items():

            if not st.session_state.profile_data.get(field_key):tab1, tab2, tab3, tab4 = st.tabs(["📝 Basic Info", "💼 Professional", "🔧 Preferences", "📊 Summary"])

                if field_config['required']:

                    missing_required.append(field_config['label'])user_name = st.session_state.get('authenticated_user', 'User')user_name = st.session_state.get('authenticated_user', 'User')

                else:

                    missing_optional.append(field_config['label'])with tab1:

    

    if missing_required:    st.markdown('<div class="profile-card">', unsafe_allow_html=True)user_email = st.session_state.get('user_email', '')user_email = st.session_state.get('user_email', '')

        st.markdown('<div class="alert-warning">', unsafe_allow_html=True)

        st.markdown("### ⚠️ Missing Required Fields")    st.markdown("### 📋 Personal Information")

        for field in missing_required[:3]:  # Show first 3

            st.write(f"• {field}")    is_new_user = st.session_state.get('is_new_user', True)is_new_user = st.session_state.get('is_new_user', True)

        if len(missing_required) > 3:

            st.write(f"• +{len(missing_required) - 3} more required fields")    col1, col2 = st.columns(2)

        st.markdown('</div>', unsafe_allow_html=True)

    with col1:

# Profile editing form

st.markdown("---")        full_name = st.text_input(

st.markdown("## ✏️ Edit Profile Information")

            "Full Name *", # Initialize profile data in session state# Initialize profile data in session state

# Create tabs for different sections

tab_names = [section['title'] for section in PROFILE_FIELDS.values()]            value=profile_data.get('full_name', ''),

tabs = st.tabs(tab_names)

            placeholder="Enter your full name"if 'profile_data' not in st.session_state:if 'profile_data' not in st.session_state:

profile_updated = False

        )

for i, (section_key, section_config) in enumerate(PROFILE_FIELDS.items()):

    with tabs[i]:        email = st.text_input(    st.session_state.profile_data = {    st.session_state.profile_data = {

        st.markdown(f'<div class="profile-section">', unsafe_allow_html=True)

                    "Email Address *", 

        section_updated = False

                    value=profile_data.get('email', ''),        'personal_info': {},        'personal_info': {},

        for field_key, field_config in section_config['fields'].items():

            label = field_config['label']            placeholder="your.email@example.com"

            field_type = field_config['type']

            required = field_config['required']        )        'contact_info': {},        'contact_info': {},

            current_value = st.session_state.profile_data.get(field_key, '')

                    linkedin = st.text_input(

            # Add required indicator

            display_label = f"{label} {'*' if required else ''}"            "LinkedIn Profile",         'professional_info': {},        'professional_info': {},

            

            # Render appropriate input field            value=profile_data.get('linkedin', ''),

            if field_type == 'text':

                new_value = st.text_input(display_label, value=current_value, key=f"input_{field_key}")            placeholder="https://linkedin.com/in/yourname"        'preferences': {},        'preferences': {},

            elif field_type == 'email':

                new_value = st.text_input(display_label, value=current_value, key=f"input_{field_key}")        )

            elif field_type == 'url':

                new_value = st.text_input(display_label, value=current_value,             'completion_status': {        'completion_status': {

                                        placeholder="https://...", key=f"input_{field_key}")

            elif field_type == 'text_area':    with col2:

                new_value = st.text_area(display_label, value=current_value, 

                                       height=100, key=f"input_{field_key}")        phone = st.text_input(            'personal_info': False,            'personal_info': False,

            elif field_type == 'selectbox':

                options = field_config.get('options', [])            "Phone Number *", 

                # Add empty option for optional fields

                if not required and '' not in options:            value=profile_data.get('phone', ''),            'contact_info': False,            'contact_info': False,

                    options = [''] + options

                            placeholder="+1 (555) 123-4567"

                current_index = 0

                if current_value and current_value in options:        )            'professional_info': False,            'professional_info': False,

                    current_index = options.index(current_value)

                        location = st.text_input(

                new_value = st.selectbox(display_label, options, index=current_index, 

                                       key=f"input_{field_key}")            "Location *",             'preferences': False            'preferences': False

            else:

                new_value = current_value            value=profile_data.get('location', ''),

            

            # Update session state if value changed            placeholder="City, State/Country"        }        }

            if new_value != current_value:

                st.session_state.profile_data[field_key] = new_value        )

                section_updated = True

                profile_updated = True        github = st.text_input(    }    }

        

        # Section-specific actions            "GitHub Profile", 

        if section_updated:

            show_success(f"{section_config['title']} updated successfully!")            value=profile_data.get('github', ''),

        

        st.markdown('</div>', unsafe_allow_html=True)            placeholder="https://github.com/yourusername"



# Global save button        )# Calculate completion percentage# Calculate completion percentage

st.markdown("---")

col1, col2, col3 = st.columns(3)    



with col1:    bio = st.text_area(completion_data = st.session_state.profile_data['completion_status']completion_data = st.session_state.profile_data['completion_status']

    if st.button("💾 Save All Changes", type="primary", use_container_width=True):

        # Validate required fields        "Professional Bio",

        missing_required = []

        for section in PROFILE_FIELDS.values():        value=profile_data.get('bio', ''),completed_sections = sum(completion_data.values())completed_sections = sum(completion_data.values())

            for field_key, field_config in section['fields'].items():

                if field_config['required'] and not st.session_state.profile_data.get(field_key):        height=100,

                    missing_required.append(field_config['label'])

                placeholder="Brief description of your professional background and goals..."total_sections = len(completion_data)total_sections = len(completion_data)

        if missing_required:

            show_error(f"Please complete required fields: {', '.join(missing_required[:3])}")    )

        else:

            # Add save timestamp    completion_percentage = int((completed_sections / total_sections) * 100)completion_percentage = int((completed_sections / total_sections) * 100)

            st.session_state.profile_data['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                st.markdown('</div>', unsafe_allow_html=True)

            # Add to activity log

            if 'recent_activities' not in st.session_state:

                st.session_state.recent_activities = []

            with tab2:

            st.session_state.recent_activities.append({

                'timestamp': datetime.now(),    st.markdown('<div class="profile-card">', unsafe_allow_html=True)# Header# Header

                'type': 'profile_update',

                'description': 'Profile information updated'    st.markdown("### 💼 Professional Details")

            })

                st.markdown(f'''st.markdown(f'''

            show_success("Profile saved successfully!")

                col1, col2 = st.columns(2)

            if ERROR_HANDLER_AVAILABLE:

                log_user_action("profile_saved", {    with col1:<div class="profile-header"><div class="profile-header">

                    "completion_percentage": completion_pct,

                    "fields_completed": req_completed + opt_completed        current_title = st.text_input(

                })

                        "Current Job Title *",     <h1>👤 Welcome, {user_name}!</h1>    <h1>👤 Welcome, {user_name}!</h1>

            time.sleep(1)

                        value=profile_data.get('current_title', ''),

            # Navigate based on completion

            if completion_pct >= 80:            placeholder="e.g., Software Engineer, Marketing Manager"    <p>{"Complete your profile to unlock all IntelliCV features" if is_new_user else "Manage your profile and preferences"}</p>    <p>{"Complete your profile to unlock all IntelliCV features" if is_new_user else "Manage your profile and preferences"}</p>

                st.info("🎉 Profile complete! Ready to upload resume or explore features.")

            else:        )

                st.info("💡 Continue completing your profile for better job matching.")

            <div class="progress-bar">    <div class="progress-bar">

with col2:

    if st.button("🏠 Back to Dashboard", use_container_width=True):        experience_level = st.selectbox(

        st.switch_page("pages/04_Dashboard.py")

            "Experience Level *",        <div class="progress-fill" style="width: {completion_percentage}%">        <div class="progress-fill" style="width: {completion_percentage}%">

with col3:

    if st.button("📄 Upload Resume", use_container_width=True):            options=["", "Entry Level (0-2 years)", "Mid Level (3-5 years)", 

        if completion_pct >= 50:

            st.switch_page("pages/05_Resume_Upload.py")                    "Senior Level (6-10 years)", "Executive (10+ years)"],            {completion_percentage}% Complete            {completion_percentage}% Complete

        else:

            show_warning("Complete at least 50% of your profile before uploading resume")            index=0 if not profile_data.get('experience_level') else 



# Profile preview section                  ["", "Entry Level (0-2 years)", "Mid Level (3-5 years)",         </div>        </div>

if completion_pct > 30:

    st.markdown("---")                   "Senior Level (6-10 years)", "Executive (10+ years)"].index(profile_data.get('experience_level', ''))

    st.markdown("## 👀 Profile Preview")

            )    </div>    </div>

    with st.expander("View Profile Summary"):

        st.markdown('<div class="field-group">', unsafe_allow_html=True)        

        

        # Basic info preview        portfolio = st.text_input(</div></div>

        if st.session_state.profile_data.get('full_name'):

            st.markdown(f"### {st.session_state.profile_data['full_name']}")            "Portfolio Website", 

        

        if st.session_state.profile_data.get('current_title'):            value=profile_data.get('portfolio', ''),''', unsafe_allow_html=True)''', unsafe_allow_html=True)

            st.markdown(f"**{st.session_state.profile_data['current_title']}**")

                    placeholder="https://yourportfolio.com"

        if st.session_state.profile_data.get('current_company'):

            st.markdown(f"at {st.session_state.profile_data['current_company']}")        )

        

        if st.session_state.profile_data.get('location'):    

            st.markdown(f"📍 {st.session_state.profile_data['location']}")

            with col2:# New user guidance# New user guidance

        # Contact info

        contact_info = []        salary_expectation = st.text_input(

        if st.session_state.profile_data.get('email'):

            contact_info.append(f"📧 {st.session_state.profile_data['email']}")            "Salary Expectation", if is_new_user and completion_percentage < 100:if is_new_user and completion_percentage < 100:

        if st.session_state.profile_data.get('phone'):

            contact_info.append(f"📱 {st.session_state.profile_data['phone']}")            value=profile_data.get('salary_expectation', ''),

        

        if contact_info:            placeholder="e.g., $80,000 - $100,000"    st.info("🎯 **Getting Started:** Complete all sections below to unlock the full power of IntelliCV-AI!")    st.info("🎯 **Getting Started:** Complete all sections below to unlock the full power of IntelliCV-AI!")

            st.markdown(" • ".join(contact_info))

                )

        # Professional summary

        prof_details = []        

        if st.session_state.profile_data.get('industry'):

            prof_details.append(f"Industry: {st.session_state.profile_data['industry']}")        availability = st.selectbox(

        if st.session_state.profile_data.get('experience_level'):

            prof_details.append(f"Experience: {st.session_state.profile_data['experience_level']}")            "Availability",# Profile completion sections# Profile completion sections

        if st.session_state.profile_data.get('work_preference'):

            prof_details.append(f"Work Style: {st.session_state.profile_data['work_preference']}")            options=["", "Immediately", "2 weeks notice", "1 month notice", "3+ months"],

        

        if prof_details:            index=0 if not profile_data.get('availability') else col1, col2 = st.columns(2)col1, col2 = st.columns(2)

            st.markdown("**Professional Details:**")

            for detail in prof_details:                  ["", "Immediately", "2 weeks notice", "1 month notice", "3+ months"].index(profile_data.get('availability', ''))

                st.write(f"• {detail}")

                )

        # Skills

        if st.session_state.profile_data.get('key_skills'):    

            st.markdown("**Key Skills:**")

            skills = [skill.strip() for skill in st.session_state.profile_data['key_skills'].split(',')]    # Skills sectionwith col1:with col1:

            for skill in skills[:8]:  # Show first 8 skills

                st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)    st.markdown("#### 🛠️ Skills")

        

        st.markdown('</div>', unsafe_allow_html=True)    skills_input = st.text_input(    # Personal Information Section    # Personal Information Section



# Quick actions sidebar        "Add Skills (comma-separated)",

st.sidebar.markdown("### 🚀 Quick Actions")

        placeholder="Python, JavaScript, Project Management, etc."    with st.container():    with st.container():

completion_actions = []

if completion_pct < 50:    )

    completion_actions.append("Complete basic information")

if completion_pct < 80:            section_complete = completion_data['personal_info']        section_complete = completion_data['personal_info']

    completion_actions.append("Add professional details")

if not st.session_state.get('resume_data', {}).get('processed'):    if st.button("➕ Add Skills") and skills_input:

    completion_actions.append("Upload your resume")

        new_skills = [skill.strip() for skill in skills_input.split(',') if skill.strip()]        st.markdown(f'<div class="profile-section">', unsafe_allow_html=True)        st.markdown(f'<div class="profile-section">', unsafe_allow_html=True)

if completion_actions:

    st.sidebar.markdown("**Next Steps:**")        current_skills = profile_data.get('skills', [])

    for action in completion_actions:

        st.sidebar.write(f"• {action}")        updated_skills = list(set(current_skills + new_skills))                



# Navigation buttons        profile_data['skills'] = updated_skills

if st.sidebar.button("📊 View Dashboard", use_container_width=True):

    st.switch_page("pages/04_Dashboard.py")        st.session_state.profile_data = profile_data        st.markdown(f"### {'✅' if section_complete else '⭕'} Personal Information")        st.markdown(f"### {'✅' if section_complete else '⭕'} Personal Information")



if st.sidebar.button("📄 Resume Upload", use_container_width=True):        st.rerun()

    st.switch_page("pages/05_Resume_Upload.py")

                    

if st.sidebar.button("🎯 Find Jobs", use_container_width=True):

    st.switch_page("pages/06_Job_Match.py")    # Display current skills



# Profile tips    if profile_data.get('skills'):        with st.form("personal_info_form"):        with st.form("personal_info_form"):

st.sidebar.markdown("### 💡 Profile Tips")

st.sidebar.info("""        st.markdown("**Current Skills:**")

**Maximize Your Profile:**

• Use a professional photo        skills_html = ""            st.markdown("**Basic Details**")            st.markdown("**Basic Details**")

• Write detailed skill descriptions  

• Keep information current        for skill in profile_data['skills']:

• Add portfolio links

• Complete all optional fields            skills_html += f'<span class="skill-tag">{skill}</span>'            first_name = st.text_input("First Name", value=st.session_state.profile_data['personal_info'].get('first_name', ''))            first_name = st.text_input("First Name", value=st.session_state.profile_data['personal_info'].get('first_name', ''))

""")

        st.markdown(skills_html, unsafe_allow_html=True)

# Profile statistics

if st.session_state.profile_data:                    last_name = st.text_input("Last Name", value=st.session_state.profile_data['personal_info'].get('last_name', ''))            last_name = st.text_input("Last Name", value=st.session_state.profile_data['personal_info'].get('last_name', ''))

    st.sidebar.markdown("### 📈 Profile Stats")

            if st.button("🗑️ Clear All Skills"):

    # Calculate profile strength

    profile_strength = "Weak" if completion_pct < 50 else "Good" if completion_pct < 80 else "Strong"            profile_data['skills'] = []                        

    st.sidebar.metric("Profile Strength", profile_strength)

                st.session_state.profile_data = profile_data

    if st.session_state.profile_data.get('last_updated'):

        st.sidebar.write(f"**Last Updated:** {st.session_state.profile_data['last_updated']}")            st.rerun()            col_a, col_b = st.columns(2)            col_a, col_b = st.columns(2)



# Footer    

st.markdown("---")

st.markdown("""    st.markdown('</div>', unsafe_allow_html=True)            with col_a:            with col_a:

<div style="text-align: center; color: #666; padding: 1.5rem; background: #f8f9fa; border-radius: 10px;">

    <p><strong>IntelliCV-AI Profile Management</strong> | Your Professional Identity</p>

    <p>🔒 Secure & Private • ✏️ Always Editable • 🚀 AI-Optimized</p>

    <p>💡 <strong>Pro Tip:</strong> Complete profiles get 3x more job matches and opportunities</p>with tab3:                date_of_birth = st.date_input("Date of Birth", value=st.session_state.profile_data['personal_info'].get('date_of_birth'))                date_of_birth = st.date_input("Date of Birth", value=st.session_state.profile_data['personal_info'].get('date_of_birth'))

</div>

""", unsafe_allow_html=True)    st.markdown('<div class="profile-card">', unsafe_allow_html=True)

    st.markdown("### 🔧 Job Search Preferences")            with col_b:            with col_b:

    

    col1, col2 = st.columns(2)                nationality = st.selectbox("Nationality", [                nationality = st.selectbox("Nationality", [

    with col1:

        work_preference = st.selectbox(                    "Select...", "American", "British", "Canadian", "Australian", "German",                     "Select...", "American", "British", "Canadian", "Australian", "German", 

            "Work Preference",

            options=["", "Remote", "Hybrid", "On-site", "No preference"],                    "French", "Italian", "Spanish", "Indian", "Chinese", "Japanese", "Other"                    "French", "Italian", "Spanish", "Indian", "Chinese", "Japanese", "Other"

            index=0 if not profile_data.get('work_preference') else 

                  ["", "Remote", "Hybrid", "On-site", "No preference"].index(profile_data.get('work_preference', ''))                ], index=0)                ], index=0)

        )

                                

        # Industry interests

        industries = st.multiselect(            if st.form_submit_button("💾 Save Personal Info", use_container_width=True):            if st.form_submit_button("💾 Save Personal Info", use_container_width=True):

            "Industry Interests",

            options=["Technology", "Finance", "Healthcare", "Education", "Retail",                 if first_name and last_name:                if first_name and last_name:

                    "Manufacturing", "Consulting", "Non-profit", "Government", "Other"],

            default=profile_data.get('industries', [])                    st.session_state.profile_data['personal_info'] = {                    st.session_state.profile_data['personal_info'] = {

        )

                            'first_name': first_name,                        'first_name': first_name,

    with col2:

        job_types = st.multiselect(                        'last_name': last_name,                        'last_name': last_name,

            "Job Types",

            options=["Full-time", "Part-time", "Contract", "Freelance", "Internship"],                        'date_of_birth': date_of_birth,                        'date_of_birth': date_of_birth,

            default=profile_data.get('job_types', [])

        )                        'nationality': nationality                        'nationality': nationality

        

        company_sizes = st.multiselect(                    }                    }

            "Company Size Preference",

            options=["Startup (1-50)", "Small (51-200)", "Medium (201-1000)",                     st.session_state.profile_data['completion_status']['personal_info'] = True                    st.session_state.profile_data['completion_status']['personal_info'] = True

                    "Large (1001-5000)", "Enterprise (5000+)"],

            default=profile_data.get('company_sizes', [])                    show_success("Personal information saved!")                    show_success("Personal information saved!")

        )

                        if ERROR_HANDLER_AVAILABLE:                    if ERROR_HANDLER_AVAILABLE:

    st.markdown('</div>', unsafe_allow_html=True)

                        log_user_action("profile_personal_updated", {"user": user_name})                        log_user_action("profile_personal_updated", {"user": user_name})

with tab4:

    st.markdown('<div class="profile-card">', unsafe_allow_html=True)                    st.rerun()                    st.rerun()

    st.markdown("### 📊 Profile Summary")

                    else:                else:

    # Display all profile information

    col1, col2 = st.columns(2)                    show_error("Please fill in all required fields")                    show_error("Please fill in all required fields")

    

    with col1:                

        st.markdown("**Personal Information:**")

        st.write(f"• Name: {profile_data.get('full_name', 'Not provided')}")        st.markdown('</div>', unsafe_allow_html=True)        st.markdown('</div>', unsafe_allow_html=True)

        st.write(f"• Email: {profile_data.get('email', 'Not provided')}")

        st.write(f"• Phone: {profile_data.get('phone', 'Not provided')}")    

        st.write(f"• Location: {profile_data.get('location', 'Not provided')}")

            # Professional Information Section    on_linkedin = st.checkbox("Are you on LinkedIn?", value=bool(profile_data.get("linkedin")))

        st.markdown("**Professional Details:**")

        st.write(f"• Current Title: {profile_data.get('current_title', 'Not provided')}")    with st.container():    linkedin_url = st.text_input("LinkedIn Profile URL (optional)", value=profile_data.get("linkedin", "")) if on_linkedin else ""

        st.write(f"• Experience: {profile_data.get('experience_level', 'Not provided')}")

        st.write(f"• Salary Expectation: {profile_data.get('salary_expectation', 'Not provided')}")        section_complete = completion_data['professional_info']

    

    with col2:        st.markdown(f'<div class="profile-section">', unsafe_allow_html=True)    if on_linkedin and not linkedin_url:

        st.markdown("**Skills:**")

        if profile_data.get('skills'):                st.caption("ℹ️ If left blank, IntelliCV will attempt to auto-locate your LinkedIn profile.")

            for skill in profile_data['skills'][:10]:  # Show first 10 skills

                st.write(f"• {skill}")        st.markdown(f"### {'✅' if section_complete else '⭕'} Professional Information")

            if len(profile_data['skills']) > 10:

                st.write(f"... and {len(profile_data['skills']) - 10} more")            submitted = st.form_submit_button("Finish Profile")

        else:

            st.write("No skills added yet")        with st.form("professional_info_form"):    if submitted:

        

        st.markdown("**Preferences:**")            st.markdown("**Career Details**")        profile_result = {

        st.write(f"• Work Style: {profile_data.get('work_preference', 'Not specified')}")

        st.write(f"• Availability: {profile_data.get('availability', 'Not specified')}")            current_role = st.text_input("Current Job Title", value=st.session_state.profile_data['professional_info'].get('current_role', ''))            "name": full_name,

    

    # Profile completeness assessment            company = st.text_input("Company", value=st.session_state.profile_data['professional_info'].get('company', ''))            "email": email,

    if completion_percentage >= 80:

        st.success("🎉 Your profile is well-completed! You're ready to start using advanced features.")                        "phone": phone,

    elif completion_percentage >= 50:

        st.warning("⚡ Your profile is partially complete. Add more details to unlock all features.")            industry = st.selectbox("Industry", [            "location": location,

    else:

        st.info("🚀 Complete your profile to access personalized job matching and AI features.")                "Select...", "Technology", "Healthcare", "Finance", "Education", "Marketing",             "experience": experience,

    

    st.markdown('</div>', unsafe_allow_html=True)                "Sales", "Engineering", "Design", "Consulting", "Manufacturing", "Retail", "Other"            "business_area": business_area,



# Save button (always visible)            ], index=0)            "skills": skills,

st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 1])                        "linkedin": linkedin_url,



with col1:            experience_level = st.selectbox("Experience Level", [            "holly_suggestions": holly_suggestions

    if st.button("💾 Save Profile", type="primary", use_container_width=True):

        # Update session state with all form values                "Select...", "Entry Level (0-2 years)", "Mid Level (3-5 years)",         }

        profile_data.update({

            'full_name': full_name,                "Senior Level (6-10 years)", "Executive (10+ years)"

            'email': email,

            'phone': phone,            ], index=0)        st.session_state["profile_data"] = profile_result

            'location': location,

            'current_title': current_title,                    session.context["user_profile"] = profile_result

            'experience_level': experience_level,

            'bio': bio,            skills = st.text_area("Key Skills (comma-separated)",         session.context["profile_complete"] = True

            'linkedin': linkedin,

            'github': github,                                value=st.session_state.profile_data['professional_info'].get('skills', ''),

            'portfolio': portfolio,

            'salary_expectation': salary_expectation,                                placeholder="Python, Project Management, Data Analysis...")        st.success("✅ Profile saved. Redirecting to dashboard...")

            'availability': availability,

            'work_preference': work_preference,                    st.switch_page("pages/04_HomeDashboard.py")

            'industries': industries,

            'job_types': job_types,            if st.form_submit_button("💾 Save Professional Info", use_container_width=True):

            'company_sizes': company_sizes                if current_role and industry != "Select...":

        })                    st.session_state.profile_data['professional_info'] = {

        st.session_state.profile_data = profile_data                        'current_role': current_role,

                                'company': company,

        if ERROR_HANDLER_AVAILABLE:                        'industry': industry,

            log_user_action("profile_updated", {"completion": completion_percentage})                        'experience_level': experience_level,

                                'skills': skills

        show_success("Profile saved successfully!")                    }

        time.sleep(1)                    st.session_state.profile_data['completion_status']['professional_info'] = True

        st.rerun()                    show_success("Professional information saved!")

                    if ERROR_HANDLER_AVAILABLE:

with col2:                        log_user_action("profile_professional_updated", {"user": user_name})

    if st.button("🏠 Dashboard", use_container_width=True):                    st.rerun()

        try:                else:

            st.switch_page("pages/04_Dashboard.py")                    show_error("Please fill in current role and select industry")

        except:        

            show_error("Dashboard page not yet available")        st.markdown('</div>', unsafe_allow_html=True)



with col3:with col2:

    if completion_percentage >= 50:    # Contact Information Section

        if st.button("📄 Upload Resume", use_container_width=True):    with st.container():

            try:        section_complete = completion_data['contact_info']

                st.switch_page("pages/05_Resume_Upload.py")        st.markdown(f'<div class="profile-section">', unsafe_allow_html=True)

            except:        

                show_error("Resume upload page not yet available")        st.markdown(f"### {'✅' if section_complete else '⭕'} Contact Information")

    else:        

        st.button("📄 Upload Resume", disabled=True, use_container_width=True,         with st.form("contact_info_form"):

                 help="Complete at least 50% of your profile to access resume upload")            st.markdown("**Contact Details**")

            email = st.text_input("Email Address", value=user_email, disabled=True)

# Footer            

st.markdown("---")            # Phone number with country code

st.markdown("""            col_phone1, col_phone2 = st.columns([1, 3])

<div style="text-align: center; color: #666; padding: 1rem;">            with col_phone1:

    <p><strong>IntelliCV-AI Profile Management</strong> | Secure & Private</p>                country_code = st.selectbox("Code", [

    <p>💡 Tip: A complete profile improves job matching accuracy by up to 70%</p>                    "+1", "+44", "+33", "+49", "+39", "+34", "+61", "+91", "+86", "+81"

</div>                ], index=0)

""", unsafe_allow_html=True)            with col_phone2:
                phone = st.text_input("Phone Number", value=st.session_state.profile_data['contact_info'].get('phone', ''))
            
            city = st.text_input("City", value=st.session_state.profile_data['contact_info'].get('city', ''))
            country = st.text_input("Country", value=st.session_state.profile_data['contact_info'].get('country', ''))
            
            linkedin = st.text_input("LinkedIn Profile (optional)", 
                                   value=st.session_state.profile_data['contact_info'].get('linkedin', ''),
                                   placeholder="https://linkedin.com/in/yourname")
            
            if st.form_submit_button("💾 Save Contact Info", use_container_width=True):
                if phone and city and country:
                    st.session_state.profile_data['contact_info'] = {
                        'phone': f"{country_code} {phone}",
                        'city': city,
                        'country': country,
                        'linkedin': linkedin
                    }
                    st.session_state.profile_data['completion_status']['contact_info'] = True
                    show_success("Contact information saved!")
                    if ERROR_HANDLER_AVAILABLE:
                        log_user_action("profile_contact_updated", {"user": user_name})
                    st.rerun()
                else:
                    show_error("Please fill in phone, city, and country")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Preferences Section
    with st.container():
        section_complete = completion_data['preferences']
        st.markdown(f'<div class="profile-section">', unsafe_allow_html=True)
        
        st.markdown(f"### {'✅' if section_complete else '⭕'} Preferences & Settings")
        
        with st.form("preferences_form"):
            st.markdown("**Job Search Preferences**")
            job_types = st.multiselect("Preferred Job Types", [
                "Full-time", "Part-time", "Contract", "Freelance", "Remote", "Hybrid"
            ], default=st.session_state.profile_data['preferences'].get('job_types', []))
            
            salary_range = st.selectbox("Salary Range (Annual)", [
                "Select...", "$30k-$50k", "$50k-$75k", "$75k-$100k", 
                "$100k-$150k", "$150k-$200k", "$200k+"
            ], index=0)
            
            st.markdown("**Notification Preferences**")
            email_notifications = st.checkbox("Email notifications", 
                                            value=st.session_state.profile_data['preferences'].get('email_notifications', True))
            job_alerts = st.checkbox("Job match alerts", 
                                   value=st.session_state.profile_data['preferences'].get('job_alerts', True))
            career_tips = st.checkbox("Career tips newsletter", 
                                    value=st.session_state.profile_data['preferences'].get('career_tips', False))
            
            if st.form_submit_button("💾 Save Preferences", use_container_width=True):
                if job_types and salary_range != "Select...":
                    st.session_state.profile_data['preferences'] = {
                        'job_types': job_types,
                        'salary_range': salary_range,
                        'email_notifications': email_notifications,
                        'job_alerts': job_alerts,
                        'career_tips': career_tips
                    }
                    st.session_state.profile_data['completion_status']['preferences'] = True
                    show_success("Preferences saved!")
                    if ERROR_HANDLER_AVAILABLE:
                        log_user_action("profile_preferences_updated", {"user": user_name})
                    st.rerun()
                else:
                    show_error("Please select job types and salary range")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Action buttons based on completion status
st.markdown("---")
if completion_percentage == 100:
    st.success("🎉 **Profile Complete!** You can now access all IntelliCV features.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📄 Upload Resume", use_container_width=True):
            st.session_state['is_new_user'] = False  # Mark as existing user
            try:
                st.switch_page("pages/01_Resume_Upload_and_Analysis.py")
            except:
                show_error("Resume upload page not available - let's create it!")
                if st.button("🔧 Create Upload Page"):
                    # Redirect to create resume upload page
                    st.info("Resume upload functionality coming soon!")
    
    with col2:
        if st.button("🎯 Find Jobs", use_container_width=True):
            try:
                st.switch_page("pages/05_Job_Match.py")
            except:
                show_error("Job matching page not available yet")
    
    with col3:
        if st.button("📊 Dashboard", use_container_width=True):
            try:
                st.switch_page("pages/06_Dashboard.py")
            except:
                show_error("Dashboard page not available yet")

else:
    st.warning(f"⏳ Complete your profile ({completion_percentage}% done) to unlock all features!")
    
    if st.button("🏠 Back to Home"):
        st.switch_page("pages/00_Home.py")

# Profile summary for existing users
if not is_new_user:
    st.markdown("---")
    st.markdown("### 📋 Profile Summary")
    
    if st.session_state.profile_data['personal_info']:
        personal = st.session_state.profile_data['personal_info']
        st.write(f"**Name:** {personal.get('first_name', '')} {personal.get('last_name', '')}")
    
    if st.session_state.profile_data['professional_info']:
        professional = st.session_state.profile_data['professional_info']
        st.write(f"**Role:** {professional.get('current_role', 'Not specified')}")
        st.write(f"**Industry:** {professional.get('industry', 'Not specified')}")
    
    if st.session_state.profile_data['contact_info']:
        contact = st.session_state.profile_data['contact_info']
        st.write(f"**Location:** {contact.get('city', '')}, {contact.get('country', '')}")

# Debug info
if st.sidebar.checkbox("🔧 Debug Profile Data"):
    st.sidebar.json(st.session_state.profile_data)