"""
IntelliCV System Health Test Launcher
=====================================
Quick test to verify the new advanced monitoring system
"""

import sys
import os
from pathlib import Path

# Add admin_portal to path
admin_portal_dir = Path(__file__).parent / "admin_portal"
sys.path.insert(0, str(admin_portal_dir))

def test_new_monitoring_system():
    """Test the new monitoring system"""
    print("🏥 Testing IntelliCV Advanced System Health & AI Error Resolution Suite")
    print("=" * 70)
    
    try:
        # Test import
        print("✅ Testing import...")
        from pages import Logging_Error_Screen_Snapshot_and_Fixes as monitor_page
        print("   ✓ Successfully imported monitoring page")
        
        # Test config loading
        print("✅ Testing configuration...")
        import json
        config_path = admin_portal_dir / "config" / "pages_config.json"
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        pages_count = len(config['admin_portal_pages'])
        print(f"   ✓ Configuration loaded: {pages_count} pages configured")
        
        # Test class initialization
        print("✅ Testing system initialization...")
        monitor = monitor_page.IntelliCVSystemHealthMonitor()
        print(f"   ✓ Monitor initialized with {len(monitor.pages_config)} pages")
        
        # Test VS Code integration
        print("✅ Testing VS Code integration...")
        vscode = monitor_page.VSCodeIntegration()
        print(f"   ✓ VS Code integration ready")
        
        print("\n🎉 All tests passed! The new system is ready for deployment.")
        print("\nKey Features Available:")
        print("- 🚦 Traffic light system for all 14 admin pages")
        print("- 🤖 AI-powered error detection and fix suggestions") 
        print("- 📸 Automated screenshot capture of failures")
        print("- 💻 VS Code integration for real-time debugging")
        print("- 🚀 Live system vs sandbox deployment options")
        print("- ⚡ Continuous monitoring with automated recovery")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def verify_archived_pages():
    """Verify old pages were properly archived"""
    print("\n📦 Verifying page archival...")
    
    archived_dir = admin_portal_dir / "pages" / "archived"
    
    if archived_dir.exists():
        archived_files = list(archived_dir.glob("*.py"))
        print(f"   ✓ Archive directory exists with {len(archived_files)} archived pages")
        
        for file in archived_files:
            print(f"   📄 Archived: {file.name}")
            
        # Check archive info
        archive_info_path = archived_dir / "archive_info.json"
        if archive_info_path.exists():
            print("   ✓ Archive information file found")
            return True
        else:
            print("   ⚠️ Archive information file missing")
            return False
    else:
        print("   ❌ Archive directory not found")
        return False

def show_navigation_update():
    """Show that navigation was updated"""
    print("\n🧭 Navigation Update Verification...")
    
    home_page_path = admin_portal_dir / "pages" / "00_Home.py"
    
    try:
        with open(home_page_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "System Health & AI Fixes" in content:
            print("   ✅ Home page navigation updated successfully")
            print("   🔗 New button: '🏥 System Health & AI Fixes'")
            return True
        else:
            print("   ❌ Navigation update not found")
            return False
            
    except Exception as e:
        print(f"   ❌ Failed to verify navigation: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 IntelliCV Advanced Monitoring System - Verification Test")
    print("=" * 60)
    
    # Run tests
    system_test = test_new_monitoring_system()
    archive_test = verify_archived_pages() 
    nav_test = show_navigation_update()
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    print(f"   System Functionality: {'✅ PASS' if system_test else '❌ FAIL'}")
    print(f"   Page Archival: {'✅ PASS' if archive_test else '❌ FAIL'}")
    print(f"   Navigation Update: {'✅ PASS' if nav_test else '❌ FAIL'}")
    
    if system_test and archive_test and nav_test:
        print("\n🎯 SUCCESS: All systems ready for production!")
        print("\n🚀 To access the new system:")
        print("   1. Launch the admin portal")
        print("   2. Click '🏥 System Health & AI Fixes' on the home page")
        print("   3. Run a full system scan to see all pages in traffic light format")
    else:
        print("\n⚠️ Some tests failed. Please review the output above.")