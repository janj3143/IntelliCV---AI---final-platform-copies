"""
Phase 2 Integration Tests - Portal Bridge Validation
Tests the Portal Bridge connection to AI intelligence system

Created: October 21, 2025 - Phase 2 (Day 2)
"""

import sys
from pathlib import Path

# Add paths
backend_path = Path(__file__).parent / "shared_backend"
sys.path.insert(0, str(backend_path))

from services.portal_bridge import (
    PortalBridge,
    get_portal_bridge,
    get_career_prediction,
    get_job_match,
    get_skill_gaps,
    get_salary_estimate,
    get_company_intel,
    get_market_intel
)


def test_portal_bridge_initialization():
    """Test Portal Bridge initializes correctly"""
    print("\n" + "="*80)
    print("TEST 1: Portal Bridge Initialization")
    print("="*80)
    
    bridge = PortalBridge()
    
    # Check components initialized
    assert bridge.ai_integrator is not None, "AI Integrator not initialized"
    assert bridge.intelligence_registry is not None, "Intelligence Registry not initialized"
    assert bridge.portal_metrics is not None, "Portal metrics not initialized"
    
    print("✓ Portal Bridge initialized successfully")
    print(f"✓ Available intelligence types: {len(bridge.intelligence_registry.types)}")
    print(f"✓ Portal metrics tracking: {bridge.portal_metrics['total_requests']} requests")
    

def test_career_path_prediction():
    """Test career path prediction via portal bridge"""
    print("\n" + "="*80)
    print("TEST 2: Career Path Prediction")
    print("="*80)
    
    bridge = get_portal_bridge()
    
    user_profile = {
        'current_role': 'Software Engineer',
        'experience_years': 5,
        'skills': ['Python', 'JavaScript', 'React', 'AWS'],
        'education': 'BS Computer Science'
    }
    
    result = bridge.portal_career_path_prediction(
        user_profile=user_profile,
        target_role='Senior Software Engineer',
        portal_type='user'
    )
    
    print(f"Career Path Result: {result}")
    assert 'portal_bridge_metadata' in result, "Missing portal bridge metadata"
    assert result['portal_bridge_metadata']['intelligence_type'] == 'career_path'
    print("✓ Career path prediction working via portal bridge")


def test_job_matching():
    """Test job matching via portal bridge"""
    print("\n" + "="*80)
    print("TEST 3: Job Matching")
    print("="*80)
    
    bridge = get_portal_bridge()
    
    candidate = {
        'name': 'John Doe',
        'current_role': 'Data Analyst',
        'skills': ['Python', 'SQL', 'Tableau', 'Statistics'],
        'experience_years': 3
    }
    
    job = {
        'title': 'Senior Data Analyst',
        'required_skills': ['Python', 'SQL', 'Power BI', 'Statistics'],
        'experience_required': 3,
        'location': 'San Francisco, CA'
    }
    
    result = bridge.portal_job_matching(
        candidate_profile=candidate,
        job_posting=job,
        portal_type='user'
    )
    
    print(f"Job Match Result: {result}")
    assert 'portal_bridge_metadata' in result, "Missing portal bridge metadata"
    assert result['portal_bridge_metadata']['intelligence_type'] == 'job_match'
    print("✓ Job matching working via portal bridge")


def test_skill_gap_analysis():
    """Test skill gap analysis via portal bridge"""
    print("\n" + "="*80)
    print("TEST 4: Skill Gap Analysis")
    print("="*80)
    
    bridge = get_portal_bridge()
    
    current_skills = ['Python', 'SQL', 'Excel']
    target_role = 'Data Scientist'
    
    result = bridge.portal_skill_gap_analysis(
        current_skills=current_skills,
        target_role=target_role,
        portal_type='user'
    )
    
    print(f"Skill Gap Result: {result}")
    assert 'portal_bridge_metadata' in result, "Missing portal bridge metadata"
    assert result['portal_bridge_metadata']['intelligence_type'] == 'skill_gaps'
    print("✓ Skill gap analysis working via portal bridge")


