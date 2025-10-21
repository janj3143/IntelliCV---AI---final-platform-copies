#!/usr/bin/env python3
"""
🚀 IntelliCV-AI Enhanced User Portal - SANDBOX Version
Clean user portal with integrated home page and background logo
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="IntelliCV-AI | Your Unique Career & Advisory Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load professional logo background CSS
def load_professional_css():
    """Load the professional logo background CSS with highly visible logo"""
    st.markdown("""
    <style>
    .stApp {
        background: 
            linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%),
            url('static/logo1.png') center/contain no-repeat fixed !important;
        background-size: 60% auto;
        background-position: center center;
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 2rem auto;
        padding: 2rem !important;
    }
    
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
    }
    
    /* Make logo highly visible */
    .logo-watermark {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('static/logo1.png') center/contain no-repeat fixed;
        opacity: 0.1;
        pointer-events: none;
        z-index: -1;
    }
    </style>
    <div class="logo-watermark"></div>
    """, unsafe_allow_html=True)

# Apply professional styling
load_professional_css()

# Simple session state initialization
if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None

def show_sidebar():
    """Simple clean sidebar"""
    if not st.session_state.get("authenticated_user"):
        return

    st.sidebar.title("📂 IntelliCV")
    
    # Core Tools
    st.sidebar.markdown("### 🚀 Core Tools")
    st.sidebar.page_link("pages/01_Resume_Upload_and_Analysis.py", label="📊 Resume Analysis Hub")
    st.sidebar.page_link("pages/02_Profile.py", label="👤 Profile")
    st.sidebar.page_link("pages/03_Job_Description.py", label="📄 Job Description")
    st.sidebar.page_link("pages/04_Resume_Feedback.py", label="💬 Resume Feedback")
    st.sidebar.page_link("pages/05_Job_Match_Insights.py", label="🎯 Job Match Insights")
    st.sidebar.page_link("pages/06_Resume_History.py", label="📄 Resume History")
    
    st.sidebar.markdown("---")
    
    # Career Development
    st.sidebar.markdown("### 🎯 Career Development")
    st.sidebar.page_link("pages/09_Job_Tracker.py", label="📊 Job Tracker")
    
    st.sidebar.markdown("---")
    
    # Settings
    st.sidebar.markdown("### ⚙️ Settings")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated_user = False
        st.session_state.user_id = None
        st.rerun()

def show_home_page():
    """Integrated Home Page with Authentication and Highly Visible Logo"""
    
    # Main title with logo
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <h1 style="color: #1f2937; font-size: 4rem; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            🚀 Welcome to IntelliCV-AI
        </h1>
        <h2 style="color: #6b7280; font-size: 2rem; margin-bottom: 2rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">
            Your Intelligent Career & Resume Platform
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Authentication section
    if not st.session_state.get("authenticated_user"):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔐 Please Login or Register")
            
            tab1, tab2 = st.tabs(["Login", "Register"])
            
            with tab1:
                with st.form("login_form"):
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    login_button = st.form_submit_button("Login", use_container_width=True)
                    
                    if login_button:
                        if username and password:
                            st.session_state.authenticated_user = True
                            st.session_state.user_id = username
                            st.success("✅ Login successful!")
                            st.rerun()
                        else:
                            st.error("Please enter both username and password")
            
            with tab2:
                with st.form("register_form"):
                    reg_username = st.text_input("Choose Username")
                    reg_email = st.text_input("Email Address") 
                    reg_password = st.text_input("Choose Password", type="password")
                    reg_confirm = st.text_input("Confirm Password", type="password")
                    register_button = st.form_submit_button("Register", use_container_width=True)
                    
                    if register_button:
                        if reg_username and reg_email and reg_password and reg_confirm:
                            if reg_password == reg_confirm:
                                st.session_state.authenticated_user = True
                                st.session_state.user_id = reg_username
                                st.success("✅ Registration successful!")
                                st.rerun()
                            else:
                                st.error("Passwords don't match")
                        else:
                            st.error("Please fill all fields")
    
    else:
        # Welcome authenticated user
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #10b981, #3b82f6); 
                    border-radius: 15px; color: white; margin: 2rem 0;">
            <h2>🎉 Welcome back, {st.session_state.get('user_id', 'User')}!</h2>
            <p style="font-size: 1.2rem;">Ready to boost your career with AI-powered insights?</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature showcase
        st.markdown("### 🌟 Choose Your Next Step")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.container():
                st.markdown("""
                <div style="text-align: center; padding: 2rem; background: #f8fafc; border-radius: 10px; height: 200px;">
                    <h3>📊 Resume Analysis</h3>
                    <p>Upload and analyze your resume with AI-powered insights</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Start Resume Analysis", key="resume_analysis", use_container_width=True):
                    st.switch_page("pages/01_Resume_Upload_and_Analysis.py")
        
        with col2:
            with st.container():
                st.markdown("""
                <div style="text-align: center; padding: 2rem; background: #f8fafc; border-radius: 10px; height: 200px;">
                    <h3>👤 Profile Management</h3>
                    <p>Build and manage your professional profile</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Manage Profile", key="manage_profile", use_container_width=True):
                    st.switch_page("pages/02_Profile.py")
        
        with col3:
            with st.container():
                st.markdown("""
                <div style="text-align: center; padding: 2rem; background: #f8fafc; border-radius: 10px; height: 200px;">
                    <h3>🎯 Job Matching</h3>
                    <p>Find jobs that match your skills and experience</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Find Jobs", key="find_jobs", use_container_width=True):
                    st.switch_page("pages/05_Job_Match_Insights.py")

def main():
    """Main application entry point"""
    # Render sidebar if authenticated
    show_sidebar()
    
    # Show home page
    show_home_page()

# Entry point
if __name__ == "__main__":
    main()