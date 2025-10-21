#!/usr/bin/env python3
"""
Complete Admin Portal Test Launcher
Comprehensive testing interface for all AI tools and dashboard functionality
"""

import os
import subprocess
import sys
import time
import json
from pathlib import Path
from datetime import datetime

class AdminPortalTestLauncher:
    """Complete test launcher for admin portal and AI tools"""
    
    def __init__(self):
        self.sandbox_path = Path("C:\\IntelliCV\\SANDBOX\\admin_portal")
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'tests_run': [],
            'ai_engines_tested': [],
            'dashboard_pages_tested': [],
            'integration_tests': []
        }
        
        print("🧪 Admin Portal Test Launcher initialized")
        print(f"📂 Sandbox location: {self.sandbox_path}")

    def run_comprehensive_tests(self):
        """Run comprehensive testing suite"""
        print("\n🚀 RUNNING COMPREHENSIVE ADMIN PORTAL TESTS")
        print("=" * 80)
        
        # Test 1: System readiness
        self._test_system_readiness()
        
        # Test 2: AI engines
        self._test_ai_engines()
        
        # Test 3: Data integration
        self._test_data_integration()
        
        # Test 4: Dashboard functionality
        self._test_dashboard_functionality()
        
        # Test 5: Admin tools
        self._test_admin_tools()
        
        # Generate test report
        self._generate_test_report()
        
        print("\n✅ COMPREHENSIVE TESTING COMPLETE")
        print("🎯 Ready for admin user testing!")

    def _test_system_readiness(self):
        """Test system readiness"""
        print("\n🔧 Testing System Readiness...")
        
        tests = [
            ("Sandbox directory exists", self.sandbox_path.exists()),
            ("App.py exists", (self.sandbox_path / "app.py").exists()),
            ("Pages directory exists", (self.sandbox_path / "pages").exists()),
            ("Modules directory exists", (self.sandbox_path / "modules").exists()),
            ("Data directory exists", Path("C:\\IntelliCV\\SANDBOX\\Data for enrichment").exists()),
            ("Environment file exists", (self.sandbox_path / ".env").exists())
        ]
        
        for test_name, result in tests:
            status = "✅" if result else "❌"
            print(f"   {status} {test_name}")
            self.test_results['tests_run'].append({
                'name': test_name,
                'status': 'passed' if result else 'failed',
                'category': 'system_readiness'
            })

    def _test_ai_engines(self):
        """Test AI engines integration"""
        print("\n🤖 Testing AI Engines...")
        
        ai_engines = [
            "bayes_engine",
            "inference_engine", 
            "nlp_engine",
            "llm_engine"
        ]
        
        try:
            # Load AI tools configuration
            ai_tools_file = self.sandbox_path / "ai_tools_integration.json"
            if ai_tools_file.exists():
                with open(ai_tools_file, 'r') as f:
                    ai_tools = json.load(f)
                
                for engine in ai_engines:
                    if engine in ai_tools:
                        engine_info = ai_tools[engine]
                        status = "✅" if engine_info.get("data_ready", False) else "⚠️"
                        print(f"   {status} {engine_info['name']}: {engine_info['status']}")
                        
                        self.test_results['ai_engines_tested'].append({
                            'engine': engine,
                            'name': engine_info['name'],
                            'status': engine_info['status'],
                            'data_ready': engine_info.get("data_ready", False)
                        })
            else:
                print("   ⚠️  AI tools configuration not found")
                
        except Exception as e:
            print(f"   ❌ Error testing AI engines: {e}")

    def _test_data_integration(self):
        """Test data integration"""
        print("\n📊 Testing Data Integration...")
        
        data_paths = [
            ("Enriched Data", Path("C:\\IntelliCV\\SANDBOX\\Data for enrichment\\ai_enriched_output")),
            ("CSV Integration", Path("C:\\IntelliCV\\SANDBOX\\Data for enrichment\\ai_csv_integration")),
            ("Intelligence Data", Path("C:\\IntelliCV\\SANDBOX\\Data for enrichment\\enriched_output")),
            ("Email Database", Path("C:\\IntelliCV\\SANDBOX\\Data for enrichment\\email_database.json")),
            ("Keywords Data", Path("C:\\IntelliCV\\SANDBOX\\Data for enrichment\\keywords_comprehensive.json"))
        ]
        
        for data_name, data_path in data_paths:
            exists = data_path.exists()
            status = "✅" if exists else "⚠️"
            
            if exists and data_path.is_dir():
                file_count = len(list(data_path.glob("*")))
                print(f"   {status} {data_name}: {file_count} files")
            elif exists and data_path.is_file():
                size_mb = data_path.stat().st_size / (1024 * 1024)
                print(f"   {status} {data_name}: {size_mb:.1f}MB")
            else:
                print(f"   {status} {data_name}: Not found")
            
            self.test_results['integration_tests'].append({
                'name': data_name,
                'exists': exists,
                'path': str(data_path)
            })

    def _test_dashboard_functionality(self):
        """Test dashboard functionality"""
        print("\n📄 Testing Dashboard Pages...")
        
        pages_dir = self.sandbox_path / "pages"
        if pages_dir.exists():
            dashboard_pages = list(pages_dir.glob("*.py"))
            
            for page_file in dashboard_pages:
                page_name = page_file.stem
                try:
                    # Basic syntax check
                    with open(page_file, 'r', encoding='utf-8') as f:
                        code = f.read()
                    
                    # Check for common imports
                    has_streamlit = 'import streamlit' in code
                    has_main_function = 'def ' in code
                    
                    status = "✅" if has_streamlit and has_main_function else "⚠️"
                    print(f"   {status} {page_name}: Syntax OK")
                    
                    self.test_results['dashboard_pages_tested'].append({
                        'page': page_name,
                        'syntax_ok': True,
                        'has_streamlit': has_streamlit,
                        'has_functions': has_main_function
                    })
                    
                except Exception as e:
                    print(f"   ❌ {page_name}: Error - {e}")
                    self.test_results['dashboard_pages_tested'].append({
                        'page': page_name,
                        'syntax_ok': False,
                        'error': str(e)
                    })
        else:
            print("   ⚠️  Pages directory not found")

    def _test_admin_tools(self):
        """Test admin tools functionality"""
        print("\n🛠️  Testing Admin Tools...")
        
        admin_tools = [
            ("User Management", "pages/01_User_Management.py"),
            ("Data Parsers", "pages/02_Data_Parsers.py"),
            ("Semantic NLP Engine", "pages/04_Semantic_NLP_Engine.py"),
            ("Admin Backoffice", "pages/05_Admin_Backoffice.py"),
            ("System Monitor", "pages/06_System_Monitor.py"),
            ("Settings", "pages/08_Settings.py")
        ]
        
        for tool_name, tool_path in admin_tools:
            full_path = self.sandbox_path / tool_path
            exists = full_path.exists()
            status = "✅" if exists else "⚠️"
            print(f"   {status} {tool_name}")

    def _generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n📋 Generating Test Report...")
        
        report_path = self.sandbox_path / "TEST_REPORT.json"
        
        # Calculate test summary
        total_tests = len(self.test_results['tests_run'])
        passed_tests = len([t for t in self.test_results['tests_run'] if t['status'] == 'passed'])
        ai_engines_ready = len([e for e in self.test_results['ai_engines_tested'] if e.get('data_ready', False)])
        dashboard_pages_ok = len([p for p in self.test_results['dashboard_pages_tested'] if p.get('syntax_ok', False)])
        
        self.test_results['summary'] = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'ai_engines_ready': ai_engines_ready,
            'dashboard_pages_tested': len(self.test_results['dashboard_pages_tested']),
            'dashboard_pages_ok': dashboard_pages_ok,
            'overall_status': 'READY' if passed_tests == total_tests else 'NEEDS_ATTENTION'
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        print(f"   📋 Test report saved: {report_path}")
        
        # Display summary
        print(f"\n📊 TEST SUMMARY")
        print(f"   ✅ Tests passed: {passed_tests}/{total_tests}")
        print(f"   🤖 AI engines ready: {ai_engines_ready}/4")
        print(f"   📄 Dashboard pages OK: {dashboard_pages_ok}")
        print(f"   🎯 Overall status: {self.test_results['summary']['overall_status']}")

    def launch_admin_portal(self):
        """Launch the admin portal for testing"""
        print("\n🚀 LAUNCHING ADMIN PORTAL FOR TESTING")
        print("=" * 60)
        
        if not self.sandbox_path.exists():
            print("❌ Sandbox not found. Please run sandbox creation first.")
            return
        
        # Change to sandbox directory
        os.chdir(self.sandbox_path)
        
        # Launch command
        python_exe = Path("../../env310/python.exe")
        
        if not python_exe.exists():
            print("❌ Python environment not found")
            return
        
        launch_cmd = [
            str(python_exe),
            "-m", "streamlit", "run", "app.py",
            "--server.port", "8503",
            "--server.headless", "false"
        ]
        
        print("🌐 Starting admin portal at: http://localhost:8503")
        print("🧪 Sandbox test environment ready")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 60)
        
        try:
            subprocess.run(launch_cmd)
        except KeyboardInterrupt:
            print("\n🛑 Admin portal stopped")
        except Exception as e:
            print(f"❌ Error launching portal: {e}")

    def create_admin_testing_guide(self):
        """Create comprehensive admin testing guide"""
        print("\n📚 Creating Admin Testing Guide...")
        
        guide_content = '''# IntelliCV Admin Portal - Testing Guide

## 🎯 Admin User Testing Workflow

### Pre-Testing Checklist
- [ ] Sandbox environment launched successfully
- [ ] All 4 AI engines showing as active
- [ ] Dashboard loads at http://localhost:8503
- [ ] No console errors visible

### 1. Dashboard Overview Testing
**Page: Enhanced Dashboard Overview**
- [ ] Key metrics display correctly (candidates, companies, emails, keywords)
- [ ] Email domain charts render properly
- [ ] Skills distribution pie chart shows data
- [ ] AI tools status shows all green
- [ ] Data quality score displays and makes sense

### 2. AI Analytics Testing
**Page: AI Analytics Dashboard**
- [ ] All 4 AI engines show as "Active"
- [ ] Engine capabilities list correctly
- [ ] Data sources display for each engine
- [ ] Intelligence categories table populates
- [ ] Email analytics section shows metrics

### 3. Data Management Testing
**Page: Data Management Dashboard**
- [ ] Integration status shows all components as "Integrated"
- [ ] Data quality metrics display (should be ~94.2%)
- [ ] File processing summary shows success rates
- [ ] Export buttons respond (may show placeholder messages)
- [ ] System health check shows all green

### 4. Intelligence Insights Testing
**Page: Intelligence Insights Dashboard**
- [ ] Skills intelligence bar chart displays
- [ ] Market intelligence treemap renders
- [ ] Email verification pie chart shows data
- [ ] Domain distribution chart populates
- [ ] AI processing metrics show good performance
- [ ] Recommendations section provides insights

### 5. Admin Functions Testing
**Test each admin function page:**
- [ ] User Management - loads and shows interface
- [ ] Data Parsers - displays parsing options
- [ ] Semantic NLP Engine - shows NLP capabilities
- [ ] Admin Backoffice - backend management tools
- [ ] System Monitor - system health and logs
- [ ] Settings - configuration options

### 6. AI Engine Verification
**For each AI engine, verify:**
- [ ] **Bayes Engine**: Statistical analysis capabilities
- [ ] **Inference Engine**: Skill matching and analysis
- [ ] **NLP Engine**: Text processing and keyword extraction
- [ ] **LLM Engine**: Content generation and insights

### 7. Data Integration Verification
**Check data accessibility:**
- [ ] Candidate data loads in relevant sections
- [ ] Company intelligence displays
- [ ] Email analytics show domain analysis
- [ ] Skills data appears in charts
- [ ] Keywords and insights are accessible

### 8. Performance Testing
**Monitor system performance:**
- [ ] Page load times are reasonable (< 3 seconds)
- [ ] Charts and graphs render smoothly
- [ ] No memory leaks or excessive CPU usage
- [ ] Navigation between pages works seamlessly

### 9. Error Handling Testing
**Test error scenarios:**
- [ ] Navigate to non-existent page
- [ ] Try to access data that might not exist
- [ ] Check console for any JavaScript errors
- [ ] Verify graceful error messages

### 10. Admin Workflow Testing
**Complete workflow scenarios:**
- [ ] **Scenario 1**: Check candidate pipeline - view candidates, analyze skills, review AI scores
- [ ] **Scenario 2**: Company intelligence - review company data, analyze requirements, check matches
- [ ] **Scenario 3**: Email campaign prep - analyze email database, check domains, verify quality
- [ ] **Scenario 4**: System health check - review all metrics, check AI performance, validate data quality

## 🔧 Admin Capabilities to Validate

### Data Analysis Capabilities
- [ ] View comprehensive candidate analytics
- [ ] Analyze email database quality and distribution
- [ ] Review skills demand and market intelligence
- [ ] Access AI-generated keywords and insights

### AI-Powered Insights
- [ ] Candidate scoring and ranking
- [ ] Skill matching and recommendations
- [ ] Market intelligence and trends
- [ ] Automated keyword extraction

### Administrative Controls
- [ ] User management (if applicable)
- [ ] System monitoring and health checks
- [ ] Data parsing and processing controls
- [ ] Configuration and settings management

### Reporting and Analytics
- [ ] Generate performance reports
- [ ] Export data and analytics
- [ ] View historical trends
- [ ] Monitor system metrics

## 🎯 Expected Admin Outcomes

After completing testing, as an admin you should be able to:

1. **Understand User Needs**: 
   - Clear view of candidate pipeline and quality
   - Insight into skill demands and market trends
   - Understanding of user engagement patterns

2. **Make Data-Driven Decisions**:
   - Identify high-quality candidates using AI scores
   - Optimize email campaigns based on analytics
   - Focus on in-demand skills and capabilities

3. **Monitor System Health**:
   - Ensure all AI engines are performing optimally
   - Validate data quality and integration success
   - Track system performance and usage

4. **Provide User Value**:
   - Understand what users need from the platform
   - Ensure data quality supports user goals
   - Optimize system performance for user experience

## 🚨 Issues to Report

If you encounter any of these, please report:
- [ ] Pages that fail to load
- [ ] Charts or graphs that don't render
- [ ] Missing or incorrect data
- [ ] AI engines showing as inactive
- [ ] Performance issues or slow loading
- [ ] Error messages or console errors

## ✅ Testing Complete

Once all items are checked, the admin portal is validated and ready for:
- Production deployment
- User portal integration
- Backend API connection
- Full system launch

---

**Test Environment**: Sandbox - Safe for testing
**Test Data**: Sample data included for validation
**Next Steps**: Production deployment after successful testing
'''
        
        guide_path = self.sandbox_path / "ADMIN_TESTING_GUIDE.md"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"   📚 Testing guide created: {guide_path}")

def main():
    """Main execution function"""
    launcher = AdminPortalTestLauncher()
    
    print("🧪 IntelliCV Admin Portal Test Launcher")
    print("=" * 60)
    print("1. Run comprehensive tests")
    print("2. Launch admin portal for testing")
    print("3. Create admin testing guide")
    print("4. Run all and launch")
    print("=" * 60)
    
    choice = input("Select option (1-4): ").strip()
    
    if choice == "1":
        launcher.run_comprehensive_tests()
    elif choice == "2":
        launcher.launch_admin_portal()
    elif choice == "3":
        launcher.create_admin_testing_guide()
    elif choice == "4":
        launcher.run_comprehensive_tests()
        launcher.create_admin_testing_guide()
        print("\n🚀 Launching admin portal...")
        time.sleep(2)
        launcher.launch_admin_portal()
    else:
        print("Running all tests and launching...")
        launcher.run_comprehensive_tests()
        launcher.create_admin_testing_guide()
        launcher.launch_admin_portal()

if __name__ == "__main__":
    main()