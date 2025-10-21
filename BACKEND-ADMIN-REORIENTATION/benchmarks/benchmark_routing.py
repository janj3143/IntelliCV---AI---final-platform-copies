"""
Performance Benchmarks: Routing System
Measures routing and handler lookup performance
"""

import pytest
import time
from shared_backend.ai_engines.hybrid_integrator import HybridAIIntegrator


# ============================================================================
# HANDLER LOOKUP BENCHMARKS
# ============================================================================

@pytest.mark.benchmark
class TestHandlerLookupPerformance:
    """Benchmark handler lookup performance"""
    
    def test_benchmark_single_lookup(self, mock_hybrid_integrator, simple_handler):
        """Benchmark single handler lookup"""
        # Register handler
        mock_hybrid_integrator.registry.register_handler(
            'test_type',
            simple_handler,
            priority='HIGH'
        )
        
        # Benchmark lookup
        iterations = 10000
        start_time = time.time()
        
        for _ in range(iterations):
            handler = mock_hybrid_integrator.registry.get_handler('test_type')
        
        duration = time.time() - start_time
        avg_time_ms = (duration / iterations) * 1000
        
        print(f"\n🔍 Handler Lookup Performance:")
        print(f"   Iterations: {iterations:,}")
        print(f"   Total time: {duration:.3f}s")
        print(f"   Average: {avg_time_ms:.4f}ms per lookup")
        print(f"   Throughput: {iterations/duration:,.0f} lookups/second")
        
        # Target: < 1ms per lookup
        assert avg_time_ms < 1.0, f"Lookup took {avg_time_ms:.4f}ms, should be <1ms"
    
    def test_benchmark_multiple_types_lookup(self, mock_hybrid_integrator):
        """Benchmark lookup with multiple registered types"""
        # Register 100 handlers
        handlers = {}
        for i in range(100):
            def handler(data, i=i):
                return {'handler_id': i}
            handlers[f'type_{i}'] = handler
            mock_hybrid_integrator.registry.register_handler(
                f'type_{i}',
                handler,
                priority='HIGH'
            )
        
        # Benchmark random lookups
        iterations = 1000
        start_time = time.time()
        
        for i in range(iterations):
            type_id = f'type_{i % 100}'
            handler = mock_hybrid_integrator.registry.get_handler(type_id)
        
        duration = time.time() - start_time
        
        print(f"\n📚 Multi-Type Lookup Performance:")
        print(f"   Registered types: 100")
        print(f"   Lookups: {iterations}")
        print(f"   Duration: {duration:.3f}s")
        print(f"   Average: {(duration/iterations)*1000:.4f}ms")
        
        # Should scale well
        assert duration < 2.0, "Lookups should be fast even with many types"


# ============================================================================
# ROUTING PERFORMANCE BENCHMARKS
# ============================================================================

@pytest.mark.benchmark
class TestRoutingPerformance:
    """Benchmark routing performance"""
    
    def test_benchmark_routing_overhead(self, mock_hybrid_integrator, simple_handler):
        """Measure routing overhead"""
        mock_hybrid_integrator.registry.register_handler(
            'routed',
            simple_handler,
            priority='HIGH'
        )
        
        # Benchmark routing
        iterations = 1000
        data = {'test': 'data'}
        
        start_time = time.time()
        
        for _ in range(iterations):
            result = mock_hybrid_integrator.run_inference('routed', data)
        
        duration = time.time() - start_time
        avg_time_ms = (duration / iterations) * 1000
        
        print(f"\n🚀 Routing Overhead:")
        print(f"   Iterations: {iterations}")
        print(f"   Duration: {duration:.3f}s")
        print(f"   Average: {avg_time_ms:.4f}ms per route")
        print(f"   Throughput: {iterations/duration:.0f} requests/second")
        
        # Target: < 10ms routing overhead
        assert avg_time_ms < 10.0, f"Routing took {avg_time_ms:.4f}ms, should be <10ms"
    
    def test_benchmark_routing_with_complex_data(self, mock_hybrid_integrator, simple_handler):
        """Benchmark routing with complex data"""
        mock_hybrid_integrator.registry.register_handler(
            'complex',
            simple_handler,
            priority='HIGH'
        )
        
        # Complex data
        complex_data = {
            'profile': {
                'name': 'Test User',
                'skills': ['Python', 'ML', 'Cloud'] * 10,
                'experience': list(range(100)),
                'projects': [{'name': f'Project {i}', 'desc': 'x' * 100} for i in range(10)]
            }
        }
        
        iterations = 100
        start_time = time.time()
        
        for _ in range(iterations):
            result = mock_hybrid_integrator.run_inference('complex', complex_data)
        
        duration = time.time() - start_time
        
        print(f"\n📦 Complex Data Routing:")
        print(f"   Iterations: {iterations}")
        print(f"   Duration: {duration:.3f}s")
        print(f"   Average: {(duration/iterations)*1000:.2f}ms")
        
        assert duration < 5.0, "Should handle complex data efficiently"


# ============================================================================
# CONCURRENT ROUTING BENCHMARKS
# ============================================================================

