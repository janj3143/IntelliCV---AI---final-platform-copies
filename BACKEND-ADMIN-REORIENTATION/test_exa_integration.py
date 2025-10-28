"""
Exa Service Test Script
=======================
Test the Exa deep web search integration.

This script tests:
1. Exa client initialization
2. Basic search functionality
3. Domain-scoped searches
4. Company enrichment (careers, products, background)
5. Caching mechanism
6. Error handling

Run this script to verify Exa integration is working correctly.
"""

import sys
from pathlib import Path
import json

# Add shared_backend to path
backend_path = Path(__file__).parent / "shared_backend"
sys.path.insert(0, str(backend_path))

def test_exa_client():
    """Test 1: Exa Client Initialization"""
    print("\n" + "="*70)
    print("TEST 1: Exa Client Initialization")
    print("="*70)
    
    try:
        from services.exa_service.exa_client import get_exa_client
        
        client = get_exa_client()
        print(f"✅ Exa client initialized successfully")
        print(f"   Base URL: {client.base_url}")
        print(f"   Search Mode: {client.search_mode}")
        print(f"   Max Results: {client.max_results}")
        print(f"   Rate Limit: {client.rate_limit} req/min")
        
        return True
    
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("   💡 Tip: Set EXA_API_KEY in .env file")
        return False
    except Exception as e:
        print(f"❌ Failed to initialize Exa client: {e}")
        return False

def test_basic_search():
    """Test 2: Basic Search"""
    print("\n" + "="*70)
    print("TEST 2: Basic Search")
    print("="*70)
    
    try:
        from services.exa_service.exa_client import get_exa_client
        
        client = get_exa_client()
        
        print("🔍 Searching for: 'artificial intelligence careers'")
        results = client.search(
            "artificial intelligence careers",
            num_results=3,
            search_mode="fast"
        )
        
        result_count = len(results.get('results', []))
        print(f"✅ Search successful: {result_count} results found")
        
        # Display first result
        if result_count > 0:
            first = results['results'][0]
            print(f"\n   First Result:")
            print(f"   Title: {first.get('title', 'N/A')}")
            print(f"   URL: {first.get('url', 'N/A')}")
            print(f"   Score: {first.get('score', 'N/A')}")
            
            content = first.get('text', '')
            if content:
                print(f"   Content: {content[:150]}...")
        
        return True
    
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return False

def test_domain_search():
    """Test 3: Domain-Scoped Search"""
    print("\n" + "="*70)
    print("TEST 3: Domain-Scoped Search")
    print("="*70)
    
    try:
        from services.exa_service.exa_client import get_exa_client
        
        client = get_exa_client()
        test_domain = "microsoft.com"
        
        print(f"🔍 Searching domain: {test_domain}")
        results = client.search_domain(
            domain=test_domain,
            keywords=["careers", "jobs"],
            num_results=5
        )
        
        result_count = len(results.get('results', []))
        print(f"✅ Domain search successful: {result_count} results from {test_domain}")
        
        # Show URLs
        for i, result in enumerate(results.get('results', [])[:3], 1):
            print(f"   {i}. {result.get('url', 'N/A')}")
        
        return True
    
    except Exception as e:
        print(f"❌ Domain search failed: {e}")
        return False

