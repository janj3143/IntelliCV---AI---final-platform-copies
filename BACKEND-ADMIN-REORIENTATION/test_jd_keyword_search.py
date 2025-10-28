"""
Smart JD Keyword Search - Examples
===================================
Demonstrates the JD-focused keyword extraction and smart SQLite search.

This shows:
1. Extracting keywords from job descriptions
2. Analyzing job titles
3. Smart hybrid AI + SQLite searches
"""

import sys
from pathlib import Path

# Add shared_backend to path
backend_path = Path(__file__).parent / "shared_backend"
sys.path.insert(0, str(backend_path))

from services.exa_service.keyword_extractor import get_keyword_extractor

# Sample job description
SAMPLE_JD = """
Senior Machine Learning Engineer

We're seeking an experienced ML Engineer to join our AI team.

Requirements:
- 5+ years of experience in Python development
- Strong knowledge of TensorFlow and PyTorch
- Experience with AWS (EC2, S3, SageMaker)
- Proficient in SQL and NoSQL databases
- Bachelor's or Master's degree in Computer Science or related field

Nice to have:
- PhD in Machine Learning or AI
- Experience with Kubernetes and Docker
- Published research in top-tier conferences
- Leadership experience

Responsibilities:
- Design and implement ML models
- Optimize model performance
- Collaborate with cross-functional teams
- Mentor junior engineers

We offer:
- Competitive salary ($150k-$200k)
- Remote work options
- Stock options
- Healthcare, dental, vision
- 401k matching
"""

def test_jd_keyword_extraction():
    """Test 1: Extract keywords from job description."""
    print("\n" + "="*70)
    print("TEST 1: JOB DESCRIPTION KEYWORD EXTRACTION")
    print("="*70)
    
    extractor = get_keyword_extractor()
    result = extractor.extract_job_description_keywords(SAMPLE_JD)
    
    print(f"\n📋 Experience Required: {result['experience']}")
    print(f"\n🎓 Education: {', '.join(result['education'])}")
    
    print(f"\n✅ Required Skills ({len(result['required_skills'])}):")
    for skill in result['required_skills'][:10]:
        print(f"   - {skill}")
    
    print(f"\n💎 Nice-to-Have ({len(result['nice_to_have'])}):")
    for skill in result['nice_to_have'][:5]:
        print(f"   - {skill}")
    
    print(f"\n🔧 Tech Stack (Top 10 by frequency):")
    for tech in result['tech_stack'][:10]:
        print(f"   - {tech['keyword']}: {tech['frequency']} mentions (confidence: {tech['confidence']})")
    
    print(f"\n🤝 Soft Skills: {', '.join(result['soft_skills'])}")
    
    print(f"\n📊 Keyword Frequency Count:")
    sorted_keywords = sorted(result['keyword_counts'].items(), key=lambda x: x[1], reverse=True)
    for keyword, count in sorted_keywords[:15]:
        print(f"   {keyword}: {count}")

def test_job_title_analysis():
    """Test 2: Analyze job titles."""
    print("\n" + "="*70)
    print("TEST 2: JOB TITLE ANALYSIS")
    print("="*70)
    
    extractor = get_keyword_extractor()
    
    titles = [
        "Senior Machine Learning Engineer",
        "Staff Software Developer",
        "Junior Frontend Developer",
        "Principal Data Scientist",
        "Lead Backend Engineer",
        "ML Engineer II",
        "Entry Level Software Engineer"
    ]
    
    print(f"\n🔍 Analyzing {len(titles)} job titles:\n")
    
    for title in titles:
        analysis = extractor.analyze_job_title(title)
        print(f"Title: {title}")
        print(f"  Level: {analysis['level']} | Role: {analysis['role']} | Domain: {analysis['domain']}")
        print(f"  Seniority Score: {analysis['seniority_score']}/100")
        print()
    
    # Batch analysis
    batch_result = extractor.batch_analyze_job_titles(titles)
    
    print("\n📊 AGGREGATED ANALYSIS:")
    print(f"Total titles analyzed: {batch_result['total_titles']}")
    print(f"Average seniority: {batch_result['average_seniority']:.1f}/100")
    
    print(f"\nMost common levels:")
    for item in batch_result['most_common_levels'][:5]:
        print(f"  - {item['item']}: {item['count']} times")
    
    print(f"\nMost common roles:")
    for item in batch_result['most_common_roles'][:5]:
        print(f"  - {item['item']}: {item['count']} times")
    
    print(f"\nMost common domains:")
    for item in batch_result['most_common_domains'][:5]:
        print(f"  - {item['item']}: {item['count']} times")

