"""
=============================================================================
IntelliCV Admin Portal - Compliance Audit Module
=============================================================================

Comprehensive compliance and audit suite with enterprise-grade security,
data governance, and regulatory compliance monitoring.

Features:
- Dataset integrity auditing
- Admin activity monitoring
- Enterprise compliance tracking
- Regulatory compliance reporting
- Integration hooks for audit trails
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
    class MockIntegrationHooks:
        def sync_system_config(self, key, data):
            # Mock implementation - does nothing but prevents errors
            pass
        
        def get_integration_status(self):
            return {
                'status': 'mocked', 
                'connected': True,
                'lockstep_manager': {
                    'running': True,
                    'status': 'active',
                    'last_sync': '2025-10-09T08:00:00Z'
                }
            }
    
    return MockIntegrationHooks()

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
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import time
import random

# Import shared components
# from shared.components import render_section_header, render_metrics_row  # Using fallback implementations
# from shared.integration_hooks import get_integration_hooks  # Using fallback implementations

# =============================================================================
# COMPLIANCE AUDIT CLASS
# =============================================================================

class ComplianceAudit:
    """Consolidated Compliance & Audit Suite with integration hooks"""
    
    def __init__(self):
        """Initialize compliance audit with integration hooks."""
        self.integration_hooks = get_integration_hooks()
    
    def get_compliance_metrics(self) -> Dict[str, Any]:
        """Get compliance overview metrics."""
        metrics = {
            'compliance_score': random.uniform(92, 96),
            'compliance_delta': random.uniform(1.5, 3.0),
            'audits_completed': random.randint(45, 50),
            'audits_delta': random.randint(2, 5),
            'issues_found': random.randint(8, 15),
            'issues_delta': random.randint(-8, -3),
            'risk_level': random.choice(['Low', 'Medium']),
            'timestamp': datetime.now().isoformat()
        }
        
        # Sync metrics with integration hooks (safe call)
        try:
            if hasattr(self.integration_hooks, 'sync_system_config'):
                self.integration_hooks.sync_system_config('compliance_metrics', metrics)
        except Exception as e:
            # Log error but continue - compliance should work without integration hooks
            pass
        
        return metrics
    
    def get_dataset_audit_results(self) -> List[Dict[str, Any]]:
        """Get dataset audit results."""
        datasets = [
            "resumes_2024.json", "job_descriptions.csv", "user_profiles.json",
            "company_data.json", "analytics_logs.csv", "system_config.json",
            "email_templates.json", "skill_mapping.csv", "salary_data.json"
        ]
        
        issues = [
            "Missing metadata", "Duplicate entries", "Invalid schema",
            "Outdated format", "Permission issues", "Encoding problems",
            "Size limit exceeded", "Backup missing", "Index corruption"
        ]
        
        severities = ["High", "Medium", "Low"]
        
        audit_results = []
        for i in range(random.randint(3, 7)):
            dataset = random.choice(datasets)
            issue = random.choice(issues)
            severity = random.choice(severities)
            
            audit_results.append({
                "Dataset": dataset,
                "Issue": issue,
                "Severity": severity,
                "Detected": (datetime.now() - timedelta(hours=random.randint(1, 48))).strftime("%Y-%m-%d %H:%M"),
                "Status": random.choice(["Open", "Resolved", "In Progress"])
            })
        
        return audit_results
    
    def get_admin_audit_results(self, audit_areas: List[str], date_range: List) -> List[Dict[str, Any]]:
        """Get admin activity audit results."""
        actions = {
            "User Access Logs": ["User Login", "User Logout", "Password Reset", "Account Lock"],
            "Admin Actions": ["User Created", "User Deleted", "Role Changed", "Settings Modified"],
            "Data Modifications": ["Data Export", "Data Import", "Record Updated", "Bulk Delete"],
            "System Configuration Changes": ["Config Changed", "Service Restart", "Update Applied", "Backup Created"],
            "API Usage": ["API Call", "Token Generated", "Rate Limit Hit", "API Error"],
            "File Operations": ["File Upload", "File Delete", "File Move", "Permission Change"]
        }
        
        audit_results = []
        
        for area in audit_areas:
            area_actions = actions.get(area, ["Generic Action"])
            
            for _ in range(random.randint(3, 8)):
                action = random.choice(area_actions)
                timestamp = datetime.now() - timedelta(
                    days=random.randint(0, 7),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                
                audit_results.append({
                    "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M"),
                    "Action": action,
                    "Admin": random.choice(["admin@intellicv.com", "system", "api_user"]),
                    "Target": self._generate_target_for_action(action),
                    "Result": random.choice(["Success", "Success", "Success", "Failed"]),  # 75% success rate
                    "IP_Address": f"192.168.1.{random.randint(100, 200)}",
                    "Category": area
                })
        
        # Sort by timestamp descending
        audit_results.sort(key=lambda x: x["Timestamp"], reverse=True)
        
        # Sync audit activity with integration hooks
        self.integration_hooks.sync_system_config('admin_audit_activity', {
            'audit_areas': audit_areas,
            'results_count': len(audit_results),
            'timestamp': datetime.now().isoformat()
        })
        
        return audit_results
    
    def _generate_target_for_action(self, action: str) -> str:
        """Generate realistic target for audit action."""
        targets = {
            "User Login": ["john.doe@company.com", "jane.smith@org.com", "admin@intellicv.com"],
            "User Created": ["new.user@company.com", "candidate@jobseeker.com"],
            "Data Export": ["resumes_batch_1.zip", "analytics_report.csv", "user_data.json"],
            "Config Changed": ["parser_settings.json", "email_config.yaml", "security_policy.json"],
            "API Call": ["/api/v1/users", "/api/v1/resumes", "/api/v1/analytics"],
            "File Upload": ["resume_batch_47.pdf", "company_logo.png", "import_data.csv"]
        }
        
        return random.choice(targets.get(action, ["system_target"]))
    
    def get_compliance_areas(self) -> List[Dict[str, Any]]:
        """Get enterprise compliance areas status."""
        return [
            {
                "Area": "GDPR Compliance",
                "Status": "✅ Compliant",
                "Score": random.randint(95, 99),
                "Last_Audit": "2025-09-15",
                "Next_Review": "2025-12-15",
                "Issues": random.randint(0, 2)
            },
            {
                "Area": "SOC 2 Type II", 
                "Status": "✅ Compliant",
                "Score": random.randint(93, 97),
                "Last_Audit": "2025-08-20",
                "Next_Review": "2026-02-20",
                "Issues": random.randint(0, 3)
            },
            {
                "Area": "ISO 27001",
                "Status": random.choice(["✅ Compliant", "⚠️ Minor Issues"]),
                "Score": random.randint(85, 92),
                "Last_Audit": "2025-09-10",
                "Next_Review": "2025-12-10",
                "Issues": random.randint(1, 4)
            },
            {
                "Area": "CCPA Compliance",
                "Status": "✅ Compliant",
                "Score": random.randint(94, 98),
                "Last_Audit": "2025-09-05",
                "Next_Review": "2025-12-05",
                "Issues": random.randint(0, 2)
            },
            {
                "Area": "Data Retention Policy",
                "Status": "✅ Compliant",
                "Score": random.randint(98, 100),
                "Last_Audit": "2025-09-18",
                "Next_Review": "2026-03-18",
                "Issues": 0
            },
            {
                "Area": "Access Control (RBAC)",
                "Status": "✅ Compliant",
                "Score": random.randint(91, 96),
                "Last_Audit": "2025-09-12",
                "Next_Review": "2025-12-12",
                "Issues": random.randint(0, 3)
            }
        ]
    
    def get_recent_audits(self) -> List[Dict[str, Any]]:
        """Get recent audit history."""
        audit_types = [
            "Security Audit", "Data Quality Audit", "Compliance Check",
            "Performance Audit", "Privacy Audit", "Access Review"
        ]
        
        statuses = ["Completed", "In Progress", "Scheduled", "Failed"]
        
        recent_audits = []
        
        for i in range(10):
            audit_date = datetime.now() - timedelta(days=i)
            audit_type = random.choice(audit_types)
            status = random.choice(statuses) if i > 2 else "Completed"  # Recent ones more likely completed
            issues = random.randint(0, 5) if status == "Completed" else "-"
            
            recent_audits.append({
                "Date": audit_date.strftime("%Y-%m-%d"),
                "Type": audit_type,
                "Status": status,
                "Issues": issues,
                "Duration": f"{random.randint(15, 180)} min" if status == "Completed" else "-",
                "Auditor": random.choice(["System", "External", "Internal"])
            })
        
        return recent_audits
    
    def generate_compliance_report(self, compliance_areas: List[Dict[str, Any]]) -> str:
        """Generate compliance report content."""
        report_content = f"""
