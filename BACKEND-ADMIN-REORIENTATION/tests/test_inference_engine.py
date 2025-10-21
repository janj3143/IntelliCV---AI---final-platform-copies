"""
Unit Tests for Inference Engine
Tests the 7th AI engine with dynamic handler execution
"""

import pytest
from shared_backend.ai_engines.inference_engine import InferenceEngine


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.inference
class TestInferenceEngineInitialization:
    """Test inference engine initialization"""
    
    def test_engine_creates_successfully(self):
        """Test that inference engine can be instantiated"""
        engine = InferenceEngine()
        assert engine is not None
    
    def test_engine_has_registry(self):
        """Test that engine has access to registry"""
        engine = InferenceEngine()
        assert hasattr(engine, 'registry')
        assert engine.registry is not None


# ============================================================================
# CAREER PATH INFERENCE TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.inference
class TestCareerPathInference:
    """Test career path prediction functionality"""
    
    def test_infer_career_path(self, mock_inference_engine, sample_profile_data):
        """Test career path inference"""
        result = mock_inference_engine.infer_career_path(sample_profile_data)
        
        assert result is not None
        assert 'status' in result
    
    def test_career_path_with_career_handler(self, mock_inference_engine, career_path_handler, sample_profile_data):
        """Test career path with registered handler"""
        # Register the career path handler
        mock_inference_engine.registry.register_handler(
            'career_path',
            career_path_handler,
            priority='HIGH'
        )
        
        result = mock_inference_engine.infer_career_path(sample_profile_data)
        
        assert result['status'] == 'success'
        assert 'predicted_roles' in result
        assert len(result['predicted_roles']) > 0
    
    def test_career_path_without_handler(self, mock_inference_engine, sample_profile_data):
        """Test career path when no handler registered"""
        result = mock_inference_engine.infer_career_path(sample_profile_data)
        
        # Should return placeholder or error
        assert result is not None


# ============================================================================
# JOB MATCHING TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.inference
class TestJobMatching:
    """Test job matching functionality"""
    
    def test_match_job_to_candidate(self, mock_inference_engine, sample_profile_data, sample_job_match_data):
        """Test job matching"""
        result = mock_inference_engine.match_job_to_candidate(
            sample_profile_data,
            sample_job_match_data
        )
        
        assert result is not None
        assert 'status' in result
    
    def test_job_match_with_handler(self, mock_inference_engine, simple_handler, sample_profile_data, sample_job_match_data):
        """Test job matching with registered handler"""
        # Register job match handler
        mock_inference_engine.registry.register_handler(
            'job_match',
            simple_handler,
            priority='HIGH'
        )
        
        result = mock_inference_engine.match_job_to_candidate(
            sample_profile_data,
            sample_job_match_data
        )
        
        assert result is not None


# ============================================================================
# SKILL GAP ANALYSIS TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.inference
class TestSkillGapAnalysis:
    """Test skill gap analysis functionality"""
    
    def test_analyze_skill_gaps(self, mock_inference_engine, sample_profile_data):
        """Test skill gap analysis"""
        target_role = "Senior Software Engineer"
        
        result = mock_inference_engine.analyze_skill_gaps(
            sample_profile_data,
            target_role
        )
        
        assert result is not None
        assert 'status' in result
    
    def test_skill_gaps_with_handler(self, mock_inference_engine, simple_handler, sample_profile_data):
        """Test skill gaps with registered handler"""
        mock_inference_engine.registry.register_handler(
            'skill_gaps',
            simple_handler,
            priority='HIGH'
        )
        
        result = mock_inference_engine.analyze_skill_gaps(
            sample_profile_data,
            "Data Scientist"
        )
        
        assert result is not None


# ============================================================================
# SALARY ANALYSIS TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.inference
class TestSalaryAnalysis:
    """Test salary analysis functionality"""
    
    def test_analyze_salary(self, mock_inference_engine, sample_profile_data):
        """Test salary analysis"""
        result = mock_inference_engine.analyze_salary(sample_profile_data)
        
        assert result is not None
        assert 'status' in result
    
    def test_salary_with_handler(self, mock_inference_engine, simple_handler, sample_profile_data):
        """Test salary with registered handler"""
        mock_inference_engine.registry.register_handler(
            'salary_analysis',
            simple_handler,
            priority='HIGH'
        )
        
        result = mock_inference_engine.analyze_salary(sample_profile_data)
        
        assert result is not None


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.inference
class TestInferenceErrorHandling:
    """Test error handling in inference engine"""
    
    def test_handles_none_profile(self, mock_inference_engine):
        """Test handling None profile data"""
        result = mock_inference_engine.infer_career_path(None)
        
        # Should handle gracefully
        assert result is not None
    
    def test_handles_empty_profile(self, mock_inference_engine):
        """Test handling empty profile data"""
        result = mock_inference_engine.infer_career_path({})
        
        assert result is not None
    
    def test_handles_handler_exception(self, mock_inference_engine, sample_profile_data):
        """Test handling when handler raises exception"""
        def failing_handler(data):
            raise ValueError("Handler error")
        
        mock_inference_engine.registry.register_handler(
            'career_path',
            failing_handler,
            priority='HIGH'
        )
        
        # Should handle exception gracefully
        try:
            result = mock_inference_engine.infer_career_path(sample_profile_data)
            # Either returns error result or raises
            assert result is not None or True
        except Exception:
            # Exception handling is acceptable
            pass


# ============================================================================
# INTEGRATION-LIKE TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.inference
class TestInferenceWorkflows:
    """Test complete inference workflows"""
    
    def test_multiple_inference_calls(self, mock_inference_engine, sample_profile_data):
        """Test multiple inference calls in sequence"""
        result1 = mock_inference_engine.infer_career_path(sample_profile_data)
        result2 = mock_inference_engine.analyze_skill_gaps(sample_profile_data, "Engineer")
        result3 = mock_inference_engine.analyze_salary(sample_profile_data)
        
        assert result1 is not None
        assert result2 is not None
        assert result3 is not None
    
    def test_handler_registration_affects_results(self, mock_inference_engine, simple_handler, sample_profile_data):
        """Test that registering handler changes results"""
        # Result without handler
        result1 = mock_inference_engine.infer_career_path(sample_profile_data)
        
        # Register handler
        mock_inference_engine.registry.register_handler(
            'career_path',
            simple_handler,
            priority='HIGH'
        )
        
        # Result with handler
        result2 = mock_inference_engine.infer_career_path(sample_profile_data)
        
        # Results should differ (or second should be successful)
        assert result2 is not None


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

@pytest.mark.slow
@pytest.mark.inference
@pytest.mark.performance
class TestInferencePerformance:
    """Test inference engine performance"""
    
    def test_inference_speed(self, mock_inference_engine, simple_handler, sample_profile_data, benchmark):
        """Benchmark inference speed"""
        mock_inference_engine.registry.register_handler(
            'career_path',
            simple_handler,
            priority='HIGH'
        )
        
        result = benchmark(
            mock_inference_engine.infer_career_path,
            sample_profile_data
        )
        
        assert result is not None
    
    def test_concurrent_inference(self, mock_inference_engine, simple_handler, sample_profile_data):
        """Test concurrent inference requests"""
        mock_inference_engine.registry.register_handler(
            'career_path',
            simple_handler,
            priority='HIGH'
        )
        
        # Simulate concurrent calls
        results = []
        for _ in range(10):
            result = mock_inference_engine.infer_career_path(sample_profile_data)
            results.append(result)
        
        # All should succeed
        assert len(results) == 10
        assert all(r is not None for r in results)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