def test_salary_estimate():
    """Test salary estimation via portal bridge"""
    print("\n" + "="*80)
    print("TEST 5: Salary Estimation")
    print("="*80)
    
    bridge = get_portal_bridge()
    
    result = bridge.portal_salary_estimate(
        job_title='Software Engineer',
        location='New York, NY',
        experience_years=5,
        skills=['Python', 'React', 'AWS'],
        portal_type='user'
    )
    
    print(f"Salary Estimate Result: {result}")
    assert 'portal_bridge_metadata' in result, "Missing portal bridge metadata"
    assert result['portal_bridge_metadata']['intelligence_type'] == 'salary'
    print("✓ Salary estimation working via portal bridge")


def test_company_intelligence():
    """Test company intelligence via portal bridge"""
    print("\n" + "="*80)
    print("TEST 6: Company Intelligence")
    print("="*80)
    
    bridge = get_portal_bridge()
    
    result = bridge.portal_company_intelligence(
        company_name='RESATO INTERNATIONAL',
        research_depth='standard',
        portal_type='admin'
    )
    
    print(f"Company Intelligence Result: {result}")
    assert 'portal_bridge_metadata' in result, "Missing portal bridge metadata"
    assert result['portal_bridge_metadata']['intelligence_type'] == 'company_intelligence'
    print("✓ Company intelligence working via portal bridge")


def test_market_intelligence():
    """Test market intelligence via portal bridge"""
    print("\n" + "="*80)
    print("TEST 7: Market Intelligence")
    print("="*80)
    
    bridge = get_portal_bridge()
    
    result = bridge.portal_market_intelligence(
        industry='Technology',
        location='San Francisco Bay Area',
        portal_type='admin'
    )
    
    print(f"Market Intelligence Result: {result}")
    assert 'portal_bridge_metadata' in result, "Missing portal bridge metadata"
    assert result['portal_bridge_metadata']['intelligence_type'] == 'market_intelligence'
    print("✓ Market intelligence working via portal bridge")


def test_profile_enrichment():
    """Test profile enrichment via portal bridge"""
    print("\n" + "="*80)
    print("TEST 8: Profile Enrichment")
    print("="*80)
    
    bridge = get_portal_bridge()
    
    user_profile = {
        'name': 'Jane Smith',
        'current_role': 'Marketing Manager',
        'skills': ['SEO', 'Content Strategy', 'Analytics'],
        'experience_years': 6
    }
    
    result = bridge.portal_profile_enrichment(
        user_profile=user_profile,
        enrichment_level='standard',
        portal_type='user'
    )
    
    print(f"Profile Enrichment Result: {result}")
    assert 'portal_bridge_metadata' in result, "Missing portal bridge metadata"
    assert result['portal_bridge_metadata']['intelligence_type'] == 'profile_analysis'
    print("✓ Profile enrichment working via portal bridge")


def test_universal_intelligence_access():
    """Test universal get_intelligence method"""
    print("\n" + "="*80)
    print("TEST 9: Universal Intelligence Access")
    print("="*80)
    
    bridge = get_portal_bridge()
    
    # Test accessing custom intelligence type
    result = bridge.get_intelligence(
        intelligence_type='commute_analysis',
        data={'location': 'San Francisco, CA'},
        portal_type='user'
    )
    
    print(f"Universal Intelligence Result: {result}")
    assert 'portal_bridge_metadata' in result, "Missing portal bridge metadata"
    assert result['portal_bridge_metadata']['intelligence_type'] == 'commute_analysis'
    print("✓ Universal intelligence access working")


def test_admin_dashboard_metrics():
    """Test admin dashboard metrics"""
    print("\n" + "="*80)
    print("TEST 10: Admin Dashboard Metrics")
    print("="*80)
    
    bridge = get_portal_bridge()
    
    metrics = bridge.portal_admin_dashboard_metrics()
    
    print(f"Dashboard Metrics: {metrics}")
    assert 'intelligence_metrics' in metrics, "Missing intelligence metrics"
    assert 'portal_metrics' in metrics, "Missing portal metrics"
    assert 'ai_performance' in metrics, "Missing AI performance"
    print("✓ Admin dashboard metrics working")


