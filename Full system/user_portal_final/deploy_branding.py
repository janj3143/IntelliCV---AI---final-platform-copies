"""
🚀 IntelliCV-AI Branding Deployment Script
==========================================
Systematically apply 30% logo branding to all portal pages
One-click deployment for consistent visual identity
"""

import os
import re
from pathlib import Path

class BrandingDeployment:
    def __init__(self, pages_directory):
        self.pages_dir = Path(pages_directory)
        self.branding_import = "from intellicv_master_branding import apply_intellicv_branding, create_intellicv_header, create_intellicv_footer"
        self.deployment_log = []
    
    def analyze_page(self, file_path):
        """Analyze a page to determine branding requirements"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analysis = {
            'has_branding': 'apply_intellicv_branding' in content,
            'has_streamlit': 'import streamlit as st' in content,
            'has_page_config': 'st.set_page_config' in content,
            'has_header': any(tag in content for tag in ['st.title', 'st.header', 'st.markdown.*h1']),
            'has_auth_check': 'authenticated_user' in content,
            'has_token_system': 'token_management_system' in content or 'TokenManager' in content,
            'estimated_tokens': self.estimate_token_cost(content),
            'page_type': self.determine_page_type(file_path.name, content)
        }
        
        return analysis
    
    def estimate_token_cost(self, content):
        """Estimate token cost based on page complexity"""
        if 'AI' in content and 'enhanced' in content.lower():
            return 5
        elif 'upload' in content.lower() or 'analysis' in content.lower():
            return 3
        elif 'admin' in content.lower() or 'management' in content.lower():
            return 2
        else:
            return 1
    
    def determine_page_type(self, filename, content):
        """Determine appropriate branding type for page"""
        if 'admin' in filename.lower() or 'admin' in content.lower():
            return 'admin'
        elif 'enhanced' in filename.lower() or 'premium' in content.lower() or 'AI' in content:
            return 'premium'
        elif 'home' in filename.lower() or 'welcome' in filename.lower():
            return 'landing'
        else:
            return 'standard'
    
    def generate_branding_code(self, analysis, filename):
        """Generate the branding code to insert"""
        page_name = filename.replace('.py', '').replace('_', ' ').title()
        
        branding_code = f"""
# Apply IntelliCV-AI Branding
from intellicv_master_branding import apply_intellicv_branding, create_intellicv_header, create_intellicv_footer

# Apply {analysis['page_type']} branding
apply_intellicv_branding("{analysis['page_type']}")
"""
        
        if analysis['has_header']:
            branding_code += f"""
# Enhanced header (replace existing title/header)
create_intellicv_header(
    "{page_name}",
    "Professional resume and career intelligence platform",
    "{analysis['page_type']}",
    True,
    {analysis['estimated_tokens']}
)
"""
        
        return branding_code
    
    def create_footer_code(self, analysis, filename):
        """Generate footer code"""
        page_name = filename.replace('.py', '').replace('_', ' ').title()
        
        footer_code = f"""
