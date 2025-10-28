# Job Description Keyword Extraction - Complete Guide

## 🎯 Overview

The **JD Keyword Extraction** system is a specialized module designed specifically for extracting, analyzing, and searching job-related keywords from career pages and job descriptions. Unlike generic keyword extraction, this system focuses on:

- **Job descriptions**: Required skills, nice-to-have qualifications, experience, education
- **Job titles**: Parsing into level, role, domain components
- **Smart search**: Hybrid AI + SQLite queries with semantic expansion

## 📁 Architecture

### File Location
```
shared_backend/services/exa_service/keyword_extractor.py
```

### Key Components

1. **KeywordExtractor Class** - Main extraction engine
   - Multi-method extraction: Regex → spaCy → OpenAI GPT-3.5
   - Confidence scoring based on method
   - Caching and batch processing

2. **Pattern Libraries**
   ```python
   JD_REQUIREMENT_PATTERNS     # Experience/education regex
   JOB_TITLE_LEVELS            # senior, junior, staff, principal
   JOB_TITLE_ROLES             # engineer, developer, manager, scientist
   JOB_TITLE_DOMAINS           # ML, AI, data, frontend, backend
   KEYWORD_PATTERNS            # Technologies, frameworks, tools
   ```

3. **Methods**
   - `extract_job_description_keywords()` - Full JD analysis
   - `analyze_job_title()` - Parse title components
   - `batch_analyze_job_titles()` - Aggregate analysis
   - `smart_search()` - Hybrid AI + SQLite search
   - `_expand_keyword()` - Semantic expansion

## 🔧 Core Features

### 1. Job Description Keyword Extraction

**Method**: `extract_job_description_keywords(jd_text: str)`

**Returns**:
```python
{
    'required_skills': ['Python', 'AWS', 'Docker', ...],
    'nice_to_have': ['PhD', 'Kubernetes', 'Published research', ...],
    'experience': {
        'years_required': 5,
        'mentions': 2
    },
    'education': ['bachelor', 'MS'],
    'tech_stack': [
        {
            'keyword': 'python',
            'frequency': 7,
            'confidence': 0.95,
            'method': 'openai'
        },
        ...
    ],
    'soft_skills': ['communication', 'leadership', 'teamwork'],
    'keyword_counts': {
        'python': 7,
        'aws': 3,
        'docker': 2,
        ...
    }
}
```

**Features**:
- ✅ Extracts experience requirements with regex ("5+ years", "minimum of 3 years")
- ✅ Parses education levels (BS, MS, PhD)
- ✅ Counts keyword frequency across JD text
- ✅ Splits required skills vs nice-to-have based on section markers
- ✅ Detects soft skills (communication, leadership, etc.)
- ✅ Confidence scoring: Regex (90%), spaCy (75%), OpenAI (95%)

**Example**:
```python
from services.exa_service.keyword_extractor import get_keyword_extractor

extractor = get_keyword_extractor()

jd_text = """
Senior ML Engineer - 5+ years Python required.
Must have AWS, Docker, TensorFlow experience.
Nice to have: PhD in ML, Kubernetes expertise.
"""

result = extractor.extract_job_description_keywords(jd_text)

print(f"Experience: {result['experience']['years_required']} years")
print(f"Required: {result['required_skills']}")
print(f"Nice-to-have: {result['nice_to_have']}")
print(f"Keyword counts: {result['keyword_counts']}")
```

### 2. Job Title Analysis

**Method**: `analyze_job_title(job_title: str)`

**Returns**:
```python
{
    'original_title': 'Senior Machine Learning Engineer',
    'level': 'senior',
    'role': 'engineer',
    'domain': 'ml',
    'keywords': ['senior', 'machine', 'learning', 'engineer'],
    'seniority_score': 100  # 0-100 scale
}
```

**Seniority Scoring**:
- **0-30**: Entry level, junior, associate
- **40-60**: Mid-level, II, III
- **70-100**: Senior, staff, principal, lead, chief

**Example**:
```python
analysis = extractor.analyze_job_title("Staff ML Engineer")

# Output:
# {
#     'level': 'staff',
#     'role': 'engineer', 
#     'domain': 'ml',
#     'seniority_score': 100
# }
```

### 3. Batch Job Title Analysis

**Method**: `batch_analyze_job_titles(job_titles: List[str])`

