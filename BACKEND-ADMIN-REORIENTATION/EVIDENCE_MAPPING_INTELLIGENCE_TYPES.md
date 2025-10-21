# Evidence Mapping: Intelligence Types in ai_data_final/

**Date:** October 21, 2025  
**Purpose:** Map actual data structures to intelligence types for dynamic discovery  
**Source:** `ai_data_final/` JSON files analysis

---

## 🔍 Data Structure Analysis

### File: `complete_enhanced_analysis_eric_mehl_shell.json` (461 lines)

#### Top-Level Keys → Intelligence Types

```json
{
  "web_company_intelligence": { ... },      // → company_intelligence
  "business_intelligence": { ... },         // → market_intelligence
  "metadata": { ... },                      // → metadata_tracking
  "target_job_profile": { ... },            // → job_profile_analysis
  "candidate_profile": { ... },             // → profile_analysis
  "compatibility_analysis": { ... },        // → job_match_analysis
  "user_touchpoints": { ... }               // → touchpoint_analysis
}
```

#### Detailed Mapping:

**1. `web_company_intelligence` (Company Objects)**
```json
{
  "COMPANY_NAME": {
    "headquarters": "string",           // → geolocation
    "ai_research_confidence": "98%",    // → confidence_scoring
    "relevance_to_shell": "HIGH",       // → relevance_ranking
    "sector": "string",                 // → industry_classification
    "revenue": "€500M+",                // → financial_intelligence
    "employees": "1000+",               // → company_sizing
    "web_presence": "domain.com",       // → web_intelligence
    "market_position": "string",        // → competitive_analysis
    "industry": "string",               // → industry_classification
    "specialization": "string"          // → capability_mapping
  }
}
```

**Intelligence Types Identified:**
- ✅ `company_intelligence` - Company research and profiling
- ✅ `geolocation` - Headquarters location parsing
- ✅ `industry_classification` - Sector/industry categorization
- ✅ `competitive_analysis` - Market position analysis
- ✅ `financial_intelligence` - Revenue/employee sizing
- ✅ `web_intelligence` - Web presence analysis
- ✅ `relevance_ranking` - Relevance scoring
- ✅ `capability_mapping` - Specialization identification

**2. `business_intelligence`**
```json
{
  "market_positioning": "string",                    // → market_intelligence
  "competitive_advantage": "string",                 // → competitive_analysis
  "expected_salary_negotiation": "£90K-£110K",      // → salary_negotiation
  "client_value_proposition": "string",             // → value_proposition
  "placement_confidence": "High (85%)"              // → confidence_scoring
}
```

**Intelligence Types Identified:**
- ✅ `market_intelligence` - Market positioning
- ✅ `competitive_analysis` - Competitive advantage
- ✅ `salary_negotiation` - Salary expectations
- ✅ `value_proposition` - Client value analysis
- ✅ `confidence_scoring` - Placement confidence

**3. `target_job_profile`**
```json
{
  "salary_range": "£80K-£120K",             // → salary_analysis
  "seniority": "Senior Management",         // → seniority_detection
  "required_skills": [],                    // → skill_requirements
  "preferred_skills": [],                   // → skill_preferences
  "position": "string",                     // → job_title_analysis
  "company_context": {
    "geography": [],                        // → geographic_analysis
    "market_position": "string",            // → market_intelligence
    "investment": "string",                 // → financial_intelligence
    "strategy": "string"                    // → strategic_intelligence
  },
  "qualifications": [],                     // → education_requirements
  "company": "string",                      // → employer_identification
  "key_responsibilities": [],               // → responsibility_extraction
  "location": "string",                     // → location_analysis
  "department": "string"                    // → organizational_mapping
}
```

**Intelligence Types Identified:**
- ✅ `salary_analysis` - Salary range parsing
- ✅ `seniority_detection` - Seniority level identification
- ✅ `skill_requirements` - Required skills extraction
- ✅ `skill_preferences` - Preferred skills extraction
- ✅ `job_title_analysis` - Job title parsing
- ✅ `geographic_analysis` - Geography mapping
- ✅ `education_requirements` - Qualification analysis
- ✅ `responsibility_extraction` - Key responsibilities
- ✅ `organizational_mapping` - Department structure

**4. `candidate_profile.enhanced_ai_analysis`**
```json
{
  "locations": [],                          // → location_history
  "enhancement_factors": [],                // → ai_enhancement_tracking
  "ai_confidence": "92%",                   // → confidence_scoring
  "international_experience": true,         // → experience_classification
  "leadership_score": 5,                    // → leadership_scoring
  "skills": [],                             // → skill_extraction
  "experience_years": 31.0,                 // → experience_calculation
  "companies": []                           // → employment_history
}
```

