import streamlit as st

# Enhanced Sidebar Integration
import sys
from pathlib import Path
shared_path = Path(__file__).parent.parent / "shared"
if str(shared_path) not in sys.path:
    sys.path.insert(0, str(shared_path))

try:
    from enhanced_sidebar import render_enhanced_sidebar, inject_sidebar_css
    ENHANCED_SIDEBAR_AVAILABLE = True
except ImportError:
    ENHANCED_SIDEBAR_AVAILABLE = False


# Import enhanced admin integration
try:
    from enhanced_admin_integration import (
        check_enhanced_admin_availability,
        get_enhanced_admin_status,
        integrate_with_existing_sidebar
    )
    ENHANCED_ADMIN_AVAILABLE = True
except ImportError as e:
    ENHANCED_ADMIN_AVAILABLE = False
    print(f"Enhanced admin integration not available: {e}")

def show_admin_sidebar():

# Activate Enhanced Sidebar
if ENHANCED_SIDEBAR_AVAILABLE:
    inject_sidebar_css()
    render_enhanced_sidebar()

    st.sidebar.title("🛡️ IntelliCV Admin Portal")

    # --- Enhanced Admin Status Integration ---
    if ENHANCED_ADMIN_AVAILABLE:
        try:
            integrate_with_existing_sidebar()
        except Exception as e:
            st.sidebar.error(f"Enhanced Admin Status Error: {e}")
    else:
        st.sidebar.info("🚀 Enhanced Admin: Module Not Found")

    # --- Enhanced Admin Dashboard Navigation ---
    st.sidebar.subheader("🚀 Enhanced Admin Features")
    enhanced_pages = [
        ("📊 Overview Dashboard", "enhanced_admin/enhanced_admin_dashboard.py"),
        ("🔤 Prompt Registry", "enhanced_admin/config/prompt_registry.py"),
        ("🎯 Evaluation Harness", "enhanced_admin/evaluation/evaluation_harness.py"),
        ("🎭 Model Orchestrator", "enhanced_admin/orchestration/model_orchestrator.py"),
        ("📈 Response Analytics", "enhanced_admin/enhanced_admin_dashboard.py#response_analytics"),
        ("🛡️ Safety & Compliance", "enhanced_admin/enhanced_admin_dashboard.py#safety_compliance"),
        ("🔍 Observability Hub", "enhanced_admin/enhanced_admin_dashboard.py#observability_hub"),
        ("⚙️ System Settings", "enhanced_admin/enhanced_admin_dashboard.py#system_settings"),
    ]
    for page_name, page_file in enhanced_pages:
        if st.sidebar.button(page_name, key=f"enhanced_{page_name}"):
            st.session_state["current_admin_page"] = page_file
            st.switch_page(page_file)

    st.sidebar.markdown("---")

    # --- Standard Admin Portal Navigation ---
    ADMIN_GROUPS = [
        {"group": "🏠 Dashboard", "pages": [
            ("Admin Home", "pages/00_Admin_Home.py"),
            ("Admin Dashboard", "pages/admin_dashboard.py"),
            ("Consolidated Dashboard", "pages/admin_dashboard_consolidated.py"),
        ]},
        {"group": "👥 User & Access Management", "pages": [
            ("User Management", "pages/01_User_Management.py"),
            ("Admin Login", "pages/admin_login.py"),
            ("Session Manager", "pages/session_manager.py"),
        ]},
        {"group": "📂 Data & Parsers", "pages": [
            ("Data Parsers", "pages/02_Data_Parsers.py"),
            ("Batch Resume Analysis", "pages/batch_resume_analysis.py"),
            ("Admin Parsers", "pages/admin_parsers.py"),
            ("Parsing Test Harness", "pages/parsing_test_harness.py"),
            ("Resume Reparse", "pages/92_resume_reparse.py"),
        ]},
        {"group": "📊 Analytics & Insights", "pages": [
            ("Enrichment Dashboard", "pages/enrichment_dashboard.py"),
            ("Analytics Insights", "pages/61_Analytics_Insights.py"),
            ("Insights", "pages/insights.py"),
            ("Evaluation Hub", "pages/62_evaluation_hub.py"),
        ]},
        {"group": "🛠️ System & Config", "pages": [
            ("System Monitor", "pages/system_monitor.py"),
            ("System Architecture", "pages/system_architecture.py"),
            ("Settings", "pages/settings.py"),
            ("Config Manager", "pages/44_config_manager.py"),
            ("Environment Manager", "pages/environment_manager.ps1"),
        ]},
        {"group": "📖 Glossary & Docs", "pages": [
            ("Glossary Manager", "pages/53_glossary_manager.py"),
            ("Glossary Trend Tracker", "pages/55_glossary_trend_tracker.py"),
            ("Glossary Usage Dashboard", "pages/56_glossary_usage_dashboard.py"),
            ("Admin Portal Guide", "README_admin_portal.txt"),
        ]},
        {"group": "🧰 Utilities & Misc", "pages": [
            ("Screensaver Capture", "pages/05_Screensaver_Capture.py"),
            ("Test Suite", "pages/46_test_suite.py"),
        ]},
    ]

    for idx, group in enumerate(ADMIN_GROUPS):
        st.sidebar.subheader(group["group"])
        for page_name, page_file in group["pages"]:
            if st.sidebar.button(page_name, key=f"admin_{page_file}"):
                st.session_state["current_admin_page"] = page_file
                st.switch_page(page_file)

    st.sidebar.markdown("---")
    st.sidebar.caption("🔒 Admin Only | 🛡️ Secure | 🧠 Advanced")