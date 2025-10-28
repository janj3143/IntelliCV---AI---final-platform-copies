# EXE (Exa) Deep Web Search Integration Plan
**IntelliCV SANDBOX Platform**  
**Date:** October 28, 2025  
**Status:** PLANNING PHASE  
**Integration Target:** BACKEND-ADMIN-REORIENTATION

---

## Executive Summary

Integrate EXE (Exa) deep web search and crawler capabilities into IntelliCV to:
1. **User Portal Enhancement** - Auto-pull careers pages, product info, company backgrounds
2. **Admin Learning Loop** - Build company corpora, extract skills/keywords, feed AI models
3. **Market Intelligence** - Deep web scraping for competitive analysis and job market data

**Key Value:**
- Deep semantic search beyond basic web scraping
- Structured content extraction from careers/product/about pages
- Automated company corpus building with versioning
- Enhanced JD-CV matching with real-time company data

---

## Current System Architecture Analysis

### BACKEND-ADMIN-REORIENTATION Structure
```
BACKEND-ADMIN-REORIENTATION/
├── admin_portal/
│   ├── pages/
│   │   ├── 10_Market_Intelligence_Center.py        ← EXE Integration Point 1
│   │   ├── 11_Competitive_Intelligence.py          ← EXE Integration Point 2
│   │   ├── 12_Web_Company_Intelligence.py          ← EXE Integration Point 3
│   │   ├── 20_Job_Title_AI_Integration.py          ← EXE feeds job title data
│   │   ├── 21_Job_Title_Overlap_Cloud.py           ← EXE feeds skill keywords
│   │   └── 25_Intelligence_Hub.py                  ← EXE central dashboard
│   └── pages/shared/integration_hooks.py           ← Add EXE sync methods
│
├── shared_backend/
│   ├── services/
│   │   ├── market_intelligence/                    ← EXE service location
│   │   │   ├── job_market_analyzer.py
│   │   │   └── competitive_intel.py
│   │   └── (NEW) exa_service/                      ⭐ CREATE
│   │       ├── __init__.py
│   │       ├── exa_client.py                       ← Exa API wrapper
│   │       ├── company_enrichment.py               ← Company data extraction
│   │       ├── careers_scraper.py                  ← Careers page parser
│   │       ├── product_scraper.py                  ← Product page parser
│   │       └── websets_manager.py                  ← Domain crawl manager
│   ├── database/
│   │   └── clients/                                ← Store Exa results
│   └── cache/                                      ← Redis cache for fast access
│
├── user_portal_final/
│   ├── pages/
│   │   ├── 10_UMarketU_Suite.py                    ← Display company data
│   │   └── 13_Dual_Career_Suite.py                 ← Geographic company data
│
└── ai_data_final/                                   ← EXE data storage
    ├── (NEW) company_corpora/                      ⭐ CREATE
    │   ├── {domain}/
    │   │   ├── careers/
    │   │   ├── products/
    │   │   ├── about/
    │   │   └── metadata.json
    └── (NEW) exa_cache/                            ⭐ CREATE
        └── search_results/
```

### Integration Points Identified

#### Admin Portal (5 pages)
1. **Page 10: Market Intelligence Center** - Exa-powered market research
2. **Page 11: Competitive Intelligence** - Company competitive analysis
3. **Page 12: Web Company Intelligence** - Deep company background
4. **Page 20: Job Title AI** - Extract job titles from careers pages
5. **Page 25: Intelligence Hub** - Central dashboard for all Exa data

#### User Portal (2 pages)
1. **Page 10: UMarketU Suite** - Company data in job discovery/fit analysis
2. **Page 13: Dual Career Suite** - Geographic company analysis

