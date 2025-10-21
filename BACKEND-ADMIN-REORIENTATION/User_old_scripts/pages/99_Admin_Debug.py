"""
🔧 Admin Debug Page for User Portal
Shows users from SANDBOX admin portal to verify lockstep sync
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Authentication check
def check_authentication():
    """Simple authentication check"""
    return st.session_state.get('user_authenticated', False)

# Add auth directory to path
current_dir = Path(__file__).parent.parent
auth_dir = current_dir / "auth"
sys.path.insert(0, str(auth_dir))

try:
    from secure_auth import UserAuthenticator
    SECURE_AUTH_AVAILABLE = True
except ImportError:
    SECURE_AUTH_AVAILABLE = False
    st.error("❌ Enhanced authentication system not available")

# Page configuration
st.set_page_config(
    page_title="Admin Debug - User Sync",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 Admin Debug - SANDBOX User Sync")

if not SECURE_AUTH_AVAILABLE:
    st.error("❌ Cannot load authentication system")
    st.stop()

# Initialize authenticator
if "user_authenticator" not in st.session_state:
    st.session_state.user_authenticator = UserAuthenticator()

auth = st.session_state.user_authenticator

# Show lockstep sync status
st.markdown("### 🔄 Lockstep Synchronization Status")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📁 SANDBOX Admin Portal Users")
    admin_users = auth._load_admin_portal_users()
    
    if admin_users:
        st.success(f"✅ Found {len(admin_users)} users in admin portal")
        
        for email, user_data in admin_users.items():
            with st.expander(f"👤 {user_data.get('first_name', '')} {user_data.get('last_name', '')}"):
                st.write(f"**Email:** {email}")
                st.write(f"**Status:** {user_data.get('status', 'unknown')}")
                st.write(f"**Registration:** {user_data.get('registration_date', 'unknown')}")
                st.write(f"**Email Confirmed:** {user_data.get('email_confirmed', False)}")
                st.write(f"**Newsletter:** {user_data.get('newsletter_opt_in', False)}")
                
                # Show raw data
                if st.checkbox(f"Show raw data for {email}", key=f"raw_{email}"):
                    st.json(user_data)
    else:
        st.warning("⚠️ No users found in admin portal")

with col2:
    st.markdown("#### 👥 All Users (Combined View)")
    all_users = auth.list_all_users()
    
    if all_users:
        st.success(f"✅ Total accessible users: {len(all_users)}")
        
        # Count by source
        admin_count = sum(1 for u in all_users.values() if u.get('source') == 'admin_portal')
        local_count = sum(1 for u in all_users.values() if u.get('source') == 'local')
        
        st.metric("Admin Portal Users", admin_count)
        st.metric("Local Users", local_count)
        
        # Show users table
        users_data = []
        for email, user_data in all_users.items():
            users_data.append({
                "Name": user_data.get('full_name', 'Unknown'),
                "Email": email,
                "Source": user_data.get('source', 'unknown'),
                "Status": user_data.get('account_status', 'unknown'),
                "Email Verified": user_data.get('email_verified', False)
            })
        
        st.dataframe(users_data, use_container_width=True)
    else:
        st.warning("⚠️ No users found")

# Test authentication with Jan Johnston
st.markdown("---")
st.markdown("### 🧪 Test Authentication")

with st.form("test_auth"):
    st.write("**Test Jan Johnston Login:**")
    test_email = st.text_input("Email", value="Janatmainswood@gmail.com")
    test_password = st.text_input("Password", type="password", help="Enter the password used in registration")
    
    if st.form_submit_button("🔍 Test Login"):
        if test_password:
            # Note: We can't actually test without the real password
            # But we can check if the user exists
            user_info = auth.get_user_info(test_email)
            if user_info:
                st.success("✅ User found in system!")
                st.write(f"**Name:** {user_info.get('full_name')}")
                st.write(f"**Account Status:** {user_info.get('account_status')}")
                st.write(f"**Email Verified:** {user_info.get('email_verified')}")
                st.info("💡 Password verification would work if correct password is provided")
            else:
                st.error("❌ User not found")
        else:
            st.warning("⚠️ Please enter a password to test")

# Live monitoring
st.markdown("---")
st.markdown("### 📊 Live Monitoring")

if st.button("🔄 Refresh Data"):
    st.rerun()

st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Path information
st.markdown("---")
st.markdown("### 📁 System Paths")
st.code(f"""
Admin Portal Data: C:/IntelliCV/SANDBOX/admin_portal/data/user_registrations
User Portal Data: {Path.cwd()}/user_credentials.json
Current Working Directory: {Path.cwd()}
""")

# Show sync health
sync_healthy = len(admin_users) > 0
st.markdown("### 🏥 Sync Health")
if sync_healthy:
    st.success("🟢 Lockstep synchronization is healthy")
    st.balloons()
else:
    st.error("🔴 Lockstep synchronization has issues")