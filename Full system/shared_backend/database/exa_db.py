"""
Exa Database Connector
======================
Purpose: Database operations for Exa deep web search integration.

This module provides functions to:
- Store and retrieve company sources (web pages)
- Manage company keywords and signals
- Track enrichment crawls and jobs
- Log API usage and metrics

Dependencies:
- PostgreSQL with exa_schema.sql applied
- SQLAlchemy for ORM
- psycopg2 for connection
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4

try:
    from sqlalchemy import create_engine, text, and_, or_, desc, func
    from sqlalchemy.orm import sessionmaker, Session
    from sqlalchemy.pool import NullPool
except ImportError:
    print("⚠️  SQLAlchemy not installed. Run: pip install sqlalchemy psycopg2-binary")
    raise

# Database connection configuration
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', 'intellicv'),
    'user': os.getenv('POSTGRES_USER', 'intellicv'),
    'password': os.getenv('POSTGRES_PASSWORD', 'changeme'),
}

# Global engine and session factory
_engine = None
_SessionFactory = None

def get_engine():
    """Get or create SQLAlchemy engine."""
    global _engine
    if _engine is None:
        connection_string = (
            f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
            f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )
        _engine = create_engine(connection_string, poolclass=NullPool, echo=False)
    return _engine

def get_session() -> Session:
    """Get a new database session."""
    global _SessionFactory
    if _SessionFactory is None:
        _SessionFactory = sessionmaker(bind=get_engine())
    return _SessionFactory()

def close_engine():
    """Close the database engine."""
    global _engine, _SessionFactory
    if _engine:
        _engine.dispose()
        _engine = None
        _SessionFactory = None


# ============================================================================
# COMPANY SOURCES - Store discovered web pages
# ============================================================================

def save_company_source(
    domain: str,
    url: str,
    title: str,
    content_type: str,
    text_content: Optional[str] = None,
    html_content: Optional[str] = None,
    exa_id: Optional[str] = None,
    exa_score: Optional[float] = None,
    search_query: Optional[str] = None,
    search_mode: Optional[str] = None,
    search_keywords: Optional[List[str]] = None,
    company_name: Optional[str] = None,
    published_date: Optional[datetime] = None,
    author: Optional[str] = None,
) -> UUID:
    """
    Save a company source page to the database.
    
    Args:
        domain: Company domain (e.g., 'microsoft.com')
        url: Full URL of the page
        title: Page title
        content_type: Type of content ('careers', 'products', 'background', etc.)
        text_content: Main page text
        html_content: Raw HTML (optional)
        exa_id: Exa's internal ID
        exa_score: Relevance score from Exa (0-1)
        search_query: Query that found this page
        search_mode: Search mode used ('auto', 'fast', 'deep')
        search_keywords: List of keywords used in search
        company_name: Company name
        published_date: Publication date (if available)
        author: Author (if available)
    
    Returns:
        UUID of the saved source
    """
    session = get_session()
    try:
        # Check if URL already exists for this domain
        existing = session.execute(
            text("""
                SELECT id FROM company_sources 
                WHERE domain = :domain AND url = :url
            """),
            {'domain': domain, 'url': url}
        ).fetchone()
        
        if existing:
            # Update existing record
            source_id = existing[0]
            session.execute(
                text("""
                    UPDATE company_sources SET
                        title = :title,
                        content_type = :content_type,
                        text_content = :text_content,
                        html_content = :html_content,
                        exa_id = :exa_id,
                        exa_score = :exa_score,
                        search_query = :search_query,
                        search_mode = :search_mode,
                        search_keywords = :search_keywords,
                        company_name = :company_name,
                        published_date = :published_date,
                        author = :author,
                        updated_at = CURRENT_TIMESTAMP,
                        last_checked = CURRENT_TIMESTAMP
                    WHERE id = :id
                """),
                {
                    'id': source_id,
                    'title': title,
                    'content_type': content_type,
                    'text_content': text_content,
                    'html_content': html_content,
                    'exa_id': exa_id,
                    'exa_score': exa_score,
                    'search_query': search_query,
                    'search_mode': search_mode,
                    'search_keywords': search_keywords,
                    'company_name': company_name,
                    'published_date': published_date,
                    'author': author,
                }
            )
        else:
            # Insert new record
            source_id = uuid4()
            session.execute(
                text("""
                    INSERT INTO company_sources (
                        id, domain, url, title, content_type, text_content,
                        html_content, exa_id, exa_score, search_query, search_mode,
                        search_keywords, company_name, published_date, author,
                        last_checked
                    ) VALUES (
                        :id, :domain, :url, :title, :content_type, :text_content,
                        :html_content, :exa_id, :exa_score, :search_query, :search_mode,
                        :search_keywords, :company_name, :published_date, :author,
                        CURRENT_TIMESTAMP
                    )
                """),
                {
                    'id': source_id,
                    'domain': domain,
                    'url': url,
                    'title': title,
                    'content_type': content_type,
                    'text_content': text_content,
                    'html_content': html_content,
                    'exa_id': exa_id,
                    'exa_score': exa_score,
                    'search_query': search_query,
                    'search_mode': search_mode,
                    'search_keywords': search_keywords,
                    'company_name': company_name,
                    'published_date': published_date,
                    'author': author,
                }
            )
        
        session.commit()
        return source_id
    
    except Exception as e:
        session.rollback()
        raise Exception(f"Failed to save company source: {e}")
    finally:
        session.close()


def get_company_sources(
    domain: str,
    content_type: Optional[str] = None,
    limit: int = 50
) -> List[Dict[str, Any]]:
    """
    Get company sources for a domain.
    
    Args:
        domain: Company domain
        content_type: Filter by content type (optional)
        limit: Maximum results to return
    
    Returns:
        List of source dictionaries
    """
    session = get_session()
    try:
        query = """
            SELECT 
                id, domain, company_name, url, title, content_type,
                text_content, exa_score, search_query, created_at
            FROM company_sources
            WHERE domain = :domain AND status = 'active'
        """
        params = {'domain': domain, 'limit': limit}
        
        if content_type:
            query += " AND content_type = :content_type"
            params['content_type'] = content_type
        
        query += " ORDER BY exa_score DESC, created_at DESC LIMIT :limit"
        
        results = session.execute(text(query), params).fetchall()
        
        return [
            {
                'id': str(row[0]),
                'domain': row[1],
                'company_name': row[2],
                'url': row[3],
                'title': row[4],
                'content_type': row[5],
                'text_content': row[6],
                'exa_score': float(row[7]) if row[7] else None,
                'search_query': row[8],
                'created_at': row[9].isoformat() if row[9] else None,
            }
            for row in results
        ]
    
    finally:
        session.close()


# ============================================================================
# COMPANY CRAWLS - Track enrichment jobs
# ============================================================================

def create_company_crawl(
    domain: str,
    crawl_type: str,
    search_types: List[str],
    triggered_by: str,
    triggered_from: str,
    company_name: Optional[str] = None,
) -> UUID:
    """
    Create a new company crawl job.
    
    Args:
        domain: Company domain
        crawl_type: Type of crawl ('manual', 'scheduled', 'auto', 'webset')
        search_types: List of search types (['careers', 'products', 'background'])
        triggered_by: User or system that triggered
        triggered_from: Source ('admin_page_27', 'background_worker', etc.)
        company_name: Company name (optional)
    
    Returns:
        UUID of the crawl job
    """
    session = get_session()
    try:
        crawl_id = uuid4()
        session.execute(
            text("""
                INSERT INTO company_crawls (
                    id, domain, company_name, crawl_type, search_types,
                    triggered_by, triggered_from, status
                ) VALUES (
                    :id, :domain, :company_name, :crawl_type, :search_types,
                    :triggered_by, :triggered_from, 'pending'
                )
            """),
            {
                'id': crawl_id,
                'domain': domain,
                'company_name': company_name,
                'crawl_type': crawl_type,
                'search_types': search_types,
                'triggered_by': triggered_by,
                'triggered_from': triggered_from,
            }
        )
        session.commit()
        return crawl_id
    
    except Exception as e:
        session.rollback()
        raise Exception(f"Failed to create company crawl: {e}")
    finally:
        session.close()


def update_crawl_status(
    crawl_id: UUID,
    status: str,
    total_pages_found: Optional[int] = None,
    careers_pages_found: Optional[int] = None,
    products_pages_found: Optional[int] = None,
    background_pages_found: Optional[int] = None,
    duration_seconds: Optional[int] = None,
    api_calls_made: Optional[int] = None,
    cache_hits: Optional[int] = None,
    corpus_path: Optional[str] = None,
    error_message: Optional[str] = None,
) -> None:
    """
    Update a crawl job's status and metrics.
    
    Args:
        crawl_id: Crawl job ID
        status: New status ('running', 'completed', 'failed', 'cancelled')
        total_pages_found: Total pages found
        careers_pages_found: Careers pages found
        products_pages_found: Products pages found
        background_pages_found: Background pages found
        duration_seconds: Duration in seconds
        api_calls_made: Number of API calls
        cache_hits: Cache hits
        corpus_path: Path to corpus file
        error_message: Error message if failed
    """
    session = get_session()
    try:
        update_fields = ['status = :status', 'updated_at = CURRENT_TIMESTAMP']
        params = {'id': crawl_id, 'status': status}
        
        if status == 'running':
            update_fields.append('started_at = CURRENT_TIMESTAMP')
        elif status in ('completed', 'failed', 'cancelled'):
            update_fields.append('completed_at = CURRENT_TIMESTAMP')
        
        if total_pages_found is not None:
            update_fields.append('total_pages_found = :total_pages_found')
            params['total_pages_found'] = total_pages_found
        
        if careers_pages_found is not None:
            update_fields.append('careers_pages_found = :careers_pages_found')
            params['careers_pages_found'] = careers_pages_found
        
        if products_pages_found is not None:
            update_fields.append('products_pages_found = :products_pages_found')
            params['products_pages_found'] = products_pages_found
        
        if background_pages_found is not None:
            update_fields.append('background_pages_found = :background_pages_found')
            params['background_pages_found'] = background_pages_found
        
        if duration_seconds is not None:
            update_fields.append('duration_seconds = :duration_seconds')
            params['duration_seconds'] = duration_seconds
        
        if api_calls_made is not None:
            update_fields.append('api_calls_made = :api_calls_made')
            params['api_calls_made'] = api_calls_made
        
        if cache_hits is not None:
            update_fields.append('cache_hits = :cache_hits')
            params['cache_hits'] = cache_hits
        
        if corpus_path is not None:
            update_fields.append('corpus_path = :corpus_path')
            params['corpus_path'] = corpus_path
        
        if error_message is not None:
            update_fields.append('error_message = :error_message')
            params['error_message'] = error_message
        
        query = f"UPDATE company_crawls SET {', '.join(update_fields)} WHERE id = :id"
        session.execute(text(query), params)
        session.commit()
    
    except Exception as e:
        session.rollback()
        raise Exception(f"Failed to update crawl status: {e}")
    finally:
        session.close()


def get_crawl_history(domain: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get crawl history for a domain.
    
    Args:
        domain: Company domain
        limit: Maximum results to return
    
    Returns:
        List of crawl dictionaries
    """
    session = get_session()
    try:
        results = session.execute(
            text("""
                SELECT 
                    id, domain, company_name, crawl_type, status,
                    total_pages_found, careers_pages_found, products_pages_found,
                    background_pages_found, duration_seconds, created_at,
                    completed_at, triggered_by, error_message
                FROM company_crawls
                WHERE domain = :domain
                ORDER BY created_at DESC
                LIMIT :limit
            """),
            {'domain': domain, 'limit': limit}
        ).fetchall()
        
        return [
            {
                'id': str(row[0]),
                'domain': row[1],
                'company_name': row[2],
                'crawl_type': row[3],
                'status': row[4],
                'total_pages_found': row[5],
                'careers_pages_found': row[6],
                'products_pages_found': row[7],
                'background_pages_found': row[8],
                'duration_seconds': row[9],
                'created_at': row[10].isoformat() if row[10] else None,
                'completed_at': row[11].isoformat() if row[11] else None,
                'triggered_by': row[12],
                'error_message': row[13],
            }
            for row in results
        ]
    
    finally:
        session.close()


