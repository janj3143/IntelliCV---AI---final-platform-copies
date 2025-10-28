"""
👤 IntelliCV-AI Complete Profile Management
=========================================
DEFINITIVE VERSION: Merged best features with Enhanced AI Chatbot
- Complete profile management system
- AI-powered conversational assistant with whimsical questioning
- Career planning features and admin AI integration
- Token management and enhanced user experience
"""

import streamlit as st
from pathlib import Path
import sys
import time
import json
import random
from datetime import datetime, date

# Setup paths and imports
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

# Import token management
try:
    from token_management_system import TokenManager
    TOKEN_SYSTEM_AVAILABLE = True
except ImportError:
    TOKEN_SYSTEM_AVAILABLE = False

# Import admin AI integration
try:
    from user_portal_admin_integration import process_user_action_with_admin_ai, init_admin_ai_for_user_page
    ADMIN_AI_AVAILABLE = True
except ImportError:
    ADMIN_AI_AVAILABLE = False

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

# Page configuration
st.set_page_config(
    page_title="👤 Complete Profile Management | IntelliCV-AI",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication check
if not st.session_state.get('authenticated_user'):
    st.error("❌ Please complete registration and payment first")
    if st.button("🔙 Go to Home"):
        st.switch_page("pages/01_Home.py")
    st.stop()

# Token Management Check
if TOKEN_SYSTEM_AVAILABLE:
    token_manager = TokenManager()
    if not token_manager.check_page_access(st.session_state.get('user_id'), '08_Profile_Complete.py'):
        st.error("🪙 Insufficient tokens for Complete Profile Management (Cost: 2 tokens)")
        if st.button("💰 Get More Tokens"):
            st.switch_page("pages/05_Payment.py")
        st.stop()
    
    # Consume tokens when page is accessed
    token_manager.consume_page_tokens(st.session_state.get('user_id'), '08_Profile_Complete.py')

# AI Chatbot Class for Whimsical Questioning
class ProfileAIChatbot:
    def __init__(self):
        self.conversation_history = st.session_state.get('profile_chatbot_history', [])
        self.user_insights = st.session_state.get('profile_user_insights', {})
        
        # Whimsical question categories
        self.skill_questions = [
            "🎨 If you could have a superpower for your job, what would it be and why?",
            "🌟 What's the one thing you do that makes your colleagues go 'How did you do that?'",
            "🎭 If your skills were ingredients in a recipe, what would you be cooking up?",
            "🚀 What skill makes you feel like you're in your element - like time just flies by?",
            "💫 If you had to teach someone your favorite skill in just 5 minutes, what would you focus on?"
        ]
        
        self.location_questions = [
            "🌍 If you could work from anywhere in the world for a month, where would you go and why?",
            "🏙️ What kind of environment makes you feel most creative and productive?",
            "🌊 Are you more of a 'buzzing city energy' person or a 'peaceful countryside' type?",
            "✈️ If distance wasn't a factor, what three places would you love to have offices in?",
            "🏡 Describe your ideal workspace - is it a cozy coffee shop, a modern office, or your own special hideaway?"
        ]
        
        self.aspiration_questions = [
            "🎯 If you had a magic wand and could reshape your industry, what would you change?",
            "🌈 What does success look like to you when nobody else is watching?",
            "🎪 If your career was a movie, what genre would it be and what would the sequel be called?",
            "💭 What problem in the world makes you think 'I wish I could help solve that'?",
            "🌟 When you daydream about your ideal workday, what are you actually doing?"
        ]
        
        self.personality_questions = [
            "🎨 Are you more of a 'let's plan everything' or 'let's see what happens' kind of person?",
            "🤝 Do you energize by working with people or by having focused solo time?",
            "🧩 What type of challenges get you excited vs. the ones that make you groan?",
            "📚 How do you like to learn new things - by reading, doing, watching, or discussing?",
            "💡 When you have a great idea, do you want to share it immediately or polish it first?"
        ]
    
    def get_random_question(self, category):
        """Get a random question from specified category"""
        questions = getattr(self, f"{category}_questions", [])
        return random.choice(questions) if questions else "Tell me more about yourself!"
    
    def analyze_response(self, response, category):
        """Analyze user response for insights"""
        insights = {
            'response_length': len(response),
            'enthusiasm_level': self.detect_enthusiasm(response),
            'creativity_indicators': self.detect_creativity(response),
            'category': category,
            'timestamp': datetime.now().isoformat()
        }
        
        # Store insights
        if category not in self.user_insights:
            self.user_insights[category] = []
        self.user_insights[category].append(insights)
        
        st.session_state['profile_user_insights'] = self.user_insights
        return insights
    
    def detect_enthusiasm(self, text):
        """Detect enthusiasm level in response"""
        enthusiasm_words = ['love', 'excited', 'amazing', 'awesome', 'fantastic', 'incredible', 'passion']
        enthusiasm_score = sum(1 for word in enthusiasm_words if word.lower() in text.lower())
        exclamations = text.count('!')
        return min(enthusiasm_score + exclamations, 10)
    
    def detect_creativity(self, text):
        """Detect creativity indicators in response"""
        creative_words = ['imagine', 'create', 'design', 'innovate', 'unique', 'different', 'new', 'original']
        return sum(1 for word in creative_words if word.lower() in text.lower())
    
    def generate_follow_up(self, response, category):
        """Generate intelligent follow-up based on response"""
        insights = self.analyze_response(response, category)
        
        follow_ups = {
            'skill': [
                "That's fascinating! How did you first discover this talent?",
                "I can sense your passion! What challenges you most in this area?",
                "Interesting perspective! How do you think this skill will evolve in the future?"
            ],
            'location': [
                "What a wonderful choice! What draws you to that kind of environment?",
                "I love your vision! How does location impact your creativity?",
                "That sounds perfect for you! What would your typical day look like there?"
            ],
            'aspiration': [
                "Your ambition is inspiring! What first sparked this vision?",
                "What an impactful goal! What steps are you taking toward this?",
                "I can feel your passion! Who or what influences this dream most?"
            ],
            'personality': [
                "That really shows your authentic self! How has this shaped your career?",
                "Your self-awareness is impressive! How do others respond to this trait?",
                "What a great insight! How do you leverage this in your work?"
            ]
        }
        
        return random.choice(follow_ups.get(category, ["Tell me more about that!"]))

# Initialize chatbot
@st.cache_resource
def get_chatbot():
    return ProfileAIChatbot()

# Main Application
def main():
    # Header with branding
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='color: #2E86AB; margin-bottom: 0.5rem;'>👤 Complete Profile Management</h1>
        <p style='color: #666; font-size: 1.1rem; margin-bottom: 2rem;'>
            Build your professional profile with AI-powered assistance
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'profile_complete' not in st.session_state:
        st.session_state.profile_complete = False
    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = {}

    # Tab selection
    tab1, tab2, tab3 = st.tabs(["📋 Basic Profile", "🤖 AI Chat Assistant", "📊 Profile Insights"])
    
    with tab1:
        basic_profile_section()
    
    with tab2:
        ai_chatbot_section()
    
    with tab3:
        profile_insights_section()

def basic_profile_section():
    """Basic profile information collection"""
    st.header("📋 Essential Profile Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Personal Details")
        first_name = st.text_input("First Name", value=st.session_state.profile_data.get('first_name', ''))
        last_name = st.text_input("Last Name", value=st.session_state.profile_data.get('last_name', ''))
        email = st.text_input("Email", value=st.session_state.profile_data.get('email', ''))
        phone = st.text_input("Phone", value=st.session_state.profile_data.get('phone', ''))
        
        st.subheader("Location Preferences")
        current_location = st.text_input("Current Location", value=st.session_state.profile_data.get('current_location', ''))
        preferred_locations = st.text_area("Preferred Work Locations", value=st.session_state.profile_data.get('preferred_locations', ''))
        remote_preference = st.selectbox("Remote Work Preference", 
                                       ["Fully Remote", "Hybrid", "On-site", "Flexible"], 
                                       index=0)
    
    with col2:
        st.subheader("Professional Details")
        current_role = st.text_input("Current Job Title", value=st.session_state.profile_data.get('current_role', ''))
        experience_level = st.selectbox("Experience Level", 
                                      ["Entry Level", "Mid Level", "Senior Level", "Executive", "Student/Graduate"],
                                      index=0)
        industry = st.selectbox("Industry", 
                              ["Technology", "Finance", "Healthcare", "Education", "Marketing", "Other"],
                              index=0)
        skills = st.text_area("Key Skills (comma-separated)", value=st.session_state.profile_data.get('skills', ''))
        
        st.subheader("Career Goals")
        career_goals = st.text_area("Career Goals & Aspirations", value=st.session_state.profile_data.get('career_goals', ''))
    
    # Save profile data
    if st.button("💾 Save Profile Information", type="primary"):
        profile_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'current_location': current_location,
            'preferred_locations': preferred_locations,
            'remote_preference': remote_preference,
            'current_role': current_role,
            'experience_level': experience_level,
            'industry': industry,
            'skills': skills,
            'career_goals': career_goals,
            'last_updated': datetime.now().isoformat()
        }
        
        st.session_state.profile_data = profile_data
        show_success("Profile information saved successfully!")
        
        # Log action
        if ERROR_HANDLER_AVAILABLE:
            log_user_action("profile_saved", {"user_id": st.session_state.get('user_id')})