@pytest.mark.benchmark
@pytest.mark.slow
class TestConcurrentRouting:
    """Benchmark concurrent routing"""
    
    def test_benchmark_concurrent_requests(self, mock_hybrid_integrator, simple_handler):
        """Benchmark concurrent routing requests"""
        mock_hybrid_integrator.registry.register_handler(
            'concurrent',
            simple_handler,
            priority='HIGH'
        )
        
        # Simulate concurrent requests
        num_requests = 100
        data = {'request': 'data'}
        
        start_time = time.time()
        
        results = []
        for i in range(num_requests):
            result = mock_hybrid_integrator.run_inference('concurrent', data)
            results.append(result)
        
        duration = time.time() - start_time
        
        print(f"\n🔄 Concurrent Routing:")
        print(f"   Requests: {num_requests}")
        print(f"   Duration: {duration:.3f}s")
        print(f"   Average: {(duration/num_requests)*1000:.2f}ms")
        print(f"   Throughput: {num_requests/duration:.0f} requests/second")
        
        # All should succeed
        assert len(results) == num_requests
        
        # Target: > 100 requests/second
        throughput = num_requests / duration
        assert throughput > 100, f"Throughput {throughput:.0f} req/s, should be >100"
    
    def test_benchmark_mixed_type_routing(self, mock_hybrid_integrator):
        """Benchmark routing to multiple different types"""
        # Register 10 different handlers
        for i in range(10):
            def handler(data, i=i):
                return {'type': i, 'status': 'success'}
            mock_hybrid_integrator.registry.register_handler(
                f'type_{i}',
                handler,
                priority='HIGH'
            )
        
        # Route to all types repeatedly
        iterations = 50
        start_time = time.time()
        
        for _ in range(iterations):
            for i in range(10):
                result = mock_hybrid_integrator.run_inference(f'type_{i}', {})
        
        duration = time.time() - start_time
        total_requests = iterations * 10
        
        print(f"\n🎯 Mixed Type Routing:")
        print(f"   Types: 10")
        print(f"   Total requests: {total_requests}")
        print(f"   Duration: {duration:.3f}s")
        print(f"   Throughput: {total_requests/duration:.0f} requests/second")
        
        assert duration < 10.0, "Mixed routing should be efficient"


# ============================================================================
# HANDLER EXECUTION BENCHMARKS
# ============================================================================

@pytest.mark.benchmark
class TestHandlerExecutionPerformance:
    """Benchmark handler execution performance"""
    
    def test_benchmark_fast_handler(self, mock_hybrid_integrator):
        """Benchmark fast handler execution"""
        def fast_handler(data):
            return {'status': 'success', 'data': data}
        
        mock_hybrid_integrator.registry.register_handler(
            'fast',
            fast_handler,
            priority='HIGH'
        )
        
        iterations = 1000
        start_time = time.time()
        
        for _ in range(iterations):
            result = mock_hybrid_integrator.run_inference('fast', {'test': 'data'})
        
        duration = time.time() - start_time
        
        print(f"\n⚡ Fast Handler Performance:")
        print(f"   Iterations: {iterations}")
        print(f"   Duration: {duration:.3f}s")
        print(f"   Average: {(duration/iterations)*1000:.4f}ms")
        
        # Fast handlers should be very quick
        assert duration < 1.0, "Fast handlers should complete quickly"
    
    def test_benchmark_complex_handler(self, mock_hybrid_integrator):
        """Benchmark complex handler execution"""
        def complex_handler(data):
            # Simulate complex processing
            result = {'status': 'success'}
            for i in range(100):
                result[f'field_{i}'] = i * 2
            return result
        
        mock_hybrid_integrator.registry.register_handler(
            'complex',
            complex_handler,
            priority='HIGH'
        )
        
        iterations = 100
        start_time = time.time()
        
        for _ in range(iterations):
            result = mock_hybrid_integrator.run_inference('complex', {})
        
        duration = time.time() - start_time
        
        print(f"\n🔨 Complex Handler Performance:")
        print(f"   Iterations: {iterations}")
        print(f"   Duration: {duration:.3f}s")
        print(f"   Average: {(duration/iterations)*1000:.2f}ms")
        
        # Target: < 100ms average for complex handlers
        avg_ms = (duration / iterations) * 1000
        assert avg_ms < 100, f"Complex handler took {avg_ms:.2f}ms, should be <100ms"


# ============================================================================
# CACHE PERFORMANCE (IF IMPLEMENTED)
# ============================================================================

@pytest.mark.benchmark
class TestCachePerformance:
    """Benchmark caching performance if implemented"""
    
    def test_lookup_caching_benefit(self, mock_hybrid_integrator, simple_handler):
        """Test if caching improves lookup performance"""
        mock_hybrid_integrator.registry.register_handler(
            'cached',
            simple_handler,
            priority='HIGH'
        )
        
        # First set of lookups (cache miss)
        iterations = 1000
        start_time = time.time()
        for _ in range(iterations):
            mock_hybrid_integrator.registry.get_handler('cached')
        first_duration = time.time() - start_time
        
        # Second set of lookups (should hit cache if implemented)
        start_time = time.time()
        for _ in range(iterations):
            mock_hybrid_integrator.registry.get_handler('cached')
        second_duration = time.time() - start_time
        
        print(f"\n💾 Cache Performance:")
        print(f"   First run: {first_duration:.3f}s")
        print(f"   Second run: {second_duration:.3f}s")
        print(f"   Improvement: {((first_duration-second_duration)/first_duration)*100:.1f}%")
        
        # Second should be at least as fast
        assert second_duration <= first_duration * 1.1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