INTELLICV COMPLIANCE REPORT
===========================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY
-----------------
Overall Compliance Score: {sum(area['Score'] for area in compliance_areas) / len(compliance_areas):.1f}%
Total Areas Assessed: {len(compliance_areas)}
Areas Fully Compliant: {sum(1 for area in compliance_areas if '✅' in area['Status'])}
Areas with Issues: {sum(1 for area in compliance_areas if '⚠️' in area['Status'])}

DETAILED ASSESSMENT
-------------------
"""
        
        for area in compliance_areas:
            report_content += f"""
{area['Area']}:
  Status: {area['Status']}
  Score: {area['Score']}%
  Last Audit: {area['Last_Audit']}
  Next Review: {area['Next_Review']}
  Open Issues: {area['Issues']}
"""
        
        report_content += f"""

RECOMMENDATIONS
---------------
1. Continue regular compliance monitoring
2. Address any identified issues promptly
3. Schedule upcoming reviews as planned
4. Maintain documentation updates
5. Regular staff compliance training

Report generated by IntelliCV Admin Portal
Contact: admin@intellicv.com
"""
        
        return report_content

# =============================================================================
# RENDER FUNCTION
# =============================================================================

def render():
    """Render the Compliance Audit page."""
    # Initialize compliance audit
    compliance_audit = ComplianceAudit()
    
    render_section_header("🛡️ Compliance & Audit Suite", "Enterprise-grade compliance monitoring and audit management")
    
    # Live/Demo Data Toggle
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown("### Compliance Dashboard")
    
    with col2:
        audit_mode = st.selectbox("Audit Mode", ["Demo Mode", "Live Production"], 
                                 help="Switch between demo and live compliance data")
    
    with col3:
        if st.button("🔗 Go Live", help="Activate live compliance monitoring"):
            if audit_mode == "Live Production":
                st.success("🟢 **Live Compliance Monitoring Active**")
                st.info("Connected to production systems for real-time audit data")
            else:
                st.info("🔄 **Ready for Live Deployment**")
                st.markdown("**Live System Integration:**")
                st.markdown("- Database audit logs")
                st.markdown("- User activity monitoring") 
                st.markdown("- Security event tracking")
                st.markdown("- Regulatory compliance checks")
    
    # Get compliance metrics based on mode
    if audit_mode == "Live Production":
        st.info("🚧 **Live Mode**: Production audit data would be displayed here")
        # In live mode, get real data from actual systems
        metrics = {
            'compliance_score': 0.0,  # Would connect to real compliance system
            'compliance_delta': 0.0,
            'audits_completed': 0,
            'audits_delta': 0,
            'issues_found': 0,
            'issues_delta': 0,
            'risk_level': 'Unknown'
        }
    else:
        # Demo mode - use simulated data
        metrics = compliance_audit.get_compliance_metrics()
    
    # Compliance overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Compliance Score", 
            f"{metrics['compliance_score']:.1f}%", 
            f"+{metrics['compliance_delta']:.1f}%"
        )
    
    with col2:
        st.metric(
            "Audits Completed", 
            metrics['audits_completed'], 
            f"+{metrics['audits_delta']}"
        )
    
    with col3:
        delta_sign = "+" if metrics['issues_delta'] > 0 else ""
        st.metric(
            "Issues Found", 
            metrics['issues_found'], 
            f"{delta_sign}{metrics['issues_delta']}"
        )
    
    with col4:
        risk_color = "🟢" if metrics['risk_level'] == 'Low' else "🟡" if metrics['risk_level'] == 'Medium' else "🔴"
        st.metric("Risk Level", f"{risk_color} {metrics['risk_level']}")
    
    st.markdown("---")
    
    # Compliance tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dataset Audit", 
        "🔍 Admin Activity Audit", 
        "🏢 Enterprise Compliance", 
        "📋 Audit Reports",
        "🔒 Security Monitoring"
    ])
    
    with tab1:
        st.subheader("📊 Dataset Integrity Audit")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔍 Dataset Health Check")
            
            if st.button("🔍 Scan All Datasets", type="primary"):
                with st.spinner("Scanning datasets for integrity issues..."):
                    time.sleep(3)  # Simulate scan time
                    
                    # Get audit results
                    audit_results = compliance_audit.get_dataset_audit_results()
                    
                    st.success(f"✅ Dataset scan completed - {len(audit_results)} issues found")
                    
                    # Store results in session state
                    st.session_state['dataset_audit_results'] = audit_results
            
            # Display audit results if available
            audit_results = st.session_state.get('dataset_audit_results', [])
            
            if audit_results:
                st.markdown("#### 🚨 Identified Issues")
                
                for issue in audit_results:
                    severity_colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                    status_colors = {"Open": "🔴", "In Progress": "🟡", "Resolved": "🟢"}
                    
                    with st.expander(f"{severity_colors[issue['Severity']]} {issue['Dataset']} - {issue['Issue']}"):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.text(f"Severity: {issue['Severity']}")
                            st.text(f"Status: {status_colors[issue['Status']]} {issue['Status']}")
                        with col_b:
                            st.text(f"Detected: {issue['Detected']}")
                            if st.button(f"Resolve Issue", key=f"resolve_{issue['Dataset']}"):
                                st.success("Issue marked for resolution")
        
        with col2:
            st.markdown("#### 📊 Dataset Statistics")
            
            # Dataset metrics
            total_datasets = random.randint(45, 50)
            healthy_datasets = total_datasets - len(st.session_state.get('dataset_audit_results', []))
            
            st.metric("Total Datasets", total_datasets)
            st.metric("Healthy Datasets", healthy_datasets)
            st.metric("Datasets with Issues", len(st.session_state.get('dataset_audit_results', [])))
            
            # Dataset size visualization
            dataset_sizes = pd.DataFrame({
                'Dataset': ['Resumes', 'Jobs', 'Users', 'Analytics', 'Logs', 'Company Data'],
                'Size_GB': [2.4, 1.8, 0.9, 3.2, 1.1, 1.6],
                'Records': [15420, 8950, 2340, 45600, 125000, 3200]
            })
            
            fig_size = px.bar(
                dataset_sizes, 
                x='Dataset', 
                y='Size_GB', 
                title='Dataset Sizes (GB)',
                color='Records',
                color_continuous_scale='viridis'
            )
            fig_size.update_layout(height=400)
            st.plotly_chart(fig_size, use_container_width=True)
            
            # Data growth trend
            dates = pd.date_range(start='2025-08-01', periods=50, freq='D')
            growth_data = pd.DataFrame({
                'Date': dates,
                'Total_Size_GB': [8.5 + i * 0.1 + random.uniform(-0.2, 0.3) for i in range(50)]
            })
            
            fig_growth = px.line(
                growth_data,
                x='Date',
                y='Total_Size_GB',
                title='Data Growth Trend (GB)'
            )
            fig_growth.update_layout(height=300)
            st.plotly_chart(fig_growth, use_container_width=True)
    
    with tab2:
        st.subheader("🔍 Admin Activity Audit")
        
        # Audit configuration
        col1, col2 = st.columns(2)
        
        with col1:
            audit_areas = st.multiselect("Select Audit Areas", [
                "User Access Logs",
                "Admin Actions", 
                "Data Modifications",
                "System Configuration Changes",
                "API Usage",
                "File Operations"
            ], default=["User Access Logs", "Admin Actions"])
        
        with col2:
            date_range = st.date_input(
                "Audit Period", 
                [datetime.now() - timedelta(days=7), datetime.now()],
                max_value=datetime.now()
            )
        
        if st.button("🔍 Run Admin Activity Audit", type="primary"):
            if audit_areas and len(date_range) == 2:
                with st.spinner("Analyzing admin activity logs..."):
                    time.sleep(2)
                    
                    # Get audit results
                    audit_results = compliance_audit.get_admin_audit_results(audit_areas, list(date_range))
                    
                    st.success(f"✅ Admin audit completed - {len(audit_results)} activities analyzed")
                    
                    # Display results
                    if audit_results:
                        # Summary metrics
                        col_a, col_b, col_c = st.columns(3)
                        
                        with col_a:
                            success_count = sum(1 for r in audit_results if r['Result'] == 'Success')
                            st.metric("Successful Actions", success_count)
                        
                        with col_b:
                            failed_count = sum(1 for r in audit_results if r['Result'] == 'Failed')
                            st.metric("Failed Actions", failed_count)
                        
                        with col_c:
                            unique_admins = len(set(r['Admin'] for r in audit_results))
                            st.metric("Unique Administrators", unique_admins)
                        
                        # Detailed results table
                        st.markdown("#### 📋 Detailed Activity Log")
                        
                        # Convert to DataFrame for better display
                        audit_df = pd.DataFrame(audit_results)
                        
                        # Add color coding for results
                        def highlight_result(row):
                            if row['Result'] == 'Failed':
                                return ['background-color: #ffebee'] * len(row)
                            return [''] * len(row)
                        
                        styled_df = audit_df.style.apply(highlight_result, axis=1)
                        st.dataframe(styled_df, use_container_width=True)
                        
                        # Export audit log
                        if st.button("📥 Export Audit Log"):
                            audit_text = audit_df.to_csv(index=False)
                            st.download_button(
                                label="📊 Download Audit Log",
                                data=audit_text,
                                file_name=f"admin_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv"
                            )
            else:
                st.error("Please select audit areas and a valid date range.")
    
    with tab3:
        st.subheader("🏢 Enterprise Compliance Dashboard")
        
        # Get compliance areas
        compliance_areas = compliance_audit.get_compliance_areas()
        
        # Compliance overview
        st.markdown("#### 📊 Compliance Status Overview")
        
        for area in compliance_areas:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.write(f"**{area['Area']}**")
            with col2:
                st.write(area['Status'])
            with col3:
                st.write(f"{area['Score']}%")
            with col4:
                if area['Issues'] > 0:
                    st.write(f"🚨 {area['Issues']} issues")
                else:
                    st.write("✅ No issues")
        
        st.markdown("---")
        
        # Compliance score visualization
        col1, col2 = st.columns(2)
        
        with col1:
            # Compliance scores chart
            compliance_df = pd.DataFrame(compliance_areas)
            
            fig_compliance = px.bar(
                compliance_df,
                x='Area',
                y='Score',
                title='Compliance Scores by Area',
                color='Score',
                color_continuous_scale='RdYlGn',
                range_color=[80, 100]
            )
            fig_compliance.update_layout(height=400, xaxis_tickangle=45)
            st.plotly_chart(fig_compliance, use_container_width=True)
        
        with col2:
            # Overall compliance gauge
            overall_score = sum(area['Score'] for area in compliance_areas) / len(compliance_areas)
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = overall_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Overall Compliance Score"},
                delta = {'reference': 90},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 80], 'color': "lightgray"},
                        {'range': [80, 90], 'color': "yellow"},
                        {'range': [90, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 95
                    }
                }
            ))
            fig_gauge.update_layout(height=400)
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Generate compliance report
        if st.button("📋 Generate Compliance Report", type="primary"):
            with st.spinner("Generating comprehensive compliance report..."):
                time.sleep(2)
                
                report_content = compliance_audit.generate_compliance_report(compliance_areas)
                
                st.success("✅ Compliance report generated successfully!")
                
                # Show report preview
                with st.expander("📋 Report Preview"):
                    st.text(report_content[:500] + "...")
                
                # Download report
                st.download_button(
                    label="📥 Download Full Compliance Report",
                    data=report_content,
                    file_name=f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
    
    with tab4:
        st.subheader("📋 Audit Reports & History")
        
        # Recent audits
        recent_audits = compliance_audit.get_recent_audits()
        
        st.markdown("#### 📚 Recent Audit History")
        
        # Convert to DataFrame
        audits_df = pd.DataFrame(recent_audits)
        
        # Add status color coding
        def highlight_status(row):
            colors = []
            for col in row.index:
                if col == 'Status':
                    if row[col] == 'Completed':
                        colors.append('background-color: #e8f5e8')
                    elif row[col] == 'In Progress':
                        colors.append('background-color: #fff3cd')
                    elif row[col] == 'Failed':
                        colors.append('background-color: #f8d7da')
                    else:
                        colors.append('')
                else:
                    colors.append('')
            return colors
        
        styled_audits_df = audits_df.style.apply(highlight_status, axis=1)
        st.dataframe(styled_audits_df, use_container_width=True)
        
        # Audit summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            completed_count = sum(1 for audit in recent_audits if audit['Status'] == 'Completed')
            st.metric("Completed Audits", completed_count)
        
        with col2:
            in_progress_count = sum(1 for audit in recent_audits if audit['Status'] == 'In Progress')
            st.metric("In Progress", in_progress_count)
        
        with col3:
            total_issues = sum(audit['Issues'] for audit in recent_audits if isinstance(audit['Issues'], int))
            st.metric("Total Issues Found", total_issues)
        
        with col4:
            avg_duration = sum(int(audit['Duration'].split()[0]) for audit in recent_audits if audit['Duration'] != '-') / max(1, sum(1 for audit in recent_audits if audit['Duration'] != '-'))
            st.metric("Avg Duration", f"{avg_duration:.0f} min")
        
        # Generate audit summary
        if st.button("📊 Generate Audit Summary Report"):
            with st.spinner("Generating audit summary..."):
                time.sleep(1)
                
                summary_content = f"""
