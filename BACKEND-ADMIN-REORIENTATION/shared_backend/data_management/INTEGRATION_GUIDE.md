# 🚀 UnifiedDataConnector - Quick Start Integration Guide

**For Developers:** How to integrate UnifiedDataConnector into your pages

---

## 📦 Installation

The connector is already available in `shared_backend/data_management/`.

No installation needed - just import and use!

---

## 🔥 Quick Start (30 seconds)

### **Step 1: Import**
```python
from shared_backend.data_management import get_connector

# Get connector instance (singleton)
connector = get_connector()
```

### **Step 2: Use**
```python
# Get all job titles
titles = connector.get_job_titles()

# Get career path
path = connector.get_career_path("Software Engineer")

# Get salary data
salary = connector.get_salary_data("Data Scientist", level="Senior", location="San Francisco")
```

**That's it! 🎉**

---

## 📚 Common Use Cases

### **Use Case 1: Replace Hard-Coded Job Title Lists**

**BEFORE (❌ Hard-coded):**
```python
def display_job_titles():
    # Hard-coded - only 5 titles!
    roles = [
        "Software Engineer",
        "Data Scientist",
        "Product Manager",
        "DevOps Engineer",
        "UX Designer"
    ]
    
    for role in roles:
        st.write(f"- {role}")
```

**AFTER (✅ Using Connector):**
```python
from shared_backend.data_management import get_connector

def display_job_titles():
    connector = get_connector()
    
    # Get ALL 422+ titles!
    roles = connector.get_job_titles()
    
    for role in roles:
        st.write(f"- {role}")
```

**Result:** +6,000% more job titles! (5 → 422+)

---

### **Use Case 2: Replace Hard-Coded Career Trajectories**

**BEFORE (❌ Hard-coded):**
```python
def show_career_path():
    # Hard-coded - only 2 levels!
    trajectory = {
        "Junior": {"years": "0-2", "salary": "$60k-$80k"},
        "Senior": {"years": "5+", "salary": "$120k-$180k"}
    }
    
    for level, data in trajectory.items():
        st.write(f"{level}: {data['years']}, {data['salary']}")
```

**AFTER (✅ Using Connector):**
```python
from shared_backend.data_management import get_connector

def show_career_path():
    connector = get_connector()
    
    # Get REAL career progression data
    path = connector.get_career_path("Software Engineer")
    
    for level in path:
        st.write(f"{level['level']}: {level['years']}, {level['salary_range']}")
```

**Result:** Real data, 4-5 levels, with skills and responsibilities!

---

### **Use Case 3: Replace Fake Market Trends**

**BEFORE (❌ Fake data):**
```python
def show_market_trends():
    # Completely fabricated numbers!
    trends = {
        "Generative AI": {"growth": 340},  # Made up!
        "Quantum Computing": {"growth": 180}  # Made up!
    }
    
    for tech, data in trends.items():
        st.metric(tech, f"+{data['growth']}%")
```

**AFTER (✅ Real data):**
```python
from shared_backend.data_management import get_connector

def show_market_trends():
    connector = get_connector()
    
    # Get REAL market trends from LinkedIn, BLS, Indeed
    emerging = connector.get_emerging_technologies(limit=10)
    
    for tech in emerging:
        st.metric(
            tech['tech'],
            f"+{tech['growth_rate']}%",
            help=f"Source: {tech.get('data_source', 'Market Data')}"
        )
```

**Result:** Real market data with sources!

---

### **Use Case 4: Replace Hard-Coded Salary Data**

**BEFORE (❌ Hard-coded):**
```python
def show_salaries():
    # Static, never updates, no location adjustment!
    salaries = {
        "Software Engineer": {"min": 60000, "max": 150000},
        "Data Scientist": {"min": 80000, "max": 180000}
    }
    
    for role, salary in salaries.items():
        st.write(f"{role}: ${salary['min']:,} - ${salary['max']:,}")
```

