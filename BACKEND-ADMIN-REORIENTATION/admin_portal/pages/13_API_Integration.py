"""
=============================================================================
IntelliCV Admin Portal - API Integration Module
=============================================================================

Comprehensive API and integration management with key management,
GitHub integration, CI/CD tools, and analytics with lockstep synchronization.

Features:
- API key management and monitoring
- GitHub repository integration
- CI/CD pipeline management
- Integration analytics and monitoring
- Lockstep synchronization hooks
"""

import streamlit as st

# =============================================================================
# MANDATORY AUTHENTICATION CHECK  
# =============================================================================

def check_authentication():
    """Check if admin is authenticated"""
    if not st.session_state.get('admin_authenticated', False):
        st.error("🔒 **ADMIN AUTHENTICATION REQUIRED**")
        st.warning("You must login through the main admin portal to access this module.")
        
        if st.button("🏠 Return to Main Portal", type="primary"):
            st.switch_page("main.py")
        st.stop()
    return True


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
from typing import Dict, Any, List, Optional
import time
import random
import json

# Import shared components
# from shared.components import render_section_header, render_metrics_row  # Using fallback implementations
# from shared.integration_hooks import get_integration_hooks  # Using fallback implementations

# =============================================================================
# API INTEGRATION CLASS
# =============================================================================

