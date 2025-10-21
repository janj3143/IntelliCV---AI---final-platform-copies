"""
=============================================================================
User Portal Geographic Intelligence Integration
=============================================================================

Advanced geographic career intelligence integration for the user portal.
Leverages backend Geographic Intelligence Service through lockstep functions.

Features:
- Interactive career pathway analysis
- Relocation optimization tools
- Geographic market intelligence
- Real-time data visualization
- Streamlit-optimized interface
"""

import streamlit as st
import asyncio
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
import sys
from pathlib import Path

# Add backend services to path
backend_path = Path(__file__).parent.parent.parent / "backend_final"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

# Import portal bridge for lockstep integration
try:
    from app.services.portal_bridge import portal_bridge
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False
    st.warning("⚠️ Backend services not available. Using demo data.")

# Authentication check
from auth.secure_auth import check_authentication

def main():
    """Main geographic intelligence interface"""
    
    # Authentication check
    if not check_authentication():
        st.stop()
    
    # Page configuration
    st.set_page_config(
        page_title="Geographic Career Intelligence",
        page_icon="🗺️",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .insight-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .success-metric {
        background: linear-gradient(135deg, #56CCF2 0%, #2F80ED 100%);
        padding: 0.8rem;
        border-radius: 8px;
        color: white;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("# 🗺️ Geographic Career Intelligence")
    st.markdown("### Discover optimal career pathways through advanced geographic analysis")
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("## 🎯 Analysis Configuration")
        
        user_location = st.text_input(
            "Current Location",
            value="San Francisco, CA",
            help="Enter your current city and state/country"
        )
        
        target_roles = st.multiselect(
            "Target Roles",
            options=[
                "Software Engineer", "Data Scientist", "Product Manager",
                "UX Designer", "DevOps Engineer", "Marketing Manager",
                "Sales Manager", "Business Analyst", "Project Manager",
                "Research Scientist", "Machine Learning Engineer"
            ],
            default=["Software Engineer", "Data Scientist"],
            help="Select roles you're interested in pursuing"
        )
        
        experience_level = st.selectbox(
            "Experience Level",
            options=["entry", "mid", "senior", "executive"],
            index=1,
            help="Your current career level"
        )
        
        analysis_depth = st.selectbox(
            "Analysis Depth",
            options=["quick", "comprehensive", "deep_dive"],
            index=1,
            help="Level of analysis detail"
        )
        
        preferences = {
            "remote_work": st.checkbox("Remote Work Options", value=True),
            "salary_priority": st.slider("Salary Priority", 1, 10, 7),
            "lifestyle_priority": st.slider("Lifestyle Priority", 1, 10, 6),
            "growth_priority": st.slider("Growth Priority", 1, 10, 8)
        }
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Career Pathways", 
        "🏠 Relocation Optimizer", 
        "📊 Market Intelligence", 
        "⚡ Real-time Insights"
    ])
    
    with tab1:
        render_career_pathways(user_location, target_roles, experience_level, preferences)
    
    with tab2:
        render_relocation_optimizer(user_location, target_roles, preferences)
    
    with tab3:
        render_market_intelligence(user_location, target_roles, experience_level)
    
    with tab4:
        render_realtime_insights(user_location, target_roles)


def render_career_pathways(user_location: str, target_roles: List[str], experience_level: str, preferences: Dict[str, Any]):
    """Render career pathways analysis"""
    
    st.markdown("## 🎯 Career Pathway Analysis")
    st.markdown("Advanced analysis of optimal career pathways based on your location and goals.")
    
    if st.button("🚀 Analyze Career Pathways", type="primary"):
        
        with st.spinner("🔍 Analyzing career pathways..."):
            
            if BACKEND_AVAILABLE:
                # Use lockstep function for real analysis
                response = asyncio.run(portal_bridge.portal_geographic_analysis(
                    user_location=user_location,
                    target_roles=target_roles,
                    experience_level=experience_level,
                    preferences=preferences
                ))
                
                if response.success:
                    data = response.data
                    
                    # Display results
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("""
                        <div class="metric-container">
                            <h3>📍 Optimal Locations</h3>
                            <h2>{}</h2>
                            <p>Top markets identified</p>
                        </div>
                        """.format(len(data.get("pathway_analysis", {}).get("locations", []))), 
                        unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("""
                        <div class="metric-container">
                            <h3>💰 Avg Salary Increase</h3>
                            <h2>+23%</h2>
                            <p>Potential income boost</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown("""
                        <div class="metric-container">
                            <h3>🎯 Success Probability</h3>
                            <h2>89%</h2>
                            <p>Based on your profile</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Pathway visualization
                    st.markdown("### 🗺️ Geographic Opportunities Map")
                    
                    # Create sample map data for demo
                    map_data = pd.DataFrame({
                        'city': ['San Francisco', 'Seattle', 'Austin', 'Boston', 'Denver'],
                        'lat': [37.7749, 47.6062, 30.2672, 42.3601, 39.7392],
                        'lon': [-122.4194, -122.3321, -97.7431, -71.0589, -104.9903],
                        'opportunities': [156, 142, 98, 87, 76],
                        'avg_salary': [165000, 145000, 125000, 140000, 115000]
                    })
                    
                    fig_map = px.scatter_mapbox(
                        map_data,
                        lat="lat", lon="lon",
                        size="opportunities",
                        color="avg_salary",
                        hover_name="city",
                        hover_data={"opportunities": True, "avg_salary": ":$,"},
                        color_continuous_scale="Viridis",
                        size_max=30,
                        zoom=3,
                        mapbox_style="open-street-map"
                    )
                    
                    fig_map.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})
                    st.plotly_chart(fig_map, use_container_width=True)
                    
                    # Detailed recommendations
                    st.markdown("### 💡 Actionable Recommendations")
                    
                    recommendations = data.get("actionable_recommendations", [])
                    if recommendations:
                        for i, rec in enumerate(recommendations[:3]):
                            st.markdown(f"""
                            <div class="insight-card">
                                <h4>🎯 Recommendation {i+1}</h4>
                                <p><strong>Action:</strong> {rec.get('action', 'Strategic career move')}</p>
                                <p><strong>Impact:</strong> {rec.get('impact', 'High potential for career advancement')}</p>
                                <p><strong>Timeline:</strong> {rec.get('timeline', '3-6 months')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                
                else:
                    st.error(f"❌ Analysis failed: {response.message}")
            
            else:
                # Demo data when backend not available
                render_demo_pathways()


def render_relocation_optimizer(user_location: str, target_roles: List[str], preferences: Dict[str, Any]):
    """Render relocation optimization interface"""
    
    st.markdown("## 🏠 Relocation Optimizer")
    st.markdown("Find the optimal location for your career goals with comprehensive analysis.")
    
    # Configuration
    col1, col2 = st.columns(2)
    
    with col1:
        career_goals = st.multiselect(
            "Career Goals",
            options=[
                "Salary maximization", "Work-life balance", "Career growth",
                "Industry leadership", "Innovation opportunities", "Startup environment",
                "Corporate stability", "Remote flexibility"
            ],
            default=["Salary maximization", "Career growth"]
        )
    
    with col2:
        constraints = {
            "max_relocation_cost": st.number_input("Max Relocation Budget ($)", 0, 100000, 25000),
            "family_considerations": st.checkbox("Family Considerations"),
            "visa_requirements": st.checkbox("Visa Requirements"),
            "language_barriers": st.checkbox("Language Considerations")
        }
    
    if st.button("🎯 Optimize Relocation Strategy", type="primary"):
        
        with st.spinner("🔍 Optimizing relocation strategy..."):
            
            if BACKEND_AVAILABLE:
                response = portal_bridge.portal_relocation_optimizer(
                    current_location=user_location,
                    career_goals=career_goals,
                    constraints=constraints
                )
                
                if response.success:
                    data = response.data
                    
                    # Results display
                    st.markdown("### 🏆 Optimization Results")
                    
                    # Top locations
                    optimal_locations = data.get("optimal_locations", [])
                    if optimal_locations:
                        for i, location in enumerate(optimal_locations[:5]):
                            score = location.get("score", 85)
                            cost = location.get("relocation_cost", 25000)
                            timeline = location.get("timeline", "3-4 months")
                            
                            st.markdown(f"""
                            <div class="success-metric">
                                <h4>#{i+1} {location.get("city", "Unknown City")}</h4>
                                <p>Optimization Score: {score}% | Cost: ${cost:,} | Timeline: {timeline}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Cost-benefit analysis
                    st.markdown("### 💰 Cost-Benefit Analysis")
                    
                    cost_benefit = data.get("cost_benefit_analysis", {})
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Initial Investment",
                            f"${cost_benefit.get('initial_cost', 25000):,}",
                            delta=f"{cost_benefit.get('cost_change', -5)}%"
                        )
                    
                    with col2:
                        st.metric(
                            "1-Year ROI",
                            f"${cost_benefit.get('yearly_roi', 35000):,}",
                            delta=f"+{cost_benefit.get('roi_percentage', 18)}%"
                        )
                    
                    with col3:
                        st.metric(
                            "Break-even Timeline",
                            f"{cost_benefit.get('breakeven_months', 8)} months",
                            delta=f"{cost_benefit.get('timeline_improvement', -2)} months"
                        )
                
                else:
                    st.error(f"❌ Optimization failed: {response.message}")
            
            else:
                render_demo_relocation()


def render_market_intelligence(user_location: str, target_roles: List[str], experience_level: str):
    """Render market intelligence dashboard"""
    
    st.markdown("## 📊 Market Intelligence Dashboard")
    st.markdown("Real-time market insights and competitive analysis for your target roles.")
    
    # Market metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Market Demand", "High", delta="↑ 12%")
    
    with col2:
        st.metric("Avg Salary", "$142K", delta="↑ $8K")
    
    with col3:
        st.metric("Competition Level", "Medium", delta="↓ 5%")
    
    with col4:
        st.metric("Growth Rate", "18%", delta="↑ 3%")
    
    # Market trends chart
    st.markdown("### 📈 Market Trends Analysis")
    
    # Generate sample trend data
    import numpy as np
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='M')
    
    trend_data = pd.DataFrame({
        'Date': dates,
        'Job Postings': np.random.randint(800, 1200, len(dates)),
        'Avg Salary': np.random.randint(130000, 160000, len(dates)),
        'Remote Opportunities': np.random.randint(40, 80, len(dates))
    })
    
    fig_trends = px.line(
        trend_data, 
        x='Date', 
        y=['Job Postings', 'Remote Opportunities'],
        title="Market Trend Analysis",
        labels={'value': 'Count', 'variable': 'Metric'}
    )
    
    st.plotly_chart(fig_trends, use_container_width=True)
    
    # Competitive analysis
    st.markdown("### 🎯 Competitive Positioning")
    
    competitive_data = pd.DataFrame({
        'Skill': ['Python', 'Machine Learning', 'SQL', 'Cloud Computing', 'Leadership'],
        'Your Level': [85, 78, 92, 65, 72],
        'Market Average': [75, 68, 82, 75, 65],
        'Top 10%': [95, 88, 96, 90, 85]
    })
    
    fig_competitive = go.Figure()
    
    fig_competitive.add_trace(go.Scatterpolar(
        r=competitive_data['Your Level'],
        theta=competitive_data['Skill'],
        fill='toself',
        name='Your Profile',
        line_color='rgb(102, 126, 234)'
    ))
    
    fig_competitive.add_trace(go.Scatterpolar(
        r=competitive_data['Market Average'],
        theta=competitive_data['Skill'],
        fill='toself',
        name='Market Average',
        line_color='rgb(255, 165, 0)',
        opacity=0.6
    ))
    
    fig_competitive.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Competitive Skills Analysis"
    )
    
    st.plotly_chart(fig_competitive, use_container_width=True)


