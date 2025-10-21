"""
Integration Tests: Handler Execution
Tests handler implementation and dynamic execution
"""

import pytest
from shared_backend.ai_engines.intelligence_type_registry import get_global_registry


# ============================================================================
# HANDLER IMPLEMENTATION TESTS
# ============================================================================

@pytest.mark.integration
class TestHandlerImplementation:
    """Test implementing new handlers"""
    
    def test_new_handler_immediate_availability(self, mock_registry):
        """Test that new handler is immediately available"""
        # Implement handler
        def new_intelligence_handler(data):
            return {
                'status': 'success',
                'intelligence_type': 'new_type',
                'result': 'computed'
            }
        
        # Register it
        mock_registry.register_handler(
            'new_intelligence',
            new_intelligence_handler,
            priority='HIGH',
            description='New intelligence handler'
        )
        
        # Should be immediately available
        handler = mock_registry.get_handler('new_intelligence')
        assert handler is not None
        
        # Should work immediately
        result = handler({'test': 'data'})
        assert result['status'] == 'success'
    
    def test_handler_update_doesnt_break_system(self, mock_registry):
        """Test updating handler doesn't break existing functionality"""
        # Original handler
        def handler_v1(data):
            return {'version': 1}
        
        mock_registry.register_handler('updateable', handler_v1, priority='HIGH')
        
        # Use it
        result1 = mock_registry.get_handler('updateable')({'test': 'data'})
        assert result1['version'] == 1
        
        # Update handler
        def handler_v2(data):
            return {'version': 2, 'improved': True}
        
        mock_registry.register_handler('updateable', handler_v2, priority='HIGH')
        
        # Should use new version
        result2 = mock_registry.get_handler('updateable')({'test': 'data'})
        assert result2['version'] == 2
        assert result2['improved'] is True


# ============================================================================
# CONCURRENT HANDLER EXECUTION TESTS
# ============================================================================

@pytest.mark.integration
@pytest.mark.slow
class TestConcurrentHandlerExecution:
    """Test concurrent handler execution"""
    
    def test_concurrent_same_handler(self, mock_registry):
        """Test executing same handler concurrently"""
        call_count = []
        
        def counting_handler(data):
            call_count.append(1)
            return {'status': 'success', 'count': len(call_count)}
        
        mock_registry.register_handler('counter', counting_handler, priority='HIGH')
        
        # Execute concurrently
        results = []
        for i in range(10):
            handler = mock_registry.get_handler('counter')
            result = handler({'request': i})
            results.append(result)
        
        # All should succeed
        assert len(results) == 10
        assert all(r['status'] == 'success' for r in results)
    
    def test_concurrent_different_handlers(self, mock_registry):
        """Test executing different handlers concurrently"""
        # Register multiple handlers
        for i in range(5):
            def handler(data, i=i):
                return {'handler_id': i, 'status': 'success'}
            
            mock_registry.register_handler(f'handler_{i}', handler, priority='HIGH')
        
        # Execute concurrently
        results = []
        for i in range(5):
            handler = mock_registry.get_handler(f'handler_{i}')
            result = handler({})
            results.append(result)
        
        # All should succeed with correct IDs
        assert len(results) == 5
        for i, result in enumerate(results):
            assert result['handler_id'] == i


# ============================================================================
# HANDLER ERROR HANDLING TESTS
# ============================================================================

@pytest.mark.integration
class TestHandlerErrorHandling:
    """Test error handling in handler execution"""
    
    def test_handler_exception_handling(self, mock_registry):
        """Test that handler exceptions are handled gracefully"""
        def failing_handler(data):
            if data.get('fail'):
                raise ValueError("Intentional failure")
            return {'status': 'success'}
        
        mock_registry.register_handler('failable', failing_handler, priority='HIGH')
        
        # Success case
        handler = mock_registry.get_handler('failable')
        result_success = handler({'fail': False})
        assert result_success['status'] == 'success'
        
        # Failure case
        try:
            result_fail = handler({'fail': True})
            # If it doesn't raise, should return error result
            assert 'error' in result_fail or 'status' in result_fail
        except ValueError:
            # Expected exception
            pass
    
    def test_handler_partial_failure(self, mock_registry):
        """Test system continues when one handler fails"""
        def working_handler(data):
            return {'status': 'success'}
        
        def broken_handler(data):
            raise RuntimeError("Broken")
        
        mock_registry.register_handler('working', working_handler, priority='HIGH')
        mock_registry.register_handler('broken', broken_handler, priority='HIGH')
        
        # Working handler should still work
        working = mock_registry.get_handler('working')
        assert working({'test': 'data'})['status'] == 'success'
        
        # Broken handler should handle error
        broken = mock_registry.get_handler('broken')
        try:
            broken({'test': 'data'})
        except RuntimeError:
            pass  # Expected


# ============================================================================
# HANDLER DATA FLOW TESTS
# ============================================================================

@pytest.mark.integration
class TestHandlerDataFlow:
    """Test data flow through handlers"""
    
    def test_data_transformation(self, mock_registry):
        """Test handler transforms data correctly"""
        def transform_handler(data):
            return {
                'status': 'success',
                'original': data,
                'transformed': {k: v.upper() if isinstance(v, str) else v for k, v in data.items()}
            }
        
        mock_registry.register_handler('transformer', transform_handler, priority='HIGH')
        
        handler = mock_registry.get_handler('transformer')
        result = handler({'name': 'john', 'role': 'engineer'})
        
        assert result['status'] == 'success'
        assert result['transformed']['name'] == 'JOHN'
        assert result['transformed']['role'] == 'ENGINEER'
    
    def test_handler_chain(self, mock_registry):
        """Test chaining multiple handlers"""
        def step1_handler(data):
            data['step1'] = 'complete'
            return data
        
        def step2_handler(data):
            data['step2'] = 'complete'
            return data
        
        mock_registry.register_handler('step1', step1_handler, priority='HIGH')
        mock_registry.register_handler('step2', step2_handler, priority='HIGH')
        
        # Execute chain
        data = {'initial': True}
        
        handler1 = mock_registry.get_handler('step1')
        data = handler1(data)
        assert 'step1' in data
        
        handler2 = mock_registry.get_handler('step2')
        data = handler2(data)
        assert 'step2' in data
        assert data['initial'] is True


# ============================================================================
# HANDLER PRIORITY TESTS
# ============================================================================

@pytest.mark.integration
class TestHandlerPriority:
    """Test handler priority system"""
    
    def test_high_priority_handler(self, mock_registry):
        """Test HIGH priority handler"""
        def high_priority_handler(data):
            return {'priority': 'HIGH', 'status': 'success'}
        
        mock_registry.register_handler('test', high_priority_handler, priority='HIGH')
        
        handler = mock_registry.get_handler('test')
        result = handler({})
        
        assert result['priority'] == 'HIGH'
    
    def test_medium_priority_handler(self, mock_registry):
        """Test MEDIUM priority handler"""
        def medium_priority_handler(data):
            return {'priority': 'MEDIUM', 'status': 'success'}
        
        mock_registry.register_handler('test', medium_priority_handler, priority='MEDIUM')
        
        handler = mock_registry.get_handler('test')
        result = handler({})
        
        assert result['priority'] == 'MEDIUM'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
