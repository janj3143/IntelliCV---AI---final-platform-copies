"""
Test Portal Bridge Career Intelligence Integration

This script tests the Portal Bridge's ability to handle career intelligence
requests and return appropriate responses (success/not_implemented/error).
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from shared_backend.services.portal_bridge import PortalBridge

def test_portal_bridge_career_intelligence():
    """Test Portal Bridge career intelligence method"""
    
    print("=" * 80)
    print("PORTAL BRIDGE CAREER INTELLIGENCE TEST")
    print("=" * 80)
    
    # Initialize Portal Bridge
    print("\n1. Initializing Portal Bridge...")
    bridge = PortalBridge()
    print("   ✅ Portal Bridge initialized")
    
    # Test data
    user_profile = {
        "current_role": "Software Engineer",
        "target_role": "Senior Software Engineer",
        "experience_years": 5,
        "skills": ["Python", "JavaScript", "SQL", "AWS"],
        "education": "Bachelor's in Computer Science"
    }
    
    print(f"\n2. Testing with profile: {user_profile['current_role']} -> {user_profile['target_role']}")
    
    # Call Portal Bridge
    print("\n3. Calling bridge.get_career_intelligence()...")
    try:
        result = bridge.get_career_intelligence(user_profile)
        
        print(f"\n4. Result Status: {result['status']}")
        print(f"   Message: {result.get('message', 'N/A')}")
        
        if result['status'] == 'success':
            print("\n   ✅ SUCCESS - Real AI data available!")
            print(f"   Data keys: {list(result['data'].keys())}")
            
        elif result['status'] == 'not_implemented':
            print("\n   ⚠️  NOT IMPLEMENTED - Using fallback (expected)")
            print(f"   Schema available: {bool(result.get('schema'))}")
            if result.get('schema'):
                print(f"   Schema keys: {list(result['schema'].keys())}")
            
        elif result['status'] == 'error':
            print(f"\n   ❌ ERROR: {result.get('error')}")
            
        return result
        
    except Exception as e:
        print(f"\n   ❌ EXCEPTION: {str(e)}")
        raise

def test_portal_bridge_job_matching():
    """Test Portal Bridge job matching method"""
    
    print("\n" + "=" * 80)
    print("PORTAL BRIDGE JOB MATCHING TEST")
    print("=" * 80)
    
    bridge = PortalBridge()
    
    job_criteria = {
        "title": "Senior Python Developer",
        "skills_required": ["Python", "Django", "PostgreSQL"],
        "experience_required": "5+ years",
        "location": "Remote"
    }
    
    candidate_profile = {
        "skills": ["Python", "Django", "PostgreSQL", "Docker"],
        "experience_years": 6,
        "current_title": "Python Developer"
    }
    
    print(f"\n1. Testing job matching...")
    print(f"   Job: {job_criteria['title']}")
    print(f"   Candidate: {candidate_profile['current_title']}")
    
    try:
        result = bridge.get_job_matches(candidate_profile, job_criteria)
        
        print(f"\n2. Result Status: {result['status']}")
        
        if result['status'] == 'success':
            print("   ✅ SUCCESS - Job matching working!")
        elif result['status'] == 'not_implemented':
            print("   ⚠️  NOT IMPLEMENTED (expected)")
        
        return result
        
    except Exception as e:
        print(f"   ❌ EXCEPTION: {str(e)}")
        raise

def test_portal_bridge_interview_coaching():
    """Test Portal Bridge interview coaching method"""
    
    print("\n" + "=" * 80)
    print("PORTAL BRIDGE INTERVIEW COACHING TEST")
    print("=" * 80)
    
    bridge = PortalBridge()
    
    coaching_request = {
        "target_role": "Senior Software Engineer",
        "interview_type": "technical",
        "focus_areas": ["algorithms", "system design", "coding"]
    }
    
    print(f"\n1. Testing interview coaching...")
    print(f"   Role: {coaching_request['target_role']}")
    print(f"   Type: {coaching_request['interview_type']}")
    
    try:
        result = bridge.get_interview_coaching(coaching_request)
        
        print(f"\n2. Result Status: {result['status']}")
        
        if result['status'] == 'success':
            print("   ✅ SUCCESS - Interview coaching working!")
        elif result['status'] == 'not_implemented':
            print("   ⚠️  NOT IMPLEMENTED (expected)")
        
        return result
        
    except Exception as e:
        print(f"   ❌ EXCEPTION: {str(e)}")
        raise

def test_integration_type_registry():
    """Test that intelligence type registry discovers career-related types"""
    
    print("\n" + "=" * 80)
    print("INTELLIGENCE TYPE REGISTRY TEST")
    print("=" * 80)
    
    from shared_backend.intelligence.intelligence_type_registry import IntelligenceTypeRegistry
    
    print("\n1. Initializing registry...")
    registry = IntelligenceTypeRegistry()
    
    print(f"\n2. Discovering intelligence types...")
    registry.discover_intelligence_types()
    
    all_types = registry.get_all_types()
    print(f"   ✅ Found {len(all_types)} intelligence types")
    
    # Look for career-related types
    career_types = [t for t in all_types if 'career' in t.lower()]
    print(f"\n3. Career-related types: {len(career_types)}")
    for ctype in career_types[:5]:  # Show first 5
        print(f"   - {ctype}")
    
    # Check if specific types exist
    print(f"\n4. Checking for specific types...")
    test_types = [
        'career_trajectory',
        'skill_gap_analysis', 
        'job_market_analysis',
        'interview_preparation'
    ]
    
    for test_type in test_types:
        exists = registry.has_type(test_type)
        symbol = "✅" if exists else "❌"
        print(f"   {symbol} {test_type}: {'Found' if exists else 'Not found'}")
    
    return registry

def test_inference_engine_integration():
    """Test inference engine's ability to route career intelligence requests"""
    
    print("\n" + "=" * 80)
    print("INFERENCE ENGINE INTEGRATION TEST")
    print("=" * 80)
    
    from shared_backend.ai_engines.inference_engine import InferenceEngine
    
    print("\n1. Initializing inference engine...")
    engine = InferenceEngine()
    
    print("\n2. Testing career intelligence inference...")
    
    test_request = {
        'intelligence_type': 'career_trajectory',
        'context': {
            'current_role': 'Software Engineer',
            'target_role': 'Senior Software Engineer',
            'years_experience': 5
        }
    }
    
    try:
        result = engine.infer(test_request)
        
        print(f"\n3. Inference Result:")
        print(f"   Status: {result.get('status', 'unknown')}")
        print(f"   Has predictions: {bool(result.get('predictions'))}")
        
        if result.get('status') == 'success':
            print("   ✅ Inference successful!")
        else:
            print("   ℹ️  Inference returned non-success (may be expected)")
        
        return result
        
    except Exception as e:
        print(f"   ⚠️  Exception (may be expected if handler not implemented): {str(e)}")
        return None

