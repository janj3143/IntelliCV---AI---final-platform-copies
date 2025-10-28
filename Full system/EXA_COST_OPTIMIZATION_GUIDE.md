# 💰 Exa Cost Optimization Guide

## 🎯 Problem Statement

**Exa AI is a paid service** with costs based on API calls. Without optimization, heavy usage can lead to significant expenses:

- **Exa API**: ~$0.01-0.05 per search (varies by plan)
- **100 searches/day**: $1-5/day = $30-150/month
- **1000 searches/day**: $10-50/day = $300-1,500/month

**Solution**: Two-tier search strategy reduces costs by **70-90%** while maintaining quality.

---

## 🏗️ Two-Tier Search Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      TWO-TIER SEARCH STRATEGY                       │
│                  (Cost Reduction: 70-90%)                           │
└─────────────────────────────────────────────────────────────────────┘

TIER 1: Google Custom Search (Free/Cheap - Broad Results)
┌─────────────────────────────────────────────────────────────────┐
│  Query: "Microsoft careers software engineer"                  │
│  ↓                                                              │
│  Google API → 100 candidate URLs                               │
│  Cost: FREE (100 queries/day) or $0.50 (paid tier)            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────────────┐
                    │   FILTER LAYER  │
                    └─────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Filtering Criteria:                                            │
│  ✓ URL must contain "career/jobs/hiring"                       │
│  ✓ Domain not in blacklist (spam.com, etc.)                    │
│  ✓ HTTPS only                                                   │
│  ✓ Deduplicate URLs                                             │
│  ✓ Custom filters (domain authority, recency, etc.)            │
│                                                                  │
│  Result: 100 URLs → 10 URLs (90% filtered out)                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
TIER 2: Exa Deep Analysis (Paid - High Quality Extraction)
┌─────────────────────────────────────────────────────────────────┐
│  Filtered URLs → Exa API (deep content extraction)             │
│  ↓                                                              │
│  10 URLs analyzed by Exa                                        │
│  Cost: $0.10-0.50 (instead of $1-5 for 100 URLs)              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────────────┐
                    │  STORE RESULTS  │
                    └─────────────────┘

TOTAL COST: $0.10-0.50 (90% savings vs Exa-only)
```

---

## 📊 Cost Comparison

### Scenario: 100 Company Enrichment Searches/Day

#### ❌ **Without Two-Tier** (Exa-Only):
```
100 searches × $0.03/search = $3.00/day
Monthly: $3.00 × 30 = $90/month
Yearly: $90 × 12 = $1,080/year
```

#### ✅ **With Two-Tier** (Google → Filter → Exa):
```
Stage 1 - Google: 100 queries × $0 (free tier) = $0/day
Stage 2 - Filter: No cost (local processing)
Stage 3 - Exa: 10 queries × $0.03/search = $0.30/day

Monthly: $0.30 × 30 = $9/month
Yearly: $9 × 12 = $108/year

SAVINGS: $1,080 - $108 = $972/year (90% reduction!)
```

### Breakdown by Filter Efficiency

| Filter Pass Rate | Google Queries | Exa Queries | Daily Cost | Monthly Cost | Yearly Cost | Savings |
|------------------|----------------|-------------|------------|--------------|-------------|---------|
| **10%** (recommended) | 100 | 10 | $0.30 | $9 | $108 | 90% |
| **20%** | 100 | 20 | $0.60 | $18 | $216 | 80% |
| **50%** | 100 | 50 | $1.50 | $45 | $540 | 50% |
| **100%** (no filter) | 0 | 100 | $3.00 | $90 | $1,080 | 0% |

**Optimal**: Keep filter pass rate at **10-20%** for best cost/quality balance.

---

## 🔧 Implementation

### 1. Enable Two-Tier Search

**Update `.env`**:
```properties
# Enable two-tier search
USE_TWO_TIER_SEARCH=true

