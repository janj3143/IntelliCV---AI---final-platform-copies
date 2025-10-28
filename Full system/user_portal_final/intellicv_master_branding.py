"""
🎨 IntelliCV-AI Master Branding System
=====================================
Consistent 30% logo branding and styling for all portal pages
Ready for systematic deployment across 50+ pages
"""

import streamlit as st
from pathlib import Path

def apply_intellicv_branding(page_type="standard", custom_opacity=0.08, logo_size="medium"):
    """
    Apply consistent IntelliCV-AI branding to any page
    
    Parameters:
    - page_type: "standard", "admin", "premium", "landing"
    - custom_opacity: 0.05-0.15 (default 0.08 for 30% background effect)
    - logo_size: "small", "medium", "large"
    """
    
    # Logo size configurations
    logo_sizes = {
        "small": {"font_size": "16", "width": "50%", "height": "50%", "top": "25%", "left": "25%"},
        "medium": {"font_size": "20", "width": "60%", "height": "60%", "top": "20%", "left": "20%"},
        "large": {"font_size": "24", "width": "70%", "height": "70%", "top": "15%", "left": "15%"}
    }
    
    # Color schemes by page type
    color_schemes = {
        "standard": "#667eea",      # Primary blue
        "admin": "#764ba2",         # Purple accent
        "premium": "#28a745",       # Success green
        "landing": "#ffc107"        # Warning yellow/gold
    }
    
    size_config = logo_sizes.get(logo_size, logo_sizes["medium"])
    brand_color = color_schemes.get(page_type, color_schemes["standard"])
    
    # Generate CSS with branding
    branding_css = f'''
    <style>
    /* IntelliCV-AI Master Branding System */
    
    /* Clean background with logo watermark */
    .stApp {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
        position: relative;
    }}
    
    /* 30% Logo Background Watermark */
    .stApp::before {{
        content: '';
        position: fixed;
        top: {size_config["top"]};
        left: {size_config["left"]};
        width: {size_config["width"]};
        height: {size_config["height"]};
        background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><text x="50%" y="50%" font-family="Arial, sans-serif" font-size="{size_config["font_size"]}" font-weight="bold" text-anchor="middle" dy=".3em" fill="{brand_color}" opacity="{custom_opacity}">IntelliCV-AI</text></svg>');
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
        pointer-events: none;
        z-index: -1;
    }}
    
    /* Main Container Enhancement */
    .main .block-container {{
        background: rgba(255,255,255,0.97) !important;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        margin-top: 1rem;
        backdrop-filter: blur(10px);
        max-width: 1400px;
        margin-left: auto;
        margin-right: auto;
        position: relative;
        z-index: 1;
    }}
    
    /* Header Styling */
    .intellicv-header {{
        background: linear-gradient(135deg, {brand_color} 0%, rgba(118, 75, 162, 0.9) 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        position: relative;
        z-index: 2;
    }}
    
    .intellicv-header h1 {{
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    
    .intellicv-header p {{
        font-size: 1.1rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }}
    
    /* Section Cards */
    .intellicv-section {{
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        margin-bottom: 2rem;
        position: relative;
        z-index: 2;
    }}
    
    /* Premium Feature Highlighting */
    .intellicv-premium {{
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(40,167,69,0.3);
        position: relative;
        z-index: 2;
    }}
    
    /* Token Status Display */
    .intellicv-token-status {{
        background: linear-gradient(45deg, #ffc107, #fd7e14);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
        position: relative;
        z-index: 2;
    }}
    
    /* Sidebar Enhancement */
    .css-1d391kg {{
        background: rgba(255,255,255,0.95) !important;
        backdrop-filter: blur(5px);
    }}
    
    /* Button Styling */
    .stButton > button {{
        background: linear-gradient(45deg, {brand_color}, rgba(118, 75, 162, 0.9));
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        position: relative;
        z-index: 2;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }}
    
    /* Progress Elements */
    .intellicv-progress {{
        background: #f0f0f0;
        border-radius: 10px;
        height: 20px;
        margin: 1rem 0;
        overflow: hidden;
        position: relative;
        z-index: 2;
    }}
    
    .intellicv-progress-bar {{
        height: 100%;
        background: linear-gradient(90deg, {brand_color}, #20c997);
        border-radius: 10px;
        transition: width 0.3s ease;
    }}
    
    /* Metric Cards */
    .intellicv-metric {{
        text-align: center;
        padding: 1rem;
        margin: 0.5rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid {brand_color};
        position: relative;
        z-index: 2;
    }}
    
    .intellicv-metric-value {{
        font-size: 1.8rem;
        font-weight: bold;
        color: {brand_color};
    }}
    
    .intellicv-metric-label {{
        font-size: 0.9rem;
        color: #666;
    }}
    
    /* Alert Styling */
    .intellicv-alert {{
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid {brand_color};
        background: rgba(102, 126, 234, 0.1);
        position: relative;
        z-index: 2;
    }}
    
    /* Footer Enhancement */
    .intellicv-footer {{
        text-align: center;
        padding: 1rem;
        margin-top: 2rem;
        border-top: 2px solid #e0e0e0;
        color: #666;
        font-size: 0.9rem;
        position: relative;
        z-index: 2;
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding: 1rem;
        }}
        
        .intellicv-header h1 {{
            font-size: 1.8rem;
        }}
        
        .stApp::before {{
            top: 30%;
            left: 30%;
            width: 40%;
            height: 40%;
        }}
    }}
    
    /* Animation for page load */
    .main {{
        animation: intellicvFadeIn 0.8s ease-in-out;
    }}
    
    @keyframes intellicvFadeIn {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    </style>
    '''
    
    st.markdown(branding_css, unsafe_allow_html=True)