# ============================================================================
# EXA API USAGE - Track API calls and billing
# ============================================================================

def log_api_usage(
    endpoint: str,
    method: str,
    query: Optional[str] = None,
    domain: Optional[str] = None,
    search_mode: Optional[str] = None,
    num_results: Optional[int] = None,
    results_returned: Optional[int] = None,
    response_time_ms: Optional[int] = None,
    status_code: Optional[int] = None,
    credits_used: Optional[float] = None,
    crawl_id: Optional[UUID] = None,
    triggered_by: Optional[str] = None,
    triggered_from: Optional[str] = None,
    error_type: Optional[str] = None,
    error_message: Optional[str] = None,
) -> UUID:
    """
    Log an Exa API call for usage tracking.
    
    Args:
        endpoint: API endpoint ('/search', '/findSimilar', '/contents')
        method: Method called ('search', 'search_domain', 'find_similar', etc.)
        query: Search query
        domain: Domain searched
        search_mode: Search mode ('auto', 'fast', 'deep')
        num_results: Number of results requested
        results_returned: Number of results actually returned
        response_time_ms: Response time in milliseconds
        status_code: HTTP status code
        credits_used: Exa API credits consumed
        crawl_id: Related crawl job ID
        triggered_by: User or system
        triggered_from: Source location
        error_type: Error type if failed
        error_message: Error message if failed
    
    Returns:
        UUID of the usage log entry
    """
    session = get_session()
    try:
        usage_id = uuid4()
        session.execute(
            text("""
                INSERT INTO exa_api_usage (
                    id, endpoint, method, query, domain, search_mode,
                    num_results, results_returned, response_time_ms,
                    status_code, credits_used, crawl_id, triggered_by,
                    triggered_from, error_type, error_message
                ) VALUES (
                    :id, :endpoint, :method, :query, :domain, :search_mode,
                    :num_results, :results_returned, :response_time_ms,
                    :status_code, :credits_used, :crawl_id, :triggered_by,
                    :triggered_from, :error_type, :error_message
                )
            """),
            {
                'id': usage_id,
                'endpoint': endpoint,
                'method': method,
                'query': query,
                'domain': domain,
                'search_mode': search_mode,
                'num_results': num_results,
                'results_returned': results_returned,
                'response_time_ms': response_time_ms,
                'status_code': status_code,
                'credits_used': credits_used,
                'crawl_id': crawl_id,
                'triggered_by': triggered_by,
                'triggered_from': triggered_from,
                'error_type': error_type,
                'error_message': error_message,
            }
        )
        session.commit()
        return usage_id
    
    except Exception as e:
        session.rollback()
        raise Exception(f"Failed to log API usage: {e}")
    finally:
        session.close()


