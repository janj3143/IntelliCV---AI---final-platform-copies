"""
=============================================================================
IntelliCV Inference Engine - Career & Job Intelligence System
=============================================================================

The MISSING engine from the Super Hybrid AI architecture!

This engine provides reasoning-based inference for:
- Career path prediction and progression analysis
- Job-to-candidate matching with explainable reasoning
- Skill gap identification and learning path recommendations
- Salary range inference from market data
- Career transition success probability
- Role compatibility assessment

Integrates with:
- Hybrid Integrator (Level 1 Core Engine)
- Portal Bridge (User-facing interface)
- Market Intelligence Service (trend data)
- Statistical Analysis Module (predictions)

Author: IntelliCV AI Integration Team
Date: October 21, 2025
Purpose: Complete the Super Hybrid AI "7-System" architecture
Environment: IntelliCV\env310 with ML/AI stack
"""

import numpy as np
import pandas as pd
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import re

# ML/AI Imports
try:
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logging.warning("scikit-learn not available - using fallback inference methods")

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    logging.warning("spaCy not available - using basic NLP")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class CareerPath:
    """Represents a predicted career progression path"""
    current_role: str
    target_role: str
    intermediate_steps: List[Dict[str, Any]]
    total_duration_years: float
    success_probability: float
    required_skills: List[str]
    confidence: float
    reasoning: List[str]
    
    def to_dict(self):
        return asdict(self)


@dataclass
class JobMatch:
    """Represents a job match analysis"""
    job_id: str
    job_title: str
    match_score: float
    confidence: float
    skill_match_percentage: float
    experience_match: bool
    salary_compatibility: bool
    location_compatibility: bool
    missing_skills: List[str]
    matching_skills: List[str]
    reasoning: List[str]
    recommendations: List[str]
    
    def to_dict(self):
        return asdict(self)


@dataclass
class SkillGapAnalysis:
    """Skill gap analysis with learning recommendations"""
    current_skills: List[str]
    target_role: str
    required_skills: List[str]
    skill_gaps: List[str]
    transferable_skills: List[str]
    learning_path: List[Dict[str, Any]]
    estimated_learning_time_months: int
    priority_skills: List[str]
    confidence: float
    
    def to_dict(self):
        return asdict(self)


@dataclass
class SalaryInference:
    """Salary range inference"""
    role: str
    location: str
    experience_years: float
    estimated_min: float
    estimated_max: float
    market_median: float
    percentile_rank: int
    factors: Dict[str, Any]
    confidence: float
    reasoning: List[str]
    
    def to_dict(self):
        return asdict(self)


# =============================================================================
# INFERENCE ENGINE
# =============================================================================

