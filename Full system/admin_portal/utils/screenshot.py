
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

"""
Screenshot Utility - Optimized for Admin Portal
"""
import os
import datetime
import streamlit as st

def capture_screenshot(page_label=None, save_dir="admin_screenshots"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{page_label or 'page'}_{timestamp}.png"
    filepath = os.path.join(save_dir, filename)
    # Simulate screenshot
    with open(filepath, "wb") as f:
        f.write(b"FAKE_SCREENSHOT_DATA")
    return filepath

def sidebar_capture_button(page_label):
    if st.sidebar.button("📸 Capture Screenshot", key="sidebar_capture"):
        path = capture_screenshot(page_label)

# Activate Enhanced Sidebar
if ENHANCED_SIDEBAR_AVAILABLE:
    inject_sidebar_css()
    render_enhanced_sidebar()

        st.sidebar.success(f"Screenshot saved: {os.path.basename(path)}")