def test_smart_search():
    """Test 3: Smart SQLite hybrid search."""
    print("\n" + "="*70)
    print("TEST 3: SMART HYBRID AI + SQLITE SEARCH")
    print("="*70)
    
    extractor = get_keyword_extractor()
    
    # Test queries
    queries = [
        "Find companies hiring Python developers",
        "Senior ML engineer roles in Seattle",
        "Remote backend jobs at startups",
        "AWS engineers with Docker experience",
    ]
    
    for query in queries:
        print(f"\n🔍 Query: \"{query}\"")
        print("-" * 70)
        
        result = extractor.smart_search(query, search_type='hybrid')
        
        print(f"\n📌 Extracted Components:")
        print(f"   Keywords: {result['extracted_keywords']}")
        print(f"   Level: {result['extracted_level']}")
        print(f"   Role: {result['extracted_role']}")
        print(f"   Location: {result['extracted_location']}")
        
        if result['semantic_expansions']:
            print(f"\n🧠 Semantic Expansions:")
            for base, expanded in result['semantic_expansions'].items():
                print(f"   {base} -> {', '.join(expanded[:3])}")
        
        print(f"\n💾 SQLite WHERE Clauses:")
        for clause in result['sql_where_clauses']:
            print(f"   {clause}")
        
        print(f"\n📝 Generated SQL:")
        print(f"   {result['final_sql'][:150]}...")
        print()

def test_keyword_comparison():
    """Test 4: Compare JDs for keyword overlap."""
    print("\n" + "="*70)
    print("TEST 4: KEYWORD COMPARISON ACROSS JDs")
    print("="*70)
    
    jd1 = "Python developer with AWS and Docker experience. 5+ years required."
    jd2 = "Senior Python engineer. AWS, Kubernetes, and CI/CD expertise needed. 7 years experience."
    jd3 = "Backend developer. Java, Spring Boot, AWS. 3-5 years experience."
    
    extractor = get_keyword_extractor()
    
    results = [
        extractor.extract_job_description_keywords(jd1),
        extractor.extract_job_description_keywords(jd2),
        extractor.extract_job_description_keywords(jd3)
    ]
    
    print("\n📊 Comparing 3 Job Descriptions:\n")
    
    # Find common skills
    all_skills = []
    for r in results:
        all_skills.extend(r['required_skills'])
    
    from collections import Counter
    skill_counts = Counter(all_skills)
    
    print("🎯 Most Commonly Required Skills:")
    for skill, count in skill_counts.most_common(10):
        percentage = (count / len(results)) * 100
        print(f"   {skill}: {count}/{len(results)} JDs ({percentage:.0f}%)")
    
    print("\n📈 Experience Requirements:")
    for i, r in enumerate(results, 1):
        exp = r['experience']
        if exp:
            print(f"   JD {i}: {exp.get('years_required', 'N/A')} years")
    
    print("\n💡 Insight: Skills appearing in 100% of JDs are MUST-HAVE")
    print("           Skills in 33-66% are COMPETITIVE ADVANTAGE")

def main():
    """Run all tests."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     SMART JD KEYWORD EXTRACTION & SEARCH - TEST SUITE           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    test_jd_keyword_extraction()
    test_job_title_analysis()
    test_smart_search()
    test_keyword_comparison()
    
    print("\n" + "="*70)
    print("✅ ALL TESTS COMPLETE!")
    print("="*70)
    print("\nKey Features Demonstrated:")
    print("  ✓ JD keyword extraction (required vs nice-to-have)")
    print("  ✓ Tech stack frequency counting")
    print("  ✓ Job title analysis (level, role, domain)")
    print("  ✓ Smart hybrid AI + SQLite search")
    print("  ✓ Semantic keyword expansion")
    print("  ✓ Multi-JD comparison")
    print("\n💡 Use these features in:")
    print("   - Admin Page 27: Enhanced company enrichment")
    print("   - User Portal: Smart job search")
    print("   - Backend: Automated matching algorithms")
    print()

if __name__ == "__main__":
    main()
