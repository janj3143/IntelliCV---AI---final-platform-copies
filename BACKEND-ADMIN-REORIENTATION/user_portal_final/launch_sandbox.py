#!/usr/bin/env python3
"""
🚀 IntelliCV Sandbox User Portal Final - Launch Script
=====================================================

Quick launcher for the comprehensive sandbox testing environment.
Handles environment setup, dependency checking, and application startup.

Usage:
    python launch_sandbox.py [options]

Options:
    --debug     Enable debug mode with verbose logging
    --setup     Run initial setup and dependency installation
    --test      Run in test mode with sample data
    --reset     Reset configuration to defaults

Date: September 29, 2025
Version: Sandbox Launcher v1.0
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
import json
import time
from typing import List, Dict, Optional

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    """Print application header"""
    print(f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                    🧪 IntelliCV-AI Sandbox                   ║
║                  User Portal Final Launcher                  ║
║                                                              ║
║  🚀 Comprehensive Testing Environment                        ║
║  🔐 Enhanced Authentication System                           ║
║  📊 Performance Monitoring & Analytics                       ║
║  🎯 Complete Feature Integration Testing                     ║  
║                                                              ║
║  Version: Sandbox Final v1.0                                ║
║  Date: September 29, 2025                                    ║
╚══════════════════════════════════════════════════════════════╝
{Colors.ENDC}
    """)

def check_python_version() -> bool:
    """Check if Python version is compatible"""
    print(f"{Colors.OKBLUE}🐍 Checking Python version...{Colors.ENDC}")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"{Colors.OKGREEN}✅ Python {version.major}.{version.minor}.{version.micro} - Compatible{Colors.ENDC}")
        return True
    else:
        print(f"{Colors.FAIL}❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+{Colors.ENDC}")
        return False

def check_dependencies() -> bool:
    """Check if required dependencies are installed"""
    print(f"{Colors.OKBLUE}📦 Checking dependencies...{Colors.ENDC}")
    
    required_packages = [
        'streamlit',
        'pandas', 
        'numpy',
        'requests',
        'pathlib',
        'hashlib',
        'secrets',
        'datetime'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"{Colors.OKGREEN}  ✅ {package}{Colors.ENDC}")
        except ImportError:
            print(f"{Colors.WARNING}  ⚠️ {package} - Missing{Colors.ENDC}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"{Colors.FAIL}❌ Missing packages: {', '.join(missing_packages)}{Colors.ENDC}")
        return False
    else:
        print(f"{Colors.OKGREEN}✅ All dependencies available{Colors.ENDC}")
        return True

def install_dependencies() -> bool:
    """Install required dependencies"""
    print(f"{Colors.OKBLUE}📦 Installing dependencies...{Colors.ENDC}")
    
    requirements_file = Path(__file__).parent / "requirements_sandbox.txt"
    
    if not requirements_file.exists():
        print(f"{Colors.WARNING}⚠️ Requirements file not found: {requirements_file}{Colors.ENDC}")
        return False
    
    try:
        print(f"{Colors.OKBLUE}Installing packages from {requirements_file}...{Colors.ENDC}")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"{Colors.OKGREEN}✅ Dependencies installed successfully{Colors.ENDC}")
            return True
        else:
            print(f"{Colors.FAIL}❌ Failed to install dependencies:{Colors.ENDC}")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"{Colors.FAIL}❌ Installation timed out{Colors.ENDC}")
        return False
    except Exception as e:
        print(f"{Colors.FAIL}❌ Installation error: {e}{Colors.ENDC}")
        return False

def setup_environment(reset: bool = False) -> bool:
    """Setup sandbox environment"""
    print(f"{Colors.OKBLUE}⚙️ Setting up sandbox environment...{Colors.ENDC}")
    
    current_dir = Path(__file__).parent
    
    # Create directories if they don't exist
    directories = [
        "auth", "pages", "services", "utils", "fragments", 
        "static", "tests", "data", "logs"
    ]
    
    for directory in directories:
        dir_path = current_dir / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"{Colors.OKGREEN}  ✅ Created directory: {directory}{Colors.ENDC}")
        else:
            print(f"{Colors.OKCYAN}  📁 Directory exists: {directory}{Colors.ENDC}")
    
    # Setup configuration
    config_file = current_dir / "sandbox_config.json"
    
    if reset or not config_file.exists():
        default_config = {
            "environment": "sandbox",
            "debug": True,
            "testing": True,
            "created": time.strftime("%Y-%m-%d %H:%M:%S"),
            "feature_flags": {
                "enhanced_auth": True,
                "admin_integration": True,
                "analytics_dashboard": True,
                "ai_processing": True,
                "job_matching": True,
                "resume_optimization": True,
                "interview_prep": True,
                "market_intelligence": True,
                "debug_mode": True,
                "performance_monitoring": True
            }
        }
        
        try:
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            print(f"{Colors.OKGREEN}  ✅ Configuration initialized{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}  ❌ Failed to create configuration: {e}{Colors.ENDC}")
            return False
    else:
        print(f"{Colors.OKCYAN}  📁 Configuration exists{Colors.ENDC}")
    
    print(f"{Colors.OKGREEN}✅ Environment setup complete{Colors.ENDC}")
    return True