# Apply IntelliCV-AI Footer
create_intellicv_footer(
    "{page_name}",
    {analysis['estimated_tokens'] if analysis['has_token_system'] else 'None'},
    "Enhanced with AI intelligence"
)
"""
        return footer_code
    
    def deploy_to_page(self, file_path, dry_run=True):
        """Deploy branding to a specific page"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = self.analyze_page(file_path)
            
            if analysis['has_branding']:
                self.deployment_log.append(f"✅ SKIP: {file_path.name} - Already has branding")
                return True
            
            if not analysis['has_streamlit']:
                self.deployment_log.append(f"⚠️ SKIP: {file_path.name} - Not a Streamlit page")
                return False
            
            # Generate new content with branding
            new_content = content
            
            # Add import after existing imports
            import_pattern = r'(import streamlit as st.*?\n)'
            if re.search(import_pattern, content, re.DOTALL):
                new_content = re.sub(
                    import_pattern,
                    r'\1' + self.branding_import + '\n\n',
                    new_content
                )
            
            # Add branding code after page config
            if analysis['has_page_config']:
                config_pattern = r'(st\.set_page_config\(.*?\)\n)'
                branding_code = self.generate_branding_code(analysis, file_path.name)
                new_content = re.sub(
                    config_pattern,
                    r'\1' + branding_code,
                    new_content,
                    flags=re.DOTALL
                )
            
            # Add footer at the end (before any existing footer)
            footer_code = self.create_footer_code(analysis, file_path.name)
            if not any(term in content for term in ['create_intellicv_footer', 'Last Updated']):
                new_content += '\n' + footer_code
            
            if dry_run:
                self.deployment_log.append(f"📋 PLAN: {file_path.name} - Would add {analysis['page_type']} branding")
                return True
            else:
                # Write the updated content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                self.deployment_log.append(f"✅ DEPLOYED: {file_path.name} - Added {analysis['page_type']} branding")
                return True
                
        except Exception as e:
            self.deployment_log.append(f"❌ ERROR: {file_path.name} - {str(e)}")
            return False
    
    def deploy_all_pages(self, dry_run=True):
        """Deploy branding to all pages in the directory"""
        python_files = list(self.pages_dir.glob("*.py"))
        
        results = {
            'total_pages': len(python_files),
            'processed': 0,
            'skipped': 0,
            'errors': 0,
            'deployed': 0
        }
        
        self.deployment_log.append(f"🚀 Starting branding deployment for {len(python_files)} pages")
        self.deployment_log.append(f"📁 Directory: {self.pages_dir}")
        self.deployment_log.append(f"🔍 Mode: {'DRY RUN' if dry_run else 'LIVE DEPLOYMENT'}")
        self.deployment_log.append("=" * 60)
        
        for file_path in python_files:
            if file_path.name.startswith('__'):
                continue
                
            results['processed'] += 1
            
            success = self.deploy_to_page(file_path, dry_run)
            
            if 'SKIP' in self.deployment_log[-1]:
                results['skipped'] += 1
            elif 'ERROR' in self.deployment_log[-1]:
                results['errors'] += 1
            elif 'DEPLOYED' in self.deployment_log[-1] or 'PLAN' in self.deployment_log[-1]:
                results['deployed'] += 1
        
        self.deployment_log.append("=" * 60)
        self.deployment_log.append(f"📊 DEPLOYMENT SUMMARY:")
        self.deployment_log.append(f"   Total Pages: {results['total_pages']}")
        self.deployment_log.append(f"   Processed: {results['processed']}")
        self.deployment_log.append(f"   To Deploy: {results['deployed']}")
        self.deployment_log.append(f"   Skipped: {results['skipped']}")
        self.deployment_log.append(f"   Errors: {results['errors']}")
        
        return results
    
    def generate_deployment_report(self):
        """Generate a deployment report"""
        return "\\n".join(self.deployment_log)
    
    def create_branded_page_template(self, page_name, page_type="standard", token_cost=1):
        """Create a new page with branding pre-applied"""
        template = f'''"""
{page_name} - IntelliCV-AI Portal Page
{"=" * (len(page_name) + 30)}
Professional resume and career intelligence platform
"""

import streamlit as st
from pathlib import Path
import sys
from datetime import datetime

# Setup paths and imports
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

# Apply IntelliCV-AI Branding
from intellicv_master_branding import apply_intellicv_branding, create_intellicv_header, create_intellicv_footer

# Import token management
try:
    from token_management_system import TokenManager
    TOKEN_SYSTEM_AVAILABLE = True
except ImportError:
    TOKEN_SYSTEM_AVAILABLE = False

# Import utilities with fallbacks
try:
    from utils.error_handler import log_user_action, show_error, show_success
    ERROR_HANDLER_AVAILABLE = True
except ImportError:
    ERROR_HANDLER_AVAILABLE = False
    def log_user_action(action, details=None): pass
    def show_error(msg): st.error(f"❌ {{msg}}")
    def show_success(msg): st.success(f"✅ {{msg}}")

# Page configuration
st.set_page_config(
    page_title="{page_name} | IntelliCV-AI",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply {page_type} branding
apply_intellicv_branding("{page_type}")

# Authentication check
if not st.session_state.get('authenticated_user'):
    st.error("🔒 Please log in to access this page")
    if st.button("🏠 Return to Home"):
        st.switch_page("pages/00_Home.py")
    st.stop()

# Token Management Check
if TOKEN_SYSTEM_AVAILABLE:
    token_manager = TokenManager()
    if not token_manager.check_page_access(st.session_state.get('user_id'), '{page_name.lower().replace(" ", "_")}'):
        st.error(f"🪙 Insufficient tokens for {page_name} (Cost: {token_cost} tokens)")
        if st.button("💰 Get More Tokens"):
            st.switch_page("pages/02_Payment.py")
        st.stop()

# Enhanced header
create_intellicv_header(
    "{page_name}",
    "Professional resume and career intelligence platform",
    "{page_type}",
    True,
    {token_cost}
)

# Main content area
st.markdown("### 🚀 Page Content")
st.write("This is a template page with IntelliCV-AI branding pre-applied.")

# Sidebar content
with st.sidebar:
    st.markdown("### 🔧 Page Tools")
    
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/01_Dashboard.py")
    
    if st.button("👤 Profile", use_container_width=True):
        st.switch_page("pages/03_Profile_Setup_Enhanced_AI_Chatbot.py")
    
    if st.button("📄 Resume", use_container_width=True):
        st.switch_page("pages/05_Resume_Upload_Instant_Analysis.py")

# Log page access and consume tokens
if ERROR_HANDLER_AVAILABLE:
    log_user_action("page_view", {{"page": "{page_name.lower().replace(" ", "_")}", "timestamp": datetime.now().isoformat()}})

if TOKEN_SYSTEM_AVAILABLE:
    token_manager.consume_page_tokens(st.session_state.get('user_id'), '{page_name.lower().replace(" ", "_")}', {token_cost})

# Apply IntelliCV-AI Footer
create_intellicv_footer(
    "{page_name}",
    {token_cost},
    "Enhanced with AI intelligence"
)
'''
        return template