def get_api_usage_stats(days: int = 7) -> Dict[str, Any]:
    """
    Get API usage statistics for the last N days.
    
    Args:
        days: Number of days to look back
    
    Returns:
        Dictionary with usage statistics
    """
    session = get_session()
    try:
        cutoff = datetime.now() - timedelta(days=days)
        
        result = session.execute(
            text("""
                SELECT 
                    COUNT(*) as total_calls,
                    SUM(results_returned) as total_results,
                    AVG(response_time_ms) as avg_response_time_ms,
                    SUM(credits_used) as total_credits_used,
                    COUNT(DISTINCT domain) as unique_domains,
                    COUNT(CASE WHEN status_code != 200 THEN 1 END) as failed_calls
                FROM exa_api_usage
                WHERE created_at >= :cutoff
            """),
            {'cutoff': cutoff}
        ).fetchone()
        
        return {
            'total_calls': result[0] or 0,
            'total_results': result[1] or 0,
            'avg_response_time_ms': float(result[2]) if result[2] else 0,
            'total_credits_used': float(result[3]) if result[3] else 0,
            'unique_domains': result[4] or 0,
            'failed_calls': result[5] or 0,
            'days': days,
        }
    
    finally:
        session.close()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_enrichment_summary(domain: str) -> Optional[Dict[str, Any]]:
    """
    Get the latest enrichment summary for a domain.
    
    Args:
        domain: Company domain
    
    Returns:
        Dictionary with enrichment summary or None
    """
    session = get_session()
    try:
        result = session.execute(
            text("""
                SELECT * FROM v_company_enrichment_summary
                WHERE domain = :domain
            """),
            {'domain': domain}
        ).fetchone()
        
        if not result:
            return None
        
        return {
            'domain': result[0],
            'company_name': result[1],
            'status': result[2],
            'total_pages_found': result[3],
            'careers_pages_found': result[4],
            'products_pages_found': result[5],
            'background_pages_found': result[6],
            'completed_at': result[7].isoformat() if result[7] else None,
            'duration_seconds': result[8],
            'total_sources': result[9],
            'total_keywords': result[10],
        }
    
    finally:
        session.close()


def health_check() -> Dict[str, Any]:
    """
    Check database connectivity and table existence.
    
    Returns:
        Dictionary with health check results
    """
    try:
        session = get_session()
        
        # Check if tables exist
        tables = ['company_sources', 'company_keywords', 'company_crawls', 'exa_api_usage']
        existing_tables = []
        
        for table in tables:
            result = session.execute(
                text(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table}')")
            ).fetchone()
            if result and result[0]:
                existing_tables.append(table)
        
        session.close()
        
        return {
            'status': 'healthy' if len(existing_tables) == len(tables) else 'degraded',
            'database': DB_CONFIG['database'],
            'tables_expected': len(tables),
            'tables_found': len(existing_tables),
            'missing_tables': [t for t in tables if t not in existing_tables],
        }
    
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e),
        }
