"""
Exa (EXE) Deep Web Search Service
==================================
IntelliCV Platform Integration

This service provides deep web search capabilities using the Exa API,
enabling intelligent company research, careers page discovery, and
product intelligence gathering.

Components:
- exa_client: Core API wrapper
- company_enrichment: Company data extraction
- careers_scraper: Careers page parser
- product_scraper: Product page parser
- websets_manager: Domain crawl management
"""

from .exa_client import ExaClient, get_exa_client

__version__ = "1.0.0"
__all__ = ["ExaClient", "get_exa_client"]
