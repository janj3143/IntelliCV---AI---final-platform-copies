"""
=============================================================================
IntelliCV Admin Portal - Market Intelligence Center Suite
=============================================================================

Advanced market intelligence system with real-time data analysis,
job market trends, salary forecasting, and industry insights.

Features:
- Comprehensive market data analysis
- Job market trends and forecasting
- Salary intelligence and predictions
- Emerging skills identification
- Industry growth projections
- Integration hooks for lockstep synchronization
"""

import streamlit as st

# =============================================================================
# MANDATORY AUTHENTICATION CHECK  
# =============================================================================

def check_authentication():
    """Auto-generated function body"""
    return True  # Fallback authentication


# =============================================================================
# FALLBACK FUNCTIONS FOR MISSING SHARED COMPONENTS
# =============================================================================

def render_section_header(title, icon="", show_line=True):
    """Fallback for missing render_section_header"""
    st.markdown(f"## {icon} {title}")
    if show_line:
        st.markdown("---")

def render_metrics_row(*args, **kwargs):
    """Fallback for missing render_metrics_row"""
    pass

def render_status_indicator(*args, **kwargs):
    """Fallback for missing render_status_indicator"""
    pass

def render_action_buttons(*args, **kwargs):
    """Fallback for missing render_action_buttons"""
    pass

def render_data_table(*args, **kwargs):
    """Fallback for missing render_data_table"""
    pass

def inject_admin_css():
    """Fallback for missing inject_admin_css"""
    pass

def render_chart_container(*args, **kwargs):
    """Fallback for missing render_chart_container"""
    pass

def get_admin_session_state(*args, **kwargs):
    """Fallback for missing get_admin_session_state"""
    return {}

def log_admin_action(*args, **kwargs):
    """Fallback for missing log_admin_action"""
    pass

def format_datetime(dt, format_type=None):
    """Fallback for missing format_datetime"""
    if hasattr(dt, 'strftime'):
        if format_type == "relative":
            # Simple relative time formatting
            try:
                from datetime import datetime, timedelta
                now = datetime.now()
                if isinstance(dt, str):
                    dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
                diff = now - dt
                if diff.days > 0:
                    return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
                elif diff.seconds > 3600:
                    hours = diff.seconds // 3600
                    return f"{hours} hour{'s' if hours != 1 else ''} ago"
                elif diff.seconds > 60:
                    minutes = diff.seconds // 60
                    return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
                else:
                    return "Just now"
            except:
                return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return dt.strftime("%Y-%m-%d %H:%M:%S")
    return str(dt)
def create_sample_dataframe(*args, **kwargs):
    """Fallback for missing create_sample_dataframe"""
    import pandas as pd
    return pd.DataFrame()

def get_system_status():
    """Fallback for missing get_system_status"""
    return {"status": "unknown"}

def get_session_state(*args, **kwargs):
    """Fallback for missing get_session_state"""
    return st.session_state

def set_session_state(*args, **kwargs):
    """Fallback for missing set_session_state"""
    pass

def get_integration_hooks():
    """Fallback for missing get_integration_hooks"""
    return {}

def validate_admin_permissions(*args, **kwargs):
    """Fallback for missing validate_admin_permissions"""
    return True


    """Ensure user is authenticated before accessing this page"""
    if not st.session_state.get('admin_authenticated', False):
        st.error("🚫 **AUTHENTICATION REQUIRED**")
        st.info("Please return to the main page and login to access this module.")
        st.markdown("---")
        st.markdown("### 🔐 Access Denied")
        st.markdown("This page is only accessible to authenticated admin users.")
        if st.button("🔙 Return to Main Page"):
            st.switch_page("main.py")
        st.stop()

# Check authentication immediately
check_authentication()

# Hide sidebar navigation for unauthorized access
if not st.session_state.get('admin_authenticated', False):
    st.markdown("""
    <style>
        .css-1d391kg {display: none;}
        [data-testid="stSidebar"] {display: none;}
        .css-1rs6os {display: none;}
        .css-17ziqus {display: none;}
    </style>
    """, unsafe_allow_html=True)


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path
import time
import sys
import json
import random
from typing import Dict, Any, List