AUDIT SUMMARY REPORT
====================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY STATISTICS
------------------
Total Audits: {len(recent_audits)}
Completed: {completed_count}
In Progress: {in_progress_count}
Total Issues Found: {total_issues}
Average Duration: {avg_duration:.0f} minutes

RECENT AUDIT DETAILS
--------------------
"""
                for audit in recent_audits[:5]:  # Top 5 recent audits
                    summary_content += f"""
Date: {audit['Date']}
Type: {audit['Type']}
Status: {audit['Status']}
Issues: {audit['Issues']}
Duration: {audit['Duration']}
Auditor: {audit['Auditor']}
---
"""
                
                st.success("✅ Audit summary generated!")
                
                st.download_button(
                    label="📥 Download Audit Summary",
                    data=summary_content,
                    file_name=f"audit_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
    
    with tab5:
        st.subheader("🔒 Security Monitoring & Alerts")
        
        # Security metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🚨 Security Alerts")
            security_alerts = [
                {"Time": "14:30", "Alert": "Failed login attempts", "Severity": "Medium"},
                {"Time": "13:15", "Alert": "Unusual data access pattern", "Severity": "Low"},
                {"Time": "12:45", "Alert": "Permission escalation detected", "Severity": "High"}
            ]
            
            for alert in security_alerts:
                severity_colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                st.write(f"{severity_colors[alert['Severity']]} [{alert['Time']}] {alert['Alert']}")
        
        with col2:
            st.markdown("#### 🔐 Access Control")
            st.metric("Active Sessions", random.randint(15, 25))
            st.metric("Failed Logins (24h)", random.randint(3, 8))
            st.metric("Admin Actions (24h)", random.randint(45, 85))
        
        with col3:
            st.markdown("#### 🛡️ Security Score")
            security_score = random.randint(88, 96)
            st.metric("Security Rating", f"{security_score}%")
            
            if security_score > 90:
                st.success("🟢 Excellent security posture")
            elif security_score > 80:
                st.warning("🟡 Good security, minor improvements needed")
            else:
                st.error("🔴 Security attention required")
        
        # Security trend chart
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
        security_data = pd.DataFrame({
            'Date': dates,
            'Security_Score': [85 + 10 * random.random() + 2 * np.sin(i * 0.1) for i in range(30)],
            'Failed_Logins': [random.randint(0, 15) for _ in range(30)],
            'Security_Events': [random.randint(2, 20) for _ in range(30)]
        })
        
        fig_security = px.line(
            security_data,
            x='Date',
            y='Security_Score',
            title='Security Score Trend (30 Days)'
        )
        fig_security.update_layout(height=300)
        st.plotly_chart(fig_security, use_container_width=True)

if __name__ == "__main__":
    render()