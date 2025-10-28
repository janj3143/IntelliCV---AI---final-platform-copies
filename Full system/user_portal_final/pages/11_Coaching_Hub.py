"""
🎓 Coaching Hub - Your Comprehensive Career Coaching Center
===========================================================
Unified coaching platform with AI-powered specialists:
- 🎤 Interview Coach: Interview preparation, Q&A practice, performance feedback
- 📊 Career Coach: Career planning, skill development, trajectory optimization
- 🤝 Mentorship Coach: Mentor matching, session management, growth tracking

Each coach includes dedicated AI chatbot for personalized guidance.

Token Cost: 15 tokens | Premium Feature
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from pathlib import Path
import json
import sys

# Setup paths
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

# Import portal bridge for cross-portal communication
try:
    from shared_backend.services.portal_bridge import ChatService
    chat_service = ChatService()
    PORTAL_BRIDGE_AVAILABLE = True
except ImportError as e:
    PORTAL_BRIDGE_AVAILABLE = False
    chat_service = None

# Page configuration
st.set_page_config(
    page_title="🎓 Coaching Hub | IntelliCV-AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication check
if not st.session_state.get('authenticated_user'):
    st.error("🔒 Please log in to access Coaching Hub")
    if st.button("🏠 Return to Home"):
        st.switch_page("main.py")
    st.stop()

# Tier check for premium features
user_tier = st.session_state.get('subscription_tier', 'free')
PREMIUM_TIERS = ['monthly_pro', 'annual_pro', 'enterprise_pro']

if user_tier not in PREMIUM_TIERS:
    st.warning("⭐ Coaching Hub requires Premium subscription (£99/month or £299/year)")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⬆️ Upgrade to Premium", type="primary", use_container_width=True):
            st.switch_page("pages/06_Pricing.py")
    st.stop()

# Initialize coaching session state
if 'coaching_state' not in st.session_state:
    st.session_state.coaching_state = {
        'active_coach': 'interview',
        'interview_sessions': [],
        'career_plans': [],
        'mentorship_connections': [],
        'chat_history': {
            'interview': [],
            'career': [],
            'mentorship': []
        }
    }

# Title and introduction
st.title("🎓 Coaching Hub")
st.markdown("""
### Your Personal Career Development Center
Access specialized AI coaches for interview preparation, career planning, and mentorship guidance.
Each coach includes a dedicated chatbot for 24/7 personalized support.
""")

# Token cost display
st.info("💎 **Token Cost: 15 tokens** | Includes unlimited coach access + AI chatbot interactions")

# Quick metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🎤 Interview Preps", "12", "+3", help="Total interview coaching sessions")
with col2:
    st.metric("📊 Career Plans", "5", "+1", help="Active career development plans")
with col3:
    st.metric("🤝 Mentorship Hours", "24h", "+6h", help="Total mentorship engagement")
with col4:
    st.metric("⭐ Success Rate", "87%", "+5%", help="Goal achievement rate")

st.markdown("---")

# Navigation tabs for coaching specialists
tab1, tab2, tab3 = st.tabs([
    "🎤 Interview Coach", 
    "📊 Career Coach", 
    "🤝 Mentorship Coach"
])

# ===========================
# TAB 1: INTERVIEW COACH
# ===========================
with tab1:
    st.header("🎤 Interview Coach")
    st.markdown("**AI-powered interview preparation with real-time practice and feedback**")
    
    # Interview Coach sections
    subtab1, subtab2, subtab3, subtab4 = st.tabs([
        "💬 Chat with Coach",
        "📋 Interview Prep",
        "🎯 Practice Sessions",
        "📊 Performance Analytics"
    ])
    
    with subtab1:
        st.subheader("💬 Interview Coach Chatbot")
        st.markdown("Ask your interview coach anything about preparation, strategies, or specific questions.")
        
        # Initialize interview chatbot history
        if 'interview' not in st.session_state.coaching_state['chat_history']:
            st.session_state.coaching_state['chat_history']['interview'] = [
                {"role": "assistant", "content": "👋 Hi! I'm your AI Interview Coach. I can help you prepare for interviews, practice common questions, and provide feedback on your responses. What interview are you preparing for?"}
            ]
        
        # Display chat messages
        for message in st.session_state.coaching_state['chat_history']['interview']:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about interview preparation, common questions, strategies..."):
            # Add user message
            st.session_state.coaching_state['chat_history']['interview'].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # AI response using portal_bridge ChatService
            if PORTAL_BRIDGE_AVAILABLE and chat_service:
                try:
                    # Get context from session state
                    context = {
                        "coach_type": "interview",
                        "user_tier": user_tier,
                        "resume_data": st.session_state.get('resume_data', {}),
                        "target_role": st.session_state.get('target_job_title', 'Not specified')
                    }
                    
                    # Call admin AI chatbot via portal_bridge
                    response = chat_service.ask(
                        question=prompt,
                        context=context,
                        conversation_history=st.session_state.coaching_state['chat_history']['interview']
                    )
                    
                    # Display AI response
                    with st.chat_message("assistant"):
                        st.markdown(response)
                    
                    # Add to chat history
                    st.session_state.coaching_state['chat_history']['interview'].append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    # Fallback response if portal_bridge fails
                    st.error(f"⚠️ AI Coach temporarily unavailable: {str(e)}")
                    fallback_response = "I apologize, but I'm having trouble connecting to the coaching system. Please try again in a moment."
                    with st.chat_message("assistant"):
                        st.markdown(fallback_response)
                    st.session_state.coaching_state['chat_history']['interview'].append({"role": "assistant", "content": fallback_response})
            else:
                # Demo response (offline mode)
                interview_tips = [
                    "Excellent question! For behavioral questions, always use the STAR method (Situation, Task, Action, Result). Let me give you an example...",
                    "Great! When preparing for technical interviews, focus on these key areas: problem-solving approach, code quality, and communication...",
                    "That's a common concern. Here's my recommendation: Practice with real interview questions from your target company...",
                    "Perfect timing to discuss this! Mock interviews are crucial. Let me set up a practice session for you..."
                ]
                response = interview_tips[len(st.session_state.coaching_state['chat_history']['interview']) % len(interview_tips)]
            
            st.session_state.coaching_state['chat_history']['interview'].append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
        
        # Quick action buttons
        st.markdown("---")
        st.markdown("**🚀 Quick Actions**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📚 Common Questions Library", use_container_width=True):
                st.session_state.coaching_state['chat_history']['interview'].append({
                    "role": "assistant", 
                    "content": "Here are the top 20 most common interview questions with sample answers..."
                })
                st.rerun()
        with col2:
            if st.button("🎯 STAR Method Guide", use_container_width=True):
                st.session_state.coaching_state['chat_history']['interview'].append({
                    "role": "assistant",
                    "content": "**STAR Method Framework:**\n\n**S**ituation: Set the context\n**T**ask: Describe your responsibility\n**A**ction: Explain what you did\n**R**esult: Share the outcome\n\nLet's practice with an example..."
                })
                st.rerun()
        with col3:
            if st.button("🔄 Start Mock Interview", use_container_width=True):
                st.session_state.coaching_state['chat_history']['interview'].append({
                    "role": "assistant",
                    "content": "Great! Let's start your mock interview. I'll ask you 10 questions. Ready? Here's the first: 'Tell me about yourself.'"
                })
                st.rerun()
    
    with subtab2:
        st.subheader("📋 Interview Preparation Hub")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 🎯 Upcoming Interviews")
            
            # Add new interview
            with st.expander("➕ Add Interview", expanded=False):
                int_company = st.text_input("Company", placeholder="e.g., Google, Amazon")
                int_position = st.text_input("Position", placeholder="e.g., Senior ML Engineer")
                int_date = st.date_input("Interview Date")
                int_type = st.selectbox("Interview Type", [
                    "Phone Screen", "Technical", "Behavioral", "System Design", 
                    "Coding Challenge", "Panel", "Final Round"
                ])
                
                if st.button("💾 Save Interview", type="primary"):
                    st.success("✅ Interview added to preparation schedule!")
            
            # Interview list
            st.markdown("---")
            interviews_data = [
                {
                    "Company": "TechCorp AI",
                    "Position": "Senior ML Engineer",
                    "Date": "2025-10-30",
                    "Type": "Technical",
                    "Status": "🟡 Preparing"
                },
                {
                    "Company": "FinTech Innovations",
                    "Position": "Data Science Lead",
                    "Date": "2025-11-02",
                    "Type": "Panel",
                    "Status": "🟢 Ready"
                }
            ]
            df_interviews = pd.DataFrame(interviews_data)
            st.dataframe(df_interviews, use_container_width=True)
        
        with col2:
            st.markdown("#### 📚 Preparation Materials")
            
            prep_category = st.selectbox("Category", [
                "Company Research", "Technical Questions", "Behavioral Questions",
                "System Design", "Coding Practice", "Case Studies"
            ])
            
            if prep_category == "Technical Questions":
                st.markdown("**🔹 Top Technical Questions**")
                st.markdown("""
                1. Explain machine learning fundamentals
                2. Difference between supervised and unsupervised learning
                3. How do you handle imbalanced datasets?
                4. Explain overfitting and how to prevent it
                5. Walk through your ML pipeline design
                """)
            elif prep_category == "Behavioral Questions":
                st.markdown("**🔹 Top Behavioral Questions**")
                st.markdown("""
                1. Tell me about a challenging project
                2. Describe a time you failed and what you learned
                3. How do you handle tight deadlines?
                4. Give an example of leadership
                5. Conflict resolution experience
                """)
            
            st.markdown("---")
            st.markdown("**📖 Resources**")
            st.markdown("- [Interview question bank (347 questions)](#)")
            st.markdown("- [Company interview guides](#)")
            st.markdown("- [Video tutorials](#)")
    
    with subtab3:
        st.subheader("🎯 Practice Sessions & Mock Interviews")
        
        st.markdown("#### 🎬 Start New Practice Session")
        
        col1, col2 = st.columns(2)
        with col1:
            practice_type = st.selectbox("Session Type", [
                "Quick Practice (5 questions)",
                "Standard Mock (10 questions)",
                "Full Interview (20 questions)",
                "Custom Session"
            ])
        with col2:
            focus_area = st.selectbox("Focus Area", [
                "Technical Skills",
                "Behavioral/STAR",
                "Company-Specific",
                "Mixed (Balanced)"
            ])
        
        if st.button("🚀 Start Practice Session", type="primary", use_container_width=True):
            with st.spinner("Preparing your practice session..."):
                st.success("✅ Practice session ready! Check the Interview Coach chatbot for your first question.")
                st.session_state.coaching_state['chat_history']['interview'].append({
                    "role": "assistant",
                    "content": f"🎯 **{practice_type} - {focus_area}**\n\nLet's begin! I'll ask questions and provide feedback on your responses.\n\n**Question 1**: Tell me about a time you had to learn a new technology quickly to complete a project."
                })
        
        st.markdown("---")
        st.markdown("#### 📊 Recent Practice Sessions")
        
        sessions_data = [
            {"Date": "2025-10-25", "Type": "Standard Mock", "Questions": 10, "Score": "85%", "Duration": "45m"},
            {"Date": "2025-10-23", "Type": "Technical Focus", "Questions": 8, "Score": "92%", "Duration": "35m"},
            {"Date": "2025-10-20", "Type": "Behavioral STAR", "Questions": 5, "Score": "78%", "Duration": "25m"}
        ]
        df_sessions = pd.DataFrame(sessions_data)
        st.dataframe(df_sessions, use_container_width=True)
    
    with subtab4:
        st.subheader("📊 Performance Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Performance metrics
            st.markdown("#### 📈 Overall Performance")
            
            metrics_col1, metrics_col2 = st.columns(2)
            with metrics_col1:
                st.metric("Success Rate", "87%", "+5%")
                st.metric("Practice Hours", "24h", "+6h")
            with metrics_col2:
                st.metric("Avg Score", "85%", "+8%")
                st.metric("Sessions", "12", "+3")
            
            # Performance trend chart
            st.markdown("#### 📊 Score Trend")
            trend_data = pd.DataFrame({
                'Session': list(range(1, 13)),
                'Score': [65, 68, 72, 75, 78, 82, 84, 86, 85, 88, 90, 87]
            })
            fig = px.line(trend_data, x='Session', y='Score', 
                         title='Practice Session Performance',
                         markers=True)
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Category breakdown
            st.markdown("#### 🎯 Performance by Category")
            
            category_data = pd.DataFrame({
                'Category': ['Technical', 'Behavioral', 'System Design', 'Coding', 'Case Study'],
                'Score': [92, 85, 78, 88, 82]
            })
            fig = px.bar(category_data, x='Category', y='Score',
                        title='Scores by Interview Type',
                        color='Score',
                        color_continuous_scale='RdYlGn')
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Improvement areas
            st.markdown("#### 🎓 Areas for Improvement")
            st.markdown("1. 🔸 **System Design**: Practice more distributed systems questions")
            st.markdown("2. 🔸 **Case Studies**: Improve business problem-solving framework")
            st.markdown("3. 🔸 **Behavioral**: Expand STAR example library")

# ===========================
# TAB 2: CAREER COACH
# ===========================
with tab2:
    st.header("📊 Career Coach")
    st.markdown("**AI-powered career planning, skill development, and trajectory optimization**")
    
    # Career Coach sections
    subtab1, subtab2, subtab3, subtab4 = st.tabs([
        "💬 Chat with Coach",
        "🗺️ Career Roadmap",
        "📈 Skill Development",
        "🎯 Goal Tracking"
    ])
    
    with subtab1:
        st.subheader("💬 Career Coach Chatbot")
        st.markdown("Get personalized career advice, planning guidance, and skill recommendations.")
        
        # Initialize career chatbot history
        if 'career' not in st.session_state.coaching_state['chat_history']:
            st.session_state.coaching_state['chat_history']['career'] = [
                {"role": "assistant", "content": "👋 Hi! I'm your AI Career Coach. I can help you plan your career path, develop new skills, and achieve your professional goals. What would you like to work on today?"}
            ]
        
        # Display chat messages
        for message in st.session_state.coaching_state['chat_history']['career']:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about career planning, skill gaps, next steps..."):
            # Add user message
            st.session_state.coaching_state['chat_history']['career'].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # AI response using portal_bridge ChatService
            if PORTAL_BRIDGE_AVAILABLE and chat_service:
                try:
                    # Get context for career coaching
                    context = {
                        "coach_type": "career",
                        "user_tier": user_tier,
                        "resume_data": st.session_state.get('resume_data', {}),
                        "current_role": st.session_state.get('current_role', 'Not specified'),
                        "career_goals": st.session_state.get('career_goals', [])
                    }
                    
                    # Call admin AI chatbot via portal_bridge
                    response = chat_service.ask(
                        question=prompt,
                        context=context,
                        conversation_history=st.session_state.coaching_state['chat_history']['career']
                    )
                    
                    # Display AI response
                    with st.chat_message("assistant"):
                        st.markdown(response)
                    
                    # Add to chat history
                    st.session_state.coaching_state['chat_history']['career'].append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    # Fallback response
                    st.error(f"⚠️ Career Coach temporarily unavailable: {str(e)}")
                    fallback_response = "I'm having trouble connecting. Please try again in a moment."
                    with st.chat_message("assistant"):
                        st.markdown(fallback_response)
                    st.session_state.coaching_state['chat_history']['career'].append({"role": "assistant", "content": fallback_response})
            else:
                # Demo response (offline mode)
                career_tips = [
                    "Based on your current role as ML Engineer, here are 3 career paths to consider: 1) Technical Leadership (Senior → Lead → Principal), 2) People Management (Manager → Director), 3) Deep Specialization (Research Scientist)...",
                    "Great question! To transition into that role, you'll need to develop these key skills: 1) Cloud architecture (AWS/Azure), 2) Team leadership, 3) System design at scale...",
                    "Your skill gap analysis shows: Strong in Python & ML, but could improve in: DevOps/MLOps (6-month timeline), Leadership skills (ongoing), Business communication (3 months)...",
                    "Excellent! Let me create a personalized 12-month career development plan with quarterly milestones..."
                ]
                response = career_tips[len(st.session_state.coaching_state['chat_history']['career']) % len(career_tips)]
            
                st.session_state.coaching_state['chat_history']['career'].append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)
        
        # Quick actions
        st.markdown("---")
        st.markdown("**🚀 Quick Actions**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🗺️ Create Career Plan", use_container_width=True):
                st.session_state.coaching_state['chat_history']['career'].append({
                    "role": "assistant",
                    "content": "Let's build your career plan! First, tell me your 3-year goal. What role do you want to be in?"
                })
                st.rerun()
        with col2:
            if st.button("📊 Analyze Skill Gaps", use_container_width=True):
                st.session_state.coaching_state['chat_history']['career'].append({
                    "role": "assistant",
                    "content": "**Skill Gap Analysis:**\n\n✅ **Strengths**: Python, ML, Data Analysis\n🔸 **Develop**: Cloud (AWS/Azure), Leadership, System Design\n⚠️ **Critical**: DevOps, Team Management\n\nShall I create a learning plan?"
                })
                st.rerun()
        with col3:
            if st.button("🎯 Set New Goal", use_container_width=True):
                st.session_state.coaching_state['chat_history']['career'].append({
                    "role": "assistant",
                    "content": "Great! Let's set a SMART goal (Specific, Measurable, Achievable, Relevant, Time-bound). What's your objective?"
                })
                st.rerun()
    
    with subtab2:
        st.subheader("🗺️ Career Roadmap & Trajectory")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 🎯 Current Position")
            st.info("**Senior ML Engineer**\n\nTenure: 3 years | Level: IC4 | Salary: £85k")
            
            st.markdown("#### 📊 Career Trajectory Analysis")
            trajectory_score = 8.7
            st.metric("Trajectory Score", f"{trajectory_score}/10", "+0.5")
            
            # Progress bars
            st.markdown("**Growth Dimensions:**")
            st.progress(0.92, text="Technical Excellence: 92%")
            st.progress(0.76, text="Leadership Impact: 76%")
            st.progress(0.85, text="Industry Visibility: 85%")
            st.progress(0.68, text="Strategic Thinking: 68%")
        
        with col2:
            st.markdown("#### 🚀 Recommended Career Paths")
            
            paths = [
                {
                    "path": "Technical Leadership",
                    "probability": "75%",
                    "timeline": "12-18 months",
                    "next_role": "Lead ML Engineer",
                    "requirements": ["Lead 2+ projects", "Mentor 3+ engineers", "Drive architecture decisions"]
                },
                {
                    "path": "People Management",
                    "probability": "60%",
                    "timeline": "18-24 months",
                    "next_role": "Engineering Manager",
                    "requirements": ["Leadership training", "Team lead experience", "Stakeholder management"]
                },
                {
                    "path": "Deep Specialist",
                    "probability": "55%",
                    "timeline": "24-36 months",
                    "next_role": "Principal ML Scientist",
                    "requirements": ["Research publications", "PhD or equivalent", "Domain expertise"]
                }
            ]
            
            for i, path in enumerate(paths, 1):
                with st.expander(f"Path {i}: {path['path']} ({path['probability']} match)"):
                    st.markdown(f"**Next Role**: {path['next_role']}")
                    st.markdown(f"**Timeline**: {path['timeline']}")
                    st.markdown("**Requirements:**")
                    for req in path['requirements']:
                        st.markdown(f"- {req}")
        
        # Roadmap visualization
        st.markdown("---")
        st.markdown("#### 🗺️ 5-Year Career Roadmap")
        
        roadmap_data = pd.DataFrame({
            'Year': ['2025', '2026', '2027', '2028', '2029', '2030'],
            'Role': ['Senior ML Engineer', 'Lead ML Engineer', 'Staff ML Engineer', 'Principal Engineer', 'Distinguished Engineer', 'VP Engineering'],
            'Salary': [85000, 110000, 140000, 175000, 220000, 280000]
        })
        
        fig = px.line(roadmap_data, x='Year', y='Salary', text='Role',
                     title='Projected Career & Salary Growth',
                     markers=True)
        fig.update_traces(textposition='top center')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with subtab3:
        st.subheader("📈 Skill Development Plan")
        
        st.markdown("#### 🎯 Active Learning Paths")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Current skills
            skills_data = pd.DataFrame({
                'Skill': ['Python', 'Machine Learning', 'AWS', 'Leadership', 'System Design', 'DevOps'],
                'Current': [95, 90, 65, 55, 70, 45],
                'Target': [95, 95, 85, 80, 90, 75],
                'Gap': [0, 5, 20, 25, 20, 30]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Current Level', x=skills_data['Skill'], y=skills_data['Current'], marker_color='lightblue'))
            fig.add_trace(go.Bar(name='Target Level', x=skills_data['Skill'], y=skills_data['Target'], marker_color='darkblue'))
            fig.update_layout(title='Skills: Current vs Target', barmode='group', height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Priority Skills**")
            st.markdown("1. 🔴 DevOps/MLOps (Gap: 30%)")
            st.markdown("   Timeline: 6 months")
            st.markdown("2. 🟡 Leadership (Gap: 25%)")
            st.markdown("   Timeline: 12 months")
            st.markdown("3. 🟡 System Design (Gap: 20%)")
            st.markdown("   Timeline: 4 months")
            st.markdown("4. 🟢 AWS Cloud (Gap: 20%)")
            st.markdown("   Timeline: 3 months")
        
        st.markdown("---")
        st.markdown("#### 📚 Recommended Learning Resources")
        
        learning_tab1, learning_tab2, learning_tab3 = st.tabs(["Courses", "Certifications", "Books"])
        
        with learning_tab1:
            st.markdown("**🎓 Top Courses for Your Goals**")
            st.markdown("1. AWS Certified Solutions Architect (Udemy, 40h)")
            st.markdown("2. System Design Interview Masterclass (Educative, 25h)")
            st.markdown("3. Engineering Leadership Fundamentals (LinkedIn Learning, 15h)")
        
        with learning_tab2:
            st.markdown("**📜 Recommended Certifications**")
            st.markdown("1. ✅ AWS Solutions Architect Associate (Priority)")
            st.markdown("2. ⭐ Kubernetes Administrator (CKA)")
            st.markdown("3. 🎯 MLOps Specialization (Coursera)")
        
        with learning_tab3:
            st.markdown("**📖 Must-Read Books**")
            st.markdown("1. 'Designing Data-Intensive Applications' - Martin Kleppmann")
            st.markdown("2. 'The Staff Engineer's Path' - Tanya Reilly")
            st.markdown("3. 'An Elegant Puzzle' - Will Larson")
    
    with subtab4:
        st.subheader("🎯 Goal Tracking & Progress")
        
        # Active goals
        st.markdown("#### 📋 Active Career Goals")
        
        goals_data = [
            {
                "Goal": "Achieve AWS Solutions Architect certification",
                "Category": "Technical",
                "Deadline": "2025-12-31",
                "Progress": 65,
                "Status": "🟡 In Progress"
            },
            {
                "Goal": "Lead cross-functional ML project",
                "Category": "Leadership",
                "Deadline": "2026-03-31",
                "Progress": 40,
                "Status": "🟢 On Track"
            },
            {
                "Goal": "Mentor 3 junior engineers",
                "Category": "Leadership",
                "Deadline": "2025-11-30",
                "Progress": 85,
                "Status": "🟢 On Track"
            }
        ]
        
        for goal in goals_data:
            with st.expander(f"{goal['Status']} {goal['Goal']}", expanded=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.progress(goal['Progress']/100, text=f"Progress: {goal['Progress']}%")
                with col2:
                    st.markdown(f"**Category**: {goal['Category']}")
                with col3:
                    st.markdown(f"**Due**: {goal['Deadline']}")
        
        # Add new goal
        st.markdown("---")
        with st.expander("➕ Add New Goal"):
            goal_name = st.text_input("Goal Description")
            goal_category = st.selectbox("Category", ["Technical", "Leadership", "Networking", "Personal Brand"])
            goal_deadline = st.date_input("Target Deadline")
            
            if st.button("💾 Save Goal", type="primary"):
                st.success("✅ Goal added to tracking!")

# ===========================
# TAB 3: MENTORSHIP COACH
# ===========================
with tab3:
    st.header("🤝 Mentorship Coach")
    st.markdown("**AI-powered mentor matching, session management, and growth tracking**")
    
    # Mentorship Coach sections
    subtab1, subtab2, subtab3, subtab4 = st.tabs([
        "💬 Chat with Coach",
        "🔍 Find Mentors",
        "📅 Manage Sessions",
        "📊 Growth Analytics"
    ])
    
    with subtab1:
        st.subheader("💬 Mentorship Coach Chatbot")
        st.markdown("Get advice on finding mentors, preparing for sessions, and maximizing mentorship value.")
        
        # Initialize mentorship chatbot history
        if 'mentorship' not in st.session_state.coaching_state['chat_history']:
            st.session_state.coaching_state['chat_history']['mentorship'] = [
                {"role": "assistant", "content": "👋 Hi! I'm your AI Mentorship Coach. I can help you find the right mentor, prepare for sessions, and track your growth. What area of mentorship can I help you with?"}
            ]
        
        # Display chat messages
        for message in st.session_state.coaching_state['chat_history']['mentorship']:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about finding mentors, session prep, growth tracking..."):
            # Add user message
            st.session_state.coaching_state['chat_history']['mentorship'].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # AI response using portal_bridge ChatService
            if PORTAL_BRIDGE_AVAILABLE and chat_service:
                try:
                    # Get context for mentorship coaching
                    context = {
                        "coach_type": "mentorship",
                        "user_tier": user_tier,
                        "resume_data": st.session_state.get('resume_data', {}),
                        "mentorship_goals": st.session_state.get('mentorship_goals', []),
                        "active_mentors": st.session_state.coaching_state.get('mentorship_connections', [])
                    }
                    
                    # Call admin AI chatbot via portal_bridge
                    response = chat_service.ask(
                        question=prompt,
                        context=context,
                        conversation_history=st.session_state.coaching_state['chat_history']['mentorship']
                    )
                    
                    # Display AI response
                    with st.chat_message("assistant"):
                        st.markdown(response)
                    
                    # Add to chat history
                    st.session_state.coaching_state['chat_history']['mentorship'].append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    # Fallback response
                    st.error(f"⚠️ Mentorship Coach temporarily unavailable: {str(e)}")
                    fallback_response = "I'm having trouble connecting. Please try again in a moment."
                    with st.chat_message("assistant"):
                        st.markdown(fallback_response)
                    st.session_state.coaching_state['chat_history']['mentorship'].append({"role": "assistant", "content": fallback_response})
            else:
                # Demo response (offline mode)
                mentor_tips = [
                    "Great question! When looking for a mentor, focus on: 1) Relevant experience in your target area, 2) Communication style fit, 3) Availability and commitment. Let me show you some matches...",
                    "Excellent! To prepare for your mentorship session: 1) Set clear goals, 2) Prepare specific questions, 3) Share context in advance, 4) Take notes. Would you like a session prep template?",
                    "Based on your mentorship history, you're making great progress in: Leadership skills (+15%), Network expansion (12 new connections), Career clarity (scored 8.5/10)...",
                    "Perfect timing! Let me help you find mentors in your field. I'll analyze mentorship offers across these sectors: ML Engineering, Technical Leadership, Career Transition..."
                ]
                response = mentor_tips[len(st.session_state.coaching_state['chat_history']['mentorship']) % len(mentor_tips)]
            
                st.session_state.coaching_state['chat_history']['mentorship'].append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)
        
        # Quick actions
        st.markdown("---")
        st.markdown("**🚀 Quick Actions**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔍 Browse Mentorship Offers", use_container_width=True):
                st.info("💡 Navigate to page 42 (Mentorship Marketplace) to browse sector-specific mentorship offers")
                if st.button("📂 Go to Marketplace"):
                    st.switch_page("pages/15_Mentorship_Marketplace.py")
        with col2:
            if st.button("📅 Schedule Session", use_container_width=True):
                st.session_state.coaching_state['chat_history']['mentorship'].append({
                    "role": "assistant",
                    "content": "Let's schedule a mentorship session! Who would you like to meet with? (Check the 'Manage Sessions' tab for your active mentors)"
                })
                st.rerun()
        with col3:
            if st.button("📊 View My Progress", use_container_width=True):
                st.session_state.coaching_state['chat_history']['mentorship'].append({
                    "role": "assistant",
                    "content": "**Your Mentorship Progress:**\n\n✅ Sessions completed: 8\n⭐ Avg session rating: 4.7/5\n📈 Goals achieved: 5/7\n🎯 Next milestone: 10 sessions"
                })
                st.rerun()
    
    with subtab2:
        st.subheader("🔍 Find Mentors & Browse Offers")
        
        st.info("🌟 **Premium Feature**: Access to Mentorship Marketplace requires Annual Pro (£299/year) subscription")
        
        if user_tier in ['annual_pro', 'enterprise_pro']:
            st.success("✅ You have access to the full Mentorship Marketplace!")
            
            # Quick search
            col1, col2 = st.columns([2, 1])
            with col1:
                search_sector = st.multiselect(
                    "Search by Sector",
                    ["Machine Learning", "Data Science", "Engineering Leadership", 
                     "Product Management", "Career Transition", "Entrepreneurship"]
                )
            with col2:
                experience_level = st.selectbox("Mentor Experience", 
                    ["All Levels", "5-10 years", "10-15 years", "15+ years"])
            
            if st.button("🔍 Search Mentorship Offers", type="primary"):
                st.info("🔗 Redirecting to Mentorship Marketplace for detailed search...")
                with st.spinner("Loading marketplace..."):
                    if st.button("📂 Open Mentorship Marketplace"):
                        st.switch_page("pages/15_Mentorship_Marketplace.py")
            
            # Quick preview
            st.markdown("---")
            st.markdown("#### ⭐ Featured Mentorship Offers")
            
            offers_preview = [
                {
                    "Sector": "Machine Learning Engineering",
                    "Focus": "MLOps & Production Systems",
                    "Sessions": "6 sessions over 3 months",
                    "Price": "£299"
                },
                {
                    "Sector": "Engineering Leadership",
                    "Focus": "IC to Manager Transition",
                    "Sessions": "8 sessions over 4 months",
                    "Price": "£399"
                },
                {
                    "Sector": "Career Transition",
                    "Focus": "Industry Switch Strategy",
                    "Sessions": "4 sessions over 2 months",
                    "Price": "£199"
                }
            ]
            
            for offer in offers_preview:
                with st.expander(f"🎯 {offer['Sector']} - {offer['Focus']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Focus**: {offer['Focus']}")
                        st.markdown(f"**Duration**: {offer['Sessions']}")
                    with col2:
                        st.markdown(f"**Investment**: {offer['Price']}")
                        if st.button("View Details", key=offer['Sector']):
                            st.switch_page("pages/15_Mentorship_Marketplace.py")
        else:
            st.warning("⬆️ Upgrade to Annual Pro (£299/year) to access the Mentorship Marketplace")
            if st.button("💎 View Pricing Plans", type="primary"):
                st.switch_page("pages/06_Pricing.py")
    
    with subtab3:
        st.subheader("📅 Mentorship Sessions Management")
        
        # Active mentorships
        st.markdown("#### 🤝 Active Mentorship Connections")
        
        mentorships = [
            {
                "Mentor": "Sarah Johnson",
                "Sector": "ML Engineering",
                "Sessions": "3/6 completed",
                "Next Session": "2025-11-05",
                "Status": "🟢 Active"
            },
            {
                "Mentor": "Michael Chen",
                "Sector": "Engineering Leadership",
                "Sessions": "5/8 completed",
                "Next Session": "2025-11-12",
                "Status": "🟢 Active"
            }
        ]
        
        for mentor in mentorships:
            with st.expander(f"{mentor['Status']} {mentor['Mentor']} - {mentor['Sector']}", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Progress**: {mentor['Sessions']}")
                with col2:
                    st.markdown(f"**Next Session**: {mentor['Next Session']}")
                with col3:
                    if st.button("📅 Schedule", key=f"schedule_{mentor['Mentor']}"):
                        st.success("Session scheduling interface would open here")
        
        # Session history
        st.markdown("---")
        st.markdown("#### 📚 Session History")
        
        history_data = [
            {"Date": "2025-10-22", "Mentor": "Sarah Johnson", "Topic": "MLOps Pipeline Design", "Rating": "⭐⭐⭐⭐⭐"},
            {"Date": "2025-10-15", "Mentor": "Michael Chen", "Topic": "Leadership Transition", "Rating": "⭐⭐⭐⭐"},
            {"Date": "2025-10-08", "Mentor": "Sarah Johnson", "Topic": "Model Deployment Strategy", "Rating": "⭐⭐⭐⭐⭐"}
        ]
        
        df_history = pd.DataFrame(history_data)
        st.dataframe(df_history, use_container_width=True)
    
    with subtab4:
        st.subheader("📊 Mentorship Growth Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 Mentorship Impact")
            
            impact_metrics = st.columns(2)
            with impact_metrics[0]:
                st.metric("Total Sessions", "24", "+6")
                st.metric("Goals Achieved", "12", "+3")
            with impact_metrics[1]:
                st.metric("Network Growth", "+45", "+12")
                st.metric("Satisfaction", "4.8/5", "+0.3")
            
            # Growth over time
            growth_data = pd.DataFrame({
                'Month': ['Jul', 'Aug', 'Sep', 'Oct'],
                'Sessions': [4, 6, 7, 7],
                'Skills Improved': [2, 3, 4, 5]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Sessions', x=growth_data['Month'], y=growth_data['Sessions']))
            fig.add_trace(go.Bar(name='Skills Improved', x=growth_data['Month'], y=growth_data['Skills Improved']))
            fig.update_layout(title='Mentorship Activity', barmode='group', height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🎯 Skills Developed")
            
            skills_improved = pd.DataFrame({
                'Skill': ['Leadership', 'System Design', 'Communication', 'Strategy', 'Networking'],
                'Before': [55, 70, 65, 60, 50],
                'After': [80, 85, 82, 78, 75]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(name='Before', x=skills_improved['Skill'], y=skills_improved['Before'], 
                                    mode='lines+markers', line=dict(color='lightblue')))
            fig.add_trace(go.Scatter(name='After', x=skills_improved['Skill'], y=skills_improved['After'],
                                    mode='lines+markers', line=dict(color='darkblue')))
            fig.update_layout(title='Skills Growth Through Mentorship', height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### 💡 Key Achievements")
            st.markdown("✅ Promoted to Senior ML Engineer")
            st.markdown("✅ Led first cross-functional project")
            st.markdown("✅ Built network of 45+ industry contacts")
            st.markdown("✅ Improved leadership score by 25 points")

# Footer
st.markdown("---")
st.markdown("### 🎓 Continue Your Journey")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("**📚 More Coaching Resources**")
    if st.button("📖 Coaching Library", use_container_width=True):
        st.info("Access to coaching articles, videos, and resources")

with footer_col2:
    st.markdown("**🌟 Premium Features**")
    if st.button("🏪 Mentorship Marketplace", use_container_width=True):
        st.switch_page("pages/15_Mentorship_Marketplace.py")

with footer_col3:
    st.markdown("**⚙️ Settings**")
    if st.button("🔧 Coaching Preferences", use_container_width=True):
        st.info("Customize your coaching experience")

# Debug mode
if st.checkbox("🔧 Debug: Show Coaching State", value=False):
    st.json(st.session_state.coaching_state)

