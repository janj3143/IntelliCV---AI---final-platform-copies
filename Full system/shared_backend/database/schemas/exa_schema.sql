-- ============================================================================
-- EXA (EXE) DEEP WEB SEARCH - DATABASE SCHEMA
-- ============================================================================
-- Purpose: Store Exa search results, company enrichment data, and metadata
-- Created: Phase 1 - Foundation (Week 1-2)
-- Dependencies: PostgreSQL 12+, requires UUID extension
-- ============================================================================

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- For text search optimization

-- ============================================================================
-- TABLE: company_sources
-- Purpose: Store all discovered company web pages from Exa searches
-- ============================================================================
CREATE TABLE IF NOT EXISTS company_sources (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Company identification
    domain VARCHAR(255) NOT NULL,
    company_name VARCHAR(500),
    
    -- Page details
    url TEXT NOT NULL,
    title TEXT,
    content_type VARCHAR(50), -- 'careers', 'products', 'background', 'about', 'news'
    
    -- Content
    text_content TEXT, -- Main page text
    html_content TEXT, -- Raw HTML (optional)
    summary TEXT, -- AI-generated summary
    
    -- Metadata
    exa_id VARCHAR(100), -- Exa's internal ID
    exa_score DECIMAL(5, 4), -- Relevance score from Exa (0-1)
    published_date TIMESTAMP, -- If available from Exa
    author VARCHAR(500), -- If available from Exa
    
    -- Search context
    search_query TEXT, -- Query that found this page
    search_mode VARCHAR(20), -- 'auto', 'fast', 'deep'
    search_keywords TEXT[], -- Array of keywords used
    
    -- Status & timestamps
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'archived', 'invalid'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_checked TIMESTAMP, -- Last time we verified the URL
    
    -- Constraints
    CONSTRAINT unique_url_per_domain UNIQUE (domain, url)
);

-- Indexes for company_sources
CREATE INDEX idx_company_sources_domain ON company_sources(domain);
CREATE INDEX idx_company_sources_content_type ON company_sources(content_type);
CREATE INDEX idx_company_sources_created_at ON company_sources(created_at DESC);
CREATE INDEX idx_company_sources_status ON company_sources(status);
CREATE INDEX idx_company_sources_exa_score ON company_sources(exa_score DESC);
CREATE INDEX idx_company_sources_search_keywords ON company_sources USING gin(search_keywords);
CREATE INDEX idx_company_sources_text_search ON company_sources USING gin(to_tsvector('english', text_content));


-- ============================================================================
-- TABLE: company_keywords
-- Purpose: Store extracted keywords and signals from company pages
-- ============================================================================
CREATE TABLE IF NOT EXISTS company_keywords (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Company identification
    domain VARCHAR(255) NOT NULL,
    source_id UUID REFERENCES company_sources(id) ON DELETE CASCADE, -- Link to source page
    
    -- Keyword details
    keyword VARCHAR(500) NOT NULL,
    keyword_type VARCHAR(50), -- 'skill', 'technology', 'industry', 'benefit', 'location', 'role'
    category VARCHAR(100), -- More specific categorization
    
    -- Context
    context TEXT, -- Surrounding text where keyword was found
    frequency INTEGER DEFAULT 1, -- How many times it appears
    
    -- Confidence & validation
    confidence_score DECIMAL(5, 4), -- AI extraction confidence (0-1)
    is_validated BOOLEAN DEFAULT FALSE, -- Human verified
    validated_by VARCHAR(100), -- User who validated
    validated_at TIMESTAMP,
    
    -- Metadata
    extraction_method VARCHAR(50), -- 'regex', 'nlp', 'llm', 'manual'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT unique_keyword_per_source UNIQUE (source_id, keyword, keyword_type)
);

-- Indexes for company_keywords
CREATE INDEX idx_company_keywords_domain ON company_keywords(domain);
CREATE INDEX idx_company_keywords_source_id ON company_keywords(source_id);
CREATE INDEX idx_company_keywords_keyword ON company_keywords(keyword);
CREATE INDEX idx_company_keywords_keyword_type ON company_keywords(keyword_type);
CREATE INDEX idx_company_keywords_confidence ON company_keywords(confidence_score DESC);
CREATE INDEX idx_company_keywords_created_at ON company_keywords(created_at DESC);


