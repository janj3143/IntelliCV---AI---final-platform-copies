Company Parser Module
"""
from pathlib import Path

def extract_company_info(file_path: Path) -> dict:
    # Placeholder: implement actual company extraction logic
    return {"filename": file_path.name, "company": "Sample Company", "fields": {}}

def parse_all_companies(resume_dir: Path) -> list:
    return [extract_company_info(f) for f in resume_dir.glob("*.pdf")]

