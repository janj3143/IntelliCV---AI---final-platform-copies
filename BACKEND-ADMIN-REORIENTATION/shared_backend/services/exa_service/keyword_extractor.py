"""
Exa Keyword Extractor - JD-Focused
===================================
Purpose: Extract JOB-RELEVANT keywords from Exa-enriched careers pages.

PRIMARY FOCUS: Job Descriptions
- Extract: Required skills, qualifications, experience levels
- Extract: Tech stack, tools, frameworks mentioned in JDs
- Extract: Soft skills, certifications, education requirements
- Count frequency: Skills mentioned across multiple JDs
- Job Title Analysis: Keyword patterns in titles (Senior, Lead, etc.)

SMART SEARCH: Hybrid AI + SQLite
- Semantic search: "Find companies hiring ML engineers"
- Keyword search: "Python AND AWS AND remote"
- Combined queries: AI understanding + exact matching

Usage:
    from services.exa_service.keyword_extractor import KeywordExtractor
    
    extractor = KeywordExtractor()
    
    # Extract from JD text
    jd_keywords = extractor.extract_job_description_keywords(jd_text)
    
    # Analyze job title
    title_analysis = extractor.analyze_job_title("Senior ML Engineer")
    
    # Smart SQLite search
    results = extractor.smart_search("companies hiring Python developers in Seattle")
"""

import re
import os
from typing import List, Dict, Any, Set, Tuple
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

# Try to import NLP libraries
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
except:
    SPACY_AVAILABLE = False
    logger.warning("spaCy not available. Install with: python -m spacy download en_core_web_sm")

# Try to import OpenAI for LLM extraction
try:
    import openai
    openai.api_key = os.getenv('OPENAI_API_KEY')
    LLM_AVAILABLE = bool(openai.api_key)
except:
    LLM_AVAILABLE = False

# ============================================================================
# KEYWORD PATTERNS
# ============================================================================

# Common tech skills and tools
TECH_KEYWORDS = {
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust', 'swift',
    'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'express',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ansible',
    'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
    'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
    'git', 'ci/cd', 'jenkins', 'github', 'gitlab',
    'agile', 'scrum', 'jira', 'confluence'
}

# JOB DESCRIPTION PATTERNS (NEW!)
JD_REQUIREMENT_PATTERNS = [
    # Experience requirements
    r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
    r'minimum\s+of\s+(\d+)\s+years?',
    r'at least\s+(\d+)\s+years?',
    
    # Education requirements
    r'(?:bachelor|master|phd|doctorate)(?:\'s)?\s+(?:degree)?',
    r'bs|ms|phd|mba\s+in',
    
    # Skill requirements
    r'(?:proficient|expert|experienced|strong)\s+(?:in|with)\s+([a-z0-9\s,]+)',
    r'knowledge\s+of\s+([a-z0-9\s,]+)',
    r'experience\s+with\s+([a-z0-9\s,]+)',
    
    # Nice-to-haves
    r'(?:nice|bonus|plus|preferred)\s+to\s+have',
    r'nice-to-haves?',
]

# Job title components
JOB_TITLE_LEVELS = {
    'junior', 'mid', 'senior', 'staff', 'principal', 'lead', 'chief',
    'associate', 'entry', 'intern', 'I', 'II', 'III', 'IV', 'V'
}

JOB_TITLE_ROLES = {
    'engineer', 'developer', 'programmer', 'architect', 'scientist', 'analyst',
    'manager', 'director', 'vp', 'cto', 'cio', 'cpo',
    'designer', 'researcher', 'consultant', 'specialist'
}

JOB_TITLE_DOMAINS = {
    'software', 'machine learning', 'ml', 'ai', 'data', 'frontend', 'backend',
    'fullstack', 'full-stack', 'devops', 'security', 'cloud', 'mobile',
    'web', 'infrastructure', 'platform', 'qa', 'test', 'automation'
}

