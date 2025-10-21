"""
📄 Resume Upload - Enhanced with Admin AI Integration
===================================================
Streamlined resume upload with REAL admin AI analysis and processing
NOW WITH: Enhanced Job Title Engine + Real AI Data Connector + Statistical Tools
"""

import streamlit as st
from pathlib import Path
import time
from datetime import datetime
import tempfile
import os

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
    page_title="📄 Resume Upload | IntelliCV-AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication check
if not st.session_state.get('authenticated_user'):
    st.error("🔒 Please log in to upload your resume")
    if st.button("🏠 Return to Home"):
        st.switch_page("pages/00_Home.py")
    st.stop()

# Initialize Admin AI Integration
if ADMIN_AI_AVAILABLE:
    admin_ai = init_admin_ai_for_user_page()
    st.sidebar.success("🚀 Admin AI Integration: ACTIVE")
    st.sidebar.info("Enhanced analysis with 422-line job engine + 548-line data connector processing 3,418+ JSON files")
else:
    st.sidebar.warning("⚠️ Admin AI Integration: NOT AVAILABLE")
    st.sidebar.error("Basic processing only")

# Check profile completion
profile_data = st.session_state.get('profile_data', {})
required_fields = ['full_name', 'email', 'phone', 'location']
completed_fields = sum(1 for field in required_fields if profile_data.get(field))
profile_completion = (completed_fields / len(required_fields)) * 100

if profile_completion < 50:
    st.warning("⚠️ Complete at least 50% of your profile before uploading resume")
    if st.button("👤 Complete Profile"):
        st.switch_page("pages/02_Profile.py")
    st.stop()

# Professional CSS styling
def load_upload_css():
    css = '''
    <style>
    .upload-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    .upload-zone {
        border: 3px dashed #667eea;
        border-radius: 12px;
        padding: 3rem;
        text-align: center;
        background: #f8f9fa;
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-zone:hover {
        border-color: #764ba2;
        background: #f0f2f6;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .ai-enhancement-box {
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(40,167,69,0.3);
    }
    
    .admin-integration-status {
        background: #e3f2fd;
        border-left: 5px solid #2196f3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 5px 5px 0;
    }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

load_upload_css()

# Header with Admin AI status
st.markdown('''
<div class="upload-header">
    <h1>📄 Enhanced Resume Upload</h1>
    <p>Upload your resume and get <strong>real AI analysis</strong> powered by admin intelligence systems</p>
</div>
''', unsafe_allow_html=True)

# Admin AI Integration Status Display
if ADMIN_AI_AVAILABLE and admin_ai.is_admin_ai_available():
    st.markdown('''
    <div class="ai-enhancement-box">
        <h3>🚀 AI Enhancement Active</h3>
        <p><strong>Enhanced Job Title Engine:</strong> 422 lines of LinkedIn industry integration</p>
        <p><strong>Real AI Data Connector:</strong> 548 lines processing 3,418+ JSON files</p>
        <p><strong>Statistical Analysis:</strong> Admin-grade benchmarking and insights</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Display integration status
    admin_ai.display_admin_integration_status()
    
else:
    st.markdown('''
    <div class="admin-integration-status">
        <h4>⚠️ Limited Processing Available</h4>
        <p>Admin AI systems not connected - using basic processing only</p>
    </div>
    ''', unsafe_allow_html=True)

