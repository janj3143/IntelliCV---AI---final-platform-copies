"""
BACKEND-ADMIN-REORIENTATION Verification Script
===============================================

This script verifies that all backend components and updated services
are properly synced and functional in the REORIENTATION workspace.

Run from: C:\IntelliCV-AI\IntelliCV\BACKEND-ADMIN-REORIENTATION\admin_portal
"""

import sys
from pathlib import Path
import json

def check_backend_structure():
    """Verify backend directory structure"""
    print("=" * 60)
    print("VERIFYING BACKEND DIRECTORY STRUCTURE")
    print("=" * 60)
    
    backend_path = Path("backend")
    
    critical_files = [
        "backend/ai_services/hybrid_integrator.py",
        "backend/ai_services/neural_network_engine.py",
        "backend/ai_services/expert_system_engine.py",
        "backend/ai_services/feedback_loop_engine.py",
        "backend/ai_services/model_trainer.py",
        "backend/api/main.py",
        "backend/api/requirements.txt",
        "backend/tests/test_hybrid_ai.py",
        "backend/COMPLETE_IMPLEMENTATION_SUMMARY.md",
        "backend/INTEGRATION_GUIDE.md"
    ]
    
    critical_dirs = [
        "backend/data/models",
        "backend/data/rules",
        "backend/data/feedback",
        "backend/logs"
    ]
    
    results = {
        "files_found": 0,
        "files_missing": 0,
        "dirs_found": 0,
        "dirs_missing": 0
    }
    
    print("\n📄 Checking Critical Files:")
    for file_path in critical_files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"  ✅ {file_path} ({size:,} bytes)")
            results["files_found"] += 1
        else:
            print(f"  ❌ {file_path} - MISSING!")
            results["files_missing"] += 1
    
    print("\n📁 Checking Critical Directories:")
    for dir_path in critical_dirs:
        path = Path(dir_path)
        if path.exists() and path.is_dir():
            print(f"  ✅ {dir_path}")
            results["dirs_found"] += 1
        else:
            print(f"  ❌ {dir_path} - MISSING!")
            results["dirs_missing"] += 1
    
    return results

def check_service_updates():
    """Verify updated service files"""
    print("\n" + "=" * 60)
    print("VERIFYING UPDATED SERVICE FILES")
    print("=" * 60)
    
    service_files = [
        "services/intellicv_data_manager.py",
        "services/ai_data_manager.py",
        "services/enhanced_job_title_engine.py",
        "services/linkedin_industry_classifier.py",
        "services/unified_ai_engine.py",
        "services/complete_data_parser.py"
    ]
    
    results = {
        "services_found": 0,
        "services_missing": 0
    }
    
    for service_path in service_files:
        path = Path(service_path)
        if path.exists():
            size = path.stat().st_size
            print(f"  ✅ {service_path} ({size:,} bytes)")
            results["services_found"] += 1
        else:
            print(f"  ❌ {service_path} - MISSING!")
            results["services_missing"] += 1
    
    return results

def check_page_updates():
    """Verify updated page files"""
    print("\n" + "=" * 60)
    print("VERIFYING UPDATED PAGE FILES")
    print("=" * 60)
    
    page_files = [
        "pages/23_AI_Model_Training_Review.py",
        "pages/05_Email_Integration.py",
        "pages/25_Intelligence_Hub.py",
        "pages/90_Production_AI_Data_Generator.py",
        "pages/20_Job_Title_AI_Integration.py",
        "pages/08_AI_Enrichment.py",
        "pages/06_Complete_Data_Parser.py",
        "pages/09_AI_Content_Generator.py"
    ]
    
    results = {
        "pages_found": 0,
        "pages_missing": 0
    }
    
    for page_path in page_files:
        path = Path(page_path)
        if path.exists():
            size = path.stat().st_size
            print(f"  ✅ {page_path} ({size:,} bytes)")
            results["pages_found"] += 1
        else:
            print(f"  ❌ {page_path} - MISSING!")
            results["pages_missing"] += 1
    
    return results