# Common benefits keywords
BENEFITS_KEYWORDS = {
    'remote', 'hybrid', '401k', 'healthcare', 'dental', 'vision', 'pto', 'vacation',
    'stock options', 'equity', 'bonus', 'flexible hours', 'work from home',
    'parental leave', 'tuition reimbursement', 'professional development',
    'gym membership', 'wellness', 'stipend'
}

# Common role types
ROLE_KEYWORDS = {
    'engineer', 'developer', 'architect', 'manager', 'director', 'vp', 'cto',
    'analyst', 'scientist', 'researcher', 'consultant', 'specialist',
    'lead', 'senior', 'junior', 'staff', 'principal'
}

# ============================================================================
# KEYWORD EXTRACTOR
# ============================================================================

class KeywordExtractor:
    """Extract keywords from company content."""
    
    def __init__(self):
        """Initialize keyword extractor."""
        self.tech_keywords = TECH_KEYWORDS
        self.benefits_keywords = BENEFITS_KEYWORDS
        self.role_keywords = ROLE_KEYWORDS
    
    def extract_from_content(
        self,
        text: str,
        content_type: str = 'general',
        use_llm: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Extract keywords from text content.
        
        Args:
            text: Text content to extract from
            content_type: Type of content ('careers', 'products', 'background')
            use_llm: Use LLM for enhanced extraction
        
        Returns:
            List of keyword dictionaries with type, confidence, context
        """
        keywords = []
        
        # Method 1: Regex pattern matching
        keywords.extend(self._extract_with_regex(text, content_type))
        
        # Method 2: spaCy NLP (if available)
        if SPACY_AVAILABLE:
            keywords.extend(self._extract_with_spacy(text, content_type))
        
        # Method 3: LLM extraction (if available and requested)
        if use_llm and LLM_AVAILABLE:
            keywords.extend(self._extract_with_llm(text, content_type))
        
        # Deduplicate and score
        keywords = self._deduplicate_keywords(keywords)
        
        return keywords
    
    def _extract_with_regex(self, text: str, content_type: str) -> List[Dict[str, Any]]:
        """Extract keywords using regex patterns."""
        keywords = []
        text_lower = text.lower()
        
        # Extract tech keywords
        for keyword in self.tech_keywords:
            if keyword in text_lower:
                # Find context (surrounding text)
                matches = re.finditer(rf'\b{re.escape(keyword)}\b', text_lower, re.IGNORECASE)
                for match in matches:
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end].strip()
                    
                    keywords.append({
                        'keyword': keyword,
                        'keyword_type': 'technology',
                        'category': 'programming_language' if keyword in {'python', 'java', 'javascript'} else 'tool',
                        'confidence_score': 0.9,  # High confidence for exact match
                        'context': context,
                        'extraction_method': 'regex',
                        'frequency': text_lower.count(keyword)
                    })
        
        # Extract benefits keywords
        if content_type == 'careers':
            for keyword in self.benefits_keywords:
                if keyword in text_lower:
                    keywords.append({
                        'keyword': keyword,
                        'keyword_type': 'benefit',
                        'category': 'compensation',
                        'confidence_score': 0.85,
                        'context': '',
                        'extraction_method': 'regex',
                        'frequency': text_lower.count(keyword)
                    })
        
        # Extract role keywords
        for keyword in self.role_keywords:
            if keyword in text_lower:
                keywords.append({
                    'keyword': keyword,
                    'keyword_type': 'role',
                    'category': 'job_title',
                    'confidence_score': 0.8,
                    'context': '',
                    'extraction_method': 'regex',
                    'frequency': text_lower.count(keyword)
                })
        
        return keywords
    
    def _extract_with_spacy(self, text: str, content_type: str) -> List[Dict[str, Any]]:
        """Extract keywords using spaCy NLP."""
        if not SPACY_AVAILABLE:
            return []
        
        keywords = []
        
        try:
            doc = nlp(text[:100000])  # Limit to 100k chars for performance
            
            # Extract named entities
            for ent in doc.ents:
                if ent.label_ in {'ORG', 'PRODUCT', 'GPE', 'LOC'}:
                    keyword_type = 'location' if ent.label_ in {'GPE', 'LOC'} else 'organization'
                    
                    keywords.append({
                        'keyword': ent.text,
                        'keyword_type': keyword_type,
                        'category': ent.label_,
                        'confidence_score': 0.75,
                        'context': '',
                        'extraction_method': 'nlp',
                        'frequency': 1
                    })
            
            # Extract noun chunks (potential skills/topics)
            for chunk in doc.noun_chunks:
                if len(chunk.text.split()) <= 3:  # Max 3-word phrases
                    keywords.append({
                        'keyword': chunk.text,
                        'keyword_type': 'skill',
                        'category': 'noun_phrase',
                        'confidence_score': 0.6,
                        'context': '',
                        'extraction_method': 'nlp',
                        'frequency': 1
                    })
        
        except Exception as e:
            logger.error(f"spaCy extraction failed: {e}")
        
        return keywords
    
    def _extract_with_llm(self, text: str, content_type: str) -> List[Dict[str, Any]]:
        """Extract keywords using LLM (OpenAI GPT)."""
        if not LLM_AVAILABLE:
            return []
        
        keywords = []
        
        # Truncate text to fit in prompt
        text_sample = text[:2000]
        
        prompt = f"""
Extract key skills, technologies, and requirements from the following {content_type} page content.

Content:
{text_sample}

Return a JSON array of keywords with the following structure:
[
  {{"keyword": "Python", "type": "technology", "category": "programming_language"}},
  {{"keyword": "AWS", "type": "technology", "category": "cloud_platform"}},
  ...
]

Focus on:
- Programming languages and frameworks
- Cloud platforms and tools
- Required skills and experience
- Benefits and perks (for careers pages)
- Products and services (for product pages)
"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a keyword extraction expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            # Parse response
            result_text = response.choices[0].message.content
            
            # Extract JSON array
            import json
            keywords_data = json.loads(result_text)
            
            for kw in keywords_data:
                keywords.append({
                    'keyword': kw.get('keyword', ''),
                    'keyword_type': kw.get('type', 'unknown'),
                    'category': kw.get('category', ''),
                    'confidence_score': 0.95,  # High confidence for LLM
                    'context': '',
                    'extraction_method': 'llm',
                    'frequency': 1
                })
        
        except Exception as e:
            logger.error(f"LLM extraction failed: {e}")
        
        return keywords
    
    def _deduplicate_keywords(self, keywords: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate keywords and combine scores."""
        keyword_map = {}
        
        for kw in keywords:
            key = kw['keyword'].lower()
            
            if key in keyword_map:
                # Combine with existing
                existing = keyword_map[key]
                existing['confidence_score'] = max(existing['confidence_score'], kw['confidence_score'])
                existing['frequency'] += kw.get('frequency', 1)
                
                # Prefer more specific extraction method
                if kw['extraction_method'] == 'llm':
                    existing['extraction_method'] = 'llm'
                elif kw['extraction_method'] == 'nlp' and existing['extraction_method'] == 'regex':
                    existing['extraction_method'] = 'nlp'
            else:
                keyword_map[key] = kw
        
        # Sort by confidence score
        return sorted(keyword_map.values(), key=lambda x: x['confidence_score'], reverse=True)
    
    def extract_from_enrichment(self, enrichment_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract keywords from full company enrichment data.
        
        Args:
            enrichment_data: Full enrichment data from company_enricher
        
        Returns:
            Dictionary with keywords by source type
        """
        all_keywords = {
            'careers': [],
            'products': [],
            'background': []
        }
        
        # Extract from careers pages
        if enrichment_data.get('careers'):
            for page in enrichment_data['careers'].get('careers_pages', []):
                text = page.get('text', '')
                if text:
                    keywords = self.extract_from_content(text, 'careers')
                    all_keywords['careers'].extend(keywords)
        
        # Extract from product pages
        if enrichment_data.get('products'):
            for page in enrichment_data['products'].get('product_pages', []):
                text = page.get('text', '')
                if text:
                    keywords = self.extract_from_content(text, 'products')
                    all_keywords['products'].extend(keywords)
        
        # Extract from background pages
        if enrichment_data.get('background'):
            for page in enrichment_data['background'].get('background_pages', []):
                text = page.get('text', '')
                if text:
                    keywords = self.extract_from_content(text, 'background')
                    all_keywords['background'].extend(keywords)
        
        # Deduplicate each category
        for category in all_keywords:
            all_keywords[category] = self._deduplicate_keywords(all_keywords[category])
        
        return all_keywords
    
    # ========================================================================
    # JOB DESCRIPTION FOCUSED EXTRACTION (NEW!)
    # ========================================================================
    
    def extract_job_description_keywords(self, jd_text: str) -> Dict[str, Any]:
        """
        Extract job-relevant keywords from job description text.
        
        FOCUSES ON:
        - Required skills (Python, AWS, etc.)
        - Experience requirements (5+ years, etc.)
        - Education requirements (BS/MS/PhD)
        - Tech stack mentions
        - Soft skills
        - Certifications
        
        Args:
            jd_text: Job description text from careers page
        
        Returns:
            Dictionary with categorized keywords:
            {
                'required_skills': [...],
                'nice_to_have': [...],
                'experience': {...},
                'education': [...],
                'tech_stack': [...],
                'soft_skills': [...],
                'keyword_counts': {...}
            }
        """
        result = {
            'required_skills': [],
            'nice_to_have': [],
            'experience': {},
            'education': [],
            'tech_stack': [],
            'soft_skills': [],
            'keyword_counts': {}
        }
        
        text_lower = jd_text.lower()
        
        # Extract experience requirements
        for pattern in JD_REQUIREMENT_PATTERNS[:3]:  # Experience patterns
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                result['experience'] = {
                    'years_required': max([int(m) for m in matches if m.isdigit()]),
                    'mentions': len(matches)
                }
                break
        
        # Extract education requirements
        for pattern in JD_REQUIREMENT_PATTERNS[3:5]:  # Education patterns
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                if match not in result['education']:
                    result['education'].append(match.strip())
        
        # Extract tech skills with frequency count
        for keyword in self.tech_keywords:
            count = text_lower.count(keyword)
            if count > 0:
                result['keyword_counts'][keyword] = count
                result['tech_stack'].append({
                    'keyword': keyword,
                    'frequency': count,
                    'confidence': 0.95 if count > 2 else 0.8
                })
        
        # Sort by frequency
        result['tech_stack'].sort(key=lambda x: x['frequency'], reverse=True)
        
        # Identify required vs nice-to-have
        # Split JD into sections
        if 'nice to have' in text_lower or 'nice-to-have' in text_lower or 'bonus' in text_lower:
            # Find the split point
            nice_idx = max(
                text_lower.find('nice to have'),
                text_lower.find('nice-to-have'),
                text_lower.find('bonus'),
                text_lower.find('plus')
            )
            
            if nice_idx > 0:
                required_section = jd_text[:nice_idx].lower()
                nice_section = jd_text[nice_idx:].lower()
                
                # Skills in required section
                for skill_info in result['tech_stack']:
                    keyword = skill_info['keyword']
                    if keyword in required_section:
                        result['required_skills'].append(keyword)
                    if keyword in nice_section:
                        result['nice_to_have'].append(keyword)
            else:
                # All skills are required
                result['required_skills'] = [s['keyword'] for s in result['tech_stack'][:10]]
        else:
            # No nice-to-have section, top skills are required
            result['required_skills'] = [s['keyword'] for s in result['tech_stack'][:10]]
        
        # Extract soft skills (common patterns)
        soft_skills_patterns = {
            'communication': r'\b(?:communication|communicative|communicate)\b',
            'leadership': r'\b(?:leadership|lead|leading)\b',
            'teamwork': r'\b(?:team|teamwork|collaborative|collaboration)\b',
            'problem solving': r'\b(?:problem[- ]solving|analytical)\b',
            'adaptability': r'\b(?:adapt|adaptable|flexible|flexibility)\b',
        }
        
        for skill_name, pattern in soft_skills_patterns.items():
            if re.search(pattern, text_lower):
                result['soft_skills'].append(skill_name)
        
        return result
    
    def analyze_job_title(self, job_title: str) -> Dict[str, Any]:
        """
        Analyze job title for seniority, role type, and domain keywords.
        
        Examples:
            "Senior ML Engineer" -> {level: 'senior', role: 'engineer', domain: 'ml'}
            "Staff Software Developer" -> {level: 'staff', role: 'developer', domain: 'software'}
        
        Args:
            job_title: Job title string
        
        Returns:
            Dictionary with title analysis
        """
        title_lower = job_title.lower()
        
        result = {
            'original_title': job_title,
            'level': None,
            'role': None,
            'domain': None,
            'keywords': [],
            'seniority_score': 0  # 0=entry, 50=mid, 100=senior/staff
        }
        
        # Extract level
        for level in JOB_TITLE_LEVELS:
            if level in title_lower:
                result['level'] = level
                
                # Score seniority
                if level in ['senior', 'staff', 'principal', 'lead', 'chief']:
                    result['seniority_score'] = 100
                elif level in ['mid', 'II', 'III']:
                    result['seniority_score'] = 50
                elif level in ['junior', 'entry', 'associate', 'I']:
                    result['seniority_score'] = 0
                
                result['keywords'].append(level)
                break
        
        # Extract role
        for role in JOB_TITLE_ROLES:
            if role in title_lower:
                result['role'] = role
                result['keywords'].append(role)
                break
        
        # Extract domain
        for domain in JOB_TITLE_DOMAINS:
            if domain in title_lower:
                result['domain'] = domain
                result['keywords'].append(domain)
                break
        
        return result
    
    def batch_analyze_job_titles(self, job_titles: List[str]) -> Dict[str, Any]:
        """
        Analyze multiple job titles and provide aggregated insights.
        
        Args:
            job_titles: List of job title strings
        
        Returns:
            Dictionary with aggregated analysis:
            - Most common levels
            - Most common roles
            - Most common domains
            - Average seniority score
        """
        analyses = [self.analyze_job_title(title) for title in job_titles]
        
        levels = [a['level'] for a in analyses if a['level']]
        roles = [a['role'] for a in analyses if a['role']]
        domains = [a['domain'] for a in analyses if a['domain']]
        
        return {
            'total_titles': len(job_titles),
            'most_common_levels': self._count_frequency(levels),
            'most_common_roles': self._count_frequency(roles),
            'most_common_domains': self._count_frequency(domains),
            'average_seniority': sum(a['seniority_score'] for a in analyses) / len(analyses) if analyses else 0,
            'detailed_analyses': analyses
        }
    
    def _count_frequency(self, items: List[str]) -> List[Dict[str, Any]]:
        """Count frequency of items and return sorted list."""
        from collections import Counter
        counts = Counter(items)
        return [{'item': item, 'count': count} for item, count in counts.most_common(10)]
    
    # ========================================================================
    # SMART SQLITE SEARCH (HYBRID AI)
    # ========================================================================
    
    def smart_search(
        self,
        query: str,
        search_type: str = 'hybrid'  # 'semantic', 'keyword', 'hybrid'
    ) -> Dict[str, Any]:
        """
        Smart SQLite search combining AI understanding + exact keyword matching.
        
        HYBRID APPROACH:
        1. AI interprets query: "ML engineers in Seattle" -> skills=['ML'], location='Seattle'
        2. SQLite exact match: WHERE keywords LIKE '%ML%' AND location='Seattle'
        3. Semantic expansion: ML -> machine learning, tensorflow, pytorch
        4. Combined results with relevance scoring
        
        Examples:
            "Find companies hiring Python developers"
            "Remote ML jobs at startups"
            "Senior engineer roles in tech hubs"
        
        Args:
            query: Natural language search query
            search_type: 'semantic' (AI-focused), 'keyword' (exact), 'hybrid' (both)
        
        Returns:
            Search strategy dictionary for SQLite execution
        """
        result = {
            'original_query': query,
            'search_type': search_type,
            'extracted_keywords': [],
            'extracted_location': None,
            'extracted_level': None,
            'extracted_role': None,
            'sql_where_clauses': [],
            'semantic_expansions': {}
        }
        
        query_lower = query.lower()
        
        # Extract tech keywords from query
        for keyword in self.tech_keywords:
            if keyword in query_lower:
                result['extracted_keywords'].append(keyword)
                
                # Semantic expansion
                result['semantic_expansions'][keyword] = self._expand_keyword(keyword)
        
        # Extract seniority level
        for level in JOB_TITLE_LEVELS:
            if level in query_lower:
                result['extracted_level'] = level
                break
        
        # Extract role type
        for role in JOB_TITLE_ROLES:
            if role in query_lower:
                result['extracted_role'] = role
                break
        
        # Extract location hints
        location_patterns = [
            r'\bin\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',  # "in Seattle", "in San Francisco"
            r'\bat\s+([A-Z][a-z]+)',  # "at Microsoft"
            r'\bremote\b',
            r'\bhybrid\b',
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, query)
            if matches:
                result['extracted_location'] = matches[0] if isinstance(matches[0], str) else matches[0]
                break
        
        # Build SQLite WHERE clauses
        if search_type in ['keyword', 'hybrid']:
            # Exact keyword matching
            for kw in result['extracted_keywords']:
                result['sql_where_clauses'].append(
                    f"(text_content LIKE '%{kw}%' OR title LIKE '%{kw}%')"
                )
            
            if result['extracted_level']:
                result['sql_where_clauses'].append(
                    f"title LIKE '%{result['extracted_level']}%'"
                )
            
            if result['extracted_role']:
                result['sql_where_clauses'].append(
                    f"title LIKE '%{result['extracted_role']}%'"
                )
            
            if result['extracted_location']:
                result['sql_where_clauses'].append(
                    f"(text_content LIKE '%{result['extracted_location']}%' OR url LIKE '%{result['extracted_location']}%')"
                )
        
        if search_type in ['semantic', 'hybrid']:
            # Add semantic expansions to WHERE clauses
            for base_kw, expanded in result['semantic_expansions'].items():
                expansion_clauses = [f"text_content LIKE '%{exp}%'" for exp in expanded[:3]]
                if expansion_clauses:
                    result['sql_where_clauses'].append(
                        f"({' OR '.join(expansion_clauses)})"
                    )
        
        # Construct final SQL
        if result['sql_where_clauses']:
            result['final_sql'] = (
                "SELECT * FROM company_sources WHERE content_type = 'careers' AND ("
                + " AND ".join(result['sql_where_clauses'])
                + ") ORDER BY exa_score DESC LIMIT 50"
            )
        else:
            result['final_sql'] = "SELECT * FROM company_sources WHERE content_type = 'careers' ORDER BY exa_score DESC LIMIT 50"
        
        return result
    
    def _expand_keyword(self, keyword: str) -> List[str]:
        """
        Semantically expand a keyword to related terms.
        
        Example: 'python' -> ['python', 'django', 'flask', 'fastapi']
        """
        expansions = {
            'python': ['python', 'django', 'flask', 'fastapi', 'pandas'],
            'ml': ['machine learning', 'tensorflow', 'pytorch', 'scikit-learn', 'deep learning'],
            'aws': ['aws', 'amazon web services', 'ec2', 's3', 'lambda'],
            'react': ['react', 'reactjs', 'react.js', 'next.js', 'gatsby'],
            'docker': ['docker', 'container', 'kubernetes', 'k8s'],
        }
        
        return expansions.get(keyword.lower(), [keyword])

# ============================================================================
# SINGLETON
# ============================================================================

_extractor_instance = None

def get_keyword_extractor() -> KeywordExtractor:
    """Get or create KeywordExtractor singleton."""
    global _extractor_instance
    
    if _extractor_instance is None:
        _extractor_instance = KeywordExtractor()
    
    return _extractor_instance
