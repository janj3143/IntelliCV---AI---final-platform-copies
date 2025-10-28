import streamlit as st
import os

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


def show_admin_sidebar():
    """Simple admin sidebar without enhanced functions"""
    st.sidebar.title("🛡️ Admin Panel")

    admin_folder = "pages/99_admin"
    for filename in sorted(os.listdir(admin_folder)):
        if filename.endswith(".py") and not filename.startswith("__"):
            page_path = f"{admin_folder}/{filename}"
            label = filename.replace(".py", "").replace("_", " ").title()
            st.sidebar.page_link(page_path, label=f"🔧 {label}", help="Admin utility or management tool")

    st.sidebar.markdown("---")
    st.sidebar.caption("🛡️ Admin Tools © IntelliCV 2025")