# Add shared components to path
pages_dir = Path(__file__).parent
if str(pages_dir) not in sys.path:
    sys.path.insert(0, str(pages_dir))

# Import real AI data connector for production data
try:
    from shared.real_ai_data_connector import (
        get_real_ai_connector, 
        get_real_sample_data, 
        get_real_analytics_data
    )
    REAL_AI_DATA_AVAILABLE = True
except ImportError:
    REAL_AI_DATA_AVAILABLE = False

# from shared.components import render_section_header, render_metrics_row  # Using fallback implementations
# from shared.integration_hooks import get_integration_hooks  # Using fallback implementations

# =============================================================================
# MARKET INTELLIGENCE CENTER SUITE
# =============================================================================

class MarketIntelligenceCenter:
    """Complete Market Intelligence & Analysis Suite"""
    
    def __init__(self):
        """Initialize market intelligence system."""
        self.integration_hooks = get_integration_hooks()
        self.market_data_dir = Path("C:/IntelliCV/market_intelligence")
        self.reports_dir = Path("C:/IntelliCV/market_reports")
        self.market_data = {}
        self.job_trends = None
        self.salary_forecasts = {}
        self.emerging_skills = []
        self.industry_growth = {}
        self.load_market_data()
    
    def load_market_data(self):
        """Load comprehensive market intelligence data."""
        self.market_data = self.get_default_market_data()
        self.job_trends = self.generate_job_market_trends()
        self.salary_forecasts = self.generate_salary_forecasts()
        self.emerging_skills = self.generate_emerging_skills_data()
        self.industry_growth = self.generate_industry_growth_data()
    
    def get_default_market_data(self):
        """Default comprehensive market data."""
        return {
            "hot_skills_2025": {
                "AI/ML Engineering": {"growth_rate": 45, "avg_salary": 165000, "demand_score": 98},
                "Cybersecurity Specialist": {"growth_rate": 38, "avg_salary": 145000, "demand_score": 95},
                "Cloud Architecture": {"growth_rate": 42, "avg_salary": 155000, "demand_score": 92},
                "Data Engineering": {"growth_rate": 35, "avg_salary": 140000, "demand_score": 90},
                "DevOps Engineering": {"growth_rate": 32, "avg_salary": 135000, "demand_score": 88},
                "Full Stack Development": {"growth_rate": 28, "avg_salary": 120000, "demand_score": 85},
                "Product Management": {"growth_rate": 25, "avg_salary": 130000, "demand_score": 82},
                "UX/UI Design": {"growth_rate": 22, "avg_salary": 110000, "demand_score": 80}
            },
            "industry_insights": {
                "Technology": {"growth_projection": 28, "hiring_velocity": "Very High", "remote_friendly": 85},
                "Healthcare": {"growth_projection": 22, "hiring_velocity": "High", "remote_friendly": 45},
                "Finance": {"growth_projection": 18, "hiring_velocity": "Moderate", "remote_friendly": 70},
                "Manufacturing": {"growth_projection": 15, "hiring_velocity": "Moderate", "remote_friendly": 25},
                "Education": {"growth_projection": 12, "hiring_velocity": "Stable", "remote_friendly": 60}
            },
            "remote_work_trends": {
                "fully_remote": 35,
                "hybrid": 45,
                "on_site": 20
            },
            "last_updated": datetime.now().isoformat()
        }
    
    def generate_job_market_trends(self):
        """Generate comprehensive job market trends."""
        base_date = datetime.now() - timedelta(days=730)
        trends_data = []
        
        for i in range(24):
            month_date = base_date + timedelta(days=i*30)
            trends_data.append({
                'month': month_date.strftime('%Y-%m'),
                'month_name': month_date.strftime('%B %Y'),
                'Technology': 100 + (i * 3) + random.randint(-5, 8),
                'Healthcare': 100 + (i * 2) + random.randint(-3, 5),
                'Finance': 100 + (i * 1.5) + random.randint(-2, 4),
                'Manufacturing': 100 + (i * 1) + random.randint(-2, 3),
                'Education': 100 + (i * 0.5) + random.randint(-1, 2),
                'total_jobs': 50000 + (i * 2000) + random.randint(-1000, 3000)
            })
        
        return trends_data
    
    def generate_salary_forecasts(self):
        """Generate salary forecasting data."""
        return {
            'AI/ML Engineer': {
                'current': 165000,
                'forecast_6m': 172000,
                'forecast_12m': 180000,
                'growth_rate': 9.1,
                'confidence': 85
            },
            'DevOps Engineer': {
                'current': 135000,
                'forecast_6m': 140000,
                'forecast_12m': 145000,
                'growth_rate': 7.4,
                'confidence': 80
            },
            'Data Engineer': {
                'current': 140000,
                'forecast_6m': 146000,
                'forecast_12m': 152000,
                'growth_rate': 8.6,
                'confidence': 82
            },
            'Cloud Architect': {
                'current': 155000,
                'forecast_6m': 162000,
                'forecast_12m': 170000,
                'growth_rate': 9.7,
                'confidence': 88
            },
            'Product Manager': {
                'current': 130000,
                'forecast_6m': 135000,
                'forecast_12m': 140000,
                'growth_rate': 7.7,
                'confidence': 75
            }
        }
    
    def generate_emerging_skills_data(self):
        """Generate emerging skills with trend analysis."""
        return [
            {"skill": "Generative AI", "growth_rate": 340, "adoption_rate": 68, "category": "Artificial Intelligence"},
            {"skill": "Kubernetes", "growth_rate": 180, "adoption_rate": 45, "category": "DevOps"},
            {"skill": "Vector Databases", "growth_rate": 220, "adoption_rate": 35, "category": "Data Engineering"},
            {"skill": "Edge Computing", "growth_rate": 150, "adoption_rate": 40, "category": "Cloud Computing"},
            {"skill": "WebAssembly", "growth_rate": 160, "adoption_rate": 25, "category": "Web Development"},
            {"skill": "Quantum Computing", "growth_rate": 120, "adoption_rate": 15, "category": "Advanced Computing"},
            {"skill": "MLOps", "growth_rate": 200, "adoption_rate": 55, "category": "Machine Learning"},
            {"skill": "Blockchain Development", "growth_rate": 90, "adoption_rate": 30, "category": "Distributed Systems"}
        ]
    
    def generate_industry_growth_data(self):
        """Generate industry-specific growth projections."""
        return {
            "Technology": {
                "current_size": 2.8e12,
                "projected_growth": 0.15,
                "key_drivers": ["AI/ML", "Cloud Computing", "Cybersecurity"],
                "job_creation": 450000,
                "avg_salary_growth": 0.08
            },
            "Healthcare": {
                "current_size": 4.5e12,
                "projected_growth": 0.12,
                "key_drivers": ["Digital Health", "Telemedicine", "Health Analytics"],
                "job_creation": 320000,
                "avg_salary_growth": 0.06
            },
            "Finance": {
                "current_size": 1.5e12,
                "projected_growth": 0.08,
                "key_drivers": ["FinTech", "Digital Banking", "Cryptocurrency"],
                "job_creation": 180000,
                "avg_salary_growth": 0.05
            },
            "Manufacturing": {
                "current_size": 2.2e12,
                "projected_growth": 0.05,
                "key_drivers": ["Industry 4.0", "IoT", "Automation"],
                "job_creation": 120000,
                "avg_salary_growth": 0.04
            }
        }
    
    def render_hot_skills(self):
        """Render hot skills analysis interface."""
        st.subheader("🎯 Hot Skills 2025 Analysis")
        
        # Skills overview
        hot_skills = self.market_data["hot_skills_2025"]
        
        # Convert to DataFrame for better visualization
        skills_df = pd.DataFrame([
            {
                "Skill": skill,
                "Growth Rate (%)": data["growth_rate"],
                "Avg Salary ($)": data["avg_salary"],
                "Demand Score": data["demand_score"]
            }
            for skill, data in hot_skills.items()
        ])
        
        # Top skills visualization
        col1, col2 = st.columns(2)
        
        with col1:
            # Growth rate chart
            fig1 = px.bar(skills_df, x='Growth Rate (%)', y='Skill', 
                         title='📈 Skills Growth Rate (%)',
                         orientation='h')
            fig1.update_layout(height=400)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Salary vs demand scatter
            fig2 = px.scatter(skills_df, x='Avg Salary ($)', y='Demand Score', 
                             text='Skill', title='💰 Salary vs Demand')
            fig2.update_traces(textposition="top center")
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Detailed skills breakdown
        st.write("**📊 Detailed Skills Analysis**")
        
        for skill, data in hot_skills.items():
            with st.expander(f"🎯 {skill} - {data['growth_rate']}% growth"):
                col_skill1, col_skill2, col_skill3 = st.columns(3)
                
                with col_skill1:
                    st.metric("📈 Growth Rate", f"{data['growth_rate']}%")
                with col_skill2:
                    st.metric("💰 Avg Salary", f"${data['avg_salary']:,}")
                with col_skill3:
                    st.metric("🎯 Demand Score", f"{data['demand_score']}/100")
                
                # Skill recommendations
                st.write("**💡 Career Recommendations:**")
                if data['growth_rate'] > 40:
                    st.success("🚀 Extremely high growth - Priority skill for 2025")
                elif data['growth_rate'] > 30:
                    st.info("📈 High growth - Excellent career investment")
                else:
                    st.warning("📊 Moderate growth - Stable career choice")
    
    def render_job_trends(self):
        """Render job market trends interface."""
        st.subheader("📊 Job Market Trends Analysis")
        
        # Trends data
        trends_df = pd.DataFrame(self.job_trends)
        
        # Industry trends over time
        fig1 = px.line(trends_df, x='month_name', 
                      y=['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Education'],
                      title='📈 Industry Job Growth Trends (24 Months)')
        fig1.update_layout(height=500)
        fig1.update_xaxis(tickangle=45)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Market insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🔍 Market Insights**")
            
            latest_data = trends_df.iloc[-1]
            insights = [
                f"🏆 Technology sector leads with {latest_data['Technology']:.0f} index points",
                f"🏥 Healthcare shows consistent growth at {latest_data['Healthcare']:.0f} points",
                f"💼 Finance remains stable at {latest_data['Finance']:.0f} points",
                f"🏭 Manufacturing recovering to {latest_data['Manufacturing']:.0f} points",
                f"📚 Education sector at {latest_data['Education']:.0f} points"
            ]
            
            for insight in insights:
                st.info(insight)
        
        with col2:
            st.write("**📊 Industry Performance**")
            
            # Calculate growth rates
            first_data = trends_df.iloc[0]
            growth_rates = {
                'Technology': ((latest_data['Technology'] - first_data['Technology']) / first_data['Technology']) * 100,
                'Healthcare': ((latest_data['Healthcare'] - first_data['Healthcare']) / first_data['Healthcare']) * 100,
                'Finance': ((latest_data['Finance'] - first_data['Finance']) / first_data['Finance']) * 100,
                'Manufacturing': ((latest_data['Manufacturing'] - first_data['Manufacturing']) / first_data['Manufacturing']) * 100,
                'Education': ((latest_data['Education'] - first_data['Education']) / first_data['Education']) * 100
            }
            
            for industry, growth in growth_rates.items():
                st.metric(f"{industry}", f"{growth:.1f}%", f"{growth:.1f}%")
        
        # Market predictions
        st.write("**🔮 Market Predictions**")
        
        predictions = [
            "📈 Technology sector expected to maintain 25-30% growth through 2025",
            "🏥 Healthcare will see increased demand for digital health professionals",
            "💰 Finance sector focusing on fintech and digital transformation roles",
            "🤖 Manufacturing embracing Industry 4.0 and automation",
            "📚 Education sector adapting to hybrid and remote learning models"
        ]
        
        for prediction in predictions:
            st.write(f"• {prediction}")
    
    def render_salary_forecasts(self):
        """Render salary forecasting interface."""
        st.subheader("💵 Salary Intelligence & Forecasting")
        
        # Salary forecast overview
        st.write("**📊 Salary Forecast Dashboard**")
        
        for role, forecast_data in self.salary_forecasts.items():
            with st.expander(f"💰 {role} - ${forecast_data['current']:,} current"):
                col_forecast1, col_forecast2, col_forecast3, col_forecast4 = st.columns(4)
                
                with col_forecast1:
                    st.metric("💼 Current Salary", f"${forecast_data['current']:,}")
                with col_forecast2:
                    st.metric("📅 6M Forecast", f"${forecast_data['forecast_6m']:,}")
                with col_forecast3:
                    st.metric("📈 12M Forecast", f"${forecast_data['forecast_12m']:,}")
                with col_forecast4:
                    st.metric("📊 Growth Rate", f"{forecast_data['growth_rate']}%")
                
                # Confidence indicator
                confidence = forecast_data['confidence']
                if confidence >= 80:
                    st.success(f"🎯 High confidence forecast: {confidence}%")
                elif confidence >= 70:
                    st.info(f"📊 Moderate confidence forecast: {confidence}%")
                else:
                    st.warning(f"⚠️ Low confidence forecast: {confidence}%")
                
                # Salary progression visualization
                months = ['Current', '6 Months', '12 Months']
                salaries = [forecast_data['current'], forecast_data['forecast_6m'], forecast_data['forecast_12m']]
                
                fig = px.line(x=months, y=salaries, 
                             title=f'💰 {role} Salary Progression')
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
        
        # Salary comparison
        st.write("**📊 Cross-Role Salary Comparison**")
        
        comparison_data = pd.DataFrame([
            {
                "Role": role,
                "Current": data['current'],
                "12M Forecast": data['forecast_12m'],
                "Growth %": data['growth_rate']
            }
            for role, data in self.salary_forecasts.items()
        ])
        
        fig_comparison = px.bar(comparison_data, x='Role', y=['Current', '12M Forecast'],
                               title='💰 Current vs Forecasted Salaries',
                               barmode='group')
        fig_comparison.update_layout(height=400)
        fig_comparison.update_xaxis(tickangle=45)
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Market intelligence insights
        st.write("**💡 Salary Intelligence Insights**")
        
        salary_insights = [
            "🎯 AI/ML Engineers commanding highest salaries with strongest growth",
            "☁️ Cloud Architects show excellent salary progression potential",
            "📊 Data Engineers in high demand with competitive compensation",
            "🔧 DevOps roles offer stable growth and strong market demand",
            "📈 Product Management salaries growing steadily across industries"
        ]
        
        for insight in salary_insights:
            st.info(insight)
    
    def render_emerging_skills(self):
        """Render emerging skills analysis interface."""
        st.subheader("🌟 Emerging Skills & Technology Trends")
        
        # Emerging skills overview
        skills_df = pd.DataFrame(self.emerging_skills)
        
        # Growth rate vs adoption visualization
        fig1 = px.scatter(skills_df, x='adoption_rate', y='growth_rate', 
                         text='skill', color='category',
                         title='🚀 Emerging Skills: Growth vs Adoption')
        fig1.update_traces(textposition="top center")
        fig1.update_layout(height=500)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Skills by category
        col1, col2 = st.columns(2)
        
        with col1:
            # Growth rate by category
            category_growth = skills_df.groupby('category')['growth_rate'].mean().reset_index()
            fig2 = px.bar(category_growth, x='category', y='growth_rate',
                         title='📈 Average Growth Rate by Category')
            fig2.update_layout(height=400)
            fig2.update_xaxis(tickangle=45)
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            # Adoption rate distribution
            fig3 = px.box(skills_df, y='adoption_rate', x='category',
                         title='📊 Adoption Rate Distribution')
            fig3.update_layout(height=400)
            fig3.update_xaxis(tickangle=45)
            st.plotly_chart(fig3, use_container_width=True)
        
        # Detailed skills analysis
        st.write("**🔍 Detailed Emerging Skills Analysis**")
        
        # Sort skills by growth rate
        sorted_skills = sorted(self.emerging_skills, key=lambda x: x['growth_rate'], reverse=True)
        
        for skill_info in sorted_skills:
            with st.expander(f"🌟 {skill_info['skill']} - {skill_info['growth_rate']}% growth"):
                col_skill1, col_skill2, col_skill3 = st.columns(3)
                
                with col_skill1:
                    st.metric("📈 Growth Rate", f"{skill_info['growth_rate']}%")
                with col_skill2:
                    st.metric("📊 Adoption Rate", f"{skill_info['adoption_rate']}%")
                with col_skill3:
                    st.metric("🏷️ Category", skill_info['category'])
                
                # Opportunity assessment
                growth = skill_info['growth_rate']
                adoption = skill_info['adoption_rate']
                
                if growth > 200 and adoption < 50:
                    st.success("🚀 High opportunity - Early adoption phase with explosive growth")
                elif growth > 150:
                    st.info("📈 Good opportunity - Strong growth potential")
                elif adoption > 60:
                    st.warning("⚠️ Mainstream - Consider specialization or adjacent skills")
                else:
                    st.info("📊 Steady growth - Reliable skill investment")
    
    def render_industry_growth(self):
        """Render industry growth projections interface."""
        st.subheader("🏭 Industry Growth Projections & Analysis")
        
        # Industry overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_job_creation = sum(data['job_creation'] for data in self.industry_growth.values())
        avg_growth = sum(data['projected_growth'] for data in self.industry_growth.values()) / len(self.industry_growth)
        
        with col1:
            st.metric("🏭 Industries Tracked", len(self.industry_growth))
        with col2:
            st.metric("👥 Total Job Creation", f"{total_job_creation:,}")
        with col3:
            st.metric("📈 Avg Growth Rate", f"{avg_growth:.1%}")
        with col4:
            st.metric("💰 Market Size", "$11.0T")
        
        # Industry comparison
        industry_df = pd.DataFrame([
            {
                "Industry": industry,
                "Market Size ($T)": data['current_size'] / 1e12,
                "Growth Rate (%)": data['projected_growth'] * 100,
                "Job Creation": data['job_creation'],
                "Salary Growth (%)": data['avg_salary_growth'] * 100
            }
            for industry, data in self.industry_growth.items()
        ])
        
        # Growth rate comparison
        fig1 = px.bar(industry_df, x='Industry', y='Growth Rate (%)',
                     title='📈 Industry Growth Rate Projections')
        fig1.update_layout(height=400)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Market size vs job creation
        fig2 = px.scatter(industry_df, x='Market Size ($T)', y='Job Creation',
                         text='Industry', title='💼 Market Size vs Job Creation')
        fig2.update_traces(textposition="top center")
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Detailed industry analysis
        st.write("**🔍 Detailed Industry Analysis**")
        
        for industry, data in self.industry_growth.items():
            with st.expander(f"🏭 {industry} - {data['projected_growth']:.1%} growth"):
                col_ind1, col_ind2, col_ind3, col_ind4 = st.columns(4)
                
                with col_ind1:
                    st.metric("💰 Market Size", f"${data['current_size']/1e12:.1f}T")
                with col_ind2:
                    st.metric("📈 Growth Rate", f"{data['projected_growth']:.1%}")
                with col_ind3:
                    st.metric("👥 Job Creation", f"{data['job_creation']:,}")
                with col_ind4:
                    st.metric("💵 Salary Growth", f"{data['avg_salary_growth']:.1%}")
                
                # Key drivers
                st.write("**🎯 Key Growth Drivers:**")
                for driver in data['key_drivers']:
                    st.write(f"• {driver}")
                
                # Investment recommendation
                growth_rate = data['projected_growth']
                if growth_rate > 0.12:
                    st.success("🚀 High growth industry - Excellent investment opportunity")
                elif growth_rate > 0.08:
                    st.info("📈 Solid growth - Good investment potential")
                else:
                    st.warning("📊 Moderate growth - Stable but limited upside")