# Google Custom Search API (free tier: 100 queries/day)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CX_ID=your_google_cx_id_here
```

### 2. Get Google API Credentials (FREE)

**Step 1**: Create Google Cloud Project
- Go to: https://console.cloud.google.com/
- Create new project or select existing

**Step 2**: Enable Custom Search API
- Navigate to: APIs & Services → Library
- Search "Custom Search API"
- Click "Enable"

**Step 3**: Create API Key
- Go to: APIs & Services → Credentials
- Click "Create Credentials" → API Key
- Copy `GOOGLE_API_KEY`

**Step 4**: Create Custom Search Engine
- Go to: https://programmablesearchengine.google.com/
- Click "Add"
- Search the entire web: Yes
- Copy `CX ID` (Search engine ID)

**FREE TIER**: 100 queries/day (3,000/month) - Perfect for development!

### 3. Use in Code

```python
from services.exa_service.company_enrichment import get_company_enricher

# Initialize with two-tier enabled
enricher = get_company_enricher()

# Automatic cost optimization (uses two-tier if configured)
careers = enricher.find_careers_pages("microsoft.com")

# Or explicitly enable/disable
careers = enricher.find_careers_pages("microsoft.com", use_two_tier=True)  # Cost-optimized
products = enricher.find_product_pages("apple.com", use_two_tier=False)    # Direct Exa
```

### 4. Custom Filters

```python
from services.exa_service.smart_search_orchestrator import SearchFilter

# Create custom filter
filter_config = SearchFilter()
filter_config.required_url_patterns = ['career', 'jobs', 'hiring']
filter_config.blocked_domains = {'spam.com', 'low-quality.com'}
filter_config.require_https = True

# Use with enricher
careers = enricher.find_careers_pages(
    "company.com",
    use_two_tier=True,
    custom_filter=filter_config
)
```

---

## 📈 Monitoring Costs

### Built-in Cost Tracker

```python
from services.exa_service.smart_search_orchestrator import get_smart_search_orchestrator

orchestrator = get_smart_search_orchestrator()

# Execute searches
result = orchestrator.smart_search("Python jobs at Microsoft")

# Print cost summary
orchestrator.cost_tracker.print_summary()
```

**Output**:
```
======================================================================
COST TRACKER SUMMARY
======================================================================

Google Queries: 20
Google Cost: $0.0000 (free tier)

Exa Queries: 2
Exa Cost: $0.0600

Total Cost: $0.0600
Savings vs Exa-only: $0.5400
Efficiency Ratio: 9.1% Exa usage
======================================================================
```

### Database Cost Logging

All API usage is automatically logged to `exa_api_usage` table:

```sql
SELECT 
    DATE(query_timestamp) as date,
    COUNT(*) as queries,
    SUM(CASE WHEN api_endpoint = 'google' THEN 1 ELSE 0 END) as google_queries,
    SUM(CASE WHEN api_endpoint = 'exa' THEN 1 ELSE 0 END) as exa_queries
FROM exa_api_usage
WHERE query_timestamp >= NOW() - INTERVAL '30 days'
GROUP BY DATE(query_timestamp)
ORDER BY date DESC;
```

### Admin Portal Analytics

**Page 27 → Analytics Tab** shows:
- Daily/weekly/monthly cost breakdown
- Google vs Exa query distribution
- Filter efficiency metrics
- Cost savings vs Exa-only approach

---

## 🎯 Filter Optimization Strategies

### 1. Careers Pages Filter (90% reduction)

```python
from services.exa_service.smart_search_orchestrator import create_careers_page_filter

filter_config = create_careers_page_filter()
# Pre-configured for:
# - Required: career, jobs, hiring, opportunities
# - Blocked: login, cart, blog, terms
# - HTTPS only
```

**Typical Results**:
- Google: 100 URLs
- After filter: 10 URLs (careers pages only)
- Exa cost: $0.30 instead of $3.00

### 2. Product Pages Filter (80% reduction)

```python
from services.exa_service.smart_search_orchestrator import create_product_page_filter

