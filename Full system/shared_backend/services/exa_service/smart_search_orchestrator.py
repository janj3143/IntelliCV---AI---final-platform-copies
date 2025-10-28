"""
Smart Search Orchestrator - Cost-Efficient Two-Tier Strategy
==============================================================

Implements a two-tier search approach to minimize Exa API costs:

1. **Google Search** (Free/Cheap):
   - Primary search for candidate URLs
   - Get broad results quickly
   - Filter by relevance, domain authority, etc.

2. **Exa Deep Analysis** (Paid):
   - Only for URLs that pass filters
   - Deep content extraction
   - Neural search for quality insights

This approach can reduce Exa API costs by 70-90% while maintaining quality.

Cost Analysis:
- Google Custom Search: $5/1000 queries (or free tier: 100/day)
- Exa API: ~$0.01-0.05 per search (varies by plan)
- Savings: If only 10% of Google results go to Exa = 90% cost reduction

Example Flow:
1. User searches "Python jobs at Microsoft"
2. Google returns 100 career page URLs
3. Filter: Only .com domains, careers pages, recent (50 URLs remain)
4. Exa analyzes those 50 URLs (instead of crawling all 100)
5. Store high-quality results
"""

import os
import time
import logging
from typing import List, Dict, Optional, Callable
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)


class SearchFilter:
    """Filter criteria for Google results before sending to Exa."""
    
    def __init__(self):
        # Domain filters
        self.allowed_domains = set()  # Empty = all allowed
        self.blocked_domains = {'spam.com', 'malware.com'}
        
        # URL pattern filters
        self.required_url_patterns = ['career', 'jobs', 'opportunities', 'hiring']
        self.blocked_url_patterns = ['login', 'signup', 'cart', 'checkout']
        
        # Content filters
        self.min_domain_authority = 0  # 0-100 (use SEO API if available)
        self.require_https = False
        
        # Recency filters
        self.max_age_days = None  # None = no limit
        
        # Deduplication
        self.seen_urls = set()
    
    def passes_filter(self, result: Dict) -> bool:
        """
        Check if Google result passes filters for Exa analysis.
        
        Args:
            result: Dict with 'url', 'title', 'snippet', 'domain', etc.
        
        Returns:
            True if should send to Exa, False to skip
        """
        url = result.get('url', '')
        domain = result.get('domain', '')
        
        # Deduplication
        if url in self.seen_urls:
            logger.debug(f"Skipping duplicate: {url}")
            return False
        
        # Domain whitelist
        if self.allowed_domains and domain not in self.allowed_domains:
            logger.debug(f"Domain not in whitelist: {domain}")
            return False
        
        # Domain blacklist
        if domain in self.blocked_domains:
            logger.debug(f"Domain blocked: {domain}")
            return False
        
        # URL pattern requirements
        url_lower = url.lower()
        has_required_pattern = any(
            pattern in url_lower 
            for pattern in self.required_url_patterns
        )
        if self.required_url_patterns and not has_required_pattern:
            logger.debug(f"URL missing required pattern: {url}")
            return False
        
        # URL pattern blocks
        has_blocked_pattern = any(
            pattern in url_lower 
            for pattern in self.blocked_url_patterns
        )
        if has_blocked_pattern:
            logger.debug(f"URL has blocked pattern: {url}")
            return False
        
        # HTTPS requirement
        if self.require_https and not url.startswith('https://'):
            logger.debug(f"URL not HTTPS: {url}")
            return False
        
        # Passed all filters
        self.seen_urls.add(url)
        return True


