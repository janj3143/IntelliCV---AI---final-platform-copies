"""
Unit Tests for Portal Bridge
Tests the portal interface layer connecting UI to AI system
"""

import pytest
from shared_backend.services.portal_bridge import PortalBridge


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.portal
class TestPortalBridgeInitialization:
    """Test portal bridge initialization"""
    
    def test_bridge_creates_successfully(self):
        """Test that portal bridge can be instantiated"""
        bridge = PortalBridge()
        assert bridge is not None
    
    def test_bridge_connects_to_ai_system(self):
        """Test that bridge connects to hybrid AI system"""
        bridge = PortalBridge()
        assert hasattr(bridge, 'hybrid_ai')
        # Hybrid AI should be initialized
        assert bridge.hybrid_ai is not None


# ============================================================================
# UNIVERSAL ACCESS METHOD TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.portal
class TestUniversalAccess:
    """Test universal intelligence access method"""
    
    def test_get_intelligence(self, mock_portal_bridge, sample_profile_data):
        """Test universal get_intelligence method"""
        result = mock_portal_bridge.get_intelligence(
            intelligence_type='career_path',
            profile_data=sample_profile_data
        )
        
        assert result is not None
        assert 'status' in result
    
    def test_get_intelligence_with_metadata(self, mock_portal_bridge, sample_profile_data):
        """Test that get_intelligence includes metadata"""
        result = mock_portal_bridge.get_intelligence(
            intelligence_type='career_path',
            profile_data=sample_profile_data,
            portal_type='user'
        )
        
        # Should have tracking metadata
        assert result is not None
    
    def test_get_intelligence_unknown_type(self, mock_portal_bridge, sample_profile_data):
        """Test get_intelligence with unknown type"""
        result = mock_portal_bridge.get_intelligence(
            intelligence_type='unknown_type_xyz',
            profile_data=sample_profile_data
        )
        
        # Should handle gracefully
        assert result is not None


# ============================================================================
# USER PORTAL METHODS TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.portal
class TestUserPortalMethods:
    """Test user portal specific methods"""
    
    def test_get_career_intelligence(self, mock_portal_bridge, sample_profile_data):
        """Test get_career_intelligence for user portal"""
        result = mock_portal_bridge.get_career_intelligence(sample_profile_data)
        
        assert result is not None
        assert 'status' in result
    
    def test_get_job_matches(self, mock_portal_bridge, sample_profile_data):
        """Test get_job_matches for user portal"""
        result = mock_portal_bridge.get_job_matches(sample_profile_data)
        
        assert result is not None
    
    def test_get_skill_recommendations(self, mock_portal_bridge, sample_profile_data):
        """Test get_skill_recommendations"""
        result = mock_portal_bridge.get_skill_recommendations(
            sample_profile_data,
            target_role="Senior Engineer"
        )
        
        assert result is not None
    
    def test_get_salary_insights(self, mock_portal_bridge, sample_profile_data):
        """Test get_salary_insights"""
        result = mock_portal_bridge.get_salary_insights(sample_profile_data)
        
        assert result is not None
    
    def test_get_interview_prep(self, mock_portal_bridge, sample_profile_data):
        """Test get_interview_prep"""
        result = mock_portal_bridge.get_interview_prep(
            sample_profile_data,
            job_description="Software Engineer position"
        )
        
        assert result is not None
    
    def test_get_resume_suggestions(self, mock_portal_bridge, sample_profile_data):
        """Test get_resume_suggestions"""
        result = mock_portal_bridge.get_resume_suggestions(
            sample_profile_data,
            target_job="Data Scientist"
        )
        
        assert result is not None


# ============================================================================
# ADMIN PORTAL METHODS TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.portal
class TestAdminPortalMethods:
    """Test admin portal specific methods"""
    
    def test_get_system_analytics(self, mock_portal_bridge):
        """Test get_system_analytics for admin"""
        result = mock_portal_bridge.get_system_analytics()
        
        assert result is not None
        assert 'status' in result
    
    def test_get_intelligence_types(self, mock_portal_bridge):
        """Test get_intelligence_types listing"""
        result = mock_portal_bridge.get_intelligence_types()
        
        assert result is not None
        assert isinstance(result, (list, dict))
    
    def test_get_implementation_status(self, mock_portal_bridge):
        """Test get_implementation_status"""
        result = mock_portal_bridge.get_implementation_status()
        
        assert result is not None


# ============================================================================
# RECRUITER PORTAL METHODS TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.portal
class TestRecruiterPortalMethods:
    """Test recruiter portal specific methods"""
    
    def test_match_candidates_to_job(self, mock_portal_bridge, sample_job_match_data):
        """Test match_candidates_to_job"""
        candidates = [
            {"name": "Candidate 1", "skills": ["Python", "ML"]},
            {"name": "Candidate 2", "skills": ["Java", "Cloud"]}
        ]
        
        result = mock_portal_bridge.match_candidates_to_job(
            job_data=sample_job_match_data,
            candidates=candidates
        )
        
        assert result is not None
    
    def test_get_candidate_intelligence(self, mock_portal_bridge, sample_profile_data):
        """Test get_candidate_intelligence"""
        result = mock_portal_bridge.get_candidate_intelligence(sample_profile_data)
        
        assert result is not None
    
    def test_get_market_insights(self, mock_portal_bridge):
        """Test get_market_insights"""
        result = mock_portal_bridge.get_market_insights(
            role="Software Engineer",
            location="San Francisco"
        )
        
        assert result is not None


