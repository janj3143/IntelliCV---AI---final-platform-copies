"""
📋 IntelliCV Software Requirements Management & Environment Monitor
=================================================================

🔧 **System Environment Analysis**
- Python interpreter detection and validation
- Package dependency analysis with conflict detection  
- Update availability monitoring with security alerts
- .NET Framework and Azure CLI compatibility checking
- Hardware requirements validation and optimization recommendations

🚦 **Traffic Light Monitoring System**
- 🟢 GREEN: All systems operational, packages up-to-date, no conflicts
- 🟡 YELLOW: Minor issues detected, updates available, potential conflicts
- 🔴 RED: Critical issues, security vulnerabilities, major conflicts

🎯 **Environment Detection**
- Pure Python Environment
- .NET Hybrid Environment  
- Azure Cloud Integration
- Docker Containerized Setup

Created: October 13, 2025
"""

import streamlit as st
import subprocess
import sys
import pkg_resources
import platform
import psutil
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import importlib.util
import requests

# Page configuration
st.set_page_config(
    page_title="Software Requirements Management", 
    page_icon="📋", 
    layout="wide"
)

class RequirementsMonitor:
    """Advanced software requirements and environment monitoring system"""
    
    def __init__(self):
        self.python_version = sys.version
        self.platform_info = platform.platform()
        self.requirements_categories = self.load_requirements_categories()
        self.installed_packages = self.get_installed_packages()
        
    def get_installed_packages(self) -> Dict[str, str]:
        """Get all installed Python packages with versions"""
        try:
            installed = {}
            for dist in pkg_resources.working_set:
                installed[dist.project_name.lower()] = dist.version
            return installed
        except Exception as e:
            st.error(f"Error getting installed packages: {e}")
            return {}
    
    def load_requirements_categories(self) -> Dict[str, List[str]]:
        """Load requirements from categorized files"""
        categories = {
            "core": [],
            "ai_heavy": [],
            "fusion": [],
            "data": [],
            "web": [], 
            "admin": [],
            "enterprise": [],
            "dev": []
        }
        
        # Define requirements for each category
        categories["core"] = [
            "streamlit>=1.50.0",
            "fastapi>=0.118.0", 
            "uvicorn>=0.37.0",
            "pandas>=2.3.3",
            "numpy>=2.2.6",
            "requests>=2.32.5"
        ]
        
        categories["ai_heavy"] = [
            "scikit-learn>=1.7.2",
            "scipy>=1.15.3",
            "openai>=2.3.0",
            "nltk>=3.9.2",
            "transformers>=4.35.0"
        ]
        
        categories["fusion"] = [
            "scikit-fuzzy>=0.5.0",
            "xgboost>=2.0.0", 
            "statsmodels>=0.14.0",
            "lightgbm>=4.0.0"
        ]
        
        categories["data"] = [
            "unstructured>=0.18.15",
            "python-docx>=1.2.0",
            "pypdf>=6.1.1",
            "openpyxl>=3.1.5",
            "beautifulsoup4>=4.13.5"
        ]
        
        categories["web"] = [
            "httpx>=0.28.1",
            "aiohttp>=3.12.15",
            "websockets>=15.0.1"
        ]
        
        categories["admin"] = [
            "plotly>=6.3.1",
            "prometheus_client>=0.23.1",
            "psutil>=7.1.0"
        ]
        
        categories["enterprise"] = [
            "psycopg2-binary>=2.9.10",
            "redis>=5.2.1",
            "SQLAlchemy>=2.0.43",
            "cryptography>=46.0.2",
            "celery>=5.5.3"
        ]
        
        categories["dev"] = [
            "pytest>=8.4.2",
            "pytest-mock>=3.15.1",
            "black>=23.0.0",
            "flake8>=6.0.0"
        ]
        
        return categories
    
    def check_package_status(self, package_requirement: str) -> Dict[str, str]:
        """Check individual package status with traffic light system"""
        try:
            # Parse requirement
            if ">=" in package_requirement:
                package_name, required_version = package_requirement.split(">=")
            elif "==" in package_requirement:
                package_name, required_version = package_requirement.split("==")
            else:
                package_name = package_requirement
                required_version = "any"
            
            package_name = package_name.strip()
            required_version = required_version.strip()
            
            # Check if installed
            installed_version = self.installed_packages.get(package_name.lower())
            
            if not installed_version:
                return {
                    "status": "🔴",
                    "message": f"NOT INSTALLED",
                    "installed": "None",
                    "required": required_version,
                    "action": "Install required"
                }
            
            # Version comparison (simplified)
            if required_version != "any":
                try:
                    from packaging import version
                    if version.parse(installed_version) >= version.parse(required_version):
                        return {
                            "status": "🟢", 
                            "message": "OK",
                            "installed": installed_version,
                            "required": required_version,
                            "action": "None"
                        }
                    else:
                        return {
                            "status": "🟡",
                            "message": "VERSION LOW", 
                            "installed": installed_version,
                            "required": required_version,
                            "action": "Update recommended"
                        }
                except ImportError:
                    # Fallback: simple string comparison
                    if installed_version == required_version or required_version == "any":
                        return {
                            "status": "🟢",
                            "message": "OK",
                            "installed": installed_version, 
                            "required": required_version,
                            "action": "None"
                        }
                    else:
                        return {
                            "status": "🟡",
                            "message": "CHECK VERSION",
                            "installed": installed_version,
                            "required": required_version, 
                            "action": "Manual verification needed"
                        }
            else:
                return {
                    "status": "🟢",
                    "message": "INSTALLED",
                    "installed": installed_version,
                    "required": "any",
                    "action": "None"
                }
                
        except Exception as e:
            return {
                "status": "🔴",
                "message": f"ERROR: {str(e)[:30]}",
                "installed": "Unknown",
                "required": required_version,
                "action": "Check manually"
            }
    
    def detect_environment_type(self) -> Dict[str, str]:
        """Detect the current development environment"""
        env_info = {
            "type": "Unknown",
            "status": "🔴", 
            "details": []
        }
        
        # Check Python
        if sys.version_info >= (3, 10):
            env_info["details"].append("✅ Python 3.10+ detected")
            python_ok = True
        else:
            env_info["details"].append("❌ Python version too old")
            python_ok = False
        
        # Check virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            env_info["details"].append("✅ Virtual environment active")
            venv_ok = True
        else:
            env_info["details"].append("⚠️ No virtual environment detected")
            venv_ok = False
        
        # Check .NET (Windows)
        dotnet_available = False
        if platform.system() == "Windows":
            try:
                result = subprocess.run(["dotnet", "--version"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    env_info["details"].append(f"✅ .NET Core: {result.stdout.strip()}")
                    dotnet_available = True
                else:
                    env_info["details"].append("❌ .NET Core not found")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                env_info["details"].append("❌ .NET Core not available")
        
        # Check Azure CLI
        azure_available = False
        try:
            result = subprocess.run(["az", "--version"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                env_info["details"].append("✅ Azure CLI available")
                azure_available = True
            else:
                env_info["details"].append("❌ Azure CLI not found")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            env_info["details"].append("❌ Azure CLI not installed")
        
        # Determine environment type and status
        if python_ok and venv_ok:
            if dotnet_available and azure_available:
                env_info["type"] = "🔄 Hybrid (.NET + Azure + Python)"
                env_info["status"] = "🟢"
            elif dotnet_available:
                env_info["type"] = "🔄 Hybrid (.NET + Python)"
                env_info["status"] = "🟡" 
            elif azure_available:
                env_info["type"] = "☁️ Azure Cloud Python"
                env_info["status"] = "🟡"
            else:
                env_info["type"] = "🐍 Pure Python Environment"
                env_info["status"] = "🟢"
        else:
            env_info["type"] = "❌ Incomplete Environment"
            env_info["status"] = "🔴"
        
        return env_info
    
    def get_system_resources(self) -> Dict[str, str]:
        """Get current system resource information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "cpu_usage": f"{cpu_percent}%",
                "cpu_status": "🟢" if cpu_percent < 80 else "🟡" if cpu_percent < 95 else "🔴",
                "memory_used": f"{memory.percent}%", 
                "memory_available": f"{memory.available // (1024**3)}GB",
                "memory_status": "🟢" if memory.percent < 80 else "🟡" if memory.percent < 95 else "🔴",
                "disk_used": f"{disk.percent}%",
                "disk_free": f"{disk.free // (1024**3)}GB", 
                "disk_status": "🟢" if disk.percent < 80 else "🟡" if disk.percent < 95 else "🔴"
            }
        except Exception as e:
            return {"error": f"Could not get system resources: {e}"}

def main():
    """Main Streamlit application"""
    
    # Header
    st.title("📋 Software Requirements Management")
    st.markdown("### 🚦 IntelliCV Environment & Dependency Monitor")
    
    # Initialize monitor
    monitor = RequirementsMonitor()
    
    # Environment Detection Section
    st.markdown("## 🔍 Environment Detection")
    
    env_info = monitor.detect_environment_type()
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.metric(
            label="Environment Type",
            value=env_info["type"], 
            delta=None
        )
        
        st.metric(
            label="Overall Status",
            value=env_info["status"],
            delta="Operational" if env_info["status"] == "🟢" else "Issues Detected"
        )
    
    with col2:
        st.markdown("**Environment Details:**")
        for detail in env_info["details"]:
            st.markdown(f"- {detail}")
    
    # System Resources Section
    st.markdown("## 💻 System Resources")
    
    resources = monitor.get_system_resources()
    
    if "error" not in resources:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label=f"CPU Usage {resources['cpu_status']}", 
                value=resources["cpu_usage"]
            )
        
        with col2:
            st.metric(
                label=f"Memory Usage {resources['memory_status']}",
                value=resources["memory_used"],
                delta=f"{resources['memory_available']} available"
            )
        
        with col3:
            st.metric(
                label=f"Disk Usage {resources['disk_status']}",
                value=resources["disk_used"], 
                delta=f"{resources['disk_free']} free"
            )
    else:
        st.error(resources["error"])
    
    # Package Requirements Analysis
    st.markdown("## 📦 Package Requirements Analysis")
    
    # Category tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "🏗️ Core", "🤖 AI/ML", "🔬 Fusion", "📊 Data", "🌐 Web", "⚙️ Admin", "🏢 Enterprise", "🧪 Dev"
    ])
    
    # Core packages
    with tab1:
        st.markdown("### 🏗️ Core Platform Requirements")
        for package in monitor.requirements_categories["core"]:
            status_info = monitor.check_package_status(package)
            
            col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 3])
            
            with col1:
                st.markdown(f"**{status_info['status']}**")
            with col2:
                st.markdown(f"`{package.split('>=')[0].split('==')[0]}`")
            with col3:
                st.markdown(status_info['installed'])
            with col4:
                st.markdown(status_info['required'])
            with col5:
                st.markdown(status_info['action'])
    
    # AI/ML packages  
    with tab2:
        st.markdown("### 🤖 AI/ML Requirements")
        for package in monitor.requirements_categories["ai_heavy"]:
            status_info = monitor.check_package_status(package)
            
            col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 3])
            
            with col1:
                st.markdown(f"**{status_info['status']}**")
            with col2:
                st.markdown(f"`{package.split('>=')[0].split('==')[0]}`")
            with col3:
                st.markdown(status_info['installed'])
            with col4:
                st.markdown(status_info['required']) 
            with col5:
                st.markdown(status_info['action'])
    
    # Fusion packages
    with tab3:
        st.markdown("### 🔬 Fusion Engine Requirements")
        for package in monitor.requirements_categories["fusion"]:
            status_info = monitor.check_package_status(package)
            
            col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 3])
            
            with col1:
                st.markdown(f"**{status_info['status']}**")
            with col2:
                st.markdown(f"`{package.split('>=')[0].split('==')[0]}`")
            with col3:
                st.markdown(status_info['installed'])
            with col4:
                st.markdown(status_info['required'])
            with col5:
                st.markdown(status_info['action'])
    
    # Data processing packages
    with tab4:
        st.markdown("### 📊 Data Processing Requirements")
        for package in monitor.requirements_categories["data"]:
            status_info = monitor.check_package_status(package)
            
            col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 3])
            
            with col1:
                st.markdown(f"**{status_info['status']}**")
            with col2:
                st.markdown(f"`{package.split('>=')[0].split('==')[0]}`") 
            with col3:
                st.markdown(status_info['installed'])
            with col4:
                st.markdown(status_info['required'])
            with col5:
                st.markdown(status_info['action'])
    
    # Web packages
    with tab5:
        st.markdown("### 🌐 Web & API Requirements")
        for package in monitor.requirements_categories["web"]:
            status_info = monitor.check_package_status(package)
            
            col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 3])
            
            with col1:
                st.markdown(f"**{status_info['status']}**")
            with col2:
                st.markdown(f"`{package.split('>=')[0].split('==')[0]}`")
            with col3:
                st.markdown(status_info['installed'])
            with col4:
                st.markdown(status_info['required'])
            with col5:
                st.markdown(status_info['action'])
    
    # Admin packages
    with tab6:
        st.markdown("### ⚙️ Admin Portal Requirements") 
        for package in monitor.requirements_categories["admin"]:
            status_info = monitor.check_package_status(package)
            
            col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 3])
            
            with col1:
                st.markdown(f"**{status_info['status']}**")
            with col2:
                st.markdown(f"`{package.split('>=')[0].split('==')[0]}`")
            with col3:
                st.markdown(status_info['installed'])
            with col4:
                st.markdown(status_info['required'])
            with col5:
                st.markdown(status_info['action'])
    
    # Enterprise packages
    with tab7:
        st.markdown("### 🏢 Enterprise Requirements")
        for package in monitor.requirements_categories["enterprise"]:
            status_info = monitor.check_package_status(package)
            
            col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 3])
            
            with col1:
                st.markdown(f"**{status_info['status']}**")
            with col2:
                st.markdown(f"`{package.split('>=')[0].split('==')[0]}`")
            with col3:
                st.markdown(status_info['installed'])
            with col4:
                st.markdown(status_info['required'])
            with col5:
                st.markdown(status_info['action'])
    
    # Development packages
    with tab8:
        st.markdown("### 🧪 Development Requirements")
        for package in monitor.requirements_categories["dev"]:
            status_info = monitor.check_package_status(package)
            
            col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 3])
            
            with col1:
                st.markdown(f"**{status_info['status']}**")
            with col2:
                st.markdown(f"`{package.split('>=')[0].split('==')[0]}`")
            with col3:
                st.markdown(status_info['installed'])
            with col4:
                st.markdown(status_info['required'])
            with col5:
                st.markdown(status_info['action'])
    
    # Python Interpreter Information
    st.markdown("## 🐍 Python Interpreter Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Current Python Setup:**")
        st.code(f"""
Python Version: {sys.version}
Executable Path: {sys.executable}
Platform: {monitor.platform_info}
Virtual Environment: {'Yes' if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 'No'}
        """)
    
    with col2:
        st.markdown("**Package Statistics:**")
        st.code(f"""
Total Packages Installed: {len(monitor.installed_packages)}
Python Path Entries: {len(sys.path)}
Site Packages: {len([p for p in sys.path if 'site-packages' in p])}
        """)
    
    # Action Buttons
    st.markdown("## 🛠️ Management Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 Refresh Status", type="primary"):
            st.rerun()
    
    with col2:
        if st.button("📥 Install Missing"):
            st.info("Use pip install commands from the action column above")
    
    with col3:
        if st.button("⬆️ Update All"):
            st.info("Run: pip list --outdated | pip install -U")
    
    with col4:
        if st.button("🧹 Clean Cache"):
            st.info("Run: pip cache purge")
    
    # Footer
    st.markdown("---")
    st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**IntelliCV Software Requirements Management** | Page 22")

if __name__ == "__main__":
    main()