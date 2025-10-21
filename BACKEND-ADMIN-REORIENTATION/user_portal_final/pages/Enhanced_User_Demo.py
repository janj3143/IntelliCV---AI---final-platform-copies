"""
Enhanced User Portal Demo - User-Focused UX Components
=====================================================

Demo page showcasing user-focused UI components without administrative
monitoring features. This demonstrates the proper separation between
user portal (job seekers) and admin portal (system administrators).

Author: IntelliCV Enhancement Team
Python Environment: IntelliCV/env310
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import random

# Add shared infrastructure to path
shared_path = Path(__file__).parent.parent / "shared_infrastructure_final"
if str(shared_path) not in sys.path:
    sys.path.insert(0, str(shared_path))

# Import user-focused UI components
try:
    from ui.user_components import *
    USER_COMPONENTS_AVAILABLE = True
except ImportError as e:
    st.error(f"User components not available: {e}")
    USER_COMPONENTS_AVAILABLE = False

# =============================================================================
# PAGE SETUP
# =============================================================================

st.set_page_config(
    page_title="User Portal Demo | IntelliCV",
    page_icon="👤",
    layout="wide"
)

if USER_COMPONENTS_AVAILABLE:
    inject_user_portal_css()

# =============================================================================
# MAIN DEMO CONTENT
# =============================================================================

if USER_COMPONENTS_AVAILABLE:
    
    # Welcome header
    render_user_welcome_header(
        user_name="John Smith",
        recent_activity="Last login: 2 hours ago"
    )
    
    # User stats dashboard
    user_stats = {
        "Profile Score": "92%",
        "Job Matches": "18",
        "Applications": "7",
        "Interviews": "2"
    }
    render_user_stats_dashboard(user_stats)
    
    # Create tabs for different user functions
    tab1, tab2, tab3, tab4 = st.tabs([
        "📤 CV Upload",
        "🎯 Job Matches",
        "📋 My Applications",
        "👤 Profile & Progress"
    ])
    
    with tab1:
        st.markdown("## 📤 CV/Resume Upload")
        
        # CV upload area
        uploaded_file = render_cv_upload_area("demo")
        
        if uploaded_file:
            st.markdown("### ✅ CV Processing Results")
            
            # Simulate CV processing results
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 CV Analysis")
                analysis_data = {
                    "Skills Identified": "15",
                    "Experience Level": "Mid-Level",
                    "Education Level": "Bachelor's",
                    "Certifications": "3"
                }
                render_user_stats_dashboard(analysis_data)
            
            with col2:
                st.markdown("#### 🎯 Job Matching Preview")
                st.info("Based on your CV, we found 18 matching jobs!")
                st.success("Your profile is 92% complete")
                st.warning("Consider adding more skills to improve matches")
    
    with tab2:
        # Sample job matches
        job_matches = [
            {'company': 'TechCorp Inc.', 'title': 'Senior Software Engineer', 'location': 'San Francisco, CA', 'score': 95},
            {'company': 'DataSystems Ltd.', 'title': 'Full Stack Developer', 'location': 'New York, NY', 'score': 88},
            {'company': 'AI Solutions', 'title': 'Machine Learning Engineer', 'location': 'Seattle, WA', 'score': 82},
            {'company': 'StartupXYZ', 'title': 'Lead Developer', 'location': 'Austin, TX', 'score': 76}
        ]
        render_job_matches(job_matches)
    
    with tab3:
        # Sample applications
        applications = [
            {'company': 'TechCorp Inc.', 'title': 'Senior Software Engineer', 'status': 'interview', 'date_applied': '2024-01-15'},
            {'company': 'DataSystems Ltd.', 'title': 'Full Stack Developer', 'status': 'applied', 'date_applied': '2024-01-12'},
            {'company': 'WebDev Co.', 'title': 'Frontend Developer', 'status': 'offer', 'date_applied': '2024-01-08'},
            {'company': 'CodeFactory', 'title': 'Backend Engineer', 'status': 'rejected', 'date_applied': '2024-01-05'},
        ]
        render_application_tracker(applications)
    
    with tab4:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # User profile section
            sample_profile = {
                'name': 'John Smith',
                'email': 'john.smith@email.com',
                'phone': '+1 (555) 123-4567',
                'location': 'San Francisco, CA',
                'skills': ['Python', 'JavaScript', 'React']
            }
            render_user_profile_section(sample_profile)
        
        with col2:
            # Progress section
            progress_data = {
                'profile_complete': 92,
                'cvs_uploaded': 3,
                'jobs_applied': 7,
                'interviews': 2
            }
            render_user_progress_section(progress_data)
    
    # Quick actions section
    st.markdown("---")
    render_user_quick_actions()
    
    # Tips sidebar
    render_user_tips_sidebar()

else:
    # Fallback when components are not available
    st.title("👤 User Portal Demo")
    st.error("Enhanced user components are not available. Please check the shared infrastructure setup.")
    
    st.markdown("""
    ## What This Demo Would Show:
    
    - **CV Upload Area**: Enhanced file upload with drag-and-drop
    - **Job Matching**: AI-powered job recommendations 
    - **Application Tracking**: Status of submitted applications
    - **Profile Management**: Update personal and professional info
    - **Progress Dashboard**: Track job search journey
    - **User-Friendly Interface**: Clean, intuitive design focused on job seekers
    
    ### Key Differences from Admin Portal:
    
    ✅ **User Portal Features:**
    - CV/Resume upload and processing
    - Job search and matching
    - Application management
    - Personal profile editing
    - Career progress tracking
    
    ❌ **No Administrative Features:**
    - No service status monitoring
    - No Docker controls
    - No system administration tools
    - No backend API management
    - No database administration
    """)

# =============================================================================
# DEMO INFORMATION
# =============================================================================

with st.expander("ℹ️ About This Demo", expanded=False):
    st.markdown("""
    ### User Portal Focus
    
    This demo showcases the **user-focused** components that are appropriate for
    the user portal. Notice how all features are centered around the job seeker
    experience:
    
    - **CV Processing**: Help users upload and analyze resumes
    - **Job Matching**: Connect users with relevant opportunities  
    - **Application Management**: Track application status and interviews
    - **Profile Building**: Maintain professional information
    - **Progress Tracking**: Visualize job search journey
    
    ### Administrative Functions Moved
    
    The following administrative functions have been moved to admin portals where they belong:
    
    - 🔧 Service Status Monitoring → Admin Portal
    - 🐳 Docker Controls → Admin Portal  
    - 🛠️ Development Tools → Admin Portal
    - 📊 System Information → Admin Portal
    - 🔧 Backend API Management → Admin Portal
    
    This separation ensures:
    - **Security**: Regular users can't access system controls
    - **Usability**: Clean, focused interface for each user type
    - **Maintainability**: Clear separation of concerns
    """)