-- ============================================================================
-- TABLE: company_crawls
-- Purpose: Track enrichment jobs and crawl history
-- ============================================================================
CREATE TABLE IF NOT EXISTS company_crawls (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Company identification
    domain VARCHAR(255) NOT NULL,
    company_name VARCHAR(500),
    
    -- Crawl details
    crawl_type VARCHAR(50) NOT NULL, -- 'manual', 'scheduled', 'auto', 'webset'
    search_types TEXT[], -- ['careers', 'products', 'background']
    
    -- Results
    total_pages_found INTEGER DEFAULT 0,
    careers_pages_found INTEGER DEFAULT 0,
    products_pages_found INTEGER DEFAULT 0,
    background_pages_found INTEGER DEFAULT 0,
    
    -- Performance
    duration_seconds INTEGER, -- How long the crawl took
    api_calls_made INTEGER DEFAULT 0, -- Number of Exa API calls
    cache_hits INTEGER DEFAULT 0, -- How many results from cache
    
    -- Status
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'running', 'completed', 'failed', 'cancelled'
    error_message TEXT, -- If failed
    
    -- Metadata
    triggered_by VARCHAR(100), -- User or system that triggered
    triggered_from VARCHAR(50), -- 'admin_page_27', 'background_worker', 'api', 'test'
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Data location
    corpus_path TEXT, -- Path to saved corpus file
    cache_key VARCHAR(255) -- Redis cache key if applicable
);

-- Indexes for company_crawls
CREATE INDEX idx_company_crawls_domain ON company_crawls(domain);
CREATE INDEX idx_company_crawls_status ON company_crawls(status);
CREATE INDEX idx_company_crawls_crawl_type ON company_crawls(crawl_type);
CREATE INDEX idx_company_crawls_created_at ON company_crawls(created_at DESC);
CREATE INDEX idx_company_crawls_triggered_by ON company_crawls(triggered_by);


-- ============================================================================
-- TABLE: exa_api_usage
-- Purpose: Track Exa API usage for billing and analytics
-- ============================================================================
CREATE TABLE IF NOT EXISTS exa_api_usage (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- API call details
    endpoint VARCHAR(100), -- '/search', '/findSimilar', '/contents'
    method VARCHAR(50), -- Function called: 'search', 'search_domain', 'find_similar', etc.
    
    -- Request details
    query TEXT,
    domain VARCHAR(255),
    search_mode VARCHAR(20), -- 'auto', 'fast', 'deep'
    num_results INTEGER,
    include_content BOOLEAN DEFAULT FALSE,
    
    -- Response details
    results_returned INTEGER,
    response_time_ms INTEGER, -- Milliseconds
    status_code INTEGER, -- HTTP status
    
    -- Cost tracking
    credits_used DECIMAL(10, 4), -- Exa API credits consumed
    
    -- Context
    crawl_id UUID REFERENCES company_crawls(id) ON DELETE SET NULL, -- Link to crawl if applicable
    triggered_by VARCHAR(100), -- User or system
    triggered_from VARCHAR(50), -- 'admin_page_27', 'background_worker', etc.
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Error tracking
    error_type VARCHAR(100), -- 'rate_limit', 'timeout', 'auth_error', etc.
    error_message TEXT
);

-- Indexes for exa_api_usage
CREATE INDEX idx_exa_api_usage_endpoint ON exa_api_usage(endpoint);
CREATE INDEX idx_exa_api_usage_created_at ON exa_api_usage(created_at DESC);
CREATE INDEX idx_exa_api_usage_status_code ON exa_api_usage(status_code);
CREATE INDEX idx_exa_api_usage_crawl_id ON exa_api_usage(crawl_id);
CREATE INDEX idx_exa_api_usage_triggered_by ON exa_api_usage(triggered_by);
CREATE INDEX idx_exa_api_usage_domain ON exa_api_usage(domain);


-- ============================================================================
-- VIEWS: Convenience views for common queries
-- ============================================================================

-- View: Latest company enrichment summary
CREATE OR REPLACE VIEW v_company_enrichment_summary AS
SELECT 
    c.domain,
    c.company_name,
    c.status,
    c.total_pages_found,
    c.careers_pages_found,
    c.products_pages_found,
    c.background_pages_found,
    c.completed_at,
    c.duration_seconds,
    (SELECT COUNT(*) FROM company_sources WHERE domain = c.domain) as total_sources,
    (SELECT COUNT(*) FROM company_keywords WHERE domain = c.domain) as total_keywords
