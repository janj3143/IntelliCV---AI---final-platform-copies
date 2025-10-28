"""
Exa (EXE) Deep Web Search Client
=================================
Wrapper for Exa API with IntelliCV-specific features.

Features:
- Semantic search with auto/fast/deep modes
- Domain-scoped searches
- Similar page discovery
- Content extraction with citations
- Rate limiting and caching support
"""

import os
import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import hashlib
import time

logger = logging.getLogger(__name__)

class ExaClient:
    """
    Exa deep search client with caching and rate limiting.
    
    Usage:
        client = ExaClient()
        results = client.search("site:microsoft.com careers")
        
    Environment Variables:
        EXA_API_KEY: Your Exa API key (required)
        EXA_BASE_URL: API base URL (default: https://api.exa.ai)
        EXA_SEARCH_MODE: Default search mode (auto/fast/deep)
        EXA_MAX_RESULTS: Max results per search (default: 50)
        EXA_RATE_LIMIT: Requests per minute (default: 100)
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize Exa client.
        
        Args:
            api_key: Exa API key (defaults to EXA_API_KEY env var)
            base_url: API base URL (defaults to EXA_BASE_URL env var)
        
        Raises:
            ValueError: If API key not provided or found in environment
        """
        self.api_key = api_key or os.getenv("EXA_API_KEY")
        self.base_url = base_url or os.getenv("EXA_BASE_URL", "https://api.exa.ai")
        self.search_mode = os.getenv("EXA_SEARCH_MODE", "auto")
        self.max_results = int(os.getenv("EXA_MAX_RESULTS", "50"))
        self.rate_limit = int(os.getenv("EXA_RATE_LIMIT", "100"))
        
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        # Rate limiting
        self._request_times = []
        
        if not self.api_key:
            raise ValueError(
                "EXA_API_KEY not found. Please set it in environment variables or pass to constructor."
            )
        
        logger.info(f"Exa client initialized (mode={self.search_mode}, max_results={self.max_results})")
    
    def _check_rate_limit(self):
        """Check and enforce rate limiting."""
        now = time.time()
        # Remove requests older than 1 minute
        self._request_times = [t for t in self._request_times if now - t < 60]
        
        if len(self._request_times) >= self.rate_limit:
            sleep_time = 60 - (now - self._request_times[0])
            if sleep_time > 0:
                logger.warning(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
        
        self._request_times.append(now)
    
    def search(
        self,
        query: str,
        num_results: int = 10,
        search_mode: Optional[str] = None,
        use_autoprompt: bool = True,
        include_content: bool = True,
        include_citations: bool = True,
        start_published_date: Optional[str] = None,
        end_published_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute Exa semantic search.
        
        Args:
            query: Search query (supports site: operators, semantic queries)
            num_results: Number of results to return (max 50)
            search_mode: Search depth (auto/fast/deep, defaults to config)
            use_autoprompt: Let Exa optimize query for better results
            include_content: Include extracted text content
            include_citations: Include source citations
            start_published_date: Filter by publish date (YYYY-MM-DD)
            end_published_date: Filter by publish date (YYYY-MM-DD)
        
        Returns:
            Dict with search results, including:
                - results: List of result objects
                - autoprompt_string: Optimized query (if use_autoprompt=True)
                - request_id: Unique request identifier
        
        Raises:
            requests.exceptions.RequestException: If API request fails
        
        Example:
            results = client.search(
                "site:microsoft.com careers OR jobs",
                num_results=10,
                search_mode="deep"
            )
        """
        self._check_rate_limit()
        
        mode = search_mode or self.search_mode
        
        payload = {
            "query": query,
            "num_results": min(num_results, self.max_results),
            "type": mode,
            "use_autoprompt": use_autoprompt,
            "contents": {
                "text": include_content
            }
        }
        
        # Add date filters if provided
        if start_published_date:
            payload["start_published_date"] = start_published_date
        if end_published_date:
            payload["end_published_date"] = end_published_date
        
        try:
            logger.info(f"Exa search: '{query[:50]}...' (mode={mode}, results={num_results})")
            
            response = requests.post(
                f"{self.base_url}/search",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            results = response.json()
            
            # Log search metadata
            result_count = len(results.get('results', []))
            logger.info(f"Exa search completed: {result_count} results found")
            
            # Add metadata
            results['_metadata'] = {
                'query': query,
                'mode': mode,
                'timestamp': datetime.now().isoformat(),
                'result_count': result_count
            }
            
            return results
            
        except requests.exceptions.Timeout:
            logger.error(f"Exa search timeout: {query[:50]}...")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Exa search failed: {e}")
            raise
    
    def search_domain(
        self,
        domain: str,
        keywords: List[str],
        num_results: int = 20,
        search_mode: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search within a specific domain.
        
        Args:
            domain: Target domain (e.g., 'microsoft.com')
            keywords: Keywords to search for (joined with OR)
            num_results: Number of results to return
            search_mode: Search depth (auto/fast/deep)
        
        Returns:
            Search results scoped to the domain
        
        Example:
            results = client.search_domain(
                "microsoft.com",
                ["careers", "jobs", "openings"],
                num_results=10
            )
        """
        # Build site-scoped query with OR keywords
        query = f"site:{domain} {' OR '.join(keywords)}"
        
        logger.info(f"Domain search: {domain} with {len(keywords)} keywords")
        
        return self.search(
            query,
            num_results=num_results,
            search_mode=search_mode
        )
    
    def find_similar(
        self,
        url: str,
        num_results: int = 10,
        include_content: bool = True
    ) -> Dict[str, Any]:
        """
        Find pages similar to a given URL.
        
        Args:
            url: Reference URL to find similar pages
            num_results: Number of similar pages to return
            include_content: Include extracted text content
        
        Returns:
            Similar pages with content and scores
        
        Example:
            similar = client.find_similar(
                "https://microsoft.com/careers/engineering",
                num_results=5
            )
        """
        self._check_rate_limit()
        
        payload = {
            "url": url,
            "num_results": num_results,
            "contents": {"text": include_content}
        }
        
        try:
            logger.info(f"Finding similar to: {url}")
            
            response = requests.post(
                f"{self.base_url}/findSimilar",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            results = response.json()
            
            logger.info(f"Found {len(results.get('results', []))} similar pages")
            
            return results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Find similar failed: {e}")
            raise
    
    def get_contents(
        self,
        ids: List[str],
        include_text: bool = True,
        include_html: bool = False
    ) -> Dict[str, Any]:
        """
        Get full contents for specific result IDs.
        
        Args:
            ids: List of Exa result IDs
            include_text: Include extracted text
            include_html: Include raw HTML
        
        Returns:
            Full content for specified results
        """
        self._check_rate_limit()
        
        payload = {
            "ids": ids,
            "contents": {
                "text": include_text,
                "html": include_html
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/contents",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Get contents failed: {e}")
            raise
    
    def health_check(self) -> bool:
        """
        Check if Exa API is accessible.
        
        Returns:
            True if API is healthy, False otherwise
        """
        try:
            # Simple search to verify API access
            result = self.search("test", num_results=1, use_autoprompt=False)
            return True
        except Exception as e:
            logger.error(f"Exa health check failed: {e}")
            return False
    
    def get_cache_key(self, query: str, num_results: int, mode: str) -> str:
        """
        Generate cache key for a search query.
        
        Args:
            query: Search query
            num_results: Number of results
            mode: Search mode
        
        Returns:
            MD5 hash suitable for caching
        """
        key_string = f"{query}:{num_results}:{mode}"
        return hashlib.md5(key_string.encode()).hexdigest()


# Singleton instance
_exa_client: Optional[ExaClient] = None

def get_exa_client(api_key: Optional[str] = None) -> ExaClient:
    """
    Get or create Exa client singleton.
    
    Args:
        api_key: Optional API key (uses env var if not provided)
    
    Returns:
        ExaClient instance
    
    Example:
        client = get_exa_client()
        results = client.search("artificial intelligence")
    """
    global _exa_client
    
    if _exa_client is None:
        _exa_client = ExaClient(api_key=api_key)
        logger.info("Exa client singleton created")
    
    return _exa_client


def reset_exa_client():
    """Reset the singleton instance (useful for testing)."""
    global _exa_client
    _exa_client = None
    logger.info("Exa client singleton reset")
