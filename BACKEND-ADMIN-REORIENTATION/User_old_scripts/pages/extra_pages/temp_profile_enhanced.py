#!/usr/bin/env python3
"""
👤 IntelliCV-AI Enhanced User Profile
Complete profile management with career planning features and admin AI integration
"""

import streamlit as st
import json
from datetime import datetime
from pathlib import Path

# Setup paths and imports
current_dir = Path(__file__).parent.parent
import sys
sys.path.insert(0, str(current_dir))

# Import admin AI integration
try:
    from user_portal_admin_integration import process_user_action_with_admin_ai, init_admin_ai_for_user_page
    ADMIN_AI_AVAILABLE = True
except ImportError:
    ADMIN_AI_AVAILABLE = False

# Import utilities with fallbacks
try:
    from utils.error_handler import log_user_action, show_error, show_success, show_warning
    ERROR_HANDLER_AVAILABLE = True
except ImportError:
    ERROR_HANDLER_AVAILABLE = False
    def log_user_action(action, details=None): pass
    def show_error(msg): st.error(f"❌ {msg}")
    def show_success(msg): st.success(f"✅ {msg}")
    def show_warning(msg): st.warning(f"⚠️ {msg}")

# Page configuration
st.set_page_config(
    page_title="👤 My Profile | IntelliCV-AI", 
    page_icon="👤",
    layout="wide"
)

# Initialize session state for profile
def init_profile_session():
    """Initialize profile session state"""
    if "profile_data" not in st.session_state:
        st.session_state.profile_data = {}
    if "profile_completed" not in st.session_state:
        st.session_state.profile_completed = False

init_profile_session()

# Professional CSS styling
st.markdown("""
<style>
.profile-section {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    padding: 2rem;
    border-radius: 15px;
    margin: 1rem 0;
    border: 1px solid #cbd5e1;
}

.form-section {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.career-insights {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
}

.profile-stats {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
}

.progress-bar {
    background: #e5e7eb;
    border-radius: 10px;
    height: 20px;
    margin: 0.5rem 0;
}

.progress-fill {
    background: linear-gradient(90deg, #3b82f6, #10b981);
    height: 100%;
    border-radius: 10px;
    transition: width 0.3s ease;
}
</style>
""", unsafe_allow_html=True)

def calculate_profile_completeness():
    """Calculate profile completion percentage"""
    profile = st.session_state.profile_data
    required_fields = [
        'full_name', 'email', 'phone', 'address', 'current_salary', 
        'salary_expectations', 'linkedin_url', 'commute_preference'
    ]
    
    completed = sum(1 for field in required_fields if profile.get(field))
    return (completed / len(required_fields)) * 100

