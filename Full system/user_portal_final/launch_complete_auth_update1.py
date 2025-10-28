#!/usr/bin/env python3
"""
🚀 IntelliCV-AI Complete Authentication System Launcher
Runs the enhanced app with all security features
"""
import subprocess
import sys
import os
from pathlib import Path

# Use virtual environment Python
VENV_PYTHON = Path(__file__).parent.parent / "env310" / "Scripts" / "python.exe"

def get_python_executable():
    """Get the correct Python executable"""
    if VENV_PYTHON.exists():
        return str(VENV_PYTHON)
    else:
        print(f"⚠️ Virtual environment Python not found at {VENV_PYTHON}")
        print("Using system Python")
        return "python"

def main():
    """Launch the complete authentication system"""
    python_exe = get_python_executable()
    app_file = Path(__file__).parent / "enhanced_app_complete_auth_update1.py"
    
    if not app_file.exists():
        print(f"❌ App file not found: {app_file}")
        return
    
    print("🚀 Starting IntelliCV-AI Complete Authentication System...")
    print(f"📁 App file: {app_file}")
    print(f"🐍 Python: {python_exe}")
    print("🌐 Will be available at: http://localhost:8506")
    print("=" * 60)
    
    try:
        # Run with streamlit
        cmd = [
            python_exe, "-m", "streamlit", "run", 
            str(app_file),
            "--server.port", "8506",
            "--server.address", "localhost"
        ]
        
        subprocess.run(cmd, cwd=str(app_file.parent))
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Alternative: Run manually with:")
        print(f"   cd {app_file.parent}")
        print(f"   {python_exe} -m streamlit run {app_file.name} --server.port 8506")

if __name__ == "__main__":
    main()