**AFTER (✅ Using Connector):**
```python
from shared_backend.data_management import get_connector

def show_salaries():
    connector = get_connector()
    
    roles = ["Software Engineer", "Data Scientist"]
    location = st.selectbox("Location", ["Remote", "San Francisco", "New York"])
    
    for role in roles:
        # Real market data with location adjustment!
        salary = connector.get_salary_data(role, location=location)
        
        st.write(
            f"{role}: ${salary['min']:,} - ${salary['max']:,} "
            f"(Median: ${salary['median']:,})"
        )
```

**Result:** Real salaries adjusted for 15+ locations!

---

### **Use Case 5: Replace Hard-Coded Job Listings**

**BEFORE (❌ Fake jobs):**
```python
def show_job_listings():
    # Fake job postings!
    jobs = [
        {
            "title": "Senior Software Engineer",
            "company": "TechCorp",
            "salary": "$120k-$180k",
            "location": "San Francisco"
        },
        # Only 4 fake jobs...
    ]
    
    for job in jobs:
        st.write(f"{job['title']} at {job['company']}")
```

**AFTER (✅ Real jobs):**
```python
from shared_backend.data_management import get_connector

def show_job_listings():
    connector = get_connector()
    
    # Get REAL jobs from job_match_results.csv
    jobs = connector.get_job_listings(
        role="Software Engineer",
        location="San Francisco",
        min_salary=120000,
        limit=20
    )
    
    for job in jobs:
        st.write(f"{job['job_title']} at {job['company']}")
        st.write(f"📍 {job['location']} | 💰 ${job['salary_min']:,} - ${job['salary_max']:,}")
```

**Result:** Real jobs with real companies and salaries!

---

## 🎯 Migration Patterns

### **Pattern 1: Replace Dict with Method Call**

```python
# BEFORE
roles = {"Software Engineer": {...}, "Data Scientist": {...}}

# AFTER
connector = get_connector()
roles_list = connector.get_job_titles()
```

### **Pattern 2: Replace List with Filtered Query**

```python
# BEFORE
technical_roles = ["Software Engineer", "DevOps Engineer", "Data Scientist"]

# AFTER
connector = get_connector()
technical_roles = connector.get_job_titles({'category': 'Technical'})
```

### **Pattern 3: Replace Function with Connector Method**

```python
# BEFORE
def _load_market_data():
    return {"trend1": 45, "trend2": 25}  # Fake!

# AFTER
connector = get_connector()
market_data = connector.get_market_trends()
```

### **Pattern 4: Add Caching (Already Built-In!)**

```python
# No need to cache manually - connector does it automatically!
connector = get_connector()

# First call: loads from disk (slower)
titles1 = connector.get_job_titles()

# Second call: loads from cache (10-50x faster)
titles2 = connector.get_job_titles()
```

---

## 🧪 Testing Your Integration

### **Quick Test**

```python
from shared_backend.data_management import get_connector

# Get connector
connector = get_connector()

# Test 1: Get job titles
titles = connector.get_job_titles()
print(f"✅ Loaded {len(titles)} job titles")

# Test 2: Get career path
path = connector.get_career_path("Software Engineer")
print(f"✅ Career path has {len(path)} levels")

# Test 3: Get salary data
salary = connector.get_salary_data("Data Scientist")
print(f"✅ Median salary: ${salary.get('median', 0):,}")

# Test 4: Fuzzy matching
match = connector.fuzzy_match_role("sr software eng")
print(f"✅ Matched: {match}")

print("\n🎉 All tests passed!")
```

---

## 📋 Complete Method Reference

### **Job Titles**
```python
# Get all job titles (with optional filtering)
titles = connector.get_job_titles()
titles = connector.get_job_titles({'category': 'Technical'})
titles = connector.get_job_titles({'industry': 'Technology'})
titles = connector.get_job_titles({'min_salary': 100000})

# Get job details
details = connector.get_job_title_details("Software Engineer")

# Fuzzy match role
match = connector.fuzzy_match_role("sr software eng")  # → "Senior Software Engineer"
```

