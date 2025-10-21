#!/usr/bin/env python3
"""
🎯 IntelliCV AI Industry Classification & Job Analysis Demo Script
==================================================================

This script demonstrates the comprehensive industry classification and job title 
enhancement capabilities of the IntelliCV AI system.

Features:
- LinkedIn Industry Classification (26 categories, 223+ subcategories)
- Enhanced Job Title Analysis (salary, skills, market demand)
- Business Software Taxonomy (992+ categories)
- Export capabilities for AI integration

Author: IntelliCV AI System
Version: 2.0
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Add the admin portal to Python path
current_dir = Path(__file__).parent
admin_portal_path = current_dir.parent
sys.path.insert(0, str(admin_portal_path))

try:
    from services.linkedin_industry_classifier import LinkedInIndustryClassifier
    from services.enhanced_job_title_engine import EnhancedJobTitleEngine
    SYSTEMS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Could not import IntelliCV systems: {e}")
    SYSTEMS_AVAILABLE = False

def demonstrate_system():
    """Demonstrate the complete IntelliCV AI system capabilities"""
    
    print("🚀 IntelliCV AI System Demonstration")
    print("=" * 60)
    
    if not SYSTEMS_AVAILABLE:
        print("❌ IntelliCV AI systems not available for demo")
        return
    
    # Initialize systems
    industry_classifier = LinkedInIndustryClassifier()
    job_title_engine = EnhancedJobTitleEngine()
    
    print(f"✅ Systems initialized successfully!")
    print(f"📊 LinkedIn Industries: {len(industry_classifier.linkedin_industries)}")
    print(f"🏷️  Industry Subcategories: {sum(len(subs) for subs in industry_classifier.industry_subcategories.values())}")
    print(f"💼 Software Categories: {len(industry_classifier.software_categories)}")
    print(f"🎯 Job Title Database: {len(job_title_engine.job_titles_db)} normalized titles")
    
    # Demo job titles for analysis
    demo_jobs = [
        "Senior Software Engineer",
        "Digital Marketing Manager", 
        "Data Science Lead",
        "Healthcare Administrator",
        "Financial Risk Analyst",
        "UX/UI Designer",
        "DevOps Engineer",
        "Construction Project Manager"
    ]
    
    print(f"\n🔍 Analyzing {len(demo_jobs)} Job Titles")
    print("-" * 60)
    
    results = []
    
    for job_title in demo_jobs:
        print(f"\n📋 **{job_title}**")
        
        # Industry classification
        industry_result = industry_classifier.classify_job_title(job_title)
        print(f"   🏢 Industry: {industry_result['industry']} ({industry_result['confidence']:.2f})")
        
        # Enhanced job analysis
        job_analysis = job_title_engine.analyze_job_title_comprehensive(job_title)
        print(f"   💰 Salary: ${job_analysis['salary_min']:,} - ${job_analysis['salary_max']:,}")
        print(f"   📈 Market Demand: {job_analysis['market_demand']}")
        print(f"   🏠 Remote Work: {job_analysis['remote_potential']}")
        print(f"   🛠️  Top Skills: {', '.join(job_analysis['skills'][:3])}")
        
        # Store results
        results.append({
            'job_title': job_title,
            'industry': industry_result['industry'],
            'confidence': industry_result['confidence'],
            'salary_range': f"${job_analysis['salary_min']:,} - ${job_analysis['salary_max']:,}",
            'market_demand': job_analysis['market_demand'],
            'remote_potential': job_analysis['remote_potential'],
            'top_skills': job_analysis['skills'][:3]
        })
    
    # Export results
    export_data = {
        'demo_timestamp': datetime.now().isoformat(),
        'system_info': {
            'linkedin_industries': len(industry_classifier.linkedin_industries),
            'subcategories': sum(len(subs) for subs in industry_classifier.industry_subcategories.values()),
            'software_categories': len(industry_classifier.software_categories),
            'job_titles_db': len(job_title_engine.job_titles_db)
        },
        'analysis_results': results
    }
    
    # Save demo results
    output_file = current_dir / 'intellicv_demo_results.json'
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"\n💾 Demo Results Exported")
    print("-" * 30)
    print(f"📄 File: {output_file}")
    print(f"📊 Records: {len(results)}")
    print(f"🎯 Classification Success Rate: {sum(1 for r in results if r['confidence'] > 0.5) / len(results) * 100:.1f}%")
    
    # Summary statistics
    avg_confidence = sum(r['confidence'] for r in results) / len(results)
    high_demand_jobs = sum(1 for r in results if r['market_demand'] == 'High')
    high_remote_jobs = sum(1 for r in results if r['remote_potential'] == 'High')
    
    print(f"\n📈 Analysis Summary")
    print("-" * 30)
    print(f"🎯 Average Classification Confidence: {avg_confidence:.3f}")
    print(f"🔥 High Demand Positions: {high_demand_jobs}/{len(results)} ({high_demand_jobs/len(results)*100:.1f}%)")
    print(f"🏠 High Remote Work Potential: {high_remote_jobs}/{len(results)} ({high_remote_jobs/len(results)*100:.1f}%)")
    
    print(f"\n✅ IntelliCV AI System Demo Complete!")
    print(f"🚀 Ready for production integration and AI enhancement")

if __name__ == "__main__":
    demonstrate_system()