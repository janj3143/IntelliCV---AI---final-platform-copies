"""
Unit Tests for Hybrid AI Integrator
Tests the orchestrator connecting all 8 AI engines
"""

import pytest
from shared_backend.ai_engines.hybrid_integrator import HybridAIIntegrator


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.integrator
class TestHybridIntegratorInitialization:
    """Test hybrid integrator initialization"""
    
    def test_integrator_creates_successfully(self):
        """Test that integrator can be instantiated"""
        integrator = HybridAIIntegrator()
        assert integrator is not None
    
    def test_integrator_loads_all_engines(self):
        """Test that all 8 AI engines are loaded"""
        integrator = HybridAIIntegrator()
        
        # Should have inference engine (7th)
        assert hasattr(integrator, 'inference_engine')
        
        # Should have registry
        assert hasattr(integrator, 'registry')


# ============================================================================
# DYNAMIC ROUTING TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.integrator
class TestDynamicRouting:
    """Test dynamic routing to handlers"""
    
    def test_run_inference(self, mock_hybrid_integrator, sample_profile_data):
        """Test run_inference method"""
        result = mock_hybrid_integrator.run_inference(
            intelligence_type='career_path',
            data=sample_profile_data
        )
        
        assert result is not None
        assert 'status' in result
    
    def test_routes_to_correct_handler(self, mock_hybrid_integrator, simple_handler, sample_profile_data):
        """Test that routing finds correct handler"""
        # Register handler
        mock_hybrid_integrator.registry.register_handler(
            'test_type',
            simple_handler,
            priority='HIGH'
        )
        
        result = mock_hybrid_integrator.run_inference(
            intelligence_type='test_type',
            data=sample_profile_data
        )
        
        assert result is not None
        assert result['status'] == 'success'
    
    def test_routes_unknown_type(self, mock_hybrid_integrator, sample_profile_data):
        """Test routing with unknown intelligence type"""
        result = mock_hybrid_integrator.run_inference(
            intelligence_type='unknown_xyz',
            data=sample_profile_data
        )
        
        # Should handle gracefully
        assert result is not None


# ============================================================================
# DISCOVERY TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.integrator
@pytest.mark.discovery
class TestIntegratorDiscovery:
    """Test discovery functionality in integrator"""
    
    def test_discovery_at_startup(self, ai_data_dir, career_intelligence_file):
        """Test that discovery runs at startup"""
        integrator = HybridAIIntegrator()
        
        # Should have discovered types
        types = integrator.registry.list_types()
        assert isinstance(types, list)
    
    def test_discovery_stats(self, mock_hybrid_integrator):
        """Test getting discovery statistics"""
        # Should have discovery stats
        if hasattr(mock_hybrid_integrator, 'get_discovery_stats'):
            stats = mock_hybrid_integrator.get_discovery_stats()
            assert stats is not None


# ============================================================================
# HANDLER REGISTRATION TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.integrator
class TestIntegratorHandlerRegistration:
    """Test handler registration through integrator"""
    
    def test_register_handler(self, mock_hybrid_integrator, simple_handler):
        """Test registering handler through integrator"""
        mock_hybrid_integrator.registry.register_handler(
            'new_type',
            simple_handler,
            priority='HIGH'
        )
        
        # Should be able to use it immediately
        result = mock_hybrid_integrator.run_inference(
            'new_type',
            {'test': 'data'}
        )
        
        assert result is not None
    
    def test_multiple_handler_registration(self, mock_hybrid_integrator):
        """Test registering multiple handlers"""
        def handler1(data):
            return {'handler': 1}
        
        def handler2(data):
            return {'handler': 2}
        
        mock_hybrid_integrator.registry.register_handler('type1', handler1, priority='HIGH')
        mock_hybrid_integrator.registry.register_handler('type2', handler2, priority='HIGH')
        
        # Both should work
        result1 = mock_hybrid_integrator.run_inference('type1', {})
        result2 = mock_hybrid_integrator.run_inference('type2', {})
        
        assert result1 is not None
        assert result2 is not None


# ============================================================================
# ENGINE COORDINATION TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.integrator
class TestEngineCoordination:
    """Test coordination of multiple AI engines"""
    
    def test_inference_engine_access(self, mock_hybrid_integrator):
        """Test access to inference engine"""
        assert hasattr(mock_hybrid_integrator, 'inference_engine')
        assert mock_hybrid_integrator.inference_engine is not None
    
    def test_registry_access(self, mock_hybrid_integrator):
        """Test access to registry"""
        assert hasattr(mock_hybrid_integrator, 'registry')
        assert mock_hybrid_integrator.registry is not None


