# Developer Guide: Dynamic Intelligence System

**Version:** 1.0  
**Last Updated:** October 21, 2025  
**Status:** Production Ready ✅

---

## 📚 Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Using Portal Bridge](#using-portal-bridge)
4. [Adding New Intelligence Types](#adding-new-intelligence-types)
5. [Implementing Handlers](#implementing-handlers)
6. [Working with Intelligence Types](#working-with-intelligence-types)
7. [Portal Integration Patterns](#portal-integration-patterns)
8. [Advanced Topics](#advanced-topics)
9. [Best Practices](#best-practices)
10. [Common Patterns](#common-patterns)
11. [Troubleshooting](#troubleshooting)

---

## 1. Introduction

### What is the Dynamic Intelligence System?

The **Dynamic Intelligence System** is a revolutionary approach to AI-powered career intelligence that eliminates hard-coded intelligence types and enables unlimited extensibility through auto-discovery.

**Key Innovation:** Instead of hard-coding 43 intelligence types, the system:
- ✅ Auto-discovers types from JSON data files
- ✅ Extracts schemas automatically
- ✅ Provides helpful stubs for unimplemented types
- ✅ Supports unlimited intelligence types (70+ discovered, 200+ projected)
- ✅ Requires ZERO code changes to add new types

### Key Benefits

**For Developers:**
- 🚀 **10x Faster Development:** Add new intelligence types by adding JSON files
- 📉 **75% Less Code:** Eliminated 280 lines of if/elif chains
- 🧪 **Better Testing:** Comprehensive test infrastructure
- 📖 **Self-Documenting:** Schemas extracted automatically

**For Users:**
- ⚡ **Faster Features:** New intelligence types deployed instantly
- 🎯 **More Intelligence:** 70+ types vs 4 before
- 🔧 **Better Errors:** Helpful stubs with schemas
- 📊 **Metadata Tracking:** Every request tracked

**For Business:**
- 💰 **Lower Costs:** Less maintenance, faster development
- 🔄 **More Flexibility:** Unlimited intelligence types
- 📈 **Better Insights:** Comprehensive analytics
- 🚀 **Faster Time-to-Market:** Hours instead of days

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        PORTAL LAYER                             │
│  ┌─────────────┬──────────────┬─────────────┬─────────────┐   │
│  │ User Portal │ Admin Portal │ Recruiter   │ Partner     │   │
│  │   Pages     │    Pages     │   Portal    │  Portal     │   │
│  └─────────────┴──────────────┴─────────────┴─────────────┘   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SERVICE LAYER                              │
│                    ┌─────────────────┐                          │
│                    │  PortalBridge   │                          │
│                    │   (560 lines)   │                          │
│                    │   21 Methods    │                          │
│                    └────────┬────────┘                          │
└─────────────────────────────┼───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       ENGINE LAYER                              │
│       ┌─────────────────────────────────────────┐               │
│       │     HybridAIIntegrator (Orchestrator)   │               │
│       │            (~790 lines)                 │               │
│       └──────────────────┬──────────────────────┘               │
│                          │                                       │
│   ┌──────────┬──────────┼──────────┬──────────┬──────────┐     │
│   ▼          ▼          ▼          ▼          ▼          ▼     │
│ Engine1  Engine2  Engine3  ... InferenceEngine (7th) Stats(8th)│
│                                  (1,277 lines)  (Wrapper)       │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     REGISTRY LAYER                              │
│              ┌───────────────────────────┐                      │
│              │ IntelligenceTypeRegistry  │                      │
│              │      (528 lines)          │                      │
│              │  - Auto-Discovery         │                      │
│              │  - Schema Extraction      │                      │
│              │  - Handler Management     │                      │
│              └───────────┬───────────────┘                      │
└──────────────────────────┼─────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                │
│         ┌─────────────────────────────────────┐                 │
│         │    ai_data_final/ Directory         │                 │
│         │    (3,502 JSON files)               │                 │
│         │    (28,698 intelligence types)      │                 │
│         └─────────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────────┘
```

**Data Flow:**
1. **Startup:** Registry scans `ai_data_final/` → Discovers 70+ types → Extracts schemas
2. **Request:** Portal page → PortalBridge → HybridAIIntegrator → Registry lookup → Handler execute
3. **Response:** Result + Metadata → Portal page → Display to user

---

## 2. Getting Started

### Prerequisites

**Required:**
- Python 3.10+
- Access to `shared_backend/` directory
- `ai_data_final/` directory with JSON files

**Optional:**
- pytest (for testing)
- Streamlit (for portal pages)

### Installation

**1. Verify Environment:**
```bash
# Check Python version
python --version  # Should be 3.10+

# Check shared_backend location
cd c:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION
ls shared_backend/
```

**2. Add to PYTHONPATH:**
```bash
# Windows PowerShell
$env:PYTHONPATH = "c:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION"

# Linux/Mac
export PYTHONPATH="/path/to/BACKEND-ADMIN-REORIENTATION"
```

**3. Verify Installation:**
```python
# Test import
from shared_backend.services.portal_bridge import PortalBridge

# Create instance
bridge = PortalBridge()
print("✅ Installation successful!")
```

### Your First Intelligence Request

**Simple Example:**
```python
from shared_backend.services.portal_bridge import PortalBridge

# Initialize Portal Bridge
bridge = PortalBridge()

# Prepare profile data
profile_data = {
    'name': 'John Smith',
    'current_role': 'Software Engineer',
    'experience_years': 5,
    'skills': ['Python', 'JavaScript', 'React'],
    'education': 'BS Computer Science'
}

# Get career intelligence
result = bridge.get_career_intelligence(profile_data)

# Display result
print(f"Status: {result['status']}")
print(f"Career Path: {result['career_path']}")
print(f"Next Roles: {result['next_roles']}")
```

**Expected Output:**
```json
{
    "status": "success",
    "career_path": ["Junior Dev", "Software Engineer", "Senior Engineer", "Tech Lead"],
    "next_roles": ["Senior Software Engineer", "Team Lead", "Engineering Manager"],
    "growth_potential": "HIGH",
    "recommended_skills": ["System Design", "Leadership", "Cloud Architecture"],
    "portal_bridge_metadata": {
        "intelligence_type": "career_path",
        "portal_type": "user",
        "timestamp": "2025-10-21T10:30:00"
    }
}
```

---

## 3. Using Portal Bridge

### Basic Usage

**Import and Initialize:**
```python
from shared_backend.services.portal_bridge import PortalBridge

# Create instance (typically in session state)
if 'portal_bridge' not in st.session_state:
    st.session_state.portal_bridge = PortalBridge()

bridge = st.session_state.portal_bridge
```

### Universal `get_intelligence()` Method

The most flexible method - works with ANY intelligence type:

```python
result = bridge.get_intelligence(
    intelligence_type='career_path',  # Any discovered type
    data=profile_data,                # Your data
    portal_type='user',               # 'user', 'admin', or 'recruiter'
    **kwargs                           # Additional parameters
)
```

**Example - Career Path:**
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
```

**Example - Salary Analysis:**
```python
result = bridge.get_intelligence(
    intelligence_type='salary_analysis',
    data={
        'current_role': 'Software Engineer',
        'location': 'San Francisco, CA',
        'experience_years': 5,
        'skills': ['Python', 'AWS', 'Docker']
    },
    portal_type='user'
)
```

**Example - Unimplemented Type (Gets Helpful Stub):**
```python
result = bridge.get_intelligence(
    intelligence_type='interview_coach',  # Not implemented yet
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
    'priority': 'MEDIUM',
    'hint': 'Auto-discovered from data files. Implementation coming soon!'
}
```

### Portal-Specific Methods (Convenience Functions)

**Career Intelligence (4 methods):**

```python
# 1. General career intelligence
result = bridge.get_career_intelligence(profile_data)

# 2. Career trajectory prediction
result = bridge.get_career_trajectory(profile_data)

# 3. Career advancement plan
result = bridge.get_career_advancement_plan(
    profile_data=profile_data,
    target_role='Engineering Manager'
)

# 4. Career pivot analysis
result = bridge.get_career_pivot_analysis(
    profile_data=profile_data,
    target_industry='FinTech'
)
```

**Job Intelligence (4 methods):**

```python
# 1. Job matches
result = bridge.get_job_matches(
    profile_data=profile_data,
    filters={'location': 'Remote', 'min_salary': 120000}
)

# 2. Job recommendations
result = bridge.get_job_recommendations(
    profile_data=profile_data,
    preferences={'work_style': 'remote', 'company_size': 'startup'}
)

# 3. Job market insights
result = bridge.get_job_market_insights(
    location='Austin, TX',
    role='Software Engineer'
)

# 4. Job application optimization
result = bridge.get_job_application_optimization(
    profile_data=profile_data,
    job_id='job_12345'
)
```

**Skill Intelligence (3 methods):**

```python
# 1. Skill recommendations
result = bridge.get_skill_recommendations(
    profile_data=profile_data,
    target_role='DevOps Engineer'
)

# 2. Skill gap analysis
result = bridge.get_skill_gap_analysis(
    profile_data=profile_data,
    target_role='Cloud Architect'
)

# 3. Skill development path
result = bridge.get_skill_development_path(
    profile_data=profile_data,
    target_skills=['Kubernetes', 'Terraform', 'AWS']
)
```

**Salary Intelligence (2 methods):**

```python
# 1. Salary insights
result = bridge.get_salary_insights(profile_data)

# 2. Salary negotiation intel
result = bridge.get_salary_negotiation_intel(
    profile_data=profile_data,
    job_offer={'base_salary': 130000, 'equity': 50000}
)
```

**Company Intelligence (2 methods):**

```python
# 1. Company intelligence
result = bridge.get_company_intelligence(company_id='company_456')

# 2. Company culture analysis
result = bridge.get_company_culture_analysis(company_id='company_456')
```

**Profile Intelligence (2 methods):**

```python
# 1. Profile strength analysis
result = bridge.get_profile_strength_analysis(profile_data)

# 2. Profile optimization suggestions
result = bridge.get_profile_optimization_suggestions(profile_data)
```

**Admin Methods (2 methods):**

```python
# 1. System analytics
analytics = bridge.get_system_analytics()
# Returns: system health, usage stats, performance metrics

# 2. Intelligence types list
types = bridge.get_intelligence_types()
# Returns: all 70+ discovered types with metadata
```

### Error Handling

**Best Practice:**
```python
try:
    result = bridge.get_career_intelligence(profile_data)
    
    if result['status'] == 'success':
        # Handle successful result
        display_career_path(result['career_path'])
    
    elif result['status'] == 'not_implemented':
        # Handle unimplemented type (show stub)
        st.info(f"Coming soon! Schema: {result['schema']}")
    
    elif result['status'] == 'error':
        # Handle error
        st.error(f"Error: {result['error']}")
        logger.error(f"Intelligence error: {result['error']}")
    
except Exception as e:
    st.error(f"Unexpected error: {e}")
    logger.exception("Portal bridge error")
```

---

## 4. Adding New Intelligence Types

### The Magic: Just Add JSON Files!

**No Code Changes Required!** 🎉

**Step 1: Create JSON File**

```bash
# Navigate to data directory
cd ai_data_final/

# Create new JSON file
# File name: new_intelligence_example.json
```

**Step 2: Add Intelligence Data**

```json
{
    "interview_coach": {
        "target_role": "Senior Software Engineer",
        "questions": [
            {
                "question": "Describe a complex system you designed",
                "difficulty": "hard",
                "topic": "system_design"
            },
            {
                "question": "How do you handle technical debt?",
                "difficulty": "medium",
                "topic": "leadership"
            }
        ],
        "best_practices": [
            "Use the STAR method",
            "Provide specific examples",
            "Quantify your impact"
        ],
        "example_answers": [
            {
                "question_id": 1,
                "answer": "At my previous company, I designed a distributed caching system..."
            }
        ],
        "preparation_tips": [
            "Research the company's tech stack",
            "Prepare 3-5 project examples",
            "Practice system design problems"
        ]
    }
}
```

**Step 3: Restart Application**

```bash
# Restart your Streamlit app
streamlit run app.py
```

**Step 4: Test Discovery**

```python
from shared_backend.services.portal_bridge import PortalBridge

bridge = PortalBridge()

# New type is now available!
result = bridge.get_intelligence(
    intelligence_type='interview_coach',
    data={'target_role': 'Senior Software Engineer'},
    portal_type='user'
)

print(result)
```

**Output:**
```json
{
    "status": "not_implemented",
    "intelligence_type": "interview_coach",
    "message": "Type 'interview_coach' discovered but not yet implemented",
    "schema": {
        "questions": "array of objects (3 properties: question, difficulty, topic)",
        "best_practices": "array of strings",
        "example_answers": "array of objects",
        "preparation_tips": "array of strings"
    },
    "example_usage": {
        "target_role": "Senior Software Engineer",
        "questions": [{"question": "...", "difficulty": "hard"}]
    },
    "priority": "MEDIUM",
    "category": "interview",
    "source_files": ["new_intelligence_example.json"],
    "hint": "Auto-discovered from data files. Implementation coming soon!"
}
```

**That's It!** 🎉
- ✅ Type discovered automatically
- ✅ Schema extracted automatically
- ✅ Stub response available immediately
- ✅ Ready to implement handler (optional)

### Discovery Rules

The registry recognizes these patterns:

**Pattern 1: Keys ending in `_intelligence`**
```json
{
    "career_intelligence": {...},  // Discovered as "career_intelligence"
    "company_intelligence": {...}  // Discovered as "company_intelligence"
}
```

**Pattern 2: Keys ending in `_analysis`**
```json
{
    "salary_analysis": {...},      // Discovered as "salary_analysis"
    "skill_gap_analysis": {...}    // Discovered as "skill_gap_analysis"
}
```

**Pattern 3: Keys ending in `_recommendations`**
```json
{
    "job_recommendations": {...},   // Discovered as "job_recommendations"
    "skill_recommendations": {...}  // Discovered as "skill_recommendations"
}
```

**Pattern 4: Nested structures**
```json
{
    "career_data": {
        "trajectory": {...},       // Discovered as "career_trajectory"
        "growth_potential": {...}  // Discovered as "career_growth_potential"
    }
}
```

---

## 5. Implementing Handlers

### When to Implement a Handler

**Use Stub Response When:**
- ✅ Type recently discovered
- ✅ Testing/prototyping
- ✅ Low priority feature
- ✅ Data-only response sufficient

**Implement Handler When:**
- ✅ Production feature
- ✅ Complex logic needed
- ✅ Multiple data sources
- ✅ Business rules required
- ✅ High priority feature

### Handler Function Signature

```python
def my_handler(data: dict) -> dict:
    """
    Handler for my_intelligence_type.
    
    Args:
        data: Input data dictionary containing required fields
        
    Returns:
        dict: Result with 'status' and intelligence-specific fields
        
    Raises:
        ValueError: If data validation fails
        Exception: For other errors
    """
    try:
        # 1. Validate input
        if 'required_field' not in data:
            raise ValueError("Missing required_field")
        
        # 2. Process data
        result = process_intelligence(data)
        
        # 3. Return result
        return {
            'status': 'success',
            'intelligence_type': 'my_intelligence_type',
            'result_field_1': result.field_1,
            'result_field_2': result.field_2,
            'confidence': 0.95
        }
        
    except Exception as e:
        logger.error(f"Handler error: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'intelligence_type': 'my_intelligence_type'
        }
```

### Registration Process

**Location:** `shared_backend/ai_engines/hybrid_integrator.py`

**Method:** `_register_intelligence_handlers()`

```python
def _register_intelligence_handlers(self):
    """Register implemented intelligence type handlers"""
    logger.info("Registering intelligence type handlers...")
    
    # Register your new handler
    self.intelligence_registry.register_handler(
        'interview_coach',                    # Type name (must match discovered type)
        self._interview_coach_handler,        # Handler function
        priority='HIGH',                      # Priority: HIGH, MEDIUM, LOW
        description='Interview preparation and coaching'  # Description
    )
    
    # Register more handlers...
    logger.info(f"Registered {len([...])} handlers")
```

### Complete Example: Implementing Interview Coach Handler

**Step 1: Implement Handler Function**

```python
def _interview_coach_handler(self, data: dict) -> dict:
    """
    Provide interview preparation and coaching.
    
    Args:
        data: {
            'target_role': str,
            'experience_years': int,
            'skills': list[str],
            'company': str (optional),
            'interview_type': str (optional)
        }
    
    Returns:
        dict: Interview coaching intelligence
    """
    try:
        # Validate input
        if 'target_role' not in data:
            raise ValueError("target_role is required")
        
        target_role = data['target_role']
        experience = data.get('experience_years', 0)
        skills = data.get('skills', [])
        company = data.get('company', 'General')
        interview_type = data.get('interview_type', 'technical')
        
        # Generate questions based on role and experience
        questions = self._generate_interview_questions(
            target_role, experience, interview_type
        )
        
        # Provide best practices
        best_practices = self._get_interview_best_practices(
            target_role, interview_type
        )
        
        # Generate example answers
        example_answers = self._generate_example_answers(
            questions, skills
        )
        
        # Preparation tips
        prep_tips = self._get_preparation_tips(
            target_role, company, skills
        )
        
        return {
            'status': 'success',
            'intelligence_type': 'interview_coach',
            'target_role': target_role,
            'interview_type': interview_type,
            'questions': questions,
            'best_practices': best_practices,
            'example_answers': example_answers,
            'preparation_tips': prep_tips,
            'confidence': 0.90,
            'recommended_practice_time': f"{len(questions) * 15} minutes"
        }
        
    except Exception as e:
        logger.error(f"Interview coach error: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'intelligence_type': 'interview_coach'
        }

def _generate_interview_questions(self, role, experience, type):
    """Generate role-appropriate questions"""
    # Implementation...
    return questions

def _get_interview_best_practices(self, role, type):
    """Get best practices for interview type"""
    # Implementation...
    return best_practices

def _generate_example_answers(self, questions, skills):
    """Generate example answers based on skills"""
    # Implementation...
    return example_answers

def _get_preparation_tips(self, role, company, skills):
    """Get personalized preparation tips"""
    # Implementation...
    return tips
```

**Step 2: Register Handler**

```python
def _register_intelligence_handlers(self):
    """Register all handlers"""
    
    # ... existing handlers ...
    
    # NEW: Register interview coach handler
    self.intelligence_registry.register_handler(
        'interview_coach',
        self._interview_coach_handler,
        priority='HIGH',
        description='Interview preparation and coaching intelligence'
    )
```

**Step 3: Test Handler**

```python
from shared_backend.services.portal_bridge import PortalBridge

bridge = PortalBridge()

result = bridge.get_intelligence(
    intelligence_type='interview_coach',
    data={
        'target_role': 'Senior Software Engineer',
        'experience_years': 5,
        'skills': ['Python', 'System Design', 'Leadership'],
        'company': 'Google',
        'interview_type': 'technical'
    },
    portal_type='user'
)

print(f"Status: {result['status']}")  # Should be 'success'
print(f"Questions: {len(result['questions'])}")
print(f"First question: {result['questions'][0]}")
```

### Priority Levels

**HIGH Priority:**
- Production-critical features
- User-facing intelligence
- Core business logic
- Implemented first

**MEDIUM Priority:**
- Important but not critical
- Admin features
- Analytics
- Implement second

**LOW Priority:**
- Experimental features
- Nice-to-have
- Internal tools
- Implement last

---

## 6. Working with Intelligence Types

### Discovering Available Types

```python
from shared_backend.services.portal_bridge import PortalBridge

bridge = PortalBridge()

# Get all intelligence types
types = bridge.get_intelligence_types()

print(f"Total types: {len(types['types'])}")
print(f"Implemented: {types['implemented_count']}")
print(f"Not implemented: {types['not_implemented_count']}")

# List by category
for category, type_list in types['by_category'].items():
    print(f"\n{category}: {len(type_list)} types")
    for type_name in type_list[:5]:  # Show first 5
        print(f"  - {type_name}")
```

### Viewing Type Schema

```python
# Get specific type information
result = bridge.get_intelligence(
    intelligence_type='interview_coach',
    data={},  # Empty data to get stub with schema
    portal_type='user'
)

if result['status'] == 'not_implemented':
    print("Schema:")
    for field, field_type in result['schema'].items():
        print(f"  {field}: {field_type}")
    
    print("\nExample:")
    print(result['example_usage'])
```

### Understanding Type Metadata

```python
# Access registry directly for detailed info
from shared_backend.ai_engines.intelligence_type_registry import get_global_registry

registry = get_global_registry()

# Get type info
type_info = registry.get_type_info('interview_coach')

print(f"Category: {type_info.category}")
print(f"Priority: {type_info.priority}")
print(f"Source files: {type_info.source_files}")
print(f"Occurrences: {type_info.occurrences}")
print(f"Schema: {type_info.schema}")
```

---

## 7. Portal Integration Patterns

### User Portal Pattern

```python
import streamlit as st
from shared_backend.services.portal_bridge import PortalBridge

def career_intelligence_page():
    """User portal career intelligence page"""
    
    st.title("Career Intelligence")
    
    # Initialize Portal Bridge (once per session)
    if 'portal_bridge' not in st.session_state:
        st.session_state.portal_bridge = PortalBridge()
    
    bridge = st.session_state.portal_bridge
    
    # Get user profile
    if 'user_profile' not in st.session_state:
        st.warning("Please complete your profile first")
        return
    
    profile_data = st.session_state.user_profile
    
    # Career Intelligence Section
    st.header("Your Career Path")
    
    with st.spinner("Analyzing your career trajectory..."):
        try:
            result = bridge.get_career_intelligence(profile_data)
            
            if result['status'] == 'success':
                # Display career path
                st.success("Career Analysis Complete!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        "Growth Potential",
                        result.get('growth_potential', 'N/A')
                    )
                
                with col2:
                    st.metric(
                        "Next Level",
                        result.get('next_level', 'N/A')
                    )
                
                # Career trajectory
                st.subheader("Career Trajectory")
                career_path = result.get('career_path', [])
                for i, role in enumerate(career_path):
                    st.write(f"{i+1}. {role}")
                
                # Recommended skills
                st.subheader("Recommended Skills")
                skills = result.get('recommended_skills', [])
                for skill in skills:
                    st.badge(skill)
            
            elif result['status'] == 'not_implemented':
                st.info("🚧 Coming soon! This feature is under development.")
                with st.expander("Preview Schema"):
                    st.json(result['schema'])
            
            else:
                st.error(f"Error: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            logger.exception("Career intelligence error")
```

### Admin Portal Pattern

```python
import streamlit as st
from shared_backend.services.portal_bridge import PortalBridge

def admin_analytics_page():
    """Admin portal analytics page"""
    
    st.title("Admin: System Analytics")
    
    # Initialize Portal Bridge
    if 'portal_bridge' not in st.session_state:
        st.session_state.portal_bridge = PortalBridge()
    
    bridge = st.session_state.portal_bridge
    
    # Get system analytics
    try:
        analytics = bridge.get_system_analytics()
        
        # Display KPIs
        st.header("Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Intelligence Types",
                analytics.get('total_types', 0)
            )
        
        with col2:
            st.metric(
                "Implemented Types",
                analytics.get('implemented_types', 0)
            )
        
        with col3:
            st.metric(
                "Requests Today",
                analytics.get('requests_today', 0)
            )
        
        with col4:
            st.metric(
                "Avg Response Time",
                f"{analytics.get('avg_response_time', 0):.2f}ms"
            )
        
        # Intelligence type breakdown
        st.header("Intelligence Types by Category")
        
        types = bridge.get_intelligence_types()
        
        for category, type_list in types['by_category'].items():
            with st.expander(f"{category.title()} ({len(type_list)} types)"):
                for type_name in type_list:
                    handler = registry.get_handler(type_name)
                    status = "✅ Implemented" if handler else "⏳ Stub"
                    st.write(f"- {type_name}: {status}")
        
    except Exception as e:
        st.error(f"Error loading analytics: {e}")
```

### Recruiter Portal Pattern

```python
import streamlit as st
from shared_backend.services.portal_bridge import PortalBridge

def candidate_matching_page():
    """Recruiter portal candidate matching"""
    
    st.title("Candidate Matching")
    
    # Initialize Portal Bridge
    if 'portal_bridge' not in st.session_state:
        st.session_state.portal_bridge = PortalBridge()
    
    bridge = st.session_state.portal_bridge
    
    # Job requirements
    st.header("Job Requirements")
    
    job_data = {
        'role': st.text_input("Role", "Senior Software Engineer"),
        'required_skills': st.multiselect(
            "Required Skills",
            ["Python", "Java", "JavaScript", "React", "AWS"]
        ),
        'experience_years': st.slider("Years of Experience", 0, 20, 5),
        'location': st.text_input("Location", "San Francisco, CA")
    }
    
    if st.button("Find Candidates"):
        with st.spinner("Finding matching candidates..."):
            try:
                # Get candidate matches
                result = bridge.get_intelligence(
                    intelligence_type='candidate_matching',
                    data=job_data,
                    portal_type='recruiter'
                )
                
                if result['status'] == 'success':
                    candidates = result.get('candidates', [])
                    
                    st.success(f"Found {len(candidates)} matching candidates")
                    
                    for candidate in candidates:
                        with st.container():
                            col1, col2, col3 = st.columns([3, 2, 1])
                            
                            with col1:
                                st.subheader(candidate['name'])
                                st.write(candidate['current_role'])
                            
                            with col2:
                                st.metric("Match Score", f"{candidate['match_score']}%")
                            
                            with col3:
                                if st.button(f"View {candidate['name']}", key=candidate['id']):
                                    st.session_state.selected_candidate = candidate
                
                else:
                    st.warning(result.get('message', 'No matches found'))
                    
            except Exception as e:
                st.error(f"Error: {e}")
```

### Error Handling Pattern

```python
def safe_intelligence_request(bridge, intelligence_type, data, portal_type='user'):
    """
    Safe wrapper for intelligence requests with comprehensive error handling.
    
    Returns:
        tuple: (success: bool, result: dict)
    """
    try:
        result = bridge.get_intelligence(
            intelligence_type=intelligence_type,
            data=data,
            portal_type=portal_type
        )
        
        if result['status'] == 'success':
            return True, result
        
        elif result['status'] == 'not_implemented':
            logger.info(f"Type '{intelligence_type}' not yet implemented")
            return False, {
                'error': 'Feature coming soon',
                'schema': result.get('schema'),
                'message': result.get('message')
            }
        
        elif result['status'] == 'error':
            logger.error(f"Intelligence error: {result.get('error')}")
            return False, {
                'error': result.get('error', 'Unknown error'),
                'type': intelligence_type
            }
        
        else:
            logger.warning(f"Unknown status: {result['status']}")
            return False, {'error': 'Unknown response status'}
    
    except Exception as e:
        logger.exception(f"Unexpected error in {intelligence_type}")
        return False, {'error': str(e)}

# Usage:
success, result = safe_intelligence_request(
    bridge,
    'career_path',
    profile_data,
    'user'
)

if success:
    display_career_path(result)
else:
    st.error(f"Error: {result['error']}")
```

---

## 8. Advanced Topics

### Multi-Engine Orchestration

```python
from shared_backend.services.portal_bridge import PortalBridge

def comprehensive_career_analysis(profile_data):
    """
    Get comprehensive career analysis using multiple intelligence types.
    """
    bridge = PortalBridge()
    
    results = {}
    
    # 1. Career path analysis
    results['career_path'] = bridge.get_career_intelligence(profile_data)
    
    # 2. Skill gap analysis
    results['skill_gaps'] = bridge.get_skill_gap_analysis(
        profile_data,
        target_role='Senior Engineer'
    )
    
    # 3. Salary analysis
    results['salary'] = bridge.get_salary_insights(profile_data)
    
    # 4. Job matches
    results['job_matches'] = bridge.get_job_matches(profile_data, {})
    
    # 5. Profile strength
    results['profile_strength'] = bridge.get_profile_strength_analysis(profile_data)
    
    return results

# Usage:
analysis = comprehensive_career_analysis(user_profile)

for intel_type, result in analysis.items():
    if result['status'] == 'success':
        print(f"✅ {intel_type}: Success")
    else:
        print(f"⏳ {intel_type}: {result['status']}")
```

### Custom Intelligence Pipelines

```python
def custom_career_pipeline(profile_data, preferences):
    """
    Custom pipeline combining multiple intelligence types with business logic.
    """
    bridge = PortalBridge()
    
    # Step 1: Get base career intelligence
    career_result = bridge.get_career_intelligence(profile_data)
    
    if career_result['status'] != 'success':
        return {'error': 'Career analysis failed'}
    
    # Step 2: Filter career paths by preferences
    career_paths = career_result['career_path']
    filtered_paths = [
        path for path in career_paths
        if matches_preferences(path, preferences)
    ]
    
    # Step 3: Get skills for each filtered path
    path_skills = {}
    for path in filtered_paths:
        skill_result = bridge.get_skill_recommendations(
            profile_data,
            target_role=path
        )
        if skill_result['status'] == 'success':
            path_skills[path] = skill_result['skills']
    
    # Step 4: Get salary projections
    salary_projections = {}
    for path in filtered_paths:
        salary_result = bridge.get_intelligence(
            intelligence_type='salary_projection',
            data={'target_role': path, 'location': profile_data['location']},
            portal_type='user'
        )
        if salary_result['status'] == 'success':
            salary_projections[path] = salary_result['projected_salary']
    
    # Step 5: Combine and rank
    ranked_paths = rank_career_paths(
        filtered_paths,
        path_skills,
        salary_projections,
        preferences
    )
    
    return {
        'status': 'success',
        'recommended_paths': ranked_paths,
        'total_paths_analyzed': len(career_paths),
        'paths_matching_preferences': len(filtered_paths)
    }
```

### Performance Optimization

**Caching Results:**
```python
from functools import lru_cache
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_cached_intelligence(intelligence_type, profile_id, portal_type):
    """
    Cache intelligence results to avoid redundant API calls.
    """
    bridge = PortalBridge()
    
    # Load profile
    profile_data = load_profile(profile_id)
    
    # Get intelligence
    result = bridge.get_intelligence(
        intelligence_type=intelligence_type,
        data=profile_data,
        portal_type=portal_type
    )
    
    return result

# Usage:
result = get_cached_intelligence('career_path', user_id, 'user')
```

**Batch Processing:**
```python
def batch_intelligence_requests(profiles, intelligence_type, portal_type='user'):
    """
    Process multiple profiles efficiently.
    """
    bridge = PortalBridge()
    results = []
    
    for profile in profiles:
        result = bridge.get_intelligence(
            intelligence_type=intelligence_type,
            data=profile,
            portal_type=portal_type
        )
        results.append({
            'profile_id': profile['id'],
            'result': result
        })
    
    return results

# Usage:
profiles = load_all_profiles()
results = batch_intelligence_requests(profiles, 'career_path', 'admin')
```

---

## 9. Best Practices

### Code Organization

**✅ DO:**
```python
# Good: Initialize once in session state
if 'portal_bridge' not in st.session_state:
    st.session_state.portal_bridge = PortalBridge()

bridge = st.session_state.portal_bridge
```

**❌ DON'T:**
```python
# Bad: Re-initialize every time
bridge = PortalBridge()  # Creates new instance each run
```

**✅ DO:**
```python
# Good: Use convenience methods for common tasks
result = bridge.get_career_intelligence(profile_data)
```

**❌ DON'T:**
```python
# Bad: Bypass Portal Bridge
from shared_backend.ai_engines.inference_engine import InferenceEngine
engine = InferenceEngine()  # Direct engine access
```

### Error Handling

**✅ DO:**
```python
# Good: Comprehensive error handling
try:
    result = bridge.get_intelligence('career_path', data, 'user')
    
    if result['status'] == 'success':
        process_success(result)
    elif result['status'] == 'not_implemented':
        show_coming_soon(result['schema'])
    else:
        show_error(result['error'])
        
except Exception as e:
    logger.exception("Intelligence error")
    show_error("Unexpected error occurred")
```

**❌ DON'T:**
```python
# Bad: No error handling
result = bridge.get_intelligence('career_path', data, 'user')
display(result['career_path'])  # Will crash if error
```

### Testing Strategies

**Unit Tests:**
```python
import pytest
from shared_backend.services.portal_bridge import PortalBridge

def test_career_intelligence():
    bridge = PortalBridge()
    
    profile_data = {
        'current_role': 'Software Engineer',
        'experience_years': 5
    }
    
    result = bridge.get_career_intelligence(profile_data)
    
    assert result['status'] == 'success'
    assert 'career_path' in result
    assert len(result['career_path']) > 0
```

**Integration Tests:**
```python
def test_full_career_pipeline():
    """Test complete career intelligence pipeline"""
    bridge = PortalBridge()
    
    # Get career intelligence
    career_result = bridge.get_career_intelligence(test_profile)
    assert career_result['status'] == 'success'
    
    # Get skills for next role
    next_role = career_result['next_roles'][0]
    skill_result = bridge.get_skill_recommendations(test_profile, next_role)
    assert skill_result['status'] == 'success'
    
    # Get salary projection
    salary_result = bridge.get_salary_insights(test_profile)
    assert salary_result['status'] == 'success'
```

### Performance Tips

**1. Use Caching:**
```python
@st.cache_data(ttl=3600)
def get_career_intel(profile_id):
    # Cached for 1 hour
    pass
```

**2. Batch Operations:**
```python
# Process multiple profiles at once
results = batch_intelligence_requests(profiles, 'career_path')
```

**3. Async Operations (Advanced):**
```python
import asyncio

async def async_intelligence_request(bridge, type, data):
    return bridge.get_intelligence(type, data, 'user')

# Run multiple requests concurrently
results = await asyncio.gather(
    async_intelligence_request(bridge, 'career_path', data1),
    async_intelligence_request(bridge, 'job_match', data2),
    async_intelligence_request(bridge, 'salary', data3)
)
```

---

## 10. Common Patterns

### Pattern 1: Career Dashboard

```python
def career_dashboard(profile_data):
    """Complete career dashboard with multiple intelligence types"""
    bridge = PortalBridge()
    
    st.header("Your Career Dashboard")
    
    # Row 1: Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        career_result = bridge.get_career_intelligence(profile_data)
        if career_result['status'] == 'success':
            st.metric(
                "Career Level",
                career_result.get('current_level', 'N/A')
            )
    
    with col2:
        profile_result = bridge.get_profile_strength_analysis(profile_data)
        if profile_result['status'] == 'success':
            st.metric(
                "Profile Strength",
                f"{profile_result.get('strength_score', 0)}%"
            )
    
    with col3:
        salary_result = bridge.get_salary_insights(profile_data)
        if salary_result['status'] == 'success':
            st.metric(
                "Market Value",
                f"${salary_result.get('market_value', 0):,}"
            )
    
    # Row 2: Detailed sections
    tab1, tab2, tab3 = st.tabs(["Career Path", "Skills", "Jobs"])
    
    with tab1:
        display_career_path(career_result)
    
    with tab2:
        skill_result = bridge.get_skill_gap_analysis(profile_data, target_role)
        display_skill_gaps(skill_result)
    
    with tab3:
        job_result = bridge.get_job_matches(profile_data, {})
        display_job_matches(job_result)
```

### Pattern 2: Real-Time Updates

```python
def real_time_intelligence_monitor():
    """Monitor intelligence requests in real-time"""
    bridge = PortalBridge()
    
    st.header("Real-Time Intelligence Monitor")
    
    # Create placeholder
    placeholder = st.empty()
    
    while True:
        # Get latest analytics
        analytics = bridge.get_system_analytics()
        
        with placeholder.container():
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Requests/min", analytics['requests_per_minute'])
            
            with col2:
                st.metric("Avg Response", f"{analytics['avg_response_time']:.2f}ms")
            
            with col3:
                st.metric("Success Rate", f"{analytics['success_rate']}%")
            
            # Recent requests
            st.subheader("Recent Requests")
            for req in analytics['recent_requests'][:10]:
                st.write(f"{req['timestamp']}: {req['type']} - {req['status']}")
        
        time.sleep(5)  # Update every 5 seconds
```

### Pattern 3: Comparison View

```python
def compare_candidates(candidate_ids):
    """Compare multiple candidates side-by-side"""
    bridge = PortalBridge()
    
    st.header("Candidate Comparison")
    
    # Create columns for each candidate
    cols = st.columns(len(candidate_ids))
    
    for i, candidate_id in enumerate(candidate_ids):
        with cols[i]:
            profile = load_profile(candidate_id)
            
            st.subheader(profile['name'])
            
            # Get intelligence for each
            career = bridge.get_career_intelligence(profile)
            skills = bridge.get_skill_gap_analysis(profile, target_role)
            salary = bridge.get_salary_insights(profile)
            
            # Display metrics
            if career['status'] == 'success':
                st.metric("Career Level", career['current_level'])
            
            if skills['status'] == 'success':
                st.metric("Skill Match", f"{skills['match_percentage']}%")
            
            if salary['status'] == 'success':
                st.metric("Salary", f"${salary['current_salary']:,}")
```

---

## 11. Troubleshooting

### Common Issues

**Issue: "Module not found"**
```
ModuleNotFoundError: No module named 'shared_backend'
```

**Solution:**
```bash
# Add to PYTHONPATH
$env:PYTHONPATH = "c:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION"
```

**Issue: "No types discovered"**
```
WARNING: Discovery complete: 0 types from 0 files
```

**Solution:**
- Check `ai_data_final/` directory exists
- Verify JSON files are valid
- Check discovery path in logs

**Issue: "Handler not found"**
```
{
    'status': 'not_implemented',
    'intelligence_type': 'career_path'
}
```

**Solution:**
- Verify handler is registered in `_register_intelligence_handlers()`
- Check handler name matches discovered type
- Restart application

**Issue: "Slow performance"**

**Solutions:**
- Implement caching with `@st.cache_data`
- Use batch processing for multiple requests
- Check JSON file sizes (large files slow discovery)
- Profile code to find bottlenecks

---

## 📝 Summary

**Key Takeaways:**

1. **Portal Bridge is your main interface** - Always use it instead of direct engine access
2. **Adding new types is easy** - Just add JSON files, no code changes
3. **Stubs are helpful** - Unimplemented types return schema and examples
4. **Handlers are optional** - Implement when you need complex logic
5. **Error handling is critical** - Always handle all status types
6. **Testing is essential** - Write tests for handlers and integrations
7. **Performance matters** - Use caching and batch operations

**Next Steps:**

- ✅ Read API_REFERENCE.md for complete API documentation
- ✅ Read PORTAL_MIGRATION_GUIDE.md for migration examples
- ✅ Review ARCHITECTURE.md for system design details
- ✅ Check TROUBLESHOOTING.md for more solutions

---

**Document Version:** 1.0  
**Last Updated:** October 21, 2025  
**Status:** ✅ Production Ready

**Need Help?**
- Check logs: `logs/ai_system.log`
- Review test examples in `tests/`
- Contact: [support email]
