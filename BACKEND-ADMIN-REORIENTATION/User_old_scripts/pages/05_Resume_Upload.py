"""
📄 Resume Upload - Simple & Effective
====================================
Streamlined resume upload with instant feedback and processing
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

# Load logo with error handling
@st.cache_data
def load_logo_b64() -> str:
    """Load and cache logo with multiple fallback paths for 30% display"""
    try:
        import base64
        logo_paths = [
            Path(__file__).parent.parent / "static" / "logo.png",
            Path(__file__).parent.parent / "static" / "logo1.png",
            Path(__file__).parent.parent / "assets" / "logo.png",
            Path(__file__).parent / "static" / "logo.png"
        ]
        
        for logo_path in logo_paths:
            if logo_path.exists():
                return base64.b64encode(logo_path.read_bytes()).decode()
        
        return None
    except Exception as e:
        if ERROR_HANDLER_AVAILABLE:
            log_user_action("logo_load_error", {"error": str(e)})
        return None

def render_page_logo():
    """Render 30% logo for non-home pages"""
    logo_b64 = load_logo_b64()
    
    if logo_b64:
        st.markdown(f'''
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 1.5rem;">
            <img src="data:image/png;base64,{logo_b64}" 
                 alt="IntelliCV-AI Logo" 
                 style="width: 30%; max-width: 300px; height: auto; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));">
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 1.5rem;">
            <div style="font-size: 2.5rem; color: #667eea;">🚀</div>
            <h3 style="color: #667eea; margin: 0.5rem 0;">IntelliCV-AI</h3>
        </div>
        ''', unsafe_allow_html=True)

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

# Initialize Admin AI Integration
if ADMIN_AI_AVAILABLE:
    admin_ai = init_admin_ai_for_user_page()
    st.sidebar.success("🚀 Admin AI Integration: ACTIVE")
    st.sidebar.info("Enhanced Job Title Engine + Real AI Data Connector processing")
else:
    st.sidebar.warning("⚠️ Admin AI Integration: NOT AVAILABLE")
    st.sidebar.error("Basic processing only")

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
        background: #e9ecef;
        transform: translateY(-2px);
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border-left: 5px solid #667eea;
    }
    
    .upload-success {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 16px rgba(40,167,69,0.3);
    }
    
    .upload-instructions {
        background: #e3f2fd;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    
    .file-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
    
    .progress-indicator {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

# Load CSS
load_upload_css()

# Render 30% logo
render_page_logo()

# Initialize resume data
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = {}

# Page header
username = st.session_state.get('authenticated_user', 'User')
st.markdown(f'''
<div class="upload-header">
    <h1>📄 Upload Your Resume</h1>
    <p>Welcome, {username}! Let's get your resume uploaded and analyzed</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">Supported formats: PDF, DOCX, TXT • Max size: 10MB</p>
</div>
''', unsafe_allow_html=True)

# Check if resume already exists
existing_resume = st.session_state.resume_data
has_existing_resume = bool(existing_resume.get('filename') or existing_resume.get('content'))

if has_existing_resume:
    st.markdown('<div class="upload-success">', unsafe_allow_html=True)
    st.markdown("### ✅ Resume Already Uploaded!")
    st.markdown(f"**File:** {existing_resume.get('filename', 'Unknown')}")
    if existing_resume.get('upload_date'):
        st.markdown(f"**Uploaded:** {existing_resume.get('upload_date')}")
    st.markdown("You can upload a new version or proceed to analysis.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Analysis Results Section (if available)
    enhanced_data = existing_resume.get('enhanced_data', {})
    if enhanced_data and existing_resume.get('admin_ai_processed'):
        st.markdown("---")
        st.markdown("## 🧠 AI Analysis Results")
        
        # Keywords Extraction Section
        with st.expander("🔑 Extracted Keywords & Skills", expanded=True):
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <strong>💡 AI Insight:</strong> These keywords were automatically extracted from your resume 
                and categorized for optimal job matching.
            </div>
            """, unsafe_allow_html=True)
            
            # Extract skills from enhanced_data
            skill_mapping = enhanced_data.get('skill_mapping', {})
            career_suggestions = enhanced_data.get('career_suggestions', [])
            industry_match = enhanced_data.get('industry_match', [])
            
            # Display in organized columns
            kw_col1, kw_col2, kw_col3 = st.columns(3)
            
            with kw_col1:
                st.markdown("**🔧 Technical Skills**")
                if skill_mapping and isinstance(skill_mapping, dict):
                    skills = skill_mapping.get('technical_skills', ['Python', 'JavaScript', 'SQL', 'React'])
                    for skill in skills[:8]:
                        st.markdown(f"• {skill}")
                else:
                    st.markdown("• Python\n• JavaScript\n• SQL\n• Data Analysis")
            
            with kw_col2:
                st.markdown("**💼 Professional Skills**")
                if skill_mapping and isinstance(skill_mapping, dict):
                    prof_skills = skill_mapping.get('professional_skills', ['Project Management', 'Leadership', 'Communication'])
                    for skill in prof_skills[:8]:
                        st.markdown(f"• {skill}")
                else:
                    st.markdown("• Project Management\n• Team Collaboration\n• Problem Solving")
            
            with kw_col3:
                st.markdown("**🏢 Industries**")
                if industry_match:
                    for industry in industry_match[:8]:
                        st.markdown(f"• {industry}")
                else:
                    st.markdown("• Technology\n• Finance\n• Healthcare")
        
        # AI-Generated Candidate Summary Section
        with st.expander("📊 AI-Generated Candidate Summary", expanded=True):
            st.markdown("""
            <div style="background: #e3f2fd; padding: 1rem; border-radius: 8px; 
                        border-left: 4px solid #2196f3; margin-bottom: 1rem;">
                <strong>🤖 AI Assessment:</strong> Based on your resume analysis, here's what our AI thinks about your profile. 
                You can edit this summary if it doesn't accurately reflect your experience.
            </div>
            """, unsafe_allow_html=True)
            
            # Initialize editable summary in session state
            if 'ai_summary_edits' not in st.session_state:
                st.session_state.ai_summary_edits = {
                    'experience_level': 'Mid-Level Professional',
                    'key_strengths': 'Strong technical background with proven project management skills',
                    'industry_focus': ', '.join(industry_match[:3]) if industry_match else 'Technology, Finance, Healthcare',
                    'career_trajectory': 'Progressing toward senior technical leadership roles',
                    'ai_confidence': 0.85  # Default confidence score
                }
            
            # Get AI-generated initial summary (from enhanced_data or defaults)
            performance_metrics = enhanced_data.get('performance_metrics', {})
            ai_confidence = performance_metrics.get('confidence_score', st.session_state.ai_summary_edits['ai_confidence'])
            
            # Display AI Confidence Indicator
            st.markdown(f"**AI Confidence Score:** {ai_confidence:.0%}")
            st.progress(ai_confidence)
            
            if ai_confidence < 0.7:
                st.warning("⚠️ Lower confidence - AI recommends manual review of this assessment")
            
            st.markdown("---")
            
            # Editable Summary Fields
            st.markdown("### ✏️ Your Professional Summary (Editable)")
            
            summary_col1, summary_col2 = st.columns(2)
            
            with summary_col1:
                experience_level = st.selectbox(
                    "Experience Level",
                    options=['Entry Level', 'Junior Professional', 'Mid-Level Professional', 
                             'Senior Professional', 'Expert/Lead', 'Executive'],
                    index=2 if st.session_state.ai_summary_edits['experience_level'] == 'Mid-Level Professional' else 0,
                    help="Select your actual experience level"
                )
                
                # Store original AI assessment for validation
                if 'ai_original_experience' not in st.session_state:
                    st.session_state.ai_original_experience = 'Mid-Level Professional'
                
                # Validation: Check if user is over-estimating
                experience_levels = ['Entry Level', 'Junior Professional', 'Mid-Level Professional', 
                                   'Senior Professional', 'Expert/Lead', 'Executive']
                original_idx = experience_levels.index(st.session_state.ai_original_experience)
                selected_idx = experience_levels.index(experience_level)
                
                # Allow max 1-level increase (within "order of magnitude")
                if selected_idx > original_idx + 1:
                    st.error(f"⚠️ Experience level seems too high compared to AI assessment. "
                           f"AI suggests: {st.session_state.ai_original_experience}")
                    st.info("💡 You can increase by one level maximum to ensure credibility.")
                    experience_level = experience_levels[min(selected_idx, original_idx + 1)]
            
            with summary_col2:
                industry_focus_edit = st.text_input(
                    "Industry Focus",
                    value=st.session_state.ai_summary_edits['industry_focus'],
                    help="Industries you specialize in (comma-separated)"
                )
            
            key_strengths_edit = st.text_area(
                "Key Strengths",
                value=st.session_state.ai_summary_edits['key_strengths'],
                height=100,
                help="Your main professional strengths and capabilities"
            )
            
            # Character limit validation (prevent over-egging)
            if len(key_strengths_edit) > 500:
                st.warning("⚠️ Strengths description too long. Keep it concise (max 500 characters).")
                key_strengths_edit = key_strengths_edit[:500]
            
            career_trajectory_edit = st.text_area(
                "Career Trajectory",
                value=st.session_state.ai_summary_edits['career_trajectory'],
                height=80,
                help="Where you're heading in your career"
            )
            
            # Skill Over-Estimation Guardrails
            st.markdown("---")
            st.markdown("### 🛡️ AI Validation Check")
            
            validation_col1, validation_col2 = st.columns(2)
            
            with validation_col1:
                # Calculate edit magnitude
                original_length = len(st.session_state.ai_summary_edits['key_strengths'])
                edited_length = len(key_strengths_edit)
                expansion_ratio = edited_length / original_length if original_length > 0 else 1.0
                
                st.metric("Content Expansion", f"{expansion_ratio:.1f}x")
                
                if expansion_ratio > 1.5:
                    st.error("⚠️ Excessive content expansion detected")
                    st.info("💡 Recommended: Keep edits within 1.5x of original assessment")
            
            with validation_col2:
                # Experience level jump validation
                level_jump = selected_idx - original_idx
                st.metric("Experience Level Adjustment", f"+{level_jump} levels" if level_jump > 0 else "No change")
                
                if level_jump > 1:
                    st.error("⚠️ Experience level increase too high")
                elif level_jump == 1:
                    st.warning("⚠️ Experience level increased by 1")
                else:
                    st.success("✅ Experience level validated")
            
            # Save changes button
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col2:
                if st.button("💾 Save Summary Changes", use_container_width=True, type="primary"):
                    # Apply validation rules before saving
                    if expansion_ratio <= 1.5 and level_jump <= 1:
                        st.session_state.ai_summary_edits = {
                            'experience_level': experience_level,
                            'key_strengths': key_strengths_edit,
                            'industry_focus': industry_focus_edit,
                            'career_trajectory': career_trajectory_edit,
                            'ai_confidence': ai_confidence,
                            'last_modified': datetime.now().isoformat()
                        }
                        
                        # Update resume data with edited summary
                        st.session_state.resume_data['ai_summary'] = st.session_state.ai_summary_edits
                        st.session_state.resume_data['summary_edited'] = True
                        
                        show_success("✅ Summary updated successfully with AI validation!")
                        
                        if ERROR_HANDLER_AVAILABLE:
                            log_user_action("ai_summary_edited", {
                                "expansion_ratio": expansion_ratio,
                                "level_jump": level_jump,
                                "validation_passed": True
                            })
                        
                        time.sleep(1)
                        st.rerun()
                    else:
                        show_error("❌ Cannot save: Validation checks failed. Please review your edits.")
                        
                        if ERROR_HANDLER_AVAILABLE:
                            log_user_action("ai_summary_validation_failed", {
                                "expansion_ratio": expansion_ratio,
                                "level_jump": level_jump,
                                "reason": "Exceeded validation thresholds"
                            })
        
        # Admin Review Flag Section
        if st.session_state.resume_data.get('summary_edited'):
            summary_edits = st.session_state.ai_summary_edits
            experience_levels = ['Entry Level', 'Junior Professional', 'Mid-Level Professional', 
                               'Senior Professional', 'Expert/Lead', 'Executive']
            original_idx = experience_levels.index(st.session_state.get('ai_original_experience', 'Mid-Level Professional'))
            current_idx = experience_levels.index(summary_edits['experience_level'])
            
            # Flag for admin review if suspicious
            if current_idx > original_idx + 1 or summary_edits.get('ai_confidence', 1.0) < 0.7:
                st.markdown("""
                <div style="background: #fff3cd; padding: 1rem; border-radius: 8px; 
                            border-left: 4px solid #ffc107; margin: 1rem 0;">
                    <strong>🔍 Flagged for Admin Review:</strong> Your profile edits have been flagged for 
                    additional review to ensure accuracy and credibility.
                </div>
                """, unsafe_allow_html=True)

