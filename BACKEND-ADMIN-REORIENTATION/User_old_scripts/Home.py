"""
🏠 IntelliCV-AI Entry Point Redirect
===================================
Redirects to the consolidated main.py application entry point
"""

import streamlit as st
from pathlib import Path
import sys
import subprocess
import os

# Setup page config for redirect
st.set_page_config(
    page_title="IntelliCV-AI | Redirecting...",
    page_icon="🚀",
    layout="wide"
)

# Show redirect message
st.markdown("""
# 🚀 IntelliCV-AI
## Redirecting to Main Application...

Please wait while we redirect you to the main IntelliCV-AI platform.
""")

# Add redirect information
with st.spinner("Loading IntelliCV-AI..."):
    st.info("🔄 Redirecting to main application entry point...")
    
    # Check if main.py exists
    main_py_path = Path(__file__).parent / "main.py"
    
    if main_py_path.exists():
        st.success("✅ Main application found - launching main.py")
        # Redirect by running main.py content directly
        try:
            # Import and execute main.py
            sys.path.insert(0, str(Path(__file__).parent))
            import main
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error loading main application: {e}")
            st.markdown("**Fallback:** [Access Home Page](pages/00_Home.py)")
    else:
        st.warning("⚠️ Main application not found - using fallback")
        st.switch_page("pages/00_Welcome_Page.py")