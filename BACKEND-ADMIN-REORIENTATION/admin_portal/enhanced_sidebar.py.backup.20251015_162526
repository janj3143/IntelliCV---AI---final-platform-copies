"""
IntelliCV Enhanced Sidebar Module
=================================

Provides enhanced sidebar functionality with service monitoring, development tools,
and system status integration for the IntelliCV Admin Portal.

Classes:
- IntelliCVSidebar: Main sidebar management class
- render_enhanced_sidebar: Function to render the sidebar
- inject_sidebar_css: Function to inject custom CSS
"""

import streamlit as st
import socket
import subprocess
import psutil
from datetime import datetime
from typing import Dict, Any, List, Optional
import json
import os
from pathlib import Path

class IntelliCVSidebar:
    """Enhanced sidebar with service monitoring and development tools"""
    
    def __init__(self):
        self.services = {
            "PostgreSQL": {"port": 5432, "icon": "🗄️", "description": "Database Server"},
            "Redis": {"port": 6379, "icon": "📦", "description": "Cache Server"},
            "Nginx": {"port": 80, "icon": "🌐", "description": "Web Server"},
            "Streamlit": {"port": 8501, "icon": "📊", "description": "Admin Portal"},
            "pgAdmin": {"port": 8080, "icon": "🔧", "description": "DB Management"},
            "Redis Commander": {"port": 8081, "icon": "⚡", "description": "Redis UI"}
        }
        
    def check_port_status(self, port: int) -> bool:
        """Check if a port is in use (service is running)"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system performance metrics"""
        try:
            return {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent,
                'timestamp': datetime.now()
            }
        except Exception:
            return {
                'cpu_percent': 0,
                'memory_percent': 0,
                'disk_percent': 0,
                'timestamp': datetime.now()
            }
    
    def get_service_status_summary(self) -> Dict[str, Any]:
        """Get summary of all service statuses"""
        running_services = 0
        total_services = len(self.services)
        
        for service_name, config in self.services.items():
            if self.check_port_status(config['port']):
                running_services += 1
        
        return {
            'running': running_services,
            'total': total_services,
            'status': 'healthy' if running_services >= total_services * 0.8 else 'warning' if running_services > 0 else 'critical'
        }

def inject_sidebar_css():
    """Inject custom CSS for enhanced sidebar styling"""
    st.markdown("""
    <style>
    /* Enhanced Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .sidebar-header {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .sidebar-header h1 {
        color: white;
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    .sidebar-header p {
        color: rgba(255,255,255,0.9);
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
    }
    
    .service-status {
        padding: 0.5rem;
        margin: 0.3rem 0;
        border-radius: 8px;
        background: white;
        border-left: 4px solid;
    }
    
    .service-running {
        border-left-color: #28a745;
    }
    
    .service-stopped {
        border-left-color: #dc3545;
    }
    
    .system-metric {
        background: white;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-good { border-left: 4px solid #28a745; }
    .metric-warning { border-left: 4px solid #ffc107; }
    .metric-critical { border-left: 4px solid #dc3545; }
    </style>
    """, unsafe_allow_html=True)

def render_enhanced_sidebar():
    """Render the enhanced sidebar with all features"""
    sidebar_instance = IntelliCVSidebar()
    
    # Header
    st.sidebar.markdown("""
    <div class="sidebar-header">
        <h1>🛡️ IntelliCV</h1>
        <p>Enhanced Development Portal</p>
    </div>
    """, unsafe_allow_html=True)
    
    # System Status Overview
    st.sidebar.markdown("### 🖥️ System Status")
    
    metrics = sidebar_instance.get_system_metrics()
    service_summary = sidebar_instance.get_service_status_summary()
    
    # System metrics with color coding
    cpu_class = "metric-critical" if metrics['cpu_percent'] > 80 else "metric-warning" if metrics['cpu_percent'] > 60 else "metric-good"
    memory_class = "metric-critical" if metrics['memory_percent'] > 85 else "metric-warning" if metrics['memory_percent'] > 70 else "metric-good"
    disk_class = "metric-critical" if metrics['disk_percent'] > 90 else "metric-warning" if metrics['disk_percent'] > 75 else "metric-good"
    
    st.sidebar.markdown(f"""
    <div class="system-metric {cpu_class}">
        <strong>💻 CPU:</strong> {metrics['cpu_percent']:.1f}%
    </div>
    <div class="system-metric {memory_class}">
        <strong>🧠 Memory:</strong> {metrics['memory_percent']:.1f}%
    </div>
    <div class="system-metric {disk_class}">
        <strong>💽 Disk:</strong> {metrics['disk_percent']:.1f}%
    </div>
    """, unsafe_allow_html=True)
    
    # Services Status
    st.sidebar.markdown("### 🔧 Services Status")
    
    for service_name, config in sidebar_instance.services.items():
        is_running = sidebar_instance.check_port_status(config['port'])
        status_class = "service-running" if is_running else "service-stopped"
        status_icon = "🟢" if is_running else "🔴"
        
        st.sidebar.markdown(f"""
        <div class="service-status {status_class}">
            <strong>{config['icon']} {service_name}</strong><br>
            <small>{status_icon} Port {config['port']} - {config['description']}</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Overall service health
    health_color = "#28a745" if service_summary['status'] == 'healthy' else "#ffc107" if service_summary['status'] == 'warning' else "#dc3545"
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 0.8rem; background: {health_color}; color: white; border-radius: 8px; margin: 1rem 0;">
        <strong>Services: {service_summary['running']}/{service_summary['total']} Running</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # Development Tools
    st.sidebar.markdown("### 🚀 Development Tools")
    
    if st.sidebar.button("🔧 Open pgAdmin", key="pgAdmin"):
        st.sidebar.success("pgAdmin: http://localhost:8080")
    
    if st.sidebar.button("⚡ Redis Commander", key="redis_commander"):
        st.sidebar.success("Redis UI: http://localhost:8081")
    
    if st.sidebar.button("📊 System Monitor", key="system_monitor"):
        st.sidebar.info("System metrics updated above ⬆️")
    
    # Quick Actions
    st.sidebar.markdown("### ⚡ Quick Actions")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("🔄 Refresh", key="refresh_sidebar"):
            st.rerun()
    
    with col2:
        if st.button("📈 Analytics", key="goto_analytics"):
            try:
                st.switch_page("pages/02_Analytics.py")
            except:
                st.sidebar.info("Analytics page available in main navigation")
    
    # Footer info
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <small>
    <strong>Last Updated:</strong> {datetime.now().strftime('%H:%M:%S')}<br>
    <strong>Status:</strong> Enhanced Sidebar Active
    </small>
    """, unsafe_allow_html=True)

# Convenience functions for backward compatibility
def render_enhanced_sidebar_legacy():
    """Legacy function name for backward compatibility"""
    return render_enhanced_sidebar()

def inject_enhanced_css():
    """Alternative function name for CSS injection"""
    return inject_sidebar_css()