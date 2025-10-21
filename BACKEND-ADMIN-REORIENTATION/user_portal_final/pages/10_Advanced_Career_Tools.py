"""
🛠️ IntelliCV User Portal - Advanced Career Tools Suite
=====================================================

Comprehensive career development toolkit featuring:
- Salary evaluation and negotiation tools
- Market intelligence and industry insights
- Skills gap analysis and learning paths
- Career transition planning
- Job market forecasting and trends
- Professional brand optimization

Integrated from frontend advanced tools and intelligence modules
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import time
import random

# Page configuration
st.set_page_config(
    page_title="Advanced Career Tools | IntelliCV",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class SalaryIntelligenceEngine:
    """Advanced salary analysis and market intelligence system"""
    
    def __init__(self):
        self.salary_data = self._load_salary_data()
        self.market_trends = self._load_market_trends()
        self.negotiation_insights = self._load_negotiation_data()
        
    def _load_salary_data(self) -> Dict[str, Any]:
        """Load comprehensive salary and compensation data"""
        return {
            "roles": {
                "Software Engineer": {
                    "levels": {
                        "Junior (0-2 years)": {"min": 70000, "median": 85000, "max": 105000, "equity": "0.1-0.5%"},
                        "Mid-Level (2-5 years)": {"min": 100000, "median": 120000, "max": 150000, "equity": "0.2-1.0%"},
                        "Senior (5-8 years)": {"min": 140000, "median": 170000, "max": 220000, "equity": "0.5-2.0%"},
                        "Staff/Principal (8+ years)": {"min": 200000, "median": 280000, "max": 400000, "equity": "1.0-5.0%"}
                    },
                    "by_location": {
                        "San Francisco, CA": {"multiplier": 1.4, "cost_of_living": 1.8},
                        "New York, NY": {"multiplier": 1.3, "cost_of_living": 1.6},
                        "Seattle, WA": {"multiplier": 1.2, "cost_of_living": 1.3},
                        "Austin, TX": {"multiplier": 1.1, "cost_of_living": 1.1},
                        "Remote": {"multiplier": 1.0, "cost_of_living": 1.0}
                    },
                    "by_company_size": {
                        "Startup (1-50)": {"multiplier": 0.8, "equity_upside": "High"},
                        "Scale-up (51-500)": {"multiplier": 0.9, "equity_upside": "Medium"},
                        "Mid-size (501-5000)": {"multiplier": 1.0, "equity_upside": "Low"},
                        "Enterprise (5000+)": {"multiplier": 1.2, "equity_upside": "Very Low"}
                    }
                },
                "Data Scientist": {
                    "levels": {
                        "Junior (0-2 years)": {"min": 80000, "median": 95000, "max": 120000, "equity": "0.1-0.5%"},
                        "Mid-Level (2-5 years)": {"min": 115000, "median": 135000, "max": 170000, "equity": "0.2-1.0%"},
                        "Senior (5-8 years)": {"min": 155000, "median": 185000, "max": 240000, "equity": "0.5-2.0%"},
                        "Principal/Staff (8+ years)": {"min": 220000, "median": 300000, "max": 450000, "equity": "1.0-5.0%"}
                    },
                    "by_location": {
                        "San Francisco, CA": {"multiplier": 1.5, "cost_of_living": 1.8},
                        "New York, NY": {"multiplier": 1.3, "cost_of_living": 1.6},
                        "Seattle, WA": {"multiplier": 1.2, "cost_of_living": 1.3},
                        "Boston, MA": {"multiplier": 1.15, "cost_of_living": 1.4},
                        "Remote": {"multiplier": 1.0, "cost_of_living": 1.0}
                    }
                },
                "Product Manager": {
                    "levels": {
                        "Associate PM (0-2 years)": {"min": 90000, "median": 110000, "max": 140000, "equity": "0.1-0.5%"},
                        "Product Manager (2-5 years)": {"min": 130000, "median": 155000, "max": 190000, "equity": "0.2-1.0%"},
                        "Senior PM (5-8 years)": {"min": 170000, "median": 210000, "max": 270000, "equity": "0.5-2.0%"},
                        "Principal/Director (8+ years)": {"min": 250000, "median": 350000, "max": 500000, "equity": "1.0-8.0%"}
                    }
                }
            },
            "benefits_benchmarks": {
                "health_insurance": {"employer_coverage": "80-100%", "value": "$8000-15000/year"},
                "retirement_401k": {"match": "3-6%", "vesting": "Immediate to 4 years"},
                "pto_vacation": {"days": "15-25 days", "unlimited": "35% of companies"},
                "learning_budget": {"amount": "$1000-5000/year", "availability": "70% of companies"},
                "remote_work": {"full_remote": "40%", "hybrid": "45%", "office_only": "15%"}
            }
        }
    
    def _load_market_trends(self) -> Dict[str, Any]:
        """Load salary and hiring trends data"""
        return {
            "salary_growth": {
                "2024": {"software_engineer": 8.5, "data_scientist": 12.3, "product_manager": 6.2},
                "2023": {"software_engineer": 5.1, "data_scientist": 15.7, "product_manager": 4.8},
                "2022": {"software_engineer": 12.4, "data_scientist": 18.2, "product_manager": 9.1}
            },
            "hiring_trends": {
                "hot_skills": [
                    {"skill": "AI/Machine Learning", "demand_increase": "+45%", "salary_premium": "+25%"},
                    {"skill": "Cloud Architecture", "demand_increase": "+32%", "salary_premium": "+18%"},
                    {"skill": "DevOps/SRE", "demand_increase": "+28%", "salary_premium": "+15%"},
                    {"skill": "Product Management", "demand_increase": "+22%", "salary_premium": "+12%"},
                    {"skill": "Cybersecurity", "demand_increase": "+38%", "salary_premium": "+20%"}
                ],
                "market_conditions": {
                    "competition_level": "High",
                    "time_to_hire": "45-60 days",
                    "offer_acceptance_rate": "68%",
                    "counter_offer_frequency": "35%"
                }
            }
        }
    
    def _load_negotiation_data(self) -> Dict[str, Any]:
        """Load salary negotiation insights and strategies"""
        return {
            "negotiation_success_rates": {
                "salary_increase": {"attempt_rate": "68%", "success_rate": "85%", "avg_increase": "12%"},
                "signing_bonus": {"attempt_rate": "35%", "success_rate": "65%", "avg_amount": "$8500"},
                "equity_increase": {"attempt_rate": "28%", "success_rate": "45%", "avg_increase": "25%"},
                "flexible_work": {"attempt_rate": "45%", "success_rate": "78%"}
            },
            "timing_insights": {
                "best_times": ["End of fiscal year", "After performance reviews", "During job transitions"],
                "worst_times": ["Beginning of fiscal year", "During hiring freezes", "Economic downturns"]
            }
        }
    
    def calculate_salary_estimate(self, role: str, experience: str, location: str, company_size: str) -> Dict[str, Any]:
        """Calculate personalized salary estimate"""
        
        if role not in self.salary_data["roles"]:
            role = "Software Engineer"  # Default fallback
        
        role_data = self.salary_data["roles"][role]
        
        # Base salary from experience level
        if experience not in role_data["levels"]:
            experience = list(role_data["levels"].keys())[0]  # Default to first level
        
        base_salary = role_data["levels"][experience]
        
        # Apply location multiplier
        location_multiplier = 1.0
        cost_of_living = 1.0
        if "by_location" in role_data and location in role_data["by_location"]:
            location_data = role_data["by_location"][location]
            location_multiplier = location_data["multiplier"]
            cost_of_living = location_data["cost_of_living"]
        
        # Apply company size multiplier
        company_multiplier = 1.0
        equity_upside = "Medium"
        if "by_company_size" in role_data and company_size in role_data["by_company_size"]:
            company_data = role_data["by_company_size"][company_size]
            company_multiplier = company_data["multiplier"]
            equity_upside = company_data["equity_upside"]
        
        # Calculate adjusted salary ranges
        adjusted_min = int(base_salary["min"] * location_multiplier * company_multiplier)
        adjusted_median = int(base_salary["median"] * location_multiplier * company_multiplier)
        adjusted_max = int(base_salary["max"] * location_multiplier * company_multiplier)
        
        # Calculate real purchasing power
        real_min = int(adjusted_min / cost_of_living)
        real_median = int(adjusted_median / cost_of_living)
        real_max = int(adjusted_max / cost_of_living)
        
        return {
            "base_range": base_salary,
            "adjusted_range": {
                "min": adjusted_min,
                "median": adjusted_median,
                "max": adjusted_max,
                "equity": base_salary["equity"]
            },
            "real_purchasing_power": {
                "min": real_min,
                "median": real_median,
                "max": real_max
            },
            "location_factor": location_multiplier,
            "company_factor": company_multiplier,
            "cost_of_living": cost_of_living,
            "equity_upside": equity_upside
        }

class SkillsGapAnalyzer:
    """Analyzes skill gaps and creates learning paths"""
    
    def __init__(self):
        self.skill_data = self._load_skill_requirements()
        self.learning_paths = self._load_learning_paths()
        
    def _load_skill_requirements(self) -> Dict[str, Any]:
        """Load current skill requirements by role"""
        return {
            "Software Engineer": {
                "core_technical": ["Programming Languages", "Data Structures", "Algorithms", "System Design"],
                "frameworks_tools": ["Git/Version Control", "CI/CD", "Cloud Platforms", "Databases"],
                "soft_skills": ["Problem Solving", "Communication", "Teamwork", "Time Management"],
                "emerging_skills": ["AI/ML Basics", "Containerization", "Microservices", "Security"]
            },
            "Data Scientist": {
                "core_technical": ["Statistics", "Machine Learning", "Programming", "Data Analysis"],
                "frameworks_tools": ["Python/R", "SQL", "Visualization Tools", "ML Frameworks"],
                "soft_skills": ["Business Acumen", "Communication", "Critical Thinking", "Presentation"],
                "emerging_skills": ["MLOps", "Deep Learning", "NLP", "Computer Vision"]
            },
            "Product Manager": {
                "core_technical": ["Analytics", "A/B Testing", "Basic Technical Knowledge", "Data Analysis"],
                "frameworks_tools": ["Project Management", "Design Tools", "Analytics Platforms", "Roadmapping"],
                "soft_skills": ["Leadership", "Communication", "Strategic Thinking", "Customer Empathy"],
                "emerging_skills": ["AI Product Management", "Growth Hacking", "UX Research", "Agile/Scrum"]
            }
        }
    
    def _load_learning_paths(self) -> Dict[str, List[Dict]]:
        """Load recommended learning paths for skill development"""
        return {
            "AI/ML Basics": [
                {"course": "Machine Learning Fundamentals", "provider": "Coursera", "duration": "6 weeks", "cost": "$49/month"},
                {"course": "Python for Data Science", "provider": "DataCamp", "duration": "4 weeks", "cost": "$29/month"},
                {"course": "Statistics for ML", "provider": "Khan Academy", "duration": "3 weeks", "cost": "Free"}
            ],
            "Cloud Platforms": [
                {"course": "AWS Cloud Practitioner", "provider": "AWS", "duration": "8 weeks", "cost": "$100"},
                {"course": "Azure Fundamentals", "provider": "Microsoft", "duration": "6 weeks", "cost": "Free"},
                {"course": "Google Cloud Essentials", "provider": "Google", "duration": "4 weeks", "cost": "Free"}
            ],
            "System Design": [
                {"course": "Designing Data-Intensive Applications", "provider": "Book", "duration": "12 weeks", "cost": "$45"},
                {"course": "System Design Interview", "provider": "Educative", "duration": "8 weeks", "cost": "$79/year"},
                {"course": "Scalability Patterns", "provider": "Pluralsight", "duration": "6 weeks", "cost": "$29/month"}
            ]
        }

class CareerTransitionPlanner:
    """Plans career transitions and pathway optimization"""
    
    def __init__(self):
        self.transition_data = self._load_transition_data()
        
    def _load_transition_data(self) -> Dict[str, Any]:
        """Load career transition patterns and success rates"""
        return {
            "common_transitions": {
                "Software Engineer": [
                    {"to": "Senior Engineer", "timeline": "2-3 years", "success_rate": "85%", "key_skills": ["Leadership", "System Design"]},
                    {"to": "Engineering Manager", "timeline": "3-5 years", "success_rate": "60%", "key_skills": ["People Management", "Project Management"]},
                    {"to": "Product Manager", "timeline": "1-2 years", "success_rate": "45%", "key_skills": ["Business Acumen", "User Research"]},
                    {"to": "Data Scientist", "timeline": "6-12 months", "success_rate": "70%", "key_skills": ["Statistics", "ML Algorithms"]}
                ],
                "Data Scientist": [
                    {"to": "Senior Data Scientist", "timeline": "2-3 years", "success_rate": "80%", "key_skills": ["MLOps", "Business Impact"]},
                    {"to": "ML Engineer", "timeline": "6-18 months", "success_rate": "75%", "key_skills": ["Software Engineering", "Production ML"]},
                    {"to": "Product Manager", "timeline": "1-2 years", "success_rate": "55%", "key_skills": ["Product Sense", "Strategy"]},
                    {"to": "Data Science Manager", "timeline": "3-5 years", "success_rate": "50%", "key_skills": ["Team Leadership", "Strategy"]}
                ]
            },
            "transition_strategies": {
                "internal_move": {"timeline": "3-6 months", "success_rate": "70%", "investment": "Low"},
                "new_company": {"timeline": "6-12 months", "success_rate": "60%", "investment": "Medium"},
                "career_change": {"timeline": "12-24 months", "success_rate": "40%", "investment": "High"}
            }
        }

def main():
    """Main application interface"""
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; margin-bottom: 30px;">
        <h1 style="color: white; margin: 0;">🛠️ Advanced Career Tools Suite</h1>
        <p style="color: white; margin: 5px 0 0 0; opacity: 0.9;">
            Comprehensive tools for salary analysis, skill development, and career planning
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize engines
    salary_engine = SalaryIntelligenceEngine()
    skills_analyzer = SkillsGapAnalyzer()
    transition_planner = CareerTransitionPlanner()
    
    # Sidebar navigation
    st.sidebar.markdown("## 🛠️ Career Tools")
    
    tool = st.sidebar.radio(
        "Select Tool:",
        [
            "💰 Salary Intelligence",
            "📊 Skills Gap Analysis", 
            "🚀 Career Transition Planner",
            "📈 Market Intelligence",
            "🎯 Negotiation Advisor",
            "🔮 Future Readiness"
        ]
    )
    
    if tool == "💰 Salary Intelligence":
        st.markdown("## Salary Intelligence & Compensation Analysis")
        
        # Input parameters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            role = st.selectbox(
                "Target Role:",
                ["Software Engineer", "Data Scientist", "Product Manager"]
            )
        
        with col2:
            experience = st.selectbox(
                "Experience Level:",
                ["Junior (0-2 years)", "Mid-Level (2-5 years)", "Senior (5-8 years)", "Staff/Principal (8+ years)"]
            )
        
        with col3:
            location = st.selectbox(
                "Location:",
                ["San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX", "Remote"]
            )
        
        with col4:
            company_size = st.selectbox(
                "Company Size:",
                ["Startup (1-50)", "Scale-up (51-500)", "Mid-size (501-5000)", "Enterprise (5000+)"]
            )
        
        # Calculate salary estimate
        if st.button("🔍 Analyze Compensation", type="primary"):
            estimate = salary_engine.calculate_salary_estimate(role, experience, location, company_size)
            
            # Display results
            st.markdown("### 💼 Compensation Analysis Results")
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Market Median",
                    f"${estimate['adjusted_range']['median']:,}",
                    delta=f"{((estimate['adjusted_range']['median'] / estimate['base_range']['median']) - 1) * 100:+.0f}% vs base"
                )
            
            with col2:
                st.metric(
                    "Salary Range",
                    f"${estimate['adjusted_range']['min']:,} - ${estimate['adjusted_range']['max']:,}"
                )
            
            with col3:
                st.metric(
                    "Real Purchasing Power",
                    f"${estimate['real_purchasing_power']['median']:,}",
                    delta=f"Adjusted for COL"
                )
            
            with col4:
                st.metric(
                    "Equity Range",
                    estimate['adjusted_range']['equity'],
                    delta=f"{estimate['equity_upside']} upside"
                )
            
            # Salary distribution chart
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Create salary range visualization
                fig = go.Figure()
                
                ranges = ["Min", "25th %", "Median", "75th %", "Max"]
                salaries = [
                    estimate['adjusted_range']['min'],
                    estimate['adjusted_range']['min'] + (estimate['adjusted_range']['median'] - estimate['adjusted_range']['min']) * 0.5,
                    estimate['adjusted_range']['median'],
                    estimate['adjusted_range']['median'] + (estimate['adjusted_range']['max'] - estimate['adjusted_range']['median']) * 0.5,
                    estimate['adjusted_range']['max']
                ]
                
                fig.add_trace(go.Bar(
                    x=ranges,
                    y=salaries,
                    marker_color=['lightcoral', 'orange', 'gold', 'lightgreen', 'green'],
                    text=[f"${s:,.0f}" for s in salaries],
                    textposition='auto'
                ))
                
                fig.update_layout(
                    title=f"Salary Distribution: {role} in {location}",
                    yaxis_title="Annual Salary ($)",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 📊 Breakdown Details")
                
                st.write(f"**Location Factor:** {estimate['location_factor']:.1f}x")
                st.write(f"**Company Size Factor:** {estimate['company_factor']:.1f}x")
                st.write(f"**Cost of Living:** {estimate['cost_of_living']:.1f}x")
                
                st.markdown("### 💡 Insights")
                
                if estimate['location_factor'] > 1.2:
                    st.info("🏙️ High-cost location with premium salaries")
                elif estimate['location_factor'] < 0.9:
                    st.info("🏡 Lower cost area, consider remote opportunities")
                
                if estimate['company_factor'] > 1.1:
                    st.success("🏢 Large company premium")
                elif estimate['company_factor'] < 0.9:
                    st.warning("🚀 Startup - lower base but higher equity upside")
            
            # Market comparison
            st.markdown("### 🎯 Market Position Analysis")
            
            # Show salary trends
            trends = salary_engine.market_trends["salary_growth"]
            role_key = role.lower().replace(" ", "_")
            
            if role_key in trends["2024"]:
                growth_2024 = trends["2024"][role_key]
                growth_2023 = trends["2023"][role_key]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        "2024 Growth Rate",
                        f"{growth_2024:.1f}%",
                        delta=f"{growth_2024 - growth_2023:+.1f}% vs 2023"
                    )
                
                with col2:
                    if growth_2024 > 10:
                        st.success("🔥 Hot market with strong growth")
                    elif growth_2024 > 5:
                        st.info("📈 Steady market growth")
                    else:
                        st.warning("📊 Slower growth market")
            
            # Benefits benchmarks
            st.markdown("### 🎁 Benefits Benchmarks")
            
            benefits = salary_engine.salary_data["benefits_benchmarks"]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Health Insurance**")
                st.write(f"Employer Coverage: {benefits['health_insurance']['employer_coverage']}")
                st.write(f"Annual Value: {benefits['health_insurance']['value']}")
            
            with col2:
                st.write("**Retirement (401k)**")
                st.write(f"Company Match: {benefits['retirement_401k']['match']}")
                st.write(f"Vesting: {benefits['retirement_401k']['vesting']}")
            
            with col3:
                st.write("**Time Off**")
                st.write(f"Vacation Days: {benefits['pto_vacation']['days']}")
                st.write(f"Unlimited PTO: {benefits['pto_vacation']['unlimited']}")
    
    elif tool == "📊 Skills Gap Analysis":
        st.markdown("## Skills Gap Analysis & Development Planning")
        
        # Role selection
        target_role = st.selectbox(
            "Analyze skills for role:",
            ["Software Engineer", "Data Scientist", "Product Manager"]
        )
        
        # Current skill assessment
        st.markdown("### 🎯 Current Skills Assessment")
        
        if target_role in skills_analyzer.skill_data:
            role_skills = skills_analyzer.skill_data[target_role]
            
            user_skills = {}
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Core Technical Skills")
                for skill in role_skills["core_technical"]:
                    level = st.slider(f"{skill}", 0, 10, 5, key=f"core_{skill}")
                    user_skills[skill] = {"level": level, "category": "core_technical"}
                
                st.markdown("#### Frameworks & Tools")
                for skill in role_skills["frameworks_tools"]:
                    level = st.slider(f"{skill}", 0, 10, 5, key=f"tools_{skill}")
                    user_skills[skill] = {"level": level, "category": "frameworks_tools"}
            
            with col2:
                st.markdown("#### Soft Skills") 
                for skill in role_skills["soft_skills"]:
                    level = st.slider(f"{skill}", 0, 10, 5, key=f"soft_{skill}")
                    user_skills[skill] = {"level": level, "category": "soft_skills"}
                
                st.markdown("#### Emerging Skills")
                for skill in role_skills["emerging_skills"]:
                    level = st.slider(f"{skill}", 0, 10, 5, key=f"emerging_{skill}")
                    user_skills[skill] = {"level": level, "category": "emerging_skills"}
            
            if st.button("📊 Analyze Skills Gap", type="primary"):
                
                # Calculate gaps and priorities
                gaps = []
                for skill, data in user_skills.items():
                    if data["level"] < 7:  # Below proficiency threshold
                        gap_size = 7 - data["level"]
                        priority = "High" if data["category"] in ["core_technical", "emerging_skills"] else "Medium"
                        if data["level"] < 4:
                            priority = "Critical"
                        
                        gaps.append({
                            "skill": skill,
                            "current_level": data["level"],
                            "target_level": 7,
                            "gap_size": gap_size,
                            "priority": priority,
                            "category": data["category"]
                        })
                
                gaps.sort(key=lambda x: (x["priority"] == "Critical", x["gap_size"]), reverse=True)
                
                # Display analysis results
                st.markdown("### 📈 Skills Gap Analysis Results")
                
                # Overall assessment
                total_skills = len(user_skills)
                proficient_skills = len([s for s in user_skills.values() if s["level"] >= 7])
                proficiency_rate = (proficient_skills / total_skills) * 100
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Skills Assessed", total_skills)
                with col2:
                    st.metric("Proficient Skills", proficient_skills)
                with col3:
                    st.metric("Proficiency Rate", f"{proficiency_rate:.0f}%")
                with col4:
                    readiness = "Ready" if proficiency_rate >= 80 else "Developing" if proficiency_rate >= 60 else "Needs Focus"
                    st.metric("Role Readiness", readiness)
                
                # Skills radar chart
                categories = list(set(data["category"] for data in user_skills.values()))
                category_averages = {}
                
                for category in categories:
                    cat_skills = [data["level"] for skill, data in user_skills.items() if data["category"] == category]
                    category_averages[category] = np.mean(cat_skills) if cat_skills else 0
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=list(category_averages.values()),
                    theta=list(category_averages.keys()),
                    fill='toself',
                    name='Your Skills'
                ))
                
                # Add target line (7/10)
                fig.add_trace(go.Scatterpolar(
                    r=[7] * len(categories),
                    theta=list(category_averages.keys()),
                    name='Target Level',
                    line_dash='dash'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 10]
                        )
                    ),
                    title="Skills Profile Analysis"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Priority development areas
                st.markdown("### 🎯 Priority Development Areas")
                
                if gaps:
                    for i, gap in enumerate(gaps[:5]):  # Show top 5 gaps
                        priority_color = {
                            "Critical": "🔴",
                            "High": "🟡", 
                            "Medium": "🟢"
                        }
                        
                        with st.expander(f"{priority_color[gap['priority']]} {gap['skill']} - {gap['priority']} Priority"):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.write(f"**Current Level:** {gap['current_level']}/10")
                                st.write(f"**Target Level:** {gap['target_level']}/10")
                                st.write(f"**Gap Size:** {gap['gap_size']} points")
                                
                                # Progress bar
                                progress = gap['current_level'] / 10
                                st.progress(progress, text=f"Current progress: {progress:.0%}")
                            
                            with col2:
                                if gap['skill'] in skills_analyzer.learning_paths:
                                    st.write("**Learning Resources:**")
                                    for resource in skills_analyzer.learning_paths[gap['skill']][:2]:
                                        st.write(f"• {resource['course']} ({resource['provider']})")
                                        st.write(f"  Duration: {resource['duration']}, Cost: {resource['cost']}")
                else:
                    st.success("🎉 Great job! You're proficient in all key areas for this role.")
                
                # Learning path recommendations
                st.markdown("### 📚 Recommended Learning Path")
                
                if gaps:
                    # Create 90-day learning plan
                    st.write("**90-Day Development Plan:**")
                    
                    critical_gaps = [g for g in gaps if g['priority'] == 'Critical']
                    high_gaps = [g for g in gaps if g['priority'] == 'High']
                    
                    plan = []
                    
                    if critical_gaps:
                        plan.append({"weeks": "Weeks 1-4", "focus": critical_gaps[0]['skill'], "goal": "Reach basic proficiency"})
                    if len(critical_gaps) > 1:
                        plan.append({"weeks": "Weeks 5-8", "focus": critical_gaps[1]['skill'], "goal": "Build foundation"})
                    if high_gaps:
                        plan.append({"weeks": "Weeks 9-12", "focus": high_gaps[0]['skill'], "goal": "Advance to intermediate"})
                    
                    for phase in plan:
                        st.info(f"**{phase['weeks']}:** Focus on {phase['focus']} - {phase['goal']}")
    
    elif tool == "🚀 Career Transition Planner":
        st.markdown("## Career Transition Planning")
        
        # Current role input
        current_role = st.selectbox(
            "Current Role:",
            ["Software Engineer", "Data Scientist", "Product Manager"]
        )
        
        # Show transition options
        if current_role in transition_planner.transition_data["common_transitions"]:
            transitions = transition_planner.transition_data["common_transitions"][current_role]
            
            st.markdown("### 🎯 Available Career Paths")
            
            for transition in transitions:
                with st.expander(f"🚀 {current_role} → {transition['to']}", expanded=False):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Timeline", transition['timeline'])
                    with col2:
                        st.metric("Success Rate", transition['success_rate'])
                    with col3:
                        difficulty = "Easy" if float(transition['success_rate'].rstrip('%')) > 70 else "Medium" if float(transition['success_rate'].rstrip('%')) > 50 else "Hard"
                        st.metric("Difficulty", difficulty)
                    
                    st.write("**Key Skills to Develop:**")
                    for skill in transition['key_skills']:
                        st.write(f"• {skill}")
                    
                    if st.button(f"Plan Transition to {transition['to']}", key=f"plan_{transition['to']}"):
                        st.success(f"Creating detailed transition plan for {transition['to']}...")
                        
                        # Detailed transition plan
                        st.markdown(f"#### 📋 Transition Plan: {current_role} → {transition['to']}")
                        
                        # Timeline breakdown
                        timeline_months = {
                            "6-12 months": 9,
                            "1-2 years": 18,
                            "2-3 years": 30,
                            "3-5 years": 48
                        }.get(transition['timeline'], 12)
                        
                        phases = []
                        if timeline_months <= 12:
                            phases = [
                                {"phase": "Months 1-3", "focus": "Skill Assessment & Learning Plan", "activities": ["Identify skill gaps", "Start online courses", "Build side projects"]},
                                {"phase": "Months 4-6", "focus": "Practical Experience", "activities": ["Apply skills at work", "Contribute to relevant projects", "Network in target field"]},
                                {"phase": "Months 7-9", "focus": "Job Search Preparation", "activities": ["Update resume/portfolio", "Practice interviews", "Apply to positions"]},
                                {"phase": "Months 10-12", "focus": "Active Job Search", "activities": ["Interview process", "Negotiate offers", "Make transition"]}
                            ]
                        else:
                            phases = [
                                {"phase": "Year 1", "focus": "Foundation Building", "activities": ["Master core skills", "Build relevant experience", "Start networking"]},
                                {"phase": "Year 2", "focus": "Advanced Skills & Leadership", "activities": ["Take on leadership projects", "Mentor others", "Industry recognition"]},
                                {"phase": "Year 3+", "focus": "Strategic Positioning", "activities": ["Senior role experience", "Industry expertise", "Thought leadership"]}
                            ]
                        
                        for phase in phases:
                            st.write(f"**{phase['phase']}: {phase['focus']}**")
                            for activity in phase['activities']:
                                st.write(f"  • {activity}")
                            st.write("")
        
        # Transition strategy comparison
        st.markdown("### 📊 Transition Strategy Options")
        
        strategies = transition_planner.transition_data["transition_strategies"]
        
        strategy_data = []
        for strategy, data in strategies.items():
            strategy_data.append({
                "Strategy": strategy.replace("_", " ").title(),
                "Timeline": data["timeline"],
                "Success Rate": data["success_rate"],
                "Investment": data["investment"]
            })
        
        df = pd.DataFrame(strategy_data)
        st.dataframe(df, use_container_width=True)
        
        # Strategy recommendations
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            **🏢 Internal Move**
            - Leverage existing relationships
            - Lower risk transition
            - May have limited scope
            """)
        
        with col2:
            st.warning("""
            **🔄 New Company**
            - Fresh start opportunity
            - Market rate compensation
            - Need to prove yourself again
            """)
        
        with col3:
            st.error("""
            **🎯 Career Change**
            - Complete role transformation
            - Highest potential upside
            - Requires significant investment
            """)
    
    elif tool == "📈 Market Intelligence":
        st.markdown("## Market Intelligence Dashboard")
        
        # Hot skills trends
        st.markdown("### 🔥 Hot Skills in the Market")
        
        hot_skills = salary_engine.market_trends["hiring_trends"]["hot_skills"]
        
        for skill in hot_skills:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**{skill['skill']}**")
            with col2:
                st.metric("Demand", skill['demand_increase'])
            with col3:
                st.metric("Salary Premium", skill['salary_premium'])
        
        # Market conditions
        st.markdown("### 📊 Current Market Conditions")
        
        market_conditions = salary_engine.market_trends["hiring_trends"]["market_conditions"]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Competition", market_conditions["competition_level"])
        with col2:
            st.metric("Time to Hire", market_conditions["time_to_hire"])
        with col3:
            st.metric("Offer Acceptance", market_conditions["offer_acceptance_rate"])
        with col4:
            st.metric("Counter Offers", market_conditions["counter_offer_frequency"])
        
        # Salary growth trends
        st.markdown("### 📈 Salary Growth Trends")
        
        growth_data = salary_engine.market_trends["salary_growth"]
        
        # Create trends chart
        roles = ["Software Engineer", "Data Scientist", "Product Manager"]
        years = ["2022", "2023", "2024"]
        
        fig = go.Figure()
        
        for role in roles:
            role_key = role.lower().replace(" ", "_")
            values = [growth_data[year].get(role_key, 0) for year in years]
            
            fig.add_trace(go.Scatter(
                x=years,
                y=values,
                mode='lines+markers',
                name=role,
                line=dict(width=3)
            ))
        
        fig.update_layout(
            title="Salary Growth Rate by Role (%)",
            xaxis_title="Year",
            yaxis_title="Growth Rate (%)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif tool == "🎯 Negotiation Advisor":
        st.markdown("## Salary Negotiation Advisor")
        
        # Negotiation success rates
        st.markdown("### 📊 Negotiation Success Statistics")
        
        success_rates = salary_engine.negotiation_insights["negotiation_success_rates"]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Salary Increase", 
                     f"{success_rates['salary_increase']['success_rate']} success",
                     f"Avg: {success_rates['salary_increase']['avg_increase']} increase")
        
        with col2:
            st.metric("Signing Bonus",
                     f"{success_rates['signing_bonus']['success_rate']} success", 
                     f"Avg: ${success_rates['signing_bonus']['avg_amount']}")
        
        with col3:
            st.metric("Equity Increase",
                     f"{success_rates['equity_increase']['success_rate']} success",
                     f"Avg: {success_rates['equity_increase']['avg_increase']} more")
        
        with col4:
            st.metric("Flexible Work",
                     f"{success_rates['flexible_work']['success_rate']} success")
        
        # Negotiation simulator
        st.markdown("### 🎭 Negotiation Scenario Planner")
        
        with st.form("negotiation_form"):
            current_salary = st.number_input("Current Salary ($):", min_value=50000, max_value=500000, value=100000)
            target_increase = st.slider("Target Increase (%):", 5, 50, 15)
            
            negotiation_items = st.multiselect(
                "Items to Negotiate:",
                ["Base Salary", "Signing Bonus", "Equity/Stock Options", "Vacation Days", "Remote Work", "Learning Budget"]
            )
            
            leverage = st.selectbox(
                "Your Leverage:",
                ["Low - No competing offers", "Medium - Strong performance", "High - Competing offer", "Very High - Multiple competing offers"]
            )
            
            if st.form_submit_button("🎯 Generate Negotiation Strategy"):
                st.markdown("#### 📋 Your Negotiation Strategy")
                
                target_salary = current_salary * (1 + target_increase/100)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Current Salary:** ${current_salary:,}")
                    st.write(f"**Target Salary:** ${target_salary:,.0f}")
                    st.write(f"**Requested Increase:** {target_increase}%")
                
                with col2:
                    # Calculate success probability
                    base_success = 60
                    if "High" in leverage:
                        base_success += 20
                    elif "Medium" in leverage:
                        base_success += 10
                    
                    if target_increase > 20:
                        base_success -= 15
                    elif target_increase > 30:
                        base_success -= 25
                    
                    st.metric("Success Probability", f"{max(base_success, 20)}%")
                
                # Strategy recommendations
                st.markdown("#### 💡 Recommended Approach")
                
                if target_increase <= 15:
                    st.success("✅ Conservative ask - good chance of success")
                elif target_increase <= 25:
                    st.warning("⚠️ Moderate ask - prepare strong justification")
                else:
                    st.error("🔴 Aggressive ask - need exceptional leverage")
                
                st.markdown("**Key Talking Points:**")
                if "Base Salary" in negotiation_items:
                    st.write("• Market research shows similar roles pay X% more")
                    st.write("• Your performance has delivered Y value to the company")
                
                if "Signing Bonus" in negotiation_items:
                    st.write("• One-time bonus to bridge gap between current and target salary")
                
                if "Remote Work" in negotiation_items:
                    st.write("• Highlight productivity gains from flexible work arrangements")
        
        # Timing guidance
        st.markdown("### ⏰ Timing Your Negotiation")
        
        timing = salary_engine.negotiation_insights["timing_insights"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("**Best Times to Negotiate:**")
            for time in timing["best_times"]:
                st.write(f"✅ {time}")
        
        with col2:
            st.error("**Times to Avoid:**")
            for time in timing["worst_times"]:
                st.write(f"❌ {time}")
    
    elif tool == "🔮 Future Readiness":
        st.markdown("## Future Readiness Assessment")
        
        st.info("🚧 Advanced future readiness tools coming soon! This will include AI impact analysis, automation risk assessment, and future skill predictions.")
        
        # Placeholder for future features
        st.markdown("### 🤖 AI Impact Analysis")
        st.write("Analyze how AI might affect your role and industry")
        
        st.markdown("### 📊 Automation Risk Score") 
        st.write("Assess the likelihood of your tasks being automated")
        
        st.markdown("### 🎯 Future Skill Predictions")
        st.write("Identify skills that will be in demand 5-10 years from now")

if __name__ == "__main__":
    main()