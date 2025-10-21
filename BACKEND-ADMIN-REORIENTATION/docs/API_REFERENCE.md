# API Reference: Dynamic Intelligence System

**Version:** 1.0  
**Last Updated:** October 21, 2025  
**Status:** Production Ready ✅

---

## 📚 Quick Links

- [PortalBridge Class](#portalbridge-class)
- [IntelligenceTypeRegistry Class](#intelligencetyperegistry-class)
- [HybridAIIntegrator Class](#hybridaiintegrator-class)
- [InferenceEngine Class](#inferenceengine-class)
- [Return Value Formats](#return-value-formats)
- [Error Codes](#error-codes)
- [Data Structures](#data-structures)

---

## PortalBridge Class

**Location:** `shared_backend/services/portal_bridge.py`

**Description:** Primary interface for all portal pages to access AI intelligence. Provides unified API with 21 methods for different intelligence types.

### Constructor

```python
PortalBridge()
```

**Description:** Initialize Portal Bridge with access to all 8 AI engines and intelligence registry.

**Parameters:** None

**Returns:** PortalBridge instance

**Example:**
```python
from shared_backend.services.portal_bridge import PortalBridge

bridge = PortalBridge()
```

**Initialization Details:**
- Initializes `HybridAIIntegrator` (gives access to all 8 engines)
- Gets global `IntelligenceTypeRegistry` (70+ types)
- Sets up metadata tracking
- Ready to serve intelligence requests

---

### Universal Intelligence Method

#### `get_intelligence(intelligence_type, data, portal_type='user', **kwargs)`

**Description:** Universal method to get ANY intelligence type. Most flexible method in the API.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `intelligence_type` | str | Yes | - | Intelligence type name (e.g., 'career_path', 'job_match') |
| `data` | dict | Yes | - | Input data for intelligence processing |
| `portal_type` | str | No | 'user' | Portal type: 'user', 'admin', or 'recruiter' |
| `**kwargs` | dict | No | {} | Additional parameters passed to handler |

**Returns:** `dict` - Intelligence result with status and type-specific fields

**Possible Statuses:**
- `'success'` - Intelligence generated successfully
- `'not_implemented'` - Type discovered but handler not implemented (returns helpful stub)
- `'error'` - Error occurred (returns error details)
- `'unknown'` - Intelligence type not found

**Example 1: Implemented Type**
```python
result = bridge.get_intelligence(
    intelligence_type='career_path',
    data={
        'current_role': 'Software Engineer',
        'experience_years': 5,
        'skills': ['Python', 'Django', 'PostgreSQL']
    },
    portal_type='user'
)

# Returns:
{
    'status': 'success',
    'career_path': ['Junior Dev', 'Software Engineer', 'Senior Engineer', 'Tech Lead'],
    'next_roles': ['Senior Software Engineer', 'Team Lead'],
    'growth_potential': 'HIGH',
    'portal_bridge_metadata': {
        'intelligence_type': 'career_path',
        'portal_type': 'user',
        'timestamp': '2025-10-21T10:30:00'
    }
}
```

**Example 2: Unimplemented Type (Stub)**
```python
result = bridge.get_intelligence(
    intelligence_type='interview_coach',
    data={'target_role': 'Senior Engineer'},
    portal_type='user'
)

# Returns:
{
    'status': 'not_implemented',
    'intelligence_type': 'interview_coach',
    'message': 'Type discovered but not yet implemented',
    'schema': {
        'questions': 'array of objects',
        'best_practices': 'array of strings',
        'example_answers': 'array of objects'
    },
    'example_usage': {...},
    'priority': 'MEDIUM',
    'hint': 'Auto-discovered from data files. Implementation coming soon!'
}
```

**Example 3: Error Handling**
```python
result = bridge.get_intelligence(
    intelligence_type='career_path',
    data={},  # Invalid: missing required fields
    portal_type='user'
)

# Returns:
{
    'status': 'error',
    'error': 'Missing required field: current_role',
    'intelligence_type': 'career_path'
}
```

---

### Career Intelligence Methods

#### `get_career_intelligence(profile_data)`

**Description:** Get comprehensive career intelligence including path, trajectory, and recommendations.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `profile_data` | dict | Yes | User profile with career history and skills |

**Required Fields in `profile_data`:**
- `current_role` (str): Current job title
- `experience_years` (int): Years of professional experience
- `skills` (list[str]): List of skills

**Returns:** `dict` - Career intelligence result

**Success Response:**
```json
{
    "status": "success",
    "career_path": ["Junior Dev", "Software Engineer", "Senior Engineer", "Tech Lead"],
    "next_roles": ["Senior Software Engineer", "Engineering Manager"],
    "growth_potential": "HIGH",
    "recommended_skills": ["System Design", "Leadership", "Cloud Architecture"],
    "career_level": "Mid-Level",
    "years_to_next_level": 2.5,
    "confidence": 0.92,
    "portal_bridge_metadata": {
        "intelligence_type": "career_path",
        "portal_type": "user",
        "timestamp": "2025-10-21T10:30:00"
    }
}
```

**Example:**
```python
profile = {
    'name': 'John Smith',
    'current_role': 'Software Engineer',
    'experience_years': 5,
    'skills': ['Python', 'JavaScript', 'React', 'PostgreSQL'],
    'education': 'BS Computer Science',
    'location': 'San Francisco, CA'
}

result = bridge.get_career_intelligence(profile)

if result['status'] == 'success':
    print(f"Career Path: {result['career_path']}")
    print(f"Next Roles: {result['next_roles']}")
    print(f"Growth Potential: {result['growth_potential']}")
```

#### `get_career_trajectory(profile_data)`

**Description:** Predict career trajectory over next 5-10 years with timelines.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `profile_data` | dict | Yes | User profile data |

**Returns:** `dict` - Career trajectory with timeline

**Success Response:**
```json
{
    "status": "success",
    "trajectory": [
        {"year": 2025, "role": "Software Engineer", "probability": 1.0},
        {"year": 2027, "role": "Senior Software Engineer", "probability": 0.85},
        {"year": 2029, "role": "Tech Lead", "probability": 0.70},
        {"year": 2032, "role": "Engineering Manager", "probability": 0.55}
    ],
    "peak_role": "VP of Engineering",
    "peak_year": 2035,
    "growth_rate": "ABOVE_AVERAGE",
    "confidence": 0.88
}
```

#### `get_career_advancement_plan(profile_data, target_role)`

**Description:** Generate personalized plan to advance to target role.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `profile_data` | dict | Yes | User profile data |
| `target_role` | str | Yes | Desired target role |

**Returns:** `dict` - Step-by-step advancement plan

**Success Response:**
```json
{
    "status": "success",
    "target_role": "Engineering Manager",
    "current_gap": "MEDIUM",
    "estimated_time": "2-3 years",
    "action_items": [
        {
            "action": "Develop leadership skills",
            "priority": "HIGH",
            "timeline": "6 months",
            "resources": ["Leadership course", "Mentorship"]
        },
        {
            "action": "Lead 2-3 projects",
            "priority": "HIGH",
            "timeline": "1 year",
            "resources": ["Internal projects", "Team initiatives"]
        }
    ],
    "milestones": [
        {"milestone": "Complete leadership training", "target_date": "2026-04-01"},
        {"milestone": "Lead first major project", "target_date": "2026-10-01"}
    ]
}
```

#### `get_career_pivot_analysis(profile_data, target_industry)`

**Description:** Analyze feasibility and requirements for pivoting to different industry.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `profile_data` | dict | Yes | User profile data |
| `target_industry` | str | Yes | Target industry (e.g., 'FinTech', 'Healthcare') |

**Returns:** `dict` - Pivot feasibility analysis

**Success Response:**
```json
{
    "status": "success",
    "target_industry": "FinTech",
    "feasibility": "HIGH",
    "transferable_skills": ["Python", "System Design", "API Development"],
    "skills_to_acquire": ["Financial Regulations", "Blockchain", "Payment Processing"],
    "estimated_transition_time": "6-12 months",
    "salary_impact": "+15%",
    "recommended_roles": ["FinTech Engineer", "Payment Systems Developer"],
    "next_steps": ["Get financial certifications", "Build fintech portfolio projects"]
}
```

---

### Job Intelligence Methods

#### `get_job_matches(profile_data, filters=None)`

**Description:** Find jobs matching user profile and optional filters.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `profile_data` | dict | Yes | User profile data |
| `filters` | dict | No | Job filters (location, salary, remote, etc.) |

**Filter Options:**
- `location` (str): Geographic location or "Remote"
- `min_salary` (int): Minimum salary
- `max_salary` (int): Maximum salary
- `company_size` (str): 'startup', 'mid-size', 'enterprise'
- `work_style` (str): 'remote', 'hybrid', 'onsite'

**Returns:** `dict` - Matching jobs list

**Success Response:**
```json
{
    "status": "success",
    "matches": [
        {
            "job_id": "job_12345",
            "title": "Senior Software Engineer",
            "company": "TechCorp",
            "location": "San Francisco, CA",
            "salary_range": "$140,000 - $180,000",
            "match_score": 92,
            "key_matches": ["Python", "System Design", "AWS"],
            "missing_skills": ["Kubernetes"],
            "work_style": "hybrid"
        }
    ],
    "total_matches": 25,
    "filters_applied": {"location": "San Francisco, CA", "min_salary": 120000}
}
```

**Example:**
```python
filters = {
    'location': 'Remote',
    'min_salary': 120000,
    'work_style': 'remote'
}

result = bridge.get_job_matches(profile_data, filters)

for job in result['matches']:
    print(f"{job['title']} at {job['company']}: {job['match_score']}% match")
```

#### `get_job_recommendations(profile_data, preferences=None)`

**Description:** Get personalized job recommendations based on profile and preferences.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `profile_data` | dict | Yes | User profile data |
| `preferences` | dict | No | User preferences |

**Returns:** `dict` - Recommended jobs

#### `get_job_market_insights(location, role)`

**Description:** Get market insights for specific role and location.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `location` | str | Yes | Geographic location |
| `role` | str | Yes | Job role/title |

**Returns:** `dict` - Market insights

**Success Response:**
```json
{
    "status": "success",
    "role": "Software Engineer",
    "location": "Austin, TX",
    "market_data": {
        "avg_salary": 115000,
        "salary_range": "$85,000 - $155,000",
        "openings_count": 342,
        "growth_trend": "INCREASING",
        "competition_level": "MEDIUM",
        "top_employers": ["Indeed", "Oracle", "Tesla"]
    },
    "demand_forecast": "High demand expected through 2026"
}
```

#### `get_job_application_optimization(profile_data, job_id)`

**Description:** Optimize application materials for specific job.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `profile_data` | dict | Yes | User profile data |
| `job_id` | str | Yes | Target job identifier |

**Returns:** `dict` - Application optimization suggestions

---

### Skill Intelligence Methods

#### `get_skill_recommendations(profile_data, target_role)`

**Description:** Get recommended skills to acquire for target role.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `profile_data` | dict | Yes | User profile data |
| `target_role` | str | Yes | Target role |

**Returns:** `dict` - Skill recommendations

**Success Response:**
```json
{
    "status": "success",
    "target_role": "DevOps Engineer",
    "recommended_skills": [
        {
            "skill": "Kubernetes",
            "priority": "HIGH",
            "proficiency_level": "Intermediate",
            "learning_time": "2-3 months",
            "resources": ["Kubernetes courses", "Practice clusters"],
            "demand": "VERY_HIGH"
        },
        {
            "skill": "Terraform",
            "priority": "HIGH",
            "proficiency_level": "Intermediate",
            "learning_time": "1-2 months",
            "resources": ["Terraform tutorials", "Practice projects"],
            "demand": "HIGH"
        }
    ],
    "skill_categories": {
        "container_orchestration": ["Kubernetes", "Docker Swarm"],
        "infrastructure_as_code": ["Terraform", "CloudFormation"],
        "ci_cd": ["Jenkins", "GitLab CI"]
    }
}
```

#### `get_skill_gap_analysis(profile_data, target_role)`

**Description:** Analyze skill gaps between current skills and target role requirements.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `profile_data` | dict | Yes | User profile data |
| `target_role` | str | Yes | Target role |

**Returns:** `dict` - Skill gap analysis

**Success Response:**
```json
{
    "status": "success",
    "target_role": "Cloud Architect",
    "current_skills": ["Python", "AWS", "Docker"],
    "required_skills": ["Python", "AWS", "Docker", "Kubernetes", "Terraform", "System Design"],
    "skill_gaps": [
        {
            "skill": "Kubernetes",
            "gap_level": "HIGH",
            "importance": "CRITICAL",
            "learning_priority": 1
        },
        {
            "skill": "Terraform",
            "gap_level": "MEDIUM",
            "importance": "HIGH",
            "learning_priority": 2
        }
    ],
    "overall_readiness": "65%",
    "estimated_preparation_time": "4-6 months"
}
```

#### `get_skill_development_path(profile_data, target_skills)`

**Description:** Generate learning path to develop target skills.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `profile_data` | dict | Yes | User profile data |
| `target_skills` | list[str] | Yes | Skills to develop |

**Returns:** `dict` - Skill development path

---

### Salary Intelligence Methods

#### `get_salary_insights(profile_data)`

**Description:** Get salary insights based on profile.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `profile_data` | dict | Yes | User profile data |

**Returns:** `dict` - Salary insights

**Success Response:**
```json
{
    "status": "success",
    "current_salary": 110000,
    "market_value": 125000,
    "percentile": 65,
    "salary_range": {
        "min": 95000,
        "median": 120000,
        "max": 160000
    },
    "factors": {
        "location": "High cost of living area",
        "experience": "Above average for level",
        "skills": "In-demand skill set"
    },
    "recommendations": [
        "You're paid below market value by 12%",
        "Consider negotiating or exploring new opportunities"
    ]
}
```

#### `get_salary_negotiation_intel(profile_data, job_offer)`

**Description:** Get intelligence for salary negotiation.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `profile_data` | dict | Yes | User profile data |
| `job_offer` | dict | Yes | Job offer details |

**Job Offer Fields:**
- `base_salary` (int): Offered base salary
- `equity` (int): Equity value
- `bonus` (int): Bonus amount
- `benefits` (dict): Benefits details

**Returns:** `dict` - Negotiation intelligence

**Success Response:**
```json
{
    "status": "success",
    "offer_analysis": {
        "base_salary": 130000,
        "total_compensation": 195000,
        "market_comparison": "FAIR",
        "percentile": 60
    },
    "negotiation_leverage": "MEDIUM",
    "recommended_counter": {
        "base_salary": 145000,
        "rationale": "Based on market data and your experience",
        "success_probability": 0.70
    },
    "talking_points": [
        "Your experience exceeds role requirements",
        "Specialized skills command premium",
        "Market data supports higher compensation"
    ]
}
```

---

### Company Intelligence Methods

#### `get_company_intelligence(company_id)`

**Description:** Get comprehensive intelligence about a company.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `company_id` | str | Yes | Company identifier |

**Returns:** `dict` - Company intelligence (stub currently)

#### `get_company_culture_analysis(company_id)`

**Description:** Analyze company culture and work environment.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `company_id` | str | Yes | Company identifier |

**Returns:** `dict` - Culture analysis (stub currently)

---

### Profile Intelligence Methods

#### `get_profile_strength_analysis(profile_data)`

**Description:** Analyze profile completeness and strength.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `profile_data` | dict | Yes | User profile data |

**Returns:** `dict` - Profile strength analysis (stub currently)

#### `get_profile_optimization_suggestions(profile_data)`

**Description:** Get suggestions to optimize profile.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `profile_data` | dict | Yes | User profile data |

**Returns:** `dict` - Optimization suggestions (stub currently)

---

### Admin Methods

#### `get_system_analytics()`

**Description:** Get system-wide analytics (admin only).

**Parameters:** None

**Returns:** `dict` - System analytics

**Success Response:**
```json
{
    "status": "success",
    "total_types": 72,
    "implemented_types": 4,
    "not_implemented_types": 68,
    "requests_today": 1543,
    "requests_per_minute": 12.5,
    "avg_response_time": 245.8,
    "success_rate": 98.5,
    "top_intelligence_types": [
        {"type": "career_path", "requests": 456},
        {"type": "job_match", "requests": 312},
        {"type": "skill_gaps", "requests": 289}
    ],
    "system_health": "HEALTHY"
}
```

#### `get_intelligence_types()`

**Description:** Get all discovered intelligence types with metadata.

**Parameters:** None

**Returns:** `dict` - Intelligence types list

**Success Response:**
```json
{
    "status": "success",
    "total_types": 72,
    "implemented_count": 4,
    "not_implemented_count": 68,
    "types": [
        {
            "name": "career_path",
            "category": "career",
            "priority": "HIGH",
            "implemented": true,
            "occurrences": 15,
            "source_files": ["complete_enhanced_analysis_eric_mehl_shell.json"]
        },
        {
            "name": "interview_coach",
            "category": "interview",
            "priority": "MEDIUM",
            "implemented": false,
            "occurrences": 3,
            "source_files": ["interview_intelligence.json"]
        }
    ],
    "by_category": {
        "career": ["career_path", "career_trajectory", ...],
        "job": ["job_match", "job_recommendations", ...],
        "skill": ["skill_gaps", "skill_recommendations", ...]
    },
    "by_priority": {
        "HIGH": 18,
        "MEDIUM": 32,
        "LOW": 22
    }
}
```

---

## IntelligenceTypeRegistry Class

**Location:** `shared_backend/ai_engines/intelligence_type_registry.py`

**Description:** Auto-discovers and manages intelligence types from JSON files.

### Discovery Methods

#### `discover_from_directory(directory_path)`

**Description:** Scan directory for JSON files and auto-discover intelligence types.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `directory_path` | Path | Yes | Path to directory containing JSON files |

**Returns:** `dict` - Discovery statistics

**Example:**
```python
from pathlib import Path
from shared_backend.ai_engines.intelligence_type_registry import get_global_registry

registry = get_global_registry()
data_dir = Path('ai_data_final/')

stats = registry.discover_from_directory(data_dir)

print(f"Types discovered: {stats['types_discovered']}")
print(f"Files scanned: {stats['files_scanned']}")
```

#### `get_type_info(type_name)`

**Description:** Get detailed information about an intelligence type.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type_name` | str | Yes | Intelligence type name |

**Returns:** `IntelligenceTypeInfo` object or `None`

**Example:**
```python
type_info = registry.get_type_info('career_path')

if type_info:
    print(f"Category: {type_info.category}")
    print(f"Priority: {type_info.priority}")
    print(f"Schema: {type_info.schema}")
    print(f"Sources: {type_info.source_files}")
```

#### `list_types(category=None, priority=None)`

**Description:** List intelligence types with optional filters.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `category` | str | No | Filter by category |
| `priority` | str | No | Filter by priority |

**Returns:** `list[str]` - List of type names

**Example:**
```python
# Get all types
all_types = registry.list_types()

# Get only career types
career_types = registry.list_types(category='career')

# Get only high priority types
high_priority = registry.list_types(priority='HIGH')
```

### Handler Methods

#### `register_handler(type_name, handler, priority, description)`

**Description:** Register handler function for intelligence type.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type_name` | str | Yes | Intelligence type name |
| `handler` | callable | Yes | Handler function |
| `priority` | str | Yes | Priority: 'HIGH', 'MEDIUM', 'LOW' |
| `description` | str | Yes | Handler description |

**Returns:** None

**Example:**
```python
def my_handler(data):
    return {'status': 'success', 'result': process(data)}

registry.register_handler(
    'my_intelligence_type',
    my_handler,
    priority='HIGH',
    description='My custom intelligence handler'
)
```

#### `get_handler(type_name)`

**Description:** Get registered handler for intelligence type.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type_name` | str | Yes | Intelligence type name |

**Returns:** `callable` or `None`

**Example:**
```python
handler = registry.get_handler('career_path')

if handler:
    result = handler(profile_data)
else:
    print("Handler not implemented")
```

#### `list_handlers()`

**Description:** List all registered handlers.

**Returns:** `dict` - Mapping of type names to handlers

---

## HybridAIIntegrator Class

**Location:** `shared_backend/ai_engines/hybrid_integrator.py`

**Description:** Orchestrates all 8 AI engines and provides dynamic routing.

### Core Methods

#### `run_inference(data, intelligence_type, **kwargs)`

**Description:** Run intelligence operation with dynamic routing.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `data` | dict | Yes | Input data |
| `intelligence_type` | str | Yes | Intelligence type |
| `**kwargs` | dict | No | Additional parameters |

**Returns:** `dict` - Intelligence result

**Example:**
```python
from shared_backend.ai_engines.hybrid_integrator import HybridAIIntegrator

integrator = HybridAIIntegrator()

result = integrator.run_inference(
    data=profile_data,
    intelligence_type='career_path'
)
```

#### `get_available_engines()`

**Description:** Get list of available AI engines.

**Returns:** `list[str]` - Engine names

#### `get_engine_status()`

**Description:** Get status of all engines.

**Returns:** `dict` - Engine status information

---

## InferenceEngine Class

**Location:** `shared_backend/ai_engines/inference_engine.py`

**Description:** 7th AI engine for intelligence operations.

### Inference Methods

#### `infer_career_path(profile_data)`

**Description:** Infer career path from profile.

**Returns:** `CareerPathResult` object

#### `match_job_to_candidate(profile_data, job_data)`

**Description:** Match job to candidate.

**Returns:** `JobMatchResult` object

#### `analyze_skill_gaps(profile_data, target_role)`

**Description:** Analyze skill gaps.

**Returns:** `SkillGapResult` object

#### `analyze_salary(profile_data)`

**Description:** Analyze salary expectations.

**Returns:** `SalaryAnalysisResult` object

---

## Return Value Formats

### Success Response

```json
{
    "status": "success",
    "intelligence_type": "career_path",
    "[type-specific fields]": "...",
    "confidence": 0.92,
    "portal_bridge_metadata": {
        "intelligence_type": "career_path",
        "portal_type": "user",
        "timestamp": "2025-10-21T10:30:00"
    }
}
```

### Not Implemented Response

```json
{
    "status": "not_implemented",
    "intelligence_type": "interview_coach",
    "message": "Type discovered but not yet implemented",
    "schema": {
        "field1": "type description",
        "field2": "type description"
    },
    "example_usage": {...},
    "priority": "MEDIUM",
    "category": "interview",
    "source_files": ["file1.json", "file2.json"],
    "hint": "Auto-discovered from data files. Implementation coming soon!"
}
```

### Error Response

```json
{
    "status": "error",
    "error": "Error message describing what went wrong",
    "intelligence_type": "career_path",
    "portal_bridge_metadata": {
        "intelligence_type": "career_path",
        "portal_type": "user",
        "timestamp": "2025-10-21T10:30:00"
    }
}
```

### Unknown Type Response

```json
{
    "status": "unknown",
    "error": "Unknown intelligence type: invalid_type",
    "available_types": ["career_path", "job_match", "..."],
    "total_types": 72,
    "hint": "Use available type, or add data files to auto-discover"
}
```

---

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | success | Intelligence generated successfully |
| 404 | unknown | Intelligence type not found |
| 501 | not_implemented | Type discovered but handler not implemented |
| 500 | error | Internal error occurred |

---

## Data Structures

### ProfileData

```python
{
    'name': str,
    'current_role': str,
    'experience_years': int,
    'skills': list[str],
    'education': str,
    'location': str,
    'salary': int (optional),
    'industry': str (optional),
    'company': str (optional)
}
```

### JobData

```python
{
    'job_id': str,
    'title': str,
    'company': str,
    'location': str,
    'salary_range': str,
    'required_skills': list[str],
    'preferred_skills': list[str],
    'experience_required': int,
    'work_style': str  # 'remote', 'hybrid', 'onsite'
}
```

### IntelligenceResult

```python
{
    'status': str,  # 'success', 'error', 'not_implemented', 'unknown'
    'intelligence_type': str,
    '[type-specific fields]': any,
    'confidence': float (optional),
    'portal_bridge_metadata': dict
}
```

### TypeInfo

```python
{
    'name': str,
    'category': str,
    'priority': str,  # 'HIGH', 'MEDIUM', 'LOW'
    'schema': dict,
    'examples': list[dict],
    'source_files': list[str],
    'occurrences': int,
    'implemented': bool
}
```

---

**Document Version:** 1.0  
**Last Updated:** October 21, 2025  
**Status:** ✅ Production Ready
