# JD Keyword Extraction - System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        INTELLICV JD KEYWORD EXTRACTION                      │
│                         Job-Focused Intelligence Layer                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACES                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────┐        ┌────────────────────────────┐      │
│  │  Admin Portal - Page 27    │        │   User Portal - Page 10     │      │
│  │  "JD Analysis" Tab         │        │   "UMarketU Suite"          │      │
│  ├────────────────────────────┤        ├────────────────────────────┤      │
│  │  1. JD Keyword Extraction  │        │  - Company Insights         │      │
│  │  2. Job Title Analysis     │        │  - Job Discovery            │      │
│  │  3. Smart Search           │        │  - Enhanced Job Cards       │      │
│  └────────────┬───────────────┘        └──────────┬─────────────────┘      │
│               │                                    │                         │
└───────────────┼────────────────────────────────────┼─────────────────────────┘
                │                                    │
                └────────────────┬───────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CORE EXTRACTION ENGINE                              │
│                  shared_backend/services/exa_service/                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                     KeywordExtractor Class                            │  │
│  │                         (keyword_extractor.py)                        │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │                                                                       │  │
│  │  Main Methods:                                                        │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │  │
│  │  │ extract_job_description_keywords(jd_text)                       │ │  │
│  │  │ → Returns: {required_skills, nice_to_have, experience,          │ │  │
│  │  │            education, tech_stack, soft_skills, keyword_counts}  │ │  │
│  │  └─────────────────────────────────────────────────────────────────┘ │  │
│  │                                                                       │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │  │
│  │  │ analyze_job_title(job_title)                                    │ │  │
│  │  │ → Returns: {level, role, domain, seniority_score, keywords}    │ │  │
│  │  └─────────────────────────────────────────────────────────────────┘ │  │
│  │                                                                       │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │  │
│  │  │ smart_search(query, search_type='hybrid')                       │ │  │
│  │  │ → Returns: {extracted_keywords, semantic_expansions,            │ │  │
│  │  │            sql_where_clauses, final_sql}                        │ │  │
│  │  └─────────────────────────────────────────────────────────────────┘ │  │
│  │                                                                       │  │
│  │  Pattern Libraries:                                                   │  │
│  │  • JD_REQUIREMENT_PATTERNS (experience/education regex)              │  │
│  │  • JOB_TITLE_LEVELS (senior, junior, staff, principal, etc.)        │  │
│  │  • JOB_TITLE_ROLES (engineer, developer, manager, etc.)             │  │
│  │  • JOB_TITLE_DOMAINS (ML, AI, data, frontend, backend, etc.)        │  │
│  │  • KEYWORD_PATTERNS (technologies, frameworks, tools)               │  │
│  │                                                                       │  │
│  └───────────────────────────┬───────────────────────────────────────────┘  │
│                              │                                               │
└──────────────────────────────┼───────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        EXTRACTION METHODS (MULTI-LAYER)                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐     │
│  │  1. Regex        │    │  2. spaCy NLP    │    │  3. OpenAI GPT   │     │
│  │     Patterns     │ →  │     Processing   │ →  │     (LLM)        │     │
│  ├──────────────────┤    ├──────────────────┤    ├──────────────────┤     │
│  │ • "5+ years"     │    │ • Entity         │    │ • Semantic       │     │
│  │ • "BS/MS/PhD"    │    │   recognition    │    │   understanding  │     │
│  │ • Section splits │    │ • POS tagging    │    │ • Context-aware  │     │
│  │ • Structured     │    │ • Locations      │    │ • Best quality   │     │
│  │   parsing        │    │ • Companies      │    │ • Slowest        │     │
│  │                  │    │                  │    │                  │     │
│  │ Speed: 50ms      │    │ Speed: 200ms     │    │ Speed: 2-5s      │     │
│  │ Confidence: 90%  │    │ Confidence: 75%  │    │ Confidence: 95%  │     │
│  └──────────────────┘    └──────────────────┘    └──────────────────┘     │
│                                                                              │
│  Result Merging: Combine all methods with confidence-weighted consensus     │
│                                                                              │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SEMANTIC EXPANSION LAYER                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Keyword → Related Terms (for Smart Search)                                 │
│                                                                              │
│  python      → ['django', 'flask', 'fastapi', 'pandas', 'numpy']           │
│  ml          → ['machine learning', 'tensorflow', 'pytorch', 'sklearn']    │
│  aws         → ['amazon web services', 'ec2', 's3', 'lambda']              │
│  javascript  → ['js', 'node.js', 'react', 'angular', 'vue']                │
│  backend     → ['server-side', 'api', 'database', 'rest']                  │
│  frontend    → ['ui', 'ux', 'html', 'css', 'responsive']                   │
│  docker      → ['container', 'containerization', 'kubernetes']             │
│  sql         → ['mysql', 'postgresql', 'database', 'query']                │
│                                                                              │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA STORAGE & CACHE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────┐        ┌────────────────────────────┐      │
│  │  PostgreSQL                │        │  Local File Cache          │      │
│  │  (Primary Storage)         │        │  (Performance Layer)       │      │
│  ├────────────────────────────┤        ├────────────────────────────┤      │
│  │ • company_sources          │        │ ai_data_final/exa_cache/   │      │
│  │ • company_keywords         │        │   keyword_extraction/      │      │
│  │ • company_crawls           │        │                            │      │
│  │ • exa_api_usage            │        │ TTL: 24 hours              │      │
│  │                            │        │ Cache hit: 60-80%          │      │
│  │ Views:                     │        │                            │      │
│  │ • v_enrichment_summary     │        │ Format: JSON files         │      │
│  │ • v_top_keywords_by_domain │        │ Key: hash(jd_text)         │      │
│  │ • v_api_usage_by_day       │        │                            │      │
│  └────────────────────────────┘        └────────────────────────────┘      │
│                                                                              │
│  ┌────────────────────────────┐        ┌────────────────────────────┐      │
│  │  SQLite                    │        │  Redis                     │      │
│  │  (Smart Search Target)     │        │  (Queue System)            │      │
│  ├────────────────────────────┤        ├────────────────────────────┤      │
│  │ • Hybrid AI + exact        │        │ • exa_enrichment queue     │      │
│  │   matching queries         │        │ • Background workers       │      │
│  │ • WHERE clause generation  │        │ • Scheduled jobs           │      │
│  │ • Semantic expansion       │        │                            │      │
│  └────────────────────────────┘        └────────────────────────────┘      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW EXAMPLE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Input: Job Description Text                                                │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ "Senior ML Engineer - 5+ years Python required. AWS, Docker,      │    │
│  │  TensorFlow expertise needed. BS/MS in CS. Nice to have: PhD,     │    │
│  │  Kubernetes experience, published research."                       │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  Step 1: Regex Extraction (90% confidence)                                  │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ Experience: {'years_required': 5, 'mentions': 1}                   │    │
│  │ Education: ['BS', 'MS']                                            │    │
│  │ Section split: "Nice to have" → nice_to_have skills               │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  Step 2: spaCy NLP (75% confidence)                                         │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ Entities: Python (TECH), AWS (TECH), Docker (TECH), CS (FIELD)    │    │
│  │ Keywords: ['python', 'aws', 'docker', 'tensorflow', 'kubernetes'] │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  Step 3: OpenAI GPT-3.5 (95% confidence)                                    │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ Required skills: ['Python', 'AWS', 'Docker', 'TensorFlow']        │    │
│  │ Nice-to-have: ['PhD', 'Kubernetes', 'Research']                   │    │
│  │ Tech stack: python(freq:2), aws(freq:1), docker(freq:1), ...     │    │
│  │ Soft skills: ['expertise needed']                                 │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  Result Merging: Combine with confidence weighting                          │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ Final Output:                                                      │    │
│  │ {                                                                  │    │
│  │   'required_skills': ['Python', 'AWS', 'Docker', 'TensorFlow'],   │    │
│  │   'nice_to_have': ['PhD', 'Kubernetes', 'Research'],              │    │
│  │   'experience': {'years_required': 5, 'mentions': 1},             │    │
│  │   'education': ['BS', 'MS'],                                       │    │
│  │   'tech_stack': [                                                  │    │
│  │     {'keyword': 'python', 'frequency': 2, 'confidence': 0.95},    │    │
│  │     {'keyword': 'aws', 'frequency': 1, 'confidence': 0.90},       │    │
│  │     ...                                                            │    │
│  │   ],                                                               │    │
│  │   'keyword_counts': {'python': 2, 'aws': 1, 'docker': 1, ...},    │    │
│  │   'soft_skills': []                                                │    │
│  │ }                                                                  │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                        SMART SEARCH FLOW EXAMPLE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Input: Natural Language Query                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ "Find companies hiring Python developers in Seattle"              │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  Step 1: Extract Components                                                 │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ Keywords: ['python']                                               │    │
│  │ Role: 'developers'                                                 │    │
│  │ Location: 'Seattle'                                                │    │
│  │ Level: None                                                        │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  Step 2: Semantic Expansion (if search_type='hybrid' or 'semantic')         │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ python → ['django', 'flask', 'fastapi', 'pandas', 'numpy']        │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  Step 3: Build SQLite WHERE Clauses                                         │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ 1. content_type = 'careers'                                        │    │
│  │ 2. (text_content LIKE '%python%' OR title LIKE '%python%')        │    │
│  │ 3. (text_content LIKE '%django%' OR ...)  [semantic expansion]    │    │
│  │ 4. (text_content LIKE '%flask%' OR ...)   [semantic expansion]    │    │
│  │ 5. (text_content LIKE '%Seattle%' OR location LIKE '%Seattle%')   │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  Step 4: Generate Final SQL                                                 │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ SELECT * FROM company_sources                                      │    │
│  │ WHERE content_type = 'careers'                                     │    │
│  │   AND (text_content LIKE '%python%' OR title LIKE '%python%')     │    │
│  │   AND (text_content LIKE '%django%' OR title LIKE '%django%'      │    │
│  │        OR text_content LIKE '%flask%' OR title LIKE '%flask%'     │    │
│  │        ...)                                                        │    │
│  │   AND (text_content LIKE '%Seattle%' OR location LIKE '%Seattle%')│    │
│  │ ORDER BY exa_score DESC                                            │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  Execute → Return matching companies                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                         JOB TITLE ANALYSIS FLOW                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Input: Job Title                                                           │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ "Senior Machine Learning Engineer"                                │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  Step 1: Lowercase & Tokenize                                               │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ Tokens: ['senior', 'machine', 'learning', 'engineer']             │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  Step 2: Match Against Pattern Libraries                                    │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ Level:  'senior' ∈ JOB_TITLE_LEVELS     → level = 'senior'       │    │
│  │ Role:   'engineer' ∈ JOB_TITLE_ROLES    → role = 'engineer'      │    │
│  │ Domain: 'machine learning' ∈ DOMAINS    → domain = 'ml'          │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  Step 3: Calculate Seniority Score                                          │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ senior → seniority_score = 100                                     │    │
│  │ (scale: entry=0, mid=50, senior/staff/principal=100)              │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  Output:                                                                     │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ {                                                                  │    │
│  │   'original_title': 'Senior Machine Learning Engineer',           │    │
│  │   'level': 'senior',                                               │    │
│  │   'role': 'engineer',                                              │    │
│  │   'domain': 'ml',                                                  │    │
│  │   'keywords': ['senior', 'machine', 'learning', 'engineer'],      │    │
│  │   'seniority_score': 100                                           │    │
│  │ }                                                                  │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                          INTEGRATION POINTS                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. Admin Portal (Page 27 - JD Analysis Tab)                                │
│     • Manual JD analysis                                                     │
│     • Job title batch processing                                             │
│     • Smart search query builder                                             │
│                                                                              │
│  2. User Portal (Page 10 - UMarketU Suite)                                  │
│     • Enhanced job cards with keyword matching                               │
│     • Company insights from Exa enrichment                                   │
│     • Smart job search with semantic expansion                               │
│                                                                              │
│  3. Background Workers (exa_worker.py)                                       │
│     • Automated JD extraction for all careers pages                          │
│     • Batch keyword indexing                                                 │
│     • Scheduled re-analysis for updated JDs                                  │
│                                                                              │
│  4. Database (PostgreSQL + SQLite)                                           │
│     • Store extracted keywords in company_keywords table                     │
│     • Link to company_sources via foreign key                                │
│     • Hybrid queries for smart search                                        │
│                                                                              │
│  5. Integration Hooks (shared/integration_hooks.py)                          │
│     • sync_exa_company_data() - Push JD keywords to user portals             │
│     • sync_exa_market_intelligence() - Aggregate keyword trends              │
│     • sync_exa_batch_enrichment() - Bulk JD processing                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                              KEY BENEFITS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ✅ JOB-SPECIFIC: Focused on careers pages and JDs, not generic web content │
│  ✅ FREQUENCY COUNTING: Know which skills are mentioned most (importance)   │
│  ✅ STRUCTURED PARSING: Required vs nice-to-have, experience, education     │
│  ✅ TITLE INTELLIGENCE: Automatic level/role/domain extraction              │
│  ✅ HYBRID SEARCH: AI understanding + exact SQLite matching                 │
│  ✅ SEMANTIC EXPANSION: python → django, flask (better recall)              │
│  ✅ MULTI-METHOD: Regex + spaCy + OpenAI = highest accuracy                 │
│  ✅ CACHED: Fast repeat queries (60-80% cache hit rate)                     │
│  ✅ INTEGRATED: Works with existing Exa enrichment system                   │
│  ✅ TESTABLE: Complete test suite (test_jd_keyword_search.py)               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**Architecture Version**: 1.0.0  
**Date**: 2025-01-15  
**Phase**: 5+ (JD-Focused Enhancement)