def test_intelligence_catalog():
    """Test intelligence type catalog"""
    print("\n" + "="*80)
    print("TEST 11: Intelligence Type Catalog")
    print("="*80)
    
    bridge = get_portal_bridge()
    
    catalog = bridge.portal_admin_intelligence_catalog()
    
    print(f"Intelligence Catalog: {len(catalog)} types available")
    assert len(catalog) > 0, "No intelligence types in catalog"
    print("✓ Intelligence catalog working")


def test_portal_metrics_tracking():
    """Test portal metrics tracking"""
    print("\n" + "="*80)
    print("TEST 12: Portal Metrics Tracking")
    print("="*80)
    
    bridge = get_portal_bridge()
    
    # Make several requests
    initial_requests = bridge.portal_metrics['total_requests']
    
    bridge.portal_career_path_prediction(
        user_profile={'current_role': 'Engineer'},
        portal_type='user'
    )
    
    bridge.portal_company_intelligence(
        company_name='Test Company',
        portal_type='admin'
    )
    
    # Check metrics updated
    final_requests = bridge.portal_metrics['total_requests']
    assert final_requests > initial_requests, "Metrics not tracking requests"
    
    print(f"Total Requests: {final_requests}")
    print(f"Admin Requests: {bridge.portal_metrics['admin_requests']}")
    print(f"User Requests: {bridge.portal_metrics['user_requests']}")
    print("✓ Portal metrics tracking working")


def test_convenience_functions():
    """Test convenience functions"""
    print("\n" + "="*80)
    print("TEST 13: Convenience Functions")
    print("="*80)
    
    # Test career prediction
    result1 = get_career_prediction({'current_role': 'Analyst'})
    assert result1 is not None, "Career prediction convenience function failed"
    print("✓ get_career_prediction() working")
    
    # Test job match
    result2 = get_job_match({'skills': ['Python']}, {'title': 'Developer'})
    assert result2 is not None, "Job match convenience function failed"
    print("✓ get_job_match() working")
    
    # Test skill gaps
    result3 = get_skill_gaps(['Python'], 'Data Scientist')
    assert result3 is not None, "Skill gaps convenience function failed"
    print("✓ get_skill_gaps() working")
    
    # Test salary estimate
    result4 = get_salary_estimate('Engineer', 'SF', 5)
    assert result4 is not None, "Salary estimate convenience function failed"
    print("✓ get_salary_estimate() working")
    
    # Test company intel
    result5 = get_company_intel('Test Corp')
    assert result5 is not None, "Company intel convenience function failed"
    print("✓ get_company_intel() working")
    
    # Test market intel
    result6 = get_market_intel('Technology')
    assert result6 is not None, "Market intel convenience function failed"
    print("✓ get_market_intel() working")


def test_intelligence_type_queries():
    """Test intelligence type query methods"""
    print("\n" + "="*80)
    print("TEST 14: Intelligence Type Queries")
    print("="*80)
    
    bridge = get_portal_bridge()
    
    # List all types
    all_types = bridge.list_available_intelligence_types()
    print(f"Available intelligence types: {len(all_types)}")
    assert len(all_types) > 0, "No intelligence types available"
    
    # Get type info
    if all_types:
        first_type = all_types[0]
        type_info = bridge.get_intelligence_type_info(first_type)
        print(f"Type info for {first_type}: {type_info}")
    
    print("✓ Intelligence type queries working")


def run_all_tests():
    """Run all Phase 2 integration tests"""
    print("\n" + "#"*80)
    print("# PHASE 2 INTEGRATION TESTS - PORTAL BRIDGE VALIDATION")
    print("#"*80)
    
    tests = [
        test_portal_bridge_initialization,
        test_career_path_prediction,
        test_job_matching,
        test_skill_gap_analysis,
        test_salary_estimate,
        test_company_intelligence,
        test_market_intelligence,
        test_profile_enrichment,
        test_universal_intelligence_access,
        test_admin_dashboard_metrics,
        test_intelligence_catalog,
        test_portal_metrics_tracking,
        test_convenience_functions,
        test_intelligence_type_queries
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"\n✗ TEST FAILED: {test.__name__}")
            print(f"Error: {e}")
            failed += 1
    
    print("\n" + "#"*80)
    print("# TEST SUMMARY")
    print("#"*80)
    print(f"Total Tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n✓ ALL PHASE 2 TESTS PASSED!")
    else:
        print(f"\n✗ {failed} test(s) failed")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
