"""
=============================================================================
IntelliCV Admin Portal - Multi-Provider Email Capture
=============================================================================

Comprehensive email capture system for extracting unique emails from:
- Gmail (existing app password)
- Yahoo (existing app password)  
- Outlook (new app password to be configured)

Exports to CSV for Contact Communications integration and marketing campaigns.
"""

import streamlit as st
import sys
import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent))

# Import the email capture system
try:
    from modules.email_capture_system import MultiProviderEmailCapture, get_email_capture_manager
    EMAIL_CAPTURE_AVAILABLE = True
except ImportError as e:
    EMAIL_CAPTURE_AVAILABLE = False

# Authentication check
if not st.session_state.get('admin_authenticated', False):
    st.error("🚫 **AUTHENTICATION REQUIRED**")
    st.info("Please return to the main page and login to access this module.")
    st.stop()

st.set_page_config(
    page_title="📧 Email Capture - IntelliCV",
    page_icon="📧",
    layout="wide"
)

def main():
    """Main function for email capture interface"""
    
    # Page header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem; text-align: center;'>
        <h1>📧 Multi-Provider Email Capture System</h1>
        <h3>Extract unique emails from Gmail, Yahoo & Outlook for Contact Communications</h3>
        <p>Capture email addresses for marketing campaigns and app offers</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not EMAIL_CAPTURE_AVAILABLE:
        st.error("❌ Email capture system not available")
        st.info("💡 The email capture module needs to be installed")
        return
    
    # Initialize email capture manager
    try:
        email_manager = get_email_capture_manager()
        st.success("✅ Email capture system initialized successfully!")
    except Exception as e:
        st.error(f"❌ Failed to initialize email capture system: {e}")
        return
    
    # Get current statistics
    try:
        stats = email_manager.get_capture_statistics()
        
        # Display current statistics
        st.subheader("📊 Current Email Database Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📧 Total Emails", f"{stats.get('total_emails', 0):,}")
        with col2:
            st.metric("📮 Gmail", f"{stats.get('gmail_count', 0):,}")
        with col3:
            st.metric("📮 Yahoo", f"{stats.get('yahoo_count', 0):,}")
        with col4:
            st.metric("📮 Outlook", f"{stats.get('outlook_count', 0):,}")
        
        # Provider breakdown
        if 'provider_breakdown' in stats:
            st.subheader("📈 Provider Distribution")
            provider_df = pd.DataFrame(list(stats['provider_breakdown'].items()), 
                                     columns=['Provider', 'Count'])
            st.bar_chart(provider_df.set_index('Provider'))
    
    except Exception as e:
        st.warning(f"⚠️ Could not load statistics: {e}")
        stats = {}
    
    # Main interface tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⚙️ Account Setup", 
        "🔍 Email Capture", 
        "📊 Results & Stats",
        "📤 CSV Export", 
        "🔗 Contact Integration"
    ])
    
    # Tab 1: Account Setup
    with tab1:
        st.subheader("⚙️ Multi-Provider Account Configuration")
        
        st.info("""
        **📧 Configure your email accounts for capturing unique email addresses**
        
        **Required: App Passwords (NOT regular passwords)**
        - Gmail: Use existing app password
        - Yahoo: Use existing app password  
        - Outlook: Generate new app password
        """)
        
        # Account configuration forms
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📮 Configured Accounts")
            
            # Initialize session state for accounts
            if 'email_accounts' not in st.session_state:
                st.session_state.email_accounts = []
            
            if st.session_state.email_accounts:
                for i, account in enumerate(st.session_state.email_accounts):
                    with st.expander(f"📧 {account['provider'].title()} - {account['email_address']}"):
                        st.write(f"**Provider:** {account['provider'].title()}")
                        st.write(f"**Email:** {account['email_address']}")
                        st.write(f"**Status:** {'✅ Ready' if account.get('password') else '❌ No Password'}")
                        
                        if st.button(f"🗑️ Remove", key=f"remove_{i}"):
                            st.session_state.email_accounts.pop(i)
                            st.rerun()
            else:
                st.info("📭 No accounts configured yet")
        
        with col2:
            st.markdown("### ➕ Add Email Account")
            
            with st.form("add_email_account"):
                provider = st.selectbox("📧 Provider", ["gmail", "yahoo", "outlook"])
                email_address = st.text_input("Email Address", placeholder="your.email@example.com")
                app_password = st.text_input("App Password", type="password", 
                                           placeholder="Your app-specific password")
                
                # Provider-specific help
                if provider == "gmail":
                    st.info("🔵 Gmail: Use existing app password (2FA required)")
                elif provider == "yahoo":
                    st.info("🟡 Yahoo: Use existing app password (2FA required)")
                elif provider == "outlook":
                    st.warning("🔴 Outlook: Generate NEW app password for this system")
                
                test_connection = st.checkbox("🔍 Test connection before saving")
                
                if st.form_submit_button("➕ Add Account"):
                    if email_address and app_password:
                        # Validate email domain matches provider
                        domain = email_address.split('@')[1].lower()
                        valid_domains = {
                            'gmail': ['gmail.com', 'googlemail.com'],
                            'yahoo': ['yahoo.com', 'yahoo.co.uk', 'yahoo.fr', 'yahoo.ca'],
                            'outlook': ['outlook.com', 'hotmail.com', 'live.com', 'msn.com']
                        }
                        
                        if domain not in valid_domains.get(provider, []):
                            st.error(f"❌ Email domain '{domain}' doesn't match provider '{provider}'")
                        else:
                            account_config = {
                                'provider': provider,
                                'email_address': email_address,
                                'app_password': app_password,
                                'added_date': datetime.now().isoformat()
                            }
                            
                            if test_connection:
                                # Test connection
                                with st.spinner(f"🔗 Testing {provider} connection..."):
                                    try:
                                        test_mail = email_manager.connect_to_email_provider(
                                            provider, email_address, app_password
                                        )
                                        if test_mail:
                                            test_mail.close()
                                            test_mail.logout()
                                            st.success("✅ Connection test successful!")
                                            st.session_state.email_accounts.append(account_config)
                                            st.rerun()
                                        else:
                                            st.error("❌ Connection test failed")
                                    except Exception as e:
                                        st.error(f"❌ Connection error: {e}")
                            else:
                                st.session_state.email_accounts.append(account_config)
                                st.success(f"✅ {provider.title()} account added successfully!")
                                st.rerun()
                    else:
                        st.error("❌ Please fill in all fields")
    
    # Tab 2: Email Capture
    with tab2:
        st.subheader("🔍 Multi-Provider Email Capture")
        
        if not st.session_state.get('email_accounts', []):
            st.warning("⚠️ Please configure email accounts first in the 'Account Setup' tab")
        else:
            st.success(f"✅ {len(st.session_state.email_accounts)} email account(s) configured")
            
            # Capture configuration
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### ⚙️ Capture Settings")
                
                days_back = st.slider(
                    "📅 Days to scan back",
                    min_value=7,
                    max_value=3650,  # 10 years
                    value=365,
                    help="How far back to scan for emails"
                )
                
                max_emails_per_provider = st.slider(
                    "📧 Max emails per provider",
                    min_value=100,
                    max_value=5000,
                    value=1000,
                    help="Maximum emails to process per account"
                )
                
                # Provider selection
                available_providers = [acc['provider'] for acc in st.session_state.email_accounts]
                selected_providers = st.multiselect(
                    "📮 Select providers to capture from",
                    available_providers,
                    default=available_providers
                )
            
            with col2:
                st.markdown("### 📊 Capture Preview")
                
                total_accounts = len([acc for acc in st.session_state.email_accounts 
                                    if acc['provider'] in selected_providers])
                estimated_emails = total_accounts * max_emails_per_provider
                
                st.metric("📧 Accounts to scan", total_accounts)
                st.metric("📅 Time period", f"{days_back} days")
                st.metric("📊 Est. emails to process", f"{estimated_emails:,}")
                
                # Processing time estimate
                est_minutes = (estimated_emails / 100) * 2  # Rough estimate
                st.info(f"⏱️ Estimated time: {est_minutes:.0f} minutes")
            
            # Start capture button
            if st.button("🚀 Start Multi-Provider Email Capture", type="primary", use_container_width=True):
                if not selected_providers:
                    st.error("❌ Please select at least one provider")
                else:
                    # Prepare account configurations
                    capture_configs = [
                        acc for acc in st.session_state.email_accounts 
                        if acc['provider'] in selected_providers
                    ]
                    
                    st.info(f"🔍 Starting capture from {len(capture_configs)} accounts...")
                    
                    # Progress tracking
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        # Run the capture
                        with st.spinner("📧 Capturing emails from all providers..."):
                            results = email_manager.run_multi_provider_capture(
                                capture_configs, days_back, max_emails_per_provider
                            )
                        
                        progress_bar.progress(100)
                        
                        # Display results
                        if results.get('total_emails_found', 0) > 0:
                            st.success("🎉 Email capture completed successfully!")
                            
                            # Results metrics
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("📧 Total Emails Found", f"{results['total_emails_found']:,}")
                            with col2:
                                st.metric("✨ New Emails Added", f"{results.get('new_emails_added', 0):,}")
                            with col3:
                                st.metric("⏱️ Processing Time", results.get('processing_time', 'Unknown'))
                            
                            # Provider breakdown
                            if results.get('providers_processed'):
                                st.subheader("📊 Provider Results")
                                for provider_result in results['providers_processed']:
                                    st.write(f"📮 **{provider_result['provider'].title()}**: {provider_result['emails_found']:,} emails found")
                            
                            # Store results in session state
                            st.session_state['last_capture_results'] = results
                            
                        else:
                            st.info("ℹ️ No new emails found or capture failed")
                            if results.get('errors'):
                                for error in results['errors']:
                                    st.error(f"❌ Error: {error}")
                    
                    except Exception as e:
                        st.error(f"❌ Capture failed: {e}")
                        progress_bar.progress(0)
    
    # Tab 3: Results & Stats
    with tab3:
        st.subheader("📊 Capture Results & Statistics")
        
        # Refresh statistics
        if st.button("🔄 Refresh Statistics"):
            st.rerun()
        
        try:
            current_stats = email_manager.get_capture_statistics()
            
            # Overview metrics
            st.markdown("### 📈 Database Overview")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📧 Total Unique Emails", f"{current_stats.get('total_emails', 0):,}")
            with col2:
                st.metric("🌐 Unique Domains", len(current_stats.get('top_domains', {})))
            with col3:
                gmail_pct = (current_stats.get('gmail_count', 0) / max(current_stats.get('total_emails', 1), 1)) * 100
                st.metric("📮 Gmail %", f"{gmail_pct:.1f}%")
            with col4:
                other_pct = (current_stats.get('other_count', 0) / max(current_stats.get('total_emails', 1), 1)) * 100
                st.metric("🏢 Business Emails %", f"{other_pct:.1f}%")
            
            # Provider breakdown chart
            if current_stats.get('provider_breakdown'):
                st.markdown("### 📊 Email Distribution by Provider")
                provider_df = pd.DataFrame(
                    list(current_stats['provider_breakdown'].items()),
                    columns=['Provider', 'Count']
                )
                st.bar_chart(provider_df.set_index('Provider'))
            
            # Top domains
            if current_stats.get('top_domains'):
                st.markdown("### 🏆 Top Email Domains")
                domains_df = pd.DataFrame(
                    list(current_stats['top_domains'].items()),
                    columns=['Domain', 'Count']
                )
                st.dataframe(domains_df, use_container_width=True)
            
            # Last capture results
            if 'last_capture_results' in st.session_state:
                st.markdown("### 📋 Last Capture Session")
                results = st.session_state['last_capture_results']
                
                with st.expander("📊 View Last Capture Details"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Providers Processed:** {len(results.get('providers_processed', []))}")
                        st.write(f"**Total Emails Found:** {results.get('total_emails_found', 0):,}")
                        st.write(f"**New Emails Added:** {results.get('new_emails_added', 0):,}")
                    
                    with col2:
                        st.write(f"**Processing Time:** {results.get('processing_time', 'Unknown')}")
                        st.write(f"**Duplicates Filtered:** {results.get('duplicates_filtered', 0):,}")
                        st.write(f"**Total in Database:** {results.get('total_in_database', 0):,}")
        
        except Exception as e:
            st.error(f"❌ Error loading statistics: {e}")
    
    # Tab 4: CSV Export
    with tab4:
        st.subheader("📤 CSV Export for Contact Communications")
        
        st.info("""
        **📊 Export captured emails in CSV format for Contact Communications**
        
        CSV includes marketing fields for:
        - App offer targeting
        - Marketing consent tracking
        - Contact status management
        """)
        
        # Export options
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ⚙️ Export Settings")
            
            export_provider = st.selectbox(
                "📮 Filter by Provider",
                ["all", "gmail", "yahoo", "outlook", "other"],
                help="Filter emails by provider"
            )
            
            domain_filter = st.text_input(
                "🌐 Domain Filter (optional)",
                placeholder="e.g., gmail.com",
                help="Filter by specific domain"
            )
            
            include_app_targeting = st.checkbox(
                "🎯 Mark for App Offer Targeting",
                value=True,
                help="Mark emails as eligible for app offers"
            )
            
            include_metadata = st.checkbox(
                "📋 Include Metadata Fields",
                value=True,
                help="Include fields for marketing consent, contact status, etc."
            )
        
        with col2:
            st.markdown("### 📊 Export Preview")
            
            try:
                stats = email_manager.get_capture_statistics()
                
                # Calculate export count
                if export_provider == "all":
                    export_count = stats.get('total_emails', 0)
                else:
                    export_count = stats.get(f'{export_provider}_count', 0)
                
                st.metric("📧 Emails to Export", f"{export_count:,}")
                
                # Show sample CSV structure
                sample_data = {
                    'email': 'john.doe@gmail.com',
                    'domain': 'gmail.com',
                    'provider': 'gmail',
                    'first_seen': '2025-10-22T10:30:00',
                    'contact_status': 'new',
                    'marketing_consent': 'unknown',
                    'app_offer_eligible': 'yes' if include_app_targeting else 'no',
                    'contact_source': 'email_extraction'
                }
                
                st.markdown("**📋 CSV Structure Preview:**")
                for key, value in sample_data.items():
                    st.text(f"{key}: {value}")
            
            except Exception as e:
                st.warning(f"⚠️ Could not load export preview: {e}")
        
        # Export button
        if st.button("📤 Export to CSV", type="primary", use_container_width=True):
            try:
                with st.spinner("📊 Generating CSV export..."):
                    # Perform export
                    provider_filter = None if export_provider == "all" else export_provider
                    csv_path = email_manager.export_emails_to_csv(
                        provider_filter=provider_filter,
                        domain_filter=domain_filter if domain_filter else None,
                        include_app_targeting=include_app_targeting
                    )
                
                if csv_path:
                    st.success(f"✅ CSV exported successfully!")
                    st.info(f"📁 **Export Location:** `{csv_path}`")
                    
                    # Show download instructions
                    st.markdown("""
                    **📋 Next Steps:**
                    1. Copy the CSV file to your Contact Communications directory
                    2. Import the CSV in the Contact Communications page (Page 14)
                    3. Use for marketing campaigns and app offers
                    """)
                    
                    # Show file info
                    csv_file = Path(csv_path)
                    if csv_file.exists():
                        file_size = csv_file.stat().st_size / 1024  # KB
                        st.caption(f"📊 File size: {file_size:.1f} KB")
                
                else:
                    st.error("❌ Export failed - no data to export")
            
            except Exception as e:
                st.error(f"❌ Export error: {e}")
    
    # Tab 5: Contact Integration
    with tab5:
        st.subheader("🔗 Contact Communications Integration")
        
        st.info("""
        **📞 Integration with Contact Communications Page (Page 14)**
        
        This system integrates with the Contact Communications module to provide:
        - Automated contact imports from captured emails
        - Marketing campaign targeting
        - App offer distribution lists
        """)
        
        # Integration status
        st.markdown("### 📊 Integration Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📧 Email Database**")
            try:
                stats = email_manager.get_capture_statistics()
                st.success(f"✅ {stats.get('total_emails', 0):,} emails ready for import")
                st.info(f"📮 Gmail: {stats.get('gmail_count', 0):,}")
                st.info(f"📮 Yahoo: {stats.get('yahoo_count', 0):,}")
                st.info(f"📮 Outlook: {stats.get('outlook_count', 0):,}")
            except:
                st.error("❌ Could not load email database")
        
        with col2:
            st.markdown("**🔗 Contact Communications**")
            # Check if Contact Communications page exists
            contact_comm_path = Path(__file__).parent / "14_Contact_Communication.py"
            if contact_comm_path.exists():
                st.success("✅ Contact Communications page available")
                st.info("🔗 Ready for CSV import integration")
            else:
                st.warning("⚠️ Contact Communications page not found")
        
        # Quick export for Contact Communications
        st.markdown("### 🚀 Quick Export for Contact Communications")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📮 Export Gmail Contacts", use_container_width=True):
                try:
                    csv_path = email_manager.export_emails_to_csv(provider_filter="gmail")
                    if csv_path:
                        st.success("✅ Gmail contacts exported!")
                        st.caption(f"File: {Path(csv_path).name}")
                except Exception as e:
                    st.error(f"❌ Export failed: {e}")
        
        with col2:
            if st.button("📮 Export Yahoo Contacts", use_container_width=True):
                try:
                    csv_path = email_manager.export_emails_to_csv(provider_filter="yahoo")
                    if csv_path:
                        st.success("✅ Yahoo contacts exported!")
                        st.caption(f"File: {Path(csv_path).name}")
                except Exception as e:
                    st.error(f"❌ Export failed: {e}")
        
        with col3:
            if st.button("📮 Export Outlook Contacts", use_container_width=True):
                try:
                    csv_path = email_manager.export_emails_to_csv(provider_filter="outlook")
                    if csv_path:
                        st.success("✅ Outlook contacts exported!")
                        st.caption(f"File: {Path(csv_path).name}")
                except Exception as e:
                    st.error(f"❌ Export failed: {e}")
        
        # App offer targeting
        st.markdown("### 🎯 App Offer Targeting")
        
        st.info("""
        **📱 Target captured emails for app offers:**
        - Mark emails as eligible for IntelliCV app promotion
        - Filter by provider for targeted campaigns
        - Include GDPR-compliant consent tracking
        """)
        
        if st.button("🎯 Export App Offer Target List", type="primary"):
            try:
                csv_path = email_manager.export_emails_to_csv(
                    provider_filter=None,  # All providers
                    include_app_targeting=True
                )
                if csv_path:
                    st.success("✅ App offer target list exported!")
                    st.info("📧 All captured emails marked for app offer eligibility")
                    st.caption(f"📁 File: {Path(csv_path).name}")
            except Exception as e:
                st.error(f"❌ Export failed: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **💡 Usage Tips:**
    - Use **app passwords** for all providers (never regular passwords)
    - Larger scan periods will take more time but capture more emails
    - Export regularly to avoid losing captured data
    - Use provider filters for targeted marketing campaigns
    
    **🔐 Security:** All credentials are stored temporarily and not persisted between sessions.
    **📧 Integration:** Exported CSVs are compatible with Contact Communications page.
    """)

if __name__ == "__main__":
    main()