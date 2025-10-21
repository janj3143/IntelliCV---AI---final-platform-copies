"""
🎯 IntelliCV User Portal - Career Intelligence Dashboard
========================================================

Advanced career positioning analytics showing:
- Career quadrant mapping (skills vs. market demand)
- Peer comparison and benchmarking
- Market trend analysis and forecasting
- Personalized career advancement recommendations
- Visual career journey mapping

Integrated from frontend career intelligence modules
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
import sys

# Setup paths and imports
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

# Import admin AI integration
try:
    from user_portal_admin_integration import process_user_action_with_admin_ai, init_admin_ai_for_user_page
    ADMIN_AI_AVAILABLE = True
except ImportError:
    ADMIN_AI_AVAILABLE = False

# Import utilities with fallbacks
try:
    from utils.error_handler import log_user_action, show_error, show_success, show_warning
    ERROR_HANDLER_AVAILABLE = True
except ImportError:
    ERROR_HANDLER_AVAILABLE = False
    def log_user_action(action, details=None): pass
    def show_error(msg): st.error(f"❌ {msg}")
    def show_success(msg): st.success(f"✅ {msg}")
    def show_warning(msg): st.warning(f"⚠️ {msg}")

# Page configuration
st.set_page_config(
    page_title="Career Intelligence | IntelliCV",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class CareerIntelligenceEngine:
    """Advanced career positioning and market intelligence system"""
    
    def __init__(self):
        self.market_data = self._load_market_data()
        self.skill_benchmarks = self._load_skill_benchmarks()
        self.career_trajectories = self._load_career_trajectories()
        self.industry_trends = self._load_industry_trends()
        
    def _load_market_data(self) -> Dict[str, Any]:
        """Load current market demand and salary data"""
        return {
            "roles": {
                "Software Engineer": {
                    "demand_score": 95,
                    "avg_salary": 95000,
                    "growth_rate": 22,
                    "skills_required": ["Python", "JavaScript", "Cloud", "APIs"],
                    "market_saturation": "Low",
                    "remote_friendly": True
                },
                "Data Scientist": {
                    "demand_score": 88,
                    "avg_salary": 105000,
                    "growth_rate": 35,
                    "skills_required": ["Python", "SQL", "Machine Learning", "Statistics"],
                    "market_saturation": "Medium",
                    "remote_friendly": True
                },
                "Product Manager": {
                    "demand_score": 82,
                    "avg_salary": 115000,
                    "growth_rate": 18,
                    "skills_required": ["Strategy", "Analytics", "Leadership", "Communication"],
                    "market_saturation": "High",
                    "remote_friendly": True
                },
                "DevOps Engineer": {
                    "demand_score": 91,
                    "avg_salary": 100000,
                    "growth_rate": 28,
                    "skills_required": ["AWS", "Kubernetes", "CI/CD", "Monitoring"],
                    "market_saturation": "Low",
                    "remote_friendly": True
                },
                "UX Designer": {
                    "demand_score": 75,
                    "avg_salary": 85000,
                    "growth_rate": 13,
                    "skills_required": ["Figma", "User Research", "Prototyping", "Design Systems"],
                    "market_saturation": "Medium",
                    "remote_friendly": True
                }
            },
            "skills_demand": {
                "Python": {"demand": 95, "trend": "rising", "salary_impact": 15},
                "JavaScript": {"demand": 90, "trend": "stable", "salary_impact": 12},
                "Machine Learning": {"demand": 88, "trend": "rising", "salary_impact": 20},
                "Cloud Computing": {"demand": 92, "trend": "rising", "salary_impact": 18},
                "Leadership": {"demand": 85, "trend": "stable", "salary_impact": 25},
                "Data Analysis": {"demand": 87, "trend": "rising", "salary_impact": 16}
            }
        }
    
    def _load_skill_benchmarks(self) -> Dict[str, Dict]:
        """Load skill benchmarks and peer comparison data"""
        return {
            "technical_skills": {
                "Python": {"user_level": 7, "market_average": 6, "top_10_percent": 9},
                "JavaScript": {"user_level": 6, "market_average": 6, "top_10_percent": 8},
                "SQL": {"user_level": 8, "market_average": 5, "top_10_percent": 9},
                "Machine Learning": {"user_level": 5, "market_average": 4, "top_10_percent": 8},
                "Cloud Platforms": {"user_level": 6, "market_average": 5, "top_10_percent": 8}
            },
            "soft_skills": {
                "Communication": {"user_level": 8, "market_average": 6, "top_10_percent": 9},
                "Leadership": {"user_level": 6, "market_average": 5, "top_10_percent": 8},
                "Problem Solving": {"user_level": 8, "market_average": 6, "top_10_percent": 9},
                "Project Management": {"user_level": 7, "market_average": 5, "top_10_percent": 8},
                "Strategic Thinking": {"user_level": 6, "market_average": 5, "top_10_percent": 8}
            }
        }
    
    def _load_career_trajectories(self) -> Dict[str, List[Dict]]:
        """Load typical career progression paths"""
        return {
            "Software Engineer": [
                {"level": "Junior", "years": "0-2", "salary_range": "60-80k", "skills": ["Basic Programming", "Version Control"]},
                {"level": "Mid-Level", "years": "2-5", "salary_range": "80-110k", "skills": ["Architecture", "Mentoring"]},
                {"level": "Senior", "years": "5-8", "salary_range": "110-150k", "skills": ["System Design", "Leadership"]},
                {"level": "Staff/Principal", "years": "8+", "salary_range": "150-250k", "skills": ["Technical Strategy", "Org Impact"]}
            ],
            "Data Scientist": [
                {"level": "Junior", "years": "0-2", "salary_range": "70-90k", "skills": ["Statistics", "Python/R"]},
                {"level": "Mid-Level", "years": "2-5", "salary_range": "90-130k", "skills": ["ML Engineering", "Business Acumen"]},
                {"level": "Senior", "years": "5-8", "salary_range": "130-180k", "skills": ["ML Strategy", "Team Leadership"]},
                {"level": "Principal/Director", "years": "8+", "salary_range": "180-300k", "skills": ["Data Strategy", "Cross-org Impact"]}
            ]
        }
    
    def _load_industry_trends(self) -> Dict[str, Any]:
        """Load industry trend data and forecasts"""
        return {
            "emerging_technologies": [
                {"tech": "Artificial Intelligence", "growth_rate": 45, "job_impact": "High"},
                {"tech": "Cloud Computing", "growth_rate": 25, "job_impact": "Very High"},
                {"tech": "Cybersecurity", "growth_rate": 35, "job_impact": "High"},
                {"tech": "Blockchain", "growth_rate": 15, "job_impact": "Medium"},
                {"tech": "IoT", "growth_rate": 20, "job_impact": "Medium"}
            ],
            "skill_predictions": {
                "2024": ["AI/ML", "Cloud Architecture", "Data Engineering"],
                "2025": ["Quantum Computing", "Edge Computing", "Advanced Analytics"],
                "2026": ["Autonomous Systems", "Neuromorphic Computing", "Sustainable Tech"]
            }
        }
    
    def calculate_career_quadrant_position(self, user_profile: Dict) -> Dict[str, float]:
        """Calculate user's position in the career quadrant"""
        # Skills Assessment Score (0-100)
        technical_avg = np.mean([
            skill["user_level"] for skill in self.skill_benchmarks["technical_skills"].values()
        ]) * 10  # Convert to 0-100 scale
        
        soft_skills_avg = np.mean([
            skill["user_level"] for skill in self.skill_benchmarks["soft_skills"].values()
        ]) * 10
        
        skills_score = (technical_avg + soft_skills_avg) / 2
        
        # Market Demand Score (0-100)
        user_role = user_profile.get("target_role", "Software Engineer")
        role_data = self.market_data["roles"].get(user_role, self.market_data["roles"]["Software Engineer"])
        market_demand = role_data["demand_score"]
        
        return {
            "skills_score": skills_score,
            "market_demand": market_demand,
            "quadrant": self._determine_quadrant(skills_score, market_demand)
        }
    
    def _determine_quadrant(self, skills: float, demand: float) -> str:
        """Determine which career quadrant the user falls into"""
        if skills >= 70 and demand >= 70:
            return "Star Performer"
        elif skills >= 70 and demand < 70:
            return "Skill Master"
        elif skills < 70 and demand >= 70:
            return "Market Surfer"
        else:
            return "Growth Opportunity"

