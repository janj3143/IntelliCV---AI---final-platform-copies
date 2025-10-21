#!/usr/bin/env python3
"""
🎯 IntelliCV AI Industry Classification & Job Analysis Quick Demo
===============================================================

Quick demonstration of the IntelliCV AI system capabilities
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

def quick_demo():
    """Quick demonstration of core capabilities"""
    
    print("🚀 IntelliCV AI Quick Demo")
    print("=" * 40)
    
    if not SYSTEMS_AVAILABLE:
        print("❌ IntelliCV AI systems not available")
        return
    
    # Initialize systems
    industry_classifier = LinkedInIndustryClassifier()
    job_title_engine = EnhancedJobTitleEngine()
    
    print(f"✅ Systems loaded successfully!")
    
    # Demo job titles
    demo_jobs = [
        "Software Engineer",
        "Marketing Manager", 
        "Data Scientist",
        "Registered Nurse",
        "Financial Analyst"
    ]
    
    print(f"\n🔍 Analyzing {len(demo_jobs)} Job Titles:")
    print("-" * 40)
    
    results = []
    
    for job_title in demo_jobs:
        print(f"\n📋 {job_title}")
        
        # Industry classification
        try:
            industry_result = industry_classifier.classify_job_title(job_title)
            print(f"   🏢 Industry: {industry_result.get('industry', 'Unknown')}")
            print(f"   📊 Confidence: {industry_result.get('confidence', 0.0):.2f}")
        except Exception as e:
            print(f"   ⚠️  Industry classification error: {e}")
            industry_result = {'industry': 'Error', 'confidence': 0.0}
        
        # Job analysis
        try:
            job_analysis = job_title_engine.analyze_job_title_comprehensive(job_title)
            print(f"   💰 Salary: ${job_analysis.get('salary_min', 0):,} - ${job_analysis.get('salary_max', 0):,}")
            print(f"   📈 Demand: {job_analysis.get('market_demand', 'Unknown')}")
            print(f"   🏠 Remote: {job_analysis.get('remote_potential', 'Unknown')}")
        except Exception as e:
            print(f"   ⚠️  Job analysis error: {e}")
            job_analysis = {'salary_min': 0, 'salary_max': 0, 'market_demand': 'Error', 'remote_potential': 'Error'}
        
        results.append({
            'job_title': job_title,
            'industry': industry_result.get('industry', 'Unknown'),
            'confidence': industry_result.get('confidence', 0.0),
            'salary_min': job_analysis.get('salary_min', 0),
            'salary_max': job_analysis.get('salary_max', 0),
            'market_demand': job_analysis.get('market_demand', 'Unknown'),
            'remote_potential': job_analysis.get('remote_potential', 'Unknown')
        })
    
    # Summary
    print(f"\n📊 Demo Summary:")
    print("-" * 20)
    successful_classifications = sum(1 for r in results if r['confidence'] > 0.0)
    print(f"🎯 Successful Classifications: {successful_classifications}/{len(results)}")
    
    if successful_classifications > 0:
        avg_confidence = sum(r['confidence'] for r in results if r['confidence'] > 0.0) / successful_classifications
        print(f"📈 Average Confidence: {avg_confidence:.3f}")
    
    high_demand = sum(1 for r in results if r['market_demand'] == 'High')
    high_remote = sum(1 for r in results if r['remote_potential'] == 'High')
    
    print(f"🔥 High Demand Jobs: {high_demand}")
    print(f"🏠 High Remote Potential: {high_remote}")
    
    # Export results
    output_file = current_dir / 'quick_demo_results.json'
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'results': results,
            'summary': {
                'total_jobs': len(results),
                'successful_classifications': successful_classifications,
                'high_demand_jobs': high_demand,
                'high_remote_jobs': high_remote
            }
        }, f, indent=2)
    
    print(f"💾 Results saved to: {output_file.name}")
    print(f"✅ IntelliCV AI Demo Complete!")

if __name__ == "__main__":
    quick_demo()