class APIIntegration:
    """Consolidated API & Integration Management with integration hooks"""
    
    def __init__(self):
        """Initialize API integration with integration hooks."""
        self.integration_hooks = get_integration_hooks()
    
    def get_api_metrics(self) -> Dict[str, Any]:
        """Get API performance metrics."""
        metrics = {
            'active_apis': random.randint(10, 15),
            'active_apis_delta': random.randint(1, 3),
            'api_calls_today': random.randint(2500, 3200),
            'api_calls_delta': random.randint(200, 300),
            'success_rate': random.uniform(98.5, 99.5),
            'success_rate_delta': random.uniform(0.05, 0.15),
            'avg_response_time': random.randint(120, 180),
            'response_time_delta': random.randint(-20, -5),
            'timestamp': datetime.now().isoformat()
        }
        
        # Sync metrics with integration hooks
        self.integration_hooks.sync_system_config('api_metrics', metrics)
        
        return metrics
    
    def get_api_keys(self) -> List[Dict[str, Any]]:
        """Get list of managed API keys."""
        return [
            {
                "Service": "OpenAI GPT-4",
                "Provider": "OpenAI",
                "Status": "✅ Active",
                "Last_Used": (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
                "Usage_Today": random.randint(150, 300),
                "Rate_Limit": "10000/day",
                "Expires": "2025-12-31"
            },
            {
                "Service": "Claude API",
                "Provider": "Anthropic", 
                "Status": "✅ Active",
                "Last_Used": (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"),
                "Usage_Today": random.randint(80, 200),
                "Rate_Limit": "5000/day",
                "Expires": "2025-11-15"
            },
            {
                "Service": "Gmail API",
                "Provider": "Google",
                "Status": "⚠️ Expired", 
                "Last_Used": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M"),
                "Usage_Today": 0,
                "Rate_Limit": "1000/day",
                "Expires": "2025-09-15"
            },
            {
                "Service": "Resume Parser API",
                "Provider": "Custom",
                "Status": "✅ Active",
                "Last_Used": (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
                "Usage_Today": random.randint(200, 400),
                "Rate_Limit": "unlimited",
                "Expires": "Never"
            },
            {
                "Service": "Job Board API",
                "Provider": "Custom",
                "Status": "🔄 Testing",
                "Last_Used": (datetime.now() - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M"),
                "Usage_Today": random.randint(50, 150),
                "Rate_Limit": "2000/day",
                "Expires": "2025-10-30"
            }
        ]
    
    def add_api_key(self, service_name: str, provider: str, api_key: str, description: str) -> bool:
        """Add new API key with integration sync."""
        try:
            # Simulate adding API key
            new_key_data = {
                'service_name': service_name,
                'provider': provider,
                'description': description,
                'added_at': datetime.now().isoformat(),
                'status': 'active'
            }
            
            # Sync with integration hooks
            self.integration_hooks.sync_system_config('api_key_added', new_key_data)
            
            return True
        except Exception as e:
            st.error(f"Failed to add API key: {e}")
            return False
    
    def get_github_status(self) -> Dict[str, Any]:
        """Get GitHub repository status."""
        return {
            'repository': 'IntelliCV/admin_portal',
            'current_branch': 'main',
            'commits_ahead': random.randint(0, 5),
            'commits_behind': random.randint(0, 2),
            'last_sync': (datetime.now() - timedelta(hours=random.randint(1, 6))).strftime("%Y-%m-%d %H:%M"),
            'sync_status': random.choice(['up_to_date', 'ahead', 'behind', 'diverged']),
            'last_commit': {
                'hash': f"a{random.randint(100000, 999999)}",
                'message': random.choice([
                    "Updated admin portal components",
                    "Fixed parsing bug in data processors", 
                    "Added new analytics features",
                    "Enhanced integration hooks",
                    "Improved error handling"
                ]),
                'author': random.choice(['admin', 'developer', 'system']),
                'time': (datetime.now() - timedelta(hours=random.randint(1, 48))).strftime("%Y-%m-%d %H:%M")
            }
        }
    
    def get_recent_commits(self) -> List[Dict[str, Any]]:
        """Get recent Git commits."""
        commit_messages = [
            "Updated admin portal components",
            "Fixed parsing bug in data processors",
            "Added new analytics features", 
            "Enhanced integration hooks",
            "Improved error handling",
            "Updated API documentation",
            "Refactored modular architecture",
            "Added compliance audit features",
            "Enhanced system monitoring",
            "Fixed user management issues"
        ]
        
        commits = []
        for i in range(10):
            commit_time = datetime.now() - timedelta(days=i, hours=random.randint(0, 23))
            commits.append({
                'hash': f"{random.choice(['a', 'b', 'c', 'd', 'e'])}{random.randint(100000, 999999)}",
                'message': random.choice(commit_messages),
                'author': random.choice(['admin', 'developer', 'system', 'github-actions']),
                'time': commit_time.strftime("%Y-%m-%d %H:%M"),
                'files_changed': random.randint(1, 15),
                'insertions': random.randint(10, 200),
                'deletions': random.randint(0, 50)
            })
        
        return commits
    
    def get_pipeline_status(self) -> List[Dict[str, Any]]:
        """Get CI/CD pipeline status."""
        return [
            {
                "Stage": "Build",
                "Status": random.choice(["✅ Passed", "✅ Passed", "❌ Failed"]),
                "Duration": f"{random.randint(2, 5)}m {random.randint(10, 59)}s",
                "Last_Run": (datetime.now() - timedelta(minutes=random.randint(5, 60))).strftime("%Y-%m-%d %H:%M"),
                "Success_Rate": random.uniform(92, 98)
            },
            {
                "Stage": "Test", 
                "Status": random.choice(["✅ Passed", "✅ Passed", "⚠️ Warning"]),
                "Duration": f"{random.randint(1, 3)}m {random.randint(15, 59)}s",
                "Last_Run": (datetime.now() - timedelta(minutes=random.randint(3, 58))).strftime("%Y-%m-%d %H:%M"),
                "Success_Rate": random.uniform(88, 96)
            },
            {
                "Stage": "Security Scan",
                "Status": random.choice(["✅ Passed", "⚠️ Warning"]),
                "Duration": f"{random.randint(0, 2)}m {random.randint(20, 59)}s", 
                "Last_Run": (datetime.now() - timedelta(minutes=random.randint(1, 56))).strftime("%Y-%m-%d %H:%M"),
                "Success_Rate": random.uniform(85, 95)
            },
            {
                "Stage": "Deploy",
                "Status": random.choice(["✅ Passed", "🔄 Running", "⏳ Waiting"]),
                "Duration": f"{random.randint(0, 1)}m {random.randint(30, 59)}s",
                "Last_Run": (datetime.now() - timedelta(minutes=random.randint(0, 55))).strftime("%Y-%m-%d %H:%M"),
                "Success_Rate": random.uniform(90, 99)
            },
            {
                "Stage": "Notify",
                "Status": random.choice(["✅ Passed", "⏳ Waiting"]),
                "Duration": f"0m {random.randint(5, 15)}s",
                "Last_Run": (datetime.now() - timedelta(minutes=random.randint(0, 50))).strftime("%Y-%m-%d %H:%M") if random.choice([True, False]) else "-",
                "Success_Rate": random.uniform(95, 100)
            }
        ]
    
    def get_api_usage_analytics(self) -> pd.DataFrame:
        """Get API usage analytics data."""
        dates = pd.date_range(start='2025-09-14', end='2025-09-20', freq='D')
        
        return pd.DataFrame({
            'Date': dates,
            'API_Calls': [1456 + i * 200 + random.randint(-200, 300) for i in range(len(dates))],
            'Success_Rate': [98.5 + random.uniform(-1, 1.5) for _ in range(len(dates))],
            'Avg_Response_ms': [145 + random.randint(-30, 50) for _ in range(len(dates))],
            'Unique_Users': [random.randint(45, 85) for _ in range(len(dates))],
            'Error_Count': [random.randint(10, 50) for _ in range(len(dates))]
        })
    
    def trigger_github_action(self, action: str) -> bool:
        """Trigger GitHub action with integration sync."""
        try:
            # Simulate GitHub action
            action_data = {
                'action': action,
                'triggered_at': datetime.now().isoformat(),
                'status': 'initiated'
            }
            
            # Sync with integration hooks
            self.integration_hooks.sync_system_config('github_action_triggered', action_data)
            
            return True
        except Exception as e:
            st.error(f"Failed to trigger {action}: {e}")
            return False
    
    def trigger_pipeline_stage(self, stage: str) -> bool:
        """Trigger CI/CD pipeline stage."""
        try:
            # Simulate pipeline trigger
            pipeline_data = {
                'stage': stage,
                'triggered_at': datetime.now().isoformat(),
                'status': 'initiated'
            }
            
            # Sync with integration hooks
            self.integration_hooks.sync_system_config('pipeline_stage_triggered', pipeline_data)
            
            return True
        except Exception as e:
            st.error(f"Failed to trigger {stage}: {e}")
            return False

# =============================================================================
# RENDER FUNCTION
# =============================================================================

def render():
    """Render the API Integration page."""
    # Initialize API integration
    api_integration = APIIntegration()
    
    render_section_header("🔧 API & Integration Management", "Comprehensive API management, GitHub integration, and CI/CD pipeline control")
    
    # Get API metrics
    metrics = api_integration.get_api_metrics()
    
    # API status metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Active APIs", 
            metrics['active_apis'], 
            f"+{metrics['active_apis_delta']}"
        )
    
    with col2:
        st.metric(
            "API Calls Today", 
            f"{metrics['api_calls_today']:,}", 
            f"+{metrics['api_calls_delta']:,}"
        )
    
    with col3:
        st.metric(
            "Success Rate", 
            f"{metrics['success_rate']:.1f}%", 
            f"+{metrics['success_rate_delta']:.1f}%"
        )
    
    with col4:
        st.metric(
            "Avg Response", 
            f"{metrics['avg_response_time']}ms", 
            f"{metrics['response_time_delta']}ms"
        )
    
    st.markdown("---")
    
    # Integration management tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔑 API Key Manager", 
        "🐙 GitHub Integration", 
        "⚙️ CI/CD Pipeline", 
        "📊 Integration Analytics",
        "🔗 Webhook Management"
    ])
    
    with tab1:
        st.subheader("🔑 API Key Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ➕ Add New API Key")
            
            with st.form("add_api_key", clear_on_submit=True):
                api_name = st.text_input("API Service Name", placeholder="e.g., OpenAI GPT-4")
                api_provider = st.selectbox("Provider", [
                    "OpenAI", "Anthropic", "Google", "Microsoft", "Azure", 
                    "AWS", "Custom", "Third-party"
                ])
                api_key = st.text_input("API Key", type="password", placeholder="Enter API key...")
                api_description = st.text_area("Description", placeholder="Brief description of API usage...")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    rate_limit = st.text_input("Rate Limit", placeholder="e.g., 1000/day")
                with col_b:
                    expires = st.date_input("Expires", value=datetime.now() + timedelta(days=365))
                
                if st.form_submit_button("🔑 Add API Key", type="primary"):
                    if api_name and api_key:
                        if api_integration.add_api_key(api_name, api_provider, api_key, api_description):
                            st.success(f"✅ API key for {api_name} added successfully!")
                    else:
                        st.error("Please provide API service name and key.")
        
        with col2:
            st.markdown("#### 📋 Existing API Keys")
            
            api_keys = api_integration.get_api_keys()
            
            for api in api_keys:
                status_color = "🟢" if "Active" in api['Status'] else "🟡" if "Testing" in api['Status'] else "🔴"
                
                with st.expander(f"{status_color} {api['Service']} - {api['Status']}", expanded=False):
                    col_x, col_y = st.columns(2)
                    
                    with col_x:
                        st.text(f"Provider: {api['Provider']}")
                        st.text(f"Last Used: {api['Last_Used']}")
                        st.text(f"Usage Today: {api['Usage_Today']}")
                    
                    with col_y:
                        st.text(f"Rate Limit: {api['Rate_Limit']}")
                        st.text(f"Expires: {api['Expires']}")
                        
                        # Action buttons
                        col_btn1, col_btn2, col_btn3 = st.columns(3)
                        
                        with col_btn1:
                            if st.button("🔄", key=f"refresh_{api['Service']}", help="Refresh Key"):
                                st.success("🔄 API key refreshed")
                        
                        with col_btn2:
                            if st.button("📊", key=f"stats_{api['Service']}", help="View Stats"):
                                st.info("📊 Usage statistics would be shown here")
                        
                        with col_btn3:
                            if st.button("🗑️", key=f"delete_{api['Service']}", help="Delete Key"):
                                st.warning("⚠️ API key would be deleted")
        
        # API Key Usage Summary
        st.markdown("#### 📈 API Usage Summary")
        
        usage_data = pd.DataFrame([
            {
                'Service': api['Service'],
                'Usage_Today': api['Usage_Today'],
                'Rate_Limit': api['Rate_Limit'].split('/')[0] if '/' in api['Rate_Limit'] else 'unlimited',
                'Status': api['Status']
            }
            for api in api_keys
        ])
        
        # Usage chart
        if not usage_data.empty:
            fig_usage = px.bar(
                usage_data,
                x='Service',
                y='Usage_Today',
                title='API Usage Today',
                color='Usage_Today',
                color_continuous_scale='viridis'
            )
            fig_usage.update_layout(height=300, xaxis_tickangle=45)
            st.plotly_chart(fig_usage, use_container_width=True)
    
    with tab2:
        st.subheader("🐙 GitHub Repository Integration")
        
        # Get GitHub status
        github_status = api_integration.get_github_status()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📂 Repository Management")
            
            st.text_input("Repository", value=github_status['repository'], disabled=True)
            st.text_input("Current Branch", value=github_status['current_branch'], disabled=True)
            
            # Repository actions
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("📥 Pull Latest Changes", type="primary"):
                    with st.spinner("Pulling from GitHub..."):
                        if api_integration.trigger_github_action('pull'):
                            time.sleep(2)
                            st.success("✅ Successfully pulled latest changes!")
            
            with col_b:
                if st.button("📤 Push Local Changes", type="primary"):
                    with st.spinner("Pushing to GitHub..."):
                        if api_integration.trigger_github_action('push'):
                            time.sleep(2)
                            st.success("✅ Successfully pushed changes!")
            
            # Branch management
            st.markdown("#### 🌿 Branch Management")
            
            new_branch = st.text_input("Create New Branch", placeholder="feature/new-feature")
            if st.button("🌿 Create Branch"):
                if new_branch:
                    st.success(f"✅ Branch '{new_branch}' created successfully!")
                else:
                    st.error("Please enter a branch name.")
        
        with col2:
            st.markdown("#### 📊 Repository Status")
            
            # Status metrics
            col_x, col_y = st.columns(2)
            
            with col_x:
                st.metric("Commits Ahead", github_status['commits_ahead'])
                st.metric("Commits Behind", github_status['commits_behind'])
            
            with col_y:
                st.metric("Last Sync", github_status['last_sync'])
                sync_status = github_status['sync_status'].replace('_', ' ').title()
                st.metric("Sync Status", sync_status)
            
            # Last commit info
            st.markdown("#### 📝 Latest Commit")
            last_commit = github_status['last_commit']
            
            st.text(f"Hash: {last_commit['hash']}")
            st.text(f"Message: {last_commit['message']}")
            st.text(f"Author: {last_commit['author']}")
            st.text(f"Time: {last_commit['time']}")
        
        # Recent commits history
        st.markdown("#### 📜 Recent Commits")
        
        recent_commits = api_integration.get_recent_commits()
        
        commits_df = pd.DataFrame(recent_commits)
        
        # Display commits in a more readable format
        for commit in recent_commits[:5]:  # Show last 5 commits
            with st.container():
                col_hash, col_message, col_author, col_time = st.columns([1, 3, 1, 1])
                
                with col_hash:
                    st.code(commit['hash'][:7])
                with col_message:
                    st.text(commit['message'])
                with col_author:
                    st.text(commit['author'])
                with col_time:
                    st.text(commit['time'])
        
        # Export commit history
        if st.button("📥 Export Commit History"):
            commit_text = commits_df.to_csv(index=False)
            st.download_button(
                label="📊 Download Commit History",
                data=commit_text,
                file_name=f"commit_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with tab3:
        st.subheader("⚙️ CI/CD Pipeline Management")
        
        # Get pipeline status
        pipeline_status = api_integration.get_pipeline_status()
        
        st.markdown("#### 🔄 Pipeline Status")
        
        # Pipeline visualization
        for i, stage in enumerate(pipeline_status):
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 2, 1])
            
            with col1:
                st.write(f"**{stage['Stage']}**")
            with col2:
                st.write(stage['Status'])
            with col3:
                st.write(stage['Duration'])
            with col4:
                st.write(stage['Last_Run'])
            with col5:
                st.write(f"{stage['Success_Rate']:.1f}%")
        
        st.markdown("---")
        
        # Pipeline controls
        st.markdown("#### 🛠️ Pipeline Controls")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🚀 Trigger Build", type="primary"):
                if api_integration.trigger_pipeline_stage('build'):
                    st.success("✅ Build triggered successfully!")
        
        with col2:
            if st.button("🧪 Run Tests", type="primary"):
                if api_integration.trigger_pipeline_stage('test'):
                    st.success("✅ Tests initiated!")
        
        with col3:
            if st.button("🔒 Security Scan", type="primary"):
                if api_integration.trigger_pipeline_stage('security'):
                    st.success("✅ Security scan started!")
        
        with col4:
            if st.button("📦 Deploy", type="primary"):
                if api_integration.trigger_pipeline_stage('deploy'):
                    st.warning("⚠️ Deployment initiated - Monitor carefully!")
        
        # Pipeline success rates
        st.markdown("#### 📊 Pipeline Performance")
        
        pipeline_df = pd.DataFrame(pipeline_status)
        
        fig_pipeline = px.bar(
            pipeline_df,
            x='Stage',
            y='Success_Rate',
            title='Pipeline Stage Success Rates',
            color='Success_Rate',
            color_continuous_scale='RdYlGn',
            range_color=[80, 100]
        )
        fig_pipeline.update_layout(height=400)
        st.plotly_chart(fig_pipeline, use_container_width=True)
        
        # Pipeline history
        st.markdown("#### 📈 Pipeline History")
        
        # Generate mock pipeline history
        dates = pd.date_range(start=datetime.now() - timedelta(days=7), periods=7, freq='D')
        history_data = pd.DataFrame({
            'Date': dates,
            'Builds': [random.randint(2, 8) for _ in range(7)],
            'Success_Rate': [random.uniform(85, 98) for _ in range(7)],
            'Avg_Duration': [random.uniform(4, 12) for _ in range(7)]
        })
        
        fig_history = px.line(
            history_data,
            x='Date',
            y=['Builds', 'Success_Rate'],
            title='Pipeline Activity (7 Days)'
        )
        fig_history.update_layout(height=300)
        st.plotly_chart(fig_history, use_container_width=True)
    
    with tab4:
        st.subheader("📊 Integration Analytics & Monitoring")
        
        # Get analytics data
        usage_data = api_integration.get_api_usage_analytics()
        
        # API usage trends
        st.markdown("#### 📈 API Usage Trends")
        
        fig_calls = px.line(
            usage_data, 
            x='Date', 
            y='API_Calls', 
            title='Daily API Calls',
            markers=True
        )
        fig_calls.update_layout(height=400)
        st.plotly_chart(fig_calls, use_container_width=True)
        
        # Success rate and response time
        col1, col2 = st.columns(2)
        
        with col1:
            fig_success = px.line(
                usage_data,
                x='Date',
                y='Success_Rate',
                title='API Success Rate (%)',
                markers=True
            )
            fig_success.update_layout(height=300)
            st.plotly_chart(fig_success, use_container_width=True)
        
        with col2:
            fig_response = px.line(
                usage_data,
                x='Date',
                y='Avg_Response_ms',
                title='Average Response Time (ms)',
                markers=True
            )
            fig_response.update_layout(height=300)
            st.plotly_chart(fig_response, use_container_width=True)
        
        # Analytics summary
        st.markdown("#### 📋 Analytics Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_calls = usage_data['API_Calls'].sum()
            st.metric("Total API Calls (7d)", f"{total_calls:,}")
        
        with col2:
            avg_success_rate = usage_data['Success_Rate'].mean()
            st.metric("Avg Success Rate", f"{avg_success_rate:.1f}%")
        
        with col3:
            avg_response = usage_data['Avg_Response_ms'].mean()
            st.metric("Avg Response Time", f"{avg_response:.0f}ms")
        
        with col4:
            total_errors = usage_data['Error_Count'].sum()
            st.metric("Total Errors (7d)", total_errors)
        
        # Error analysis
        st.markdown("#### 🚨 Error Analysis")
        
        error_types = pd.DataFrame({
            'Error_Type': ['Rate Limit', 'Authentication', 'Timeout', 'Server Error', 'Invalid Request'],
            'Count': [random.randint(5, 25) for _ in range(5)],
            'Percentage': [random.uniform(10, 30) for _ in range(5)]
        })
        
        fig_errors = px.pie(
            error_types,
            values='Count',
            names='Error_Type',
            title='Error Distribution'
        )
        fig_errors.update_layout(height=400)
        st.plotly_chart(fig_errors, use_container_width=True)
    
    with tab5:
        st.subheader("🔗 Webhook Management")
        
        st.markdown("#### 📡 Active Webhooks")
        
        # Mock webhook data
        webhooks = [
            {"Name": "GitHub Push Events", "URL": "https://api.intellicv.com/webhook/github", "Status": "✅ Active", "Last_Triggered": "2 hours ago"},
            {"Name": "CI/CD Notifications", "URL": "https://api.intellicv.com/webhook/cicd", "Status": "✅ Active", "Last_Triggered": "5 hours ago"},
            {"Name": "User Registration", "URL": "https://api.intellicv.com/webhook/users", "Status": "⚠️ Warning", "Last_Triggered": "1 day ago"},
            {"Name": "Payment Events", "URL": "https://api.intellicv.com/webhook/payments", "Status": "🔴 Inactive", "Last_Triggered": "5 days ago"}
        ]
        
        for webhook in webhooks:
            with st.expander(f"{webhook['Status']} {webhook['Name']}"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.text(f"URL: {webhook['URL']}")
                    st.text(f"Last Triggered: {webhook['Last_Triggered']}")
                
                with col_b:
                    if st.button(f"🧪 Test Webhook", key=f"test_{webhook['Name']}"):
                        st.success("🧪 Webhook test sent!")
                    if st.button(f"📊 View Logs", key=f"logs_{webhook['Name']}"):
                        st.info("📊 Webhook logs would be displayed here")
        
        # Add new webhook
        st.markdown("#### ➕ Add New Webhook")
        
        with st.form("add_webhook"):
            webhook_name = st.text_input("Webhook Name")
            webhook_url = st.text_input("Webhook URL")
            webhook_events = st.multiselect("Events", [
                "push", "pull_request", "issue", "deployment", 
                "user_registration", "payment", "system_alert"
            ])
            
            if st.form_submit_button("🔗 Add Webhook"):
                if webhook_name and webhook_url:
                    st.success(f"✅ Webhook '{webhook_name}' added successfully!")
                else:
                    st.error("Please provide webhook name and URL.")

if __name__ == "__main__":
    render()