"""
Performance Benchmarks: Portal Bridge
Measures portal bridge overhead and performance
"""

import pytest
import time
from shared_backend.services.portal_bridge import PortalBridge


# ============================================================================
# PORTAL BRIDGE OVERHEAD BENCHMARKS
# ============================================================================

@pytest.mark.benchmark
class TestPortalBridgeOverhead:
    """Benchmark portal bridge overhead"""
    
    def test_benchmark_portal_overhead(self, mock_portal_bridge, sample_profile_data):
        """Measure portal bridge overhead"""
        iterations = 1000
        
        start_time = time.time()
        
        for _ in range(iterations):
            result = mock_portal_bridge.get_intelligence(
                intelligence_type='career_path',
                data=sample_profile_data
            )
        
        duration = time.time() - start_time
        avg_time_ms = (duration / iterations) * 1000
        
        print(f"\n🌉 Portal Bridge Overhead:")
        print(f"   Iterations: {iterations}")
        print(f"   Duration: {duration:.3f}s")
        print(f"   Average: {avg_time_ms:.4f}ms per request")
        print(f"   Throughput: {iterations/duration:.0f} requests/second")
        
        # Target: < 5ms overhead
        assert avg_time_ms < 5.0, f"Portal overhead {avg_time_ms:.4f}ms, should be <5ms"
    
    def test_benchmark_direct_vs_portal_access(self, mock_portal_bridge, mock_hybrid_integrator, sample_profile_data, simple_handler):
        """Compare direct vs portal access performance"""
        # Register handler
        mock_hybrid_integrator.registry.register_handler(
            'test',
            simple_handler,
            priority='HIGH'
        )
        
        iterations = 100
        
        # Direct access
        start_time = time.time()
        for _ in range(iterations):
            result = mock_hybrid_integrator.run_inference('test', sample_profile_data)
        direct_duration = time.time() - start_time
        
        # Portal access
        start_time = time.time()
        for _ in range(iterations):
            result = mock_portal_bridge.get_intelligence(
                intelligence_type='test',
                data=sample_profile_data
            )
        portal_duration = time.time() - start_time
        
        overhead = portal_duration - direct_duration
        overhead_percent = (overhead / direct_duration) * 100
        
        print(f"\n⚖️  Direct vs Portal Access:")
        print(f"   Direct: {direct_duration:.3f}s ({(direct_duration/iterations)*1000:.2f}ms avg)")
        print(f"   Portal: {portal_duration:.3f}s ({(portal_duration/iterations)*1000:.2f}ms avg)")
        print(f"   Overhead: {overhead:.3f}s ({overhead_percent:.1f}%)")
        
        # Portal overhead should be minimal
        assert overhead_percent < 50, f"Portal overhead {overhead_percent:.1f}%, should be <50%"


# ============================================================================
# PORTAL METHOD PERFORMANCE
# ============================================================================