def show_profile_header():
    """Display profile header with completion stats"""
    completion = calculate_profile_completeness()
    
    st.markdown(f"""
    <div class="profile-section">
        <h1 style="color: #1f2937; margin-bottom: 1rem;">
            👤 My IntelliCV Profile
        </h1>
        <div class="profile-stats">
            <h3>Profile Completion: {completion:.0f}%</h3>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {completion}%"></div>
            </div>
            <p style="margin-top: 0.5rem;">
                {"🎉 Profile Complete!" if completion >= 80 else "📝 Complete your profile for better job matches"}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_basic_information():
    """Basic personal information section"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 📋 Basic Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        full_name = st.text_input(
            "Full Name *", 
            value=st.session_state.profile_data.get('full_name', ''),
            key="profile_full_name"
        )
        email = st.text_input(
            "Email Address *", 
            value=st.session_state.profile_data.get('email', ''),
            key="profile_email"
        )
        phone = st.text_input(
            "Contact Number *", 
            value=st.session_state.profile_data.get('phone', ''),
            key="profile_phone"
        )
        
    with col2:
        address = st.text_area(
            "Home Address *", 
            value=st.session_state.profile_data.get('address', ''),
            height=120,
            key="profile_address"
        )
    
    linkedin_url = st.text_input(
        "LinkedIn Profile URL *", 
        value=st.session_state.profile_data.get('linkedin_url', ''),
        placeholder="https://linkedin.com/in/your-profile",
        key="profile_linkedin"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {
        'full_name': full_name,
        'email': email, 
        'phone': phone,
        'address': address,
        'linkedin_url': linkedin_url
    }

def show_employment_information():
    """Employment and salary information"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 💼 Employment & Compensation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_salary = st.number_input(
            "Current Salary (Annual) *",
            min_value=0,
            value=st.session_state.profile_data.get('current_salary', 0),
            step=1000,
            key="profile_current_salary"
        )
        
        salary_expectations = st.number_input(
            "Salary Expectations (Annual) *",
            min_value=0,
            value=st.session_state.profile_data.get('salary_expectations', 0),
            step=1000,
            key="profile_salary_expectations"
        )
    
    with col2:
        health_plan = st.selectbox(
            "Health Plan Preference",
            ["Not Important", "Basic Coverage", "Comprehensive Coverage", "Family Coverage"],
            index=["Not Important", "Basic Coverage", "Comprehensive Coverage", "Family Coverage"].index(
                st.session_state.profile_data.get('health_plan', 'Not Important')
            ),
            key="profile_health_plan"
        )
        
        pension_plan = st.selectbox(
            "Pension/401k Preference", 
            ["Not Important", "Basic 401k", "Company Match Required", "High Match Required"],
            index=["Not Important", "Basic 401k", "Company Match Required", "High Match Required"].index(
                st.session_state.profile_data.get('pension_plan', 'Not Important')
            ),
            key="profile_pension"
        )
    
    car_allowance = st.selectbox(
        "Car/Transport Allowance",
        ["Not Required", "Car Allowance Preferred", "Company Car Required", "Public Transport Subsidy"],
        index=["Not Required", "Car Allowance Preferred", "Company Car Required", "Public Transport Subsidy"].index(
            st.session_state.profile_data.get('car_allowance', 'Not Required')
        ),
        key="profile_car"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {
        'current_salary': current_salary,
        'salary_expectations': salary_expectations,
        'health_plan': health_plan,
        'pension_plan': pension_plan,
        'car_allowance': car_allowance
    }

def show_location_preferences():
    """Location and commute preferences"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 🌍 Location & Commute Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        commute_distance = st.slider(
            "Maximum Commute Distance (miles)",
            min_value=0,
            max_value=100,
            value=st.session_state.profile_data.get('commute_distance', 25),
            key="profile_commute_distance"
        )
        
        commute_time = st.slider(
            "Maximum Commute Time (minutes)",
            min_value=0,
            max_value=120,
            value=st.session_state.profile_data.get('commute_time', 45),
            key="profile_commute_time"
        )
    
    with col2:
        relocation_willingness = st.selectbox(
            "Relocation Willingness",
            ["No Relocation", "Same City/Region", "Within Country", "International"],
            index=["No Relocation", "Same City/Region", "Within Country", "International"].index(
                st.session_state.profile_data.get('relocation_willingness', 'No Relocation')
            ),
            key="profile_relocation"
        )
        
        preferred_locations = st.text_input(
            "Preferred Relocation Areas (if applicable)",
            value=st.session_state.profile_data.get('preferred_locations', ''),
            placeholder="e.g., New York, London, remote",
            key="profile_preferred_locations"
        )
    
    partner_employment = st.text_input(
        "Partner's Employment Status & Role (for relocation planning)",
        value=st.session_state.profile_data.get('partner_employment', ''),
        placeholder="e.g., Teacher - flexible, Software Engineer - remote capable",
        key="profile_partner_employment"
    )
    
    commute_preference = st.radio(
        "Commute Preference *",
        ["Office-based", "Hybrid (2-3 days office)", "Mostly Remote", "Fully Remote"],
        index=["Office-based", "Hybrid (2-3 days office)", "Mostly Remote", "Fully Remote"].index(
            st.session_state.profile_data.get('commute_preference', 'Hybrid (2-3 days office)')
        ),
        key="profile_commute_pref"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {
        'commute_distance': commute_distance,
        'commute_time': commute_time,
        'relocation_willingness': relocation_willingness,
        'preferred_locations': preferred_locations,
        'partner_employment': partner_employment,
        'commute_preference': commute_preference
    }

def show_security_settings():
    """Security and password recovery"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 🔐 Security & Recovery Settings")
    
    security_word = st.text_input(
        "Security Word (for password recovery)",
        value=st.session_state.profile_data.get('security_word', ''),
        type="password",
        help="This will be used for password recovery - choose something memorable",
        key="profile_security_word"
    )
    
    st.info("🔗 This will be linked with our password manager for secure credential storage")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {'security_word': security_word}

def show_career_aspirations():
    """Career aspirations and preferences"""
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 🚀 Career Aspirations & Preferences")
    
    # Free-form expression box
    personal_statement = st.text_area(
        "Tell us about yourself and your career goals",
        value=st.session_state.profile_data.get('personal_statement', ''),
        height=150,
        placeholder="Share your thoughts about your career journey, aspirations, and what makes you unique...",
        key="profile_personal_statement"
    )
    
    # Career questions
    st.markdown("#### 💭 Quick Career Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        career_vision = st.text_area(
            "Where do you see yourself in 5 years?",
            value=st.session_state.profile_data.get('career_vision', ''),
            height=100,
            key="profile_career_vision"
        )
        
        preferred_role = st.text_input(
            "What's your ideal role/title?",
            value=st.session_state.profile_data.get('preferred_role', ''),
            key="profile_preferred_role"
        )
        
        location_importance = st.radio(
            "How important is location to you?",
            ["Not important", "Somewhat important", "Very important", "Deal breaker"],
            index=["Not important", "Somewhat important", "Very important", "Deal breaker"].index(
                st.session_state.profile_data.get('location_importance', 'Somewhat important')
            ),
            key="profile_location_importance"
        )
    
    with col2:
        management_style = st.text_area(
            "What type of manager do you work best with?",
            value=st.session_state.profile_data.get('management_style', ''),
            height=100,
            key="profile_management_style"
        )
        
        team_preference = st.radio(
            "Do you prefer working in teams?",
            ["Love teamwork", "Enjoy collaboration", "Mixed preference", "Prefer independent work"],
            index=["Love teamwork", "Enjoy collaboration", "Mixed preference", "Prefer independent work"].index(
                st.session_state.profile_data.get('team_preference', 'Enjoy collaboration')
            ),
            key="profile_team_preference"
        )
        
        peer_respect = st.radio(
            "How do you build respect with peers?",
            ["Through expertise", "Through collaboration", "Through leadership", "Through reliability"],
            index=["Through expertise", "Through collaboration", "Through leadership", "Through reliability"].index(
                st.session_state.profile_data.get('peer_respect', 'Through collaboration')
            ),
            key="profile_peer_respect"
        )
    
    # Current workplace insights
    st.markdown("#### 🏢 Current Workplace Insights")
    
    workplace_likes = st.text_area(
        "What do you like about your current/previous workplace?",
        value=st.session_state.profile_data.get('workplace_likes', ''),
        height=80,
        key="profile_workplace_likes"
    )
    
    workplace_dislikes = st.text_area(
        "What would you change about your current/previous workplace?",
        value=st.session_state.profile_data.get('workplace_dislikes', ''),
        height=80,
        key="profile_workplace_dislikes"
    )
    
    # Technical skills and keywords
    technical_keywords = st.text_area(
        "Additional technical skills/keywords (beyond your CV)",
        value=st.session_state.profile_data.get('technical_keywords', ''),
        height=80,
        placeholder="e.g., Python, Project Management, Agile, Leadership, Azure, etc.",
        help="Add skills that describe your technical abilities or current role that might not be prominently featured in your CV",
        key="profile_technical_keywords"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {
        'personal_statement': personal_statement,
        'career_vision': career_vision,
        'preferred_role': preferred_role,
        'location_importance': location_importance,
        'management_style': management_style,
        'team_preference': team_preference,
        'peer_respect': peer_respect,
        'workplace_likes': workplace_likes,
        'workplace_dislikes': workplace_dislikes,
        'technical_keywords': technical_keywords
    }

def save_profile_data(profile_data):
    """Save profile data to session state and potentially to file"""
    st.session_state.profile_data.update(profile_data)
    st.session_state.profile_completed = True
    
    # Save to local file for persistence (optional)
    try:
        profile_file = Path("user_profiles") / f"{st.session_state.get('user_id', 'default')}_profile.json"
        profile_file.parent.mkdir(exist_ok=True)
        
        with open(profile_file, 'w') as f:
            json.dump(st.session_state.profile_data, f, indent=2, default=str)
            
    except Exception as e:
        st.warning(f"Profile saved to session but couldn't save to file: {e}")

def main():
    """Main profile management interface"""
    # Check if user is authenticated
    if not st.session_state.get("authenticated_user"):
        st.warning("🔐 Please log in to access your profile")
        st.stop()
    
    # Initialize Admin AI Integration
    if ADMIN_AI_AVAILABLE:
        admin_ai = init_admin_ai_for_user_page()
        st.sidebar.success("🚀 Admin AI Integration: ACTIVE")
        st.sidebar.info("Enhanced profile analysis with admin career intelligence systems")
    else:
        st.sidebar.warning("⚠️ Admin AI Integration: NOT AVAILABLE")
        st.sidebar.error("Basic profile management only")
    
    # Show profile header
    show_profile_header()
    
    # Main profile form
    with st.form("comprehensive_profile_form", clear_on_submit=False):
        # Collect all profile sections
        basic_info = show_basic_information()
        employment_info = show_employment_information()
        location_prefs = show_location_preferences()
        security_settings = show_security_settings()
        career_aspirations = show_career_aspirations()
        
        # Form submission
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            submitted = st.form_submit_button(
                "💾 Save Profile", 
                use_container_width=True,
                type="primary"
            )
        
        if submitted:
            # Combine all profile data
            complete_profile = {
                **basic_info,
                **employment_info, 
                **location_prefs,
                **security_settings,
                **career_aspirations,
                'last_updated': datetime.now().isoformat()
            }
            
            # Validate required fields
            required_fields = ['full_name', 'email', 'phone', 'address', 'commute_preference']
            missing_fields = [field for field in required_fields if not complete_profile.get(field)]
            
            if missing_fields:
                st.error(f"❌ Please fill in required fields: {', '.join(missing_fields)}")
            else:
                save_profile_data(complete_profile)
                st.success("🎉 Profile saved successfully!")
                st.balloons()
                
                # Show completion message
                completion = calculate_profile_completeness()
                if completion >= 80:
                    st.success("✅ Your profile is complete! You'll get better job matches now.")
                else:
                    st.info(f"📈 Profile is {completion:.0f}% complete. Consider filling in more details for better results.")
    
    # Show AI insights if profile is substantial
    if calculate_profile_completeness() >= 50:
        st.markdown("""
        <div class="career-insights">
            <h3>🤖 AI Career Insights</h3>
            <p>Based on your profile, we'll provide personalized job recommendations and career guidance. 
            Keep your profile updated to get the most relevant opportunities!</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()