"""
💑 Dual Career Suite - Partner Career Optimization
==================================================
Upload both partner profiles and optimize dual job search
with geographic feasibility and travel distance analysis.

PREMIUM FEATURE - Annual Pro Tier ($149.99/year)
Cost: 12 tokens per dual analysis
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path for imports
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

st.set_page_config(
    page_title="Dual Career Suite - IntelliCV",
    page_icon="💑",
    layout="wide"
)

# Check authentication
if not st.session_state.get("authenticated_user"):
    st.warning("🔐 Please login to access the Dual Career Suite")
    st.stop()

# Check subscription tier
tier = st.session_state.get("subscription_tier", "free")
if tier not in ["annual_pro", "enterprise_pro"]:
    st.warning("🔒 Dual Career Suite requires Annual Pro or Enterprise Pro subscription")
    st.info("**Upgrade to unlock:** Dual job search optimization, geographic feasibility, partner profile integration")
    if st.button("⬆️ Upgrade to Annual Pro"):
        st.switch_page("pages/06_Pricing.py")
    st.stop()

# Main content
st.title("💑 Dual Career Suite")
st.markdown("### Optimize Career Opportunities for You and Your Partner")

st.info("""
🎯 **Partner Optimization Features:**
- Upload both partner resumes and career profiles
- Search for job opportunities optimized for BOTH careers
- Geographic feasibility analysis (travel distances, relocation options)
- Comparative analysis: Which location offers best opportunities for both?
- Dual salary optimization
- Work-life balance metrics
""")

# Partner profile section
st.markdown("---")
st.markdown("### 👥 Partner Profiles")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 👤 Partner 1 (You)")
    
    partner1_name = st.text_input(
        "Name",
        value=st.session_state.get("user_id", ""),
        key="partner1_name"
    )
    
    partner1_resume = st.file_uploader(
        "Upload Resume (PDF, DOCX)",
        type=["pdf", "docx"],
        key="partner1_resume"
    )
    
    partner1_career = st.text_area(
        "Career Goals",
        placeholder="e.g., Looking for senior software engineer roles in tech...",
        key="partner1_career"
    )
    
    partner1_location_pref = st.text_input(
        "Preferred Locations (comma-separated)",
        placeholder="San Francisco, Austin, Seattle",
        key="partner1_loc"
    )
    
    partner1_salary_min = st.number_input(
        "Minimum Salary ($)",
        min_value=0,
        value=80000,
        step=5000,
        key="partner1_salary"
    )

with col2:
    st.markdown("#### 👤 Partner 2")
    
    st.warning("⚠️ **ONE-TIME SETUP**: Partner profile can only be set once. Contact support to modify.")
    
    partner2_name = st.text_input(
        "Partner Name",
        key="partner2_name"
    )
    
    partner2_resume = st.file_uploader(
        "Upload Partner Resume (PDF, DOCX)",
        type=["pdf", "docx"],
        key="partner2_resume"
    )
    
    partner2_career = st.text_area(
        "Partner Career Goals",
        placeholder="e.g., Looking for marketing director roles...",
        key="partner2_career"
    )
    
    partner2_location_pref = st.text_input(
        "Partner Preferred Locations (comma-separated)",
        placeholder="San Francisco, Austin, Seattle",
        key="partner2_loc"
    )
    
    partner2_salary_min = st.number_input(
        "Partner Minimum Salary ($)",
        min_value=0,
        value=70000,
        step=5000,
        key="partner2_salary"
    )

# Search constraints
st.markdown("---")
st.markdown("### 🎯 Dual Search Constraints")

col1, col2, col3 = st.columns(3)

with col1:
    max_commute_distance = st.slider(
        "Maximum One-Way Commute (miles)",
        min_value=5,
        max_value=100,
        value=30,
        step=5
    )

with col2:
    travel_tolerance = st.selectbox(
        "Travel Distance Tolerance",
        ["Low (both same city)", "Medium (within 50 miles)", "High (within 100 miles)", "Very High (different states OK)"]
    )

with col3:
    relocation_willing = st.checkbox("Willing to relocate?", value=True)

# Action button
st.markdown("---")
if st.button("🔍 Find Dual Career Opportunities", type="primary", use_container_width=True):
    with st.spinner("🔄 Analyzing dual career opportunities..."):
        import time
        time.sleep(2)
        
        st.success("✅ Dual career analysis complete!")
        
        # Demo results
        st.markdown("### 📊 Dual Career Analysis Results")
        
        st.markdown("#### 🎯 Top 5 Optimized Locations")
        
        # Demo data
        demo_results = [
            {"city": "Austin, TX", "score": 92, "p1_jobs": 127, "p2_jobs": 89, "avg_commute": 22, "combined_salary": "$180K"},
            {"city": "San Francisco, CA", "score": 88, "p1_jobs": 234, "p2_jobs": 145, "avg_commute": 35, "combined_salary": "$240K"},
            {"city": "Seattle, WA", "score": 85, "p1_jobs": 189, "p2_jobs": 112, "avg_commute": 28, "combined_salary": "$195K"},
            {"city": "Denver, CO", "score": 82, "p1_jobs": 98, "p2_jobs": 76, "avg_commute": 18, "combined_salary": "$160K"},
            {"city": "Raleigh, NC", "score": 78, "p1_jobs": 67, "p2_jobs": 54, "avg_commute": 15, "combined_salary": "$145K"}
        ]
        
        for idx, result in enumerate(demo_results, 1):
            with st.expander(f"#{idx} - {result['city']} (Score: {result['score']}/100)"):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Partner 1 Jobs", result['p1_jobs'])
                with col2:
                    st.metric("Partner 2 Jobs", result['p2_jobs'])
                with col3:
                    st.metric("Avg Commute", f"{result['avg_commute']} mi")
                with col4:
                    st.metric("Combined Salary", result['combined_salary'])
                
                st.info(f"📍 **Analysis:** Both partners have strong opportunities in {result['city']}. Average commute is manageable at {result['avg_commute']} miles.")
                
                if st.button(f"View Detailed Analysis for {result['city']}", key=f"detail_{idx}"):
                    st.success(f"Detailed analysis for {result['city']} would load here")

# Partner pricing info
st.markdown("---")
st.markdown("### 💰 Partner Subscription Pricing")

st.info("""
**Dual Career Suite Pricing:**
- +1 Partner: Additional 50% of your subscription fee
- +2 Partners: Additional 25% each (for polyamorous relationships)

**Example:** Annual Pro ($149.99/year)
- +1 Partner: $149.99 + $74.99 = $224.98/year
- +2 Partners: $149.99 + $37.50 + $37.50 = $224.99/year
""")

# Future features
st.markdown("---")
st.markdown("### 🚀 Coming Soon")

st.warning("""
**Future Enhancements (Q1 2026):**
- 🗺️ Interactive map visualization showing optimal job clusters
- 🎯 Dartboard view showing "bulls-eye" proximity to perfect match
- 📈 Historical tracking of dual search progress
- 🤝 Couple's interview coordination calendar
- 💬 Partner communication templates for discussing opportunities
""")
