"""
🎁 User Rewards - Fractional Ownership Program
==============================================
Earn fractional ownership in IntelliCV-AI by contributing
feature suggestions, improvements, and platform enhancements.

AVAILABLE TO ALL TIERS
"""

import streamlit as st
from pathlib import Path
import sys
from datetime import datetime

# Add parent directory to path for imports
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

st.set_page_config(
    page_title="User Rewards - IntelliCV",
    page_icon="🎁",
    layout="wide"
)

# Check authentication
if not st.session_state.get("authenticated_user"):
    st.warning("🔐 Please login to access User Rewards")
    st.stop()

# Main content
st.title("🎁 User Rewards - Fractional Ownership Program")
st.markdown("### Contribute to IntelliCV-AI and Earn Ownership")

st.success("""
🌟 **Fractional Ownership Opportunity**
At IntelliCV-AI, we believe in rewarding our community members who help us improve the platform.
Submit feature suggestions, report bugs, and contribute improvements to earn fractional ownership stakes.
""")

# How it works
st.markdown("---")
st.markdown("### 📋 How It Works")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; border-radius: 10px; color: white; text-align: center;">
        <h3>1️⃣ Suggest</h3>
        <p>Submit feature ideas, improvements, or bug reports</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 1.5rem; border-radius: 10px; color: white; text-align: center;">
        <h3>2️⃣ Review</h3>
        <p>Our team evaluates and implements your suggestion</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                padding: 1.5rem; border-radius: 10px; color: white; text-align: center;">
        <h3>3️⃣ Earn</h3>
        <p>Receive ownership credits based on impact</p>
    </div>
    """, unsafe_allow_html=True)

# Reward tiers
st.markdown("---")
st.markdown("### 💎 Reward Tiers")

reward_tiers = {
    "🥉 Minor Improvement": {
        "credits": "0.001% ownership",
        "examples": "UI tweak, typo fix, small suggestion"
    },
    "🥈 Moderate Feature": {
        "credits": "0.01% ownership",
        "examples": "New feature idea, workflow improvement, integration suggestion"
    },
    "🥇 Major Enhancement": {
        "credits": "0.05% ownership",
        "examples": "Game-changing feature, major algorithm improvement, strategic partnership idea"
    },
    "💎 Revolutionary Contribution": {
        "credits": "0.1%+ ownership",
        "examples": "Platform transformation, new business model, major technical breakthrough"
    }
}

for tier, info in reward_tiers.items():
    with st.expander(f"{tier} - {info['credits']}"):
        st.markdown(f"**Examples:** {info['examples']}")
        st.markdown(f"**Ownership Credits:** {info['credits']}")

# Your current rewards
st.markdown("---")
st.markdown("### 🏆 Your Ownership Portfolio")

user_email = st.session_state.get("user_email", "unknown@example.com")

# Demo data
user_credits = 0.023  # 0.023% ownership
total_contributions = 5
pending_review = 2

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Ownership", f"{user_credits:.3f}%", "+0.005%")

with col2:
    st.metric("Total Contributions", total_contributions, "+1")

with col3:
    st.metric("Pending Review", pending_review)

with col4:
    estimated_value = user_credits * 1000000  # Assuming $1M valuation
    st.metric("Est. Value", f"${estimated_value:,.0f}")

# Contribution history
st.markdown("### 📊 Your Contribution History")

demo_history = [
    {
        "date": "2025-10-15",
        "type": "Feature Suggestion",
        "title": "Dual Career Suite concept",
        "status": "✅ Implemented",
        "credits": 0.01
    },
    {
        "date": "2025-10-20",
        "type": "UI Improvement",
        "title": "Add sidebar feature gating indicators",
        "status": "✅ Implemented",
        "credits": 0.005
    },
    {
        "date": "2025-10-22",
        "type": "Bug Report",
        "title": "Login form validation issue",
        "status": "✅ Fixed",
        "credits": 0.003
    },
    {
        "date": "2025-10-25",
        "type": "Feature Suggestion",
        "title": "Touch point analysis visualization",
        "status": "🔄 Under Review",
        "credits": 0.0
    },
    {
        "date": "2025-10-27",
        "type": "Integration Idea",
        "title": "LinkedIn API integration for job search",
        "status": "🔄 Pending",
        "credits": 0.0
    }
]

for contribution in demo_history:
    with st.container():
        col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
        with col1:
            st.markdown(f"**{contribution['date']}**")
        with col2:
            st.markdown(f"**{contribution['title']}**")
        with col3:
            st.markdown(contribution['status'])
        with col4:
            if contribution['credits'] > 0:
                st.markdown(f"**+{contribution['credits']:.3f}%**")
        
        st.markdown("---")

# Submit new suggestion
st.markdown("### 💡 Submit New Suggestion")

with st.form("suggestion_form"):
    suggestion_type = st.selectbox(
        "Type of Contribution",
        ["Feature Suggestion", "UI/UX Improvement", "Bug Report", "Integration Idea", "Business Model Suggestion", "Other"]
    )
    
    suggestion_title = st.text_input(
        "Title (Short Description)",
        placeholder="e.g., Add real-time job alerts via email"
    )
    
    suggestion_details = st.text_area(
        "Detailed Description",
        placeholder="Explain your idea in detail. Include:\n- What problem does it solve?\n- How would it work?\n- What value does it add?\n- Any technical considerations?",
        height=200
    )
    
    suggestion_impact = st.select_slider(
        "Estimated Impact",
        options=["Minor", "Moderate", "Significant", "Major", "Revolutionary"]
    )
    
    files = st.file_uploader(
        "Attachments (mockups, screenshots, etc.)",
        accept_multiple_files=True,
        type=["png", "jpg", "pdf", "doc", "docx"]
    )
    
    submit_button = st.form_submit_button("🚀 Submit Contribution", use_container_width=True, type="primary")
    
    if submit_button:
        if suggestion_title and suggestion_details:
            st.success("✅ Contribution submitted successfully!")
            st.info("""
            📧 **Next Steps:**
            1. Our team will review your submission within 5 business days
            2. You'll receive an email with the evaluation decision
            3. If implemented, ownership credits will be added to your account
            4. You'll be credited in our changelog and contributor list
            """)
            
            # Demo: Add to session state
            st.session_state["last_submission"] = {
                "title": suggestion_title,
                "type": suggestion_type,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "status": "🔄 Pending Review"
            }
        else:
            st.error("❌ Please fill in both title and detailed description")

# Terms and conditions
st.markdown("---")
st.markdown("### 📜 Program Terms")

with st.expander("View Complete Terms & Conditions"):
    st.markdown("""
    **IntelliCV-AI Fractional Ownership Rewards Program**
    
    1. **Ownership Credits:**
        - Ownership percentages are granted as non-dilutable credits
        - Credits may convert to actual equity upon future funding rounds
        - Minimum threshold for payout: 0.1% ownership
    
    2. **Valuation:**
        - Current company valuation: $1,000,000 USD
        - Valuation updated quarterly based on revenue and growth
        - Contributors notified of valuation changes
    
    3. **Implementation Requirements:**
        - Suggestions must be implemented to earn credits
        - Implementation within 12 months to qualify
        - Partial implementations may receive partial credits
    
    4. **Intellectual Property:**
        - By submitting, you grant IntelliCV-AI rights to implement your suggestion
        - You retain rights to discuss/share your idea publicly
        - Attribution provided in changelog and contributor page
    
    5. **Payout:**
        - Cash equivalent payouts available for ownership > 0.1%
        - Equity conversion available upon Series A funding
        - Annual dividend distributions based on profitability
    
    6. **Transferability:**
        - Ownership credits are non-transferable
        - May be inherited by legal heirs
        - Cannot be sold separately from account
    
    **Questions?** Contact rewards@intellicv.ai
    """)

# Leaderboard
st.markdown("---")
st.markdown("### 🏅 Top Contributors")

st.info("📊 Top 10 contributors by ownership percentage:")

demo_leaderboard = [
    {"rank": 1, "user": "Alex M.", "ownership": 0.245, "contributions": 23},
    {"rank": 2, "user": "Sarah K.", "ownership": 0.189, "contributions": 18},
    {"rank": 3, "user": "James L.", "ownership": 0.156, "contributions": 31},
    {"rank": 4, "user": "Maria G.", "ownership": 0.134, "contributions": 15},
    {"rank": 5, "user": f"{user_email.split('@')[0]} (You)", "ownership": user_credits, "contributions": total_contributions},
]

for contributor in demo_leaderboard:
    col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
    with col1:
        if contributor['rank'] == 1:
            st.markdown("🥇")
        elif contributor['rank'] == 2:
            st.markdown("🥈")
        elif contributor['rank'] == 3:
            st.markdown("🥉")
        else:
            st.markdown(f"**#{contributor['rank']}**")
    with col2:
        st.markdown(f"**{contributor['user']}**")
    with col3:
        st.markdown(f"{contributor['ownership']:.3f}%")
    with col4:
        st.markdown(f"{contributor['contributions']} contributions")