def create_intellicv_header(title, subtitle="", page_type="standard", show_tokens=True, token_count=None):
    """
    Create standardized header for any IntelliCV-AI page
    
    Parameters:
    - title: Page title
    - subtitle: Optional subtitle/description
    - page_type: "standard", "admin", "premium", "landing"
    - show_tokens: Whether to display token information
    - token_count: Specific token cost to display
    """
    
    # Token display logic
    token_display = ""
    if show_tokens and token_count:
        token_display = f"<p><small>🪙 Token Cost: {token_count} tokens</small></p>"
    elif show_tokens:
        token_display = f"<p><small>💎 Premium Feature</small></p>"
    
    header_html = f'''
    <div class="intellicv-header">
        <h1>{title}</h1>
        {f"<p>{subtitle}</p>" if subtitle else ""}
        {token_display}
    </div>
    '''
    
    st.markdown(header_html, unsafe_allow_html=True)

def create_intellicv_section(title, content="", icon="📋"):
    """
    Create standardized section container
    
    Parameters:
    - title: Section title
    - content: Optional pre-content
    - icon: Section icon
    """
    
    section_start = f'''
    <div class="intellicv-section">
        <h3>{icon} {title}</h3>
        {f"<p>{content}</p>" if content else ""}
    '''
    
    st.markdown(section_start, unsafe_allow_html=True)

def close_intellicv_section():
    """Close section container"""
    st.markdown('</div>', unsafe_allow_html=True)

def create_intellicv_metric(label, value, icon="📊"):
    """
    Create metric display card
    
    Parameters:
    - label: Metric description
    - value: Metric value
    - icon: Display icon
    """
    
    metric_html = f'''
    <div class="intellicv-metric">
        <div class="intellicv-metric-value">{icon} {value}</div>
        <div class="intellicv-metric-label">{label}</div>
    </div>
    '''
    
    st.markdown(metric_html, unsafe_allow_html=True)

def create_intellicv_progress(percentage, label="Progress"):
    """
    Create progress bar with branding
    
    Parameters:
    - percentage: Progress percentage (0-100)
    - label: Progress label
    """
    
    progress_html = f'''
    <div style="margin: 1rem 0;">
        <p><strong>{label}: {percentage:.0f}%</strong></p>
        <div class="intellicv-progress">
            <div class="intellicv-progress-bar" style="width: {percentage}%"></div>
        </div>
    </div>
    '''
    
    st.markdown(progress_html, unsafe_allow_html=True)

def create_intellicv_alert(message, alert_type="info"):
    """
    Create branded alert message
    
    Parameters:
    - message: Alert message
    - alert_type: "info", "success", "warning", "error"
    """
    
    alert_icons = {
        "info": "ℹ️",
        "success": "✅", 
        "warning": "⚠️",
        "error": "❌"
    }
    
    icon = alert_icons.get(alert_type, "ℹ️")
    
    alert_html = f'''
    <div class="intellicv-alert">
        <strong>{icon} {message}</strong>
    </div>
    '''
    
    st.markdown(alert_html, unsafe_allow_html=True)