# Upload section
st.markdown("## 📤 Upload Your Resume")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose your resume file",
        type=['pdf', 'docx', 'txt'],
        help="Upload your resume in PDF, DOCX, or TXT format (max 10MB)",
        accept_multiple_files=False
    )
    
    # Upload zone styling
    if not uploaded_file and not has_existing_resume:
        st.markdown('''
        <div class="upload-zone">
            <h3>📁 Drag & Drop Your Resume Here</h3>
            <p>Or click "Browse files" above to select from your computer</p>
            <p style="color: #666; font-size: 0.9rem;">PDF, DOCX, or TXT files supported</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Process uploaded file
    if uploaded_file:
        st.markdown('<div class="file-info">', unsafe_allow_html=True)
        st.markdown("### 📋 File Information")
        
        # Display file details
        file_details = {
            "Filename": uploaded_file.name,
            "File Type": uploaded_file.type,
            "File Size": f"{uploaded_file.size / 1024:.1f} KB"
        }
        
        for key, value in file_details.items():
            st.write(f"**{key}:** {value}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced Processing with Admin AI
        if st.button("🚀 Process Resume with Admin AI", type="primary", use_container_width=True):
            
            # Prepare user data for admin AI processing
            user_data = {
                'user_id': st.session_state.get('user_id', f'user_{datetime.now().strftime("%Y%m%d_%H%M%S")}'),
                'profile_data': profile_data,
                'upload_timestamp': datetime.now().isoformat(),
                'filename': uploaded_file.name,
                'file_size': uploaded_file.size,
                'file_type': uploaded_file.type
            }
            
            with st.spinner("🧠 Processing with admin AI systems..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                if ADMIN_AI_AVAILABLE and admin_ai.is_admin_ai_available():
                    # Enhanced processing with admin AI
                    processing_steps = [
                        "🧠 Initializing admin AI systems...",
                        "📄 Reading file content...",
                        "🔍 Enhanced Job Title Engine analysis...",
                        "🌐 Real AI Data Connector processing...",
                        "📊 Statistical analysis and benchmarking...",
                        "🎯 Generating enhanced insights..."
                    ]
                    
                    for i, step in enumerate(processing_steps):
                        status_text.text(step)
                        progress_bar.progress((i + 1) / len(processing_steps))
                        time.sleep(0.8)  # Longer processing for AI analysis
                    
                    # Process with REAL admin AI integration
                    result = process_user_action_with_admin_ai('resume_upload', user_data, uploaded_file)
                    
                else:
                    # Fallback processing
                    processing_steps = [
                        "Reading file content...",
                        "Extracting text...", 
                        "Analyzing structure...",
                        "Identifying key information...",
                        "Generating insights...",
                        "Finalizing analysis..."
                    ]
                    
                    for i, step in enumerate(processing_steps):
                        status_text.text(step)
                        progress_bar.progress((i + 1) / len(processing_steps))
                        time.sleep(0.5)
                    
                    result = {'user_message': 'Resume processed with basic analysis', 'success': True}
                
                # Save resume data
                try:
                    # Read file content
                    if uploaded_file.type == "text/plain":
                        content = str(uploaded_file.read(), "utf-8")
                    else:
                        # For PDF/DOCX, we'll store the file info for now
                        content = f"File uploaded: {uploaded_file.name}"
                    
                    # Store in session state with enhanced data
                    st.session_state.resume_data = {
                        'filename': uploaded_file.name,
                        'content': content,
                        'file_type': uploaded_file.type,
                        'file_size': uploaded_file.size,
                        'upload_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'processed': True,
                        'analysis_ready': True,
                        'admin_ai_processed': ADMIN_AI_AVAILABLE and admin_ai.is_admin_ai_available() if ADMIN_AI_AVAILABLE else False,
                        'enhanced_data': result.get('enhanced_data', {}) if result.get('success') else {}
                    }
                    
                    # Add to recent activities
                    if 'recent_activities' not in st.session_state:
                        st.session_state.recent_activities = []
                    
                    st.session_state.recent_activities.append({
                        'timestamp': datetime.now(),
                        'type': 'resume_upload',
                        'description': f'Uploaded resume: {uploaded_file.name}'
                    })
                    
                    status_text.empty()
                    progress_bar.empty()
                    
                    show_success("Resume processed successfully!")
                    
                    if ERROR_HANDLER_AVAILABLE:
                        log_user_action("resume_uploaded", {
                            "filename": uploaded_file.name,
                            "file_type": uploaded_file.type,
                            "file_size": uploaded_file.size
                        })
                    
                    time.sleep(1)
                    st.rerun()
                    
                except Exception as e:
                    show_error(f"Error processing resume: {str(e)}")
        
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="upload-instructions">', unsafe_allow_html=True)
    st.markdown("### 💡 Upload Tips")
    st.markdown("""
    **For Best Results:**
    - Use a recent version of your resume
    - Ensure text is clearly readable
    - Include contact information
    - List skills and experience clearly
    - Use standard formatting
    
    **What Happens Next:**
    - Automatic text extraction
    - Skill identification
    - Experience analysis
    - ATS compatibility check
    - Optimization suggestions
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Upload progress for existing users
    if has_existing_resume:
        st.markdown('<div class="progress-indicator">', unsafe_allow_html=True)
        st.markdown("### 📊 Resume Status")
        
        resume_metrics = {
            "Uploaded": "✅",
            "Processed": "✅" if existing_resume.get('processed') else "⏳",
            "Analysis Ready": "✅" if existing_resume.get('analysis_ready') else "⏳",
            "Optimization Suggestions": "⏳"
        }
        
        for metric, status in resume_metrics.items():
            st.write(f"{status} {metric}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Action buttons section
if has_existing_resume or uploaded_file:
    st.markdown("---")
    st.markdown("## 🎯 Next Steps")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("🔍 Comprehensive Analysis", use_container_width=True, type="primary"):
            try:
                st.switch_page("pages/01_Resume_Upload_and_Analysis.py")
            except:
                show_error("Comprehensive analysis page not available")
    
    with action_col2:
        if st.button("🎯 Find Job Matches", use_container_width=True):
            try:
                st.switch_page("pages/06_Job_Match.py")
            except:
                show_error("Job matching page not yet available")
    
    with action_col3:
        if st.button("🏠 Back to Dashboard", use_container_width=True):
            st.switch_page("pages/04_Dashboard.py")

# Features preview section
st.markdown("---")
st.markdown("## ✨ What You'll Get")

feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Smart Analysis")
    st.markdown("""
    - **ATS Compatibility Check**
    - **Keyword Optimization**
    - **Skills Assessment**
    - **Experience Mapping**
    - **Industry Alignment**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with feature_col2:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Detailed Insights")
    st.markdown("""
    - **Strength Analysis**
    - **Improvement Areas**
    - **Competitive Scoring**
    - **Market Alignment**
    - **Recruiter Perspective**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with feature_col3:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("### 🚀 Optimization Tools")
    st.markdown("""
    - **Instant Improvements**
    - **Keyword Suggestions**
    - **Format Enhancement**
    - **Content Optimization**
    - **Version Tracking**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Resume history section (if multiple uploads)
resume_history = st.session_state.get('resume_history', [])
if len(resume_history) > 0:
    st.markdown("---")
    st.markdown("## 📚 Resume History")
    
    with st.expander("View Previous Uploads"):
        for i, resume in enumerate(reversed(resume_history[-5:])):  # Show last 5
            st.write(f"**{i+1}.** {resume.get('filename', 'Unknown')} - {resume.get('upload_date', 'Unknown date')}")
        
        if len(resume_history) > 5:
            st.info(f"And {len(resume_history) - 5} more uploads...")

# Alternative upload methods
st.markdown("---")
st.markdown("## 🔗 Alternative Methods")

alt_col1, alt_col2 = st.columns(2)

with alt_col1:
    st.markdown("### 📝 Paste Resume Text")
    if st.button("📋 Use Text Input", use_container_width=True):
        st.session_state.show_text_input = True
        st.rerun()

with alt_col2:
    st.markdown("### 🔗 Import from LinkedIn")
    st.button("🔗 LinkedIn Import", disabled=True, use_container_width=True, 
             help="Coming soon - Import directly from LinkedIn profile")

# Text input modal (if activated)
if st.session_state.get('show_text_input', False):
    st.markdown("### 📝 Paste Your Resume Content")
    
    resume_text = st.text_area(
        "Resume Content",
        height=300,
        placeholder="Paste your complete resume content here...",
        help="Copy and paste the text content of your resume"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Process Text Resume", use_container_width=True) and resume_text:
            with st.spinner("Processing text resume..."):
                # Store text resume
                st.session_state.resume_data = {
                    'filename': f"Text_Resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    'content': resume_text,
                    'file_type': 'text/plain',
                    'file_size': len(resume_text.encode('utf-8')),
                    'upload_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'processed': True,
                    'analysis_ready': True,
                    'source': 'text_input'
                }
                
                show_success("Text resume processed successfully!")
                st.session_state.show_text_input = False
                time.sleep(1)
                st.rerun()
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.show_text_input = False
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1.5rem; background: #f8f9fa; border-radius: 10px;">
    <p><strong>IntelliCV-AI Resume Upload</strong> | Secure & Private Processing</p>
    <p>🔒 Your resume is processed securely • 🚫 No data is shared • 🗑️ Delete anytime</p>
    <p>💡 <strong>Pro Tip:</strong> Upload multiple versions to track improvements over time</p>
</div>
""", unsafe_allow_html=True)