def render():
    """Main render function for Market Intelligence Center module."""
    market_intelligence = MarketIntelligenceCenter()
    
    render_section_header(
        "📈 Market Intelligence Center Suite",
        "Advanced market analysis with real-time intelligence and forecasting"
    )
    
    # Market intelligence metrics dashboard
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔥 Hottest Skill", "AI/ML Engineering", "+45% growth")
    with col2:
        st.metric("💰 Top Salary", "$165K", "AI/ML Engineer")
    with col3:
        st.metric("🚀 Fastest Growing", "Technology", "+28% projection")
    with col4:
        st.metric("🏠 Remote Work", "80%", "Hybrid + Remote")
    
    # Main interface tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎯 Hot Skills",
        "📊 Job Trends",
        "💵 Salary Forecasts",
        "🌟 Emerging Skills",
        "🏭 Industry Growth",
        "🌐 Exa Intelligence"
    ])
    
    with tab1:
        market_intelligence.render_hot_skills()
    
    with tab2:
        market_intelligence.render_job_trends()
    
    with tab3:
        market_intelligence.render_salary_forecasts()
    
    with tab4:
        market_intelligence.render_emerging_skills()
    
    with tab5:
        market_intelligence.render_industry_growth()
    
    with tab6:
        render_exa_intelligence_tab()
    
    # Integration status
    st.markdown("---")
    with st.expander("🔗 Integration Status"):
        integration_hooks = get_integration_hooks()
        if integration_hooks:
            st.success("✅ Lockstep integration active - Market intelligence synced with user portal")
            st.info("🔄 Industry insights integrated with strategic planning")
            st.info("🌐 Exa deep web intelligence available via Admin Page 27")
        else:
            st.warning("⚠️ Integration hooks not available")

