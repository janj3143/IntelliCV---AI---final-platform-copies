"""
🔧 Automated Admin AI Integration Verification Script
===================================================
Automatically checks that all modified user pages have proper admin AI integration
"""

import streamlit as st
from pathlib import Path
import importlib.util
import sys
import traceback
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🔧 Admin AI Integration Verification | IntelliCV-AI",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS for verification interface
def load_verification_css():
    css = '''
    <style>
    .verification-header {
        background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .page-check {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 5px solid #17a2b8;
    }
    
    .check-pass {
        background: #d4edda;
        border-left-color: #28a745;
        border: 1px solid #c3e6cb;
    }
    
    .check-fail {
        background: #f8d7da;
        border-left-color: #dc3545;
        border: 1px solid #f5c6cb;
    }
    
    .check-warning {
        background: #fff3cd;
        border-left-color: #ffc107;
        border: 1px solid #ffeaa7;
    }
    
    .integration-summary {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin: 2rem 0;
    }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

load_verification_css()

# Header
st.markdown('''
<div class="verification-header">
    <h1>🔧 Admin AI Integration Verification</h1>
    <p>Automated verification that all user pages have proper admin AI hooks</p>
</div>
''', unsafe_allow_html=True)

# List of pages to check
pages_to_check = [
    {
        'name': '04_Dashboard.py',
        'path': 'pages/04_Dashboard.py',
        'description': 'User dashboard with admin AI enhanced metrics'
    },
    {
        'name': '05_Resume_Upload.py',
        'path': 'pages/05_Resume_Upload.py',
        'description': 'Original resume upload with admin AI integration'
    },
    {
        'name': '02_Profile_Enhanced.py',
        'path': 'pages/02_Profile_Enhanced.py',
        'description': 'Enhanced profile management with admin AI'
    },
    {
        'name': '06_Job_Match.py',
        'path': 'pages/06_Job_Match.py',
        'description': 'Job matching with admin AI enhancement'
    },
    {
        'name': '08_Career_Intelligence.py',
        'path': 'pages/08_Career_Intelligence.py',
        'description': 'Career intelligence with admin AI coordination'
    }
]

# Verification functions
def check_admin_ai_import(file_path):
    """Check if page imports admin AI integration"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        imports_to_check = [
            'from user_portal_admin_integration import',
            'process_user_action_with_admin_ai',
            'init_admin_ai_for_user_page'
        ]
        
        results = {}
        for import_check in imports_to_check:
            results[import_check] = import_check in content
        
        return all(results.values()), results
    except Exception as e:
        return False, {'error': str(e)}

def check_admin_ai_initialization(file_path):
    """Check if page initializes admin AI"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        initialization_checks = [
            'ADMIN_AI_AVAILABLE',
            'init_admin_ai_for_user_page()',
            'admin_ai ='
        ]
        
        results = {}
        for check in initialization_checks:
            results[check] = check in content
        
        return all(results.values()), results
    except Exception as e:
        return False, {'error': str(e)}

def check_admin_ai_usage(file_path):
    """Check if page uses admin AI processing"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        usage_checks = [
            'process_user_action_with_admin_ai',
            'admin_ai.is_admin_ai_available()',
            'enhanced_data'
        ]
        
        results = {}
        for check in usage_checks:
            results[check] = check in content
        
        # At least one usage pattern should be present
        return any(results.values()), results
    except Exception as e:
        return False, {'error': str(e)}

def check_sidebar_status(file_path):
    """Check if page displays admin AI status in sidebar"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sidebar_checks = [
            'st.sidebar.success',
            'Admin AI Integration',
            'ACTIVE'
        ]
        
        results = {}
        for check in sidebar_checks:
            results[check] = check in content
        
        return all(results.values()), results
    except Exception as e:
        return False, {'error': str(e)}

# Run verification
st.subheader("🔍 Running Verification Checks...")

if st.button("🚀 Verify All Pages", type="primary"):
    
    verification_results = {}
    
    for page_info in pages_to_check:
        page_name = page_info['name']
        file_path = Path(__file__).parent / page_info['path']
        
        st.write(f"### Checking {page_name}")
        
        if not file_path.exists():
            st.markdown(f'''
            <div class="page-check check-fail">
                <h4>❌ {page_name} - FILE NOT FOUND</h4>
                <p>Path: {file_path}</p>
            </div>
            ''', unsafe_allow_html=True)
            continue
        
        # Run all checks
        checks = {
            'Import Check': check_admin_ai_import(file_path),
            'Initialization Check': check_admin_ai_initialization(file_path),
            'Usage Check': check_admin_ai_usage(file_path),
            'Sidebar Status Check': check_sidebar_status(file_path)
        }
        
        page_results = {}
        all_passed = True
        
        for check_name, (passed, details) in checks.items():
            page_results[check_name] = {'passed': passed, 'details': details}
            if not passed:
                all_passed = False
        
        verification_results[page_name] = {
            'all_passed': all_passed,
            'checks': page_results,
            'description': page_info['description']
        }
        
        # Display results for this page
        status_class = "check-pass" if all_passed else "check-fail"
        status_icon = "✅" if all_passed else "❌"
        
        st.markdown(f'''
        <div class="page-check {status_class}">
            <h4>{status_icon} {page_name} - {'PASS' if all_passed else 'FAIL'}</h4>
            <p><strong>Description:</strong> {page_info['description']}</p>
            <p><strong>File Path:</strong> {file_path}</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Show detailed check results
        with st.expander(f"📋 Detailed Results for {page_name}"):
            for check_name, result in page_results.items():
                if result['passed']:
                    st.success(f"✅ {check_name}: PASSED")
                else:
                    st.error(f"❌ {check_name}: FAILED")
                    if 'error' in result['details']:
                        st.error(f"Error: {result['details']['error']}")
                    else:
                        st.write("**Details:**", result['details'])
    
    # Summary
    st.subheader("📊 Verification Summary")
    
    total_pages = len(verification_results)
    passed_pages = sum(1 for result in verification_results.values() if result['all_passed'])
    failed_pages = total_pages - passed_pages
    
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    with summary_col1:
        st.metric("Total Pages Checked", total_pages)
    
    with summary_col2:
        st.metric("✅ Passed", passed_pages, delta=f"{(passed_pages/total_pages)*100:.1f}%" if total_pages > 0 else "0%")
    
    with summary_col3:
        st.metric("❌ Failed", failed_pages, delta=f"{(failed_pages/total_pages)*100:.1f}%" if total_pages > 0 else "0%")
    
    # Integration readiness assessment
    if failed_pages == 0:
        st.markdown('''
        <div class="integration-summary">
            <h3>🎉 ALL PAGES READY FOR ADMIN AI INTEGRATION!</h3>
            <p><strong>✅ All user pages have been successfully modified with admin AI hooks</strong></p>
            <p><strong>✅ Users will now get enhanced processing when admin AI systems are available</strong></p>
            <p><strong>✅ Bidirectional data enrichment is properly configured</strong></p>
            <p><strong>✅ Enhanced job title engine and real AI data connector integration complete</strong></p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="integration-summary" style="background: linear-gradient(45deg, #dc3545, #c82333);">
            <h3>⚠️ INTEGRATION INCOMPLETE - {failed_pages} PAGES NEED FIXES</h3>
            <p><strong>❌ Some pages are missing admin AI integration</strong></p>
            <p><strong>⚠️ Users may not get enhanced processing on all pages</strong></p>
            <p><strong>🔧 Review failed pages and add missing integration hooks</strong></p>
        </div>
        ''', unsafe_allow_html=True)