def ai_chatbot_section():
    """AI-powered conversational profile building"""
    st.header("🤖 AI Chat Assistant")
    
    chatbot = get_chatbot()
    
    # Chat categories
    categories = ['skill', 'location', 'aspiration', 'personality']
    selected_category = st.selectbox("Choose a conversation topic:", 
                                   ['Skills & Talents', 'Location & Environment', 'Goals & Aspirations', 'Personality & Style'])
    
    category_map = {
        'Skills & Talents': 'skill',
        'Location & Environment': 'location', 
        'Goals & Aspirations': 'aspiration',
        'Personality & Style': 'personality'
    }
    
    current_category = category_map[selected_category]
    
    # Display current question
    if f'current_{current_category}_question' not in st.session_state:
        st.session_state[f'current_{current_category}_question'] = chatbot.get_random_question(current_category)
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;'>
        <h4 style='margin: 0; color: white;'>💭 AI Assistant asks:</h4>
        <p style='margin: 0.5rem 0 0 0; font-size: 1.1rem;'>{st.session_state[f'current_{current_category}_question']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User response
    user_response = st.text_area("Your response:", height=150, 
                                placeholder="Share your thoughts freely - be as creative and detailed as you'd like!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💬 Submit Response", type="primary"):
            if user_response.strip():
                # Analyze response
                insights = chatbot.analyze_response(user_response, current_category)
                
                # Generate follow-up
                follow_up = chatbot.generate_follow_up(user_response, current_category)
                
                # Save conversation
                conversation_entry = {
                    'category': current_category,
                    'question': st.session_state[f'current_{current_category}_question'],
                    'response': user_response,
                    'insights': insights,
                    'timestamp': datetime.now().isoformat()
                }
                
                chatbot.conversation_history.append(conversation_entry)
                st.session_state['profile_chatbot_history'] = chatbot.conversation_history
                
                show_success("Response recorded! Here's a follow-up thought...")
                st.info(f"🤖 {follow_up}")
                
                # Log action
                if ERROR_HANDLER_AVAILABLE:
                    log_user_action("ai_chat_response", {"category": current_category, "response_length": len(user_response)})
            else:
                show_error("Please provide a response before submitting.")
    
    with col2:
        if st.button("🎲 Get New Question"):
            st.session_state[f'current_{current_category}_question'] = chatbot.get_random_question(current_category)
            st.rerun()
    
    # Display conversation history for current category
    if chatbot.conversation_history:
        st.subheader("💭 Your Conversation History")
        category_history = [entry for entry in chatbot.conversation_history if entry['category'] == current_category]
        
        for entry in category_history[-3:]:  # Show last 3 entries
            with st.expander(f"Question: {entry['question'][:50]}..."):
                st.write(f"**Your Response:** {entry['response']}")
                st.write(f"**Enthusiasm Level:** {entry['insights']['enthusiasm_level']}/10")
                st.write(f"**Creativity Indicators:** {entry['insights']['creativity_indicators']}")

def profile_insights_section():
    """Display AI-generated insights about user profile"""
    st.header("📊 Your Profile Insights")
    
    if 'profile_user_insights' in st.session_state and st.session_state['profile_user_insights']:
        insights = st.session_state['profile_user_insights']
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_responses = sum(len(category_data) for category_data in insights.values())
        avg_enthusiasm = 0
        total_creativity = 0
        
        if total_responses > 0:
            all_entries = []
            for category_data in insights.values():
                all_entries.extend(category_data)
            
            avg_enthusiasm = sum(entry['enthusiasm_level'] for entry in all_entries) / len(all_entries)
            total_creativity = sum(entry['creativity_indicators'] for entry in all_entries)
        
        with col1:
            st.metric("Total Responses", total_responses)
        with col2:
            st.metric("Avg Enthusiasm", f"{avg_enthusiasm:.1f}/10")
        with col3:
            st.metric("Creativity Score", total_creativity)
        with col4:
            completion = min((total_responses / 12) * 100, 100)  # 3 responses per category
            st.metric("Profile Completion", f"{completion:.0f}%")
        
        # Category breakdown
        st.subheader("🎯 Insights by Category")
        
        for category, data in insights.items():
            with st.expander(f"{category.title()} Insights ({len(data)} responses)"):
                if data:
                    avg_category_enthusiasm = sum(entry['enthusiasm_level'] for entry in data) / len(data)
                    category_creativity = sum(entry['creativity_indicators'] for entry in data)
                    
                    st.write(f"**Average Enthusiasm:** {avg_category_enthusiasm:.1f}/10")
                    st.write(f"**Creativity Indicators:** {category_creativity}")
                    st.write(f"**Response Pattern:** {len(data)} thoughtful responses")
                    
                    # Show most recent response
                    if data:
                        latest = data[-1]
                        st.write(f"**Latest Response Length:** {latest['response_length']} characters")
    else:
        st.info("💡 Start chatting with our AI assistant to see your profile insights here!")
        
        # Helpful tips
        st.markdown("""
        ### 🌟 Tips for Better Insights:
        - **Be detailed**: Longer responses give us more to work with
        - **Be honest**: Authentic responses lead to better matches
        - **Be creative**: Use metaphors and stories to express yourself
        - **Try all categories**: Each provides unique insights about you
        """)

    # Profile completion status
    if st.session_state.get('profile_data') and st.session_state.get('profile_chatbot_history'):
        st.success("🎉 Your profile is looking great! Ready to upload your resume?")
        if st.button("📄 Continue to Resume Upload", type="primary"):
            st.switch_page("pages/27_Resume_Upload_Instant_Analysis.py")

if __name__ == "__main__":
    main()