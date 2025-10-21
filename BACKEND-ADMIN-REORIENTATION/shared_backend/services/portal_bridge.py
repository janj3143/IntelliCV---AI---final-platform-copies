"""
Portal Bridge - Unified Interface for Admin and User Portals
Connects portal pages to the comprehensive AI intelligence system

Created: October 21, 2025 - Phase 2 (Day 2)
"""

import logging
from pathlib import Path
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

# Add paths
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

# Import AI engines
from ai_engines.hybrid_integrator import HybridAIIntegrator
from ai_engines.intelligence_type_registry import get_global_registry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PortalBridge:
    """
    Unified bridge connecting admin and user portals to AI intelligence system.
    
    Provides high-level methods for portal pages to access:
    - All 70+ intelligence types via dynamic registry
    - 8 AI engines via hybrid integrator
    - Career predictions, job matching, skill analysis
    - Company intelligence, market analysis
    - Profile enrichment, engagement tracking
    - And all other discovered intelligence types
    
    Architecture:
        Portal Pages (Admin/User)
            ↓
        Portal Bridge (this class)
            ↓
        Hybrid AI Integrator (8 engines)
            ↓
        Intelligence Type Registry (70+ types)
            ↓
        Individual AI Engines (Inference, Neural, Expert, etc.)
    """
    
    def __init__(self):
        """Initialize the Portal Bridge with AI system access"""
        logger.info("Initializing Portal Bridge...")
        
        # Initialize core AI system
        self.ai_integrator = HybridAIIntegrator()
        
        # Get intelligence type registry
        self.intelligence_registry = get_global_registry()
        
        # Track portal usage
        self.portal_metrics = {
            'total_requests': 0,
            'requests_by_type': {},
            'admin_requests': 0,
            'user_requests': 0,
            'last_request_time': None
        }
        
        logger.info("Portal Bridge initialized successfully")
        logger.info(f"Available intelligence types: {len(self.intelligence_registry.types)}")
    
    # ========================================================================
    # CORE INTELLIGENCE ACCESS METHODS
    # ========================================================================
    
    def get_intelligence(
        self,
        intelligence_type: str,
        data: Dict[str, Any],
        portal_type: str = "user",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Universal intelligence access method for all portal pages.
        
        This is the PRIMARY method for accessing any intelligence type.
        It routes to the appropriate handler via the dynamic registry.
        
        Args:
            intelligence_type: Type of intelligence (e.g., 'company_intelligence', 'job_match')
            data: Input data for the intelligence operation
            portal_type: 'admin' or 'user' (for tracking)
            **kwargs: Additional parameters
        
        Returns:
            Intelligence results dictionary
        
        Example:
            # Get company intelligence
            result = bridge.get_intelligence(
                intelligence_type='company_intelligence',
                data={'company_name': 'RESATO INTERNATIONAL'},
                portal_type='admin'
            )
            
            # Get job match
            result = bridge.get_intelligence(
                intelligence_type='job_match',
                data={'profile': {...}, 'job': {...}},
                portal_type='user'
            )
        """
        try:
            # Track request
            self._track_request(intelligence_type, portal_type)
            
            # Route via AI integrator
            logger.info(f"Processing {intelligence_type} request from {portal_type} portal")
            result = self.ai_integrator.run_inference(data, intelligence_type, **kwargs)
            
            # Add metadata
            result['portal_bridge_metadata'] = {
                'intelligence_type': intelligence_type,
                'portal_type': portal_type,
                'timestamp': datetime.now().isoformat(),
                'bridge_version': '1.0'
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Intelligence request error ({intelligence_type}): {e}")
            return {
                'error': str(e),
                'intelligence_type': intelligence_type,
                'portal_type': portal_type
            }
    
    # ========================================================================
    # CAREER & JOB INTELLIGENCE METHODS
    # ========================================================================
    
    def portal_career_path_prediction(
        self,
        user_profile: Dict[str, Any],
        target_role: Optional[str] = None,
        timeframe_years: int = 5,
        portal_type: str = "user"
    ) -> Dict[str, Any]:
        """
        Predict career progression path for a candidate.
        
        Used by:
        - User Portal: Career Planning page
        - Admin Portal: Candidate analysis
        
        Args:
            user_profile: User profile with current_role, skills, experience
            target_role: Optional target role
            timeframe_years: Planning horizon (default: 5 years)
            portal_type: 'admin' or 'user'
        
        Returns:
            CareerPath with progression steps, required skills, timeline
        """
        return self.get_intelligence(
            intelligence_type='career_path',
            data={'profile': user_profile, 'target_role': target_role},
            portal_type=portal_type,
            timeframe_years=timeframe_years
        )
    
    def portal_job_matching(
        self,
        candidate_profile: Dict[str, Any],
        job_posting: Dict[str, Any],
        include_reasoning: bool = True,
        portal_type: str = "user"
    ) -> Dict[str, Any]:
        """
        Match a job to a candidate with explainable reasoning.
        
        Used by:
        - User Portal: Job recommendations
        - Admin Portal: Candidate-job compatibility
        
        Args:
            candidate_profile: Candidate profile
            job_posting: Job posting details
            include_reasoning: Include detailed reasoning
            portal_type: 'admin' or 'user'
        
        Returns:
            JobMatch with match scores, reasoning, recommendations
        """
        return self.get_intelligence(
            intelligence_type='job_match',
            data={'profile': candidate_profile, 'job': job_posting},
            portal_type=portal_type,
            include_reasoning=include_reasoning
        )
    
    def portal_skill_gap_analysis(
        self,
        current_skills: List[str],
        target_role: str,
        portal_type: str = "user"
    ) -> Dict[str, Any]:
        """
        Analyze skill gaps for a target role.
        
        Used by:
        - User Portal: Skill development page
        - Admin Portal: Training recommendations
        
        Args:
            current_skills: Current skill set
            target_role: Target role to analyze
            portal_type: 'admin' or 'user'
        
        Returns:
            SkillGapAnalysis with gaps, priorities, learning paths
        """
        return self.get_intelligence(
            intelligence_type='skill_gaps',
            data={'current_skills': current_skills, 'target_role': target_role},
            portal_type=portal_type
        )
    
    def portal_salary_estimate(
        self,
        job_title: str,
        location: str,
        experience_years: float,
        skills: Optional[List[str]] = None,
        portal_type: str = "user"
    ) -> Dict[str, Any]:
        """
        Estimate salary range based on market data.
        
        Used by:
        - User Portal: Salary expectations
        - Admin Portal: Offer preparation
        
        Args:
            job_title: Job role/title
            location: Geographic location
            experience_years: Years of experience
            skills: Optional skills list
            portal_type: 'admin' or 'user'
        
        Returns:
            SalaryInference with range, confidence, market data
        """
        return self.get_intelligence(
            intelligence_type='salary',
            data={
                'role': job_title,
                'location': location,
                'experience_years': experience_years,
                'skills': skills
            },
            portal_type=portal_type
        )
    
    # ========================================================================
    # COMPANY & MARKET INTELLIGENCE METHODS
    # ========================================================================
    
    def portal_company_intelligence(
        self,
        company_name: str,
        research_depth: str = "standard",
        portal_type: str = "admin"
    ) -> Dict[str, Any]:
        """
        Research and profile a company.
        
        Used by:
        - Admin Portal: Market Intelligence page (page 10, 11)
        - Admin Portal: Business Intelligence page (page 12, 13)
        
        Args:
            company_name: Company name to research
            research_depth: 'quick', 'standard', 'deep'
            portal_type: 'admin' or 'user'
        
        Returns:
            Company intelligence with financials, market position, etc.
        """
        return self.get_intelligence(
            intelligence_type='company_intelligence',
            data={'company_name': company_name, 'depth': research_depth},
            portal_type=portal_type
        )
    
    def portal_market_intelligence(
        self,
        industry: str,
        location: Optional[str] = None,
        role: Optional[str] = None,
        portal_type: str = "admin"
    ) -> Dict[str, Any]:
        """
        Generate market intelligence and trends.
        
        Used by:
        - Admin Portal: Market Intelligence page (page 10)
        - Admin Portal: Strategic Planning page (page 23)
        
        Args:
            industry: Industry/sector
            location: Optional location filter
            role: Optional role filter
            portal_type: 'admin' or 'user'
        
        Returns:
            Market intelligence with trends, positioning, opportunities
        """
        return self.get_intelligence(
            intelligence_type='market_intelligence',
            data={'industry': industry, 'location': location, 'role': role},
            portal_type=portal_type
        )
    
    # ========================================================================
    # PROFILE & ENGAGEMENT METHODS
    # ========================================================================
    
    def portal_profile_enrichment(
        self,
        user_profile: Dict[str, Any],
        enrichment_level: str = "standard",
        portal_type: str = "user"
    ) -> Dict[str, Any]:
        """
        Enrich user profile with AI analysis.
        
        Used by:
        - User Portal: Profile completion
        - Admin Portal: Candidate evaluation (page 06, 07, 08)
        
        Args:
            user_profile: User profile data
            enrichment_level: 'basic', 'standard', 'comprehensive'
            portal_type: 'admin' or 'user'
        
        Returns:
            Enriched profile with AI insights
        """
        return self.get_intelligence(
            intelligence_type='profile_analysis',
            data={'profile': user_profile, 'level': enrichment_level},
            portal_type=portal_type
        )
    
    def portal_touchpoint_tracking(
        self,
        user_id: str,
        touchpoint_type: str,
        touchpoint_data: Dict[str, Any],
        portal_type: str = "user"
    ) -> Dict[str, Any]:
        """
        Track user engagement touchpoints.
        
        Used by:
        - User Portal: All pages (engagement tracking)
        - Admin Portal: User Analytics page (page 20, 21)
        
        Args:
            user_id: User identifier
            touchpoint_type: Type of touchpoint
            touchpoint_data: Touchpoint data
            portal_type: 'admin' or 'user'
        
        Returns:
            Touchpoint analysis results
        """
        return self.get_intelligence(
            intelligence_type='touchpoint_analysis',
            data={
                'user_id': user_id,
                'type': touchpoint_type,
                'data': touchpoint_data
            },
            portal_type=portal_type
        )
    
    # ========================================================================
    # ADMIN PORTAL SPECIFIC METHODS
    # ========================================================================
    
    def portal_admin_dashboard_metrics(
        self,
        date_range: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive dashboard metrics for admin portal.
        
        Used by:
        - Admin Portal: Main Dashboard (pages 06, 07, 08)
        
        Args:
            date_range: Optional date range filter
        
        Returns:
            Dashboard metrics and KPIs
        """
        return {
            'intelligence_metrics': self.ai_integrator.get_implementation_status(),
            'portal_metrics': self.portal_metrics,
            'ai_performance': self.ai_integrator.get_performance_report(),
            'available_intelligence_types': len(self.intelligence_registry.types),
            'timestamp': datetime.now().isoformat()
        }
    
    def portal_admin_intelligence_catalog(
        self,
        category: Optional[str] = None,
        implemented_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get catalog of available intelligence types.
        
        Used by:
        - Admin Portal: System Configuration (page 25)
        - Admin Portal: API Documentation
        
        Args:
            category: Optional category filter
            implemented_only: Only show implemented types
        
        Returns:
            List of intelligence type information
        """
        return self.ai_integrator.get_intelligence_types(
            category=category,
            implemented_only=implemented_only
        )
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def _track_request(self, intelligence_type: str, portal_type: str):
        """Track intelligence request for metrics"""
        self.portal_metrics['total_requests'] += 1
        self.portal_metrics['last_request_time'] = datetime.now().isoformat()
        
        if portal_type == 'admin':
            self.portal_metrics['admin_requests'] += 1
        else:
            self.portal_metrics['user_requests'] += 1
        
        if intelligence_type not in self.portal_metrics['requests_by_type']:
            self.portal_metrics['requests_by_type'][intelligence_type] = 0
        self.portal_metrics['requests_by_type'][intelligence_type] += 1
    
    def get_portal_bridge_metrics(self) -> Dict[str, Any]:
        """
        Get Portal Bridge usage metrics.
        
        Returns:
            Usage statistics and performance metrics
        """
        return {
            'portal_metrics': self.portal_metrics,
            'ai_integrator_status': self.ai_integrator.get_implementation_status(),
            'available_intelligence_types': len(self.intelligence_registry.types),
            'top_intelligence_types': self.intelligence_registry.get_usage_stats(top_n=10),
            'timestamp': datetime.now().isoformat()
        }
    
    def list_available_intelligence_types(
        self,
        category: Optional[str] = None
    ) -> List[str]:
        """
        List all available intelligence type names.
        
        Args:
            category: Optional category filter
        
        Returns:
            List of intelligence type names
        """
        types = self.intelligence_registry.list_types(category=category)
        return [t['name'] for t in types]
    
    def get_intelligence_type_info(
        self,
        intelligence_type: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about an intelligence type.
        
        Args:
            intelligence_type: Intelligence type name
        
        Returns:
            Type information or None
        """
        return self.intelligence_registry.get_type_info(intelligence_type)


# ============================================================================
# Global Portal Bridge Instance
# ============================================================================

_global_portal_bridge = None

def get_portal_bridge() -> PortalBridge:
    """Get or create global Portal Bridge instance"""
    global _global_portal_bridge
    if _global_portal_bridge is None:
        _global_portal_bridge = PortalBridge()
    return _global_portal_bridge


# ============================================================================
# Convenience Functions for Portal Pages
# ============================================================================

def get_career_prediction(user_profile: Dict, target_role: Optional[str] = None) -> Dict:
    """Quick access to career path prediction"""
    bridge = get_portal_bridge()
    return bridge.portal_career_path_prediction(user_profile, target_role)

def get_job_match(candidate: Dict, job: Dict) -> Dict:
    """Quick access to job matching"""
    bridge = get_portal_bridge()
    return bridge.portal_job_matching(candidate, job)

def get_skill_gaps(current_skills: List[str], target_role: str) -> Dict:
    """Quick access to skill gap analysis"""
    bridge = get_portal_bridge()
    return bridge.portal_skill_gap_analysis(current_skills, target_role)

def get_salary_estimate(job_title: str, location: str, experience: float) -> Dict:
    """Quick access to salary estimation"""
    bridge = get_portal_bridge()
    return bridge.portal_salary_estimate(job_title, location, experience)

def get_company_intel(company_name: str) -> Dict:
    """Quick access to company intelligence"""
    bridge = get_portal_bridge()
    return bridge.portal_company_intelligence(company_name)

def get_market_intel(industry: str) -> Dict:
    """Quick access to market intelligence"""
    bridge = get_portal_bridge()
    return bridge.portal_market_intelligence(industry)