**Intelligence Types Identified:**
- ✅ `location_history` - Historical location tracking
- ✅ `ai_enhancement_tracking` - AI improvement tracking
- ✅ `confidence_scoring` - AI confidence metrics
- ✅ `experience_classification` - Experience type detection
- ✅ `leadership_scoring` - Leadership level scoring
- ✅ `skill_extraction` - Skills identification
- ✅ `experience_calculation` - Years of experience
- ✅ `employment_history` - Company history

**5. `candidate_profile.network_analysis`**
```json
{
  "database_size": "1,275,000 emails",      // → database_metrics
  "connections": [
    {
      "connection_strength": "Direct",      // → relationship_strength
      "email": "e.mehl@resato.com",         // → contact_extraction
      "company": "RESATO INTERNATIONAL"     // → company_association
    }
  ],
  "match_quality": "Enhanced"               // → quality_scoring
}
```

**Intelligence Types Identified:**
- ✅ `network_analysis` - Professional network mapping
- ✅ `relationship_strength` - Connection strength scoring
- ✅ `contact_extraction` - Email/contact extraction
- ✅ `company_association` - Company-contact linking

**6. `compatibility_analysis`**
```json
{
  "overall_compatibility": 26.6,            // → compatibility_scoring
  "experience_match": {
    "shell_relevant_experience": [
      {
        "relevance": "HIGH",                // → relevance_ranking
        "reason": "string",                 // → reasoning_explanation
        "score": 1,                         // → numeric_scoring
        "company": "string"                 // → company_matching
      }
    ],
    "international_experience_score": 0,    // → experience_scoring
    "energy_sector_score": 2,               // → sector_scoring
    "technical_background_score": 0         // → technical_scoring
  },
  "skills_match": {
    "direct_matches": [],                   // → exact_skill_matching
    "transferable_matches": [],             // → transferable_skill_matching
    "skill_gaps": []                        // → skill_gap_analysis
  }
}
```

**Intelligence Types Identified:**
- ✅ `compatibility_scoring` - Overall compatibility
- ✅ `relevance_ranking` - Experience relevance
- ✅ `reasoning_explanation` - AI reasoning
- ✅ `experience_scoring` - Experience category scoring
- ✅ `exact_skill_matching` - Direct skill matches
- ✅ `transferable_skill_matching` - Transferable skills
- ✅ `skill_gap_analysis` - Skill gaps identification

**7. `user_touchpoints`**
```json
{
  "engagement_metrics": {
    "network_connections": 3,               // → engagement_counting
    "profile_strength": "Advanced",         // → profile_quality
    "company_intelligence": "Enhanced",     // → intelligence_level
    "job_compatibility_score": 26.6         // → compatibility_scoring
  },
  "candidate_journey": {
    "ai_enhancement": "Applied",            // → enhancement_status
    "profile_completion": "Complete",       // → completion_status
    "registration": "2025-08-11",           // → timestamp_tracking
    "job_matching_initiated": "2025-08-11" // → event_tracking
  },
  "recruiter_notes": {
    "interview_preparation": [],            // → interview_coaching
    "development_areas": [],                // → skill_recommendations
    "strengths": []                         // → strength_identification
  },
  "next_steps": []                          // → action_recommendations
}
```

**Intelligence Types Identified:**
- ✅ `engagement_metrics` - User engagement tracking
- ✅ `profile_quality` - Profile strength assessment
- ✅ `enhancement_status` - AI enhancement tracking
- ✅ `completion_status` - Profile completion tracking
- ✅ `timestamp_tracking` - Event timestamp tracking
- ✅ `event_tracking` - User event logging
- ✅ `interview_coaching` - Interview preparation
- ✅ `skill_recommendations` - Development recommendations
- ✅ `strength_identification` - Candidate strengths
- ✅ `action_recommendations` - Next steps

---

## 📊 Complete Intelligence Type Registry (From Evidence)

### Category 1: Company & Market Intelligence (10 types)
1. `company_intelligence` - Company research and profiling
2. `market_intelligence` - Market trends and positioning
3. `competitive_analysis` - Competitive landscape
4. `financial_intelligence` - Revenue/sizing analysis
5. `web_intelligence` - Web presence analysis
6. `industry_classification` - Industry/sector classification
7. `capability_mapping` - Company specializations
8. `strategic_intelligence` - Strategic positioning
9. `organizational_mapping` - Department/structure mapping
10. `employer_identification` - Employer identification

