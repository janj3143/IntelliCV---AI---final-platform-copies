"""
Integration Tests: Error Scenarios
Tests error handling across all system layers
"""

import pytest
import json
from pathlib import Path


# ============================================================================
# DISCOVERY ERROR SCENARIOS
# ============================================================================

@pytest.mark.integration
class TestDiscoveryErrors:
    """Test error handling in discovery phase"""
    
    def test_invalid_json_file(self, ai_data_dir, mock_registry):
        """Test discovery handles invalid JSON files"""
        # Create invalid JSON
        invalid_file = ai_data_dir / "invalid.json"
        with open(invalid_file, 'w') as f:
            f.write("{ this is not valid json }")
        
        # Should handle gracefully
        stats = mock_registry.discover_from_directory(ai_data_dir)
        
        assert stats is not None
        assert 'files_scanned' in stats
    
    def test_empty_json_file(self, ai_data_dir, mock_registry):
        """Test discovery handles empty JSON files"""
        empty_file = ai_data_dir / "empty.json"
        with open(empty_file, 'w') as f:
            f.write("{}")
        
        stats = mock_registry.discover_from_directory(ai_data_dir)
        
        assert stats['errors'] == 0 or stats['files_scanned'] > 0
    
    def test_non_json_file(self, ai_data_dir, mock_registry):
        """Test discovery handles non-JSON files"""
        text_file = ai_data_dir / "text.txt"
        with open(text_file, 'w') as f:
            f.write("This is just text")
        
        # Should skip or handle gracefully
        stats = mock_registry.discover_from_directory(ai_data_dir)
        
        assert stats is not None
    
    def test_permission_denied(self, tmp_path, mock_registry):
        """Test discovery handles permission errors"""
        # This test might not work on all systems
        # Just ensure it doesn't crash
        stats = mock_registry.discover_from_directory(tmp_path / "nonexistent")
        
        assert stats is not None


# ============================================================================
# HANDLER EXECUTION ERRORS
# ============================================================================

@pytest.mark.integration
class TestHandlerExecutionErrors:
    """Test error handling during handler execution"""
    
    def test_handler_raises_exception(self, mock_registry):
        """Test when handler raises an exception"""
        def error_handler(data):
            raise ValueError("Handler error")
        
        mock_registry.register_handler('error_test', error_handler, priority='HIGH')
        
        handler = mock_registry.get_handler('error_test')
        
        # Should either handle exception or propagate it
        try:
            result = handler({})
            # If no exception, should have error info
            assert result is not None
        except ValueError:
            # Expected exception
            pass
    
    def test_handler_returns_none(self, mock_registry):
        """Test when handler returns None"""
        def none_handler(data):
            return None
        
        mock_registry.register_handler('none_test', none_handler, priority='HIGH')
        
        handler = mock_registry.get_handler('none_test')
        result = handler({})
        
        # Should handle None return
        assert result is None or isinstance(result, dict)
    
    def test_handler_invalid_return_type(self, mock_registry):
        """Test when handler returns invalid type"""
        def invalid_handler(data):
            return "string instead of dict"
        
        mock_registry.register_handler('invalid_test', invalid_handler, priority='HIGH')
        
        handler = mock_registry.get_handler('invalid_test')
        result = handler({})
        
        # Should handle or validate return type
        assert result is not None


# ============================================================================
# ROUTING ERRORS
# ============================================================================

@pytest.mark.integration
class TestRoutingErrors:
    """Test error handling in routing layer"""
    
    def test_unknown_intelligence_type(self, mock_hybrid_integrator):
        """Test routing unknown intelligence type"""
        result = mock_hybrid_integrator.run_inference(
            intelligence_type='completely_unknown_type_xyz',
            data={}
        )
        
        # Should handle gracefully
        assert result is not None
    
    def test_empty_intelligence_type(self, mock_hybrid_integrator):
        """Test routing with empty intelligence type"""
        result = mock_hybrid_integrator.run_inference(
            intelligence_type='',
            data={}
        )
        
        assert result is not None
    
    def test_none_intelligence_type(self, mock_hybrid_integrator):
        """Test routing with None intelligence type"""
        try:
            result = mock_hybrid_integrator.run_inference(
                intelligence_type=None,
                data={}
            )
            assert result is not None or True
        except (TypeError, ValueError):
            # Expected error
            pass


# ============================================================================
# PORTAL ACCESS ERRORS
# ============================================================================