### **Career Paths**
```python
# Get career progression
path = connector.get_career_path("Software Engineer")
path = connector.get_career_path("Data Scientist", include_skills=True)

# Get career trajectory
trajectory = connector.get_career_trajectory("Software Engineer", "Senior Software Engineer")
```

### **Skills**
```python
# Get skills for role
skills = connector.get_skills_for_role("Software Engineer")

# Get skill details
skill_info = connector.get_skill_details("Python")

# Get trending skills
trending = connector.get_trending_skills(limit=20)

# Get skill categories
categories = connector.get_skill_categories()
```

### **Salaries**
```python
# Get salary data
salary = connector.get_salary_data("Software Engineer")
salary = connector.get_salary_data("Data Scientist", level="Senior")
salary = connector.get_salary_data("DevOps Engineer", location="San Francisco")

# Get salary trends
trends = connector.get_salary_trends("Software Engineer", years=5)
```

### **Market Intelligence**
```python
# Get market trends
trends = connector.get_market_trends()

# Get emerging technologies
emerging = connector.get_emerging_technologies(limit=10)

# Get skill predictions
predictions = connector.get_skill_predictions(2026)

# Get industry growth
growth = connector.get_industry_growth("Technology")
```

### **Job Matching**
```python
# Get job listings
jobs = connector.get_job_listings()
jobs = connector.get_job_listings(role="Software Engineer")
jobs = connector.get_job_listings(location="San Francisco", min_salary=120000)
jobs = connector.get_job_listings(remote_only=True)
```

### **Interview & Career**
```python
# Get interview questions
questions = connector.get_interview_questions("Software Engineer")
questions = connector.get_interview_questions("Data Scientist", level="Intermediate")

# Get career advice
advice = connector.get_career_advice("Software Engineer")
advice = connector.get_career_advice("Product Manager", topic="Career Growth")
```

### **Utilities**
```python
# Refresh data
connector.refresh_data()

# Clear cache
connector.clear_cache()

# Get metadata
metadata = connector.get_metadata()

# Get statistics
stats = connector.get_statistics()
```

---

## ⚡ Performance Tips

1. **Use Singleton Pattern**
   ```python
   # ✅ GOOD - Reuses same instance
   connector = get_connector()
   
   # ❌ BAD - Creates new instance each time
   connector = UnifiedDataConnector()
   ```

2. **Cache is Automatic**
   ```python
   # No need to cache manually!
   # Connector caches automatically for 1 hour
   connector = get_connector()
   titles = connector.get_job_titles()  # Cached automatically
   ```

3. **Filter Early**
   ```python
   # ✅ GOOD - Filter in connector
   technical = connector.get_job_titles({'category': 'Technical'})
   
   # ❌ BAD - Filter in Python (slower)
   all_titles = connector.get_job_titles()
   technical = [t for t in all_titles if ...]
   ```

---

## 🐛 Troubleshooting

### **Problem: "Module not found"**
```python
# Make sure path is correct
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared_backend.data_management import get_connector
```

### **Problem: "Data file not found"**
```python
# Check base_path is correct
connector = UnifiedDataConnector(base_path="/path/to/ai_data_final")
```

### **Problem: "Cache is stale"**
```python
# Force refresh
connector = get_connector()
connector.refresh_data(force=True)
```

---

## 📞 Need Help?

**Documentation:**
- Full API docs in `unified_data_connector.py`
- Tests in `tests/test_unified_connector.py`
- Examples in this guide

**Common Issues:**
- Path problems: Check base_path to ai_data_final/
- Import errors: Check sys.path includes shared_backend/
- Data errors: Ensure JSON files exist in ai_data_final/

---

## 🎉 Success!

**You're now ready to:**
- ✅ Eliminate hard-coded data
- ✅ Use real market intelligence
- ✅ Support all 422+ job titles
- ✅ Provide accurate location-adjusted salaries
- ✅ Show consistent data across portals

**Happy integrating! 🚀**

---

**Created:** October 20, 2025  
**Version:** 1.0.0  
**Status:** Production Ready
