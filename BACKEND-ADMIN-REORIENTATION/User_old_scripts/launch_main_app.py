#!/usr/bin/env python3
"""
IntelliCV-AI Main Application Launcher
=====================================
Cross-platform launcher for the consolidated main.py application
Clean Welcome → Login/Registration → Profile → CV upload flow
"""

import subprocess
import sys
import os
from pathlib import Path
import webbrowser
import time

def print_banner():
    """Print application banner"""
    print("=" * 55)
    print("  🚀 IntelliCV-AI - Intelligent Career Platform")
    print("=" * 55)
    print()

def check_requirements():
    """Check if required files and dependencies exist"""
    print("🔍 Checking requirements...")
    
    # Check main.py exists
    main_py = Path("main.py")
    if not main_py.exists():
        print("❌ Error: main.py not found")
        print("Please ensure you're in the correct directory")
        return False
    
    print("✅ Found main.py")
    
    # Check if streamlit is available
    try:
        import streamlit
        print("✅ Streamlit available")
    except ImportError:
        print("❌ Streamlit not found")
        print("Please install: pip install streamlit")
        return False
    
    return True

def show_app_info():
    """Show application information"""
    print()
    print("🌐 Application will open at: http://localhost:8501")
    print()
    print("📋 User Flow:")
    print("   1. Welcome page (professional entry)")
    print("   2. Login/Registration options")
    print("   3. Profile setup and payment") 
    print("   4. Dashboard with admin AI integration")
    print("   5. Resume upload with enhanced analysis")
    print()
    print("🧠 Features Available:")
    print("   • 6-System AI Coordination (NLP + Bayesian + LLM + Neural + Expert + Statistical)")
    print("   • Enhanced Job Title Engine (422 lines LinkedIn integration)")
    print("   • Real AI Data Connector (3,418+ JSON sources)")
    print("   • Bidirectional Admin Integration")
    print()
    print("⚡ Press Ctrl+C to stop the application")
    print("=" * 55)
    print()

def launch_application():
    """Launch the Streamlit application"""
    try:
        print("🚀 Starting IntelliCV-AI main application...")
        print()
        
        # Launch streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", "main.py",
            "--server.port=8501",
            "--server.address=localhost",
            "--server.headless=true"
        ]
        
        # Start the process
        process = subprocess.Popen(cmd)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Open browser
        print("🌐 Opening browser...")
        webbrowser.open("http://localhost:8501")
        
        # Wait for process to complete
        process.wait()
        
    except KeyboardInterrupt:
        print("\n⚡ Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        return False
    
    return True

def main():
    """Main launcher function"""
    print_banner()
    
    if not check_requirements():
        input("Press Enter to exit...")
        return 1
    
    show_app_info()
    
    if not launch_application():
        input("Press Enter to exit...")
        return 1
    
    print("\n✅ Application session completed")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)