class CostTracker:
    """Track API costs across Google and Exa."""
    
    def __init__(self):
        self.google_queries = 0
        self.exa_queries = 0
        self.google_cost_per_query = 0.005  # $5/1000 queries
        self.exa_cost_per_query = 0.03      # ~$0.03 per search (estimate)
    
    def log_google_query(self, num_queries: int = 1):
        """Log Google API usage."""
        self.google_queries += num_queries
    
    def log_exa_query(self, num_queries: int = 1):
        """Log Exa API usage."""
        self.exa_queries += num_queries
    
    def get_total_cost(self) -> float:
        """Calculate total API costs."""
        google_cost = self.google_queries * self.google_cost_per_query
        exa_cost = self.exa_queries * self.exa_cost_per_query
        return google_cost + exa_cost
    
    def get_cost_breakdown(self) -> Dict:
        """Get detailed cost breakdown."""
        google_cost = self.google_queries * self.google_cost_per_query
        exa_cost = self.exa_queries * self.exa_cost_per_query
        
        return {
            'google': {
                'queries': self.google_queries,
                'cost': google_cost,
                'cost_per_query': self.google_cost_per_query
            },
            'exa': {
                'queries': self.exa_queries,
                'cost': exa_cost,
                'cost_per_query': self.exa_cost_per_query
            },
            'total_cost': google_cost + exa_cost,
            'savings_vs_exa_only': (self.google_queries + self.exa_queries) * self.exa_cost_per_query - (google_cost + exa_cost),
            'efficiency_ratio': self.exa_queries / max(self.google_queries + self.exa_queries, 1)
        }
    
    def print_summary(self):
        """Print cost summary."""
        breakdown = self.get_cost_breakdown()
        
        print("\n" + "="*70)
        print("COST TRACKER SUMMARY")
        print("="*70)
        print(f"\nGoogle Queries: {breakdown['google']['queries']}")
        print(f"Google Cost: ${breakdown['google']['cost']:.4f}")
        print(f"\nExa Queries: {breakdown['exa']['queries']}")
        print(f"Exa Cost: ${breakdown['exa']['cost']:.4f}")
        print(f"\nTotal Cost: ${breakdown['total_cost']:.4f}")
        print(f"Savings vs Exa-only: ${breakdown['savings_vs_exa_only']:.4f}")
        print(f"Efficiency Ratio: {breakdown['efficiency_ratio']*100:.1f}% Exa usage")
        print("="*70 + "\n")