**Returns**:
```python
{
    'total_titles': 7,
    'average_seniority': 57.1,
    'most_common_levels': [
        {'item': 'senior', 'count': 3},
        {'item': 'junior', 'count': 2},
        ...
    ],
    'most_common_roles': [
        {'item': 'engineer', 'count': 5},
        {'item': 'developer', 'count': 2}
    ],
    'most_common_domains': [
        {'item': 'ml', 'count': 3},
        {'item': 'backend', 'count': 2}
    ]
}
```

**Use Cases**:
- Analyze all job titles for a company
- Identify hiring trends (seniority distribution)
- Detect most common roles/domains

### 4. Smart Hybrid Search

**Method**: `smart_search(query: str, search_type: str = 'hybrid')`

**Search Types**:
- `'hybrid'`: AI interpretation + exact matching (recommended)
- `'semantic'`: AI understanding only (broad)
- `'keyword'`: Exact matching only (narrow)

**Returns**:
```python
{
    'original_query': 'Find companies hiring Python developers',
    'extracted_keywords': ['python'],
    'extracted_level': None,
    'extracted_role': 'developers',
    'extracted_location': None,
    'semantic_expansions': {
        'python': ['django', 'flask', 'fastapi', 'pandas']
    },
    'sql_where_clauses': [
        "content_type = 'careers'",
        "(text_content LIKE '%python%' OR title LIKE '%python%')",
        "(text_content LIKE '%django%' OR ...)",
        ...
    ],
    'final_sql': "SELECT * FROM company_sources WHERE ..."
}
```

**Semantic Expansion**:
```python
# Keyword → Related terms
'python'     → ['django', 'flask', 'fastapi', 'pandas']
'ml'         → ['machine learning', 'tensorflow', 'pytorch', 'scikit-learn']
'aws'        → ['amazon web services', 'ec2', 's3', 'lambda']
'javascript' → ['js', 'node.js', 'react', 'angular', 'vue']
'backend'    → ['server-side', 'api', 'database', 'rest']
```

**Example**:
```python
query = "Find companies hiring senior Python developers in Seattle"

result = extractor.smart_search(query, search_type='hybrid')

print(f"Keywords: {result['extracted_keywords']}")
print(f"Level: {result['extracted_level']}")
print(f"Role: {result['extracted_role']}")
print(f"Location: {result['extracted_location']}")
print(f"\nGenerated SQL:\n{result['final_sql']}")

# Execute the SQL
# db.execute(result['final_sql'])
```

## 🎨 Admin Portal Integration

### Page 27 - JD Analysis Tab

**Location**: `admin_portal/pages/27_Exa_Web_Intelligence.py`

**Features**:

1. **JD Keyword Extraction Subtab**
   - Paste job description text
   - Extract required skills, nice-to-have, experience, education
   - View tech stack with frequency counts
   - Bar chart of keyword frequencies
   - Download full analysis as JSON

2. **Job Title Analysis Subtab**
   - Single title analysis (level, role, domain, seniority score)
   - Batch analysis (multiple titles, aggregated stats)
   - View individual analyses in expandable sections

3. **Smart Search Subtab**
   - Natural language search input
   - Choose search type (hybrid/semantic/keyword)
   - View extracted components
   - See semantic expansions
   - Generated SQLite WHERE clauses and full SQL
   - Download search strategy as JSON

**Usage**:
```
1. Navigate to Admin Portal → Page 27 → JD Analysis tab
2. Paste a job description or enter job titles
3. Click "Extract Keywords" or "Analyze"
4. View results, charts, and generated SQL
5. Download JSON for further processing
```

## 🧪 Testing

### Test Suite

**File**: `test_jd_keyword_search.py`

**Tests**:
1. `test_jd_keyword_extraction()` - Full JD analysis
2. `test_job_title_analysis()` - Single and batch title parsing
3. `test_smart_search()` - Hybrid search query generation
4. `test_keyword_comparison()` - Multi-JD comparison

**Run Tests**:
```bash
cd c:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION
python test_jd_keyword_search.py
```

**Sample Output**:
```
TEST 1: JOB DESCRIPTION KEYWORD EXTRACTION
=============================================================================

📋 Experience Required: {'years_required': 5, 'mentions': 2}

🎓 Education: bachelor, MS

✅ Required Skills (10):
   - Python
   - TensorFlow
   - PyTorch
   - AWS
   - SQL

💎 Nice-to-Have (5):
   - PhD
   - Kubernetes
   - Docker
   - Research
   - Leadership

🔧 Tech Stack (Top 10 by frequency):
   - python: 7 mentions (confidence: 0.95)
   - aws: 3 mentions (confidence: 0.90)
   - docker: 2 mentions (confidence: 0.75)

📊 Keyword Frequency Count:
   python: 7
   aws: 3
   tensorflow: 2
   ...
```