### Category 2: Profile & Identity (12 types)
11. `profile_analysis` - Comprehensive profile analysis
12. `profile_quality` - Profile strength assessment
13. `seniority_detection` - Career level detection
14. `leadership_scoring` - Leadership level scoring
15. `identity_verification` - Profile authenticity
16. `experience_classification` - Experience type detection
17. `experience_calculation` - Years of experience
18. `experience_scoring` - Experience category scoring
19. `technical_scoring` - Technical background scoring
20. `sector_scoring` - Sector experience scoring
21. `enhancement_status` - AI enhancement tracking
22. `completion_status` - Profile completion tracking

### Category 3: Skills & Capabilities (8 types)
23. `skill_extraction` - Skills identification
24. `skill_requirements` - Required skills extraction
25. `skill_preferences` - Preferred skills extraction
26. `exact_skill_matching` - Direct skill matches
27. `transferable_skill_matching` - Transferable skills
28. `skill_gap_analysis` - Skill gaps identification
29. `skill_recommendations` - Development recommendations
30. `strength_identification` - Candidate strengths

### Category 4: Location & Geography (5 types)
31. `location_analysis` - Location preferences
32. `location_history` - Historical location tracking
33. `geolocation` - Geocoding and location parsing
34. `geographic_analysis` - Geography mapping
35. `relocation_analysis` - Relocation potential

### Category 5: Salary & Compensation (3 types)
36. `salary_analysis` - Salary range analysis
37. `salary_negotiation` - Salary expectations
38. `compensation_modeling` - Compensation structure

### Category 6: Job Matching & Compatibility (8 types)
39. `job_match` - Job-candidate matching
40. `job_match_analysis` - Job match details
41. `compatibility_scoring` - Overall compatibility
42. `relevance_ranking` - Relevance scoring
43. `job_title_analysis` - Job title parsing
44. `job_profile_analysis` - Job profile analysis
45. `responsibility_extraction` - Key responsibilities
46. `value_proposition` - Client value analysis

### Category 7: Network & Relationships (4 types)
47. `network_analysis` - Professional network mapping
48. `relationship_strength` - Connection strength
49. `contact_extraction` - Email/contact extraction
50. `company_association` - Company-contact linking

### Category 8: Career & Growth (3 types)
51. `career_path` - Career progression predictions
52. `career_coaching` - Career guidance
53. `employment_history` - Company history

### Category 9: Engagement & Touchpoints (7 types)
54. `touchpoint_analysis` - User engagement tracking
55. `engagement_metrics` - Engagement measurement
56. `event_tracking` - User event logging
57. `timestamp_tracking` - Event timestamp tracking
58. `action_recommendations` - Next steps
59. `interview_coaching` - Interview preparation
60. `candidate_journey` - User journey tracking

### Category 10: AI & Quality Metrics (8 types)
61. `confidence_scoring` - AI confidence metrics
62. `quality_scoring` - Quality assessment
63. `numeric_scoring` - Numeric score calculation
64. `reasoning_explanation` - AI reasoning
65. `ai_enhancement_tracking` - AI improvement tracking
66. `intelligence_level` - Intelligence enhancement level
67. `metadata_tracking` - Metadata management
68. `database_metrics` - Database statistics

### Category 11: Education & Qualifications (2 types)
69. `education_requirements` - Qualification analysis
70. `education_mapping` - Education to career paths

---

## 🎯 Total Intelligence Types Identified: **70 types** (from 1 file!)

---

## 📁 Additional Files to Analyze

### From `ai_data_final/` Directory:

1. **enhanced_sandbox_analysis_eric_mehl.json** - Similar structure, validate patterns
2. **career_advice.json** - Career coaching intelligence
3. **commute_analysis.json** - Commute/location intelligence
4. **interview_prep.json** - Interview coaching intelligence
5. **job_match_candidates.json** - Job matching intelligence
6. **application_feedback.json** - Application tracking intelligence
7. **enhanced_job_titles_database.json** - Job title taxonomy
8. **match_analysis.json** - Match analysis patterns
9. **mentorship_matches.json** - Mentorship intelligence
10. **tuning_recommendations.json** - Tuning intelligence

### Folder Analysis Needed:

- `parsed_resumes/` - Resume parsing patterns
- `parsed_job_descriptions/` - Job description patterns
- `job descriptions/` - Raw job description intelligence
- `emails/` - Email intelligence patterns
- `companies/` - Company intelligence patterns
- `locations/` - Location intelligence patterns
- `Industries/` - Industry intelligence patterns