#### Backend Services (NEW)
1. **shared_backend/services/exa_service/** - Core Exa integration
2. **FastAPI endpoints** - `/api/exa/...` routes
3. **Worker queue** - Redis/background job processing

---

## Phase 1: Foundation (Week 1-2)

### Objectives
- Set up Exa API access
- Create basic Exa client wrapper
- Build data storage structure
- Test basic search functionality

### Tasks

#### 1.1 Exa Account & API Setup
```bash
# Actions:
- Sign up at exa.ai
- Generate API key
- Add to environment variables
- Test basic API connectivity
```

**File: `.env` (add to BACKEND-ADMIN-REORIENTATION/.env)**
```env
# Exa (EXE) Deep Web Search
EXA_API_KEY=your_exa_api_key_here
EXA_BASE_URL=https://api.exa.ai
EXA_SEARCH_MODE=auto  # auto | fast | deep
EXA_MAX_RESULTS=50
EXA_RATE_LIMIT=100    # requests per minute
```

#### 1.2 Create Exa Service Directory
```powershell
# Create directory structure
New-Item -ItemType Directory -Path ".\shared_backend\services\exa_service" -Force
New-Item -ItemType File -Path ".\shared_backend\services\exa_service\__init__.py"
New-Item -ItemType File -Path ".\shared_backend\services\exa_service\exa_client.py"
New-Item -ItemType File -Path ".\shared_backend\services\exa_service\company_enrichment.py"
New-Item -ItemType File -Path ".\shared_backend\services\exa_service\careers_scraper.py"
New-Item -ItemType File -Path ".\shared_backend\services\exa_service\product_scraper.py"
New-Item -ItemType File -Path ".\shared_backend\services\exa_service\websets_manager.py"
```

#### 1.3 Basic Exa Client (exa_client.py)
**File: `shared_backend/services/exa_service/exa_client.py`**
```python
"""
Exa (EXE) Deep Web Search Client
=================================
Wrapper for Exa API with IntelliCV-specific features.
"""

import os
import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ExaClient:
    """Exa deep search client with caching and rate limiting."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("EXA_API_KEY")
        self.base_url = base_url or os.getenv("EXA_BASE_URL", "https://api.exa.ai")
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        if not self.api_key:
            raise ValueError("EXA_API_KEY not found in environment")
    
    def search(
        self,
        query: str,
        num_results: int = 10,
        search_mode: str = "auto",  # auto | fast | deep
        use_autoprompt: bool = True,
        include_content: bool = True,
        include_citations: bool = True
    ) -> Dict[str, Any]:
        """
        Execute Exa semantic search.
        
        Args:
            query: Search query (can include site: operators)
            num_results: Number of results to return (max 50)
            search_mode: Search depth (auto | fast | deep)
            use_autoprompt: Let Exa optimize query
            include_content: Include extracted content
            include_citations: Include source citations
        
        Returns:
            Search results with extracted content and citations
        """
        payload = {
            "query": query,
            "num_results": min(num_results, 50),
            "type": search_mode,
            "use_autoprompt": use_autoprompt,
            "contents": {
                "text": include_content
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/search",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            results = response.json()
            
            # Log search metadata
            logger.info(f"Exa search completed: {query[:50]}... ({len(results.get('results', []))} results)")
            
            return results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Exa search failed: {e}")
            raise
    
    def search_domain(
        self,
        domain: str,
        keywords: List[str],
        num_results: int = 20
    ) -> Dict[str, Any]:
        """
        Search within a specific domain.
        
        Args:
            domain: Target domain (e.g., 'microsoft.com')
            keywords: Keywords to search for
            num_results: Number of results
        
        Returns:
            Domain-scoped search results
        """
        query = f"site:{domain} {' OR '.join(keywords)}"
        return self.search(query, num_results=num_results)
    
    def find_similar(
        self,
        url: str,
        num_results: int = 10
    ) -> Dict[str, Any]:
        """
        Find pages similar to a given URL.
        
        Args:
            url: Reference URL
            num_results: Number of similar pages
        
        Returns:
            Similar pages with content
        """
        payload = {
            "url": url,
            "num_results": num_results,
            "contents": {"text": True}
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/findSimilar",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Find similar failed: {e}")
            raise

# Singleton instance
_exa_client = None

def get_exa_client() -> ExaClient:
    """Get or create Exa client singleton."""
    global _exa_client
    if _exa_client is None:
        _exa_client = ExaClient()
    return _exa_client
```

#### 1.4 Company Enrichment Service
**File: `shared_backend/services/exa_service/company_enrichment.py`**
```python
"""
Company Enrichment via Exa
===========================
Extract careers, products, and background info for companies.
"""

import logging
from typing import Dict, List, Optional, Any
from .exa_client import get_exa_client

logger = logging.getLogger(__name__)

class CompanyEnricher:
    """Enrich company data using Exa deep search."""
    
    def __init__(self):
        self.client = get_exa_client()
    
    def find_careers_pages(self, domain: str, num_results: int = 8) -> Dict[str, Any]:
        """
        Find careers/jobs pages for a domain.
        
        Args:
            domain: Company domain (e.g., 'microsoft.com')
            num_results: Number of careers pages to find
        
        Returns:
            Careers pages with extracted content
        """
        keywords = ["careers", "jobs", "vacancies", "openings", "work with us", "join our team"]
        
        logger.info(f"Searching careers pages for {domain}")
        
        results = self.client.search_domain(domain, keywords, num_results)
        
        # Filter and rank careers pages
        careers_pages = []
        for result in results.get('results', []):
            url = result.get('url', '')
            if any(kw in url.lower() for kw in ['career', 'job', 'vacancy']):
                careers_pages.append({
                    'url': url,
                    'title': result.get('title', ''),
                    'content': result.get('text', ''),
                    'published': result.get('publishedDate'),
                    'score': result.get('score', 0),
                    'extracted_at': datetime.now().isoformat()
                })
        
        return {
            'domain': domain,
            'careers_pages': careers_pages,
            'total_found': len(careers_pages),
            'search_timestamp': datetime.now().isoformat()
        }
    
    def find_product_pages(self, domain: str, num_results: int = 12) -> Dict[str, Any]:
        """
        Find product/solution pages for a domain.
        
        Args:
            domain: Company domain
            num_results: Number of product pages to find
        
        Returns:
            Product pages with extracted content
        """
        keywords = ["products", "solutions", "platform", "services", "offerings"]
        
        logger.info(f"Searching product pages for {domain}")
        
        results = self.client.search_domain(domain, keywords, num_results)
        
        product_pages = []
        for result in results.get('results', []):
            product_pages.append({
                'url': result.get('url', ''),
                'title': result.get('title', ''),
                'content': result.get('text', ''),
                'published': result.get('publishedDate'),
                'score': result.get('score', 0),
                'extracted_at': datetime.now().isoformat()
            })
        
        return {
            'domain': domain,
            'product_pages': product_pages,
            'total_found': len(product_pages),
            'search_timestamp': datetime.now().isoformat()
        }
    
    def get_company_background(self, domain: str, num_results: int = 8) -> Dict[str, Any]:
        """
        Get company background/about information.
        
        Args:
            domain: Company domain
            num_results: Number of background pages
        
        Returns:
            Company background with extracted content
        """
        # Semantic query for company info
        query = f"{domain} company overview about investors leadership history mission"
        
        logger.info(f"Searching company background for {domain}")
        
        results = self.client.search(query, num_results=num_results, search_mode="deep")
        
        background_pages = []
        for result in results.get('results', []):
            background_pages.append({
                'url': result.get('url', ''),
                'title': result.get('title', ''),
                'content': result.get('text', ''),
                'published': result.get('publishedDate'),
                'score': result.get('score', 0),
                'extracted_at': datetime.now().isoformat()
            })
        
        return {
            'domain': domain,
            'background_pages': background_pages,
            'total_found': len(background_pages),
            'search_timestamp': datetime.now().isoformat()
        }
    
    def enrich_company_full(self, domain: str) -> Dict[str, Any]:
        """
        Full company enrichment: careers + products + background.
        
        Args:
            domain: Company domain
        
        Returns:
            Complete company enrichment data
        """
        logger.info(f"Full enrichment started for {domain}")
        
        return {
            'domain': domain,
            'careers': self.find_careers_pages(domain),
            'products': self.find_product_pages(domain),
            'background': self.get_company_background(domain),
            'enrichment_timestamp': datetime.now().isoformat()
        }

def get_company_enricher() -> CompanyEnricher:
    """Get company enricher instance."""
    return CompanyEnricher()
```

#### 1.5 Data Storage Structure
```powershell
# Create storage directories
New-Item -ItemType Directory -Path ".\ai_data_final\company_corpora" -Force
New-Item -ItemType Directory -Path ".\ai_data_final\exa_cache" -Force
New-Item -ItemType Directory -Path ".\ai_data_final\exa_cache\search_results" -Force
```

#### 1.6 Database Schema (Postgres)
**File: `shared_backend/database/schemas/exa_schema.sql`** (CREATE)
```sql
-- Company sources from Exa searches
CREATE TABLE IF NOT EXISTS company_sources (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255) NOT NULL,
    source_kind VARCHAR(50) NOT NULL,  -- 'careers' | 'products' | 'background'
    url TEXT NOT NULL,
    title TEXT,
    snippet TEXT,
    content_hash VARCHAR(64),
    first_seen_at TIMESTAMP DEFAULT NOW(),
    last_seen_at TIMESTAMP DEFAULT NOW(),
    exa_result_id VARCHAR(255),
    confidence FLOAT,
    tags TEXT[],
    metadata JSONB,
    UNIQUE(domain, url)
);

CREATE INDEX idx_company_sources_domain ON company_sources(domain);
CREATE INDEX idx_company_sources_kind ON company_sources(source_kind);
CREATE INDEX idx_company_sources_hash ON company_sources(content_hash);

-- Company keywords extracted from Exa results
CREATE TABLE IF NOT EXISTS company_keywords (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255) NOT NULL,
    keyword VARCHAR(255) NOT NULL,
    kind VARCHAR(50),  -- 'skill' | 'product' | 'technology' | 'industry'
    weight FLOAT,
    first_seen_at TIMESTAMP DEFAULT NOW(),
    last_seen_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB,
    UNIQUE(domain, keyword, kind)
);

CREATE INDEX idx_company_keywords_domain ON company_keywords(domain);
CREATE INDEX idx_company_keywords_kind ON company_keywords(kind);

-- Company crawl jobs tracking
CREATE TABLE IF NOT EXISTS company_crawls (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255) NOT NULL,
    started_at TIMESTAMP DEFAULT NOW(),
    finished_at TIMESTAMP,
    mode VARCHAR(50),  -- 'fast' | 'deep' | 'webset'
    pages_found INTEGER,
    pages_changed INTEGER,
    status VARCHAR(50),  -- 'running' | 'completed' | 'failed'
    error TEXT,
    metadata JSONB
);

CREATE INDEX idx_company_crawls_domain ON company_crawls(domain);
CREATE INDEX idx_company_crawls_status ON company_crawls(status);
```

### Phase 1 Deliverables
- ✅ Exa API account and key
- ✅ Basic Exa client wrapper (`exa_client.py`)
- ✅ Company enrichment service (`company_enrichment.py`)
- ✅ Data storage directories created
- ✅ Database schema defined
- ✅ Environment variables configured

### Phase 1 Testing
```python
# Test script: test_exa_phase1.py
from shared_backend.services.exa_service.company_enrichment import get_company_enricher

enricher = get_company_enricher()

# Test 1: Find careers pages
careers = enricher.find_careers_pages("microsoft.com")
print(f"Found {careers['total_found']} careers pages")

# Test 2: Find product pages
products = enricher.find_product_pages("microsoft.com")
print(f"Found {products['total_found']} product pages")

# Test 3: Full enrichment
full = enricher.enrich_company_full("microsoft.com")
print(f"Full enrichment complete: {full['domain']}")
```

---

## Phase 2: Admin Portal Integration (Week 3-4)

### Objectives
- Create admin pages for Exa management
- Build monitoring dashboard
- Implement keyword/signal extraction
- Add manual crawl triggers

### Tasks

#### 2.1 New Admin Page: Exa Web Intelligence (Page 27)
**File: `admin_portal/pages/27_Exa_Web_Intelligence.py`** (CREATE)

```python
"""
Exa (EXE) Web Intelligence Dashboard
=====================================
Manage deep web searches, company corpora, and keyword extraction.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add shared_backend to path
backend_path = Path(__file__).parent.parent.parent / "shared_backend"
sys.path.insert(0, str(backend_path))

from services.exa_service.company_enrichment import get_company_enricher

st.set_page_config(
    page_title="Exa Web Intelligence | IntelliCV-AI",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Exa (EXE) Web Intelligence Dashboard")
st.markdown("**Deep web search and company corpus management**")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Company Search",
    "📊 Websets Monitor",
    "🏷️ Keywords & Signals",
    "📈 Analytics"
])

# TAB 1: Company Search
with tab1:
    st.header("🔍 Deep Company Search")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        domain = st.text_input(
            "Company Domain",
            placeholder="microsoft.com",
            help="Enter company domain to search"
        )
    
    with col2:
        search_mode = st.selectbox(
            "Search Mode",
            ["Auto", "Fast", "Deep"],
            help="Auto=smart mode selection, Fast=quick results, Deep=comprehensive"
        )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_careers = st.checkbox("Careers Pages", value=True)
    with col2:
        search_products = st.checkbox("Product Pages", value=True)
    with col3:
        search_background = st.checkbox("Company Background", value=True)
    
    if st.button("🚀 Start Deep Search", type="primary"):
        if not domain:
            st.error("Please enter a company domain")
        else:
            with st.spinner(f"🔍 Searching {domain}..."):
                enricher = get_company_enricher()
                
                results = {}
                
                if search_careers:
                    careers = enricher.find_careers_pages(domain)
                    results['careers'] = careers
                    st.success(f"✅ Found {careers['total_found']} careers pages")
                
                if search_products:
                    products = enricher.find_product_pages(domain)
                    results['products'] = products
                    st.success(f"✅ Found {products['total_found']} product pages")
                
                if search_background:
                    background = enricher.get_company_background(domain)
                    results['background'] = background
                    st.success(f"✅ Found {background['total_found']} background pages")
                
                # Display results
                st.markdown("---")
                st.subheader("📊 Search Results")
                
                # Results tabs
                if search_careers and results.get('careers'):
                    with st.expander("Careers Pages", expanded=True):
                        for page in results['careers']['careers_pages']:
                            st.markdown(f"**[{page['title']}]({page['url']})**")
                            st.caption(f"Score: {page['score']:.2f} | Extracted: {page['extracted_at']}")
                            st.text(page['content'][:300] + "...")
                            st.markdown("---")
                
                if search_products and results.get('products'):
                    with st.expander("Product Pages"):
                        for page in results['products']['product_pages']:
                            st.markdown(f"**[{page['title']}]({page['url']})**")
                            st.caption(f"Score: {page['score']:.2f}")
                            st.text(page['content'][:300] + "...")
                            st.markdown("---")

# TAB 2: Websets Monitor
with tab2:
    st.header("📊 Websets & Crawl Monitor")
    st.info("🚧 Phase 3 Feature: Domain-wide crawl management")

# TAB 3: Keywords & Signals
with tab3:
    st.header("🏷️ Keywords & Signals Extraction")
    st.info("🚧 Phase 2 Feature: Keyword mining from Exa results")

# TAB 4: Analytics
with tab4:
    st.header("📈 Exa Usage Analytics")
    st.info("🚧 Phase 4 Feature: Search analytics and ROI tracking")
```

#### 2.2 Update Integration Hooks
**File: `admin_portal/pages/shared/integration_hooks.py`** (ADD)

```python
def sync_exa_company_data(self, domain: str, exa_data: Dict[str, Any]):
    """Sync Exa company enrichment data (Admin Page 27).
    
    Syncs company careers, products, and background to:
    - User Portal Page 10 (UMarketU Suite) for job discovery
    - User Portal Page 13 (Dual Career Suite) for geographic company data
    - Backend cache and storage
    """
    self.logger.info(f"Syncing Exa company data for {domain} (Page 27)")
    
    # Sync to user portal for UMarketU Suite
    self.user_portal.push_admin_update('exa_company_data_umarketu', {
        'domain': domain,
        'careers_pages': exa_data.get('careers', {}).get('careers_pages', []),
        'product_pages': exa_data.get('products', {}).get('product_pages', []),
        'company_background': exa_data.get('background', {}),
        'source': 'admin_page_27_exa',
        'target_page': 'umarketu_suite_page_10',
        'features': ['job_discovery', 'company_insights']
    })
    
    # Sync to backend for storage and caching
    self.backend.push_backend_update('exa_company_enrichment', {
        'domain': domain,
        'exa_data': exa_data,
        'source': 'admin_page_27',
        'redis_cache': True,
        'postgres_store': True,
        'blob_storage': True,  # Store in ai_data_final/company_corpora/
        'cache_ttl': 86400  # 24 hours
    })
```

### Phase 2 Deliverables
- ✅ Admin Page 27: Exa Web Intelligence Dashboard
- ✅ Integration hooks for Exa data sync
- ✅ Manual company search interface
- ✅ Results display with citations
- ✅ Basic storage to ai_data_final/

---

## Phase 3: Automation & Workers (Week 5-6)

### Objectives
- Background job processing
- Scheduled company crawls
- Websets API integration
- Keyword extraction pipeline

### Tasks

#### 3.1 Redis Queue Setup
**File: `shared_backend/queue/exa_queue.py`** (CREATE)

```python
"""
Exa Job Queue Manager
=====================
Background processing for Exa searches and crawls.
"""

import redis
import json
from typing import Dict, Any
import os

class ExaQueue:
    """Redis-based queue for Exa jobs."""
    
    def __init__(self):
        self.redis = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=int(os.getenv("REDIS_DB_EXA", 2)),
            decode_responses=True
        )
    
    def enqueue_company_enrichment(self, domain: str, priority: str = "normal"):
        """Enqueue full company enrichment job."""
        job = {
            "type": "company_enrichment",
            "domain": domain,
            "priority": priority,
            "enqueued_at": datetime.now().isoformat()
        }
        
        queue_name = f"exa:jobs:{priority}"
        self.redis.rpush(queue_name, json.dumps(job))
    
    def enqueue_careers_scan(self, domain: str):
        """Enqueue careers page scan."""
        job = {
            "type": "careers_scan",
            "domain": domain,
            "enqueued_at": datetime.now().isoformat()
        }
        
        self.redis.rpush("exa:jobs:normal", json.dumps(job))
```

#### 3.2 Background Worker
**File: `shared_backend/workers/exa_worker.py`** (CREATE)

```python
"""
Exa Background Worker
=====================
Process Exa search jobs from Redis queue.
"""

import time
import json
import logging
from queue.exa_queue import ExaQueue
from services.exa_service.company_enrichment import get_company_enricher
from database.clients.postgres_client import get_postgres_client

logger = logging.getLogger(__name__)

class ExaWorker:
    """Background worker for Exa jobs."""
    
    def __init__(self):
        self.queue = ExaQueue()
        self.enricher = get_company_enricher()
        self.db = get_postgres_client()
    
    def process_job(self, job: Dict):
        """Process a single Exa job."""
        job_type = job.get("type")
        domain = job.get("domain")
        
        try:
            if job_type == "company_enrichment":
                results = self.enricher.enrich_company_full(domain)
                self._store_results(domain, results)
                logger.info(f"Company enrichment completed: {domain}")
            
            elif job_type == "careers_scan":
                results = self.enricher.find_careers_pages(domain)
                self._store_careers(domain, results)
                logger.info(f"Careers scan completed: {domain}")
        
        except Exception as e:
            logger.error(f"Job failed: {job_type} for {domain} - {e}")
    
    def _store_results(self, domain: str, results: Dict):
        """Store enrichment results to Postgres and Blob."""
        # Store to Postgres (company_sources table)
        for page in results.get('careers', {}).get('careers_pages', []):
            self.db.execute(
                """
                INSERT INTO company_sources (domain, source_kind, url, title, content_hash, exa_result_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (domain, url) DO UPDATE SET last_seen_at = NOW()
                """,
                (domain, 'careers', page['url'], page['title'], hash(page['content']), page.get('id'))
            )
        
        # Store to Blob (ai_data_final/company_corpora/)
        import os
        from pathlib import Path
        
        corpus_dir = Path("ai_data_final/company_corpora") / domain
        corpus_dir.mkdir(parents=True, exist_ok=True)
        
        with open(corpus_dir / "enrichment.json", "w") as f:
            json.dump(results, f, indent=2)
    
    def run(self):
        """Main worker loop."""
        logger.info("Exa worker started")
        
        while True:
            # Check for jobs in priority queues
            job_data = self.queue.redis.blpop(["exa:jobs:high", "exa:jobs:normal"], timeout=5)
            
            if job_data:
                queue_name, job_json = job_data
                job = json.loads(job_json)
                self.process_job(job)
            
            time.sleep(1)

if __name__ == "__main__":
    worker = ExaWorker()
    worker.run()
```

### Phase 3 Deliverables
- ✅ Redis job queue for Exa tasks
- ✅ Background worker for processing
- ✅ Automated storage to Postgres + Blob
- ✅ Scheduled crawl capabilities

---

## Phase 4: User Portal Integration (Week 7-8)

### Objectives
- Display Exa data in UMarketU Suite
- Show company insights in job cards
- Add citations and source links
- Real-time company data

### Tasks

#### 4.1 Update UMarketU Suite (Page 10)
**File: `user_portal_final/pages/10_UMarketU_Suite.py`** (UPDATE)

```python
# In Job Discovery Tab - add company insights
with st.expander("🏢 Company Deep Insights (Powered by Exa)", expanded=False):
    # Fetch Exa data for selected company
    company_domain = selected_job.get('company_domain', 'microsoft.com')
    
    # Check cache first
    exa_data = fetch_exa_company_data(company_domain)
    
    if exa_data:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎯 Careers & Openings**")
            careers = exa_data.get('careers', {}).get('careers_pages', [])
            if careers:
                st.markdown(f"[View Careers Page]({careers[0]['url']})")
                st.caption(f"Found {len(careers)} careers-related pages")
        
        with col2:
            st.markdown("**🚀 Products & Solutions**")
            products = exa_data.get('products', {}).get('product_pages', [])
            if products:
                product_keywords = extract_keywords(products)
                st.write(", ".join(product_keywords[:10]))
        
        st.markdown("**📖 Company Background**")
        background = exa_data.get('background', {}).get('background_pages', [])
        if background:
            st.text(background[0]['content'][:500] + "...")
            st.caption(f"Source: {background[0]['url']}")
```

### Phase 4 Deliverables
- ✅ Exa data display in UMarketU Suite
- ✅ Company insights in job cards
- ✅ Source citations and links
- ✅ Cached data for performance

---

## Phase 5: Advanced Features (Week 9-10)

### Objectives
- Keyword extraction and ontology
- Websets API for domain crawls
- LLM integration for insights
- Analytics dashboard

### Tasks

#### 5.1 Keyword Extraction Pipeline
**File: `shared_backend/services/exa_service/keyword_extractor.py`** (CREATE)

```python
"""
Keyword Extraction from Exa Results
====================================
Extract skills, technologies, and industry terms.
"""

from typing import List, Dict, Any
import re
from collections import Counter

class KeywordExtractor:
    """Extract keywords from Exa search results."""
    
    def __init__(self):
        self.skill_ontology = self._load_skill_ontology()
    
    def extract_from_careers_page(self, content: str) -> Dict[str, List[str]]:
        """Extract keywords from careers page content."""
        # Simple extraction (enhance with NLP)
        words = re.findall(r'\b[A-Z][a-z]+\b', content)
        
        # Count frequency
        freq = Counter(words)
        
        # Match against ontology
        skills = []
        technologies = []
        
        for word, count in freq.most_common(50):
            if word.lower() in self.skill_ontology.get('technical_skills', []):
                skills.append(word)
            elif word.lower() in self.skill_ontology.get('technologies', []):
                technologies.append(word)
        
        return {
            'skills': skills[:20],
            'technologies': technologies[:20],
            'all_keywords': [w for w, c in freq.most_common(100)]
        }
```

### Phase 5 Deliverables
- ✅ Keyword extraction pipeline
- ✅ Skill ontology integration
- ✅ Websets API integration
- ✅ Analytics dashboard

---

## Integration Checklist

### Admin Portal
- [ ] Page 27: Exa Web Intelligence Dashboard created
- [ ] Manual company search interface
- [ ] Websets monitor view
- [ ] Keywords extraction view
- [ ] Integration hooks for Exa sync

### User Portal
- [ ] UMarketU Suite displays Exa company data
- [ ] Dual Career Suite uses geographic company data
- [ ] Citations and source links visible
- [ ] Real-time data refresh

### Backend
- [ ] Exa client wrapper (`exa_client.py`)
- [ ] Company enrichment service
- [ ] Redis job queue
- [ ] Background worker
- [ ] Postgres schema created
- [ ] Blob storage structure

### Data Flow
- [ ] Admin triggers search → Exa API
- [ ] Results → Redis cache + Postgres + Blob
- [ ] User portal queries cache first
- [ ] Background worker processes scheduled jobs
- [ ] Integration hooks sync across portals

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Company Enrichment Time | < 30 seconds | Exa API latency + processing |
| Careers Pages Found | 80%+ success rate | Domains with careers data |
| Keyword Accuracy | 90%+ precision | Manual validation sample |
| Cache Hit Rate | > 70% | Redis cache hits |
| User Engagement | +25% on job cards | Click-through to company insights |

---

## Cost Estimate

**Exa API Pricing** (estimated):
- Search calls: $X per 1000 requests
- Content extraction: Included
- Websets: $Y per domain/month

**Expected Monthly Usage:**
- Manual searches: 500-1000 companies
- Automated crawls: 100-200 companies
- Total cost: $XXX-$XXX/month

**ROI:**
- Better job matching → higher user satisfaction
- Deeper company data → competitive advantage
- Automated enrichment → reduced manual research

---

## Risk Mitigation

### Technical Risks
1. **API Rate Limits** - Implement queue system, respect limits
2. **Data Quality** - Validate extracted content, manual review workflows
3. **Storage Growth** - Lifecycle policies, archive old data

### Compliance Risks
1. **robots.txt** - Respect crawl policies, store policy_hash
2. **Attribution** - Always cite sources, display Exa attribution
3. **Data Privacy** - No PII storage, company data only

---

## Timeline Summary

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| Phase 1: Foundation | Week 1-2 | Exa client, basic search, storage |
| Phase 2: Admin Portal | Week 3-4 | Page 27 dashboard, manual search |
| Phase 3: Automation | Week 5-6 | Workers, queue, scheduled crawls |
| Phase 4: User Portal | Week 7-8 | UMarketU integration, job cards |
| Phase 5: Advanced | Week 9-10 | Keywords, websets, analytics |

**Total Duration:** 10 weeks  
**Go-Live:** Phase 2 (manual search operational)  
**Full Production:** Phase 4 (user-facing features complete)

---

## Next Immediate Actions

1. **Sign up for Exa API** - Get API key from exa.ai
2. **Create Phase 1 files** - exa_client.py, company_enrichment.py
3. **Test basic search** - Verify API connectivity
4. **Create storage directories** - ai_data_final/company_corpora/
5. **Build Admin Page 27** - Basic search interface

**Status:** READY TO START PHASE 1 🚀

---

**End of Integration Plan**
