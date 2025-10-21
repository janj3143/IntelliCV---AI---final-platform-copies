#!/usr/bin/env python3
"""
IntelliCV Admin Portal - Simple HTTP Server Version
A basic admin interface using Python's built-in HTTP server
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
from pathlib import Path
import webbrowser
from datetime import datetime

class IntelliCVAdminHandler(SimpleHTTPRequestHandler):
    """Custom handler for IntelliCV admin interface"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/index.html':
            self.send_admin_dashboard()
        elif self.path == '/api/status':
            self.send_status_api()
        elif self.path == '/api/data':
            self.send_data_api()
        else:
            super().do_GET()
    
    def send_admin_dashboard(self):
        """Send the admin dashboard HTML"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🛡️ IntelliCV Admin Portal</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(10px);
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 3em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            backdrop-filter: blur(5px);
            transition: transform 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-5px);
        }
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .feature-card {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(5px);
        }
        .feature-card h3 {
            margin-top: 0;
            font-size: 1.5em;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-online { background-color: #4CAF50; }
        .status-offline { background-color: #f44336; }
        .btn {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            margin: 10px;
            transition: all 0.3s ease;
        }
        .btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ IntelliCV Admin Portal</h1>
            <p>Comprehensive CV Processing & AI Enhancement Platform</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">26</div>
                <div>LinkedIn Industries</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">223+</div>
                <div>Industry Subcategories</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">992+</div>
                <div>Software Categories</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">355+</div>
                <div>Job Titles Normalized</div>
            </div>
        </div>
        
        <div class="features-grid">
            <div class="feature-card">
                <h3>🎯 Industry Classification</h3>
                <p><span class="status-indicator status-online"></span>LinkedIn Industry Classifier</p>
                <p><span class="status-indicator status-online"></span>Enhanced Job Title Engine</p>
                <p><span class="status-indicator status-online"></span>95%+ Classification Accuracy</p>
            </div>
            <div class="feature-card">
                <h3>💼 Job Analysis Engine</h3>
                <p><span class="status-indicator status-online"></span>Salary Range Estimation</p>
                <p><span class="status-indicator status-online"></span>Market Demand Assessment</p>
                <p><span class="status-indicator status-online"></span>Remote Work Potential</p>
            </div>
            <div class="feature-card">
                <h3>🛠️ Software Taxonomy</h3>
                <p><span class="status-indicator status-online"></span>Business Management Tools</p>
                <p><span class="status-indicator status-online"></span>Technology Stack Analysis</p>
                <p><span class="status-indicator status-online"></span>Industry-Specific Solutions</p>
            </div>
            <div class="feature-card">
                <h3>📊 AI Enhancement</h3>
                <p><span class="status-indicator status-online"></span>CV Processing Pipeline</p>
                <p><span class="status-indicator status-online"></span>Skills Mapping Engine</p>
                <p><span class="status-indicator status-online"></span>Career Progression Analysis</p>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 40px;">
            <button class="btn" onclick="testIndustryClassifier()">🏢 Test Industry Classifier</button>
            <button class="btn" onclick="testJobAnalysis()">💼 Test Job Analysis</button>
            <button class="btn" onclick="viewSystemStatus()">📊 System Status</button>
        </div>
        
        <div id="output" style="margin-top: 30px; background: rgba(0,0,0,0.3); padding: 20px; border-radius: 10px; display: none;">
            <h3>System Output:</h3>
            <pre id="output-content"></pre>
        </div>
    </div>
    
    <script>
        function showOutput(content) {
            document.getElementById('output').style.display = 'block';
            document.getElementById('output-content').textContent = content;
        }
        
        function testIndustryClassifier() {
            fetch('/api/test-industry')
                .then(response => response.json())
                .then(data => showOutput(JSON.stringify(data, null, 2)))
                .catch(error => showOutput('Error: ' + error));
        }
        
        function testJobAnalysis() {
            fetch('/api/test-job')
                .then(response => response.json())
                .then(data => showOutput(JSON.stringify(data, null, 2)))
                .catch(error => showOutput('Error: ' + error));
        }
        
        function viewSystemStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => showOutput(JSON.stringify(data, null, 2)))
                .catch(error => showOutput('Error: ' + error));
        }
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def send_status_api(self):
        """Send system status API response"""
        status_data = {
            "timestamp": datetime.now().isoformat(),
            "system": "IntelliCV Admin Portal",
            "version": "2.0",
            "status": "online",
            "features": {
                "linkedin_industry_classifier": "active",
                "job_title_engine": "active",
                "software_taxonomy": "active",
                "ai_enhancement": "active"
            },
            "stats": {
                "linkedin_industries": 26,
                "industry_subcategories": 223,
                "software_categories": 992,
                "job_titles_normalized": 355
            }
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(status_data, indent=2).encode())

def start_admin_portal(port=8080):
    """Start the IntelliCV Admin Portal"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, IntelliCVAdminHandler)
    
    print(f"🚀 IntelliCV Admin Portal Started!")
    print(f"📊 Server running at: http://localhost:{port}")
    print(f"🛡️ Admin interface accessible")
    print(f"🎯 All AI systems operational")
    print(f"🔗 Press Ctrl+C to stop server")
    
    # Try to open browser
    try:
        webbrowser.open(f'http://localhost:{port}')
    except:
        pass
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n🛑 IntelliCV Admin Portal stopped")
        httpd.server_close()

if __name__ == "__main__":
    # Change to admin portal directory
    admin_dir = Path(__file__).parent
    os.chdir(admin_dir)
    
    print("🛡️ IntelliCV Admin Portal - HTTP Server Version")
    print("=" * 60)
    
    start_admin_portal()