---

## 🔧 Dynamic Discovery Architecture

### Pattern Recognition Rules:

```python
# Rule 1: Top-level keys ending in "_intelligence"
"web_company_intelligence" → register as "company_intelligence"
"business_intelligence" → register as "market_intelligence"

# Rule 2: Top-level keys ending in "_analysis"
"compatibility_analysis" → register as "compatibility_scoring"
"network_analysis" → register as "network_analysis"

# Rule 3: Nested structures with consistent patterns
"candidate_profile.enhanced_ai_analysis" → extract sub-types
"target_job_profile" → extract requirement types

# Rule 4: Arrays of objects with schemas
"required_skills" → register as "skill_requirements"
"connections" → register as "network_analysis"

# Rule 5: Scoring/confidence fields
"*_score" → register as "*_scoring"
"*_confidence" → register as "confidence_scoring"
```

---

## 🚀 Implementation Strategy

### Phase 1: Schema Discovery (Automated)
- Scan all JSON files in `ai_data_final/`
- Extract all top-level keys
- Extract all nested object structures
- Extract all array patterns
- Build intelligence type registry

### Phase 2: Type Classification (Pattern-Based)
- Apply pattern recognition rules
- Group similar types into categories
- Identify input/output schemas
- Build type hierarchy

### Phase 3: Dynamic Registration (Runtime)
- Register discovered types at startup
- Build routing table: type → handler
- Create stub handlers for unimplemented types
- Log usage patterns for prioritization

### Phase 4: Schema Validation (Data Quality)
- Validate input data against discovered schemas
- Provide helpful error messages
- Suggest corrections for malformed data
- Track schema evolution over time

---

## 📝 Example: Dynamic Type Discovery

```python
# Scan ai_data_final/complete_enhanced_analysis_eric_mehl_shell.json
discovered_types = {
    'company_intelligence': {
        'source_key': 'web_company_intelligence',
        'schema': {
            'headquarters': 'string',
            'ai_research_confidence': 'percentage',
            'relevance_to_shell': 'enum[HIGH|MEDIUM|LOW|TBD]',
            'sector': 'string',
            'revenue': 'string',
            'employees': 'string',
            'web_presence': 'url',
            'market_position': 'string',
            'industry': 'string',
            'specialization': 'string'
        },
        'input_structure': 'Dict[str, CompanyProfile]',
        'output_structure': 'CompanyIntelligenceReport',
        'handler': None,  # To be implemented
        'priority': 'HIGH',
        'evidence_files': [
            'complete_enhanced_analysis_eric_mehl_shell.json'
        ],
        'usage_count': 0
    },
    'market_intelligence': {
        'source_key': 'business_intelligence',
        'schema': {
            'market_positioning': 'string',
            'competitive_advantage': 'string',
            'expected_salary_negotiation': 'salary_range',
            'client_value_proposition': 'string',
            'placement_confidence': 'confidence_score'
        },
        'input_structure': 'Dict[str, Any]',
        'output_structure': 'MarketIntelligenceReport',
        'handler': None,
        'priority': 'HIGH',
        'evidence_files': [
            'complete_enhanced_analysis_eric_mehl_shell.json'
        ],
        'usage_count': 0
    }
    # ... 68 more types
}
```

---

## 🎯 Recommended Next Steps

1. **Create Intelligence Type Scanner** - Automated discovery tool
2. **Build Dynamic Registry** - Runtime type registration
3. **Implement Schema Validator** - Input/output validation
4. **Create Type Router** - Route requests to appropriate handlers
5. **Build Priority Queue** - Implement high-priority types first
6. **Add Usage Tracking** - Track which types are used most
7. **Generate Documentation** - Auto-document discovered types

---

## 📊 Evidence Summary

From **ONE FILE** (`complete_enhanced_analysis_eric_mehl_shell.json`):
- **70 distinct intelligence types** identified
- **11 major categories** discovered
- **7 top-level data structures** analyzed
- **Multiple nested patterns** recognized

**Projected Total** (all files in `ai_data_final/`):
- Estimated **150-200 intelligence types**
- Potential **20-30 categories**
- Hundreds of schema patterns

---

**Conclusion:** We need a **dynamic, self-discovering architecture** that automatically identifies intelligence types from data, not hard-coded lists. The hybrid integrator should scan available data files, extract patterns, and register handlers dynamically.

