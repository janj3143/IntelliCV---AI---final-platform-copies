"""
Education Parser Module
- Extracts education history from structured/unstructured data
- Designed for modular enrichment and user profile integration
"""
from pathlib import Path
from typing import List, Dict, Any


def extract_education(file_path: Path) -> List[Dict[str, Any]]:
    # Placeholder: implement actual extraction logic (degree, institution, dates, etc.)
    return [{
        "filename": file_path.name,
        "education": [
            {"degree": "BSc Computer Science", "institution": "Sample University", "start_year": 2015, "end_year": 2019}
        ]
    }]

# --- User_final integration hook ---
def attach_education_to_user_profile(user_profile: dict, education_data: List[Dict[str, Any]]) -> dict:
    """
    Hook for User_final: Attach parsed education data to user profile structure.
    """
    user_profile = user_profile.copy()
    user_profile["education"] = education_data
    return user_profile

# --- Enrichment integration hook ---
def enrich_and_attach_education(user_profile: dict, education_data: List[Dict[str, Any]]) -> dict:
    """
    Hook for User_final: Enrich education data and attach to user profile.
    """
    # Placeholder: call enrichment logic here
    enriched = enrich_education(education_data)
    user_profile = user_profile.copy()
    user_profile["education"] = enriched
    return user_profile

def parse_all_education(resume_dir: Path) -> List[Dict[str, Any]]:
    return [extract_education(f) for f in resume_dir.glob("*.pdf")]

# Hook for enrichment (to be implemented in enrichment/education_enricher.py)
def enrich_education(education_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Placeholder: call enrichment logic here
    return education_data