# Example usage and testing
if __name__ == "__main__":
    import streamlit as st
    
    st.set_page_config(
        page_title="🚀 Branding Deployment Tool",
        page_icon="🚀",
        layout="wide"
    )
    
    # Apply branding to this demo page
    from intellicv_master_branding import apply_intellicv_branding, create_intellicv_header, create_intellicv_footer
    apply_intellicv_branding("admin")
    
    create_intellicv_header(
        "🚀 IntelliCV-AI Branding Deployment Tool",
        "Systematically apply 30% logo branding to all portal pages",
        "admin",
        False
    )
    
    # Initialize deployment system
    pages_directory = st.text_input(
        "Pages Directory Path",
        value=str(Path(__file__).parent / "pages"),
        help="Enter the path to your pages directory"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔍 Dry Run Analysis")
        
        if st.button("🔍 Analyze Pages", use_container_width=True):
            if os.path.exists(pages_directory):
                deployer = BrandingDeployment(pages_directory)
                results = deployer.deploy_all_pages(dry_run=True)
                
                st.success(f"Analysis complete! Found {results['total_pages']} pages")
                
                # Show results
                col_result1, col_result2, col_result3 = st.columns(3)
                with col_result1:
                    st.metric("To Deploy", results['deployed'])
                with col_result2:
                    st.metric("To Skip", results['skipped'])
                with col_result3:
                    st.metric("Errors", results['errors'])
                
                # Show log
                st.text_area("Deployment Log", deployer.generate_deployment_report(), height=300)
            else:
                st.error("Directory not found!")
    
    with col2:
        st.markdown("### 🚀 Live Deployment")
        
        st.warning("⚠️ This will modify your files! Make sure you have backups.")
        
        confirm_deployment = st.checkbox("I have backups and want to proceed")
        
        if confirm_deployment and st.button("🚀 Deploy Branding", use_container_width=True, type="primary"):
            if os.path.exists(pages_directory):
                deployer = BrandingDeployment(pages_directory)
                results = deployer.deploy_all_pages(dry_run=False)
                
                if results['errors'] == 0:
                    st.success(f"✅ Deployment successful! Updated {results['deployed']} pages")
                else:
                    st.warning(f"⚠️ Deployment completed with {results['errors']} errors")
                
                # Show results
                col_result1, col_result2, col_result3 = st.columns(3)
                with col_result1:
                    st.metric("Deployed", results['deployed'])
                with col_result2:
                    st.metric("Skipped", results['skipped'])
                with col_result3:
                    st.metric("Errors", results['errors'])
                
                # Show log
                st.text_area("Deployment Log", deployer.generate_deployment_report(), height=300)
            else:
                st.error("Directory not found!")
    
    # Template generator
    st.markdown("---")
    st.markdown("### 📝 New Page Template Generator")
    
    col_template1, col_template2 = st.columns(2)
    
    with col_template1:
        template_name = st.text_input("Page Name", value="New Page")
        template_type = st.selectbox("Page Type", ["standard", "premium", "admin", "landing"])
        template_tokens = st.number_input("Token Cost", min_value=1, max_value=50, value=1)
    
    with col_template2:
        if st.button("📝 Generate Template", use_container_width=True):
            deployer = BrandingDeployment("")
            template_code = deployer.create_branded_page_template(template_name, template_type, template_tokens)
            
            st.text_area("Generated Template Code", template_code, height=400)
            
            # Download button would go here in a real implementation
            st.info("💡 Copy the template code to create a new pre-branded page")
    
    create_intellicv_footer("Branding Deployment Tool", None, "Administrative utility for systematic branding deployment")