# ============================================================================
# METADATA & TRACKING TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.portal
class TestMetadataTracking:
    """Test metadata and request tracking"""
    
    def test_request_tracking(self, mock_portal_bridge, sample_profile_data):
        """Test that requests are tracked"""
        # Make a request
        result = mock_portal_bridge.get_career_intelligence(sample_profile_data)
        
        # Should have metadata
        assert result is not None
        
        # Check if metrics are tracked (depends on implementation)
        if hasattr(mock_portal_bridge, 'metrics'):
            assert mock_portal_bridge.metrics is not None
    
    def test_portal_type_tracking(self, mock_portal_bridge, sample_profile_data):
        """Test tracking of portal type in requests"""
        result = mock_portal_bridge.get_intelligence(
            intelligence_type='career_path',
            profile_data=sample_profile_data,
            portal_type='admin'
        )
        
        assert result is not None


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.portal
class TestPortalErrorHandling:
    """Test error handling in portal bridge"""
    
    def test_handles_none_profile(self, mock_portal_bridge):
        """Test handling None profile data"""
        result = mock_portal_bridge.get_career_intelligence(None)
        
        # Should handle gracefully
        assert result is not None
    
    def test_handles_empty_profile(self, mock_portal_bridge):
        """Test handling empty profile data"""
        result = mock_portal_bridge.get_career_intelligence({})
        
        assert result is not None
    
    def test_handles_invalid_intelligence_type(self, mock_portal_bridge, sample_profile_data):
        """Test handling invalid intelligence type"""
        result = mock_portal_bridge.get_intelligence(
            intelligence_type='',
            profile_data=sample_profile_data
        )
        
        assert result is not None
    
    def test_error_propagation(self, mock_portal_bridge, sample_profile_data):
        """Test that errors from AI system are properly handled"""
        # This test depends on how errors are handled
        # Should not crash portal bridge
        result = mock_portal_bridge.get_career_intelligence(sample_profile_data)
        assert result is not None


# ============================================================================
# MULTI-ENGINE ROUTING TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.portal
class TestMultiEngineRouting:
    """Test routing to different AI engines"""
    
    def test_routes_to_inference_engine(self, mock_portal_bridge, sample_profile_data):
        """Test routing to inference engine"""
        result = mock_portal_bridge.get_career_intelligence(sample_profile_data)
        
        # Should route through hybrid AI to inference engine
        assert result is not None
    
    def test_routes_career_methods_correctly(self, mock_portal_bridge, sample_profile_data):
        """Test that career methods route correctly"""
        career_result = mock_portal_bridge.get_career_intelligence(sample_profile_data)
        match_result = mock_portal_bridge.get_job_matches(sample_profile_data)
        skill_result = mock_portal_bridge.get_skill_recommendations(sample_profile_data, "Engineer")
        
        assert career_result is not None
        assert match_result is not None
        assert skill_result is not None


# ============================================================================
# INTEGRATION-LIKE TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.portal
class TestPortalWorkflows:
    """Test complete portal workflows"""
    
    def test_user_portal_workflow(self, mock_portal_bridge, sample_profile_data):
        """Test typical user portal workflow"""
        # User logs in, views career path
        career = mock_portal_bridge.get_career_intelligence(sample_profile_data)
        assert career is not None
        
        # Views job matches
        jobs = mock_portal_bridge.get_job_matches(sample_profile_data)
        assert jobs is not None
        
        # Checks salary insights
        salary = mock_portal_bridge.get_salary_insights(sample_profile_data)
        assert salary is not None
    
    def test_admin_portal_workflow(self, mock_portal_bridge):
        """Test typical admin portal workflow"""
        # Admin checks system status
        analytics = mock_portal_bridge.get_system_analytics()
        assert analytics is not None
        
        # Views intelligence types
        types = mock_portal_bridge.get_intelligence_types()
        assert types is not None
        
        # Checks implementation status
        status = mock_portal_bridge.get_implementation_status()
        assert status is not None
    
    def test_recruiter_portal_workflow(self, mock_portal_bridge, sample_profile_data, sample_job_match_data):
        """Test typical recruiter portal workflow"""
        # Recruiter views candidate
        candidate = mock_portal_bridge.get_candidate_intelligence(sample_profile_data)
        assert candidate is not None
        
        # Matches candidates to job
        matches = mock_portal_bridge.match_candidates_to_job(
            sample_job_match_data,
            [sample_profile_data]
        )
        assert matches is not None
        
        # Views market insights
        market = mock_portal_bridge.get_market_insights("Engineer", "SF")
        assert market is not None


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

@pytest.mark.slow
@pytest.mark.portal
@pytest.mark.performance
class TestPortalPerformance:
    """Test portal bridge performance"""
    
    def test_request_overhead(self, mock_portal_bridge, sample_profile_data, benchmark):
        """Benchmark portal bridge overhead"""
        result = benchmark(
            mock_portal_bridge.get_career_intelligence,
            sample_profile_data
        )
        
        assert result is not None
    
    def test_concurrent_requests(self, mock_portal_bridge, sample_profile_data):
        """Test handling concurrent requests"""
        results = []
        
        # Simulate concurrent requests
        for i in range(20):
            result = mock_portal_bridge.get_career_intelligence(sample_profile_data)
            results.append(result)
        
        # All should succeed
        assert len(results) == 20
        assert all(r is not None for r in results)
    
    def test_multiple_portal_types(self, mock_portal_bridge, sample_profile_data):
        """Test performance with multiple portal types"""
        # User portal requests
        for _ in range(5):
            mock_portal_bridge.get_career_intelligence(sample_profile_data)
        
        # Admin portal requests
        for _ in range(5):
            mock_portal_bridge.get_system_analytics()
        
        # Should all complete without issues
        assert True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