## 📊 Use Cases

### 1. Job Matching
```python
# Extract keywords from candidate resume
candidate_skills = ['Python', 'AWS', 'Docker', 'ML']

# Extract from job description
jd_result = extractor.extract_job_description_keywords(jd_text)
required = jd_result['required_skills']

# Calculate match score
match_score = len(set(candidate_skills) & set(required)) / len(required)
print(f"Match: {match_score * 100:.0f}%")
```

### 2. Company Hiring Trends
```python
# Analyze all job titles from company
titles = [
    "Senior ML Engineer",
    "Staff Software Developer",
    "Principal Data Scientist",
    ...
]

batch_result = extractor.batch_analyze_job_titles(titles)

print(f"Average seniority: {batch_result['average_seniority']:.0f}/100")
print(f"Most hired role: {batch_result['most_common_roles'][0]['item']}")
print(f"Top domain: {batch_result['most_common_domains'][0]['item']}")
```

### 3. Smart Job Search
```python
# User enters natural language query
query = "Find remote ML jobs at startups paying over $150k"

# Generate search
result = extractor.smart_search(query, search_type='hybrid')

# Execute SQLite query
sql = result['final_sql']
jobs = db.execute(sql).fetchall()

print(f"Found {len(jobs)} matching jobs")
```

### 4. Keyword Frequency Analysis
```python
# Compare multiple JDs to find common requirements
jd_texts = [jd1, jd2, jd3, ...]

all_keywords = []
for jd in jd_texts:
    result = extractor.extract_job_description_keywords(jd)
    all_keywords.extend(result['required_skills'])

from collections import Counter
common = Counter(all_keywords).most_common(10)

print("Top 10 skills across all JDs:")
for skill, count in common:
    percentage = (count / len(jd_texts)) * 100
    print(f"{skill}: {count}/{len(jd_texts)} JDs ({percentage:.0f}%)")
```

## 🔑 Best Practices

### 1. Choose the Right Method

**For structured extraction** (experience, education):
```python
# Use extract_job_description_keywords()
# → Returns structured dict with regex-parsed requirements
```

**For job title parsing**:
```python
# Use analyze_job_title()
# → Returns level, role, domain components
```

**For search queries**:
```python
# Use smart_search() with hybrid mode
# → Best balance of precision and recall
```

### 2. Confidence Thresholds

- **Regex** (90%): Use for structured data (years, degrees)
- **spaCy** (75%): Use for entity extraction (locations, companies)
- **OpenAI** (95%): Use for semantic understanding (skills, technologies)

**Filter by confidence**:
```python
result = extractor.extract_job_description_keywords(jd_text)

high_confidence_skills = [
    skill for skill in result['tech_stack']
    if skill['confidence'] >= 0.90
]
```

### 3. Semantic Expansion

**Broad search** (high recall):
```python
result = extractor.smart_search(query, search_type='semantic')
# Includes many related terms
```

**Narrow search** (high precision):
```python
result = extractor.smart_search(query, search_type='keyword')
# Exact matching only
```

**Balanced** (recommended):
```python
result = extractor.smart_search(query, search_type='hybrid')
# AI understanding + exact matching
```

### 4. Caching

The extractor caches results locally to improve performance:

```python
# First call: ~2-5 seconds (OpenAI API)
result1 = extractor.extract_job_description_keywords(jd_text)

# Second call: ~0.1 seconds (cached)
result2 = extractor.extract_job_description_keywords(jd_text)
```

**Clear cache**:
```python
# Delete ai_data_final/exa_cache/keyword_extraction/
```

## 🚀 Future Enhancements

### Planned Features

1. **Resume Parsing**
   - Extract skills from candidate resumes
   - Match against JD requirements
   - Calculate compatibility scores

2. **Skill Gap Analysis**
   - Compare candidate skills vs JD requirements
   - Identify missing skills
   - Suggest training/upskilling

3. **Salary Prediction**
   - Predict salary range based on JD keywords
   - Use tech stack frequency and seniority score
   - Compare against market data

4. **Company Classification**
   - Classify companies by hiring patterns
   - Detect tech stack trends
   - Identify growth stages (startup vs enterprise)

5. **Custom Keyword Dictionaries**
   - User-defined semantic expansions
   - Industry-specific keyword patterns
   - Regional terminology variations

## 📚 API Reference

### Class: `KeywordExtractor`

**Initialization**:
```python
from services.exa_service.keyword_extractor import get_keyword_extractor

extractor = get_keyword_extractor()  # Singleton pattern
```

