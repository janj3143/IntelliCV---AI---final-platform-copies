"""
IntelliCV SANDBOX - Local Admin Configuration
============================================
This file contains all sensitive credentials and configuration data.
It is stored locally in SANDBOX and NOT uploaded to GitHub.

IMPORTANT: Update these values with your actual credentials
"""

# Admin Portal Authentication
ADMIN_CONFIG = {
    'username': 'admin',
    'password': 'changeme123',  # CHANGE THIS PASSWORD
    'session_timeout': 3600,    # 1 hour
    'max_login_attempts': 3
}

# Email Integration API Keys
EMAIL_CONFIGS = {
    'gmail': {
        'client_id': 'your-gmail-client-id-here',
        'client_secret': 'your-gmail-client-secret-here',
        'redirect_uri': 'http://localhost:8501/gmail_callback',
        'scopes': ['https://www.googleapis.com/auth/gmail.readonly']
    },
    'outlook': {
        'client_id': 'your-outlook-client-id-here',
        'client_secret': 'your-outlook-client-secret-here',
        'redirect_uri': 'http://localhost:8501/outlook_callback',
        'scopes': ['https://graph.microsoft.com/mail.read']
    },
    'yahoo': {
        'client_id': 'your-yahoo-client-id-here',
        'client_secret': 'your-yahoo-client-secret-here',
        'redirect_uri': 'http://localhost:8501/yahoo_callback',
        'scopes': ['mail-r']
    }
}

# AI/OpenAI Configuration
AI_CONFIG = {
    'openai_api_key': 'your-openai-api-key-here',
    'model': 'gpt-4',
    'max_tokens': 2000,
    'temperature': 0.7
}

# Database Configuration (if using local database)
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'intelicv',
    'username': 'app',
    'password': 'your-db-password-here'
}

# Data Storage Paths
DATA_PATHS = {
    'parsed_documents': r'c:\IntelliCV-AI\IntelliCV\SANDBOX\IntelliCV-data\parsed_documents',
    'ai_json_data': r'c:\IntelliCV-AI\IntelliCV\SANDBOX\IntelliCV-data\ai_json_data',
    'parser_output': r'c:\IntelliCV-AI\IntelliCV\SANDBOX\IntelliCV-data\parser_output',
    'email_data': r'c:\IntelliCV-AI\IntelliCV\SANDBOX\data\email_data',
    'temp_uploads': r'c:\IntelliCV-AI\IntelliCV\SANDBOX\IntelliCV-data\temp_uploads'
}

# Security Settings
SECURITY_CONFIG = {
    'secret_key': 'your-secret-key-for-encryption-here',
    'encryption_enabled': True,
    'session_encryption': True,
    'file_upload_max_size': 50 * 1024 * 1024,  # 50MB
    'allowed_file_types': ['.pdf', '.docx', '.doc', '.txt', '.csv', '.xlsx', '.xls', '.msg', '.rtf']
}

# Feature Flags
FEATURES = {
    'email_integration_enabled': False,  # Set to True when API keys are configured
    'ai_enrichment_enabled': False,      # Set to True when OpenAI key is configured
    'advanced_parsing_enabled': True,
    'cloud_storage_enabled': False,
    'audit_logging_enabled': True
}