class SmartSearchOrchestrator:
    """
    Orchestrate two-tier search: Google (broad) → Filter → Exa (deep).
    
    This minimizes Exa API costs while maintaining quality.
    """
    
    def __init__(self, 
                 google_api_key: Optional[str] = None,
                 google_cx_id: Optional[str] = None,
                 enable_cost_tracking: bool = True):
        """
        Initialize orchestrator.
        
        Args:
            google_api_key: Google Custom Search API key
            google_cx_id: Google Custom Search Engine ID
            enable_cost_tracking: Track API costs
        """
        self.google_api_key = google_api_key or os.getenv('GOOGLE_API_KEY')
        self.google_cx_id = google_cx_id or os.getenv('GOOGLE_CX_ID')
        
        self.cost_tracker = CostTracker() if enable_cost_tracking else None
        
        # Import Exa client
        try:
            from .exa_client import get_exa_client
            self.exa_client = get_exa_client()
        except ImportError:
            logger.warning("Exa client not available")
            self.exa_client = None
    
    def google_search(self, 
                      query: str, 
                      num_results: int = 10,
                      **kwargs) -> List[Dict]:
        """
        Perform Google Custom Search.
        
        Args:
            query: Search query
            num_results: Number of results to return
            **kwargs: Additional parameters (dateRestrict, siteSearch, etc.)
        
        Returns:
            List of search results with url, title, snippet, domain
        """
        if not self.google_api_key or not self.google_cx_id:
            logger.error("Google API credentials not configured")
            return []
        
        try:
            import requests
            
            # Google Custom Search API endpoint
            url = "https://www.googleapis.com/customsearch/v1"
            
            params = {
                'key': self.google_api_key,
                'cx': self.google_cx_id,
                'q': query,
                'num': min(num_results, 10)  # Max 10 per request
            }
            
            # Add optional parameters
            if 'dateRestrict' in kwargs:
                params['dateRestrict'] = kwargs['dateRestrict']  # e.g., 'd7' = last 7 days
            
            if 'siteSearch' in kwargs:
                params['siteSearch'] = kwargs['siteSearch']  # e.g., 'careers.microsoft.com'
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Track cost
            if self.cost_tracker:
                self.cost_tracker.log_google_query()
            
            # Parse results
            results = []
            for item in data.get('items', []):
                results.append({
                    'url': item.get('link'),
                    'title': item.get('title'),
                    'snippet': item.get('snippet'),
                    'domain': self._extract_domain(item.get('link', '')),
                    'source': 'google'
                })
            
            logger.info(f"Google search returned {len(results)} results for: {query}")
            return results
        
        except Exception as e:
            logger.error(f"Google search failed: {e}")
            return []
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc.replace('www.', '')
        except:
            return ''
    
    def filter_results(self, 
                       results: List[Dict], 
                       filter_config: Optional[SearchFilter] = None) -> List[Dict]:
        """
        Filter Google results before sending to Exa.
        
        Args:
            results: List of Google search results
            filter_config: SearchFilter instance (or None for default)
        
        Returns:
            Filtered list of results
        """
        if filter_config is None:
            filter_config = SearchFilter()
        
        filtered = []
        for result in results:
            if filter_config.passes_filter(result):
                filtered.append(result)
        
        logger.info(f"Filtered {len(results)} → {len(filtered)} results ({len(filtered)/max(len(results),1)*100:.1f}% pass rate)")
        return filtered
    
    def exa_deep_analysis(self, 
                          urls: List[str], 
                          batch_size: int = 10) -> List[Dict]:
        """
        Perform Exa deep analysis on filtered URLs.
        
        Args:
            urls: List of URLs to analyze
            batch_size: Process URLs in batches (rate limiting)
        
        Returns:
            List of Exa enrichment results
        """
        if not self.exa_client:
            logger.error("Exa client not available")
            return []
        
        results = []
        
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i+batch_size]
            
            logger.info(f"Processing Exa batch {i//batch_size + 1}: {len(batch)} URLs")
            
            for url in batch:
                try:
                    # Get page content via Exa
                    content = self.exa_client.get_contents([url])
                    
                    if content and len(content) > 0:
                        results.append({
                            'url': url,
                            'content': content[0],
                            'source': 'exa'
                        })
                    
                    # Track cost
                    if self.cost_tracker:
                        self.cost_tracker.log_exa_query()
                    
                    # Rate limiting
                    time.sleep(0.1)  # 10 requests/second max
                
                except Exception as e:
                    logger.error(f"Exa analysis failed for {url}: {e}")
        
        logger.info(f"Exa deep analysis complete: {len(results)}/{len(urls)} successful")
        return results
    
    def smart_search(self,
                     query: str,
                     num_google_results: int = 50,
                     filter_config: Optional[SearchFilter] = None,
                     custom_filter: Optional[Callable] = None) -> Dict:
        """
        Execute two-tier smart search.
        
        Args:
            query: Search query
            num_google_results: Number of Google results to fetch
            filter_config: SearchFilter instance
            custom_filter: Optional custom filter function(result) -> bool
        
        Returns:
            Dict with google_results, filtered_results, exa_results, cost_summary
        """
        logger.info(f"Starting smart search for: {query}")
        
        # Stage 1: Google Search (broad, cheap)
        google_results = self.google_search(query, num_results=num_google_results)
        
        # Stage 2: Filter (reduce to high-quality candidates)
        filtered_results = self.filter_results(google_results, filter_config)
        
        # Apply custom filter if provided
        if custom_filter:
            filtered_results = [r for r in filtered_results if custom_filter(r)]
            logger.info(f"Custom filter applied: {len(filtered_results)} results remain")
        
        # Stage 3: Exa Deep Analysis (expensive, high-quality)
        urls = [r['url'] for r in filtered_results]
        exa_results = self.exa_deep_analysis(urls)
        
        # Cost summary
        cost_summary = self.cost_tracker.get_cost_breakdown() if self.cost_tracker else {}
        
        return {
            'query': query,
            'google_results': google_results,
            'filtered_results': filtered_results,
            'exa_results': exa_results,
            'cost_summary': cost_summary,
            'stats': {
                'google_count': len(google_results),
                'filtered_count': len(filtered_results),
                'exa_count': len(exa_results),
                'filter_efficiency': len(filtered_results) / max(len(google_results), 1) * 100,
                'exa_success_rate': len(exa_results) / max(len(filtered_results), 1) * 100
            }
        }
    
    def print_search_summary(self, result: Dict):
        """Print search summary."""
        print("\n" + "="*70)
        print(f"SMART SEARCH SUMMARY: {result['query']}")
        print("="*70)
        
        stats = result['stats']
        print(f"\nStage 1 - Google Search: {stats['google_count']} results")
        print(f"Stage 2 - Filtering: {stats['filtered_count']} results ({stats['filter_efficiency']:.1f}% pass rate)")
        print(f"Stage 3 - Exa Analysis: {stats['exa_count']} results ({stats['exa_success_rate']:.1f}% success)")
        
        if result.get('cost_summary'):
            cost = result['cost_summary']
            print(f"\nCost Breakdown:")
            print(f"  Google: ${cost['google']['cost']:.4f} ({cost['google']['queries']} queries)")
            print(f"  Exa: ${cost['exa']['cost']:.4f} ({cost['exa']['queries']} queries)")
            print(f"  Total: ${cost['total_cost']:.4f}")
            print(f"  Savings vs Exa-only: ${cost['savings_vs_exa_only']:.4f}")
        
        print("="*70 + "\n")