@pytest.mark.benchmark
class TestPortalMethodPerformance:
    """Benchmark individual portal methods"""
    
    def test_benchmark_get_career_intelligence(self, mock_portal_bridge, sample_profile_data):
        """Benchmark get_career_intelligence method"""
        iterations = 100
        
        start_time = time.time()
        
        for _ in range(iterations):
            try:
                result = mock_portal_bridge.get_career_intelligence(sample_profile_data)
            except AttributeError:
                # Method might not exist in mock
                result = mock_portal_bridge.get_intelligence('career_path', sample_profile_data)
        
        duration = time.time() - start_time
        
        print(f"\n💼 Career Intelligence Method:")
        print(f"   Iterations: {iterations}")
        print(f"   Duration: {duration:.3f}s")
        print(f"   Average: {(duration/iterations)*1000:.2f}ms")
        
        assert duration < 5.0, "Career intelligence should be fast"
    
    def test_benchmark_get_job_matches(self, mock_portal_bridge, sample_profile_data):
        """Benchmark get_job_matches method"""
        iterations = 100
        
        start_time = time.time()
        
        for _ in range(iterations):
            try:
                result = mock_portal_bridge.get_job_matches(sample_profile_data)
            except AttributeError:
                result = mock_portal_bridge.get_intelligence('job_match', sample_profile_data)
        
        duration = time.time() - start_time
        
        print(f"\n🎯 Job Matches Method:")
        print(f"   Iterations: {iterations}")
        print(f"   Duration: {duration:.3f}s")
        print(f"   Average: {(duration/iterations)*1000:.2f}ms")
        
        assert duration < 5.0, "Job matching should be fast"
    
    def test_benchmark_all_user_methods(self, mock_portal_bridge, sample_profile_data):
        """Benchmark all user portal methods"""
        methods = [
            ('career', lambda: mock_portal_bridge.get_intelligence('career_path', sample_profile_data)),
            ('jobs', lambda: mock_portal_bridge.get_intelligence('job_match', sample_profile_data)),
            ('skills', lambda: mock_portal_bridge.get_intelligence('skill_gaps', sample_profile_data)),
            ('salary', lambda: mock_portal_bridge.get_intelligence('salary', sample_profile_data)),
        ]
        
        print(f"\n👤 User Portal Methods Performance:")
        
        for name, method in methods:
            iterations = 50
            start_time = time.time()
            
            for _ in range(iterations):
                result = method()
            
            duration = time.time() - start_time
            avg_ms = (duration / iterations) * 1000
            
            print(f"   {name:<15}: {avg_ms:>6.2f}ms average")


# ============================================================================
# METADATA TRACKING OVERHEAD
# ============================================================================

@pytest.mark.benchmark
class TestMetadataOverhead:
    """Benchmark metadata tracking overhead"""
    
    def test_benchmark_metadata_tracking(self, mock_portal_bridge, sample_profile_data):
        """Measure overhead of metadata tracking"""
        iterations = 500
        
        # Without metadata
        start_time = time.time()
        for _ in range(iterations):
            result = mock_portal_bridge.get_intelligence(
                intelligence_type='career_path',
                data=sample_profile_data
            )
        no_metadata_duration = time.time() - start_time
        
        # With metadata
        start_time = time.time()
        for _ in range(iterations):
            result = mock_portal_bridge.get_intelligence(
                intelligence_type='career_path',
                data=sample_profile_data,
                portal_type='user'
            )
        with_metadata_duration = time.time() - start_time
        
        overhead = with_metadata_duration - no_metadata_duration
        overhead_percent = (overhead / no_metadata_duration) * 100 if no_metadata_duration > 0 else 0
        
        print(f"\n📊 Metadata Tracking Overhead:")
        print(f"   Without metadata: {no_metadata_duration:.3f}s")
        print(f"   With metadata: {with_metadata_duration:.3f}s")
        print(f"   Overhead: {overhead:.3f}s ({overhead_percent:.1f}%)")
        
        # Metadata overhead should be minimal
        assert overhead_percent < 20, f"Metadata overhead {overhead_percent:.1f}%, should be <20%"


# ============================================================================
# CONCURRENT PORTAL ACCESS
# ============================================================================

@pytest.mark.benchmark
@pytest.mark.slow
class TestConcurrentPortalAccess:
    """Benchmark concurrent portal access"""
    
    def test_benchmark_concurrent_users(self, mock_portal_bridge, sample_profile_data):
        """Simulate concurrent user requests"""
        num_users = 50
        
        start_time = time.time()
        
        results = []
        for user_id in range(num_users):
            result = mock_portal_bridge.get_intelligence(
                intelligence_type='career_path',
                data=sample_profile_data,
                portal_type='user'
            )
            results.append(result)
        
        duration = time.time() - start_time
        
        print(f"\n👥 Concurrent User Access:")
        print(f"   Users: {num_users}")
        print(f"   Duration: {duration:.3f}s")
        print(f"   Average: {(duration/num_users)*1000:.2f}ms per user")
        print(f"   Throughput: {num_users/duration:.0f} users/second")
        
        # All should succeed
        assert len(results) == num_users
        
        # Should handle concurrent users well
        assert duration < 5.0, f"Took {duration:.2f}s for {num_users} users"
    
    def test_benchmark_mixed_portal_types(self, mock_portal_bridge, sample_profile_data):
        """Benchmark mixed portal type access"""
        requests = [
            ('user', 'career_path'),
            ('user', 'job_match'),
            ('admin', 'analytics'),
            ('recruiter', 'candidate'),
            ('user', 'salary'),
        ] * 10  # 50 total requests
        
        start_time = time.time()
        
        results = []
        for portal_type, intelligence_type in requests:
            result = mock_portal_bridge.get_intelligence(
                intelligence_type=intelligence_type,
                data=sample_profile_data,
                portal_type=portal_type
            )
            results.append(result)
        
        duration = time.time() - start_time
        
        print(f"\n🎭 Mixed Portal Type Access:")
        print(f"   Requests: {len(requests)}")
        print(f"   Duration: {duration:.3f}s")
        print(f"   Average: {(duration/len(requests))*1000:.2f}ms")
        print(f"   Throughput: {len(requests)/duration:.0f} requests/second")
        
        assert len(results) == len(requests)


