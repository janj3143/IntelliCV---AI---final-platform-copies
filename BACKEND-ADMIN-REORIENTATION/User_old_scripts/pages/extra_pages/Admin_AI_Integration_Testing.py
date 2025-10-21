"""
🧪 Admin AI Integration Testing Suite
====================================
Comprehensive testing to verify admin AI systems work with user portal pages
Tests: Enhanced Job Title Engine + Real AI Data Connector + Integration Hooks
"""

import streamlit as st
from pathlib import Path
import json
import time
from datetime import datetime
import sys
import tempfile
import traceback

# Setup paths
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Page configuration
st.set_page_config(
    page_title="🧪 Admin AI Integration Testing | IntelliCV-AI",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS for testing interface
def load_testing_css():
    css = '''
    <style>
    .test-header {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .test-section {
        border: 2px solid #dee2e6;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: #f8f9fa;
    }
    
    .test-pass {
        background: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 5px 5px 0;
    }
    
    .test-fail {
        background: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 5px 5px 0;
    }
    
    .test-warning {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 5px 5px 0;
    }
    
    .integration-status {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

load_testing_css()

# Header
st.markdown('''
<div class="test-header">
    <h1>🧪 Admin AI Integration Testing</h1>
    <p>Comprehensive verification of admin AI systems integration with user portal</p>
</div>
''', unsafe_allow_html=True)

# Testing results storage
if 'test_results' not in st.session_state:
    st.session_state.test_results = {}

def run_test(test_name, test_function, description=""):
    """Run a test and store results"""
    try:
        with st.spinner(f"Running {test_name}..."):
            result = test_function()
            st.session_state.test_results[test_name] = {
                'status': 'PASS' if result else 'FAIL',
                'result': result,
                'timestamp': datetime.now().isoformat(),
                'description': description
            }
            return result
    except Exception as e:
        st.session_state.test_results[test_name] = {
            'status': 'ERROR',
            'error': str(e),
            'traceback': traceback.format_exc(),
            'timestamp': datetime.now().isoformat(),
            'description': description
        }
        return False

def test_admin_ai_integration_import():
    """Test if admin AI integration module can be imported"""
    try:
        from user_portal_admin_integration import init_admin_ai_for_user_page, process_user_action_with_admin_ai
        return True
    except ImportError:
        return False

def test_admin_systems_availability():
    """Test if admin AI systems are available"""
    try:
        # Check for admin portal files
        admin_files = [
            Path(current_dir.parent) / "SANDBOX" / "integration_hooks.py",
            Path(current_dir.parent) / "SANDBOX" / "enhanced_job_title_engine.py",
            Path(current_dir.parent) / "SANDBOX" / "real_ai_data_connector.py"
        ]
        
        available_files = []
        for file_path in admin_files:
            if file_path.exists():
                available_files.append(file_path.name)
        
        return len(available_files) >= 2  # At least 2 admin systems should be available
    except Exception:
        return False

def test_enhanced_job_title_engine():
    """Test Enhanced Job Title Engine integration"""
    try:
        from user_portal_admin_integration import init_admin_ai_for_user_page
        admin_ai = init_admin_ai_for_user_page()
        
        # Test job title analysis
        test_data = {
            'job_title': 'Senior Software Engineer',
            'industry': 'Technology',
            'skills': ['Python', 'JavaScript', 'React']
        }
        
        # This should connect to the enhanced job title engine
        result = admin_ai.process_with_job_title_engine(test_data)
        return result is not None
    except Exception:
        return False

def test_real_ai_data_connector():
    """Test Real AI Data Connector integration"""
    try:
        from user_portal_admin_integration import init_admin_ai_for_user_page
        admin_ai = init_admin_ai_for_user_page()
        
        # Test data processing
        test_data = {
            'user_action': 'resume_upload',
            'data': {'test': 'data'}
        }
        
        # This should connect to the real AI data connector
        result = admin_ai.process_with_data_connector(test_data)
        return result is not None
    except Exception:
        return False

def test_bidirectional_enrichment():
    """Test bidirectional data enrichment"""
    try:
        from user_portal_admin_integration import process_user_action_with_admin_ai
        
        test_user_data = {
            'user_id': 'test_user',
            'action': 'resume_upload',
            'data': {'skills': ['Python', 'Machine Learning']}
        }
        
        # Test if user data enriches admin systems
        result = process_user_action_with_admin_ai('test_enrichment', test_user_data)
        return result.get('bidirectional_enrichment', False)
    except Exception:
        return False

def test_statistical_analysis_integration():
    """Test statistical analysis tools integration"""
    try:
        from user_portal_admin_integration import init_admin_ai_for_user_page
        admin_ai = init_admin_ai_for_user_page()
        
        test_data = {
            'metrics': ['salary', 'job_match_score', 'market_demand'],
            'user_profile': {'experience': 5, 'skills': ['Python', 'Data Science']}
        }
        
        # Test statistical analysis
        result = admin_ai.get_statistical_analysis(test_data)
        return result is not None
    except Exception:
        return False

# Main Testing Interface
st.subheader("🔬 Test Suite Controls")

test_col1, test_col2 = st.columns(2)

with test_col1:
    if st.button("🚀 Run All Tests", type="primary"):
        st.write("### Running Comprehensive Test Suite...")
        
        # Run all tests
        tests = [
            ("Integration Import", test_admin_ai_integration_import, "Test if admin AI integration module can be imported"),
            ("Admin Systems Availability", test_admin_systems_availability, "Check if admin AI system files are available"),
            ("Enhanced Job Title Engine", test_enhanced_job_title_engine, "Test enhanced job title engine integration"),
            ("Real AI Data Connector", test_real_ai_data_connector, "Test real AI data connector integration"),
            ("Bidirectional Enrichment", test_bidirectional_enrichment, "Test bidirectional data enrichment"),
            ("Statistical Analysis", test_statistical_analysis_integration, "Test statistical analysis tools integration")
        ]
        
        for test_name, test_func, description in tests:
            result = run_test(test_name, test_func, description)
            if result:
                st.markdown(f'<div class="test-pass">✅ {test_name}: PASSED</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="test-fail">❌ {test_name}: FAILED</div>', unsafe_allow_html=True)

with test_col2:
    if st.button("🔄 Clear Test Results"):
        st.session_state.test_results = {}
        st.success("✅ Test results cleared")

# Display Test Results
if st.session_state.test_results:
    st.subheader("📊 Test Results Summary")
    
    # Calculate summary stats
    total_tests = len(st.session_state.test_results)
    passed_tests = sum(1 for result in st.session_state.test_results.values() if result['status'] == 'PASS')
    failed_tests = sum(1 for result in st.session_state.test_results.values() if result['status'] == 'FAIL')
    error_tests = sum(1 for result in st.session_state.test_results.values() if result['status'] == 'ERROR')
    
    # Summary metrics
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.metric("Total Tests", total_tests)
    
    with summary_col2:
        st.metric("✅ Passed", passed_tests, delta=f"{(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%")
    
    with summary_col3:
        st.metric("❌ Failed", failed_tests, delta=f"{(failed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%")
    
    with summary_col4:
        st.metric("🚨 Errors", error_tests, delta=f"{(error_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%")
    
    # Detailed results
    st.subheader("📋 Detailed Test Results")
    
    for test_name, result in st.session_state.test_results.items():
        with st.expander(f"🔍 {test_name} - {result['status']}", expanded=result['status'] != 'PASS'):
            if result['status'] == 'PASS':
                st.markdown(f'<div class="test-pass"><strong>✅ {test_name}: PASSED</strong><br>{result.get("description", "")}</div>', unsafe_allow_html=True)
            elif result['status'] == 'FAIL':
                st.markdown(f'<div class="test-fail"><strong>❌ {test_name}: FAILED</strong><br>{result.get("description", "")}</div>', unsafe_allow_html=True)
            else:  # ERROR
                st.markdown(f'<div class="test-fail"><strong>🚨 {test_name}: ERROR</strong><br>{result.get("description", "")}</div>', unsafe_allow_html=True)
                st.error(f"Error: {result.get('error', 'Unknown error')}")
                
                if st.checkbox(f"Show traceback for {test_name}"):
                    st.code(result.get('traceback', 'No traceback available'))
            
            st.write(f"**Timestamp:** {result.get('timestamp', 'Unknown')}")

# Manual Integration Testing
st.subheader("🔧 Manual Integration Tests")

with st.expander("🧪 Test Individual Components", expanded=False):
    st.write("### Test Admin AI Integration Manually")
    
    # Test resume upload integration
    st.write("#### 📄 Test Resume Upload Integration")
    
    if st.button("Test Resume Upload with Admin AI"):
        try:
            from user_portal_admin_integration import process_user_action_with_admin_ai
            
            # Create test file data
            test_user_data = {
                'user_id': 'test_user_' + str(int(time.time())),
                'filename': 'test_resume.pdf',
                'profile_data': {
                    'full_name': 'Test User',
                    'email': 'test@example.com',
                    'skills': ['Python', 'Machine Learning', 'Data Analysis']
                }
            }
            
            # Create a temporary file to simulate upload
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                temp_file.write(b"Test resume content for integration testing")
                temp_file_path = temp_file.name
            
            with open(temp_file_path, 'rb') as test_file:
                result = process_user_action_with_admin_ai('resume_upload', test_user_data, test_file)
            
            st.success("✅ Resume upload integration test completed")
            st.json(result)
            
        except Exception as e:
            st.error(f"❌ Resume upload test failed: {str(e)}")
    
    # Test job search integration
    st.write("#### 🎯 Test Job Search Integration")
    
    if st.button("Test Job Search with Admin AI"):
        try:
            from user_portal_admin_integration import process_user_action_with_admin_ai
            
            test_search_data = {
                'user_id': 'test_user_' + str(int(time.time())),
                'search_filters': {
                    'job_title': 'Software Engineer',
                    'location': 'San Francisco',
                    'salary_min': 80000,
                    'experience_level': 'Mid Level'
                },
                'profile_data': {
                    'skills': ['Python', 'JavaScript', 'React'],
                    'experience': 3
                }
            }
            
            result = process_user_action_with_admin_ai('job_search', test_search_data)
            
            st.success("✅ Job search integration test completed")
            st.json(result)
            
        except Exception as e:
            st.error(f"❌ Job search test failed: {str(e)}")
    
    # Test AI career intelligence integration
    st.write("#### 🧠 Test AI Career Intelligence Integration")
    
    if st.button("Test Career Intelligence with Admin AI"):
        try:
            from user_portal_admin_integration import process_user_action_with_admin_ai
            
            test_intelligence_data = {
                'user_id': 'test_user_' + str(int(time.time())),
                'profile_data': {
                    'experience_level': 'Mid Level',
                    'skills': ['Python', 'Data Science', 'Machine Learning'],
                    'industry': 'Technology'
                },
                'career_goals': {
                    'target_role': 'Senior Data Scientist',
                    'timeline': '12 months'
                }
            }
            
            result = process_user_action_with_admin_ai('career_intelligence_analysis', test_intelligence_data)
            
            st.success("✅ Career intelligence integration test completed")
            st.json(result)
            
        except Exception as e:
            st.error(f"❌ Career intelligence test failed: {str(e)}")

# Admin Systems Status Check
st.subheader("⚙️ Admin Systems Status")

try:
    # Check admin system files
    admin_systems_status = {}
    
    admin_files_to_check = [
        ("Integration Hooks", Path(current_dir.parent) / "SANDBOX" / "integration_hooks.py"),
        ("Enhanced Job Title Engine", Path(current_dir.parent) / "SANDBOX" / "enhanced_job_title_engine.py"),
        ("Real AI Data Connector", Path(current_dir.parent) / "SANDBOX" / "real_ai_data_connector.py"),
        ("User Portal Integration", Path(current_dir) / "user_portal_admin_integration.py")
    ]
    
    status_col1, status_col2 = st.columns(2)
    
    with status_col1:
        for name, file_path in admin_files_to_check[:2]:
            if file_path.exists():
                st.markdown(f'<div class="integration-status">✅ <strong>{name}:</strong> Available<br><small>{file_path}</small></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="integration-status">❌ <strong>{name}:</strong> Not Found<br><small>{file_path}</small></div>', unsafe_allow_html=True)
    
    with status_col2:
        for name, file_path in admin_files_to_check[2:]:
            if file_path.exists():
                st.markdown(f'<div class="integration-status">✅ <strong>{name}:</strong> Available<br><small>{file_path}</small></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="integration-status">❌ <strong>{name}:</strong> Not Found<br><small>{file_path}</small></div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Error checking admin systems status: {str(e)}")

# Integration Recommendations
st.subheader("💡 Integration Recommendations")

recommendations = [
    {
        'priority': 'HIGH',
        'title': 'Verify Admin AI Files Availability',
        'description': 'Ensure integration_hooks.py, enhanced_job_title_engine.py, and real_ai_data_connector.py are accessible from user portal',
        'action': 'Check file paths and import statements'
    },
    {
        'priority': 'HIGH',
        'title': 'Test Real Data Processing',
        'description': 'Verify that user actions actually trigger admin AI processing with real results',
        'action': 'Upload actual resume and verify enhanced analysis'
    },
    {
        'priority': 'MEDIUM',
        'title': 'Validate Bidirectional Enrichment',
        'description': 'Confirm that user data enriches admin AI systems for improved future processing',
        'action': 'Test multiple user interactions and verify system learning'
    },
    {
        'priority': 'MEDIUM',
        'title': 'Performance Testing',
        'description': 'Test admin AI integration performance under load',
        'action': 'Run multiple concurrent user actions and measure response times'
    }
]

for rec in recommendations:
    priority_color = '#dc3545' if rec['priority'] == 'HIGH' else '#ffc107'
    st.markdown(f'''
    <div class="integration-status" style="border-left: 5px solid {priority_color};">
        <h4>{rec['priority']} PRIORITY: {rec['title']}</h4>
        <p><strong>Description:</strong> {rec['description']}</p>
        <p><strong>Action:</strong> {rec['action']}</p>
    </div>
    ''', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"**Testing Session:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("**Integration Testing Suite:** IntelliCV-AI Admin AI Integration Verification")