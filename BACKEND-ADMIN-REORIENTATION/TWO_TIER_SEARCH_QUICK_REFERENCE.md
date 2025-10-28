# 🚀 Exa Two-Tier Search - Quick Reference

## 🎯 What Is It?

**Cost-optimized search strategy**: Google (free) → Filter → Exa (paid)

**Savings**: 70-90% reduction in Exa API costs

**Quality**: Same high-quality results, less expense

---

## ⚡ Quick Start (3 Steps)

### 1. Get Google API Credentials (FREE)

```
1. Go to: https://console.cloud.google.com/
2. Create project → Enable "Custom Search API"
3. Create API key → Copy GOOGLE_API_KEY
4. Create Custom Search Engine → Copy GOOGLE_CX_ID
   (https://programmablesearchengine.google.com/)
```

**Free Tier**: 100 queries/day (perfect for development)

### 2. Update `.env`

```properties
# Enable two-tier search
USE_TWO_TIER_SEARCH=true

# Google credentials (free tier)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CX_ID=your_google_cx_id_here
```

### 3. Use Normally - Automatic Savings!

```python
from services.exa_service.company_enrichment import get_company_enricher

enricher = get_company_enricher()

# Automatic two-tier optimization (90% cost savings)
careers = enricher.find_careers_pages("microsoft.com")
```

**Done!** You're now saving 90% on Exa costs.

---

## 💰 Cost Comparison

| Scenario | Exa-Only Cost | Two-Tier Cost | Savings |
|----------|---------------|---------------|---------|
| 10/day   | $9/month      | $0.90/month   | 90%     |
| 100/day  | $90/month     | $9/month      | 90%     |
| 1000/day | $900/month    | $90/month     | 90%     |

---

## 🔧 Code Examples

### Basic Usage

```python
from services.exa_service.company_enrichment import get_company_enricher

enricher = get_company_enricher()

# Two-tier enabled by default (if configured in .env)
careers = enricher.find_careers_pages("company.com")
products = enricher.find_product_pages("company.com")
```

### Custom Filters

```python
from services.exa_service.smart_search_orchestrator import SearchFilter

# Create custom filter
filter_config = SearchFilter()
filter_config.required_url_patterns = ['career', 'jobs']
filter_config.blocked_domains = {'spam.com'}
filter_config.require_https = True

# Use with enricher
careers = enricher.find_careers_pages(
    "company.com",
    custom_filter=filter_config
)
```

### Cost Tracking

```python
from services.exa_service.smart_search_orchestrator import get_smart_search_orchestrator

orchestrator = get_smart_search_orchestrator()

# Execute search
result = orchestrator.smart_search("Python jobs at Microsoft")

# Print cost summary
orchestrator.cost_tracker.print_summary()

# Output:
# Google Queries: 50
# Google Cost: $0.00 (free)
# Exa Queries: 5
# Exa Cost: $0.15
# Savings vs Exa-only: $1.35 (90%)
```

### Direct Orchestrator Use

```python
from services.exa_service.smart_search_orchestrator import (
    get_smart_search_orchestrator,
    create_careers_page_filter
)

orchestrator = get_smart_search_orchestrator()
filter_config = create_careers_page_filter()

# Smart search with filtering
result = orchestrator.smart_search(
    query="Microsoft software engineer careers",
    num_google_results=50,
    filter_config=filter_config
)

# Results
print(f"Google: {len(result['google_results'])} URLs")
print(f"Filtered: {len(result['filtered_results'])} URLs")
print(f"Exa analyzed: {len(result['exa_results'])} URLs")
print(f"Cost: ${result['cost_summary']['total_cost']:.2f}")
```

---

## 📊 How It Works

```
Step 1: GOOGLE SEARCH (Free)
Query: "Microsoft careers software engineer"
↓
100 candidate URLs

Step 2: FILTER (No Cost)
Remove: spam, non-careers, duplicates
↓
10 high-quality URLs (90% filtered out)

Step 3: EXA ANALYSIS (Paid - But Only 10 URLs!)
Deep content extraction
↓
10 enriched results

RESULT: $0.30 instead of $3.00 (90% savings)
```

---

## 🎛️ Configuration

### Environment Variables

```properties
# Required
USE_TWO_TIER_SEARCH=true
GOOGLE_API_KEY=your_key_here
GOOGLE_CX_ID=your_cx_id_here
EXA_API_KEY=your_exa_key_here

# Optional
GOOGLE_COST_PER_QUERY=0.005   # $5/1000 or 0 (free tier)
EXA_COST_PER_QUERY=0.03       # Adjust based on your plan
```

### Pre-Built Filters

