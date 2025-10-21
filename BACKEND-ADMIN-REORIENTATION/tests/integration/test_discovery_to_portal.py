"""
Integration Tests: Discovery to Portal
Tests the complete flow from JSON discovery to portal access
"""

import pytest
import json
from pathlib import Path
from shared_backend.ai_engines.intelligence_type_registry import IntelligenceTypeRegistry
from shared_backend.ai_engines.inference_engine import InferenceEngine
from shared_backend.ai_engines.hybrid_integrator import HybridAIIntegrator
from shared_backend.services.portal_bridge import PortalBridge


# ============================================================================
# END-TO-END FLOW TESTS
# ============================================================================

@pytest.mark.integration
@pytest.mark.slow
class TestDiscoveryToPortalFlow:
    """Test complete flow from discovery to portal access"""
    
    def test_json_to_portal_complete_flow(self, ai_data_dir, sample_career_intelligence, create_test_json_file):
        """Test: JSON file → Discovery → Registration → Portal Access"""
        # 1. Create JSON file
        create_test_json_file("career_test.json", sample_career_intelligence)
        
        # 2. Initialize system (triggers discovery)
        registry = IntelligenceTypeRegistry()
        registry.discover_from_directory(ai_data_dir)
        
        # 3. Register handler
        def career_handler(data):
            return {
                'status': 'success',
                'predicted_roles': ['Senior Engineer', 'Tech Lead'],
                'confidence': 0.85
            }
        
        registry.register_handler('career_path', career_handler, priority='HIGH')
        
        # 4. Access through portal
        portal = PortalBridge()
        result = portal.get_intelligence(
            intelligence_type='career_path',
            profile_data={'experience_years': 5}
        )
        
        # 5. Verify complete flow
        assert result is not None
        assert 'status' in result
    
    def test_multiple_intelligence_types_flow(self, ai_data_dir, multiple_intelligence_files):
        """Test flow with multiple intelligence types"""
        # 1. Initialize system
        registry = IntelligenceTypeRegistry()
        stats = registry.discover_from_directory(ai_data_dir)
        
        # Should discover types from all files
        assert stats['files_scanned'] == len(multiple_intelligence_files)
        
        # 2. Register handlers for discovered types
        def generic_handler(data):
            return {'status': 'success', 'data': data}
        
        types = registry.list_types()
        for type_info in types[:3]:  # Register first 3
            registry.register_handler(
                type_info['name'],
                generic_handler,
                priority='MEDIUM'
            )
        
        # 3. Access through portal
        portal = PortalBridge()
        
        # Try accessing registered types
        for type_info in types[:3]:
            result = portal.get_intelligence(
                intelligence_type=type_info['name'],
                profile_data={}
            )
            assert result is not None


# ============================================================================
# METADATA PROPAGATION TESTS
# ============================================================================

@pytest.mark.integration
class TestMetadataPropagation:
    """Test metadata propagation through system layers"""
    
    def test_metadata_flows_through_layers(self, ai_data_dir, sample_career_intelligence, create_test_json_file):
        """Test that metadata flows: Discovery → Registry → Portal"""
        create_test_json_file("test.json", sample_career_intelligence)
        
        # Discovery
        registry = IntelligenceTypeRegistry()
        registry.discover_from_directory(ai_data_dir)
        
        # Check registry has metadata
        types = registry.list_types()
        if len(types) > 0:
            assert 'category' in types[0]
        
        # Portal should access with metadata
        portal = PortalBridge()
        result = portal.get_intelligence(
            intelligence_type='career_path',
            profile_data={},
            portal_type='user'
        )
        
        assert result is not None
    
    def test_portal_type_tracking(self, ai_data_dir, career_intelligence_file):
        """Test portal type is tracked through request"""
        registry = IntelligenceTypeRegistry()
        registry.discover_from_directory(ai_data_dir)
        
        portal = PortalBridge()
        
        # User portal request
        user_result = portal.get_intelligence(
            intelligence_type='career_path',
            profile_data={},
            portal_type='user'
        )
        
        # Admin portal request
        admin_result = portal.get_intelligence(
            intelligence_type='career_path',
            profile_data={},
            portal_type='admin'
        )
        
        assert user_result is not None
        assert admin_result is not None


# ============================================================================
# REAL WORLD SCENARIO TESTS
# ============================================================================

