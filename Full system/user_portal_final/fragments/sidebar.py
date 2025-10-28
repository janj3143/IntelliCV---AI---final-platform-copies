
import streamlit as st
import os

def show_sidebar():
    if not st.session_state.get("authenticated_user"):
        return

    st.sidebar.title("📂 IntelliCV")

    def section(label): st.sidebar.markdown(f"### {label}")
    def divider(): st.sidebar.markdown("---")

    # Core Workflow - PHASE 1 READY
    section("🚀 Core Tools")
    st.sidebar.page_link("pages/01_Resume_Upload_and_Analysis.py", label="📊 Resume Analysis Hub")
    st.sidebar.page_link("pages/02_Profile.py", label="👤 Profile")  # PHASE 1: Enhanced Profile System
    # Coming in Phase 1: ⭐ STAR Story Builder, 🛠️ Resume Tuner
    st.sidebar.page_link("pages/03_Job_Description.py", label="� Job Description")  # PHASE 1: Enhanced Job Analysis
    st.sidebar.page_link("pages/04_Resume_Feedback.py", label="� Resume Feedback")  # PHASE 2: Smart Feedback
    st.sidebar.page_link("pages/05_Job_Match_Insights.py", label="🎯 Job Match Insights")  # PHASE 2: Enhanced Matching
    st.sidebar.page_link("pages/06_Resume_History.py", label="📄 Resume History")

    divider()

    # Career Development & Coaching - Only Existing Pages
    section("🎯 Career Development")
    st.sidebar.page_link("pages/Interview_Coach.py", label="🎤 Interview Coach")
    st.sidebar.page_link("pages/Job_Title_Intelligence.py", label="🧠 Job Title Intelligence")
    st.sidebar.page_link("pages/09_Job_Tracker.py", label="� Job Tracker")
    st.sidebar.page_link("pages/AI_Career_Intelligence.py", label="🤖 AI Career Intelligence")
    st.sidebar.page_link("pages/Geographic_Career_Intelligence.py", label="🌍 Geographic Intelligence")

    divider()
    
    # Phase Development Status
    section("📋 Development Status")
    st.sidebar.info("📈 **Phase 1 Ready**: Enhanced Profile & STAR Stories")
    st.sidebar.info("🔄 See MASTER_IMPLEMENTATION_ROADMAP.md for details")
    
    divider()
    
    # User Preferences
    section("⚙️ Settings")
    if st.sidebar.button("🔄 Refresh Session"):
        st.rerun()
    
    divider()
    st.sidebar.caption("© 2025 IntelliCV | User Portal")

    # Admin & Debug Tools
    if st.session_state.get("is_admin", False):
        section("🔐 Admin Tools")
        st.sidebar.page_link("pages/Admin_Glossary_Explorer.py", label="📚 Glossary Explorer")
        st.sidebar.page_link("pages/Admin_Log_Viewer.py", label="📝 Admin Logs")
        st.sidebar.page_link("pages/Admin_Resume_Inspector.py", label="🔍 Resume Inspector")

        section("🧪 Debug & Sandbox")
        st.sidebar.page_link("pages/100_debug_resume_path.py", label="🧭 Resume Path Debug")
        st.sidebar.page_link("pages/17_dashboardV4_consolidated.py", label="📊 Unified Dashboard")
        st.sidebar.page_link("pages/49_Tabbed_Dashboard.py", label="🧷 Tabbed Dashboard")

    divider()
    st.sidebar.caption("© 2025 IntelliCV")