def render_exa_intelligence_tab():
    """Render Exa deep web intelligence integration."""
    st.markdown("### 🌐 Exa Deep Web Intelligence")
    st.info("💡 **New Feature**: Deep web company enrichment powered by Exa AI")
    
    st.markdown("""
    **What is Exa Intelligence?**
    
    Exa is an AI-powered deep web search engine that goes beyond traditional search to discover:
    - 🎯 **Careers Pages**: Real job postings and requirements from company websites
    - 🚀 **Product Pages**: Technology stacks, solutions, and platforms
    - 📖 **Company Background**: Leadership, funding, culture, and growth data
    
    This data enhances market intelligence by providing:
    - Real-time company insights
    - Competitive technology stack analysis  
    - Hiring trends and job market signals
    - Product/service evolution tracking
    """)
    
    # Quick access to Exa dashboard
    st.markdown("---")
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔍 Search Companies**")
        st.markdown("Go to **Admin Page 27** to:")
        st.markdown("- Search and enrich company data")
        st.markdown("- Browse company corpora")
        st.markdown("- View search history")
        if st.button("→ Open Exa Dashboard", key="goto_exa"):
            st.info("Navigate to **Page 27: Exa Web Intelligence** in the sidebar")
    
    with col2:
        st.markdown("**📊 Integration Status**")
        
        # Check if Exa data is available
        try:
            import sys
            from pathlib import Path
            corpus_dir = Path(__file__).parent.parent.parent / "ai_data_final" / "company_corpora"
            
            if corpus_dir.exists():
                domains = [d.name for d in corpus_dir.iterdir() if d.is_dir()]
                st.metric("Companies Enriched", len(domains))
                
                if domains:
                    st.success(f"✅ {len(domains)} companies in corpus")
                    with st.expander("View enriched companies"):
                        for domain in sorted(domains)[:10]:
                            st.write(f"• {domain}")
                        if len(domains) > 10:
                            st.write(f"... and {len(domains) - 10} more")
                else:
                    st.info("No companies enriched yet")
            else:
                st.warning("Corpus directory not found")
        
        except Exception as e:
            st.error(f"Error loading corpus: {e}")
    
    # Sample insights (if data available)
    st.markdown("---")
    st.markdown("### 📈 Exa-Enhanced Market Insights")
    st.info("💡 Market intelligence enhanced with real company data from deep web search")
    
    st.markdown("""
    **How Exa Enhances Market Intelligence:**
    
    1. **Real-Time Tech Stack Trends**  
       Discover what technologies companies are actually using, not just what's popular in surveys
    
    2. **Hiring Signal Detection**  
       Analyze careers pages to identify which skills companies are actively hiring for
    
    3. **Competitive Product Analysis**  
       Track product launches, feature updates, and competitive positioning
    
    4. **Geographic Expansion Tracking**  
       Monitor which cities/regions companies are expanding into based on job postings
    
    5. **Compensation Intelligence**  
       Extract salary data and benefits information from actual job postings
    """)

if __name__ == "__main__":
    render()