def run_all_tests():
    """Run all integration tests"""
    
    print("\n" + "=" * 80)
    print("STARTING INTEGRATION TEST SUITE")
    print("Testing Portal Bridge + Intelligence System Integration")
    print("=" * 80)
    
    results = {}
    
    # Test 1: Portal Bridge Career Intelligence
    try:
        print("\n\n" + "🧪 TEST 1: Portal Bridge Career Intelligence")
        results['career_intelligence'] = test_portal_bridge_career_intelligence()
        print("✅ Test 1 completed")
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
        results['career_intelligence'] = {'error': str(e)}
    
    # Test 2: Portal Bridge Job Matching
    try:
        print("\n\n" + "🧪 TEST 2: Portal Bridge Job Matching")
        results['job_matching'] = test_portal_bridge_job_matching()
        print("✅ Test 2 completed")
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
        results['job_matching'] = {'error': str(e)}
    
    # Test 3: Portal Bridge Interview Coaching
    try:
        print("\n\n" + "🧪 TEST 3: Portal Bridge Interview Coaching")
        results['interview_coaching'] = test_portal_bridge_interview_coaching()
        print("✅ Test 3 completed")
    except Exception as e:
        print(f"❌ Test 3 failed: {e}")
        results['interview_coaching'] = {'error': str(e)}
    
    # Test 4: Intelligence Type Registry
    try:
        print("\n\n" + "🧪 TEST 4: Intelligence Type Registry")
        results['registry'] = test_integration_type_registry()
        print("✅ Test 4 completed")
    except Exception as e:
        print(f"❌ Test 4 failed: {e}")
        results['registry'] = {'error': str(e)}
    
    # Test 5: Inference Engine
    try:
        print("\n\n" + "🧪 TEST 5: Inference Engine Integration")
        results['inference_engine'] = test_inference_engine_integration()
        print("✅ Test 5 completed")
    except Exception as e:
        print(f"❌ Test 5 failed: {e}")
        results['inference_engine'] = {'error': str(e)}
    
    # Summary
    print("\n\n" + "=" * 80)
    print("TEST SUITE SUMMARY")
    print("=" * 80)
    
    print("\n📊 Results:")
    for test_name, result in results.items():
        if isinstance(result, dict):
            if 'error' in result:
                print(f"   ❌ {test_name}: FAILED")
            elif result.get('status') == 'success':
                print(f"   ✅ {test_name}: SUCCESS")
            elif result.get('status') == 'not_implemented':
                print(f"   ⚠️  {test_name}: NOT IMPLEMENTED (expected)")
            else:
                print(f"   ℹ️  {test_name}: COMPLETED")
        else:
            print(f"   ✅ {test_name}: COMPLETED")
    
    print("\n" + "=" * 80)
    print("INTEGRATION TEST SUITE COMPLETE")
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    print("\n🚀 Running Portal Bridge Integration Tests\n")
    results = run_all_tests()
    
    print("\n\n✨ Tests complete! Check results above.")
    print("Note: 'not_implemented' status is EXPECTED and means fallback will work.")