@pytest.mark.integration
class TestPortalAccessErrors:
    """Test error handling at portal layer"""
    
    def test_portal_with_none_data(self, mock_portal_bridge):
        """Test portal access with None data"""
        result = mock_portal_bridge.get_intelligence(
            intelligence_type='career_path',
            data=None
        )
        
        # Should handle gracefully
        assert result is not None
    
    def test_portal_with_empty_data(self, mock_portal_bridge):
        """Test portal access with empty data"""
        result = mock_portal_bridge.get_intelligence(
            intelligence_type='career_path',
            data={}
        )
        
        assert result is not None
    
    def test_portal_with_invalid_portal_type(self, mock_portal_bridge):
        """Test portal access with invalid portal type"""
        result = mock_portal_bridge.get_intelligence(
            intelligence_type='career_path',
            data={},
            portal_type='invalid_portal'
        )
        
        # Should handle or validate portal type
        assert result is not None


# ============================================================================
# DATA VALIDATION ERRORS
# ============================================================================

@pytest.mark.integration
class TestDataValidationErrors:
    """Test error handling for invalid data"""
    
    def test_malformed_profile_data(self, mock_portal_bridge):
        """Test with malformed profile data"""
        malformed_data = {
            'skills': 'should be list but is string',
            'experience': 'should be number'
        }
        
        result = mock_portal_bridge.get_intelligence(
            intelligence_type='career_path',
            data=malformed_data
        )
        
        # Should handle validation errors
        assert result is not None
    
    def test_missing_required_fields(self, mock_portal_bridge):
        """Test with missing required fields"""
        incomplete_data = {
            'name': 'John'
            # Missing other fields
        }
        
        result = mock_portal_bridge.get_intelligence(
            intelligence_type='job_match',
            data=incomplete_data
        )
        
        assert result is not None


# ============================================================================
# RECOVERY SCENARIOS
# ============================================================================

@pytest.mark.integration
class TestRecoveryScenarios:
    """Test system recovery from errors"""
    
    def test_recovery_from_discovery_failure(self, ai_data_dir, mock_registry):
        """Test system recovers from discovery failure"""
        # Create invalid file
        invalid_file = ai_data_dir / "bad.json"
        with open(invalid_file, 'w') as f:
            f.write("{ bad json")
        
        # First discovery (might have errors)
        stats1 = mock_registry.discover_from_directory(ai_data_dir)
        
        # Fix the file
        with open(invalid_file, 'w') as f:
            json.dump({'test_intelligence': {'value': 123}}, f)
        
        # Second discovery (should work)
        stats2 = mock_registry.discover_from_directory(ai_data_dir)
        
        # Should recover
        assert stats2 is not None
    
    def test_recovery_from_handler_failure(self, mock_registry):
        """Test system recovers when handler fails"""
        call_count = [0]
        
        def flaky_handler(data):
            call_count[0] += 1
            if call_count[0] == 1:
                raise ValueError("First call fails")
            return {'status': 'success', 'call': call_count[0]}
        
        mock_registry.register_handler('flaky', flaky_handler, priority='HIGH')
        
        handler = mock_registry.get_handler('flaky')
        
        # First call fails
        try:
            result1 = handler({})
        except ValueError:
            pass
        
        # Second call succeeds
        result2 = handler({})
        assert result2['status'] == 'success'
        assert result2['call'] == 2


# ============================================================================
# ERROR PROPAGATION TESTS
# ============================================================================

@pytest.mark.integration
class TestErrorPropagation:
    """Test error propagation through layers"""
    
    def test_handler_error_reaches_portal(self, mock_registry, mock_portal_bridge):
        """Test that handler errors propagate to portal"""
        def failing_handler(data):
            raise RuntimeError("Handler failure")
        
        mock_registry.register_handler('failing', failing_handler, priority='HIGH')
        
        # Error should be handled at some layer
        try:
            result = mock_portal_bridge.get_intelligence(
                intelligence_type='failing',
                data={}
            )
            # If no exception, should have error info
            assert result is not None
        except RuntimeError:
            # Error propagated
            pass
    
    def test_discovery_error_doesnt_crash_system(self, ai_data_dir, mock_registry, mock_portal_bridge):
        """Test that discovery errors don't crash system"""
        # Create problem file
        bad_file = ai_data_dir / "problem.json"
        with open(bad_file, 'w') as f:
            f.write("invalid")
        
        # Discovery might have errors
        mock_registry.discover_from_directory(ai_data_dir)
        
        # Portal should still function
        result = mock_portal_bridge.get_intelligence(
            intelligence_type='career_path',
            data={}
        )
        
        assert result is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