# File upload section
st.markdown('''
<div class="upload-zone">
    <h3>📂 Select Your Resume</h3>
    <p>Supported formats: PDF, DOCX, DOC, TXT</p>
</div>
''', unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader(
    "Choose your resume file",
    type=['pdf', 'docx', 'doc', 'txt'],
    help="Upload your resume for AI-powered analysis"
)

# Process uploaded file with Admin AI Integration
if uploaded_file is not None:
    st.success(f"📄 File uploaded: {uploaded_file.name}")
    
    # Prepare user data for admin AI processing
    user_data = {
        'user_id': st.session_state.get('user_id', f'user_{datetime.now().strftime("%Y%m%d_%H%M%S")}'),
        'profile_data': profile_data,
        'upload_timestamp': datetime.now().isoformat(),
        'filename': uploaded_file.name,
        'file_size': uploaded_file.size,
        'file_type': uploaded_file.type
    }
    
    # Display processing status
    with st.spinner("Processing with AI systems..."):
        if ADMIN_AI_AVAILABLE:
            # Process with REAL admin AI integration
            result = process_user_action_with_admin_ai('resume_upload', user_data, uploaded_file)
            
            # Display results
            st.success(result['user_message'])
            
            # Show enhanced analysis if available
            if result.get('enhanced_data'):
                st.subheader("🧠 AI Analysis Results")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'career_suggestions' in result['enhanced_data']:
                        st.write("**🎯 Career Suggestions (Admin AI Enhanced):**")
                        for suggestion in result['enhanced_data']['career_suggestions']:
                            st.write(f"• {suggestion}")
                    
                    if 'industry_match' in result['enhanced_data']:
                        st.write("**🏢 Industry Match (LinkedIn Integration):**")
                        for industry in result['enhanced_data']['industry_match']:
                            st.write(f"• {industry}")
                
                with col2:
                    if 'market_insights' in result['enhanced_data']:
                        st.write("**📊 Market Insights (Real Data Analysis):**")
                        insights = result['enhanced_data']['market_insights']
                        if isinstance(insights, dict):
                            for key, value in insights.items():
                                st.write(f"• {key}: {value}")
                    
                    if 'performance_metrics' in result['enhanced_data']:
                        st.write("**📈 Performance Metrics (Statistical Analysis):**")
                        metrics = result['enhanced_data']['performance_metrics']
                        if isinstance(metrics, dict):
                            for metric, value in metrics.items():
                                st.metric(metric.title(), value)
            
            # Show bidirectional enrichment status
            if result.get('bidirectional_enrichment'):
                st.info("✅ Your data has enhanced our AI systems for future users")
            
            # Show admin AI analysis details (for transparency)
            if st.checkbox("🔍 Show Admin AI Analysis Details"):
                st.json(result.get('admin_ai_analysis', {}))
                
        else:
            # Basic processing fallback
            st.warning("Processing with basic system (Admin AI not available)")
            
            # Simple file processing
            file_details = {
                'filename': uploaded_file.name,
                'size': uploaded_file.size,
                'type': uploaded_file.type
            }
            
            st.json(file_details)
            st.info("📈 For enhanced AI analysis, enable admin AI integration")
    
    # Action buttons
    st.subheader("🎯 Next Steps")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Find Matching Jobs"):
            st.switch_page("pages/06_Job_Match.py")
    
    with col2:
        if st.button("📊 View Analysis"):
            st.switch_page("pages/AI_Career_Intelligence.py")
    
    with col3:
        if st.button("👤 Update Profile"):
            st.switch_page("pages/02_Profile.py")

# Instructions and tips
st.subheader("💡 Tips for Better Analysis")

tips_col1, tips_col2 = st.columns(2)

with tips_col1:
    st.markdown("""
    **📝 Resume Best Practices:**
    - Use clear job titles and company names
    - Include specific skills and technologies
    - Add quantifiable achievements
    - Use industry-standard keywords
    """)

with tips_col2:
    st.markdown("""
    **🚀 AI Enhancement Benefits:**
    - LinkedIn industry classification
    - Enhanced job title analysis
    - Market intelligence insights
    - Statistical performance benchmarking
    """)

# Footer with system status
st.markdown("---")
st.markdown(f"**System Status:** Admin AI Integration: {'✅ Active' if ADMIN_AI_AVAILABLE and admin_ai.is_admin_ai_available() if ADMIN_AI_AVAILABLE else '❌ Not Available'}")
st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Log user action
if ERROR_HANDLER_AVAILABLE:
    log_user_action("resume_upload_page_viewed", {
        'user_id': st.session_state.get('user_id'),
        'admin_ai_available': ADMIN_AI_AVAILABLE,
        'timestamp': datetime.now().isoformat()
    })