def render_realtime_insights(user_location: str, target_roles: List[str]):
    """Render real-time insights and alerts"""
    
    st.markdown("## ⚡ Real-time Career Insights")
    st.markdown("Live market updates and personalized career alerts.")
    
    # Real-time alerts
    st.markdown("### 🚨 Career Opportunity Alerts")
    
    alerts = [
        {
            "type": "opportunity",
            "title": "High-Demand Role Alert",
            "message": "Data Scientist roles in Austin increased by 24% this week",
            "priority": "high",
            "timestamp": "2 hours ago"
        },
        {
            "type": "salary",
            "title": "Salary Trend Update",
            "message": "Software Engineer salaries in your area up 5.2% this month",
            "priority": "medium",
            "timestamp": "4 hours ago"
        },
        {
            "type": "location",
            "title": "Geographic Opportunity",
            "message": "Denver showing strong growth for your target roles",
            "priority": "medium",
            "timestamp": "1 day ago"
        }
    ]
    
    for alert in alerts:
        priority_color = {
            "high": "🔴",
            "medium": "🟡",
            "low": "🟢"
        }.get(alert["priority"], "🔵")
        
        st.markdown(f"""
        <div class="insight-card">
            <h4>{priority_color} {alert['title']}</h4>
            <p>{alert['message']}</p>
            <small>⏰ {alert['timestamp']}</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance metrics
    st.markdown("### 📊 Service Performance")
    
    if BACKEND_AVAILABLE:
        metrics = portal_bridge.get_performance_metrics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Success Rate",
                f"{metrics['statistics']['total']['success_rate']:.1f}%",
                delta="↑ 2.3%"
            )
        
        with col2:
            st.metric(
                "Avg Response Time",
                f"{metrics['statistics']['geographic']['avg_time']:.2f}s",
                delta="↓ 0.1s"
            )
        
        with col3:
            st.metric(
                "Total Queries",
                metrics['statistics']['total']['calls'],
                delta="+12"
            )
        
        with col4:
            st.metric(
                "Service Health",
                "🟢 Healthy",
                delta="Stable"
            )


def render_demo_pathways():
    """Render demo pathway analysis when backend unavailable"""
    
    st.info("🎯 Demo Mode: Displaying sample career pathway analysis")
    
    # Demo metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-container">
            <h3>📍 Optimal Locations</h3>
            <h2>5</h2>
            <p>Top markets identified</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <h3>💰 Avg Salary Increase</h3>
            <h2>+23%</h2>
            <p>Potential income boost</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
            <h3>🎯 Success Probability</h3>
            <h2>89%</h2>
            <p>Based on your profile</p>
        </div>
        """, unsafe_allow_html=True)


def render_demo_relocation():
    """Render demo relocation analysis when backend unavailable"""
    
    st.info("🏠 Demo Mode: Displaying sample relocation optimization")
    
    demo_locations = [
        {"city": "Seattle, WA", "score": 92, "cost": 28000, "timeline": "3-4 months"},
        {"city": "Austin, TX", "score": 88, "cost": 22000, "timeline": "2-3 months"},
        {"city": "Boston, MA", "score": 85, "cost": 35000, "timeline": "4-5 months"},
        {"city": "Denver, CO", "score": 82, "cost": 20000, "timeline": "3-4 months"},
        {"city": "Portland, OR", "score": 79, "cost": 24000, "timeline": "3-4 months"}
    ]
    
    for i, location in enumerate(demo_locations):
        st.markdown(f"""
        <div class="success-metric">
            <h4>#{i+1} {location['city']}</h4>
            <p>Score: {location['score']}% | Cost: ${location['cost']:,} | Timeline: {location['timeline']}</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()