# ============================================================================
# END-TO-END PORTAL WORKFLOWS
# ============================================================================

@pytest.mark.benchmark
@pytest.mark.slow
class TestPortalWorkflowPerformance:
    """Benchmark complete portal workflows"""
    
    def test_benchmark_user_portal_workflow(self, mock_portal_bridge, sample_profile_data):
        """Benchmark typical user portal workflow"""
        iterations = 20
        
        start_time = time.time()
        
        for _ in range(iterations):
            # Typical user workflow
            career = mock_portal_bridge.get_intelligence('career_path', sample_profile_data)
            jobs = mock_portal_bridge.get_intelligence('job_match', sample_profile_data)
            salary = mock_portal_bridge.get_intelligence('salary', sample_profile_data)
        
        duration = time.time() - start_time
        workflow_time = duration / iterations
        
        print(f"\n🔄 User Portal Workflow:")
        print(f"   Iterations: {iterations}")
        print(f"   Duration: {duration:.3f}s")
        print(f"   Per workflow: {workflow_time*1000:.2f}ms")
        print(f"   Workflows/second: {iterations/duration:.1f}")
        
        # Target: < 50ms per complete workflow
        assert workflow_time < 0.05, f"Workflow took {workflow_time*1000:.2f}ms, should be <50ms"
    
    def test_benchmark_admin_portal_workflow(self, mock_portal_bridge):
        """Benchmark typical admin portal workflow"""
        iterations = 20
        
        start_time = time.time()
        
        for _ in range(iterations):
            # Admin workflow
            analytics = mock_portal_bridge.get_intelligence('analytics', {}, portal_type='admin')
            types = mock_portal_bridge.get_intelligence('types', {}, portal_type='admin')
        
        duration = time.time() - start_time
        
        print(f"\n⚙️  Admin Portal Workflow:")
        print(f"   Iterations: {iterations}")
        print(f"   Duration: {duration:.3f}s")
        print(f"   Per workflow: {(duration/iterations)*1000:.2f}ms")
        
        assert duration < 5.0, "Admin workflow should be fast"


# ============================================================================
# STRESS TESTS
# ============================================================================

@pytest.mark.benchmark
@pytest.mark.slow
class TestPortalStress:
    """Stress test portal bridge"""
    
    def test_sustained_load(self, mock_portal_bridge, sample_profile_data):
        """Test sustained load on portal bridge"""
        duration_seconds = 5
        requests = 0
        
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        while time.time() < end_time:
            result = mock_portal_bridge.get_intelligence(
                intelligence_type='career_path',
                data=sample_profile_data
            )
            requests += 1
        
        actual_duration = time.time() - start_time
        requests_per_second = requests / actual_duration
        
        print(f"\n🔥 Sustained Load Test:")
        print(f"   Duration: {actual_duration:.1f}s")
        print(f"   Requests: {requests:,}")
        print(f"   Throughput: {requests_per_second:.0f} requests/second")
        
        # Target: > 100 requests/second sustained
        assert requests_per_second > 100, f"Throughput {requests_per_second:.0f} req/s, should be >100"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
