"""
IntelliCV Enhanced Sidebar Demo

This page demonstrates the enhanced sidebar with development tools integration.
"""

import streamlit as st
import sys
from pathlib import Path

# Add shared modules to path
shared_path = Path(__file__).parent.parent / "shared"
if str(shared_path) not in sys.path:
    sys.path.insert(0, str(shared_path))

try:
    from enhanced_sidebar import render_enhanced_sidebar, inject_sidebar_css
    ENHANCED_SIDEBAR_AVAILABLE = True
except ImportError:
    ENHANCED_SIDEBAR_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="IntelliCV Enhanced Sidebar Demo",
    page_icon="🎯",
    layout="wide"
)

# Activate Enhanced Sidebar
if ENHANCED_SIDEBAR_AVAILABLE:
    inject_sidebar_css()
    render_enhanced_sidebar()
else:
    st.sidebar.error("Enhanced sidebar not available")

# Main content
st.title("🎯 Enhanced Sidebar Demo")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.header("🛠️ Features")
    st.markdown("""
    The enhanced sidebar provides:
    
    - **Service Status Monitoring** 🔍
      - Real-time port checking
      - Docker container status
      - Health indicators
    
    - **Development Tools Access** 🚀
      - One-click Postman launch
      - pgAdmin database management
      - Redis Commander interface
      - VS Code integration
    
    - **Docker Controls** 🐳
      - Start/stop services
      - Container management
      - Log viewing
    
    - **System Monitoring** 📊
      - CPU and memory usage
      - Disk space monitoring
      - Environment status
    """)

with col2:
    st.header("🎨 Service Status")
    
    if ENHANCED_SIDEBAR_AVAILABLE:
        from enhanced_sidebar import IntelliCVSidebar
        sidebar = IntelliCVSidebar()
        
        # Display service status in main content
        for service_name, config in sidebar.services.items():
            is_running = sidebar.check_port_status(config['port'])
            status = "🟢 Running" if is_running else "🔴 Stopped"
            st.metric(
                label=f"{config['icon']} {service_name}",
                value=f"Port {config['port']}",
                delta=status
            )
    else:
        st.error("Enhanced sidebar components not available")

st.markdown("---")

# Integration guide
st.header("📖 Integration Guide")

st.code("""
# To integrate into your Streamlit app:

1. Import the enhanced sidebar:
from shared.enhanced_sidebar import render_enhanced_sidebar, inject_sidebar_css

2. Add to your app:
if ENHANCED_SIDEBAR_AVAILABLE:
    inject_sidebar_css()
    render_enhanced_sidebar()

3. Or use the integration script:
python shared/streamlit_integration.py
""", language="python")

# Footer
st.markdown("---")
st.caption("IntelliCV Enhanced Development Environment 🚀")