**Methods**:

#### `extract_job_description_keywords(jd_text: str) -> Dict`
Extract structured keywords from job description.

**Parameters**:
- `jd_text` (str): Full job description text

**Returns**: Dict with keys:
- `required_skills`: List[str]
- `nice_to_have`: List[str]
- `experience`: Dict
- `education`: List[str]
- `tech_stack`: List[Dict]
- `soft_skills`: List[str]
- `keyword_counts`: Dict[str, int]

---

#### `analyze_job_title(job_title: str) -> Dict`
Parse job title into components.

**Parameters**:
- `job_title` (str): Job title string

**Returns**: Dict with keys:
- `original_title`: str
- `level`: str (senior/junior/staff/etc.)
- `role`: str (engineer/developer/manager/etc.)
- `domain`: str (ml/ai/backend/etc.)
- `keywords`: List[str]
- `seniority_score`: int (0-100)

---

#### `batch_analyze_job_titles(job_titles: List[str]) -> Dict`
Aggregate analysis across multiple titles.

**Parameters**:
- `job_titles` (List[str]): List of job title strings

**Returns**: Dict with keys:
- `total_titles`: int
- `average_seniority`: float
- `most_common_levels`: List[Dict]
- `most_common_roles`: List[Dict]
- `most_common_domains`: List[Dict]

---

#### `smart_search(query: str, search_type: str = 'hybrid') -> Dict`
Generate SQLite search strategy from natural language.

**Parameters**:
- `query` (str): Natural language search query
- `search_type` (str): 'hybrid', 'semantic', or 'keyword'

**Returns**: Dict with keys:
- `original_query`: str
- `extracted_keywords`: List[str]
- `extracted_level`: str
- `extracted_role`: str
- `extracted_location`: str
- `semantic_expansions`: Dict[str, List[str]]
- `sql_where_clauses`: List[str]
- `final_sql`: str

---

## 💡 Examples

### Example 1: Full JD Analysis Pipeline
```python
from services.exa_service.keyword_extractor import get_keyword_extractor

extractor = get_keyword_extractor()

# Step 1: Extract from JD
jd_text = """
Senior Data Scientist - 5+ years Python, ML, SQL.
PhD preferred. Remote OK. $150k-$200k.
"""

result = extractor.extract_job_description_keywords(jd_text)

# Step 2: Analyze job title
title_analysis = extractor.analyze_job_title("Senior Data Scientist")

# Step 3: Generate search for similar jobs
query = f"Find {title_analysis['level']} {title_analysis['role']} roles"
search = extractor.smart_search(query, search_type='hybrid')

# Step 4: Display results
print(f"Required Skills: {result['required_skills']}")
print(f"Experience: {result['experience']['years_required']} years")
print(f"Seniority Score: {title_analysis['seniority_score']}/100")
print(f"Search SQL: {search['final_sql']}")
```

### Example 2: Company Hiring Analysis
```python
# Analyze all jobs from a company
company_jobs = [
    {"title": "Senior ML Engineer", "jd": "..."},
    {"title": "Staff Backend Developer", "jd": "..."},
    {"title": "Principal Data Scientist", "jd": "..."},
]

# Extract all job titles
titles = [job['title'] for job in company_jobs]
batch_result = extractor.batch_analyze_job_titles(titles)

print(f"Average Seniority: {batch_result['average_seniority']:.0f}/100")
print(f"Top Role: {batch_result['most_common_roles'][0]['item']}")

# Extract all tech keywords
all_tech = []
for job in company_jobs:
    result = extractor.extract_job_description_keywords(job['jd'])
    all_tech.extend([t['keyword'] for t in result['tech_stack']])

from collections import Counter
tech_counts = Counter(all_tech).most_common(5)

print("Top 5 Technologies:")
for tech, count in tech_counts:
    print(f"  {tech}: {count} jobs")
```

---

## 📞 Support

**Questions?** 
- Check `PHASES_1_TO_5_COMPLETE.md` for full Exa integration guide
- See `test_jd_keyword_search.py` for test examples
- Review Admin Page 27 → JD Analysis tab for UI examples

**Issues?**
- Verify OpenAI API key is set: `OPENAI_API_KEY` in `.env`
- Check spaCy model installed: `python -m spacy download en_core_web_sm`
- Enable debug logging: `ENABLE_VERBOSE_LOGGING=true` in `.env`

---

**Last Updated**: 2025-01-15  
**Version**: 1.0.0 (JD-Focused Enhancement)