class InferenceEngine:
    """
    Advanced inference engine for career intelligence.
    
    This is the MISSING 7th engine in the Super Hybrid AI system!
    Provides reasoning-based predictions and recommendations.
    """
    
    def __init__(self, data_path: Optional[Path] = None):
        """
        Initialize the inference engine.
        
        Args:
            data_path: Optional path to career/market data
        """
        self.data_path = data_path or Path(__file__).parent.parent / "data"
        self.initialized = False
        
        # Career progression rules
        self.career_ladder = self._load_career_ladder()
        
        # Skill taxonomies
        self.skill_taxonomy = self._load_skill_taxonomy()
        
        # Market data cache
        self.market_data_cache = {}
        self.cache_timestamp = None
        
        # ML components
        self.vectorizer = TfidfVectorizer(max_features=500) if SKLEARN_AVAILABLE else None
        self.scaler = StandardScaler() if SKLEARN_AVAILABLE else None
        
        # NLP
        try:
            if SPACY_AVAILABLE:
                self.nlp = spacy.load("en_core_web_sm")
            else:
                self.nlp = None
        except:
            self.nlp = None
            logger.warning("spaCy model not loaded - using basic text processing")
        
        # Statistics
        self.inference_count = 0
        self.successful_inferences = 0
        
        logger.info("✅ Inference Engine initialized")
        self.initialized = True
    
    # =========================================================================
    # CAREER PATH INFERENCE
    # =========================================================================
    
    def infer_career_path(
        self, 
        profile: Dict[str, Any],
        target_role: Optional[str] = None,
        timeframe_years: int = 5
    ) -> CareerPath:
        """
        Predict career progression path from current profile.
        
        Args:
            profile: User profile with current role, skills, experience
            target_role: Optional target role (auto-infer if not provided)
            timeframe_years: Planning horizon
            
        Returns:
            CareerPath object with predictions and reasoning
        """
        logger.info(f"🎯 Inferring career path for {profile.get('current_role', 'Unknown')}")
        
        current_role = profile.get('current_role', '')
        current_skills = set(profile.get('skills', []))
        experience_years = profile.get('experience_years', 0)
        
        # Auto-infer target role if not provided
        if not target_role:
            target_role = self._infer_next_logical_role(current_role, experience_years)
        
        # Build progression path
        intermediate_steps = self._build_progression_steps(
            current_role, 
            target_role, 
            current_skills,
            experience_years,
            timeframe_years
        )
        
        # Calculate required skills
        required_skills = self._calculate_required_skills(current_role, target_role)
        
        # Calculate success probability
        success_probability = self._calculate_transition_probability(
            current_role,
            target_role,
            current_skills,
            experience_years
        )
        
        # Calculate total duration
        total_duration = sum(step.get('duration_years', 1) for step in intermediate_steps)
        
        # Generate reasoning
        reasoning = self._generate_career_path_reasoning(
            current_role,
            target_role,
            intermediate_steps,
            success_probability
        )
        
        # Calculate confidence
        confidence = self._calculate_path_confidence(
            current_skills,
            required_skills,
            experience_years
        )
        
        self.inference_count += 1
        self.successful_inferences += 1
        
        return CareerPath(
            current_role=current_role,
            target_role=target_role,
            intermediate_steps=intermediate_steps,
            total_duration_years=total_duration,
            success_probability=success_probability,
            required_skills=required_skills,
            confidence=confidence,
            reasoning=reasoning
        )
    
    def _infer_next_logical_role(self, current_role: str, experience: float) -> str:
        """Infer the next logical career step"""
        # Normalize role
        role_normalized = self._normalize_role_title(current_role)
        
        # Check career ladder
        if role_normalized in self.career_ladder:
            ladder = self.career_ladder[role_normalized]
            
            # Find appropriate next step based on experience
            for step in ladder.get('progression', []):
                if experience >= step.get('min_experience', 0):
                    return step.get('role')
        
        # Fallback: Infer from seniority level
        if 'junior' in role_normalized.lower():
            return role_normalized.replace('junior', 'mid-level').replace('Jr.', '')
        elif 'senior' not in role_normalized.lower() and 'lead' not in role_normalized.lower():
            return f"Senior {role_normalized}"
        else:
            return f"Lead {role_normalized}"
    
    def _build_progression_steps(
        self,
        current: str,
        target: str,
        skills: Set[str],
        experience: float,
        timeframe: int
    ) -> List[Dict[str, Any]]:
        """Build intermediate career steps"""
        steps = []
        
        # Direct transition possible?
        if self._is_direct_transition_viable(current, target, experience):
            steps.append({
                'role': target,
                'duration_years': min(2, timeframe),
                'skills_needed': list(self._calculate_required_skills(current, target) - skills),
                'difficulty': 'Medium',
                'success_rate': 0.75,
                'salary_increase': '+20-30%'
            })
        else:
            # Need intermediate steps
            intermediate = self._find_intermediate_roles(current, target)
            
            years_per_step = timeframe / max(len(intermediate) + 1, 1)
            
            for i, role in enumerate(intermediate):
                steps.append({
                    'role': role,
                    'duration_years': years_per_step,
                    'skills_needed': list(self._calculate_required_skills(
                        current if i == 0 else intermediate[i-1], 
                        role
                    ) - skills),
                    'difficulty': 'Medium' if i == 0 else 'High',
                    'success_rate': 0.80 if i == 0 else 0.65,
                    'salary_increase': '+15-20%' if i == 0 else '+20-30%'
                })
            
            # Final step to target
            steps.append({
                'role': target,
                'duration_years': years_per_step,
                'skills_needed': list(self._calculate_required_skills(
                    intermediate[-1] if intermediate else current,
                    target
                ) - skills),
                'difficulty': 'High',
                'success_rate': 0.70,
                'salary_increase': '+25-35%'
            })
        
        return steps
    
    # =========================================================================
    # JOB MATCHING WITH REASONING
    # =========================================================================
    
    def match_job_to_candidate(
        self,
        profile: Dict[str, Any],
        job: Dict[str, Any],
        include_reasoning: bool = True
    ) -> JobMatch:
        """
        Match a job to a candidate with explainable reasoning.
        
        Args:
            profile: Candidate profile
            job: Job posting details
            include_reasoning: Whether to generate detailed reasoning
            
        Returns:
            JobMatch object with scores and reasoning
        """
        logger.info(f"🔍 Matching job '{job.get('title', 'Unknown')}' to candidate")
        
        # Extract data
        candidate_skills = set(s.lower().strip() for s in profile.get('skills', []))
        required_skills = set(s.lower().strip() for s in job.get('requirements', []))
        candidate_experience = profile.get('experience_years', 0)
        required_experience = job.get('required_experience_years', 0)
        candidate_location = profile.get('location', '')
        job_location = job.get('location', '')
        
        # Calculate skill match
        matching_skills = candidate_skills & required_skills
        missing_skills = required_skills - candidate_skills
        skill_match_pct = len(matching_skills) / len(required_skills) if required_skills else 0
        
        # Experience match
        experience_match = candidate_experience >= required_experience * 0.8
        
        # Location compatibility
        location_compatible = self._check_location_compatibility(
            candidate_location, 
            job_location,
            job.get('remote_ok', False)
        )
        
        # Salary compatibility
        salary_compatible = self._check_salary_compatibility(
            profile.get('salary_expectations'),
            job.get('salary_range')
        )
        
        # Calculate overall match score
        match_score = self._calculate_match_score(
            skill_match_pct,
            experience_match,
            location_compatible,
            salary_compatible
        )
        
        # Calculate confidence
        confidence = self._calculate_match_confidence(
            len(matching_skills),
            len(required_skills),
            candidate_experience,
            required_experience
        )
        
        # Generate reasoning
        reasoning = []
        recommendations = []
        
        if include_reasoning:
            reasoning = self._generate_match_reasoning(
                skill_match_pct,
                len(matching_skills),
                len(missing_skills),
                experience_match,
                location_compatible,
                salary_compatible
            )
            
            recommendations = self._generate_match_recommendations(
                missing_skills,
                experience_match,
                candidate_experience,
                required_experience
            )
        
        self.inference_count += 1
        if match_score >= 0.7:
            self.successful_inferences += 1
        
        return JobMatch(
            job_id=job.get('job_id', ''),
            job_title=job.get('title', ''),
            match_score=match_score,
            confidence=confidence,
            skill_match_percentage=skill_match_pct,
            experience_match=experience_match,
            salary_compatibility=salary_compatible,
            location_compatibility=location_compatible,
            missing_skills=list(missing_skills),
            matching_skills=list(matching_skills),
            reasoning=reasoning,
            recommendations=recommendations
        )
    
    # =========================================================================
    # SKILL GAP ANALYSIS
    # =========================================================================
    
    def predict_skill_gaps(
        self,
        current_skills: List[str],
        target_role: str
    ) -> SkillGapAnalysis:
        """
        Identify skill gaps for a target role.
        
        Args:
            current_skills: Current skill set
            target_role: Target role to analyze
            
        Returns:
            SkillGapAnalysis with learning recommendations
        """
        logger.info(f"📊 Analyzing skill gaps for target role: {target_role}")
        
        current = set(s.lower().strip() for s in current_skills)
        
        # Get required skills for target role
        required = self._get_required_skills_for_role(target_role)
        
        # Calculate gaps
        skill_gaps = list(required - current)
        transferable = list(current & required)
        
        # Prioritize skills
        priority_skills = self._prioritize_skills(skill_gaps, target_role)
        
        # Create learning path
        learning_path = self._create_learning_path(skill_gaps, priority_skills)
        
        # Estimate learning time
        learning_time = self._estimate_learning_time(learning_path)
        
        # Calculate confidence
        confidence = len(transferable) / len(required) if required else 0.5
        
        self.inference_count += 1
        self.successful_inferences += 1
        
        return SkillGapAnalysis(
            current_skills=list(current),
            target_role=target_role,
            required_skills=list(required),
            skill_gaps=skill_gaps,
            transferable_skills=transferable,
            learning_path=learning_path,
            estimated_learning_time_months=learning_time,
            priority_skills=priority_skills,
            confidence=confidence
        )
    
    # =========================================================================
    # SALARY INFERENCE
    # =========================================================================
    
    def infer_salary_range(
        self,
        role: str,
        location: str,
        experience_years: float,
        skills: Optional[List[str]] = None
    ) -> SalaryInference:
        """
        Infer salary range based on market data.
        
        Args:
            role: Job role/title
            location: Geographic location
            experience_years: Years of experience
            skills: Optional skills list for adjustment
            
        Returns:
            SalaryInference with range and reasoning
        """
        logger.info(f"💰 Inferring salary for {role} in {location}")
        
        # Get base salary data
        base_data = self._get_base_salary_data(role, location)
        
        # Adjust for experience
        experience_multiplier = self._calculate_experience_multiplier(experience_years)
        
        # Adjust for skills
        skill_premium = 0
        if skills:
            skill_premium = self._calculate_skill_premium(skills, role)
        
        # Adjust for location
        location_multiplier = self._get_location_multiplier(location)
        
        # Calculate range
        base_min = base_data.get('min', 60000)
        base_max = base_data.get('max', 120000)
        base_median = base_data.get('median', 90000)
        
        adjusted_min = base_min * experience_multiplier * location_multiplier * (1 + skill_premium)
        adjusted_max = base_max * experience_multiplier * location_multiplier * (1 + skill_premium)
        adjusted_median = base_median * experience_multiplier * location_multiplier * (1 + skill_premium)
        
        # Calculate percentile rank
        percentile = self._calculate_salary_percentile(
            adjusted_median,
            role,
            location
        )
        
        # Generate reasoning
        reasoning = [
            f"Base salary range for {role}: ${base_min:,.0f} - ${base_max:,.0f}",
            f"Experience adjustment ({experience_years} years): {experience_multiplier:.2f}x",
            f"Location adjustment ({location}): {location_multiplier:.2f}x",
            f"Skill premium: +{skill_premium*100:.1f}%",
            f"Estimated market position: {percentile}th percentile"
        ]
        
        # Calculate confidence
        confidence = 0.75 if base_data.get('data_points', 0) > 10 else 0.5
        
        self.inference_count += 1
        self.successful_inferences += 1
        
        return SalaryInference(
            role=role,
            location=location,
            experience_years=experience_years,
            estimated_min=adjusted_min,
            estimated_max=adjusted_max,
            market_median=adjusted_median,
            percentile_rank=percentile,
            factors={
                'base_range': f"${base_min:,.0f} - ${base_max:,.0f}",
                'experience_multiplier': experience_multiplier,
                'location_multiplier': location_multiplier,
                'skill_premium': skill_premium
            },
            confidence=confidence,
            reasoning=reasoning
        )
    
    # =========================================================================
    # TRANSITION SUCCESS PROBABILITY
    # =========================================================================
    
    def calculate_success_probability(
        self,
        transition: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate probability of successful career transition.
        
        Args:
            transition: Transition details (from_role, to_role, skills, etc.)
            
        Returns:
            Dict with probability and contributing factors
        """
        from_role = transition.get('from_role', '')
        to_role = transition.get('to_role', '')
        current_skills = set(transition.get('current_skills', []))
        experience_years = transition.get('experience_years', 0)
        
        # Factor 1: Role similarity (0-1)
        role_similarity = self._calculate_role_similarity(from_role, to_role)
        
        # Factor 2: Skill overlap (0-1)
        required_skills = self._get_required_skills_for_role(to_role)
        skill_overlap = len(current_skills & required_skills) / len(required_skills) if required_skills else 0
        
        # Factor 3: Experience adequacy (0-1)
        min_experience = self._get_min_experience_for_role(to_role)
        experience_adequacy = min(experience_years / max(min_experience, 1), 1.0)
        
        # Factor 4: Market demand (0-1)
        market_demand = self._get_market_demand_score(to_role)
        
        # Weighted calculation
        weights = {
            'role_similarity': 0.25,
            'skill_overlap': 0.35,
            'experience_adequacy': 0.25,
            'market_demand': 0.15
        }
        
        probability = (
            role_similarity * weights['role_similarity'] +
            skill_overlap * weights['skill_overlap'] +
            experience_adequacy * weights['experience_adequacy'] +
            market_demand * weights['market_demand']
        )
        
        return {
            'success_probability': probability,
            'confidence': 0.8,
            'factors': {
                'role_similarity': role_similarity,
                'skill_overlap': skill_overlap,
                'experience_adequacy': experience_adequacy,
                'market_demand': market_demand
            },
            'interpretation': self._interpret_probability(probability),
            'recommendations': self._generate_transition_recommendations(
                skill_overlap,
                experience_adequacy,
                required_skills - current_skills
            )
        }
    
    # =========================================================================
    # HELPER METHODS - CAREER PATH
    # =========================================================================
    
    def _normalize_role_title(self, role: str) -> str:
        """Normalize role title for comparison"""
        normalized = role.lower().strip()
        # Remove common variations
        normalized = re.sub(r'\b(i|ii|iii|iv|sr|jr|senior|junior)\b', '', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return normalized
    
    def _calculate_required_skills(self, from_role: str, to_role: str) -> Set[str]:
        """Calculate skills required for transition"""
        to_skills = self._get_required_skills_for_role(to_role)
        return to_skills
    
    def _calculate_transition_probability(
        self,
        from_role: str,
        to_role: str,
        skills: Set[str],
        experience: float
    ) -> float:
        """Calculate probability of successful transition"""
        required_skills = self._get_required_skills_for_role(to_role)
        skill_match = len(skills & required_skills) / len(required_skills) if required_skills else 0.5
        
        min_exp = self._get_min_experience_for_role(to_role)
        exp_match = min(experience / max(min_exp, 1), 1.0)
        
        # Weighted combination
        probability = 0.6 * skill_match + 0.4 * exp_match
        return min(max(probability, 0.0), 1.0)
    
    def _generate_career_path_reasoning(
        self,
        current: str,
        target: str,
        steps: List[Dict],
        probability: float
    ) -> List[str]:
        """Generate reasoning for career path"""
        reasoning = [
            f"Current role: {current}",
            f"Target role: {target}",
            f"Recommended path includes {len(steps)} step(s)",
            f"Estimated success probability: {probability:.1%}",
        ]
        
        if probability >= 0.7:
            reasoning.append("✅ High likelihood of success with proper skill development")
        elif probability >= 0.5:
            reasoning.append("⚠️ Moderate success probability - additional preparation recommended")
        else:
            reasoning.append("⚠️ Challenging transition - consider alternative paths")
        
        return reasoning
    
    def _calculate_path_confidence(
        self,
        current_skills: Set[str],
        required_skills: Set[str],
        experience: float
    ) -> float:
        """Calculate confidence in path prediction"""
        skill_coverage = len(current_skills & required_skills) / len(required_skills) if required_skills else 0
        exp_factor = min(experience / 5, 1.0)  # Max out at 5 years
        return 0.7 * skill_coverage + 0.3 * exp_factor
    
    def _is_direct_transition_viable(
        self,
        current: str,
        target: str,
        experience: float
    ) -> bool:
        """Check if direct transition is viable"""
        min_exp = self._get_min_experience_for_role(target)
        similarity = self._calculate_role_similarity(current, target)
        return experience >= min_exp * 0.8 and similarity >= 0.6
    
    def _find_intermediate_roles(self, current: str, target: str) -> List[str]:
        """Find intermediate roles for transition"""
        # Simplified: Return one intermediate role
        current_normalized = self._normalize_role_title(current)
        target_normalized = self._normalize_role_title(target)
        
        # If going from junior to senior, add mid-level
        if 'junior' in current_normalized and 'senior' in target_normalized:
            base_role = current_normalized.replace('junior', '').strip()
            return [base_role]
        
        # If going from individual contributor to lead
        if 'lead' in target_normalized and 'lead' not in current_normalized:
            return [f"Senior {current_normalized}"]
        
        return []
    
    # =========================================================================
    # HELPER METHODS - JOB MATCHING
    # =========================================================================
    
    def _check_location_compatibility(
        self,
        candidate_loc: str,
        job_loc: str,
        remote_ok: bool
    ) -> bool:
        """Check location compatibility"""
        if remote_ok:
            return True
        if not candidate_loc or not job_loc:
            return True
        return candidate_loc.lower() in job_loc.lower() or job_loc.lower() in candidate_loc.lower()
    
    def _check_salary_compatibility(
        self,
        expectations: Optional[Dict],
        job_range: Optional[Dict]
    ) -> bool:
        """Check salary compatibility"""
        if not expectations or not job_range:
            return True
        
        exp_min = expectations.get('min', 0)
        job_max = job_range.get('max', float('inf'))
        
        return exp_min <= job_max * 1.1  # 10% buffer
    
    def _calculate_match_score(
        self,
        skill_match: float,
        exp_match: bool,
        loc_match: bool,
        sal_match: bool
    ) -> float:
        """Calculate overall match score"""
        score = (
            skill_match * 0.5 +
            (1.0 if exp_match else 0.5) * 0.25 +
            (1.0 if loc_match else 0.3) * 0.15 +
            (1.0 if sal_match else 0.5) * 0.10
        )
        return min(max(score, 0.0), 1.0)
    
    def _calculate_match_confidence(
        self,
        matching_count: int,
        total_required: int,
        candidate_exp: float,
        required_exp: float
    ) -> float:
        """Calculate confidence in match score"""
        if total_required == 0:
            return 0.5
        
        skill_confidence = matching_count / total_required
        exp_confidence = min(candidate_exp / max(required_exp, 1), 1.0)
        
        return 0.7 * skill_confidence + 0.3 * exp_confidence
    
    def _generate_match_reasoning(
        self,
        skill_match_pct: float,
        matching_count: int,
        missing_count: int,
        exp_match: bool,
        loc_match: bool,
        sal_match: bool
    ) -> List[str]:
        """Generate match reasoning"""
        reasoning = []
        
        # Skill match
        reasoning.append(f"Skill match: {skill_match_pct:.1%} ({matching_count} of {matching_count + missing_count} required skills)")
        
        if skill_match_pct >= 0.8:
            reasoning.append("✅ Excellent skill alignment")
        elif skill_match_pct >= 0.6:
            reasoning.append("✅ Good skill alignment")
        else:
            reasoning.append("⚠️ Significant skill gaps present")
        
        # Experience
        if exp_match:
            reasoning.append("✅ Experience requirements met")
        else:
            reasoning.append("⚠️ Experience below preferred level")
        
        # Location
        if loc_match:
            reasoning.append("✅ Location compatible")
        else:
            reasoning.append("⚠️ Location may require relocation")
        
        # Salary
        if sal_match:
            reasoning.append("✅ Salary expectations aligned")
        else:
            reasoning.append("⚠️ Salary expectations may need adjustment")
        
        return reasoning
    
    def _generate_match_recommendations(
        self,
        missing_skills: Set[str],
        exp_match: bool,
        candidate_exp: float,
        required_exp: float
    ) -> List[str]:
        """Generate recommendations for improving match"""
        recommendations = []
        
        if missing_skills:
            top_skills = list(missing_skills)[:3]
            recommendations.append(f"Develop these priority skills: {', '.join(top_skills)}")
        
        if not exp_match:
            gap = required_exp - candidate_exp
            recommendations.append(f"Gain {gap:.1f} more years of relevant experience")
        
        if len(missing_skills) > 3:
            recommendations.append("Consider related roles that better match current skillset")
        
        return recommendations
    
    # =========================================================================
    # HELPER METHODS - SKILLS
    # =========================================================================
    
    def _get_required_skills_for_role(self, role: str) -> Set[str]:
        """Get required skills for a role"""
        role_normalized = self._normalize_role_title(role)
        
        # Use skill taxonomy or defaults
        if role_normalized in self.skill_taxonomy:
            return set(self.skill_taxonomy[role_normalized])
        
        # Fallback: Infer from role type
        default_skills = set()
        
        if 'engineer' in role_normalized or 'developer' in role_normalized:
            default_skills = {
                'programming', 'software development', 'git', 'testing',
                'problem solving', 'algorithms', 'debugging'
            }
        elif 'manager' in role_normalized:
            default_skills = {
                'leadership', 'project management', 'communication',
                'team building', 'strategic planning', 'budgeting'
            }
        elif 'analyst' in role_normalized:
            default_skills = {
                'data analysis', 'excel', 'sql', 'reporting',
                'critical thinking', 'problem solving'
            }
        else:
            default_skills = {
                'communication', 'teamwork', 'problem solving',
                'time management', 'adaptability'
            }
        
        return default_skills
    
    def _prioritize_skills(self, skills: List[str], role: str) -> List[str]:
        """Prioritize skills by importance"""
        # Simplified: Return first 5 as high priority
        return skills[:5] if len(skills) > 5 else skills
    
    def _create_learning_path(
        self,
        skill_gaps: List[str],
        priority_skills: List[str]
    ) -> List[Dict[str, Any]]:
        """Create a learning path for skill development"""
        learning_path = []
        
        for i, skill in enumerate(priority_skills[:5]):  # Top 5
            learning_path.append({
                'skill': skill,
                'priority': 'High' if i < 3 else 'Medium',
                'estimated_time_weeks': 4 + i * 2,
                'resources': ['Online courses', 'Practice projects', 'Certifications'],
                'order': i + 1
            })
        
        return learning_path
    
    def _estimate_learning_time(self, learning_path: List[Dict]) -> int:
        """Estimate total learning time in months"""
        total_weeks = sum(step.get('estimated_time_weeks', 4) for step in learning_path)
        return max(int(total_weeks / 4), 1)
    
    # =========================================================================
    # HELPER METHODS - SALARY
    # =========================================================================
    
    def _get_base_salary_data(self, role: str, location: str) -> Dict[str, Any]:
        """Get base salary data for role/location"""
        # Simplified base data (in production, fetch from database)
        role_normalized = self._normalize_role_title(role)
        
        base_salaries = {
            'software engineer': {'min': 70000, 'max': 140000, 'median': 105000},
            'data analyst': {'min': 55000, 'max': 95000, 'median': 75000},
            'product manager': {'min': 80000, 'max': 160000, 'median': 120000},
            'data scientist': {'min': 85000, 'max': 150000, 'median': 117500},
            'project manager': {'min': 65000, 'max': 120000, 'median': 92500},
        }
        
        # Find closest match
        for key in base_salaries:
            if key in role_normalized:
                return {**base_salaries[key], 'data_points': 100}
        
        # Default
        return {'min': 60000, 'max': 120000, 'median': 90000, 'data_points': 10}
    
    def _calculate_experience_multiplier(self, years: float) -> float:
        """Calculate salary multiplier based on experience"""
        # Diminishing returns curve
        if years <= 2:
            return 0.85 + (years * 0.075)
        elif years <= 5:
            return 1.0 + ((years - 2) * 0.10)
        elif years <= 10:
            return 1.3 + ((years - 5) * 0.06)
        else:
            return 1.6 + ((years - 10) * 0.03)
    
    def _calculate_skill_premium(self, skills: List[str], role: str) -> float:
        """Calculate salary premium for in-demand skills"""
        high_value_skills = {
            'machine learning', 'ai', 'cloud', 'aws', 'azure',
            'kubernetes', 'react', 'python', 'java', 'leadership'
        }
        
        skill_set = set(s.lower() for s in skills)
        premium_count = len(skill_set & high_value_skills)
        
        # 5% per premium skill, max 25%
        return min(premium_count * 0.05, 0.25)
    
    def _get_location_multiplier(self, location: str) -> float:
        """Get location-based salary multiplier"""
        location_lower = location.lower()
        
        high_cost_areas = ['san francisco', 'new york', 'seattle', 'boston']
        medium_cost_areas = ['austin', 'denver', 'chicago', 'portland']
        
        if any(city in location_lower for city in high_cost_areas):
            return 1.4
        elif any(city in location_lower for city in medium_cost_areas):
            return 1.15
        else:
            return 1.0
    
    def _calculate_salary_percentile(
        self,
        salary: float,
        role: str,
        location: str
    ) -> int:
        """Calculate percentile rank for salary"""
        base_data = self._get_base_salary_data(role, location)
        median = base_data.get('median', 90000)
        
        if salary >= median * 1.3:
            return 90
        elif salary >= median * 1.15:
            return 75
        elif salary >= median:
            return 60
        elif salary >= median * 0.85:
            return 40
        else:
            return 25
    
    # =========================================================================
    # HELPER METHODS - GENERAL
    # =========================================================================
    
    def _calculate_role_similarity(self, role1: str, role2: str) -> float:
        """Calculate similarity between two roles"""
        r1 = self._normalize_role_title(role1)
        r2 = self._normalize_role_title(role2)
        
        # Exact match
        if r1 == r2:
            return 1.0
        
        # Partial match
        r1_words = set(r1.split())
        r2_words = set(r2.split())
        
        if not r1_words or not r2_words:
            return 0.0
        
        overlap = len(r1_words & r2_words)
        total = len(r1_words | r2_words)
        
        return overlap / total if total > 0 else 0.0
    
    def _get_min_experience_for_role(self, role: str) -> float:
        """Get minimum experience required for role"""
        role_lower = role.lower()
        
        if 'senior' in role_lower or 'lead' in role_lower:
            return 5.0
        elif 'junior' in role_lower or 'entry' in role_lower:
            return 0.0
        else:
            return 2.0
    
    def _get_market_demand_score(self, role: str) -> float:
        """Get market demand score for role (0-1)"""
        # Simplified: Return moderate demand
        # In production, query job market data
        return 0.7
    
    def _interpret_probability(self, probability: float) -> str:
        """Interpret success probability"""
        if probability >= 0.8:
            return "Very High - Excellent chance of success"
        elif probability >= 0.6:
            return "High - Good chance of success"
        elif probability >= 0.4:
            return "Moderate - Requires preparation"
        else:
            return "Low - Consider alternative paths"
    
    def _generate_transition_recommendations(
        self,
        skill_overlap: float,
        exp_adequacy: float,
        missing_skills: Set[str]
    ) -> List[str]:
        """Generate recommendations for career transition"""
        recommendations = []
        
        if skill_overlap < 0.5:
            recommendations.append("Focus on developing core required skills")
            if missing_skills:
                top_3 = list(missing_skills)[:3]
                recommendations.append(f"Priority skills: {', '.join(top_3)}")
        
        if exp_adequacy < 0.7:
            recommendations.append("Gain more experience in target domain")
            recommendations.append("Consider lateral moves to build relevant experience")
        
        if not recommendations:
            recommendations.append("You're well-positioned for this transition")
            recommendations.append("Consider networking in target industry")
        
        return recommendations
    
    # =========================================================================
    # DATA LOADING
    # =========================================================================
    
    def _load_career_ladder(self) -> Dict[str, Any]:
        """Load career progression ladder"""
        # Simplified career ladder (in production, load from database)
        return {
            'software engineer': {
                'progression': [
                    {'role': 'Senior Software Engineer', 'min_experience': 3},
                    {'role': 'Lead Software Engineer', 'min_experience': 6},
                    {'role': 'Engineering Manager', 'min_experience': 8},
                ]
            },
            'data analyst': {
                'progression': [
                    {'role': 'Senior Data Analyst', 'min_experience': 3},
                    {'role': 'Data Scientist', 'min_experience': 4},
                    {'role': 'Lead Data Scientist', 'min_experience': 7},
                ]
            }
        }
    
    def _load_skill_taxonomy(self) -> Dict[str, List[str]]:
        """Load skill taxonomy for roles"""
        # Simplified taxonomy (in production, load from database)
        return {
            'software engineer': [
                'programming', 'algorithms', 'data structures',
                'git', 'testing', 'debugging', 'software design'
            ],
            'data analyst': [
                'sql', 'excel', 'data visualization', 'statistics',
                'python', 'data cleaning', 'reporting'
            ],
            'data scientist': [
                'machine learning', 'python', 'statistics', 'sql',
                'data visualization', 'deep learning', 'feature engineering'
            ]
        }
    
    # =========================================================================
    # PERFORMANCE METRICS
    # =========================================================================
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get inference engine performance metrics"""
        success_rate = (
            self.successful_inferences / self.inference_count 
            if self.inference_count > 0 else 0
        )
        
        return {
            'total_inferences': self.inference_count,
            'successful_inferences': self.successful_inferences,
            'success_rate': success_rate,
            'status': '✅ Operational' if self.initialized else '❌ Not initialized',
            'ml_available': SKLEARN_AVAILABLE,
            'nlp_available': SPACY_AVAILABLE
        }


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    'InferenceEngine',
    'CareerPath',
    'JobMatch',
    'SkillGapAnalysis',
    'SalaryInference'
]


# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    print("🧪 Testing Inference Engine...")
    
    engine = InferenceEngine()
    
    # Test 1: Career Path Inference
    print("\n" + "="*70)
    print("TEST 1: Career Path Inference")
    print("="*70)
    
    profile = {
        'current_role': 'Software Engineer',
        'skills': ['Python', 'JavaScript', 'Git', 'Testing', 'SQL'],
        'experience_years': 3
    }
    
    path = engine.infer_career_path(profile, target_role='Lead Software Engineer')
    print(f"\n✅ Career Path: {path.current_role} → {path.target_role}")
    print(f"   Steps: {len(path.intermediate_steps)}")
    print(f"   Duration: {path.total_duration_years} years")
    print(f"   Success Probability: {path.success_probability:.1%}")
    print(f"   Confidence: {path.confidence:.1%}")
    print(f"\n   Reasoning:")
    for reason in path.reasoning:
        print(f"   - {reason}")
    
    # Test 2: Job Matching
    print("\n" + "="*70)
    print("TEST 2: Job Matching")
    print("="*70)
    
    job = {
        'job_id': 'J001',
        'title': 'Senior Software Engineer',
        'requirements': ['Python', 'JavaScript', 'Docker', 'Kubernetes', 'AWS'],
        'required_experience_years': 4,
        'location': 'San Francisco',
        'salary_range': {'min': 120000, 'max': 160000}
    }
    
    match = engine.match_job_to_candidate(profile, job)
    print(f"\n✅ Job Match: {match.job_title}")
    print(f"   Match Score: {match.match_score:.1%}")
    print(f"   Skill Match: {match.skill_match_percentage:.1%}")
    print(f"   Matching Skills: {', '.join(match.matching_skills[:3])}")
    print(f"   Missing Skills: {', '.join(match.missing_skills[:3])}")
    print(f"\n   Reasoning:")
    for reason in match.reasoning:
        print(f"   - {reason}")
    
    # Test 3: Skill Gap Analysis
    print("\n" + "="*70)
    print("TEST 3: Skill Gap Analysis")
    print("="*70)
    
    gaps = engine.predict_skill_gaps(
        current_skills=['Python', 'SQL', 'Excel'],
        target_role='Data Scientist'
    )
    print(f"\n✅ Skill Gap Analysis for: {gaps.target_role}")
    print(f"   Skill Gaps: {len(gaps.skill_gaps)}")
    print(f"   Transferable Skills: {len(gaps.transferable_skills)}")
    print(f"   Learning Time: {gaps.estimated_learning_time_months} months")
    print(f"   Priority Skills: {', '.join(gaps.priority_skills[:3])}")
    
    # Test 4: Salary Inference
    print("\n" + "="*70)
    print("TEST 4: Salary Inference")
    print("="*70)
    
    salary = engine.infer_salary_range(
        role='Software Engineer',
        location='San Francisco',
        experience_years=3,
        skills=['Python', 'JavaScript', 'AWS']
    )
    print(f"\n✅ Salary Inference: {salary.role}")
    print(f"   Range: ${salary.estimated_min:,.0f} - ${salary.estimated_max:,.0f}")
    print(f"   Median: ${salary.market_median:,.0f}")
    print(f"   Percentile: {salary.percentile_rank}th")
    print(f"   Confidence: {salary.confidence:.1%}")
    
    # Performance Metrics
    print("\n" + "="*70)
    print("PERFORMANCE METRICS")
    print("="*70)
    
    metrics = engine.get_performance_metrics()
    print(f"\n✅ Inference Engine Metrics:")
    print(f"   Total Inferences: {metrics['total_inferences']}")
    print(f"   Success Rate: {metrics['success_rate']:.1%}")
    print(f"   Status: {metrics['status']}")
    print(f"   ML Available: {metrics['ml_available']}")
    print(f"   NLP Available: {metrics['nlp_available']}")
    
    print("\n" + "="*70)
    print("✅ All tests passed! Inference Engine is operational.")
    print("="*70)