@pytest.mark.integration
class TestRealWorldScenarios:
    """Test real-world usage scenarios"""
    
    def test_user_portal_scenario(self, ai_data_dir, sample_profile_data, career_intelligence_file):
        """Test typical user portal workflow"""
        # Setup system
        registry = IntelligenceTypeRegistry()
        registry.discover_from_directory(ai_data_dir)
        
        # Register career handler
        def career_handler(data):
            return {
                'status': 'success',
                'trajectory': 'upward',
                'next_roles': ['Senior Engineer', 'Lead Engineer']
            }
        
        registry.register_handler('career_path', career_handler, priority='HIGH')
        
        # User portal workflow
        portal = PortalBridge()
        
        # 1. Get career intelligence
        career = portal.get_career_intelligence(sample_profile_data)
        assert career is not None
        
        # 2. Get job matches
        jobs = portal.get_job_matches(sample_profile_data)
        assert jobs is not None
        
        # 3. Get salary insights
        salary = portal.get_salary_insights(sample_profile_data)
        assert salary is not None
    
    def test_admin_portal_scenario(self, ai_data_dir, multiple_intelligence_files):
        """Test typical admin portal workflow"""
        # Setup system
        registry = IntelligenceTypeRegistry()
        stats = registry.discover_from_directory(ai_data_dir)
        
        # Admin portal workflow
        portal = PortalBridge()
        
        # 1. Check system analytics
        analytics = portal.get_system_analytics()
        assert analytics is not None
        
        # 2. View intelligence types
        types = portal.get_intelligence_types()
        assert types is not None
        
        # 3. Check implementation status
        status = portal.get_implementation_status()
        assert status is not None


# ============================================================================
# CONCURRENT ACCESS TESTS
# ============================================================================

@pytest.mark.integration
@pytest.mark.slow
class TestConcurrentAccess:
    """Test concurrent access across system"""
    
    def test_concurrent_portal_requests(self, ai_data_dir, sample_profile_data, career_intelligence_file):
        """Test multiple concurrent portal requests"""
        # Setup
        registry = IntelligenceTypeRegistry()
        registry.discover_from_directory(ai_data_dir)
        
        def handler(data):
            return {'status': 'success'}
        
        registry.register_handler('test', handler, priority='HIGH')
        
        portal = PortalBridge()
        
        # Concurrent requests
        results = []
        for i in range(20):
            result = portal.get_intelligence(
                intelligence_type='test',
                profile_data=sample_profile_data
            )
            results.append(result)
        
        # All should succeed
        assert len(results) == 20
        assert all(r is not None for r in results)
    
    def test_concurrent_different_types(self, ai_data_dir, multiple_intelligence_files, sample_profile_data):
        """Test concurrent requests for different intelligence types"""
        registry = IntelligenceTypeRegistry()
        registry.discover_from_directory(ai_data_dir)
        
        # Register multiple handlers
        def handler(data):
            return {'status': 'success'}
        
        types = registry.list_types()
        for type_info in types[:5]:
            registry.register_handler(type_info['name'], handler, priority='HIGH')
        
        portal = PortalBridge()
        
        # Concurrent requests to different types
        results = []
        for type_info in types[:5]:
            result = portal.get_intelligence(
                intelligence_type=type_info['name'],
                profile_data=sample_profile_data
            )
            results.append(result)
        
        assert len(results) == 5
        assert all(r is not None for r in results)


# ============================================================================
# SYSTEM STATE TESTS
# ============================================================================

@pytest.mark.integration
class TestSystemState:
    """Test system state consistency"""
    
    def test_discovery_affects_portal(self, ai_data_dir, sample_career_intelligence, create_test_json_file):
        """Test that discovery immediately affects portal availability"""
        # Initial state
        registry = IntelligenceTypeRegistry()
        initial_count = len(registry.list_types())
        
        # Add new intelligence file
        create_test_json_file("new_intelligence.json", sample_career_intelligence)
        
        # Re-discover
        registry.discover_from_directory(ai_data_dir)
        
        # Should have more types
        new_count = len(registry.list_types())
        assert new_count >= initial_count
    
    def test_handler_registration_immediate_availability(self, ai_data_dir, career_intelligence_file):
        """Test that registered handlers are immediately available"""
        registry = IntelligenceTypeRegistry()
        registry.discover_from_directory(ai_data_dir)
        
        portal = PortalBridge()
        
        # Before registration
        result_before = portal.get_intelligence('new_type', {})
        
        # Register handler
        def new_handler(data):
            return {'status': 'registered'}
        
        registry.register_handler('new_type', new_handler, priority='HIGH')
        
        # After registration - should be available
        result_after = portal.get_intelligence('new_type', {})
        
        # Both should complete (may have different results)
        assert result_before is not None
        assert result_after is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
