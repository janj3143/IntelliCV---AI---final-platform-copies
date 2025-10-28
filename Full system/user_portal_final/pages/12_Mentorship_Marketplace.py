"""
🏪 Mentorship Marketplace - Directory of Sector-Specific Mentorship Offers
===========================================================================
Browse mentorship programs organized by industry sectors and specializations.

**Important Notes:**
- This is a directory of MENTORSHIP OFFERS (by sector), NOT individual people
- Search by sector/specialization to find structured mentorship programs
- Requires Annual Pro subscription (£299/year) for full access
- Programs include: session packages, learning paths, and expert guidance

Token Cost: 30 tokens (Annual Pro or Enterprise required)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="🏪 Mentorship Marketplace - IntelliCV",
    page_icon="🏪",
    layout="wide"
)

# Authentication check
if not st.session_state.get('authenticated_user'):
    st.error("🔒 Please log in to access Mentorship Marketplace")
    if st.button("🏠 Return to Home"):
        st.switch_page("main.py")
    st.stop()

# Tier check - requires Annual Pro or Enterprise
user_tier = st.session_state.get('subscription_tier', 'free')
if user_tier not in ['annual_pro', 'enterprise_pro']:
    st.warning("⭐ **Mentorship Marketplace requires Annual Pro subscription (£299/year)**")
    
    st.markdown("""
    ### 🏪 What You'll Get Access To:
    
    - 📁 **Sector-Specific Mentorship Programs**: Organized by industry and specialization
    - 🎯 **Structured Learning Paths**: Multi-session programs with clear outcomes
    - 🏅 **Expert Guidance**: Industry veterans sharing proven strategies
    - 📊 **Progress Tracking**: Measure your growth through mentorship
    - 🌟 **Premium Support**: Priority matching and scheduling
    
    This is a directory of **mentorship offers** (organized by sector), not individual people.
    """)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⬆️ Upgrade to Annual Pro (£299/year)", type="primary", use_container_width=True):
            st.switch_page("pages/06_Pricing.py")
    st.stop()

def main():
    st.title("🏪 Mentorship Marketplace")
    st.markdown("### Directory of Sector-Specific Mentorship Programs & Offers")
    st.info("💡 **Browse mentorship offers organized by sector** - structured programs, not individual profiles")
    
    # Token cost display
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.success("💎 **Token Cost: 30 tokens** | Annual Pro Feature ✅")
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏪 Browse by Sector", 
        "🎯 Mentorship Programs", 
        "📊 My Mentorships",
        "🌟 Success Stories"
    ])
    
    with tab1:
        st.header("🏪 Browse Mentorship Offers by Sector")
        st.markdown("**Find structured mentorship programs in your industry or target specialization**")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("🔍 Search by Sector")
            
            sector_category = st.selectbox("Industry Sector",
                                         ["Technology & Engineering",
                                          "Data Science & AI/ML",
                                          "Product & Design",
                                          "Business & Strategy",
                                          "Leadership & Management",
                                          "Entrepreneurship & Startups",
                                          "Finance & Investment",
                                          "Marketing & Sales"])
            
            specialization = st.multiselect("Specializations",
                                          ["Machine Learning Engineering",
                                           "Data Science",
                                           "Software Architecture",
                                           "Engineering Leadership",
                                           "Product Management",
                                           "Career Transition",
                                           "Executive Coaching",
                                           "Startup Founding"],
                                          default=["Machine Learning Engineering"])
            
            program_type = st.selectbox("Program Type",
                                      ["All Types",
                                       "Short-term (4-6 sessions)",
                                       "Standard (8-12 sessions)",
                                       "Long-term (6+ months)",
                                       "Project-based",
                                       "Career Transition"])
            
            price_range = st.select_slider("Price Range (Total Program)",
                                         options=["Under £200", "£200-£500", "£500-£1000", "£1000-£2000", "£2000+"],
                                         value="£500-£1000")
            
            if st.button("🔍 Search Mentorship Offers", type="primary"):
                st.success("✅ Found 23 mentorship programs matching your criteria!")
        
        with col2:
            st.subheader("⭐ Featured Mentorship Programs")
            st.markdown("*Structured programs organized by sector and outcomes*")
            
            # Featured mentorship OFFERS (not people)
            mentorship_offers = [
                {
                    "sector": "Machine Learning Engineering",
                    "program_name": "ML Engineer to MLOps Specialist",
                    "focus": "Production ML Systems & DevOps",
                    "sessions": "8 sessions over 4 months",
                    "format": "1-on-1 video + async support",
                    "outcomes": ["Deploy production ML pipelines", "Master CI/CD for ML", "Monitoring & observability"],
                    "price": "£599",
                    "rating": 4.9,
                    "participants": 127
                },
                {
                    "sector": "Engineering Leadership",
                    "program_name": "IC to Engineering Manager Transition",
                    "focus": "First-time manager skills & team leadership",
                    "sessions": "12 sessions over 6 months",
                    "format": "Bi-weekly 1-on-1 + peer group",
                    "outcomes": ["Team building strategies", "Performance management", "Stakeholder communication"],
                    "price": "£799",
                    "rating": 4.8,
                    "participants": 94
                },
                {
                    "sector": "Career Transition",
                    "program_name": "Industry Switcher Accelerator",
                    "focus": "Pivot to tech from non-tech background",
                    "sessions": "6 sessions over 3 months",
                    "format": "1-on-1 + resources library",
                    "outcomes": ["Transferable skills mapping", "Network building", "Application strategy"],
                    "price": "£399",
                    "rating": 4.7,
                    "participants": 156
                },
                {
                    "sector": "Data Science",
                    "program_name": "From Analyst to Data Scientist",
                    "focus": "ML fundamentals & project portfolio",
                    "sessions": "10 sessions over 5 months",
                    "format": "Weekly 1-on-1 + project reviews",
                    "outcomes": ["ML portfolio projects", "Interview prep", "Technical deep-dives"],
                    "price": "£699",
                    "rating": 4.9,
                    "participants": 203
                }
            ]
            
            for offer in mentorship_offers:
                with st.expander(f"🎯 **{offer['program_name']}** ({offer['sector']})", expanded=True):
                    col_a, col_b = st.columns([2, 1])
                    
                    with col_a:
                        st.markdown(f"**Focus**: {offer['focus']}")
                        st.markdown(f"**Format**: {offer['sessions']} • {offer['format']}")
                        
                        st.markdown("**Program Outcomes:**")
                        for outcome in offer['outcomes']:
                            st.markdown(f"  ✅ {outcome}")
                    
                    with col_b:
                        st.metric("Investment", offer['price'])
                        st.metric("Rating", f"{offer['rating']}/5.0")
                        st.markdown(f"*{offer['participants']} participants*")
                        
                        if st.button("📋 View Full Details", key=f"details_{offer['program_name']}", use_container_width=True):
                            st.info(f"Full program details for '{offer['program_name']}' would be shown here")
                        
                        if st.button("🎯 Express Interest", key=f"interest_{offer['program_name']}", use_container_width=True, type="primary"):
                            st.success("✅ Interest registered! Our team will contact you within 24h")
    
    with tab2:
        st.header("🎯 Mentorship Programs by Format & Duration")
    
    with tab2:
        st.header("🎯 Mentorship Programs by Format & Duration")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("📋 Filter by Format")
            
            program_format = st.radio("Program Structure",
                                    ["Short-term Intensive (4-6 sessions)",
                                     "Standard Program (8-12 sessions)",
                                     "Long-term Mentorship (6+ months)",
                                     "Project-based Coaching",
                                     "Career Transition Programs"])
            
            delivery_mode = st.multiselect("Delivery Mode",
                                         ["1-on-1 Video Sessions",
                                          "Group Cohorts",
                                          "Hybrid (Individual + Group)",
                                          "Async + Sync Mix",
                                          "Workshop Series"],
                                         default=["1-on-1 Video Sessions"])
            
            time_commitment = st.select_slider("Weekly Time Commitment",
                                             options=["1-2 hours", "2-4 hours", "4-6 hours", "6-8 hours", "8+ hours"],
                                             value="2-4 hours")
            
            st.subheader("🎯 Program Outcomes")
            st.markdown("""
            Select your primary goal:
            - 🚀 **Promotion/Advancement**
            - 💡 **Skill Development**
            - 🔄 **Career Transition**
            - 👥 **Leadership Growth**
            - 🏢 **Entrepreneurship**
            """)
        
        with col2:
            st.subheader("📦 Program Offerings")
            
            if "Short-term" in program_format:
                st.markdown("### ⚡ Short-term Intensive Programs (4-6 sessions)")
                programs = [
                    {
                        "name": "Interview Mastery Sprint",
                        "sector": "Universal - All Industries",
                        "duration": "4 sessions over 2 weeks",
                        "format": "1-on-1 intensive prep",
                        "outcomes": ["Interview confidence +80%", "Offer rate 65%", "Salary negotiation skills"],
                        "price": "£299"
                    },
                    {
                        "name": "Resume & LinkedIn Optimization",
                        "sector": "Universal - All Industries",
                        "duration": "5 sessions over 3 weeks",
                        "format": "1-on-1 + templates",
                        "outcomes": ["Profile views +200%", "Recruiter contacts +150%", "ATS compatibility 95%"],
                        "price": "£349"
                    }
                ]
            
            elif "Standard" in program_format:
                st.markdown("### 📚 Standard Programs (8-12 sessions)")
                programs = [
                    {
                        "name": "ML Engineer to MLOps Specialist",
                        "sector": "Machine Learning & AI",
                        "duration": "10 sessions over 5 months",
                        "format": "Bi-weekly 1-on-1 + resources",
                        "outcomes": ["Production ML deployment", "CI/CD for ML", "Monitoring expertise"],
                        "price": "£699"
                    },
                    {
                        "name": "IC to Engineering Manager",
                        "sector": "Engineering Leadership",
                        "duration": "12 sessions over 6 months",
                        "format": "Bi-weekly + peer group",
                        "outcomes": ["Team management skills", "Performance reviews", "Stakeholder communication"],
                        "price": "£799"
                    }
                ]
            
            elif "Long-term" in program_format:
                st.markdown("### 🎯 Long-term Mentorship (6+ months)")
                programs = [
                    {
                        "name": "Executive Leadership Track",
                        "sector": "C-Suite & Senior Leadership",
                        "duration": "20 sessions over 12 months",
                        "format": "Monthly 1-on-1 + quarterly strategy",
                        "outcomes": ["Executive presence", "Board readiness", "Strategic thinking"],
                        "price": "£2,499"
                    },
                    {
                        "name": "Startup Founder Program",
                        "sector": "Entrepreneurship",
                        "duration": "24 sessions over 12 months",
                        "format": "Bi-weekly + investor intros",
                        "outcomes": ["Product-market fit", "Fundraising strategy", "Team building"],
                        "price": "£3,299"
                    }
                ]
            
            elif "Project-based" in program_format:
                st.markdown("### 🛠️ Project-based Coaching")
                programs = [
                    {
                        "name": "ML Project Portfolio Builder",
                        "sector": "Data Science & ML",
                        "duration": "8 sessions + project reviews",
                        "format": "Weekly check-ins + code reviews",
                        "outcomes": ["3 portfolio projects", "GitHub showcase", "Technical interviews ready"],
                        "price": "£599"
                    },
                    {
                        "name": "Product Launch Mentorship",
                        "sector": "Product Management",
                        "duration": "10 sessions + launch support",
                        "format": "Weekly 1-on-1 + launch plan",
                        "outcomes": ["Market validation", "Go-to-market strategy", "Successful launch"],
                        "price": "£899"
                    }
                ]
            
            else:  # Career Transition
                st.markdown("### 🔄 Career Transition Programs")
                programs = [
                    {
                        "name": "Industry Switcher Accelerator",
                        "sector": "Career Transition",
                        "duration": "8 sessions over 4 months",
                        "format": "1-on-1 + networking support",
                        "outcomes": ["Transferable skills map", "Target industry network", "Job offers"],
                        "price": "£499"
                    },
                    {
                        "name": "Analyst to Data Scientist",
                        "sector": "Data Science",
                        "duration": "12 sessions over 6 months",
                        "format": "Weekly 1-on-1 + learning path",
                        "outcomes": ["ML skills certification", "Portfolio projects", "DS role transition"],
                        "price": "£799"
                    }
                ]
            
            # Display programs
            for program in programs:
                with st.expander(f"📘 **{program['name']}**", expanded=True):
                    col_p1, col_p2 = st.columns([2, 1])
                    
                    with col_p1:
                        st.markdown(f"**Sector**: {program['sector']}")
                        st.markdown(f"**Duration**: {program['duration']}")
                        st.markdown(f"**Format**: {program['format']}")
                        
                        st.markdown("**Expected Outcomes:**")
                        for outcome in program['outcomes']:
                            st.markdown(f"  ✅ {outcome}")
                    
                    with col_p2:
                        st.metric("Investment", program['price'])
                        st.markdown("---")
                        if st.button("� Full Details", key=f"details2_{program['name']}", use_container_width=True):
                            st.info("Full program details")
                        if st.button("🎯 Apply Now", key=f"apply_{program['name']}", use_container_width=True, type="primary"):
                            st.success("✅ Application submitted!")
    
    with tab3:
        st.header("� My Mentorships")
    
    with tab3:
        st.header("📊 My Mentorships")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Active Programs")
            
            # Active mentorship programs
            active_programs = [
                {
                    "program": "ML Engineer to MLOps Specialist",
                    "sector": "Machine Learning & AI",
                    "progress": 60,
                    "sessions_completed": 6,
                    "sessions_total": 10,
                    "next_session": "2025-11-05 14:00",
                    "mentor_assigned": "Yes"
                },
                {
                    "program": "IC to Engineering Manager",
                    "sector": "Engineering Leadership",
                    "progress": 25,
                    "sessions_completed": 3,
                    "sessions_total": 12,
                    "next_session": "2025-11-08 10:00",
                    "mentor_assigned": "Yes"
                }
            ]
            
            for prog in active_programs:
                with st.expander(f"📘 {prog['program']}", expanded=True):
                    st.markdown(f"**Sector**: {prog['sector']}")
                    st.markdown(f"**Progress**: {prog['sessions_completed']}/{prog['sessions_total']} sessions")
                    st.progress(prog['progress'] / 100)
                    st.markdown(f"**Next Session**: {prog['next_session']}")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("📅 Reschedule", key=f"resched_{prog['program'][:10]}"):
                            st.info("Rescheduling options")
                    with col_b:
                        if st.button("📝 Session Notes", key=f"notes_{prog['program'][:10]}"):
                            st.info("View session notes")
        
        with col2:
            st.subheader("📈 Your Mentorship Journey")
            
            # Journey metrics
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("Total Programs", "2", "Active")
            with col_m2:
                st.metric("Sessions Completed", "9")
            with col_m3:
                st.metric("Avg Rating Given", "4.9/5")
            
            st.subheader("🎯 Goals Progress")
            
            goals = [
                {"goal": "Master MLOps deployment", "progress": 65, "target_date": "2026-01-31"},
                {"goal": "Lead engineering team", "progress": 30, "target_date": "2026-03-31"},
                {"goal": "Get promoted to Senior", "progress": 50, "target_date": "2026-02-28"}
            ]
            
            for goal in goals:
                st.markdown(f"**{goal['goal']}** (Target: {goal['target_date']})")
                st.progress(goal['progress'] / 100)
                st.markdown(f"{goal['progress']}% complete")
                st.markdown("---")
            
            st.subheader("📚 Learning Resources")
            st.markdown("""
            - 📖 Recommended Reading: 12 articles
            - 🎥 Video Courses: 5 suggested
            - 🏆 Certifications: 3 recommended
            - 🔗 Network Connections: 8 intros available
            """)
    
    with tab4:
        st.header("🌟 Success Stories")

        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏆 Featured Success Stories")
            
            # Detailed success stories
            success_stories = [
                {
                    "mentee": "Alexandra Rodriguez",
                    "before": "Mid-level Data Analyst",
                    "after": "Director of Data Science",
                    "timeline": "18 months",
                    "mentor": "Dr. Jennifer Liu (Ex-Google VP)",
                    "outcome": "250% salary increase, leading team of 15",
                    "story": "Through strategic guidance and technical mentorship, Alexandra developed both leadership skills and advanced ML expertise, positioning her for executive-level roles.",
                    "testimonial": "Jennifer didn't just mentor me - she transformed my entire approach to career development. The ROI has been incredible."
                },
                {
                    "mentee": "Marcus Thompson",
                    "before": "Software Engineer",
                    "after": "Successful Startup Founder",
                    "timeline": "12 months",
                    "mentor": "Mark Thompson (Serial Entrepreneur)",
                    "outcome": "Founded AI startup, raised $3.2M seed round",
                    "story": "Mark's entrepreneurship mentorship provided the strategic framework and network connections needed to successfully launch and fund a tech startup.",
                    "testimonial": "Mark's guidance was invaluable in avoiding common startup pitfalls. His network opened doors I never could have accessed alone."
                }
            ]
            
            for story in success_stories:
                with st.expander(f"🎯 {story['mentee']}: {story['before']} → {story['after']}"):
                    st.write(f"**Timeline:** {story['timeline']}")
                    st.write(f"**Mentor:** {story['mentor']}")
                    st.write(f"**Outcome:** {story['outcome']}")
                    st.write(f"**Story:** {story['story']}")
                    st.success(f"💬 **Testimonial:** \"{story['testimonial']}\"")
        
        with col2:
            st.subheader("📊 Impact Metrics")
            
            # Impact visualization
            impact_data = {
                'Metric': ['Salary Increase', 'Promotion Rate', 'Career Satisfaction', 'Skill Development', 'Network Growth'],
                'Average Improvement': [45, 78, 85, 92, 67],
                'Top 10% Improvement': [120, 95, 98, 99, 89]
            }
            
            impact_df = pd.DataFrame(impact_data)
            
            fig = px.bar(impact_df, x='Metric', y=['Average Improvement', 'Top 10% Improvement'],
                        title="Career Impact Metrics (%)",
                        barmode='group')
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("💬 Recent Testimonials")
            
            testimonials = [
                "⭐⭐⭐⭐⭐ 'Life-changing mentorship experience. Worth every penny!' - Sarah K.",
                "⭐⭐⭐⭐⭐ 'My mentor helped me navigate a complex career transition flawlessly.' - David L.",
                "⭐⭐⭐⭐⭐ 'The AI matching was spot-on. Perfect mentor for my goals.' - Maria S.",
                "⭐⭐⭐⭐⭐ 'Enterprise program transformed our entire leadership pipeline.' - TechCorp HR",
                "⭐⭐⭐⭐⭐ 'ROI exceeded expectations. Team performance improved dramatically.' - StartupCEO"
            ]
            
            for testimonial in testimonials:
                st.write(testimonial)
            
            if st.button("📝 Share Your Success Story"):
                st.success("✅ Success story submission form opened!")

if __name__ == "__main__":
    main()