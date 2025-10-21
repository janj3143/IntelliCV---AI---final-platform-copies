"""
Shared Backend Configuration
=============================

Central configuration for both admin and user portals
"""

from pathlib import Path

# Root paths
INTELLICV_ROOT = Path("C:/IntelliCV-AI/IntelliCV")
REORIENTATION_ROOT = INTELLICV_ROOT / "BACKEND-ADMIN-REORIENTATION"
SANDBOX_ROOT = INTELLICV_ROOT / "SANDBOX" / "admin_portal"

# Shared backend paths
SHARED_BACKEND_ROOT = REORIENTATION_ROOT / "shared_backend"
AI_ENGINES_PATH = SHARED_BACKEND_ROOT / "ai_engines"
SERVICES_PATH = SHARED_BACKEND_ROOT / "services"
DATA_MANAGEMENT_PATH = SHARED_BACKEND_ROOT / "data_management"

# Data paths (accessible by both admin and user)
AI_DATA_PATH = SANDBOX_ROOT / "ai_data_final"
BACKEND_DATA_PATH = SHARED_BACKEND_ROOT / "data"
MODELS_PATH = BACKEND_DATA_PATH / "models"
RULES_PATH = BACKEND_DATA_PATH / "rules"
FEEDBACK_PATH = BACKEND_DATA_PATH / "feedback"

# API Configuration
API_HOST = "localhost"
API_PORT = 8000
API_BASE_URL = f"http://{API_HOST}:{API_PORT}"

# Logging
LOG_LEVEL = "INFO"
LOG_DIR = SHARED_BACKEND_ROOT / "logs"

# Portal paths
ADMIN_PORTAL_PATH = REORIENTATION_ROOT / "admin_portal"
USER_PORTAL_PATH = REORIENTATION_ROOT / "user_portal"

# Email integration (external data)
EMAIL_DATA_PATH = INTELLICV_ROOT / "IntelliCV-data" / "email_extracted"

# Feature flags
ENABLE_NEURAL_NETWORK = True
ENABLE_EXPERT_SYSTEM = True
ENABLE_FEEDBACK_LOOP = True
ENABLE_HYBRID_AI = True

# Performance settings
MAX_WORKERS = 4
CACHE_SIZE = 1000
BATCH_SIZE = 50

# Security
ADMIN_ONLY_FEATURES = [
    "model_training",
    "rule_management",
    "user_management",
    "system_configuration"
]

USER_FEATURES = [
    "cv_enrichment",
    "job_matching",
    "skills_analysis",
    "career_recommendations"
]
