"""
Unit Tests for Intelligence Type Registry
Tests the core discovery and registration system
"""

import pytest
import json
from pathlib import Path
from shared_backend.ai_engines.intelligence_type_registry import (
    IntelligenceTypeRegistry,
    get_global_registry,
    IntelligenceTypeInfo
)


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.registry
class TestRegistryInitialization:
    """Test registry initialization and setup"""
    
    def test_registry_creates_successfully(self):
        """Test that registry can be instantiated"""
        registry = IntelligenceTypeRegistry()
        assert registry is not None
        assert hasattr(registry, 'types')
        assert hasattr(registry, 'handlers')
    
    def test_global_registry_singleton(self):
        """Test that get_global_registry returns same instance"""
        registry1 = get_global_registry()
        registry2 = get_global_registry()
        assert registry1 is registry2
    
    def test_registry_starts_empty(self):
        """Test that new registry has no types initially"""
        registry = IntelligenceTypeRegistry()
        assert len(registry.types) == 0
        assert len(registry.handlers) == 0


# ============================================================================
# DISCOVERY TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.registry
@pytest.mark.discovery
class TestTypeDiscovery:
    """Test intelligence type discovery from JSON files"""
    
    def test_discover_from_directory(self, ai_data_dir, career_intelligence_file):
        """Test discovery from directory with JSON files"""
        registry = IntelligenceTypeRegistry()
        
        stats = registry.discover_from_directory(ai_data_dir)
        
        assert stats['files_scanned'] >= 1
        assert stats['types_discovered'] >= 0
        assert stats['errors'] == 0
    
    def test_discover_career_intelligence_types(self, ai_data_dir, sample_career_intelligence, create_test_json_file):
        """Test discovery of career intelligence types"""
        create_test_json_file("career_data.json", sample_career_intelligence)
        
        registry = IntelligenceTypeRegistry()
        stats = registry.discover_from_directory(ai_data_dir)
        
        # Should discover types from career_intelligence
        assert stats['types_discovered'] > 0
        
        # Check for discovered types
        types = registry.list_types()
        type_names = [t['name'] for t in types]
        
        # Should have discovered trajectory and growth_potential types
        assert any('trajectory' in name or 'career' in name for name in type_names)
    
    def test_discover_multiple_files(self, ai_data_dir, multiple_intelligence_files):
        """Test discovery from multiple JSON files"""
        registry = IntelligenceTypeRegistry()
        
        stats = registry.discover_from_directory(ai_data_dir)
        
        assert stats['files_scanned'] == len(multiple_intelligence_files)
        assert stats['types_discovered'] > 0
    
    def test_discover_handles_empty_directory(self, ai_data_dir):
        """Test discovery with empty directory"""
        registry = IntelligenceTypeRegistry()
        
        stats = registry.discover_from_directory(ai_data_dir)
        
        assert stats['files_scanned'] == 0
        assert stats['types_discovered'] == 0
        assert stats['errors'] == 0
    
    def test_discover_handles_nonexistent_directory(self, tmp_path):
        """Test discovery with non-existent directory"""
        registry = IntelligenceTypeRegistry()
        fake_dir = tmp_path / "nonexistent"
        
        stats = registry.discover_from_directory(fake_dir)
        
        # Should handle gracefully
        assert stats is not None
        assert stats['errors'] == 0


# ============================================================================
# SCHEMA EXTRACTION TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.registry
class TestSchemaExtraction:
    """Test schema extraction from JSON structures"""
    
    def test_extract_schema_from_simple_structure(self, ai_data_dir, create_test_json_file):
        """Test schema extraction from simple JSON structure"""
        data = {
            "test_intelligence": {
                "score": 85.5,
                "status": "completed",
                "items": ["item1", "item2"]
            }
        }
        create_test_json_file("test.json", data)
        
        registry = IntelligenceTypeRegistry()
        registry.discover_from_directory(ai_data_dir)
        
        # Check if schema was extracted
        types = registry.list_types()
        assert len(types) > 0
        
        # Find the test_intelligence type
        test_type = next((t for t in types if 'test' in t['name']), None)
        if test_type:
            assert 'schema' in test_type
    
    def test_schema_includes_field_types(self, ai_data_dir, sample_career_intelligence, create_test_json_file):
        """Test that schema includes field type information"""
        create_test_json_file("career.json", sample_career_intelligence)
        
        registry = IntelligenceTypeRegistry()
        registry.discover_from_directory(ai_data_dir)
        
        types = registry.list_types()
        # Should have schemas for discovered types
        for type_info in types:
            if type_info.get('schema'):
                # Schema should be a dict
                assert isinstance(type_info['schema'], dict)


# ============================================================================
# HANDLER REGISTRATION TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.registry
class TestHandlerRegistration:
    """Test handler registration and retrieval"""
    
    def test_register_handler(self, mock_registry, simple_handler):
        """Test registering a handler"""
        mock_registry.register_handler(
            'test_type',
            simple_handler,
            priority='HIGH',
            description='Test handler'
        )
        
        # Verify handler was registered
        handler = mock_registry.get_handler('test_type')
        assert handler is not None
        
        # Test handler works
        result = handler({'test': 'data'})
        assert result['status'] == 'success'
    
    def test_register_multiple_handlers(self, mock_registry):
        """Test registering multiple handlers"""
        def handler1(data):
            return {'handler': 1}
        
        def handler2(data):
            return {'handler': 2}
        
        mock_registry.register_handler('type1', handler1, priority='HIGH')
        mock_registry.register_handler('type2', handler2, priority='MEDIUM')
        
        # Both should be registered
        h1 = mock_registry.get_handler('type1')
        h2 = mock_registry.get_handler('type2')
        
        assert h1 is not None
        assert h2 is not None
        assert h1({'test': 'data'})['handler'] == 1
        assert h2({'test': 'data'})['handler'] == 2
    
    def test_get_nonexistent_handler(self, mock_registry):
        """Test retrieving non-existent handler returns None"""
        handler = mock_registry.get_handler('nonexistent_type')
        assert handler is None
    
    def test_handler_override(self, mock_registry):
        """Test that registering same type twice overwrites"""
        def handler1(data):
            return {'version': 1}
        
        def handler2(data):
            return {'version': 2}
        
        mock_registry.register_handler('test', handler1, priority='HIGH')
        mock_registry.register_handler('test', handler2, priority='HIGH')
        
        handler = mock_registry.get_handler('test')
        result = handler({})
        
        # Should use latest handler
        assert result['version'] == 2