filter_config = create_product_page_filter()
# Pre-configured for:
# - Required: product, solution, platform, service
# - Blocked: support, help, docs, terms
```

### 3. Domain Authority Filter

```python
filter_config = SearchFilter()
filter_config.min_domain_authority = 50  # Only sites with DA > 50

# Requires SEO API integration (Moz, Ahrefs, etc.)
```

### 4. Recency Filter

```python
filter_config = SearchFilter()
filter_config.max_age_days = 90  # Only pages updated in last 90 days

# Uses Google dateRestrict parameter
```

### 5. Custom Business Logic

```python
def custom_filter(result: Dict) -> bool:
    """Only Fortune 500 companies."""
    domain = result.get('domain', '')
    return domain in FORTUNE_500_DOMAINS

# Apply
result = orchestrator.smart_search(
    query="tech companies hiring",
    custom_filter=custom_filter
)
```

---

## 💡 Best Practices

### 1. **Use Caching Aggressively**

```python
# Local file cache (24h TTL by default)
# Second query is nearly free!
careers1 = enricher.find_careers_pages("microsoft.com")  # Exa API call
careers2 = enricher.find_careers_pages("microsoft.com")  # Cached (no cost)
```

**Cache hit rate**: 60-80% in production → **60-80% cost savings on top of two-tier!**

### 2. **Batch Processes**

```python
# Bad: 100 individual enrichments
for company in companies:
    enricher.find_careers_pages(company)  # 100 Exa calls

# Good: Batch with two-tier
from services.exa_service.exa_queue import get_exa_queue_manager

queue = get_exa_queue_manager()
queue.enqueue_batch([
    {'domain': company, 'search_type': 'careers'}
    for company in companies
])
# Background worker processes with two-tier → 90% savings
```

### 3. **Smart Scheduling**

```python
# Schedule enrichment during off-peak hours
queue.schedule_enrichment(
    domain="company.com",
    search_type="careers",
    schedule_time=datetime.now() + timedelta(hours=8)  # Run at night
)
```

### 4. **Rate Limiting**

```python
# Respect Exa rate limits (100 req/min default)
# Two-tier automatically reduces Exa calls → less likely to hit limits
```

### 5. **Quality Thresholds**

```python
# Only use Exa for high-value targets
if company.employee_count > 100:  # Only large companies
    enricher.find_careers_pages(company.domain, use_two_tier=True)
else:
    # Skip or use free-only Google search
    pass
```

---

## 🚀 Advanced: Hybrid Strategies

### Strategy 1: Google-Only for Discovery

```python
# Stage 1: Discover all companies (Google-only, free)
orchestrator = get_smart_search_orchestrator()
google_results = orchestrator.google_search("tech startups hiring", num_results=100)

# Stage 2: Filter to top 10 most relevant
filtered = orchestrator.filter_results(google_results)

# Stage 3: Deep analysis on top 10 only (Exa)
for result in filtered[:10]:
    exa_data = enricher.find_careers_pages(result['domain'], use_two_tier=False)
```

### Strategy 2: Tiered by Company Size

```python
if company.employee_count > 10000:
    # Large company: Use Exa directly (high-quality data critical)
    data = enricher.find_careers_pages(company.domain, use_two_tier=False)

elif company.employee_count > 500:
    # Medium company: Use two-tier (balanced)
    data = enricher.find_careers_pages(company.domain, use_two_tier=True)

else:
    # Small company: Google-only (cost-conscious)
    data = orchestrator.google_search(f"{company.name} careers")
```

### Strategy 3: Progressive Enhancement

```python
# Day 1: Google-only for all 10,000 companies (free)
for company in companies:
    google_data = orchestrator.google_search(f"{company.name} careers")
    store_preliminary_data(google_data)

# Day 2-30: Exa deep analysis for top 100 active companies
top_companies = get_most_active_companies(limit=100)
for company in top_companies:
    exa_data = enricher.find_careers_pages(company.domain)
    enhance_data(exa_data)