def check_data_manager_version():
    """Check intellicv_data_manager version"""
    print("\n" + "=" * 60)
    print("CHECKING DATA MANAGER VERSION")
    print("=" * 60)
    
    try:
        from services.intellicv_data_manager import IntelliCVDataDirectoryManager
        
        manager = IntelliCVDataDirectoryManager()
        print(f"\n  ✅ Data Manager initialized successfully!")
        print(f"  📂 AI Data Path: {manager.ai_data_path}")
        print(f"  📂 Backend Data Path: {manager.backend_data_path}")
        print(f"  📂 Email Extracted Path: {manager.email_extracted_path}")
        
        # Check if paths point to correct locations
        if "SANDBOX" in str(manager.ai_data_path):
            print(f"  ✅ AI Data Path correctly points to SANDBOX")
        else:
            print(f"  ⚠️  AI Data Path may need verification")
        
        if "backend" in str(manager.backend_data_path):
            print(f"  ✅ Backend Data Path correctly configured")
        else:
            print(f"  ⚠️  Backend Data Path may need verification")
        
        return True
    except Exception as e:
        print(f"  ❌ Error initializing Data Manager: {e}")
        return False

def check_documentation():
    """Verify documentation files"""
    print("\n" + "=" * 60)
    print("VERIFYING DOCUMENTATION FILES")
    print("=" * 60)
    
    doc_files = [
        "DATA_ARCHITECTURE_CLARIFICATION.md",
        "SANDBOX_AI_INTEGRATION_GUIDE.md",
        "REORIENTATION_SYNC_SUMMARY.md"
    ]
    
    results = {
        "docs_found": 0,
        "docs_missing": 0
    }
    
    for doc_path in doc_files:
        path = Path(doc_path)
        if path.exists():
            size = path.stat().st_size
            print(f"  ✅ {doc_path} ({size:,} bytes)")
            results["docs_found"] += 1
        else:
            print(f"  ❌ {doc_path} - MISSING!")
            results["docs_missing"] += 1
    
    return results

def generate_summary_report(all_results):
    """Generate final summary report"""
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY REPORT")
    print("=" * 60)
    
    total_items = 0
    total_found = 0
    total_missing = 0
    
    for category, results in all_results.items():
        print(f"\n{category}:")
        for key, value in results.items():
            print(f"  {key}: {value}")
            if "found" in key:
                total_found += value
            elif "missing" in key:
                total_missing += value
    
    total_items = total_found + total_missing
    
    print("\n" + "=" * 60)
    print("OVERALL STATUS")
    print("=" * 60)
    print(f"  Total Items Checked: {total_items}")
    print(f"  ✅ Found: {total_found}")
    print(f"  ❌ Missing: {total_missing}")
    
    if total_missing == 0:
        print(f"\n  🎉 ALL VERIFICATIONS PASSED!")
        print(f"  🚀 REORIENTATION workspace is ready for development!")
        return True
    else:
        success_rate = (total_found / total_items * 100) if total_items > 0 else 0
        print(f"\n  ⚠️  Success Rate: {success_rate:.1f}%")
        if success_rate >= 90:
            print(f"  ✅ Most components synced successfully")
        else:
            print(f"  ❌ Critical components missing - review errors above")
        return success_rate >= 90

def main():
    """Main verification function"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  BACKEND-ADMIN-REORIENTATION VERIFICATION SCRIPT".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Run all checks
    all_results = {
        "Backend Structure": check_backend_structure(),
        "Service Files": check_service_updates(),
        "Page Files": check_page_updates(),
        "Documentation": check_documentation()
    }
    
    # Check data manager
    data_manager_ok = check_data_manager_version()
    
    # Generate summary
    success = generate_summary_report(all_results)
    
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    
    if success and data_manager_ok:
        print("""
1. Install Backend Dependencies:
   cd backend/api
   pip install -r requirements.txt

2. Run Test Suite:
   cd backend/tests
   python test_hybrid_ai.py

3. Start Backend API Server:
   cd backend/api
   python main.py

4. Test Data Manager:
   python -c "from services.intellicv_data_manager import IntelliCVDataDirectoryManager; import json; mgr = IntelliCVDataDirectoryManager(); print(json.dumps(mgr.get_real_data_stats(), indent=2))"

5. Begin Reorientation Planning:
   - Review current admin portal structure
   - Identify optimization opportunities
   - Plan backend integration improvements
        """)
    else:
        print("""
❌ Some components are missing or need attention.
Please review the errors above and sync missing files from SANDBOX.
        """)
    
    print("=" * 60)

if __name__ == "__main__":
    main()
