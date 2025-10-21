"""
Pytest Configuration and Fixtures
Provides reusable test fixtures for all test modules
"""

import pytest
import json
import tempfile
from pathlib import Path
from typing import Dict, Any
import sys

# Add shared_backend to path
sys.path.insert(0, str(Path(__file__).parent / "shared_backend"))


# ============================================================================
# DIRECTORY FIXTURES
# ============================================================================

@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary data directory for testing"""
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    return data_dir


@pytest.fixture
def ai_data_dir(tmp_path):
    """Create a mock ai_data_final directory structure"""
    data_dir = tmp_path / "ai_data_final"
    data_dir.mkdir()
    return data_dir


# ============================================================================
# JSON FIXTURE DATA
# ============================================================================

@pytest.fixture
def sample_career_intelligence():
    """Sample career intelligence data"""
    return {
        "career_intelligence": {
            "trajectory": {
                "current_level": "Mid-Level",
                "progression_path": ["Junior", "Mid-Level", "Senior", "Lead"],
                "estimated_timeline": "3-5 years to Senior"
            },
            "growth_potential": {
                "score": 8.5,
                "factors": ["Strong technical skills", "Leadership potential"],
                "recommendations": ["Take on lead projects", "Mentor juniors"]
            }
        }
    }


@pytest.fixture
def sample_job_match_data():
    """Sample job matching data"""
    return {
        "job_match_intelligence": {
            "match_score": 87.5,
            "skill_alignment": {
                "matching_skills": ["Python", "AWS", "Docker"],
                "missing_skills": ["Kubernetes", "Terraform"],
                "transferable_skills": ["Problem solving", "Team collaboration"]
            },
            "recommendations": {
                "priority": "HIGH",
                "next_steps": ["Learn Kubernetes basics", "Complete Terraform certification"]
            }
        }
    }


@pytest.fixture
def sample_profile_data():
    """Sample candidate profile data"""
    return {
        "profile": {
            "name": "Test User",
            "current_role": "Software Engineer",
            "experience_years": 5,
            "skills": ["Python", "JavaScript", "React", "AWS"],
            "education": "BS Computer Science"
        }
    }


# ============================================================================
# JSON FILE FIXTURES
# ============================================================================

@pytest.fixture
def create_test_json_file(ai_data_dir):
    """Factory fixture to create test JSON files"""
    def _create_file(filename: str, data: Dict[str, Any]):
        file_path = ai_data_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return file_path
    return _create_file


@pytest.fixture
def career_intelligence_file(ai_data_dir, sample_career_intelligence):
    """Create a career intelligence JSON file"""
    file_path = ai_data_dir / "career_analysis.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(sample_career_intelligence, f, indent=2)
    return file_path


@pytest.fixture
def job_match_file(ai_data_dir, sample_job_match_data):
    """Create a job match JSON file"""
    file_path = ai_data_dir / "job_match_results.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(sample_job_match_data, f, indent=2)
    return file_path


@pytest.fixture
def multiple_intelligence_files(ai_data_dir, create_test_json_file):
    """Create multiple intelligence type files"""
    files = []
    
    # Career intelligence
    files.append(create_test_json_file("career_intel.json", {
        "career_path": {"trajectory": "upward", "timeline": "5 years"},
        "career_goals": {"target_role": "Senior Engineer", "target_salary": 150000}
    }))
    
    # Job matching
    files.append(create_test_json_file("job_match.json", {
        "job_compatibility": {"score": 85, "match_factors": ["skills", "experience"]},
        "job_recommendations": {"top_matches": ["Job A", "Job B"]}
    }))
    
    # Skill analysis
    files.append(create_test_json_file("skill_analysis.json", {
        "skill_gaps": {"missing": ["Kubernetes"], "proficiency": {"Python": "Advanced"}},
        "skill_recommendations": {"priority_skills": ["Docker", "AWS"]}
    }))
    
    return files


# ============================================================================
# COMPONENT FIXTURES
# ============================================================================

@pytest.fixture
def mock_registry():
    """Create a mock intelligence type registry"""
    from shared_backend.ai_engines.intelligence_type_registry import IntelligenceTypeRegistry
    return IntelligenceTypeRegistry()


@pytest.fixture
def mock_inference_engine():
    """Create a mock inference engine"""
    from shared_backend.ai_engines.inference_engine import InferenceEngine
    return InferenceEngine()


@pytest.fixture
def mock_portal_bridge():
    """Create a mock portal bridge"""
    try:
        from shared_backend.services.portal_bridge import PortalBridge
        return PortalBridge()
    except Exception as e:
        pytest.skip(f"Portal Bridge not available: {e}")


@pytest.fixture
def mock_hybrid_integrator():
    """Create a mock hybrid AI integrator"""
    try:
        from shared_backend.ai_engines.hybrid_integrator import HybridAIIntegrator
        return HybridAIIntegrator()
    except Exception as e:
        pytest.skip(f"Hybrid Integrator not available: {e}")


# ============================================================================
# HANDLER FIXTURES
# ============================================================================

@pytest.fixture
def simple_handler():
    """Simple test handler function"""
    def handler(data):
        return {
            'status': 'success',
            'data_received': data,
            'handler': 'simple_test_handler'
        }
    return handler


@pytest.fixture
def career_path_handler():
    """Mock career path handler"""
    def handler(data):
        return {
            'status': 'success',
            'predicted_path': 'Junior → Mid → Senior → Lead',
            'confidence': 0.85,
            'timeline': '5-7 years',
            'next_steps': ['Gain leadership experience', 'Complete advanced certifications']
        }
    return handler


# ============================================================================
# PERFORMANCE FIXTURES
# ============================================================================

@pytest.fixture
def benchmark_data_dir(tmp_path):
    """Create directory with many JSON files for benchmarking"""
    data_dir = tmp_path / "benchmark_data"
    data_dir.mkdir()
    
    # Create 100 sample files
    for i in range(100):
        file_path = data_dir / f"data_{i:03d}.json"
        with open(file_path, 'w') as f:
            json.dump({
                f"intelligence_type_{i}": {
                    "score": i * 0.9,
                    "data": f"test_data_{i}",
                    "metadata": {"file_id": i}
                }
            }, f)
    
    return data_dir


# ============================================================================
# CLEANUP
# ============================================================================

@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Cleanup after each test"""
    yield
    # Cleanup code here if needed
    pass


# ============================================================================
# PARAMETRIZE HELPERS
# ============================================================================

# Intelligence types for parametrized tests
INTELLIGENCE_TYPES = [
    'career_path',
    'job_match',
    'skill_gap_analysis',
    'salary_analysis',
    'company_intelligence',
    'interview_preparation'
]

# Priority levels
PRIORITY_LEVELS = ['HIGH', 'MEDIUM', 'LOW']

# Portal types
PORTAL_TYPES = ['user', 'admin', 'recruiter']
