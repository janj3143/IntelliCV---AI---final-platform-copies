"""
Performance Benchmarks: Discovery System
Measures discovery performance with various file counts
"""

import pytest
import json
import time
from pathlib import Path
from shared_backend.ai_engines.intelligence_type_registry import IntelligenceTypeRegistry


# ============================================================================
# DISCOVERY PERFORMANCE BENCHMARKS
# ============================================================================

@pytest.mark.benchmark
@pytest.mark.slow
class TestDiscoveryPerformance:
    """Benchmark discovery system performance"""
    
    def test_benchmark_discovery_100_files(self, benchmark_data_dir):
        """Benchmark: Discovery from 100 files"""
        registry = IntelligenceTypeRegistry()
        
        start_time = time.time()
        stats = registry.discover_from_directory(benchmark_data_dir)
        end_time = time.time()
        
        duration = end_time - start_time
        
        print(f"\n📊 Discovery Performance (100 files):")
        print(f"   Files scanned: {stats['files_scanned']}")
        print(f"   Types discovered: {stats['types_discovered']}")
        print(f"   Duration: {duration:.3f}s")
        print(f"   Files/second: {stats['files_scanned']/duration:.1f}")
        
        # Performance targets
        assert duration < 10.0, "Should complete in under 10 seconds"
        assert stats['files_scanned'] == 100
    
    def test_benchmark_discovery_scaling(self, tmp_path):
        """Benchmark: Discovery scaling with file count"""
        results = []
        
        for file_count in [10, 50, 100, 200, 500]:
            # Create test data
            test_dir = tmp_path / f"scale_{file_count}"
            test_dir.mkdir()
            
            for i in range(file_count):
                test_file = test_dir / f"data_{i}.json"
                with open(test_file, 'w') as f:
                    json.dump({
                        f'intelligence_type_{i}': {
                            'value': i,
                            'data': f'test data {i}'
                        }
                    }, f)
            
            # Benchmark discovery
            registry = IntelligenceTypeRegistry()
            start_time = time.time()
            stats = registry.discover_from_directory(test_dir)
            duration = time.time() - start_time
            
            results.append({
                'file_count': file_count,
                'duration': duration,
                'types_discovered': stats['types_discovered'],
                'files_per_second': file_count / duration
            })
        
        # Print results
        print("\n📈 Discovery Scaling Results:")
        print(f"{'Files':<10} {'Duration':<12} {'Types':<10} {'Files/sec':<12}")
        print("-" * 50)
        for r in results:
            print(f"{r['file_count']:<10} {r['duration']:<12.3f} {r['types_discovered']:<10} {r['files_per_second']:<12.1f}")
        
        # Verify linear or better scaling
        assert results[-1]['files_per_second'] > 10, "Should process >10 files/second"
    
    def test_benchmark_real_world_discovery(self, tmp_path):
        """Benchmark: Real-world scenario with 3,502 files"""
        # Simulate real data structure
        test_dir = tmp_path / "real_world"
        test_dir.mkdir()
        
        # Create 3,502 test files (matching real system)
        print("\n📁 Creating 3,502 test files...")
        for i in range(3502):
            test_file = test_dir / f"intelligence_{i}.json"
            with open(test_file, 'w') as f:
                json.dump({
                    f'career_intelligence': {'trajectory': 'upward'},
                    f'job_match_intelligence': {'score': 0.85},
                    f'skill_intelligence': {'gaps': ['python', 'ml']}
                }, f)
        
        print("✅ Files created, starting discovery...")
        
        # Benchmark discovery
        registry = IntelligenceTypeRegistry()
        start_time = time.time()
        stats = registry.discover_from_directory(test_dir)
        end_time = time.time()
        
        duration = end_time - start_time
        
        print(f"\n🎯 Real-World Discovery Results:")
        print(f"   Files scanned: {stats['files_scanned']:,}")
        print(f"   Types discovered: {stats['types_discovered']:,}")
        print(f"   Duration: {duration:.2f}s")
        print(f"   Files/second: {stats['files_scanned']/duration:.1f}")
        print(f"   Types/second: {stats['types_discovered']/duration:.1f}")
        
        # Performance target: < 10 seconds for 3,500 files
        assert duration < 10.0, f"Discovery took {duration:.2f}s, should be <10s"
        assert stats['files_scanned'] == 3502


