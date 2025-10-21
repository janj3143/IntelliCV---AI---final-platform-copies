"""
IntelliCV Shared Backend - Data Management Module

This module provides centralized data access for the IntelliCV platform.

Main Components:
---------------
- UnifiedDataConnector: Single source of truth for all data access
- get_connector(): Singleton function to get connector instance

Usage:
------
```python
from shared_backend.data_management import get_connector

# Get connector instance
connector = get_connector()

# Access data
job_titles = connector.get_job_titles()
career_path = connector.get_career_path("Software Engineer")
salary_data = connector.get_salary_data("Data Scientist", level="Senior")
```
"""

from .unified_data_connector import UnifiedDataConnector, get_connector

__all__ = ['UnifiedDataConnector', 'get_connector']
__version__ = '1.0.0'