def check_files() -> bool:
    """Check if required application files exist"""
    print(f"{Colors.OKBLUE}📄 Checking application files...{Colors.ENDC}")
    
    current_dir = Path(__file__).parent
    required_files = [
        "sandbox_enhanced_app.py",
        "sandbox_config.py", 
        "auth/sandbox_secure_auth.py",
        "pages/00_Sandbox_Home.py"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        full_path = current_dir / file_path
        if full_path.exists():
            print(f"{Colors.OKGREEN}  ✅ {file_path}{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}  ❌ {file_path} - Missing{Colors.ENDC}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"{Colors.FAIL}❌ Missing files: {', '.join(missing_files)}{Colors.ENDC}")
        return False
    else:
        print(f"{Colors.OKGREEN}✅ All required files present{Colors.ENDC}")
        return True

def get_free_port(start_port: int = 8501) -> int:
    """Find a free port starting from the given port"""
    import socket
    
    for port in range(start_port, start_port + 100):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    
    return start_port  # Fallback

def launch_application(debug: bool = False, test_mode: bool = False) -> bool:
    """Launch the Streamlit application"""
    print(f"{Colors.OKBLUE}🚀 Launching IntelliCV Sandbox...{Colors.ENDC}")
    
    current_dir = Path(__file__).parent
    app_file = current_dir / "sandbox_enhanced_app.py"
    
    if not app_file.exists():
        print(f"{Colors.FAIL}❌ Application file not found: {app_file}{Colors.ENDC}")
        return False
    
    # Find free port
    port = get_free_port(8501)
    
    # Setup environment variables
    env = os.environ.copy()
    if debug:
        env['STREAMLIT_LOGGER_LEVEL'] = 'debug'
    if test_mode:
        env['SANDBOX_TEST_MODE'] = 'true'
    
    # Streamlit command
    cmd = [
        sys.executable, "-m", "streamlit", "run", 
        str(app_file),
        "--server.port", str(port),
        "--server.address", "localhost",
        "--server.headless", "false",
        "--browser.gatherUsageStats", "false"
    ]
    
    print(f"{Colors.OKGREEN}🌐 Starting server on http://localhost:{port}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}📝 Debug mode: {'ON' if debug else 'OFF'}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}🧪 Test mode: {'ON' if test_mode else 'OFF'}{Colors.ENDC}")
    print(f"{Colors.WARNING}🔑 Test credentials: test@intellicv.ai / IntelliCV2025!{Colors.ENDC}")
    print(f"{Colors.HEADER}───────────────────────────────────────────────────────{Colors.ENDC}")
    
    try:
        # Launch Streamlit
        result = subprocess.run(cmd, env=env)
        return result.returncode == 0
    except KeyboardInterrupt:
        print(f"\\n{Colors.WARNING}🛑 Application stopped by user{Colors.ENDC}")
        return True
    except Exception as e:
        print(f"{Colors.FAIL}❌ Failed to launch application: {e}{Colors.ENDC}")
        return False

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(
        description="IntelliCV Sandbox User Portal Final Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug mode with verbose logging"
    )
    
    parser.add_argument(
        "--setup", 
        action="store_true", 
        help="Run initial setup and dependency installation"
    )
    
    parser.add_argument(
        "--test", 
        action="store_true", 
        help="Run in test mode with sample data"
    )
    
    parser.add_argument(
        "--reset", 
        action="store_true", 
        help="Reset configuration to defaults"
    )
    
    args = parser.parse_args()
    
    # Print header
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup environment if requested
    if args.setup or args.reset:
        if not setup_environment(reset=args.reset):
            print(f"{Colors.FAIL}❌ Environment setup failed{Colors.ENDC}")
            sys.exit(1)
        
        if not install_dependencies():
            print(f"{Colors.FAIL}❌ Dependency installation failed{Colors.ENDC}")
            sys.exit(1)
    
    # Check dependencies
    if not args.setup and not check_dependencies():
        print(f"{Colors.WARNING}⚠️ Dependencies missing. Run with --setup to install{Colors.ENDC}")
        sys.exit(1)
    
    # Check files
    if not check_files():
        print(f"{Colors.FAIL}❌ Required files missing{Colors.ENDC}")
        sys.exit(1)
    
    # Launch application
    if not launch_application(debug=args.debug, test_mode=args.test):
        print(f"{Colors.FAIL}❌ Application launch failed{Colors.ENDC}")
        sys.exit(1)
    
    print(f"{Colors.OKGREEN}✅ Sandbox session completed successfully{Colors.ENDC}")

if __name__ == "__main__":
    main()