FROM company_crawls c
WHERE c.id IN (
    SELECT DISTINCT ON (domain) id
    FROM company_crawls
    WHERE status = 'completed'
    ORDER BY domain, completed_at DESC
);

-- View: Top keywords by domain
CREATE OR REPLACE VIEW v_top_keywords_by_domain AS
SELECT 
    domain,
    keyword,
    keyword_type,
    COUNT(*) as frequency,
    AVG(confidence_score) as avg_confidence,
    MAX(created_at) as last_seen
FROM company_keywords
WHERE is_validated = TRUE OR confidence_score > 0.7
GROUP BY domain, keyword, keyword_type
ORDER BY domain, frequency DESC;

-- View: API usage by day
CREATE OR REPLACE VIEW v_api_usage_by_day AS
SELECT 
    DATE(created_at) as usage_date,
    COUNT(*) as total_calls,
    SUM(results_returned) as total_results,
    AVG(response_time_ms) as avg_response_time_ms,
    SUM(credits_used) as total_credits_used,
    COUNT(DISTINCT domain) as unique_domains
FROM exa_api_usage
WHERE status_code = 200
GROUP BY DATE(created_at)
ORDER BY usage_date DESC;


-- ============================================================================
-- FUNCTIONS: Utility functions for data management
-- ============================================================================

-- Function: Update updated_at timestamp automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for auto-updating updated_at
CREATE TRIGGER update_company_sources_updated_at
    BEFORE UPDATE ON company_sources
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_company_keywords_updated_at
    BEFORE UPDATE ON company_keywords
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- SAMPLE QUERIES: Common use cases
-- ============================================================================

-- Query 1: Get all careers pages for a domain
-- SELECT * FROM company_sources 
-- WHERE domain = 'microsoft.com' 
--   AND content_type = 'careers' 
--   AND status = 'active'
-- ORDER BY exa_score DESC;

-- Query 2: Get top skills mentioned across all companies
-- SELECT keyword, COUNT(DISTINCT domain) as company_count, SUM(frequency) as total_mentions
-- FROM company_keywords
-- WHERE keyword_type = 'skill'
-- GROUP BY keyword
-- ORDER BY company_count DESC, total_mentions DESC
-- LIMIT 50;

-- Query 3: Get enrichment status for all domains
-- SELECT * FROM v_company_enrichment_summary
-- ORDER BY completed_at DESC;

-- Query 4: Get API usage for last 7 days
-- SELECT * FROM v_api_usage_by_day
-- WHERE usage_date >= CURRENT_DATE - INTERVAL '7 days';

-- Query 5: Find companies with most product pages
-- SELECT domain, COUNT(*) as product_count
-- FROM company_sources
-- WHERE content_type = 'products'
-- GROUP BY domain
-- ORDER BY product_count DESC
-- LIMIT 20;


-- ============================================================================
-- DATA RETENTION: Cleanup policies
-- ============================================================================

-- Delete old failed crawls (> 30 days)
-- DELETE FROM company_crawls 
-- WHERE status = 'failed' 
--   AND created_at < CURRENT_DATE - INTERVAL '30 days';

-- Archive old company sources (> 90 days, not checked recently)
-- UPDATE company_sources 
-- SET status = 'archived' 
-- WHERE status = 'active' 
--   AND created_at < CURRENT_DATE - INTERVAL '90 days'
--   AND (last_checked IS NULL OR last_checked < CURRENT_DATE - INTERVAL '90 days');


-- ============================================================================
-- GRANTS: Permissions (adjust as needed for your setup)
-- ============================================================================

-- Grant permissions to backend user (replace 'backend_user' with your actual user)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO backend_user;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO backend_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO backend_user;


-- ============================================================================
-- SCHEMA COMPLETE
-- ============================================================================
-- Tables created: 4 (company_sources, company_keywords, company_crawls, exa_api_usage)
-- Views created: 3 (enrichment summary, top keywords, API usage)
-- Functions created: 1 (update_updated_at)
-- Triggers created: 2 (auto-update timestamps)
-- 
-- Next steps:
-- 1. Run this schema in your PostgreSQL database
-- 2. Update connection string in .env
-- 3. Test with test_exa_integration.py
-- 4. Begin Phase 2: Admin Portal integration
-- ============================================================================
