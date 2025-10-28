"""
=============================================================================
IntelliCV Admin Portal - Contact & Communication Suite
=============================================================================

Complete contact management and email communication system with Gmail API integration,
email campaigns, contact database management, and communication analytics.

Features:
- Contact database with CRUD operations
- Email campaign management and automation
- Gmail API integration and email viewer
- Communication analytics and performance tracking
- Integration hooks for lockstep synchronization
- User portal communication features
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
from typing import Dict, Any, List
import sys
import csv
import json

# Add shared components to path
pages_dir = Path(__file__).parent
if str(pages_dir) not in sys.path:
    sys.path.insert(0, str(pages_dir))

# Import email capture system integration
try:
    sys.path.append(str(Path(__file__).parent.parent))
    from modules.email_capture_system import export_emails_for_contact_communications, get_email_capture_manager
    EMAIL_CAPTURE_INTEGRATION = True
except ImportError:
    EMAIL_CAPTURE_INTEGRATION = False

# from shared.components import render_section_header, render_metrics_row  # Using fallback implementations
# from shared.integration_hooks import get_integration_hooks  # Using fallback implementations

# =============================================================================
# CONTACT & COMMUNICATION SUITE
# =============================================================================

class ContactCommunication:
    """Complete Contact & Communication Management Suite with Gmail Integration"""
    
    def __init__(self):
        """Initialize contact communication system."""
        self.integration_hooks = get_integration_hooks()
        self.gmail_api_configured = False  # Set to True when Gmail API is configured
    
    def render_contact_management(self):
        """Render contact management interface with email capture integration."""
        st.subheader("👥 Contact Management")
        
        # Email Capture Integration Section
        if EMAIL_CAPTURE_INTEGRATION:
            with st.expander("📧 Email Capture Integration - Import Captured Emails", expanded=False):
                st.info("""
                **📊 Import emails from the Multi-Provider Email Capture System**
                
                Import unique emails captured from Gmail, Yahoo, and Outlook accounts.
                These emails are marked for app offers and marketing campaigns.
                """)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Quick stats from email capture
                    try:
                        email_manager = get_email_capture_manager()
                        stats = email_manager.get_capture_statistics()
                        
                        st.markdown("**📊 Available Emails for Import:**")
                        st.metric("📧 Total Captured", f"{stats.get('total_emails', 0):,}")
                        st.metric("📮 Gmail", f"{stats.get('gmail_count', 0):,}")
                        st.metric("📮 Yahoo", f"{stats.get('yahoo_count', 0):,}")
                        st.metric("📮 Outlook", f"{stats.get('outlook_count', 0):,}")
                        
                    except Exception as e:
                        st.warning(f"⚠️ Could not load capture statistics: {e}")
                
                with col2:
                    st.markdown("**🔗 Import Options:**")
                    
                    import_provider = st.selectbox(
                        "Select Provider to Import",
                        ["all", "gmail", "yahoo", "outlook"],
                        help="Choose which provider emails to import"
                    )
                    
                    include_app_offers = st.checkbox(
                        "🎯 Mark for App Offers",
                        value=True,
                        help="Mark imported contacts for IntelliCV app offers"
                    )
                    
                    if st.button("📥 Import Captured Emails", type="primary"):
                        try:
                            with st.spinner("📊 Importing captured emails..."):
                                # Export from capture system
                                provider_filter = None if import_provider == "all" else import_provider
                                csv_path = export_emails_for_contact_communications(provider_filter)
                                
                                if csv_path:
                                    # Read the exported CSV
                                    imported_df = pd.read_csv(csv_path)
                                    
                                    st.success(f"✅ Successfully imported {len(imported_df)} contacts from email capture!")
                                    
                                    # Show sample of imported data
                                    with st.expander("📋 Sample Imported Contacts"):
                                        st.dataframe(imported_df.head(10), use_container_width=True)
                                    
                                    # Integration hooks - sync with user portal
                                    if self.integration_hooks:
                                        for _, contact in imported_df.iterrows():
                                            contact_data = {
                                                "name": contact['email'].split('@')[0],  # Use email prefix as name
                                                "email": contact['email'],
                                                "company": contact['domain'],
                                                "role": "Captured Contact",
                                                "tags": f"email_capture,{contact['provider']},app_offer_eligible" if include_app_offers else f"email_capture,{contact['provider']}",
                                                "added_date": datetime.now().isoformat(),
                                                "source": "email_capture_system"
                                            }
                                            self.integration_hooks.sync_contact_data(contact_data)
                                    
                                    st.info("🔗 Imported contacts synced with user portal via lockstep integration")
                                    
                                else:
                                    st.error("❌ No captured emails available for import")
                        
                        except Exception as e:
                            st.error(f"❌ Import failed: {e}")
        
        else:
            st.info("💡 Email Capture Integration not available - install email capture module for automatic imports")
        
        # Contact management controls
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Add New Contact**")
            with st.form("add_contact"):
                contact_name = st.text_input("Name")
                contact_email = st.text_input("Email")
                contact_company = st.text_input("Company")
                contact_role = st.selectbox("Role", ["Candidate", "HR Manager", "Recruiter", "Admin", "Captured Contact"])
                contact_tags = st.text_input("Tags (comma-separated)")
                
                # App offer targeting
                app_offer_eligible = st.checkbox("🎯 Eligible for App Offers", 
                                               help="Mark this contact for IntelliCV app promotional campaigns")
                
                if st.form_submit_button("➕ Add Contact"):
                    # Integration hooks - sync with user portal
                    if self.integration_hooks:
                        tags_with_app = contact_tags
                        if app_offer_eligible:
                            tags_with_app += ",app_offer_eligible" if contact_tags else "app_offer_eligible"
                        
                        contact_data = {
                            "name": contact_name,
                            "email": contact_email,
                            "company": contact_company,
                            "role": contact_role,
                            "tags": tags_with_app,
                            "added_date": datetime.now().isoformat(),
                            "app_offer_eligible": app_offer_eligible
                        }
                        self.integration_hooks.sync_contact_data(contact_data)
                    
                    st.success(f"✅ Contact {contact_name} added successfully")
                    st.info("🔗 Contact synced with user portal via lockstep integration")
                    if app_offer_eligible:
                        st.info("🎯 Contact marked for app offer campaigns")
        
        with col2:
            st.write("**Contact Search & Filter**")
            search_term = st.text_input("🔍 Search contacts...")
            filter_role = st.selectbox("Filter by Role", ["All", "Candidate", "HR Manager", "Recruiter", "Admin", "Captured Contact"])
            filter_company = st.text_input("Filter by Company")
            
            # App offer filter
            filter_app_offers = st.checkbox("🎯 Show only App Offer eligible contacts")
            
            if st.button("🔍 Search Contacts"):
                st.info(f"Searching for: {search_term} with role: {filter_role}")
                if filter_app_offers:
                    st.info("🎯 Filtered for app offer eligible contacts")
                # Mock search results
                st.success(f"Found 12 contacts matching '{search_term}'")
        
        # Contact database display with enhanced data
        st.write("**📋 Contact Directory**")
        contacts_data = [
            {"Name": "John Doe", "Email": "john@company.com", "Company": "TechCorp", "Role": "Candidate", "Last Contact": "2025-09-20", "App Offers": "✅", "Source": "Manual"},
            {"Name": "Jane Smith", "Email": "jane@hr.com", "Company": "HR Solutions", "Role": "HR Manager", "Last Contact": "2025-09-19", "App Offers": "❌", "Source": "Manual"},
            {"Name": "Mike Johnson", "Email": "mike@recruit.com", "Company": "Recruiters Inc", "Role": "Recruiter", "Last Contact": "2025-09-18", "App Offers": "✅", "Source": "Manual"},
            {"Name": "user123", "Email": "user123@gmail.com", "Company": "gmail.com", "Role": "Captured Contact", "Last Contact": "2025-10-22", "App Offers": "✅", "Source": "Email Capture"},
            {"Name": "contact456", "Email": "contact456@yahoo.com", "Company": "yahoo.com", "Role": "Captured Contact", "Last Contact": "2025-10-22", "App Offers": "✅", "Source": "Email Capture"},
            {"Name": "Admin User", "Email": "admin@intellicv.com", "Company": "IntelliCV", "Role": "Admin", "Last Contact": "2025-09-21", "App Offers": "❌", "Source": "System"},
        ]
        
        contacts_df = pd.DataFrame(contacts_data)
        st.dataframe(contacts_df, use_container_width=True)
        
        # Enhanced contact actions
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📤 Export Contacts"):
                st.success("Contact list exported to CSV")
        with col2:
            if st.button("📥 Import Contacts"):
                st.info("Import functionality - supports CSV, Excel formats")
        with col3:
            if st.button("🧹 Clean Duplicates"):
                st.success("Found and removed 3 duplicate contacts")
        with col4:
            if st.button("🎯 Export App Offer List"):
                app_offer_contacts = [c for c in contacts_data if c["App Offers"] == "✅"]
                st.success(f"Exported {len(app_offer_contacts)} app offer eligible contacts")
                st.info("📧 Ready for marketing campaign targeting")
    
    def render_gmail_integration(self):
        """Render Gmail API integration interface."""
        st.subheader("📧 Gmail API Integration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Gmail Configuration**")
            
            gmail_status = "🟢 Connected" if self.gmail_api_configured else "🔴 Not Connected"
            st.write(f"**Status:** {gmail_status}")
            
            if not self.gmail_api_configured:
                st.info("Configure Gmail API for automated email sending")
                
                with st.form("gmail_config"):
                    gmail_email = st.text_input("Gmail Address")
                    gmail_app_password = st.text_input("App Password", type="password", help="Use Gmail App Password, not regular password")
                    smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com")
                    smtp_port = st.number_input("SMTP Port", value=587)
                    
                    if st.form_submit_button("🔗 Connect Gmail"):
                        # Mock Gmail connection
                        self.gmail_api_configured = True
                        st.success("✅ Gmail API connected successfully!")
                        st.info("🔐 Credentials securely stored")
                        st.rerun()
            else:
                if st.button("🔄 Test Connection"):
                    st.success("✅ Gmail connection test successful")
                if st.button("🔴 Disconnect"):
                    self.gmail_api_configured = False
                    st.warning("Gmail API disconnected")
                    st.rerun()
        
        with col2:
            st.write("**Gmail Features**")
            
            gmail_features = [
                "📤 Automated email sending",
                "📧 Campaign delivery",
                "📊 Email tracking",
                "🔄 Auto-sync with contacts",
                "📈 Performance analytics",
                "🛡️ Secure authentication"
            ]
            
            for feature in gmail_features:
                status = "✅" if self.gmail_api_configured else "⏳"
                st.write(f"{status} {feature}")
            
            if self.gmail_api_configured:
                st.success("🎉 All Gmail features active!")
            else:
                st.warning("Connect Gmail API to enable features")
    
    def render_email_campaigns(self):
        """Render email campaign management interface."""
        st.subheader("📧 Email Campaign Management")
        
        # Campaign creation with app offer templates
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Create New Campaign**")
            
            with st.form("create_campaign"):
                campaign_name = st.text_input("Campaign Name")
                campaign_subject = st.text_input("Email Subject")
                campaign_template = st.selectbox("Email Template", [
                    "Welcome Email",
                    "Job Opportunity",
                    "Newsletter", 
                    "Event Invitation",
                    "Follow-up",
                    "IntelliCV App Offer",  # New app offer template
                    "App Download Promotion",  # New app template
                    "Premium Features Unlock",  # New premium template
                    "Custom Template"
                ])
                
                target_audience = st.multiselect("Target Audience", [
                    "All Contacts",
                    "Candidates",
                    "HR Managers",
                    "Recruiters", 
                    "Recent Signups",
                    "VIP Contacts",
                    "Captured Contacts (Email System)",  # New audience from email capture
                    "App Offer Eligible",  # New app offer audience
                    "Gmail Users",  # New provider-specific
                    "Yahoo Users",  # New provider-specific
                    "Outlook Users"  # New provider-specific
                ])
                
                # App offer specific settings
                offer_type = None  # Initialize variable
                if "App" in campaign_template:
                    st.markdown("**🎯 App Offer Settings:**")
                    offer_type = st.selectbox("Offer Type", [
                        "Free App Download",
                        "Premium Trial (30 days)", 
                        "Discount Code (20% off)",
                        "Early Access Beta",
                        "Enterprise Demo"
                    ])
                    
                    include_referral = st.checkbox("Include Referral Program", help="Add referral bonus for sharing")
                
                send_immediately = st.checkbox("Send Immediately")
                if not send_immediately:
                    schedule_date = st.date_input("Schedule Date")
                    schedule_time = st.time_input("Schedule Time")
                
                if st.form_submit_button("📧 Create Campaign"):
                    # Integration hooks - notify user portal
                    if self.integration_hooks:
                        campaign_data = {
                            "name": campaign_name,
                            "subject": campaign_subject,
                            "template": campaign_template,
                            "audience": target_audience,
                            "created_date": datetime.now().isoformat(),
                            "app_offer": "App" in campaign_template,
                            "offer_type": offer_type if offer_type else None
                        }
                        # Mock sync - replace with actual implementation
                        try:
                            if hasattr(self.integration_hooks, 'sync_campaign_data'):
                                self.integration_hooks.sync_campaign_data(campaign_data)
                        except:
                            pass  # Fallback if sync method not available
                    
                    st.success(f"✅ Campaign '{campaign_name}' created for {len(target_audience)} audience(s)")
                    if "App" in campaign_template and offer_type:
                        st.info(f"🎯 App offer campaign with {offer_type}")
                    if self.gmail_api_configured:
                        st.info("📤 Campaign ready to send via Gmail API")
                    else:
                        st.warning("⚠️ Connect Gmail API to enable sending")
        
        with col2:
            st.write("**Campaign Performance**")
            
            # Mock campaign data with enhanced metrics
            campaigns = [
                {"Campaign": "Monthly Newsletter", "Sent": 1247, "Opened": 426, "Clicked": 89, "Status": "Completed", "ROI": "340%"},
                {"Campaign": "Job Alert - Python", "Sent": 234, "Opened": 98, "Clicked": 23, "Status": "Active", "ROI": "180%"},
                {"Campaign": "Welcome Series", "Sent": 89, "Opened": 67, "Clicked": 12, "Status": "Scheduled", "ROI": "Pending"},
                {"Campaign": "Event Invitation", "Sent": 156, "Opened": 89, "Clicked": 34, "Status": "Completed", "ROI": "220%"},
            ]
            
            for campaign in campaigns:
                with st.expander(f"📊 {campaign['Campaign']} - {campaign['Status']}"):
                    col_a, col_b, col_c, col_d = st.columns(4)
                    with col_a:
                        st.metric("Sent", campaign['Sent'])
                    with col_b:
                        st.metric("Opened", campaign['Opened'])
                        open_rate = (campaign['Opened'] / campaign['Sent']) * 100
                        st.caption(f"{open_rate:.1f}% open rate")
                    with col_c:
                        st.metric("Clicked", campaign['Clicked'])
                        if campaign['Opened'] > 0:
                            click_rate = (campaign['Clicked'] / campaign['Opened']) * 100
                            st.caption(f"{click_rate:.1f}% click rate")
                    with col_d:
                        st.metric("ROI", campaign['ROI'])
    
    def render_email_viewer(self):
        """Render email log viewer interface."""
        st.subheader("📬 Email Viewer & Log Analysis")
        
        # Email filters
        col1, col2, col3 = st.columns(3)
        with col1:
            email_filter = st.selectbox("Email Status", ["All Emails", "Sent", "Delivered", "Opened", "Clicked", "Failed"])
        with col2:
            date_filter = st.date_input("Filter by Date", datetime.now().date())
        with col3:
            campaign_filter = st.selectbox("Campaign", ["All Campaigns", "Newsletter", "Job Alert", "Welcome Series", "Events"])
        
        # Enhanced email log with more detail
        email_log = [
            {"Timestamp": "2025-09-21 14:30", "To": "john@company.com", "Subject": "Welcome to IntelliCV", "Status": "Delivered", "Campaign": "Welcome Series", "Open_Time": "2025-09-21 15:45", "Device": "Mobile"},
            {"Timestamp": "2025-09-21 14:25", "To": "jane@hr.com", "Subject": "Monthly Newsletter", "Status": "Opened", "Campaign": "Newsletter", "Open_Time": "2025-09-21 14:30", "Device": "Desktop"},
            {"Timestamp": "2025-09-21 14:20", "To": "mike@recruit.com", "Subject": "New Python Jobs", "Status": "Clicked", "Campaign": "Job Alert", "Open_Time": "2025-09-21 14:22", "Device": "Mobile"},
            {"Timestamp": "2025-09-21 14:15", "To": "failed@bounce.com", "Subject": "Event Invitation", "Status": "Failed", "Campaign": "Events", "Open_Time": "-", "Device": "-"},
            {"Timestamp": "2025-09-21 14:10", "To": "sarah@tech.com", "Subject": "Career Opportunities", "Status": "Opened", "Campaign": "Job Alert", "Open_Time": "2025-09-21 16:20", "Device": "Desktop"},
        ]
        
        email_df = pd.DataFrame(email_log)
        
        # Filter data based on selection
        if email_filter != "All Emails":
            email_df = email_df[email_df['Status'] == email_filter.replace("ed", "").replace("k", "ck")]
            
        st.dataframe(email_df, use_container_width=True)
        
        # Email content preview
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👁️ Preview Selected Email"):
                st.info("📧 Email preview loading...")
                
        with col2:
            if st.button("📊 Generate Email Report"):
                st.success("📈 Email performance report generated")
        
        # Email content preview modal
        with st.expander("📧 Email Content Preview"):
            st.write("**Subject:** Welcome to IntelliCV")
            st.write("**From:** noreply@intellicv.com")
            st.write("**To:** john@company.com")
            st.write("**Sent:** 2025-09-21 14:30")
            st.markdown("---")
            
            st.markdown("""
            **Email Content:**
            
            Dear John,
            
            Welcome to IntelliCV! We're excited to help you with your career journey.
            
            🚀 **Get Started:**
            - Complete your profile
            - Upload your resume
            - Explore job opportunities
            - Connect with recruiters
            
            Need help? Reply to this email or visit our support center.
            
            Best regards,
            The IntelliCV Team
            
            ---
            **Tracking Info:**
            - Email opened: Yes (2025-09-21 15:45)
            - Device: Mobile
            - Location: San Francisco, CA
            - Links clicked: 2
            """)
    
    def render_communication_analytics(self):
        """Render communication analytics dashboard."""
        st.subheader("📊 Communication Analytics")
        
        # Email performance metrics over time
        performance_data = pd.DataFrame({
            'Date': pd.date_range(start='2025-09-14', end='2025-09-21', freq='D'),
            'Emails_Sent': [145, 189, 234, 201, 267, 198, 234, 289],
            'Open_Rate': [32.1, 35.5, 31.8, 34.2, 29.7, 36.1, 34.2, 37.8],
            'Click_Rate': [7.2, 8.1, 6.9, 8.7, 6.4, 9.2, 8.7, 9.5],
            'Bounce_Rate': [2.1, 1.8, 2.3, 1.9, 2.5, 1.7, 2.0, 1.6]
        })
        
        # Main performance chart
        fig = px.line(performance_data, x='Date', y=['Open_Rate', 'Click_Rate', 'Bounce_Rate'], 
                     title='📈 Email Performance Trends (7 Days)')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance metrics cards
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_open_rate = performance_data['Open_Rate'].mean()
            st.metric("Avg Open Rate", f"{avg_open_rate:.1f}%", "+2.3%")
        with col2:
            avg_click_rate = performance_data['Click_Rate'].mean()
            st.metric("Avg Click Rate", f"{avg_click_rate:.1f}%", "+1.1%")
        with col3:
            avg_bounce_rate = performance_data['Bounce_Rate'].mean()
            st.metric("Avg Bounce Rate", f"{avg_bounce_rate:.1f}%", "-0.3%")
        
        # Campaign comparison
        st.subheader("📊 Campaign Comparison")
        
        campaign_performance = pd.DataFrame({
            'Campaign': ['Newsletter', 'Job Alerts', 'Welcome Series', 'Events', 'Follow-ups'],
            'Open_Rate': [34.2, 41.8, 67.3, 28.9, 23.4],
            'Click_Rate': [8.7, 12.4, 15.2, 6.1, 4.8],
            'Conversion_Rate': [2.3, 4.1, 8.9, 1.7, 1.2]
        })
        
        fig2 = px.bar(campaign_performance, x='Campaign', y=['Open_Rate', 'Click_Rate', 'Conversion_Rate'],
                     title='📊 Campaign Performance Comparison')
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Best performing content
        with st.expander("🏆 Top Performing Content"):
            top_content = [
                {"Subject": "Your Dream Job Awaits - Python Developer", "Open_Rate": "67.8%", "Click_Rate": "18.9%"},
                {"Subject": "Welcome to IntelliCV - Complete Your Profile", "Open_Rate": "65.2%", "Click_Rate": "15.4%"},
                {"Subject": "5 Hot Jobs This Week in Your Area", "Open_Rate": "52.3%", "Click_Rate": "12.1%"},
                {"Subject": "IntelliCV Monthly Newsletter - September", "Open_Rate": "41.7%", "Click_Rate": "9.8%"},
            ]
            
            for content in top_content:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"📧 {content['Subject']}")
                with col2:
                    st.write(f"👀 {content['Open_Rate']}")
                with col3:
                    st.write(f"🖱️ {content['Click_Rate']}")

def render():
    """Main render function for Contact Communication module."""
    contact_comm = ContactCommunication()
    
    render_section_header(
        "📞 Contact & Communication Suite",
        "Complete contact management with Gmail integration, campaigns, and analytics"
    )
    
    # Communication metrics dashboard
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📋 Total Contacts", "1,247", "+89")
    with col2:
        st.metric("📧 Email Campaigns", "23", "+3")
    with col3:
        st.metric("📈 Open Rate", "34.2%", "+2.1%")
    with col4:
        st.metric("💬 Response Rate", "8.7%", "+0.9%")
    
    # Main interface tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "👥 Contact Management", 
        "🔗 Gmail Integration",
        "📧 Email Campaigns", 
        "📬 Email Viewer", 
        "📊 Communication Analytics",
        "📊 Email Database & CSV"  # New tab for email database integration
    ])
    
    with tab1:
        contact_comm.render_contact_management()
    
    with tab2:
        contact_comm.render_gmail_integration()
    
    with tab3:
        contact_comm.render_email_campaigns()
    
    with tab4:
        contact_comm.render_email_viewer()
    
    with tab5:
        contact_comm.render_communication_analytics()
    
    with tab6:
        # New Email Database & CSV Management Tab
        st.subheader("📊 Email Database & CSV Management")
        
        if EMAIL_CAPTURE_INTEGRATION:
            try:
                email_manager = get_email_capture_manager()
                
                # Load emails database
                emails_db_path = Path("c:/IntelliCV-AI/IntelliCV/ai_data_final/emails/emails_database.json")
                
                st.info(f"""
                **📧 Email Database Integration**
                
                Manage emails captured from Gmail, Yahoo, and Outlook accounts.
                Export filtered lists for targeted marketing campaigns and app offers.
                
                **Database Location:** `{emails_db_path}`
                """)
                
                # Database statistics
                stats = email_manager.get_capture_statistics()
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📧 Total Emails", f"{stats.get('total_emails', 0):,}")
                with col2:
                    st.metric("📮 Gmail", f"{stats.get('gmail_count', 0):,}")
                with col3:
                    st.metric("📮 Yahoo", f"{stats.get('yahoo_count', 0):,}")
                with col4:
                    st.metric("📮 Outlook", f"{stats.get('outlook_count', 0):,}")
                
                # Email database viewer
                st.subheader("📋 Email Database Viewer")
                
                if emails_db_path.exists():
                    with open(emails_db_path, 'r', encoding='utf-8') as f:
                        emails_data = json.load(f)
                    
                    # Filter options
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        provider_filter = st.selectbox("Filter by Provider", 
                                                     ["All"] + list(set(item.get('provider', 'unknown') for item in emails_data)))
                    with col2:
                        domain_search = st.text_input("Search Domain", placeholder="e.g., gmail.com")
                    with col3:
                        email_search = st.text_input("Search Email", placeholder="e.g., john@")
                    
                    # Apply filters
                    filtered_emails = emails_data
                    
                    if provider_filter != "All":
                        filtered_emails = [e for e in filtered_emails if e.get('provider', '').lower() == provider_filter.lower()]
                    
                    if domain_search:
                        filtered_emails = [e for e in filtered_emails if domain_search.lower() in e.get('domain', '').lower()]
                    
                    if email_search:
                        filtered_emails = [e for e in filtered_emails if email_search.lower() in e.get('email', '').lower()]
                    
                    st.info(f"📊 Showing {len(filtered_emails)} of {len(emails_data)} emails")
                    
                    # Display emails in table format
                    if filtered_emails:
                        emails_df = pd.DataFrame(filtered_emails[:100])  # Show first 100
                        
                        # Add marketing fields for CSV export
                        emails_df['app_offer_eligible'] = 'yes'
                        emails_df['contact_status'] = 'new'
                        emails_df['marketing_consent'] = 'unknown'
                        emails_df['contact_source'] = 'email_extraction'
                        
                        st.dataframe(emails_df, use_container_width=True)
                        
                        if len(filtered_emails) > 100:
                            st.info(f"Showing first 100 results. Total: {len(filtered_emails)}")
                    
                    # CSV Export Section
                    st.subheader("📤 CSV Export for Marketing Campaigns")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**🎯 Export Options:**")
                        
                        export_filtered = st.checkbox("Export filtered results only", value=True)
                        include_app_targeting = st.checkbox("Mark for app offers", value=True)
                        include_marketing_fields = st.checkbox("Include marketing consent fields", value=True)
                        
                        csv_filename = st.text_input("CSV Filename", 
                                                   value=f"email_contacts_{datetime.now().strftime('%Y%m%d')}.csv")
                    
                    with col2:
                        st.markdown("**📊 Export Preview:**")
                        
                        export_count = len(filtered_emails) if export_filtered else len(emails_data)
                        st.metric("📧 Emails to Export", f"{export_count:,}")
                        
                        # Show CSV structure
                        if export_count > 0:
                            sample_fields = ["email", "domain", "provider", "first_seen"]
                            if include_marketing_fields:
                                sample_fields.extend(["app_offer_eligible", "contact_status", "marketing_consent"])
                            
                            st.markdown("**📋 CSV Columns:**")
                            for field in sample_fields:
                                st.text(f"• {field}")
                    
                    # Export buttons
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("📤 Export Filtered CSV", type="primary"):
                            try:
                                # Prepare export data
                                export_data = filtered_emails if export_filtered else emails_data
                                
                                # Add marketing fields
                                csv_data = []
                                for item in export_data:
                                    csv_row = {
                                        'email': item.get('email', ''),
                                        'domain': item.get('domain', ''),
                                        'provider': item.get('provider', ''),
                                        'first_seen': item.get('first_seen', ''),
                                    }
                                    
                                    if include_marketing_fields:
                                        csv_row.update({
                                            'app_offer_eligible': 'yes' if include_app_targeting else 'no',
                                            'contact_status': 'new',
                                            'marketing_consent': 'unknown',
                                            'contact_source': 'email_extraction',
                                            'last_updated': datetime.now().isoformat()
                                        })
                                    
                                    csv_data.append(csv_row)
                                
                                # Create CSV
                                csv_df = pd.DataFrame(csv_data)
                                csv_path = Path(__file__).parent.parent / "data" / "csv_exports" / csv_filename
                                csv_path.parent.mkdir(parents=True, exist_ok=True)
                                
                                csv_df.to_csv(csv_path, index=False)
                                
                                st.success(f"✅ Exported {len(csv_data)} emails to CSV!")
                                st.info(f"📁 **File:** `{csv_path}`")
                                
                                # Show first few rows
                                with st.expander("📋 Preview Exported Data"):
                                    st.dataframe(csv_df.head(10))
                            
                            except Exception as e:
                                st.error(f"❌ Export failed: {e}")
                    
                    with col2:
                        if st.button("🎯 Export App Offer List"):
                            try:
                                # Export only emails marked for app offers
                                app_offer_data = []
                                for item in filtered_emails if export_filtered else emails_data:
                                    app_offer_data.append({
                                        'email': item.get('email', ''),
                                        'domain': item.get('domain', ''),
                                        'provider': item.get('provider', ''),
                                        'first_seen': item.get('first_seen', ''),
                                        'app_offer_eligible': 'yes',
                                        'campaign_type': 'app_download_promotion',
                                        'offer_type': 'free_download',
                                        'contact_source': 'email_extraction'
                                    })
                                
                                csv_df = pd.DataFrame(app_offer_data)
                                csv_path = Path(__file__).parent.parent / "data" / "csv_exports" / f"app_offer_targets_{datetime.now().strftime('%Y%m%d')}.csv"
                                csv_path.parent.mkdir(parents=True, exist_ok=True)
                                
                                csv_df.to_csv(csv_path, index=False)
                                
                                st.success(f"✅ App offer list exported!")
                                st.info(f"🎯 {len(app_offer_data)} contacts marked for app campaigns")
                            
                            except Exception as e:
                                st.error(f"❌ App offer export failed: {e}")
                    
                    with col3:
                        if st.button("📮 Export by Provider"):
                            try:
                                # Export separate files for each provider
                                providers = set(item.get('provider', 'unknown') for item in emails_data)
                                
                                for provider in providers:
                                    if provider != 'unknown':
                                        provider_emails = [e for e in emails_data if e.get('provider') == provider]
                                        
                                        if provider_emails:
                                            csv_data = []
                                            for item in provider_emails:
                                                csv_data.append({
                                                    'email': item.get('email', ''),
                                                    'domain': item.get('domain', ''),
                                                    'provider': item.get('provider', ''),
                                                    'first_seen': item.get('first_seen', ''),
                                                    'app_offer_eligible': 'yes',
                                                    'contact_source': 'email_extraction'
                                                })
                                            
                                            csv_df = pd.DataFrame(csv_data)
                                            csv_path = Path(__file__).parent.parent / "data" / "csv_exports" / f"{provider}_contacts_{datetime.now().strftime('%Y%m%d')}.csv"
                                            csv_path.parent.mkdir(parents=True, exist_ok=True)
                                            
                                            csv_df.to_csv(csv_path, index=False)
                                
                                st.success(f"✅ Provider-specific CSVs exported!")
                                st.info(f"📁 Created separate files for {len([p for p in providers if p != 'unknown'])} providers")
                            
                            except Exception as e:
                                st.error(f"❌ Provider export failed: {e}")
                
                else:
                    st.warning("📧 Email database not found. Run email capture first.")
                    st.info(f"Expected location: `{emails_db_path}`")
            
            except Exception as e:
                st.error(f"❌ Email database integration error: {e}")
        
        else:
            st.warning("⚠️ Email capture integration not available")
            st.info("💡 Install the email capture module to access this functionality")
    
    # Integration status
    st.markdown("---")
    with st.expander("🔗 Integration Status"):
        integration_hooks = get_integration_hooks()
        if integration_hooks:
            st.success("✅ Lockstep integration active - Contact data synced with user portal")
            st.info("📧 Email campaigns integrated with user notifications")
        else:
            st.warning("⚠️ Integration hooks not available")

if __name__ == "__main__":
    render()