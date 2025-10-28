"""
☁️ Universal Cloud Maker - Dynamic Skill & Career Visualizations
================================================================
Generate word clouds and skill visualizations from your career data:
- Skills Cloud with importance weighting
- Job Titles Cloud
- Industry Keywords Cloud
- Peer Group Overlays

Premium Feature | Token Cost: 8 tokens
"""

import streamlit as st
from pathlib import Path
import pandas as pd
import sys
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Setup paths
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

# Add admin_portal to path for ai_data_loader access
admin_portal_path = current_dir.parent / "admin_portal"
sys.path.insert(0, str(admin_portal_path))

# Import portal bridge for cross-portal communication
try:
    from shared_backend.services.portal_bridge import ResumeService, IntelligenceService
    resume_service = ResumeService()
    intelligence_service = IntelligenceService()
    PORTAL_BRIDGE_AVAILABLE = True
except ImportError as e:
    PORTAL_BRIDGE_AVAILABLE = False
    resume_service = None
    intelligence_service = None

# Import AI data loader for fallback data
try:
    from ai_data_loader import AIDataLoader
    ai_loader = AIDataLoader()
    AI_LOADER_AVAILABLE = True
except ImportError:
    AI_LOADER_AVAILABLE = False
    ai_loader = None

# Page configuration
st.set_page_config(
    page_title="☁️ Universal Cloud Maker | IntelliCV-AI",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication check
if not st.session_state.get('authenticated_user'):
    st.error("🔒 Please log in to access Universal Cloud Maker")
    if st.button("🏠 Return to Home"):
        st.switch_page("main.py")
    st.stop()

# Tier check for premium features
user_tier = st.session_state.get('subscription_tier', 'free')
PREMIUM_TIERS = ['monthly_pro', 'annual_pro', 'enterprise_pro']

if user_tier not in PREMIUM_TIERS:
    st.warning("⭐ Universal Cloud Maker requires Premium subscription")
    if st.button("⬆️ Upgrade to Premium", type="primary"):
        st.switch_page("pages/06_Pricing.py")
    st.stop()

# Title and introduction
st.title("☁️ Universal Cloud Maker")
st.markdown("**Generate dynamic word clouds and visualizations from your career data**")

st.info("💎 **Token Cost: 8 tokens** | AI-powered cloud generation with skill weighting")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    # Cloud type selection
    cloud_type = st.selectbox(
        "☁️ Cloud Type",
        ["Skills Cloud", "Job Titles Cloud", "Industry Keywords Cloud", "Technologies Cloud"]
    )
    
    # Data source
    data_source = st.radio(
        "📊 Data Source",
        ["My Resume", "Job Description", "Industry Analysis"],
        horizontal=True
    )

with col2:
    # Cloud options
    max_words = st.slider("📏 Max Words", 20, 200, 100, 10)
    color_scheme = st.selectbox("🎨 Color Scheme", 
                                ["Blues", "Greens", "Purples", "Reds", "Viridis"])
    
    show_weights = st.checkbox("📊 Show Importance Weights", value=True)

# Overlay options
with st.expander("🔄 Overlay Options"):
    enable_overlay = st.checkbox("Enable Peer Comparison Overlay")
    if enable_overlay:
        overlay_type = st.selectbox("Overlay Type", 
                                   ["Peer Average", "Top Performers", "Industry Standard"])

# Generate button
if st.button("🎨 Generate Cloud", type="primary", use_container_width=True):
    with st.spinner("☁️ Generating cloud visualization..."):
        
        # Get resume data from session
        resume_data = st.session_state.get('resume_data', {})
        
        if not resume_data and data_source == "My Resume":
            st.warning("⚠️ No resume data found. Please upload your resume first.")
            if st.button("📄 Go to Resume Analysis"):
                st.switch_page("pages/09_Resume_Upload_Analysis.py")
        else:
            # Generate cloud using portal_bridge
            if PORTAL_BRIDGE_AVAILABLE and intelligence_service:
                try:
                    # Extract skills with weights using portal_bridge
                    enriched_data = intelligence_service.enrich(
                        resume_data=resume_data,
                        intelligence_types=['skills', 'skill_weights', 'technologies']
                    )
                    
                    st.success("✅ Cloud data extracted from admin AI!")
                    
                    # Prepare word cloud data
                    if cloud_type == "Skills Cloud":
                        words = enriched_data.get('skills', [])
                        weights = enriched_data.get('skill_weights', {})
                    elif cloud_type == "Technologies Cloud":
                        words = enriched_data.get('technologies', [])
                        weights = {tech: 1.0 for tech in words}
                    else:
                        # Fallback
                        words = ["Python", "Machine Learning", "Data Science", "SQL", 
                                "Leadership", "Cloud Computing", "AI", "Analytics"]
                        weights = {word: 1.0 for word in words}
                    
                    # Create word frequency dict
                    word_freq = {word: weights.get(word, 1.0) for word in words}
                    
                    # Generate word cloud
                    if word_freq:
                        wordcloud = WordCloud(
                            width=800, 
                            height=400,
                            background_color='white',
                            colormap=color_scheme,
                            max_words=max_words
                        ).generate_from_frequencies(word_freq)
                        
                        # Display word cloud
                        fig, ax = plt.subplots(figsize=(10, 5))
                        ax.imshow(wordcloud, interpolation='bilinear')
                        ax.axis('off')
                        st.pyplot(fig)
                        
                        # Show weights if enabled
                        if show_weights:
                            st.markdown("### 📊 Word Importance Weights")
                            weights_df = pd.DataFrame([
                                {"Word": word, "Weight": weight} 
                                for word, weight in sorted(word_freq.items(), 
                                                          key=lambda x: x[1], 
                                                          reverse=True)[:20]
                            ])
                            st.dataframe(weights_df, use_container_width=True)
                    else:
                        st.warning("⚠️ No data available for cloud generation")
                    
                except Exception as e:
                    st.error(f"❌ Error generating cloud: {str(e)}")
                    st.info("Using fallback cloud generation...")
                    
                    # Fallback word cloud
                    fallback_words = {
                        "Python": 10, "Machine Learning": 9, "Data Science": 8,
                        "SQL": 7, "Leadership": 6, "Cloud Computing": 8,
                        "AI": 9, "Analytics": 7, "React": 5, "AWS": 6
                    }
                    
                    wordcloud = WordCloud(
                        width=800, height=400, background_color='white',
                        colormap=color_scheme, max_words=max_words
                    ).generate_from_frequencies(fallback_words)
                    
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    st.pyplot(fig)
                    st.warning("⚠️ Using sample data - please ensure admin backend is running")
            
            else:
                st.warning("⚠️ Portal bridge unavailable - using AI data fallback")
                
                # Generate word cloud from AI data loader (real CV data)
                sample_words = {}
                
                if AI_LOADER_AVAILABLE and ai_loader:
                    try:
                        # Load real skills from AI data
                        real_skills = ai_loader.load_real_skills_data()
                        if real_skills:
                            # Use frequency data from real skills
                            if isinstance(real_skills, dict):
                                for skill, data in list(real_skills.items())[:max_words]:
                                    freq = data.get('frequency', 5) if isinstance(data, dict) else 5
                                    sample_words[skill] = freq
                            elif isinstance(real_skills, list):
                                # If list, assign equal frequency
                                for skill in real_skills[:max_words]:
                                    sample_words[skill] = 5
                    except Exception as e:
                        st.warning(f"Could not load AI data: {e}")
                
                # Minimal fallback if AI loader unavailable
                if not sample_words:
                    sample_words = {
                        "Data Analysis": 10, "Problem Solving": 9, "Communication": 8,
                        "Leadership": 7, "Technical Skills": 8, "Project Management": 7
                    }
                
                wordcloud = WordCloud(
                    width=800, height=400, background_color='white',
                    colormap=color_scheme, max_words=max_words
                ).generate_from_frequencies(sample_words)
                
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
                
                if AI_LOADER_AVAILABLE:
                    st.info("ℹ️ Running with AI data fallback - start admin backend for real-time analysis")
                else:
                    st.info("ℹ️ Running in offline mode - start admin backend for real data")

# Footer
st.markdown("---")
st.markdown("*Powered by IntelliCV-AI Universal Cloud Maker*")