# Singleton instance
_orchestrator_instance = None


def get_smart_search_orchestrator() -> SmartSearchOrchestrator:
    """Get singleton orchestrator instance."""
    global _orchestrator_instance
    
    if _orchestrator_instance is None:
        _orchestrator_instance = SmartSearchOrchestrator()
    
    return _orchestrator_instance


def create_careers_page_filter() -> SearchFilter:
    """
    Create a filter optimized for careers pages.
    
    Returns:
        SearchFilter configured for job/career searches
    """
    filter_config = SearchFilter()
    
    # Require careers-related URL patterns
    filter_config.required_url_patterns = [
        'career', 'careers', 'jobs', 'job', 
        'opportunities', 'hiring', 'work-with-us',
        'join', 'positions', 'openings'
    ]
    
    # Block non-careers pages
    filter_config.blocked_url_patterns = [
        'login', 'signup', 'signin', 'register',
        'cart', 'checkout', 'shop', 'store',
        'blog', 'news', 'press', 'media',
        'privacy', 'terms', 'legal', 'cookie'
    ]
    
    # Prefer HTTPS
    filter_config.require_https = True
    
    # Recent pages only (optional)
    # filter_config.max_age_days = 90
    
    return filter_config


def create_product_page_filter() -> SearchFilter:
    """
    Create a filter optimized for product/solution pages.
    
    Returns:
        SearchFilter configured for product searches
    """
    filter_config = SearchFilter()
    
    filter_config.required_url_patterns = [
        'product', 'products', 'solution', 'solutions',
        'platform', 'service', 'services', 'offering'
    ]
    
    filter_config.blocked_url_patterns = [
        'login', 'signup', 'cart', 'checkout',
        'support', 'help', 'faq', 'doc', 'documentation',
        'privacy', 'terms', 'legal'
    ]
    
    filter_config.require_https = True
    
    return filter_config


if __name__ == "__main__":
    # Example usage
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     SMART SEARCH ORCHESTRATOR - TWO-TIER COST OPTIMIZATION      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize
    orchestrator = get_smart_search_orchestrator()
    
    # Create filter for careers pages
    careers_filter = create_careers_page_filter()
    
    # Example search
    query = "Microsoft careers software engineer"
    
    print(f"Executing smart search: {query}\n")
    
    result = orchestrator.smart_search(
        query=query,
        num_google_results=20,
        filter_config=careers_filter
    )
    
    # Print summary
    orchestrator.print_search_summary(result)
    
    # Print cost tracker
    if orchestrator.cost_tracker:
        orchestrator.cost_tracker.print_summary()
