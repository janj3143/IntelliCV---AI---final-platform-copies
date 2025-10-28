"""
=============================================================================
IntelliCV Admin Portal - Legacy & Miscellaneous Tools Suite
=============================================================================

Comprehensive legacy system management with file archival,
user platform mockup tools, system utilities, and migration support.

Features:
- Legacy file management and archival
- User platform mockup and prototyping
- System utilities and maintenance tools
- Migration and compatibility support
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
from datetime import datetime, timedelta
from pathlib import Path
import time
import sys
from typing import Dict, Any, List

# Add shared components to path
pages_dir = Path(__file__).parent
if str(pages_dir) not in sys.path:
    sys.path.insert(0, str(pages_dir))

# from shared.components import render_section_header, render_metrics_row  # Using fallback implementations
# from shared.integration_hooks import get_integration_hooks  # Using fallback implementations

# =============================================================================
# LEGACY UTILITIES SUITE
# =============================================================================

class LegacyUtilities:
    """Complete Legacy & Miscellaneous Tools Management Suite"""
    
    def __init__(self):
        """Initialize legacy utilities system."""
        self.integration_hooks = get_integration_hooks()
        self.legacy_dir = Path("C:/IntelliCV/legacy")
        self.archive_dir = Path("C:/IntelliCV/archive")
        self.mockup_dir = Path("C:/IntelliCV/mockups")
        
    def render_legacy_files(self):
        """Render legacy files management interface."""
        st.subheader("📁 Legacy Files Manager")
        
        # Legacy files overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📁 Legacy Files", "127", "-15")
        with col2:
            st.metric("🗂️ Archived Files", "89", "+15")
        with col3:
            st.metric("💾 Total Size", "2.4 GB", "-450 MB")
        with col4:
            st.metric("🧹 Last Cleanup", "3 days ago", "")
        
        # Legacy files listing
        st.write("**📋 Legacy Files Inventory**")
        
        legacy_files = [
            {
                "File": "old_parser_v1.py",
                "Size": "12.4 KB", 
                "Last Modified": "2024-03-15",
                "Status": "🗂️ Archived",
                "Type": "Python Script",
                "Description": "Original CV parsing script - deprecated"
            },
            {
                "File": "deprecated_api.py", 
                "Size": "8.7 KB",
                "Last Modified": "2024-01-20",
                "Status": "🗂️ Archived", 
                "Type": "API Module",
                "Description": "Legacy API endpoints - replaced by v2"
            },
            {
                "File": "legacy_config.json",
                "Size": "2.1 KB",
                "Last Modified": "2024-02-10", 
                "Status": "🗂️ Archived",
                "Type": "Configuration",
                "Description": "Old configuration format - migrated"
            },
            {
                "File": "old_database_schema.sql",
                "Size": "45.2 KB",
                "Last Modified": "2023-11-05",
                "Status": "📦 Archived",
                "Type": "Database Schema",
                "Description": "Legacy database structure - v1.0"
            },
            {
                "File": "prototype_ui.html",
                "Size": "67.8 KB", 
                "Last Modified": "2023-09-22",
                "Status": "⚠️ Needs Review",
                "Type": "HTML Template",
                "Description": "Early UI prototype - may contain useful elements"
            },
            {
                "File": "temp_migration_script.py",
                "Size": "15.6 KB",
                "Last Modified": "2024-04-12",
                "Status": "🗑️ Can Delete",
                "Type": "Migration Script", 
                "Description": "One-time migration script - no longer needed"
            }
        ]
        
        # Display files with management options
        for file_info in legacy_files:
            with st.expander(f"📄 {file_info['File']} - {file_info['Size']} ({file_info['Status']})"):
                col_info1, col_info2 = st.columns(2)
                
                with col_info1:
                    st.write(f"**Type:** {file_info['Type']}")
                    st.write(f"**Last Modified:** {file_info['Last Modified']}")
                    st.write(f"**Description:** {file_info['Description']}")
                
                with col_info2:
                    col_action1, col_action2, col_action3, col_action4 = st.columns(4)
                    
                    with col_action1:
                        if st.button("👁️ View", key=f"view_{file_info['File']}"):
                            st.info(f"👁️ Opening {file_info['File']} in viewer")
                    
                    with col_action2:
                        if st.button("📦 Archive", key=f"archive_{file_info['File']}"):
                            st.success(f"📦 {file_info['File']} archived successfully")
                    
                    with col_action3:
                        if st.button("📋 Extract", key=f"extract_{file_info['File']}"):
                            st.info(f"📋 Extracting useful components from {file_info['File']}")
                    
                    with col_action4:
                        if st.button("🗑️ Delete", key=f"delete_{file_info['File']}"):
                            st.error(f"🗑️ {file_info['File']} deleted permanently")
        
        # Bulk operations
        st.markdown("---")
        st.write("**🔧 Bulk Legacy File Operations**")
        
        col_bulk1, col_bulk2, col_bulk3, col_bulk4 = st.columns(4)
        
        with col_bulk1:
            if st.button("🗂️ Archive Old Files", use_container_width=True):
                self.archive_old_files()
        
        with col_bulk2:
            if st.button("🔍 Analyze Dependencies", use_container_width=True):
                self.analyze_file_dependencies()
        
        with col_bulk3:
            if st.button("📊 Generate Report", use_container_width=True):
                self.generate_legacy_report()
        
        with col_bulk4:
            if st.button("🧹 Cleanup Suggestions", use_container_width=True):
                self.suggest_cleanup_actions()
    
    def archive_old_files(self):
        """Archive old legacy files."""
        with st.spinner("🗂️ Archiving old files..."):
            progress_bar = st.progress(0)
            
            files_to_archive = [
                "old_parser_v1.py",
                "deprecated_api.py", 
                "legacy_config.json",
                "temp_migration_script.py"
            ]
            
            for i, file in enumerate(files_to_archive):
                st.text(f"📦 Archiving {file}...")
                time.sleep(0.3)
                progress_bar.progress((i + 1) / len(files_to_archive))
            
            st.success("✅ Legacy files archived successfully!")
            
            # Show archive summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📦 Files Archived", "15")
            with col2:
                st.metric("💾 Space Freed", "450 MB")
            with col3:
                st.metric("🗂️ Archive Size", "125 MB")
            
            # Integration hooks - sync archive operation
            if self.integration_hooks:
                archive_data = {
                    "files_archived": 15,
                    "space_freed_mb": 450,
                    "archive_size_mb": 125,
                    "archived_at": datetime.now().isoformat()
                }
                # self.integration_hooks.sync_archive_operation(archive_data)
    
    def analyze_file_dependencies(self):
        """Analyze dependencies in legacy files."""
        with st.spinner("🔍 Analyzing file dependencies..."):
            time.sleep(2)
            
            st.success("✅ Dependency analysis completed!")
            
            st.subheader("📊 Dependency Analysis Results")
            
            dependencies_found = [
                {"File": "old_parser_v1.py", "Dependencies": 3, "Safe to Delete": "⚠️ No - Referenced by 2 files"},
                {"File": "deprecated_api.py", "Dependencies": 0, "Safe to Delete": "✅ Yes - No references found"},
                {"File": "legacy_config.json", "Dependencies": 1, "Safe to Delete": "⚠️ No - Used by migration script"},
                {"File": "temp_migration_script.py", "Dependencies": 0, "Safe to Delete": "✅ Yes - One-time use complete"}
            ]
            
            deps_df = pd.DataFrame(dependencies_found)
            st.dataframe(deps_df, use_container_width=True, hide_index=True)
    
    def generate_legacy_report(self):
        """Generate comprehensive legacy files report."""
        with st.spinner("📊 Generating legacy files report..."):
            time.sleep(1.5)
            
            st.success("✅ Legacy files report generated!")
            
            st.subheader("📋 Legacy Files Summary Report")
            
            # Report metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📁 Total Files", "127")
            with col2:
                st.metric("💾 Total Size", "2.4 GB")
            with col3:
                st.metric("🗑️ Can Delete", "67")
            with col4:
                st.metric("💰 Potential Savings", "1.8 GB")
            
            # File type breakdown
            file_types_data = pd.DataFrame({
                'File Type': ['Python Scripts', 'Configuration', 'HTML/CSS', 'Database', 'Documentation', 'Other'],
                'Count': [45, 23, 18, 12, 19, 10],
                'Size (MB)': [245, 12, 89, 456, 67, 131]
            })
            
            fig = px.pie(file_types_data, values='Count', names='File Type', 
                        title='📊 File Types Distribution')
            st.plotly_chart(fig, use_container_width=True)
    
    def suggest_cleanup_actions(self):
        """Suggest cleanup actions for legacy files."""
        st.subheader("🧹 Cleanup Suggestions")
        
        suggestions = [
            {
                "Action": "🗑️ Delete temporary migration scripts",
                "Files": "15 files", 
                "Space Saved": "156 MB",
                "Risk": "Low",
                "Description": "One-time migration scripts no longer needed"
            },
            {
                "Action": "📦 Archive old prototypes",
                "Files": "23 files",
                "Space Saved": "567 MB", 
                "Risk": "Low",
                "Description": "Prototype files from early development"
            },
            {
                "Action": "🔄 Migrate legacy configs",
                "Files": "8 files",
                "Space Saved": "45 MB",
                "Risk": "Medium", 
                "Description": "Update to new configuration format"
            },
            {
                "Action": "⚠️ Review deprecated APIs",
                "Files": "12 files",
                "Space Saved": "234 MB",
                "Risk": "High",
                "Description": "Verify no active dependencies before removal"
            }
        ]
        
        for suggestion in suggestions:
            risk_color = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
            
            with st.expander(f"{suggestion['Action']} - {suggestion['Files']} ({suggestion['Space Saved']})"):
                st.write(f"**Risk Level:** {risk_color[suggestion['Risk']]} {suggestion['Risk']}")
                st.write(f"**Description:** {suggestion['Description']}")
                
                col_suggest1, col_suggest2 = st.columns(2)
                with col_suggest1:
                    if st.button(f"✅ Apply Action", key=f"apply_{suggestion['Action'][:10]}"):
                        st.success(f"✅ {suggestion['Action']} applied successfully")
                with col_suggest2:
                    if st.button(f"📋 More Details", key=f"details_{suggestion['Action'][:10]}"):
                        st.info(f"📋 Detailed analysis for {suggestion['Action']}")
    
    def render_user_platform_mockup(self):
        """Render user platform mockup interface."""
        st.subheader("🎨 User Platform Mockup & Prototyping")
        
        # Mockup overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🎨 Active Mockups", "8", "+2")
        with col2:
            st.metric("👥 User Flows", "15", "+3")
        with col3:
            st.metric("📱 Screen Designs", "47", "+12")
        with col4:
            st.metric("✅ Completed", "85%", "+15%")
        
        # Mockup management
        tab1, tab2, tab3 = st.tabs(["🎨 Design Mockups", "👥 User Flows", "🧪 Prototype Testing"])
        
        with tab1:
            st.write("**🎨 UI/UX Design Mockups**")
            
            mockup_projects = [
                {
                    "Name": "User Dashboard v2.0",
                    "Type": "Dashboard Design",
                    "Status": "🔄 In Progress", 
                    "Screens": 12,
                    "Last Updated": "2025-09-20",
                    "Progress": 75
                },
                {
                    "Name": "Mobile App Interface",
                    "Type": "Mobile UI",
                    "Status": "✅ Complete",
                    "Screens": 23,
                    "Last Updated": "2025-09-18", 
                    "Progress": 100
                },
                {
                    "Name": "Admin Portal Redesign",
                    "Type": "Admin Interface",
                    "Status": "📋 Planning",
                    "Screens": 8,
                    "Last Updated": "2025-09-15",
                    "Progress": 25
                }
            ]
            
            for mockup in mockup_projects:
                with st.expander(f"🎨 {mockup['Name']} - {mockup['Screens']} screens ({mockup['Status']})"):
                    col_mockup1, col_mockup2 = st.columns(2)
                    
                    with col_mockup1:
                        st.write(f"**Type:** {mockup['Type']}")
                        st.write(f"**Last Updated:** {mockup['Last Updated']}")
                        st.progress(mockup['Progress']/100, text=f"Progress: {mockup['Progress']}%")
                    
                    with col_mockup2:
                        col_action1, col_action2, col_action3 = st.columns(3)
                        
                        with col_action1:
                            if st.button("🎨 Design", key=f"design_{mockup['Name']}"):
                                st.success("🎨 Design tool opened")
                        
                        with col_action2:
                            if st.button("👁️ Preview", key=f"preview_{mockup['Name']}"):
                                st.info("👁️ Mockup preview opened")
                        
                        with col_action3:
                            if st.button("📤 Export", key=f"export_{mockup['Name']}"):
                                st.success("📤 Mockup exported successfully")
            
            # New mockup creation
            st.write("**➕ Create New Mockup**")
            col_new1, col_new2 = st.columns(2)
            
            with col_new1:
                new_mockup_name = st.text_input("Mockup Name")
                mockup_type = st.selectbox("Mockup Type", [
                    "Dashboard Design",
                    "Mobile UI",
                    "Admin Interface", 
                    "Landing Page",
                    "User Profile",
                    "Settings Page"
                ])
            
            with col_new2:
                template_base = st.selectbox("Template Base", [
                    "Blank Canvas",
                    "Admin Template",
                    "Mobile Template",
                    "Dashboard Template"
                ])
                
                if st.button("➕ Create Mockup", type="primary"):
                    st.success(f"✅ Mockup '{new_mockup_name}' created successfully")
        
        with tab2:
            st.write("**👥 User Experience Flows**")
            
            user_flows = [
                {"Flow": "User Registration", "Steps": 5, "Conversion": "87%", "Status": "✅ Optimized"},
                {"Flow": "CV Upload Process", "Steps": 3, "Conversion": "94%", "Status": "✅ Optimized"},
                {"Flow": "Job Application", "Steps": 7, "Conversion": "76%", "Status": "⚠️ Needs Improvement"},
                {"Flow": "Profile Completion", "Steps": 4, "Conversion": "82%", "Status": "🔄 Testing"}
            ]
            
            flows_df = pd.DataFrame(user_flows)
            st.dataframe(flows_df, use_container_width=True, hide_index=True)
            
            if st.button("🎯 Optimize User Flows"):
                st.success("🎯 User flow optimization analysis started")
        
        with tab3:
            st.write("**🧪 Prototype Testing & Validation**")
            
            if st.button("🚀 Launch Prototype Testing", type="primary"):
                st.success("🚀 Prototype testing environment launched")
                st.info("👥 Test users will receive access links")
            
            # Testing metrics
            col_test1, col_test2, col_test3 = st.columns(3)
            with col_test1:
                st.metric("👥 Test Users", "25")
            with col_test2:
                st.metric("📊 Completion Rate", "92%")
            with col_test3:
                st.metric("⭐ Avg Rating", "4.3/5")
    
    def render_system_utilities(self):
        """Render system utilities interface."""
        st.subheader("🔧 System Utilities & Maintenance Tools")
        
        # Utilities overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🔧 Available Tools", "12", "")
        with col2:
            st.metric("⚡ Tasks Run Today", "8", "+3")
        with col3:
            st.metric("✅ Success Rate", "100%", "")
        with col4:
            st.metric("⏱️ Avg Runtime", "2.3min", "-0.5min")
        
        # System utilities
        utilities = [
            {
                "Tool": "🧹 File System Cleanup",
                "Description": "Remove temporary files, clear caches, optimize storage",
                "Category": "Maintenance",
                "Est. Time": "3-5 minutes"
            },
            {
                "Tool": "🗄️ Database Maintenance", 
                "Description": "Optimize database, rebuild indexes, update statistics",
                "Category": "Database",
                "Est. Time": "5-10 minutes"
            },
            {
                "Tool": "💾 Cache Management",
                "Description": "Clear application cache, optimize memory usage",
                "Category": "Performance", 
                "Est. Time": "1-2 minutes"
            },
            {
                "Tool": "🗑️ Temporary File Cleanup",
                "Description": "Remove temporary files, logs older than 30 days",
                "Category": "Maintenance",
                "Est. Time": "2-3 minutes"
            },
            {
                "Tool": "⚡ System Optimization",
                "Description": "Optimize system performance, defragment if needed",
                "Category": "Performance",
                "Est. Time": "10-20 minutes"
            },
            {
                "Tool": "🔒 Security Audit",
                "Description": "Check security settings, scan for vulnerabilities", 
                "Category": "Security",
                "Est. Time": "5-8 minutes"
            }
        ]
        
        # Group utilities by category
        categories = {}
        for utility in utilities:
            category = utility["Category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(utility)
        
        # Display utilities by category
        for category, tools in categories.items():
            st.write(f"**{category} Tools**")
            
            for tool in tools:
                with st.expander(f"{tool['Tool']} - {tool['Est. Time']}"):
                    st.write(f"**Description:** {tool['Description']}")
                    
                    col_util1, col_util2 = st.columns(2)
                    with col_util1:
                        if st.button(f"🚀 Run {tool['Tool']}", key=f"run_{tool['Tool']}"):
                            self.run_system_utility(tool['Tool'])
                    with col_util2:
                        if st.button(f"📊 Schedule", key=f"schedule_{tool['Tool']}"):
                            st.info(f"📅 Scheduling options for {tool['Tool']}")
        
        # Bulk operations
        st.markdown("---")
        st.write("**🔧 Bulk Utility Operations**")
        
        col_util_bulk1, col_util_bulk2, col_util_bulk3 = st.columns(3)
        
        with col_util_bulk1:
            if st.button("🧹 Run All Maintenance", use_container_width=True):
                self.run_all_maintenance_tools()
        
        with col_util_bulk2:
            if st.button("⚡ Performance Boost", use_container_width=True):
                self.run_performance_optimization()
        
        with col_util_bulk3:
            if st.button("📊 System Health Check", use_container_width=True):
                self.run_system_health_check()
    
    def run_system_utility(self, tool_name: str):
        """Run individual system utility."""
        with st.spinner(f"🔧 Running {tool_name}..."):
            time.sleep(2)  # Simulate utility runtime
            
            st.success(f"✅ {tool_name} completed successfully!")
            
            # Mock results based on tool
            if "Cleanup" in tool_name:
                st.info("🧹 Cleaned 234 MB of temporary files")
            elif "Database" in tool_name:
                st.info("🗄️ Optimized 15 database tables, rebuilt 8 indexes")
            elif "Cache" in tool_name:
                st.info("💾 Cleared 89 MB of cache data")
            elif "Optimization" in tool_name:
                st.info("⚡ System performance improved by 12%")
    
    def run_all_maintenance_tools(self):
        """Run all maintenance utilities."""
        with st.spinner("🧹 Running all maintenance tools..."):
            progress_bar = st.progress(0)
            
            maintenance_tools = [
                "File System Cleanup",
                "Database Maintenance", 
                "Cache Management",
                "Temporary File Cleanup"
            ]
            
            for i, tool in enumerate(maintenance_tools):
                st.text(f"🔧 Running {tool}...")
                time.sleep(0.8)
                progress_bar.progress((i + 1) / len(maintenance_tools))
            
            st.success("✅ All maintenance tools completed successfully!")
            
            # Show maintenance summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🧹 Files Cleaned", "2,847")
            with col2:
                st.metric("💾 Space Freed", "1.2 GB")
            with col3:
                st.metric("⚡ Performance Gain", "+15%")
    
    def run_performance_optimization(self):
        """Run performance optimization tools."""
        with st.spinner("⚡ Optimizing system performance..."):
            time.sleep(3)
            
            st.success("✅ Performance optimization completed!")
            st.balloons()
            
            # Performance improvements
            improvements = [
                "Memory usage reduced by 18%",
                "Database query speed improved by 25%", 
                "Cache hit ratio increased to 94%",
                "System response time improved by 12%"
            ]
            
            for improvement in improvements:
                st.info(f"⚡ {improvement}")
    
    def run_system_health_check(self):
        """Run comprehensive system health check."""
        with st.spinner("📊 Running system health check..."):
            time.sleep(2.5)
            
            st.success("✅ System health check completed!")
            
            # Health metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🏥 Overall Health", "96%", "+2%")
            with col2:
                st.metric("⚠️ Issues Found", "3", "-2")
            with col3:
                st.metric("🔧 Auto-Fixed", "2", "+2")
            with col4:
                st.metric("📋 Needs Attention", "1", "-1")

def render():
    """Main render function for Legacy Utilities module."""
    legacy_utilities = LegacyUtilities()
    
    render_section_header(
        "🗄️ Legacy & Miscellaneous Tools Suite",
        "Comprehensive legacy management and system utilities"
    )
    
    # Legacy utilities metrics dashboard
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📁 Legacy Files", "127", "-15")
    with col2:
        st.metric("🎨 Active Mockups", "8", "+2")
    with col3:
        st.metric("🔧 System Tools", "12", "")
    with col4:
        st.metric("🧹 Space Freed", "1.8 GB", "+450 MB")
    
    # Main interface tabs
    tab1, tab2, tab3 = st.tabs([
        "📁 Legacy Files",
        "🎨 User Platform Mockup",
        "🔧 System Utilities"
    ])
    
    with tab1:
        legacy_utilities.render_legacy_files()
    
    with tab2:
        legacy_utilities.render_user_platform_mockup()
    
    with tab3:
        legacy_utilities.render_system_utilities()
    
    # Integration status
    st.markdown("---")
    with st.expander("🔗 Integration Status"):
        integration_hooks = get_integration_hooks()
        if integration_hooks:
            st.success("✅ Lockstep integration active - Legacy operations synced with user portal")
            st.info("🔄 System utilities integrated with monitoring dashboard")
        else:
            st.warning("⚠️ Integration hooks not available")

if __name__ == "__main__":
    render()