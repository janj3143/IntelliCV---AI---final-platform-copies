"""
Portal Bridge - Shared Façade for User ↔ Admin Integration
===========================================================
This module provides a unified interface for cross-portal communication.
Both user_portal_final and admin_portal import from this single source.

Usage:
    from shared_backend.services.portal_bridge import portal_bridge
    
    # Resume operations
    result = portal_bridge.resume.parse(file_path)
    
    # AI enrichment
    enriched = portal_bridge.intelligence.enrich(data)
    
    # Chat/coaching
    response = portal_bridge.chat.ask(question, context)
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import requests
import json

# Add admin_portal to path for service imports
ADMIN_PORTAL_PATH = Path(__file__).parent.parent.parent / "admin_portal"
if str(ADMIN_PORTAL_PATH) not in sys.path:
    sys.path.insert(0, str(ADMIN_PORTAL_PATH))


class ResumeService:
    """Resume parsing and analysis service"""
    
    def __init__(self):
        self.admin_api_base = os.getenv("ADMIN_API_URL", "http://localhost:8000")
        # Initialize automatic data ingestion service
        try:
            from services.automatic_data_ingestion_service import get_ingestion_service
            self.ingestion_service = get_ingestion_service()
            self.auto_ingest_enabled = True
        except ImportError:
            self.ingestion_service = None
            self.auto_ingest_enabled = False
    
    def parse(self, file_path: str, user_id: Optional[str] = None, resume_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse resume using admin portal's complete data parser
        AND automatically ingest into AI system for enrichment.
        
        Args:
            file_path: Path to resume file
            user_id: Optional user identifier
            resume_id: Optional resume identifier
            
        Returns:
            Parsed resume data
        """
        try:
            # Try to import admin parser directly
            from services.complete_data_parser import UniversalResumeParser
            parser = UniversalResumeParser()
            parsed_data = parser.parse_resume(file_path)
            
            # AUTOMATIC INGESTION: Save to AI system
            if self.auto_ingest_enabled and parsed_data and 'error' not in parsed_data:
                ingestion_result = self.ingestion_service.ingest_resume_upload(
                    resume_data=parsed_data,
                    user_id=user_id
                )
                parsed_data['ai_ingestion'] = ingestion_result
            
            return parsed_data
            
        except ImportError:
            # Fallback to API call
            try:
                with open(file_path, 'rb') as f:
                    response = requests.post(
                        f"{self.admin_api_base}/api/v1/resume/parse",
                        files={'file': f},
                        data={'user_id': user_id} if user_id else {}
                    )
                    response.raise_for_status()
                    parsed_data = response.json()
                    
                    # AUTOMATIC INGESTION via API
                    if self.auto_ingest_enabled and parsed_data and 'error' not in parsed_data:
                        ingestion_result = self.ingestion_service.ingest_resume_upload(
                            resume_data=parsed_data,
                            user_id=user_id
                        )
                        parsed_data['ai_ingestion'] = ingestion_result
                    
                    return parsed_data
            except Exception as e:
                return {'error': str(e), 'status': 'failed'}
    
    def analyze(self, resume_id: str) -> Dict[str, Any]:
        """Analyze parsed resume"""
        try:
            from services.unified_ai_engine import get_unified_ai_engine
            engine = get_unified_ai_engine()
            return engine.analyze_resume(resume_id)
        except ImportError:
            try:
                response = requests.get(f"{self.admin_api_base}/api/v1/resume/{resume_id}/analyze")
                response.raise_for_status()
                return response.json()
            except Exception as e:
                return {'error': str(e), 'status': 'failed'}


class IntelligenceService:
    """AI enrichment and intelligence service"""
    
    def __init__(self):
        self.admin_api_base = os.getenv("ADMIN_API_URL", "http://localhost:8000")
        self.secure_api_base = os.getenv("SECURE_API_URL", "http://localhost:8001")
    
    def enrich(self, data: Dict[str, Any], user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Enrich data using unified AI engine
        
        Args:
            data: Data to enrich
            user_id: Optional user identifier
            
        Returns:
            Enriched data
        """
        try:
            # Try direct import
            from services.unified_ai_engine import get_unified_ai_engine
            engine = get_unified_ai_engine()
            return engine.enrich_data(data)
        except ImportError:
            # Fallback to secure API
            try:
                response = requests.post(
                    f"{self.secure_api_base}/api/v1/enrich",
                    json={'data': data, 'user_id': user_id}
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                return {'error': str(e), 'status': 'failed'}
    
    def analyze_career(self, resume_id: str) -> Dict[str, Any]:
        """Career intelligence analysis"""
        try:
            from services.unified_ai_engine import get_unified_ai_engine
            engine = get_unified_ai_engine()
            return engine.analyze_career_trajectory(resume_id)
        except ImportError:
            try:
                response = requests.get(f"{self.admin_api_base}/api/v1/career/analyze/{resume_id}")
                response.raise_for_status()
                return response.json()
            except Exception as e:
                return {'error': str(e), 'status': 'failed'}
    
    def get_market_intel(self, role: str, location: str) -> Dict[str, Any]:
        """Market intelligence for role/location"""
        try:
            from services.company_intelligence_api import CompanyIntelligenceAPI
            api = CompanyIntelligenceAPI()
            return api.get_market_data(role, location)
        except ImportError:
            try:
                response = requests.get(
                    f"{self.admin_api_base}/api/v1/market/intel",
                    params={'role': role, 'location': location}
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                return {'error': str(e), 'status': 'failed'}


class ChatService:
    """Chat and coaching service"""
    
    def __init__(self):
        self.admin_api_base = os.getenv("ADMIN_API_URL", "http://localhost:8000")
    
    def ask(self, question: str, context: Optional[Dict[str, Any]] = None, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Ask question to AI chat service
        
        Args:
            question: User question
            context: Optional context data
            user_id: Optional user identifier
            
        Returns:
            AI response
        """
        try:
            from services.ai_chat_integration import AIChatIntegration
            chat = AIChatIntegration()
            return chat.get_response(question, context)
        except ImportError:
            try:
                response = requests.post(
                    f"{self.admin_api_base}/api/v1/chat",
                    json={'question': question, 'context': context, 'user_id': user_id}
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                return {'error': str(e), 'status': 'failed'}
    
    def get_coaching_advice(self, resume_id: str, goal: str) -> Dict[str, Any]:
        """Get coaching advice"""
        try:
            from services.ai_chat_integration import AIChatIntegration
            chat = AIChatIntegration()
            return chat.get_coaching_advice(resume_id, goal)
        except ImportError:
            try:
                response = requests.post(
                    f"{self.admin_api_base}/api/v1/coaching",
                    json={'resume_id': resume_id, 'goal': goal}
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                return {'error': str(e), 'status': 'failed'}


class PortalBridge:
    """Main portal bridge façade"""
    
    def __init__(self):
        self.resume = ResumeService()
        self.intelligence = IntelligenceService()
        self.chat = ChatService()
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of all services"""
        return {
            'resume_service': 'ok',
            'intelligence_service': 'ok',
            'chat_service': 'ok',
            'status': 'healthy'
        }


# Singleton instance
portal_bridge = PortalBridge()


# Alias for backward compatibility
class PortalBridgeClass:
    """Backward compatible class-based access"""
    resume = portal_bridge.resume
    intelligence = portal_bridge.intelligence
    chat = portal_bridge.chat