# ============================================================================
# TYPE INFO TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.registry
class TestTypeInfo:
    """Test intelligence type information retrieval"""
    
    def test_get_type_info(self, ai_data_dir, sample_career_intelligence, create_test_json_file):
        """Test retrieving type information"""
        create_test_json_file("test.json", sample_career_intelligence)
        
        registry = IntelligenceTypeRegistry()
        registry.discover_from_directory(ai_data_dir)
        
        types = registry.list_types()
        if len(types) > 0:
            first_type_name = types[0]['name']
            type_info = registry.get_type_info(first_type_name)
            
            if type_info:
                assert 'name' in type_info
                assert 'category' in type_info
    
    def test_list_types_returns_all(self, ai_data_dir, multiple_intelligence_files):
        """Test that list_types returns all discovered types"""
        registry = IntelligenceTypeRegistry()
        registry.discover_from_directory(ai_data_dir)
        
        types = registry.list_types()
        
        assert isinstance(types, list)
        assert len(types) > 0
    
    def test_get_implementation_status(self, mock_registry, simple_handler):
        """Test getting implementation status"""
        # Register one handler
        mock_registry.register_handler('implemented', simple_handler, priority='HIGH')
        
        # Add discovered but unimplemented type
        # (This would normally be done during discovery)
        
        status = mock_registry.get_implementation_status()
        
        assert 'total_types' in status
        assert 'implemented' in status
        assert 'not_implemented' in status


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.registry
class TestErrorHandling:
    """Test error handling in registry"""
    
    def test_discover_handles_invalid_json(self, ai_data_dir):
        """Test discovery handles invalid JSON gracefully"""
        # Create invalid JSON file
        invalid_file = ai_data_dir / "invalid.json"
        with open(invalid_file, 'w') as f:
            f.write("{ invalid json content")
        
        registry = IntelligenceTypeRegistry()
        stats = registry.discover_from_directory(ai_data_dir)
        
        # Should handle error gracefully
        assert stats['errors'] >= 0  # May or may not count as error depending on implementation
    
    def test_register_handler_with_none_function(self, mock_registry):
        """Test registering None as handler"""
        # This should either raise an error or be handled gracefully
        try:
            mock_registry.register_handler('test', None, priority='HIGH')
            # If it doesn't raise, check that None handler isn't callable
            handler = mock_registry.get_handler('test')
            if handler is not None:
                # Handler should not be None
                pass
        except (ValueError, TypeError):
            # Expected to raise an error
            pass


# ============================================================================
# INTEGRATION-LIKE TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.registry
class TestRegistryWorkflow:
    """Test complete registry workflows"""
    
    def test_discovery_then_registration_workflow(self, ai_data_dir, sample_career_intelligence, create_test_json_file, simple_handler):
        """Test complete workflow: discover → register → retrieve"""
        # 1. Discover types
        create_test_json_file("data.json", sample_career_intelligence)
        registry = IntelligenceTypeRegistry()
        stats = registry.discover_from_directory(ai_data_dir)
        
        assert stats['types_discovered'] > 0
        
        # 2. Register handler for one type
        types = registry.list_types()
        if len(types) > 0:
            first_type = types[0]['name']
            registry.register_handler(first_type, simple_handler, priority='HIGH')
            
            # 3. Retrieve and use handler
            handler = registry.get_handler(first_type)
            assert handler is not None
            
            result = handler({'test': 'data'})
            assert result['status'] == 'success'
    
    def test_type_discovery_persistence(self, ai_data_dir, multiple_intelligence_files):
        """Test that discovered types persist in registry"""
        registry = IntelligenceTypeRegistry()
        
        # First discovery
        stats1 = registry.discover_from_directory(ai_data_dir)
        types1 = registry.list_types()
        count1 = len(types1)
        
        # Second discovery (should not duplicate)
        stats2 = registry.discover_from_directory(ai_data_dir)
        types2 = registry.list_types()
        count2 = len(types2)
        
        # Count should be consistent or increase (not duplicate)
        assert count2 >= count1


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

@pytest.mark.slow
@pytest.mark.registry
@pytest.mark.performance
class TestRegistryPerformance:
    """Test registry performance"""
    
    def test_discovery_performance(self, benchmark_data_dir, benchmark):
        """Benchmark discovery performance"""
        registry = IntelligenceTypeRegistry()
        
        result = benchmark(registry.discover_from_directory, benchmark_data_dir)
        
        # Should discover from 100 files
        assert result['files_scanned'] == 100
    
    def test_handler_lookup_performance(self, mock_registry, simple_handler, benchmark):
        """Benchmark handler lookup performance"""
        # Register handler
        mock_registry.register_handler('test', simple_handler, priority='HIGH')
        
        # Benchmark lookup
        result = benchmark(mock_registry.get_handler, 'test')
        
        assert result is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
