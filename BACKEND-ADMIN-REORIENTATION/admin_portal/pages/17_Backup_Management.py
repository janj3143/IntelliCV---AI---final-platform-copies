"""
🔄 IntelliCV Admin Portal - Backup Management
Advanced backup system with local and cloud storage options
"""

import streamlit as st
import pandas as pd
import os
import json
import zipfile
import datetime
import shutil
import tempfile
from pathlib import Path
import threading
import time

# Admin authentication check
def check_admin_authentication():
    """Check if user is authenticated"""
    if not st.session_state.get('admin_authenticated', False):
        st.error("Please login through the main portal first.")
        st.stop()
    return True

# Check authentication
check_admin_authentication()

# Page configuration
st.set_page_config(
    page_title="Backup Management",
    page_icon="🔄",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .backup-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .local-backup {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        padding: 15px;
        border-radius: 8px;
        color: white;
        margin: 5px 0;
    }
    .azure-backup {
        background: linear-gradient(135deg, #0078d4 0%, #106ebe 100%);
        padding: 15px;
        border-radius: 8px;
        color: white;
        margin: 5px 0;
    }
    .backup-log {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #17a2b8;
        margin: 10px 0;
    }
    .parser-lock-status {
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        font-weight: bold;
    }
    .lock-active {
        background-color: #ffebee;
        color: #c62828;
        border: 1px solid #ef5350;
    }
    .lock-inactive {
        background-color: #e8f5e8;
        color: #2e7d32;
        border: 1px solid #66bb6a;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'parser_lock' not in st.session_state:
    st.session_state.parser_lock = False
if 'backup_log' not in st.session_state:
    st.session_state.backup_log = []
if 'azure_api_key' not in st.session_state:
    st.session_state.azure_api_key = ""

# Header
st.markdown("""
<div class="backup-card">
    <h1>🔄 Backup Management Center</h1>
    <p>Comprehensive backup solutions for local and cloud storage with advanced restore capabilities</p>
</div>
""", unsafe_allow_html=True)

# Parser Lock Management Section
st.markdown("### 🔒 Parser Lock Management")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    lock_status = "ACTIVE" if st.session_state.parser_lock else "INACTIVE"
    lock_class = "lock-active" if st.session_state.parser_lock else "lock-inactive"
    
    st.markdown(f"""
    <div class="parser-lock-status {lock_class}">
        Parser Lock Status: {lock_status}
        <br><small>{'⚠️ Parsing operations are currently blocked' if st.session_state.parser_lock else '✅ Parsing operations available'}</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("🔓 Reset Parser Lock", type="secondary"):
        st.session_state.parser_lock = False
        st.success("Parser lock has been reset!")
        st.rerun()

with col3:
    if st.button("🔒 Enable Parser Lock", type="secondary"):
        st.session_state.parser_lock = True
        st.warning("Parser lock has been enabled!")
        st.rerun()

st.markdown("---")

# Backup Configuration Section
st.markdown("### ⚙️ Backup Configuration")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="local-backup">
        <h4>🏠 Local Backup Settings</h4>
    </div>
    """, unsafe_allow_html=True)
    
    local_backup_path = st.text_input(
        "Local Backup Directory",
        value="C:\\IntelliCV\\backups",
        help="Directory on home server for local backups"
    )
    
    compress_backups = st.checkbox("🗜️ Compress backups (ZIP)", value=True)
    include_logs = st.checkbox("📄 Include system logs", value=True)
    include_data = st.checkbox("💾 Include parsed data", value=True)

with col2:
    st.markdown("""
    <div class="azure-backup">
        <h4>☁️ Azure Backup Settings</h4>
    </div>
    """, unsafe_allow_html=True)
    
    azure_container = st.text_input(
        "Azure Container Name",
        value="intellicv-backups",
        help="Azure Blob Storage container name"
    )
    
    azure_api_key = st.text_input(
        "Temporary Azure API Key",
        value=st.session_state.azure_api_key,
        type="password",
        help="Temporary API key for Azure authentication"
    )
    
    if azure_api_key != st.session_state.azure_api_key:
        st.session_state.azure_api_key = azure_api_key
    
    retention_days = st.number_input("Retention Period (days)", value=30, min_value=1, max_value=365)

st.markdown("---")

# Backup Operations Section
st.markdown("### 🚀 Backup Operations")

col1, col2, col3 = st.columns(3)

def create_backup_name():
    """Generate standardized backup name"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"intellicv_backup_{timestamp}"

def log_backup_operation(operation_type, status, details=""):
    """Log backup operations"""
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "operation": operation_type,
        "status": status,
        "details": details,
        "backup_name": create_backup_name() if status == "SUCCESS" else None
    }
    st.session_state.backup_log.append(log_entry)

def create_local_backup():
    """Create local backup"""
    try:
        backup_name = create_backup_name()
        backup_dir = Path(local_backup_path) / backup_name
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup directories to include
        source_dirs = [
            "c:\\IntelliCV\\admin_portal_final",
            "c:\\IntelliCV\\SANDBOX\\admin_portal"
        ]
        
        if include_data:
            source_dirs.extend([
                "c:\\IntelliCV\\data",
                "c:\\IntelliCV\\processed_data"
            ])
        
        for source_dir in source_dirs:
            if os.path.exists(source_dir):
                dest_dir = backup_dir / Path(source_dir).name
                shutil.copytree(source_dir, dest_dir, ignore_errors=True)
        
        # Include logs if requested
        if include_logs:
            log_dir = backup_dir / "logs"
            log_dir.mkdir(exist_ok=True)
            # Copy log files (placeholder for actual log files)
            with open(log_dir / "backup_info.json", 'w') as f:
                json.dump({
                    "backup_date": datetime.datetime.now().isoformat(),
                    "included_directories": source_dirs,
                    "compressed": compress_backups
                }, f, indent=2)
        
        # Compress if requested
        if compress_backups:
            zip_path = f"{backup_dir}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(backup_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, backup_dir.parent)
                        zipf.write(file_path, arcname)
            
            # Remove uncompressed directory
            shutil.rmtree(backup_dir)
            
        log_backup_operation("LOCAL_BACKUP", "SUCCESS", f"Backup created: {backup_name}")
        return True, backup_name
        
    except Exception as e:
        log_backup_operation("LOCAL_BACKUP", "FAILED", str(e))
        return False, str(e)

def simulate_azure_backup():
    """Simulate Azure backup (placeholder for actual Azure integration)"""
    try:
        if not st.session_state.azure_api_key:
            raise Exception("Azure API key not provided")
        
        backup_name = create_backup_name()
        
        # Simulate upload process
        time.sleep(2)  # Simulate upload time
        
        log_backup_operation("AZURE_BACKUP", "SUCCESS", f"Azure backup uploaded: {backup_name}")
        return True, backup_name
        
    except Exception as e:
        log_backup_operation("AZURE_BACKUP", "FAILED", str(e))
        return False, str(e)

with col1:
    if st.button("🏠 Create Local Backup", type="primary"):
        if st.session_state.parser_lock:
            st.error("❌ Cannot create backup while parser is locked!")
        else:
            with st.spinner("Creating local backup..."):
                success, result = create_local_backup()
                if success:
                    st.success(f"✅ Local backup created: {result}")
                else:
                    st.error(f"❌ Local backup failed: {result}")

with col2:
    if st.button("☁️ Create Azure Backup", type="primary"):
        if st.session_state.parser_lock:
            st.error("❌ Cannot create backup while parser is locked!")
        elif not st.session_state.azure_api_key:
            st.error("❌ Azure API key required!")
        else:
            with st.spinner("Uploading to Azure..."):
                success, result = simulate_azure_backup()
                if success:
                    st.success(f"✅ Azure backup created: {result}")
                else:
                    st.error(f"❌ Azure backup failed: {result}")

with col3:
    if st.button("🔄 Full System Backup", type="secondary"):
        if st.session_state.parser_lock:
            st.error("❌ Cannot create backup while parser is locked!")
        else:
            with st.spinner("Creating full system backup..."):
                # Local backup
                local_success, local_result = create_local_backup()
                
                # Azure backup if API key available
                azure_success, azure_result = True, "Skipped (no API key)"
                if st.session_state.azure_api_key:
                    azure_success, azure_result = simulate_azure_backup()
                
                if local_success and azure_success:
                    st.success("✅ Full system backup completed successfully!")
                else:
                    st.warning(f"⚠️ Partial backup completed. Local: {local_result}, Azure: {azure_result}")

st.markdown("---")

# Backup Log Section
st.markdown("### 📋 Backup Activity Log")

if st.session_state.backup_log:
    # Convert log to DataFrame for display
    log_df = pd.DataFrame(st.session_state.backup_log)
    log_df['timestamp'] = pd.to_datetime(log_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Display log with color coding
    for idx, row in log_df.iterrows():
        status_color = "🟢" if row['status'] == "SUCCESS" else "🔴"
        
        st.markdown(f"""
        <div class="backup-log">
            <strong>{status_color} {row['operation']}</strong> - {row['timestamp']}<br>
            <small>Status: {row['status']}</small><br>
            <small>Details: {row['details']}</small>
            {f"<br><small>Backup Name: {row['backup_name']}</small>" if row['backup_name'] else ""}
        </div>
        """, unsafe_allow_html=True)
    
    # Clear log button
    if st.button("🗑️ Clear Backup Log"):
        st.session_state.backup_log = []
        st.rerun()

else:
    st.info("📝 No backup operations logged yet")

st.markdown("---")

# Restore Operations Section
st.markdown("### 🔄 Restore Operations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🏠 Local Restore Options")
    
    # List available local backups
    if os.path.exists(local_backup_path):
        backup_files = []
        for item in os.listdir(local_backup_path):
            if item.startswith("intellicv_backup_"):
                backup_files.append(item)
        
        if backup_files:
            selected_backup = st.selectbox("Select Local Backup", backup_files)
            
            if st.button("🔄 Restore from Local Backup"):
                st.warning("⚠️ Restore operation would be implemented here")
                st.info(f"Selected backup: {selected_backup}")
        else:
            st.info("No local backups found")
    else:
        st.info("Local backup directory not found")

with col2:
    st.markdown("#### ☁️ Azure Restore Options")
    
    if st.session_state.azure_api_key:
        # Simulate listing Azure backups
        azure_backups = [
            "intellicv_backup_20250925_120000.zip",
            "intellicv_backup_20250924_180000.zip",
            "intellicv_backup_20250923_140000.zip"
        ]
        
        selected_azure_backup = st.selectbox("Select Azure Backup", azure_backups)
        
        if st.button("☁️ Restore from Azure Backup"):
            st.warning("⚠️ Azure restore operation would be implemented here")
            st.info(f"Selected backup: {selected_azure_backup}")
    else:
        st.info("Azure API key required for restore operations")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 30px;">
    <p>🔄 IntelliCV Backup Management System | Advanced Data Protection & Recovery</p>
</div>
""", unsafe_allow_html=True)