**Careers Pages**:
```python
from services.exa_service.smart_search_orchestrator import create_careers_page_filter

filter_config = create_careers_page_filter()
# Required: career, jobs, hiring, opportunities
# Blocked: login, cart, blog, terms
# HTTPS only
```

**Product Pages**:
```python
from services.exa_service.smart_search_orchestrator import create_product_page_filter

filter_config = create_product_page_filter()
# Required: product, solution, platform, service
# Blocked: support, help, docs, terms
```

---

## 📈 Monitoring

### Admin Portal

**Page 27 → Analytics Tab**:
- Real-time cost breakdown
- Google vs Exa query distribution
- Filter efficiency metrics
- Savings calculations

### Database

```sql
-- View API usage
SELECT * FROM exa_api_usage
WHERE query_timestamp >= NOW() - INTERVAL '7 days'
ORDER BY query_timestamp DESC;

-- Cost by day
SELECT 
    DATE(query_timestamp) as date,
    COUNT(*) as queries,
    COUNT(*) * 0.03 as estimated_cost
FROM exa_api_usage
WHERE api_endpoint = 'exa'
GROUP BY DATE(query_timestamp);
```

### Programmatic

```python
# Get cost breakdown
cost_summary = orchestrator.cost_tracker.get_cost_breakdown()

print(f"Total cost: ${cost_summary['total_cost']:.2f}")
print(f"Savings: ${cost_summary['savings_vs_exa_only']:.2f}")
print(f"Exa usage: {cost_summary['efficiency_ratio']*100:.1f}%")
```

---

## 🔍 Filter Optimization

### Target Pass Rate: 10-20%

**Too High (>50%)**:
- Not enough cost savings
- Tighten filters

**Too Low (<5%)**:
- Missing valid results
- Relax filters

### Adjust Filter Strength

```python
filter_config = SearchFilter()

# Lenient (30-40% pass rate)
filter_config.required_url_patterns = ['career']

# Balanced (10-20% pass rate) ← Recommended
filter_config.required_url_patterns = ['career', 'jobs', 'hiring']

# Strict (5-10% pass rate)
filter_config.required_url_patterns = ['career', 'jobs', 'hiring', 'opportunities']
filter_config.blocked_url_patterns = ['blog', 'news', 'press', 'media']
filter_config.require_https = True
```

---

## 🚨 Troubleshooting

### Google quota exceeded (>100/day)

**Option 1**: Upgrade to paid tier ($5/1000 queries)
```properties
# Still 90% cheaper than Exa-only!
```

**Option 2**: Increase cache TTL
```properties
EXA_CACHE_TTL=604800  # 7 days
```

**Option 3**: Reduce Google queries
```python
result = orchestrator.smart_search(query, num_google_results=20)
```

### Two-tier not activating

**Check `.env`**:
```properties
USE_TWO_TIER_SEARCH=true  # Must be 'true', not 'True' or '1'
GOOGLE_API_KEY=xxx        # Must be set
GOOGLE_CX_ID=xxx          # Must be set
```

**Check logs**:
```python
import logging
logging.basicConfig(level=logging.INFO)

enricher = get_company_enricher()
# Look for: "✅ Two-tier search ENABLED"
```

### Filter too aggressive (0% pass rate)

```python
# Relax criteria
filter_config = SearchFilter()
filter_config.required_url_patterns = ['career']  # Just one pattern
```

---

## 💡 Best Practices

### ✅ DO:
- Use two-tier for all production searches
- Monitor filter pass rate (target: 10-20%)
- Cache aggressively (24h+ TTL)
- Batch process when possible
- Track costs in database

### ❌ DON'T:
- Skip filters (defeats the purpose)
- Use Exa-only for high-volume searches
- Ignore cost tracking
- Set pass rate > 50% (minimal savings)

---

## 📚 Documentation

- **Complete Guide**: `EXA_COST_OPTIMIZATION_GUIDE.md`
- **Implementation**: `shared_backend/services/exa_service/smart_search_orchestrator.py`
- **Integration**: `PHASES_1_TO_5_COMPLETE.md`

---

## 🎉 Summary

```
┌─────────────────────────────────────────────────────────────┐
│  TWO-TIER SEARCH = 90% COST SAVINGS                        │
│                                                             │
│  Setup: 3 steps (5 minutes)                                │
│  Savings: $972/year (100 searches/day)                     │
│  Quality: Same results, less cost                          │
│                                                             │
│  Google → Filter → Exa                                     │
│  (free)   (smart)  (paid, but 10x less)                   │
└─────────────────────────────────────────────────────────────┘
```

**Get started today!** Update your `.env` and start saving.

---

**Version**: 1.0.0  
**Last Updated**: 2025-10-28
