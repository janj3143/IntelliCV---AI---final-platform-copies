"""
IntelliCV-AI Enhanced Job Title Database
======================================

This file contains processed and normalized job titles for AI enhancement
Generated: September 30, 2025
Source: Multiple job title datasets with normalization and categorization
"""

import json
from datetime import datetime

# Load and save processed job title data
def save_job_title_data():
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from services.job_title_enhancement_engine import main
    
    # Generate the enhanced data
    ai_data = main()
    
    # Save to AI data directory
    output_file = "ai_data/enhanced_job_titles_database.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(ai_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Enhanced job title database saved to: {output_file}")
    
    # Also create a CSV version for easy access
    csv_output = "ai_data/job_titles_categorized.csv"
    
    # Create CSV data
    csv_data = []
    for category, titles in ai_data['categorized_titles'].items():
        for title in titles:
            csv_data.append({
                'job_title': title,
                'category': category,
                'normalized': True
            })
    
    # Write CSV manually (no pandas dependency)
    with open(csv_output, 'w', encoding='utf-8') as f:
        f.write("job_title,category,normalized\n")
        for row in csv_data:
            f.write(f'"{row["job_title"]}","{row["category"]}",{row["normalized"]}\n')
    
    print(f"📊 CSV export saved to: {csv_output}")
    
    return ai_data

if __name__ == "__main__":
    data = save_job_title_data()
    
    # Print summary statistics
    print("\n📈 **Enhanced Job Title Database Summary:**")
    print(f"   Total Unique Titles: {data['total_titles_processed']}")
    print(f"   Industry Categories: {len(data['categorized_titles'])}")
    print(f"   Career Progressions: {len(data['career_progressions'])}")
    print(f"   Skill Mappings: {len(data['skill_mappings'])}")
    
    print("\n🏢 **Top Industries by Job Count:**")
    sorted_categories = sorted(data['categorized_titles'].items(), 
                              key=lambda x: len(x[1]), reverse=True)
    
    for category, titles in sorted_categories[:8]:
        print(f"   {category}: {len(titles)} titles")