def create_intellicv_footer(page_name="", token_usage=None, additional_info=""):
    """
    Create standardized footer
    
    Parameters:
    - page_name: Current page name
    - token_usage: Token count if applicable
    - additional_info: Extra footer information
    """
    
    from datetime import datetime
    
    footer_parts = []
    
    if page_name:
        footer_parts.append(f"**Page:** {page_name}")
    
    if token_usage:
        footer_parts.append(f"**Tokens Used:** {token_usage}")
    
    if additional_info:
        footer_parts.append(additional_info)
    
    footer_parts.append(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    footer_content = " | ".join(footer_parts)
    
    footer_html = f'''
    <div class="intellicv-footer">
        {footer_content}
        <br>
        <small>Powered by IntelliCV-AI • Professional Resume & Career Intelligence</small>
    </div>
    '''
    
    st.markdown(footer_html, unsafe_allow_html=True)

# Example usage functions for different page types
def apply_standard_branding():
    """Apply standard page branding"""
    apply_intellicv_branding("standard", 0.08, "medium")

def apply_admin_branding():
    """Apply admin page branding"""
    apply_intellicv_branding("admin", 0.06, "large")

def apply_premium_branding():
    """Apply premium feature branding"""
    apply_intellicv_branding("premium", 0.10, "medium")

def apply_landing_branding():
    """Apply landing page branding"""
    apply_intellicv_branding("landing", 0.12, "large")

# Quick deployment function for existing pages
def quick_brand_existing_page(page_type="standard", title="", subtitle="", token_cost=None):
    """
    One-line function to brand any existing page
    
    Usage: Add this single line to any existing page:
    quick_brand_existing_page("standard", "Page Title", "Page Description", 3)
    """
    apply_intellicv_branding(page_type)
    if title:
        create_intellicv_header(title, subtitle, page_type, token_cost is not None, token_cost)

# Master deployment checklist
PAGES_TO_BRAND = [
    # Core User Journey (High Priority)
    {"file": "00_Home.py", "type": "landing", "title": "IntelliCV-AI Home", "tokens": None},
    {"file": "01_Dashboard.py", "type": "standard", "title": "Dashboard", "tokens": 1},
    {"file": "02_Payment.py", "type": "premium", "title": "Payment & Subscriptions", "tokens": None},
    {"file": "03_Profile_Setup.py", "type": "standard", "title": "Profile Setup", "tokens": 1},
    {"file": "03_Profile_Setup_Enhanced_AI_Chatbot.py", "type": "premium", "title": "Enhanced Profile Setup", "tokens": 3},
    {"file": "04_Resume_Upload.py", "type": "standard", "title": "Resume Upload", "tokens": 2},
    {"file": "05_Resume_Upload.py", "type": "standard", "title": "Resume Upload", "tokens": 2},
    {"file": "05_Resume_Upload_Enhanced_AI.py", "type": "premium", "title": "Enhanced Resume Upload", "tokens": 4},
    {"file": "05_Resume_Upload_Instant_Analysis.py", "type": "premium", "title": "Instant Resume Analysis", "tokens": 5},
    {"file": "06_Job_Match.py", "type": "standard", "title": "Job Matching", "tokens": 3},
    {"file": "07_AI_Interview_Coach_INTEGRATED.py", "type": "premium", "title": "AI Interview Coach", "tokens": 5},
    
    # Feature Pages (Medium Priority)
    {"file": "AI_Career_Intelligence.py", "type": "premium", "title": "AI Career Intelligence", "tokens": 8},
    {"file": "Professional_Network_Builder.py", "type": "standard", "title": "Network Builder", "tokens": 2},
    {"file": "Portfolio_Showcase.py", "type": "standard", "title": "Portfolio Showcase", "tokens": 1},
    
    # Admin Pages (Admin Priority)
    # Note: Admin pages should use apply_admin_branding()
]

if __name__ == "__main__":
    # Demo of the branding system
    st.set_page_config(
        page_title="🎨 IntelliCV-AI Branding Demo",
        page_icon="🎨",
        layout="wide"
    )
    
    # Apply demo branding
    apply_intellicv_branding("premium", 0.10, "large")
    
    # Demo header
    create_intellicv_header(
        "🎨 IntelliCV-AI Master Branding System",
        "Consistent 30% logo branding for all portal pages",
        "premium",
        True,
        "Demo"
    )
    
    # Demo sections
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_intellicv_section("📊 Metrics Demo", "Sample metrics display")
        create_intellicv_metric("Users Active", "1,247", "👥")
        create_intellicv_metric("Success Rate", "94%", "🎯")
        close_intellicv_section()
    
    with col2:
        create_intellicv_section("🚀 Progress Demo", "Sample progress display")
        create_intellicv_progress(75, "Feature Completion")
        create_intellicv_progress(92, "User Satisfaction")
        close_intellicv_section()
    
    with col3:
        create_intellicv_section("💬 Alert Demo", "Sample alert display")
        create_intellicv_alert("System updated successfully!", "success")
        create_intellicv_alert("New features available", "info")
        close_intellicv_section()
    
    # Demo footer
    create_intellicv_footer("Branding Demo", "0", "All systems operational")