class CareerQuadrantVisualizer:
    """Advanced visualization system for career positioning"""
    
    def __init__(self, engine: CareerIntelligenceEngine):
        self.engine = engine
    
    def create_career_quadrant_chart(self, user_position: Dict, peer_data: List[Dict]) -> go.Figure:
        """Create interactive career quadrant positioning chart"""
        
        fig = go.Figure()
        
        # Add quadrant background
        self._add_quadrant_background(fig)
        
        # Add peer data points
        if peer_data:
            fig.add_trace(go.Scatter(
                x=[p["market_demand"] for p in peer_data],
                y=[p["skills_score"] for p in peer_data],
                mode='markers',
                marker=dict(
                    size=8,
                    color='lightblue',
                    opacity=0.6,
                    line=dict(width=1, color='darkblue')
                ),
                name='Peer Group',
                hovertemplate='Skills: %{y:.1f}<br>Market Demand: %{x:.1f}<extra></extra>'
            ))
        
        # Add user position
        fig.add_trace(go.Scatter(
            x=[user_position["market_demand"]],
            y=[user_position["skills_score"]],
            mode='markers',
            marker=dict(
                size=15,
                color='red',
                symbol='star',
                line=dict(width=2, color='darkred')
            ),
            name='Your Position',
            hovertemplate=f'<b>Your Position</b><br>Skills: %{{y:.1f}}<br>Market Demand: %{{x:.1f}}<br>Quadrant: {user_position["quadrant"]}<extra></extra>'
        ))
        
        # Customize layout
        fig.update_layout(
            title={
                'text': 'Career Quadrant Positioning',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24}
            },
            xaxis_title='Market Demand Score',
            yaxis_title='Skills Competency Score',
            xaxis=dict(range=[0, 100], gridcolor='lightgray'),
            yaxis=dict(range=[0, 100], gridcolor='lightgray'),
            plot_bgcolor='white',
            width=700,
            height=500,
            showlegend=True
        )
        
        return fig
    
    def _add_quadrant_background(self, fig: go.Figure):
        """Add colored background regions for each quadrant"""
        
        # Define quadrant colors and labels
        quadrants = [
            {"x": [0, 50], "y": [0, 50], "color": "rgba(255, 200, 200, 0.3)", "label": "Growth Opportunity"},
            {"x": [50, 100], "y": [0, 50], "color": "rgba(255, 255, 200, 0.3)", "label": "Market Surfer"},
            {"x": [0, 50], "y": [50, 100], "color": "rgba(200, 255, 200, 0.3)", "label": "Skill Master"},
            {"x": [50, 100], "y": [50, 100], "color": "rgba(200, 200, 255, 0.3)", "label": "Star Performer"}
        ]
        
        for quad in quadrants:
            fig.add_shape(
                type="rect",
                x0=quad["x"][0], y0=quad["y"][0],
                x1=quad["x"][1], y1=quad["y"][1],
                fillcolor=quad["color"],
                layer="below",
                line_width=0
            )
            
            # Add quadrant labels
            fig.add_annotation(
                x=sum(quad["x"]) / 2,
                y=sum(quad["y"]) / 2,
                text=f"<b>{quad['label']}</b>",
                showarrow=False,
                font=dict(size=12, color="gray"),
                bgcolor="white",
                bordercolor="gray",
                borderwidth=1
            )
        
        # Add dividing lines
        fig.add_hline(y=50, line_dash="dash", line_color="gray", line_width=1)
        fig.add_vline(x=50, line_dash="dash", line_color="gray", line_width=1)
    
    def create_peer_comparison_radar(self, user_skills: Dict, peer_averages: Dict) -> go.Figure:
        """Create radar chart comparing user skills to peer averages"""
        
        categories = list(user_skills.keys())
        user_values = [user_skills[cat]["user_level"] for cat in categories]
        peer_values = [peer_averages.get(cat, 5) for cat in categories]
        top_10_values = [user_skills[cat]["top_10_percent"] for cat in categories]
        
        fig = go.Figure()
        
        # Add user data
        fig.add_trace(go.Scatterpolar(
            r=user_values + [user_values[0]],  # Close the polygon
            theta=categories + [categories[0]],
            fill='toself',
            name='Your Skills',
            line_color='blue',
            fillcolor='rgba(0, 0, 255, 0.3)'
        ))
        
        # Add peer average
        fig.add_trace(go.Scatterpolar(
            r=peer_values + [peer_values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Peer Average',
            line_color='orange',
            fillcolor='rgba(255, 165, 0, 0.2)'
        ))
        
        # Add top 10% benchmark
        fig.add_trace(go.Scatterpolar(
            r=top_10_values + [top_10_values[0]],
            theta=categories + [categories[0]],
            name='Top 10%',
            line_color='green',
            line_dash='dash'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            title="Skills Comparison vs. Peers",
            showlegend=True
        )
        
        return fig
    
    def create_career_trajectory_chart(self, current_role: str, trajectories: Dict) -> go.Figure:
        """Create career trajectory visualization"""
        
        if current_role not in trajectories:
            current_role = "Software Engineer"  # Default fallback
        
        path = trajectories[current_role]
        
        fig = go.Figure()
        
        # Extract data for plotting
        levels = [stage["level"] for stage in path]
        years = [stage["years"] for stage in path]
        salaries = [int(stage["salary_range"].split("-")[1].replace("k", "")) * 1000 for stage in path]
        
        # Create trajectory line
        fig.add_trace(go.Scatter(
            x=list(range(len(levels))),
            y=salaries,
            mode='lines+markers',
            name='Career Trajectory',
            line=dict(color='blue', width=3),
            marker=dict(size=10, color='blue'),
            hovertemplate='<b>%{customdata[0]}</b><br>Experience: %{customdata[1]}<br>Salary: $%{y:,.0f}<extra></extra>',
            customdata=list(zip(levels, years))
        ))
        
        # Add annotations for each level
        for i, (level, salary) in enumerate(zip(levels, salaries)):
            fig.add_annotation(
                x=i,
                y=salary,
                text=level,
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="blue",
                ax=0,
                ay=-30
            )
        
        fig.update_layout(
            title=f'Career Trajectory: {current_role}',
            xaxis_title='Career Stage',
            yaxis_title='Salary Range',
            xaxis=dict(tickvals=list(range(len(levels))), ticktext=levels),
            yaxis=dict(tickformat='$,.0f'),
            plot_bgcolor='white'
        )
        
        return fig

def generate_peer_data(n_peers: int = 50) -> List[Dict]:
    """Generate simulated peer comparison data"""
    np.random.seed(42)  # For consistent results
    
    peers = []
    for _ in range(n_peers):
        # Generate realistic distributions
        skills_score = np.random.normal(60, 15)
        market_demand = np.random.normal(70, 12)
        
        # Clamp to valid ranges
        skills_score = max(0, min(100, skills_score))
        market_demand = max(0, min(100, market_demand))
        
        peers.append({
            "skills_score": skills_score,
            "market_demand": market_demand
        })
    
    return peers

def main():
    """Main application interface"""
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; margin-bottom: 30px;">
        <h1 style="color: white; margin: 0;">📊 Career Intelligence Dashboard</h1>
        <p style="color: white; margin: 5px 0 0 0; opacity: 0.9;">
            Discover where you stand in your career journey and map your path to success
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize systems
    engine = CareerIntelligenceEngine()
    visualizer = CareerQuadrantVisualizer(engine)
    
    # Sidebar configuration
    st.sidebar.markdown("## 📊 Career Analysis")
    
    # User profile input
    with st.sidebar.expander("🎯 Your Profile", expanded=True):
        current_role = st.selectbox(
            "Current Role:",
            ["Software Engineer", "Data Scientist", "Product Manager", "DevOps Engineer", "UX Designer"]
        )
        
        experience_years = st.slider("Years of Experience:", 0, 20, 5)
        
        target_role = st.selectbox(
            "Target Role:",
            ["Software Engineer", "Data Scientist", "Product Manager", "DevOps Engineer", "UX Designer"],
            index=0 if current_role == "Software Engineer" else 1
        )
    
    user_profile = {
        "current_role": current_role,
        "target_role": target_role,
        "experience_years": experience_years
    }
    
    # Calculate user position
    user_position = engine.calculate_career_quadrant_position(user_profile)
    
    # Main dashboard layout
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Career Positioning", 
        "📈 Skills Analysis", 
        "🚀 Career Trajectory", 
        "🔮 Market Trends"
    ])
    
    with tab1:
        st.markdown("## Your Career Quadrant Position")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Skills Score",
                f"{user_position['skills_score']:.0f}/100",
                delta=f"+{user_position['skills_score'] - 60:.0f}" if user_position['skills_score'] > 60 else None
            )
        
        with col2:
            st.metric(
                "Market Demand",
                f"{user_position['market_demand']:.0f}/100"
            )
        
        with col3:
            quadrant_colors = {
                "Star Performer": "🌟",
                "Skill Master": "🎓",
                "Market Surfer": "🏄",
                "Growth Opportunity": "🚀"
            }
            st.metric(
                "Your Quadrant",
                f"{quadrant_colors.get(user_position['quadrant'], '📍')} {user_position['quadrant']}"
            )
        
        with col4:
            role_data = engine.market_data["roles"][current_role]
            st.metric(
                "Role Growth Rate",
                f"{role_data['growth_rate']}%"
            )
        
        # Career quadrant visualization
        col1, col2 = st.columns([2, 1])
        
        with col1:
            peer_data = generate_peer_data()
            quadrant_chart = visualizer.create_career_quadrant_chart(user_position, peer_data)
            st.plotly_chart(quadrant_chart, use_container_width=True)
        
        with col2:
            st.markdown("### 📋 Quadrant Insights")
            
            quadrant = user_position['quadrant']
            
            if quadrant == "Star Performer":
                st.success("""
                🌟 **Excellent Position!**
                - High skills + High demand
                - Prime for leadership roles
                - Consider mentoring others
                - Negotiate premium compensation
                """)
            elif quadrant == "Skill Master":
                st.info("""
                🎓 **Strong Skills Foundation**
                - Excellent technical abilities
                - Seek higher-demand markets
                - Consider trending technologies
                - Leverage expertise for consulting
                """)
            elif quadrant == "Market Surfer":
                st.warning("""
                🏄 **Riding the Wave**
                - High market demand
                - Focus on skill development
                - Take advantage of opportunities
                - Invest in learning and growth
                """)
            else:
                st.error("""
                🚀 **Growth Mode**
                - Great potential ahead
                - Focus on skill building
                - Research market trends
                - Consider training programs
                """)
            
            # Action recommendations
            st.markdown("### 🎯 Recommended Actions")
            
            role_data = engine.market_data["roles"][target_role]
            missing_skills = [skill for skill in role_data["skills_required"] 
                            if skill not in engine.skill_benchmarks["technical_skills"]]
            
            if missing_skills:
                st.write("**Skills to Develop:**")
                for skill in missing_skills[:3]:
                    st.write(f"• {skill}")
            
            st.write(f"**Market Outlook:** {role_data['market_saturation']} saturation")
            st.write(f"**Remote Work:** {'✅ Yes' if role_data['remote_friendly'] else '❌ Limited'}")
    
    with tab2:
        st.markdown("## Skills Analysis & Benchmarking")
        
        # Skills comparison radar chart
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Combine technical and soft skills for display
            all_skills = {**engine.skill_benchmarks["technical_skills"], **engine.skill_benchmarks["soft_skills"]}
            peer_averages = {skill: data["market_average"] for skill, data in all_skills.items()}
            
            radar_chart = visualizer.create_peer_comparison_radar(all_skills, peer_averages)
            st.plotly_chart(radar_chart, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Skills Breakdown")
            
            # Top skills
            user_skills = [(skill, data["user_level"]) for skill, data in all_skills.items()]
            user_skills.sort(key=lambda x: x[1], reverse=True)
            
            st.write("**Your Top Skills:**")
            for skill, level in user_skills[:5]:
                progress = level / 10
                st.progress(progress, text=f"{skill}: {level}/10")
            
            # Skills to improve
            st.markdown("### 📈 Priority Development Areas")
            improvement_skills = [(skill, data["top_10_percent"] - data["user_level"]) 
                                 for skill, data in all_skills.items()]
            improvement_skills = [(skill, gap) for skill, gap in improvement_skills if gap > 1]
            improvement_skills.sort(key=lambda x: x[1], reverse=True)
            
            for skill, gap in improvement_skills[:3]:
                st.write(f"• **{skill}**: +{gap:.1f} points to top 10%")
        
        # Detailed skills table
        st.markdown("### 📊 Detailed Skills Comparison")
        
        skills_df = pd.DataFrame([
            {
                "Skill": skill,
                "Your Level": data["user_level"],
                "Market Average": data["market_average"],
                "Top 10%": data["top_10_percent"],
                "Gap to Top 10%": data["top_10_percent"] - data["user_level"],
                "Category": "Technical" if skill in engine.skill_benchmarks["technical_skills"] else "Soft Skills"
            }
            for skill_category in [engine.skill_benchmarks["technical_skills"], engine.skill_benchmarks["soft_skills"]]
            for skill, data in skill_category.items()
        ])
        
        st.dataframe(
            skills_df.style.format({
                "Your Level": "{:.1f}",
                "Market Average": "{:.1f}",
                "Top 10%": "{:.1f}",
                "Gap to Top 10%": "{:.1f}"
            }).background_gradient(subset=["Your Level"], cmap="RdYlGn"),
            use_container_width=True
        )
    
    with tab3:
        st.markdown("## Career Trajectory Planning")
        
        # Career path visualization
        trajectory_chart = visualizer.create_career_trajectory_chart(
            current_role, 
            engine.career_trajectories
        )
        st.plotly_chart(trajectory_chart, use_container_width=True)
        
        # Career planning section
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Your Career Path")
            
            if current_role in engine.career_trajectories:
                path = engine.career_trajectories[current_role]
                
                for i, stage in enumerate(path):
                    # Determine if user is at this stage
                    stage_years = stage["years"].split("-")[0]
                    is_current = (i == 0 and experience_years < 2) or \
                               (i == 1 and 2 <= experience_years < 5) or \
                               (i == 2 and 5 <= experience_years < 8) or \
                               (i == 3 and experience_years >= 8)
                    
                    icon = "👤" if is_current else "⏭️" if experience_years < int(stage_years) else "✅"
                    
                    with st.expander(f"{icon} {stage['level']} ({stage['years']} years)", expanded=is_current):
                        st.write(f"**Salary Range:** {stage['salary_range']}")
                        st.write("**Key Skills:**")
                        for skill in stage['skills']:
                            st.write(f"• {skill}")
                        
                        if is_current:
                            st.info("📍 You are currently at this level")
        
        with col2:
            st.markdown("### 📈 Advancement Strategy")
            
            # Next level recommendations
            current_level = min(experience_years // 3, 3)  # Simplified level calculation
            
            if current_role in engine.career_trajectories and current_level < len(engine.career_trajectories[current_role]) - 1:
                next_stage = engine.career_trajectories[current_role][current_level + 1]
                
                st.success(f"**Next Target:** {next_stage['level']}")
                
                st.markdown("**Skills to Develop:**")
                for skill in next_stage['skills']:
                    st.write(f"• {skill}")
                
                # Timeline estimate
                years_to_next = max(0, (current_level + 1) * 3 - experience_years)
                if years_to_next > 0:
                    st.info(f"**Estimated Timeline:** {years_to_next:.1f} years")
                else:
                    st.success("**Ready for advancement!**")
            
            # Industry-specific advice
            st.markdown("### 🎓 Development Recommendations")
            
            role_data = engine.market_data["roles"][current_role]
            
            st.write("**High-Impact Skills:**")
            for skill in role_data["skills_required"]:
                demand_data = engine.market_data["skills_demand"].get(skill, {})
                trend = demand_data.get("trend", "stable")
                impact = demand_data.get("salary_impact", 10)
                
                trend_icon = "📈" if trend == "rising" else "📊" if trend == "stable" else "📉"
                st.write(f"{trend_icon} **{skill}** (+{impact}% salary impact)")
    
    with tab4:
        st.markdown("## Market Trends & Future Outlook")
        
        # Emerging technologies
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🚀 Emerging Technologies")
            
            for tech in engine.industry_trends["emerging_technologies"]:
                st.markdown(f"""
                **{tech['tech']}**  
                Growth Rate: {tech['growth_rate']}% | Impact: {tech['job_impact']}
                """)
                
                # Visual growth indicator
                growth_normalized = tech['growth_rate'] / 50  # Normalize to 0-1
                st.progress(growth_normalized)
        
        with col2:
            st.markdown("### 📅 Skills Forecast")
            
            for year, skills in engine.industry_trends["skill_predictions"].items():
                with st.expander(f"🔮 {year} Predictions"):
                    for skill in skills:
                        st.write(f"• {skill}")
        
        # Market demand visualization
        st.markdown("### 📊 Current Market Demand")
        
        # Create market demand chart
        roles_data = []
        for role, data in engine.market_data["roles"].items():
            roles_data.append({
                "Role": role,
                "Demand Score": data["demand_score"],
                "Average Salary": data["avg_salary"],
                "Growth Rate": data["growth_rate"],
                "Market Saturation": data["market_saturation"]
            })
        
        df = pd.DataFrame(roles_data)
        
        # Bubble chart: Demand vs Salary vs Growth
        fig = px.scatter(
            df,
            x="Demand Score",
            y="Average Salary",
            size="Growth Rate",
            color="Market Saturation",
            hover_name="Role",
            title="Role Market Analysis: Demand vs Salary vs Growth",
            labels={
                "Demand Score": "Market Demand Score (0-100)",
                "Average Salary": "Average Salary ($)"
            }
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Skills demand heatmap
        st.markdown("### 🌡️ Skills Market Heat Map")
        
        skills_matrix = []
        for skill, data in engine.market_data["skills_demand"].items():
            skills_matrix.append({
                "Skill": skill,
                "Market Demand": data["demand"],
                "Salary Impact": data["salary_impact"],
                "Trend": data["trend"]
            })
        
        skills_df = pd.DataFrame(skills_matrix)
        
        fig = px.scatter(
            skills_df,
            x="Market Demand",
            y="Salary Impact",
            size="Salary Impact",
            color="Trend",
            hover_name="Skill",
            title="Skills Market Analysis",
            color_discrete_map={
                "rising": "green",
                "stable": "blue",
                "declining": "red"
            }
        )
        
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()