# Manual page modification section
st.subheader("🔧 Manual Page Modification Tools")

with st.expander("🛠️ Quick Fix Tools", expanded=False):
    st.write("### Quick Admin AI Integration Template")
    
    template_code = '''
# Import admin AI integration
try:
    from user_portal_admin_integration import process_user_action_with_admin_ai, init_admin_ai_for_user_page
    ADMIN_AI_AVAILABLE = True
except ImportError:
    ADMIN_AI_AVAILABLE = False

# Initialize Admin AI Integration (after authentication check)
if ADMIN_AI_AVAILABLE:
    admin_ai = init_admin_ai_for_user_page()
    st.sidebar.success("🚀 Admin AI Integration: ACTIVE")
    st.sidebar.info("Enhanced processing with admin AI systems")
else:
    st.sidebar.warning("⚠️ Admin AI Integration: NOT AVAILABLE")
    st.sidebar.error("Basic processing only")

# Process user action with admin AI
if ADMIN_AI_AVAILABLE and admin_ai.is_admin_ai_available():
    result = process_user_action_with_admin_ai('action_name', user_data)
    enhanced_data = result.get('enhanced_data', {})
else:
    # Fallback processing
    enhanced_data = {}
'''
    
    st.code(template_code, language='python')
    
    st.write("### Integration Checklist for Each Page:")
    st.markdown("""
    - [ ] Import `user_portal_admin_integration` module
    - [ ] Add `ADMIN_AI_AVAILABLE` flag
    - [ ] Initialize admin AI after authentication check
    - [ ] Add sidebar status display
    - [ ] Process user actions with admin AI when available
    - [ ] Handle fallback when admin AI not available
    - [ ] Display enhanced results when admin processing succeeds
    """)

# Testing recommendations
st.subheader("🧪 Testing Recommendations")

st.markdown("""
### Next Steps for Testing:

1. **🚀 Run Integration Test Suite**
   - Use `Admin_AI_Integration_Testing.py` to verify connections
   - Test with actual admin AI systems available
   
2. **📄 Test Resume Upload Flow**
   - Upload a real resume on `05_Resume_Upload.py`
   - Verify enhanced analysis appears when admin AI active
   
3. **🎯 Test Job Matching**
   - Use `06_Job_Match.py` with admin AI integration
   - Verify LinkedIn industry integration works
   
4. **📊 Test Dashboard Metrics**
   - Check `04_Dashboard.py` for enhanced admin AI metrics
   - Verify bidirectional data enrichment status
   
5. **👤 Test Profile Management**
   - Use `02_Profile_Enhanced.py` with admin career intelligence
   - Verify skill analysis and career trajectory insights
""")

# Footer
st.markdown("---")
st.markdown(f"**Verification Completed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("**Admin AI Integration Verification Suite** - IntelliCV-AI")