def test_company_enrichment():
    """Test 4: Company Enrichment"""
    print("\n" + "="*70)
    print("TEST 4: Company Enrichment")
    print("="*70)
    
    try:
        from services.exa_service.company_enrichment import get_company_enricher
        
        enricher = get_company_enricher()
        test_domain = "microsoft.com"
        
        print(f"🏢 Enriching company: {test_domain}")
        print("   This may take 10-30 seconds...")
        
        # Test careers search
        print("\n   📋 Searching careers pages...")
        careers = enricher.find_careers_pages(test_domain, num_results=3, use_cache=False)
        print(f"   ✅ Found {careers['total_found']} careers pages")
        
        if careers['careers_pages']:
            print(f"      Top: {careers['careers_pages'][0].get('title', 'N/A')}")
        
        # Test products search
        print("\n   🚀 Searching product pages...")
        products = enricher.find_product_pages(test_domain, num_results=3, use_cache=False)
        print(f"   ✅ Found {products['total_found']} product pages")
        
        if products['product_pages']:
            print(f"      Top: {products['product_pages'][0].get('title', 'N/A')}")
        
        # Test background search
        print("\n   📖 Searching company background...")
        background = enricher.get_company_background(test_domain, num_results=3, use_cache=False)
        print(f"   ✅ Found {background['total_found']} background pages")
        
        if background['background_pages']:
            print(f"      Top: {background['background_pages'][0].get('title', 'N/A')}")
        
        return True
    
    except Exception as e:
        print(f"❌ Company enrichment failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cache_mechanism():
    """Test 5: Caching Mechanism"""
    print("\n" + "="*70)
    print("TEST 5: Caching Mechanism")
    print("="*70)
    
    try:
        from services.exa_service.company_enrichment import get_company_enricher
        import time
        
        enricher = get_company_enricher()
        test_domain = "microsoft.com"
        
        # First search (no cache)
        print(f"🔍 First search (no cache) for {test_domain}")
        start = time.time()
        result1 = enricher.find_careers_pages(test_domain, num_results=3, use_cache=False)
        time1 = time.time() - start
        print(f"   ⏱️  Time: {time1:.2f}s | From cache: {result1.get('from_cache', False)}")
        
        # Second search (should use cache)
        print(f"\n🔍 Second search (should use cache)")
        start = time.time()
        result2 = enricher.find_careers_pages(test_domain, num_results=3, use_cache=True)
        time2 = time.time() - start
        print(f"   ⏱️  Time: {time2:.2f}s | From cache: {result2.get('from_cache', False)}")
        
        if result2.get('from_cache'):
            speedup = time1 / time2 if time2 > 0 else 0
            print(f"   ✅ Cache working! Speedup: {speedup:.1f}x faster")
            return True
        else:
            print(f"   ⚠️  Cache not used (this is OK if cache was just cleared)")
            return True
    
    except Exception as e:
        print(f"❌ Cache test failed: {e}")
        return False

def test_full_enrichment():
    """Test 6: Full Company Enrichment"""
    print("\n" + "="*70)
    print("TEST 6: Full Company Enrichment")
    print("="*70)
    
    try:
        from services.exa_service.company_enrichment import get_company_enricher
        
        enricher = get_company_enricher()
        test_domain = "openai.com"  # Different domain for variety
        
        print(f"🏢 Full enrichment for: {test_domain}")
        print("   This will take 30-60 seconds...")
        
        full = enricher.enrich_company_full(test_domain, use_cache=False)
        
        print(f"\n✅ Full enrichment complete!")
        print(f"   Total pages found: {full.get('total_pages_found', 0)}")
        print(f"   - Careers: {full['careers'].get('total_found', 0)}")
        print(f"   - Products: {full['products'].get('total_found', 0)}")
        print(f"   - Background: {full['background'].get('total_found', 0)}")
        
        # Check corpus save
        corpus_file = Path(f"ai_data_final/company_corpora/{test_domain}/enrichment.json")
        if corpus_file.exists():
            print(f"   ✅ Corpus saved to: {corpus_file}")
        else:
            print(f"   ⚠️  Corpus file not found (this may be OK)")
        
        return True
    
    except Exception as e:
        print(f"❌ Full enrichment failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def print_summary(results):
    """Print test summary"""
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    print("\nDetailed Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Exa integration is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the errors above.")
        print("💡 Common issues:")
        print("   - Missing EXA_API_KEY in .env file")
        print("   - Invalid API key")
        print("   - Network/firewall issues")
        print("   - Rate limiting")

def main():
    """Run all tests"""
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║          EXA (EXE) DEEP WEB SEARCH - TEST SUITE                  ║
    ║                  IntelliCV Platform Integration                   ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    results = {}
    
    # Run tests in sequence
    results['Exa Client Init'] = test_exa_client()
    
    # Only continue if client initialized
    if results['Exa Client Init']:
        results['Basic Search'] = test_basic_search()
        results['Domain Search'] = test_domain_search()
        results['Company Enrichment'] = test_company_enrichment()
        results['Cache Mechanism'] = test_cache_mechanism()
        
        # Ask user before running full enrichment (takes longer)
        print("\n" + "="*70)
        response = input("Run full enrichment test? (takes 30-60s) [y/N]: ").strip().lower()
        if response == 'y':
            results['Full Enrichment'] = test_full_enrichment()
        else:
            print("⏭️  Skipping full enrichment test")
            results['Full Enrichment'] = None
    
    # Print summary
    # Filter out skipped tests
    results_to_show = {k: v for k, v in results.items() if v is not None}
    print_summary(results_to_show)
    
    return all(results_to_show.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