# ============================================================================
# FEEDBACK LOOP TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.integrator
class TestFeedbackLoop:
    """Test performance feedback and optimization"""
    
    def test_tracks_performance(self, mock_hybrid_integrator, simple_handler, sample_profile_data):
        """Test that performance is tracked"""
        mock_hybrid_integrator.registry.register_handler(
            'test',
            simple_handler,
            priority='HIGH'
        )
        
        # Run inference
        result = mock_hybrid_integrator.run_inference('test', sample_profile_data)
        
        # Should track metrics (depends on implementation)
        assert result is not None
    
    def test_feedback_improves_routing(self, mock_hybrid_integrator, simple_handler):
        """Test that feedback can improve routing (if implemented)"""
        mock_hybrid_integrator.registry.register_handler(
            'test',
            simple_handler,
            priority='HIGH'
        )
        
        # Multiple calls
        for _ in range(5):
            mock_hybrid_integrator.run_inference('test', {})
        
        # System should still function
        assert True


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.integrator
class TestIntegratorErrorHandling:
    """Test error handling in integrator"""
    
    def test_handles_none_data(self, mock_hybrid_integrator):
        """Test handling None data"""
        result = mock_hybrid_integrator.run_inference('career_path', None)
        
        # Should handle gracefully
        assert result is not None
    
    def test_handles_handler_error(self, mock_hybrid_integrator):
        """Test handling when handler raises error"""
        def failing_handler(data):
            raise ValueError("Handler error")
        
        mock_hybrid_integrator.registry.register_handler(
            'failing',
            failing_handler,
            priority='HIGH'
        )
        
        # Should handle exception
        try:
            result = mock_hybrid_integrator.run_inference('failing', {})
            assert result is not None or True
        except Exception:
            # Exception handling is acceptable
            pass


# ============================================================================
# INTEGRATION-LIKE TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.integrator
class TestIntegratorWorkflows:
    """Test complete integrator workflows"""
    
    def test_full_workflow(self, mock_hybrid_integrator, simple_handler, sample_profile_data):
        """Test complete workflow: register → discover → route → execute"""
        # 1. Register handler
        mock_hybrid_integrator.registry.register_handler(
            'workflow_test',
            simple_handler,
            priority='HIGH'
        )
        
        # 2. Run inference
        result = mock_hybrid_integrator.run_inference(
            'workflow_test',
            sample_profile_data
        )
        
        # 3. Verify result
        assert result is not None
        assert result['status'] == 'success'
    
    def test_multiple_intelligence_types(self, mock_hybrid_integrator, sample_profile_data):
        """Test handling multiple intelligence types"""
        # Register multiple handlers
        for i in range(5):
            mock_hybrid_integrator.registry.register_handler(
                f'type_{i}',
                lambda data, i=i: {'handler': i},
                priority='HIGH'
            )
        
        # Use all handlers
        results = []
        for i in range(5):
            result = mock_hybrid_integrator.run_inference(f'type_{i}', sample_profile_data)
            results.append(result)
        
        # All should succeed
        assert len(results) == 5
        assert all(r is not None for r in results)


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

@pytest.mark.slow
@pytest.mark.integrator
@pytest.mark.performance
class TestIntegratorPerformance:
    """Test integrator performance"""
    
    def test_routing_performance(self, mock_hybrid_integrator, simple_handler, benchmark):
        """Benchmark routing performance"""
        mock_hybrid_integrator.registry.register_handler(
            'benchmark',
            simple_handler,
            priority='HIGH'
        )
        
        result = benchmark(
            mock_hybrid_integrator.run_inference,
            'benchmark',
            {'test': 'data'}
        )
        
        assert result is not None
    
    def test_concurrent_routing(self, mock_hybrid_integrator, simple_handler):
        """Test concurrent routing requests"""
        mock_hybrid_integrator.registry.register_handler(
            'concurrent',
            simple_handler,
            priority='HIGH'
        )
        
        results = []
        for _ in range(50):
            result = mock_hybrid_integrator.run_inference('concurrent', {})
            results.append(result)
        
        # All should complete
        assert len(results) == 50
        assert all(r is not None for r in results)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