```

---

## 📊 ROI Analysis

### Small Deployment (10 companies/day)

**Without Two-Tier**:
- Daily: 10 × $0.03 = $0.30
- Monthly: $9
- Yearly: $108

**With Two-Tier**:
- Daily: $0.03 (1 Exa call instead of 10)
- Monthly: $0.90
- Yearly: $10.80

**Savings**: $97.20/year (90% reduction)

### Medium Deployment (100 companies/day)

**Without Two-Tier**:
- Yearly: $1,080

**With Two-Tier**:
- Yearly: $108

**Savings**: $972/year (90% reduction)

### Large Deployment (1,000 companies/day)

**Without Two-Tier**:
- Yearly: $10,800

**With Two-Tier**:
- Yearly: $1,080

**Savings**: $9,720/year (90% reduction)

**ROI on Implementation**:
- Development time: 8 hours × $100/hour = $800
- Break-even: ~1 month for medium deployment
- Net savings (Year 1): $9,720 - $800 = $8,920

---

## 🔍 When to Use Exa-Only vs Two-Tier

### ✅ Use Two-Tier (Recommended):
- **High volume**: > 50 queries/day
- **Cost-conscious**: Budget constraints
- **Broad searches**: "All tech companies hiring"
- **Discovery phase**: Finding new companies
- **Production**: Always use two-tier in prod

### ⚠️ Use Exa-Only:
- **Low volume**: < 10 queries/day
- **Critical quality**: C-suite data, investors
- **Specific domains**: Already know exact URL
- **Real-time**: Need instant results (no Google delay)
- **Development/Testing**: Quick prototyping

---

## 🛠️ Troubleshooting

### Issue: Google API quota exceeded (>100/day)

**Solution 1**: Upgrade to paid tier ($5/1000 queries)
```properties
# Still 90% cheaper than Exa-only!
```

**Solution 2**: Cache more aggressively
```properties
EXA_CACHE_TTL=604800  # 7 days instead of 24 hours
```

**Solution 3**: Reduce Google queries
```python
# Fetch fewer results, filter more aggressively
result = orchestrator.smart_search(query, num_google_results=20)  # Instead of 50
```

### Issue: Filter too aggressive (0% pass rate)

**Solution**: Relax filter criteria
```python
filter_config = SearchFilter()
filter_config.required_url_patterns = ['career']  # Instead of ['career', 'jobs', 'hiring']
```

### Issue: Filter too lenient (>50% pass rate)

**Solution**: Tighten filter criteria
```python
filter_config.blocked_url_patterns.extend(['blog', 'news', 'press', 'media'])
filter_config.require_https = True
filter_config.min_domain_authority = 30
```

---

## 📚 Summary

### Key Takeaways

1. **Two-tier search reduces costs by 70-90%**
2. **Google (free/cheap) → Filter → Exa (paid) = optimal strategy**
3. **10-20% filter pass rate is ideal**
4. **Caching adds another 60-80% savings**
5. **Combined savings: up to 95-98% vs naive Exa-only**

### Quick Start Checklist

- [ ] Get Google API key (free)
- [ ] Update `.env` with credentials
- [ ] Set `USE_TWO_TIER_SEARCH=true`
- [ ] Test with `test_smart_search_orchestrator.py`
- [ ] Monitor costs in Admin Page 27 → Analytics
- [ ] Optimize filters based on pass rate

### Cost Optimization Formula

```
Total Cost = (Google Queries × $0) + (Exa Queries × $0.03)

Where:
  Exa Queries = Google Queries × Filter Pass Rate
  
Target:
  Filter Pass Rate = 10-20% for optimal cost/quality

Expected Savings:
  90% cost reduction vs Exa-only
  95-98% combined with caching
```

---

**Last Updated**: 2025-10-28  
**Version**: 1.0.0 (Two-Tier Implementation)