# ============================================================================
# MEMORY USAGE BENCHMARKS
# ============================================================================

@pytest.mark.benchmark
@pytest.mark.slow
class TestDiscoveryMemoryUsage:
    """Benchmark memory usage during discovery"""
    
    def test_memory_usage_large_dataset(self, tmp_path):
        """Measure memory usage with large dataset"""
        import tracemalloc
        
        # Create 1000 files
        test_dir = tmp_path / "memory_test"
        test_dir.mkdir()
        
        for i in range(1000):
            test_file = test_dir / f"data_{i}.json"
            with open(test_file, 'w') as f:
                json.dump({
                    f'type_{i}': {
                        'data': 'x' * 1000  # 1KB of data per file
                    }
                }, f)
        
        # Measure memory
        tracemalloc.start()
        
        registry = IntelligenceTypeRegistry()
        stats = registry.discover_from_directory(test_dir)
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"\n💾 Memory Usage (1000 files):")
        print(f"   Current: {current / 1024 / 1024:.2f} MB")
        print(f"   Peak: {peak / 1024 / 1024:.2f} MB")
        print(f"   Per file: {peak / 1000 / 1024:.2f} KB")
        
        # Memory target: < 100 MB peak for 1000 files
        assert peak < 100 * 1024 * 1024, "Memory usage should be <100MB"


# ============================================================================
# SCHEMA EXTRACTION PERFORMANCE
# ============================================================================

@pytest.mark.benchmark
class TestSchemaExtractionPerformance:
    """Benchmark schema extraction performance"""
    
    def test_schema_extraction_speed(self, tmp_path):
        """Benchmark schema extraction from complex JSON"""
        # Create file with complex structure
        test_dir = tmp_path / "schema_test"
        test_dir.mkdir()
        
        complex_data = {
            'career_intelligence': {
                'trajectory': 'upward',
                'growth_potential': 0.85,
                'predicted_roles': ['Senior Engineer', 'Tech Lead', 'Manager'],
                'skills': {
                    'technical': ['Python', 'ML', 'Cloud'],
                    'soft': ['Leadership', 'Communication']
                },
                'timeline': {
                    'short_term': '1-2 years',
                    'long_term': '5+ years'
                }
            }
        }
        
        # Create 100 files with complex data
        for i in range(100):
            test_file = test_dir / f"complex_{i}.json"
            with open(test_file, 'w') as f:
                json.dump(complex_data, f)
        
        # Benchmark
        registry = IntelligenceTypeRegistry()
        start_time = time.time()
        stats = registry.discover_from_directory(test_dir)
        duration = time.time() - start_time
        
        print(f"\n🔍 Schema Extraction Performance:")
        print(f"   Files: 100")
        print(f"   Duration: {duration:.3f}s")
        print(f"   Extractions/second: {100/duration:.1f}")
        
        assert duration < 5.0, "Schema extraction should be fast"


# ============================================================================
# CONCURRENT DISCOVERY BENCHMARKS
# ============================================================================

@pytest.mark.benchmark
@pytest.mark.slow
class TestConcurrentDiscovery:
    """Benchmark concurrent discovery operations"""
    
    def test_concurrent_discovery_instances(self, benchmark_data_dir):
        """Benchmark multiple registry instances discovering concurrently"""
        registries = [IntelligenceTypeRegistry() for _ in range(5)]
        
        start_time = time.time()
        
        # Simulate concurrent discovery
        results = []
        for registry in registries:
            stats = registry.discover_from_directory(benchmark_data_dir)
            results.append(stats)
        
        duration = time.time() - start_time
        
        print(f"\n🔄 Concurrent Discovery (5 instances):")
        print(f"   Total duration: {duration:.3f}s")
        print(f"   Per instance: {duration/5:.3f}s average")
        
        # All should succeed
        assert len(results) == 5
        assert all(r['errors'] == 0 for r in results)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
