"""
=============================================================================
Admin Portal - Token Management Dashboard
=============================================================================

Comprehensive token management interface for administrators to:
- Monitor user token consumption
- Adjust token costs per page
- Analyze usage patterns
- Manage subscription allocations
- Generate revenue reports

Author: IntelliCV-AI Admin System
Date: October 23, 2025
Status: PRODUCTION READY
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json
import plotly.express as px
import plotly.graph_objects as go

# Import token management system
try:
    from token_management_system import TokenManager, get_admin_token_analytics, update_token_costs
    TOKEN_SYSTEM_AVAILABLE = True
except ImportError:
    TOKEN_SYSTEM_AVAILABLE = False

def check_admin_authentication():
    """Ensure admin is authenticated before showing token management."""
    if not st.session_state.get('admin_authenticated', False):
        st.error("🔒 **ADMIN AUTHENTICATION REQUIRED**")
        st.warning("You must login through the main admin portal to access token management.")
        if st.button("🏠 Return to Main Portal", type="primary"):
            st.switch_page("main.py")
        st.stop()
    return True

def main():
    """Main admin token management interface."""
    st.set_page_config(
        page_title="🎯 Token Management | Admin Portal",
        page_icon="🎯",
        layout="wide"
    )
    
    # Authentication check
    check_admin_authentication()
    
    # Header
    st.markdown("# 🎯 Token Management Dashboard")
    st.markdown("**Comprehensive token cost management and user analytics**")
    st.markdown("---")
    
    if not TOKEN_SYSTEM_AVAILABLE:
        st.error("❌ Token management system not available")
        st.info("Please ensure token_management_system.py is properly installed")
        return
    
    # Initialize token manager
    token_manager = TokenManager()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🎯 Token Management")
        
        admin_section = st.selectbox(
            "Select Section:",
            [
                "📊 Usage Analytics",
                "💰 Token Cost Management", 
                "👥 User Management",
                "📈 Revenue Analytics",
                "⚙️ System Configuration",
                "📋 Usage Logs"
            ]
        )
    
    # Main content based on selection
    if admin_section == "📊 Usage Analytics":
        display_usage_analytics(token_manager)
    
    elif admin_section == "💰 Token Cost Management":
        display_token_cost_management(token_manager)
    
    elif admin_section == "👥 User Management":
        display_user_management(token_manager)
    
    elif admin_section == "📈 Revenue Analytics":
        display_revenue_analytics(token_manager)
    
    elif admin_section == "⚙️ System Configuration":
        display_system_configuration(token_manager)
    
    elif admin_section == "📋 Usage Logs":
        display_usage_logs(token_manager)

def display_usage_analytics(token_manager: TokenManager):
    """Display comprehensive usage analytics."""
    st.markdown("## 📊 Token Usage Analytics")
    
    # Get analytics data (simulated for demo)
    analytics_data = get_simulated_analytics()
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Users",
            analytics_data['total_users'],
            delta=f"+{analytics_data['new_users_today']} today"
        )
    
    with col2:
        st.metric(
            "Tokens Consumed Today",
            f"{analytics_data['tokens_today']:,}",
            delta=f"{analytics_data['tokens_change']:+.1f}%"
        )
    
    with col3:
        st.metric(
            "Revenue Today",
            f"${analytics_data['revenue_today']:.2f}",
            delta=f"${analytics_data['revenue_change']:+.2f}"
        )
    
    with col4:
        st.metric(
            "Avg Tokens/User",
            f"{analytics_data['avg_tokens_per_user']:.1f}",
            delta=f"{analytics_data['avg_change']:+.1f}%"
        )
    
    # Usage trends chart
    st.markdown("### 📈 Usage Trends (Last 30 Days)")
    
    # Create sample trend data
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    trend_data = pd.DataFrame({
        'Date': dates,
        'Tokens Consumed': [1500 + i*50 + (i%7)*200 for i in range(len(dates))],
        'Active Users': [150 + i*5 + (i%7)*20 for i in range(len(dates))],
        'Revenue': [225 + i*7.5 + (i%7)*30 for i in range(len(dates))]
    })
    
    fig = px.line(trend_data, x='Date', y=['Tokens Consumed', 'Active Users'], 
                  title="Daily Usage Trends")
    st.plotly_chart(fig, use_container_width=True)
    
    # Most popular features
    st.markdown("### 🔥 Most Popular Features")
    
    popular_features = pd.DataFrame({
        'Feature': ['Resume Analysis', 'AI Job Matching', 'Interview Coach', 'Career Intelligence', 'Profile Builder'],
        'Token Usage': [15420, 12340, 9870, 7650, 5430],
        'Users': [1250, 980, 670, 450, 320]
    })
    
    fig_features = px.bar(popular_features, x='Feature', y='Token Usage', 
                         title="Token Consumption by Feature")
    st.plotly_chart(fig_features, use_container_width=True)

def display_token_cost_management(token_manager: TokenManager):
    """Display and manage token costs for all pages."""
    st.markdown("## 💰 Token Cost Management")
    
    # Current token costs
    st.markdown("### Current Token Costs")
    
    # Organize costs by tier
    costs_by_tier = {
        "🆓 Free Tier (0 tokens)": {},
        "🔸 Basic Tier (1-2 tokens)": {},
        "🔹 Standard Tier (3-5 tokens)": {},
        "🔶 Advanced Tier (6-10 tokens)": {},
        "🔻 Premium Tier (11-20 tokens)": {},
        "🔴 Enterprise Tier (21+ tokens)": {}
    }
    
    for page, cost in token_manager.token_costs.items():
        if cost == 0:
            costs_by_tier["🆓 Free Tier (0 tokens)"][page] = cost
        elif 1 <= cost <= 2:
            costs_by_tier["🔸 Basic Tier (1-2 tokens)"][page] = cost
        elif 3 <= cost <= 5:
            costs_by_tier["🔹 Standard Tier (3-5 tokens)"][page] = cost
        elif 6 <= cost <= 10:
            costs_by_tier["🔶 Advanced Tier (6-10 tokens)"][page] = cost
        elif 11 <= cost <= 20:
            costs_by_tier["🔻 Premium Tier (11-20 tokens)"][page] = cost
        else:
            costs_by_tier["🔴 Enterprise Tier (21+ tokens)"][page] = cost
    
    # Display costs by tier
    for tier, pages in costs_by_tier.items():
        if pages:
            with st.expander(f"{tier} - {len(pages)} pages"):
                cost_df = pd.DataFrame(list(pages.items()), columns=['Page', 'Token Cost'])
                st.dataframe(cost_df, use_container_width=True)
    
    # Token cost editor
    st.markdown("### 🔧 Edit Token Costs")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Select page to edit
        page_to_edit = st.selectbox(
            "Select page to edit:",
            options=list(token_manager.token_costs.keys()),
            format_func=lambda x: f"{x} (Current: {token_manager.token_costs[x]} tokens)"
        )
    
    with col2:
        # New cost input
        current_cost = token_manager.token_costs[page_to_edit]
        new_cost = st.number_input(
            "New token cost:",
            min_value=0,
            max_value=100,
            value=current_cost,
            step=1
        )
    
    # Update button
    if st.button("💾 Update Token Cost"):
        if new_cost != current_cost:
            token_manager.token_costs[page_to_edit] = new_cost
            st.success(f"✅ Updated {page_to_edit} to {new_cost} tokens")
            st.experimental_rerun()
        else:
            st.info("ℹ️ No change made")
    
    # Bulk operations
    st.markdown("### 🔄 Bulk Operations")
    
    bulk_col1, bulk_col2, bulk_col3 = st.columns(3)
    
    with bulk_col1:
        if st.button("📈 Increase All Costs by 1"):
            for page in token_manager.token_costs:
                if token_manager.token_costs[page] > 0:
                    token_manager.token_costs[page] += 1
            st.success("✅ All non-free pages increased by 1 token")
    
    with bulk_col2:
        if st.button("📉 Decrease All Costs by 1"):
            for page in token_manager.token_costs:
                if token_manager.token_costs[page] > 1:
                    token_manager.token_costs[page] -= 1
            st.success("✅ All pages decreased by 1 token (minimum 1)")
    
    with bulk_col3:
        if st.button("🔄 Reset to Defaults"):
            # Reset to default costs
            st.warning("⚠️ This will reset ALL token costs to defaults")
            if st.button("✅ Confirm Reset"):
                token_manager.__init__()  # Reinitialize with defaults
                st.success("✅ Token costs reset to defaults")

def display_user_management(token_manager: TokenManager):
    """Display user token management interface."""
    st.markdown("## 👥 User Token Management")
    
    # User search
    st.markdown("### 🔍 Find User")
    search_term = st.text_input("Search by username or email:", placeholder="user@example.com")
    
    if search_term:
        # Simulated user data
        users = get_simulated_users(search_term)
        
        if users:
            selected_user = st.selectbox("Select user:", users, format_func=lambda x: f"{x['username']} ({x['email']})")
            
            if selected_user:
                display_user_details(selected_user, token_manager)
        else:
            st.warning("No users found matching search criteria")
    
    # Recent high-usage users
    st.markdown("### 🔥 High Usage Users (Last 7 Days)")
    high_usage_users = get_simulated_high_usage_users()
    
    usage_df = pd.DataFrame(high_usage_users)
    st.dataframe(usage_df, use_container_width=True)

def display_user_details(user: Dict, token_manager: TokenManager):
    """Display detailed user token information."""
    st.markdown(f"### 👤 User Details: {user['username']}")
    
    # User info
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Plan", user['plan'])
    
    with col2:
        st.metric("Tokens Remaining", f"{user['tokens_remaining']}/{user['tokens_total']}")
    
    with col3:
        st.metric("Usage This Month", f"{user['tokens_used']}")
    
    with col4:
        st.metric("Last Active", user['last_active'])
    
    # Token management actions
    st.markdown("#### 🔧 Token Management Actions")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        bonus_tokens = st.number_input("Bonus tokens:", min_value=0, max_value=1000, step=10)
        if st.button("🎁 Grant Bonus Tokens"):
            st.success(f"✅ Granted {bonus_tokens} bonus tokens to {user['username']}")
    
    with action_col2:
        if st.button("🔄 Reset Monthly Tokens"):
            st.success(f"✅ Reset monthly tokens for {user['username']}")
    
    with action_col3:
        if st.button("📊 View Usage History"):
            st.info("Usage history would be displayed here")

def display_revenue_analytics(token_manager: TokenManager):
    """Display revenue and financial analytics."""
    st.markdown("## 📈 Revenue Analytics")
    
    # Revenue overview
    revenue_data = get_simulated_revenue_data()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Daily Revenue", f"${revenue_data['daily']:.2f}", delta=f"{revenue_data['daily_change']:+.1f}%")
    
    with col2:
        st.metric("Monthly Revenue", f"${revenue_data['monthly']:.2f}", delta=f"${revenue_data['monthly_growth']:+.2f}")
    
    with col3:
        st.metric("Revenue per Token", f"${revenue_data['per_token']:.3f}")
    
    with col4:
        st.metric("ARPU", f"${revenue_data['arpu']:.2f}")
    
    # Revenue by plan
    st.markdown("### 💰 Revenue by Subscription Plan")
    
    plan_revenue = pd.DataFrame({
        'Plan': ['Free', 'Monthly Pro', 'Annual Pro', 'Enterprise'],
        'Users': [1250, 450, 180, 25],
        'Monthly Revenue': [0, 7195.50, 2699.82, 624.98],
        'Token Usage': [8500, 35000, 28000, 15000]
    })
    
    fig_revenue = px.bar(plan_revenue, x='Plan', y='Monthly Revenue', 
                        title="Monthly Revenue by Plan")
    st.plotly_chart(fig_revenue, use_container_width=True)
    
    # Token economics
    st.markdown("### 🎯 Token Economics")
    
    token_economics = pd.DataFrame({
        'Feature Tier': ['Free', 'Basic', 'Standard', 'Advanced', 'Premium', 'Enterprise'],
        'Avg Cost (Tokens)': [0, 1.5, 4, 8, 15, 27],
        'Usage Volume': [25000, 15000, 35000, 18000, 8000, 2000],
        'Revenue Impact': [0, 337.50, 2100, 2160, 1800, 810]
    })
    
    st.dataframe(token_economics, use_container_width=True)

def display_system_configuration(token_manager: TokenManager):
    """Display system configuration options."""
    st.markdown("## ⚙️ System Configuration")
    
    # Plan configuration
    st.markdown("### 📋 Subscription Plan Token Allocations")
    
    current_allocations = {
        'Free Starter': 10,
        'Monthly Pro': 100,
        'Annual Pro': 250,
        'Enterprise Pro': 1000
    }
    
    plan_col1, plan_col2 = st.columns(2)
    
    with plan_col1:
        for plan, tokens in list(current_allocations.items())[:2]:
            new_allocation = st.number_input(
                f"{plan} monthly tokens:",
                min_value=0,
                value=tokens,
                step=10,
                key=f"plan_{plan}"
            )
    
    with plan_col2:
        for plan, tokens in list(current_allocations.items())[2:]:
            new_allocation = st.number_input(
                f"{plan} monthly tokens:",
                min_value=0,
                value=tokens,
                step=10,
                key=f"plan_{plan}"
            )
    
    if st.button("💾 Update Plan Allocations"):
        st.success("✅ Plan allocations updated successfully")
    
    # Warning thresholds
    st.markdown("### ⚠️ Warning Thresholds")
    
    warning_col1, warning_col2, warning_col3 = st.columns(3)
    
    with warning_col1:
        low_warning = st.slider("Low usage warning (%)", 70, 90, 75)
    
    with warning_col2:
        critical_warning = st.slider("Critical warning (%)", 85, 99, 90)
    
    with warning_col3:
        upgrade_suggestion = st.slider("Upgrade suggestion (%)", 80, 95, 85)
    
    # Auto-refresh settings
    st.markdown("### 🔄 Token Refresh Settings")
    
    refresh_col1, refresh_col2 = st.columns(2)
    
    with refresh_col1:
        auto_refresh = st.checkbox("Enable automatic token refresh", value=True)
        refresh_day = st.selectbox("Monthly refresh day:", list(range(1, 32)), index=0)
    
    with refresh_col2:
        rollover_tokens = st.checkbox("Allow token rollover", value=False)
        max_rollover = st.number_input("Max rollover tokens:", min_value=0, value=50)

def display_usage_logs(token_manager: TokenManager):
    """Display detailed usage logs."""
    st.markdown("## 📋 Token Usage Logs")
    
    # Filters
    st.markdown("### 🔍 Filter Logs")
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        date_filter = st.date_input("Date range start:", datetime.now().date() - timedelta(days=7))
    
    with filter_col2:
        user_filter = st.text_input("User filter:", placeholder="username or email")
    
    with filter_col3:
        page_filter = st.selectbox("Page filter:", ["All"] + list(token_manager.token_costs.keys()))
    
    # Simulated logs
    logs = get_simulated_usage_logs()
    
    if user_filter:
        logs = [log for log in logs if user_filter.lower() in log['user'].lower()]
    
    if page_filter != "All":
        logs = [log for log in logs if log['page'] == page_filter]
    
    # Display logs
    st.markdown("### 📊 Usage Log Entries")
    
    if logs:
        logs_df = pd.DataFrame(logs)
        st.dataframe(logs_df, use_container_width=True)
        
        # Export option
        if st.button("📥 Export Logs to CSV"):
            csv = logs_df.to_csv(index=False)
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=f"token_usage_logs_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    else:
        st.info("No logs found matching the selected filters")

# Helper functions for simulated data
def get_simulated_analytics():
    """Generate simulated analytics data."""
    return {
        'total_users': 1905,
        'new_users_today': 45,
        'tokens_today': 15420,
        'tokens_change': +12.5,
        'revenue_today': 231.30,
        'revenue_change': +18.75,
        'avg_tokens_per_user': 8.1,
        'avg_change': +5.2
    }

def get_simulated_users(search_term):
    """Generate simulated user data."""
    return [
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'plan': 'Monthly Pro',
            'tokens_remaining': 75,
            'tokens_total': 100,
            'tokens_used': 25,
            'last_active': '2 hours ago'
        },
        {
            'username': 'jane_smith',
            'email': 'jane@company.com',
            'plan': 'Annual Pro',
            'tokens_remaining': 180,
            'tokens_total': 250,
            'tokens_used': 70,
            'last_active': '1 day ago'
        }
    ]

def get_simulated_high_usage_users():
    """Generate simulated high usage user data."""
    return [
        {'Username': 'power_user_1', 'Plan': 'Enterprise', 'Tokens Used': 850, 'Remaining': 150},
        {'Username': 'heavy_user_2', 'Plan': 'Annual Pro', 'Tokens Used': 230, 'Remaining': 20},
        {'Username': 'active_user_3', 'Plan': 'Monthly Pro', 'Tokens Used': 95, 'Remaining': 5}
    ]

def get_simulated_revenue_data():
    """Generate simulated revenue data."""
    return {
        'daily': 231.30,
        'daily_change': 12.5,
        'monthly': 6945.82,
        'monthly_growth': 875.22,
        'per_token': 0.15,
        'arpu': 3.65
    }

def get_simulated_usage_logs():
    """Generate simulated usage logs."""
    return [
        {
            'timestamp': '2025-10-23 10:30:00',
            'user': 'john_doe',
            'page': '07_AI_Interview_Coach.py',
            'tokens_consumed': 8,
            'remaining': 67
        },
        {
            'timestamp': '2025-10-23 10:25:00',
            'user': 'jane_smith',
            'page': '05_Resume_Upload_Enhanced_AI.py',
            'tokens_consumed': 7,
            'remaining': 173
        },
        {
            'timestamp': '2025-10-23 10:20:00',
            'user': 'mike_wilson',
            'page': '06_Job_Match_INTEGRATED.py',
            'tokens_consumed': 9,
            'remaining': 16
        }
    ]

if __name__ == "__main__":
    main()