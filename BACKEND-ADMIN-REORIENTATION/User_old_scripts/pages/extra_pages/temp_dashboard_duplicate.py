"""
🏠 IntelliCV User Portal - Enhanced Landing Dashboard
===================================================

Main dashboard showcasing the comprehensive career intelligence platform with:
- Career quadrant positioning visualization
- Daily engagement touchpoints
- Progress tracking and analytics
- Quick access to all platform features
- Personalized recommendations

This serves as the main entry point after authentication.
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
    page_title="IntelliCV Dashboard | Your Career Intelligence Hub",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

class DashboardEngine:
    """Main dashboard data and analytics engine"""
    
    def __init__(self):
        self.user_data = self._load_user_data()
        self.platform_stats = self._load_platform_stats()
        self.recommendations = self._generate_recommendations()
        
    def _load_user_data(self) -> Dict[str, Any]:
        """Load user profile and progress data"""
        return {
            "profile": {
                "name": "Alex Thompson",
                "title": "Senior Software Engineer",
                "experience_years": 6,
                "target_role": "Engineering Manager",
                "location": "Seattle, WA",
                "skills": ["Python", "JavaScript", "Cloud Architecture", "Team Leadership"]
            },
            "career_position": {
                "skills_score": 78,
                "market_demand": 85,
                "quadrant": "Star Performer",
                "peer_percentile": 82
            },
            "engagement": {
                "level": "Active Champion",
                "points": 1250,
                "streak_days": 12,
                "completed_modules": 8,
                "total_modules": 12
            },
            "recent_activity": [
                {"date": "2025-10-01", "activity": "Completed AI Interview Practice", "points": 50},
                {"date": "2025-09-30", "activity": "Updated Career Profile", "points": 25},
                {"date": "2025-09-29", "activity": "Connected with Mentor", "points": 75},
                {"date": "2025-09-28", "activity": "Salary Analysis Completed", "points": 40}
            ]
        }
    
    def _load_platform_stats(self) -> Dict[str, Any]:
        """Load platform-wide statistics"""
        return {
            "community": {
                "total_users": 12500,
                "active_mentors": 850,
                "successful_transitions": 2100,
                "interview_sessions": 15600
            },
            "trending": [
                {"feature": "AI Interview Coach", "growth": "+45%", "users": 3200},
                {"feature": "Career Intelligence", "growth": "+38%", "users": 2800},
                {"feature": "Mentorship Hub", "growth": "+52%", "users": 1900},
                {"feature": "Salary Intelligence", "growth": "+29%", "users": 2400}
            ]
        }
    
    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        """Generate personalized recommendations"""
        return [
            {
                "type": "skill_development",
                "priority": "high",
                "title": "Develop System Design Skills",
                "description": "Based on your target role as Engineering Manager, system design is crucial.",
                "action": "Start System Design Course",
                "estimated_time": "4 weeks",
                "impact_score": 85
            },
            {
                "type": "networking",
                "priority": "medium", 
                "title": "Connect with Engineering Managers",
                "description": "Expand your network with professionals in your target role.",
                "action": "Join Engineering Leadership Community",
                "estimated_time": "1 hour",
                "impact_score": 72
            },
            {
                "type": "interview_prep",
                "priority": "high",
                "title": "Practice Leadership Interviews",
                "description": "Leadership interviews require different preparation than technical ones.",
                "action": "Use AI Interview Coach",
                "estimated_time": "2 hours/week",
                "impact_score": 90
            }
        ]

def create_career_quadrant_mini(user_position: Dict) -> go.Figure:
    """Create mini career quadrant for dashboard"""
    
    fig = go.Figure()
    
    # Add quadrant background
    quadrants = [
        {"x": [0, 50], "y": [0, 50], "color": "rgba(255, 200, 200, 0.3)"},
        {"x": [50, 100], "y": [0, 50], "color": "rgba(255, 255, 200, 0.3)"},
        {"x": [0, 50], "y": [50, 100], "color": "rgba(200, 255, 200, 0.3)"},
        {"x": [50, 100], "y": [50, 100], "color": "rgba(200, 200, 255, 0.3)"}
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
    
    # Add dividing lines
    fig.add_hline(y=50, line_dash="dash", line_color="gray", line_width=1)
    fig.add_vline(x=50, line_dash="dash", line_color="gray", line_width=1)
    
    # Add user position
    fig.add_trace(go.Scatter(
        x=[user_position["market_demand"]],
        y=[user_position["skills_score"]],
        mode='markers',
        marker=dict(
            size=20,
            color='red',
            symbol='star',
            line=dict(width=3, color='darkred')
        ),
        name='Your Position',
        hovertemplate=f'<b>Your Position</b><br>Skills: %{{y}}<br>Market Demand: %{{x}}<br>Quadrant: {user_position["quadrant"]}<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title='Market Demand',
        yaxis_title='Skills Score',
        xaxis=dict(range=[0, 100], showgrid=False),
        yaxis=dict(range=[0, 100], showgrid=False),
        plot_bgcolor='white',
        width=300,
        height=250,
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False
    )
    
    return fig

def create_progress_chart(engagement_data: Dict) -> go.Figure:
    """Create progress tracking chart"""
    
    # Sample weekly progress data
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    completed = [3, 2, 4, 3, 2, 1, 3]
    target = [3, 3, 3, 3, 3, 2, 2]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=days,
        y=completed,
        name='Completed',
        marker_color='green',
        opacity=0.8
    ))
    
    fig.add_trace(go.Scatter(
        x=days,
        y=target,
        mode='lines+markers',
        name='Target',
        line=dict(color='red', dash='dash'),
        marker=dict(color='red')
    ))
    
    fig.update_layout(
        title='This Week\'s Activity',
        xaxis_title='Day',
        yaxis_title='Activities Completed',
        height=250,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    return fig

def main():
    """Main dashboard interface"""
    
    # Initialize dashboard engine
    dashboard = DashboardEngine()
    user_data = dashboard.user_data
    
    # Header with personalized greeting
    current_hour = datetime.now().hour
    greeting = "Good morning" if current_hour < 12 else "Good afternoon" if current_hour < 18 else "Good evening"
    
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px;">
        <h1 style="color: white; margin: 0;">{greeting}, {user_data['profile']['name']}! 👋</h1>
        <p style="color: white; margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">
            Ready to accelerate your career journey? Let's make today count! 🚀
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats overview
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Career Level",
            user_data['engagement']['level'],
            delta=f"🔥 {user_data['engagement']['streak_days']} day streak"
        )
    
    with col2:
        completion_rate = (user_data['engagement']['completed_modules'] / user_data['engagement']['total_modules']) * 100
        st.metric(
            "Platform Progress",
            f"{completion_rate:.0f}%",
            delta=f"{user_data['engagement']['completed_modules']}/{user_data['engagement']['total_modules']} modules"
        )
    
    with col3:
        st.metric(
            "Career Quadrant",
            user_data['career_position']['quadrant'],
            delta=f"Top {100-user_data['career_position']['peer_percentile']}%"
        )
    
    with col4:
        st.metric(
            "Engagement Points",
            f"{user_data['engagement']['points']:,}",
            delta="+150 this week"
        )
    
    with col5:
        next_milestone = ((user_data['engagement']['points'] // 500) + 1) * 500
        points_to_next = next_milestone - user_data['engagement']['points']
        st.metric(
            "Next Milestone",
            f"{points_to_next} points",
            delta="Champion Level"
        )
    
    # Main dashboard content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Career positioning section
        st.markdown("### 🎯 Your Career Position")
        
        subcol1, subcol2 = st.columns([1, 1])
        
        with subcol1:
            # Mini career quadrant
            quadrant_chart = create_career_quadrant_mini(user_data['career_position'])
            st.plotly_chart(quadrant_chart, use_container_width=True)
        
        with subcol2:
            st.markdown(f"""
            **Current Quadrant:** {user_data['career_position']['quadrant']} 🌟  
            **Skills Score:** {user_data['career_position']['skills_score']}/100  
            **Market Demand:** {user_data['career_position']['market_demand']}/100  
            **Peer Ranking:** Top {100-user_data['career_position']['peer_percentile']}%
            """)
            
            if st.button("📊 View Full Career Analytics", use_container_width=True):
                st.session_state.current_page = "Career_Intelligence"
                st.rerun()
        
        # Activity progress
        st.markdown("### 📈 This Week's Progress")
        
        progress_chart = create_progress_chart(user_data['engagement'])
        st.plotly_chart(progress_chart, use_container_width=True)
    
    with col2:
        # Daily touchpoints
        st.markdown("### 🎯 Today's Opportunities")
        
        # Today's challenges
        touchpoints = [
            {"title": "💡 Daily Career Insight", "points": 5, "completed": False},
            {"title": "🤝 Network Connection", "points": 10, "completed": True},
            {"title": "🧠 Skill Challenge", "points": 15, "completed": False}
        ]
        
        for touchpoint in touchpoints:
            status = "✅" if touchpoint['completed'] else "⭐"
            
            if touchpoint['completed']:
                st.success(f"{status} {touchpoint['title']} (+{touchpoint['points']} pts)")
            else:
                if st.button(f"{status} {touchpoint['title']} (+{touchpoint['points']} pts)", key=touchpoint['title']):
                    st.success("Great job! Challenge completed! 🎉")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🎯 Start Interview Practice", use_container_width=True):
            st.session_state.current_page = "AI_Interview_Coach"
            st.rerun()
        
        if st.button("🤝 Find Mentors", use_container_width=True):
            st.session_state.current_page = "Mentorship_Hub"
            st.rerun()
        
        if st.button("💰 Salary Analysis", use_container_width=True):
            st.session_state.current_page = "Advanced_Career_Tools"
            st.rerun()
    
    # Recommendations section
    st.markdown("### 🎯 Personalized Recommendations")
    
    recommendations = dashboard.recommendations
    
    for i, rec in enumerate(recommendations):
        priority_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        
        with st.expander(f"{priority_color[rec['priority']]} {rec['title']} (Impact: {rec['impact_score']}/100)", expanded=i==0):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(rec['description'])
                st.info(f"⏱️ Estimated time: {rec['estimated_time']}")
            
            with col2:
                if st.button(rec['action'], key=f"rec_{i}"):
                    # Route to appropriate page based on recommendation type
                    if rec['type'] == 'interview_prep':
                        st.session_state.current_page = "AI_Interview_Coach"
                    elif rec['type'] == 'networking':
                        st.session_state.current_page = "Mentorship_Hub"
                    elif rec['type'] == 'skill_development':
                        st.session_state.current_page = "Advanced_Career_Tools"
                    st.rerun()
    
    # Recent activity and community highlights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Recent Activity")
        
        for activity in user_data['recent_activity'][:4]:
            st.markdown(f"""
            **{activity['date']}**  
            {activity['activity']} (+{activity['points']} pts)
            """)
    
    with col2:
        st.markdown("### 🏆 Platform Highlights")
        
        platform_stats = dashboard.platform_stats
        
        for stat in platform_stats['trending'][:3]:
            st.markdown(f"""
            **{stat['feature']}** {stat['growth']}  
            {stat['users']:,} active users
            """)
        
        st.info(f"🎉 Join {platform_stats['community']['total_users']:,} professionals advancing their careers!")
    
    # Feature discovery section
    st.markdown("### 🚀 Discover Platform Features")
    
    feature_cols = st.columns(4)
    
    features = [
        {
            "name": "AI Interview Coach",
            "icon": "🎯",
            "description": "Practice with AI feedback",
            "page": "AI_Interview_Coach",
            "users": "3.2K users"
        },
        {
            "name": "Career Intelligence", 
            "icon": "📊",
            "description": "Quadrant positioning",
            "page": "Career_Intelligence",
            "users": "2.8K users"
        },
        {
            "name": "Mentorship Hub",
            "icon": "🤝", 
            "description": "Connect with mentors",
            "page": "Mentorship_Hub",
            "users": "1.9K users"
        },
        {
            "name": "Career Tools",
            "icon": "🛠️",
            "description": "Salary & market analysis",
            "page": "Advanced_Career_Tools", 
            "users": "2.4K users"
        }
    ]
    
    for i, feature in enumerate(features):
        with feature_cols[i]:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 10px; 
                        border: 1px solid #e0e0e0; text-align: center; height: 160px;">
                <div style="font-size: 30px; margin-bottom: 10px;">{feature['icon']}</div>
                <h4 style="margin: 10px 0;">{feature['name']}</h4>
                <p style="font-size: 14px; color: #666; margin: 5px 0;">{feature['description']}</p>
                <p style="font-size: 12px; color: #999;">{feature['users']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Explore {feature['name']}", key=f"feature_{i}", use_container_width=True):
                st.session_state.current_page = feature['page']
                st.rerun()

if __name__ == "__main__":
    main()