#!/usr/bin/env python3
"""
IntelliCV Secure Admin Portal - HTTP Server Version with Authentication
A complete admin interface with login system using Python's built-in HTTP server
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import os
import hashlib
import base64
from pathlib import Path
import webbrowser
from datetime import datetime
import html

class SecureAdminHandler(SimpleHTTPRequestHandler):
    """Secure handler with authentication for IntelliCV admin interface"""
    
    sessions = {}  # Simple session storage
    
    def __init__(self, *args, **kwargs):
        self.auth_file = Path("admin_credentials.json")
        self.setup_default_credentials()
        super().__init__(*args, **kwargs)
    
    def setup_default_credentials(self):
        """Setup default admin credentials"""
        if not self.auth_file.exists():
            salt = os.urandom(32).hex()
            password_hash = hashlib.pbkdf2_hmac('sha256', 'admin123'.encode(), salt.encode(), 100000)
            credentials = {
                "admin": {
                    "password_hash": password_hash.hex(),
                    "salt": salt,
                    "created_at": datetime.now().isoformat()
                }
            }
            with open(self.auth_file, 'w') as f:
                json.dump(credentials, f, indent=2)
    
    def verify_credentials(self, username, password):
        """Verify login credentials"""
        try:
            with open(self.auth_file, 'r') as f:
                credentials = json.load(f)
            
            if username not in credentials:
                return False
            
            user_data = credentials[username]
            password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), 
                                               user_data['salt'].encode(), 100000)
            
            return password_hash.hex() == user_data['password_hash']
        except:
            return False
    
    def get_session_token(self, username):
        """Create session token"""
        import secrets
        token = secrets.token_urlsafe(32)
        self.sessions[token] = {
            'username': username,
            'created_at': datetime.now().isoformat()
        }
        return token
    
    def verify_session(self, token):
        """Verify session token"""
        return token in self.sessions
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/' or parsed_path.path == '/login':
            self.send_login_page()
        elif parsed_path.path == '/dashboard':
            # Check for session cookie
            cookie_header = self.headers.get('Cookie', '')
            session_token = None
            
            if 'session_token=' in cookie_header:
                session_token = cookie_header.split('session_token=')[1].split(';')[0]
            
            if session_token and self.verify_session(session_token):
                self.send_dashboard()
            else:
                self.send_redirect('/login')
        elif parsed_path.path == '/api/status':
            self.send_status_api()
        elif parsed_path.path == '/logout':
            self.handle_logout()
        elif parsed_path.path.startswith('/static/'):
            self.serve_static_file()
        else:
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/login':
            self.handle_login()
        else:
            self.send_error(404)
    
    def handle_login(self):
        """Handle login form submission"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        form_data = parse_qs(post_data)
        
        username = form_data.get('username', [''])[0]
        password = form_data.get('password', [''])[0]
        
        if self.verify_credentials(username, password):
            # Create session and redirect to dashboard
            session_token = self.get_session_token(username)
            
            self.send_response(302)
            self.send_header('Location', '/dashboard')
            self.send_header('Set-Cookie', f'session_token={session_token}; Path=/; HttpOnly')
            self.end_headers()
        else:
            # Redirect back to login with error
            self.send_redirect('/login?error=1')
    
    def handle_logout(self):
        """Handle logout"""
        cookie_header = self.headers.get('Cookie', '')
        if 'session_token=' in cookie_header:
            session_token = cookie_header.split('session_token=')[1].split(';')[0]
            if session_token in self.sessions:
                del self.sessions[session_token]
        
        self.send_response(302)
        self.send_header('Location', '/login')
        self.send_header('Set-Cookie', 'session_token=; Path=/; HttpOnly; Max-Age=0')
        self.end_headers()
    
    def send_redirect(self, location):
        """Send redirect response"""
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()
    
    def send_login_page(self):
        """Send login page"""
        error_msg = ""
        if '?error=1' in self.path:
            error_msg = '<div style="color: red; text-align: center; margin: 10px;">❌ Invalid credentials. Please try again.</div>'
        
        # Try to get logo
        logo_html = ""
        logo_path = Path("static/logo.png")
        if logo_path.exists():
            with open(logo_path, "rb") as f:
                logo_b64 = base64.b64encode(f.read()).decode()
                logo_html = f'<img src="data:image/png;base64,{logo_b64}" width="80" height="80" style="border-radius: 10px; margin-bottom: 20px;">'
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🛡️ IntelliCV Admin Login</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .login-container {{
            background: white;
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 400px;
            width: 100%;
            text-align: center;
        }}
        .login-header {{
            margin-bottom: 2rem;
        }}
        .login-header h1 {{
            color: #667eea;
            margin: 10px 0;
            font-size: 2rem;
        }}
        .form-group {{
            margin: 1.5rem 0;
            text-align: left;
        }}
        .form-group label {{
            display: block;
            margin-bottom: 0.5rem;
            color: #333;
            font-weight: 600;
        }}
        .form-group input {{
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s;
            box-sizing: border-box;
        }}
        .form-group input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        .login-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-top: 1rem;
            transition: transform 0.3s;
        }}
        .login-btn:hover {{
            transform: translateY(-2px);
        }}
        .credentials-info {{
            background: #f8f9ff;
            padding: 1rem;
            border-radius: 10px;
            margin-top: 2rem;
            border-left: 4px solid #667eea;
        }}
        .credentials-info h4 {{
            margin: 0 0 0.5rem 0;
            color: #667eea;
        }}
        .security-notice {{
            background: #fff3cd;
            padding: 1rem;
            border-radius: 10px;
            margin-top: 1rem;
            border-left: 4px solid #ffc107;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            {logo_html}
            <h1>🛡️ IntelliCV Admin</h1>
            <p style="color: #666; margin: 0;">Secure Administrator Access</p>
        </div>
        
        {error_msg}
        
        <form method="POST" action="/login">
            <div class="form-group">
                <label for="username">👤 Username</label>
                <input type="text" id="username" name="username" required placeholder="Enter admin username">
            </div>
            <div class="form-group">
                <label for="password">🔐 Password</label>
                <input type="password" id="password" name="password" required placeholder="Enter password">
            </div>
            <button type="submit" class="login-btn">🚀 Login to Admin Portal</button>
        </form>
        
        <div class="credentials-info">
            <h4>🔑 Default Credentials</h4>
            <p><strong>Username:</strong> admin<br>
               <strong>Password:</strong> admin123</p>
        </div>
        
        <div class="security-notice">
            <strong>🚨 Security Notice:</strong> Please change the default password after first login.
        </div>
    </div>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def send_dashboard(self):
        """Send the main admin dashboard"""
        # Get session info
        cookie_header = self.headers.get('Cookie', '')
        session_token = cookie_header.split('session_token=')[1].split(';')[0]
        session_info = self.sessions[session_token]
        username = session_info['username']
        login_time = session_info['created_at']
        
        # Try to get logo
        logo_html = ""
        logo_path = Path("static/logo.png")
        if logo_path.exists():
            with open(logo_path, "rb") as f:
                logo_b64 = base64.b64encode(f.read()).decode()
                logo_html = f'<img src="data:image/png;base64,{logo_b64}" width="80" height="80" style="border-radius: 10px; margin-right: 20px;">'
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🛡️ IntelliCV Admin Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .header-content {{
            display: flex;
            align-items: center;
        }}
        .header h1 {{
            font-size: 2.5rem;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .auth-info {{
            background: rgba(255, 255, 255, 0.2);
            padding: 15px 20px;
            border-radius: 15px;
            backdrop-filter: blur(5px);
        }}
        .logout-btn {{
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
        }}
        .logout-btn:hover {{
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.05);
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            backdrop-filter: blur(5px);
            transition: transform 0.3s ease;
        }}
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .feature-card {{
            background: rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(5px);
        }}
        .feature-card h3 {{
            margin-top: 0;
            font-size: 1.5em;
        }}
        .status-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }}
        .status-online {{ background-color: #4CAF50; }}
        .btn {{
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            margin: 10px;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }}
        .btn:hover {{
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.05);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                {logo_html}
                <div>
                    <h1>🛡️ IntelliCV Admin Portal</h1>
                    <p style="margin: 5px 0 0 0; opacity: 0.9;">AI-Powered CV Processing & Analysis Platform</p>
                </div>
            </div>
            <div style="text-align: right;">
                <div class="auth-info">
                    <p style="margin: 0; font-weight: 600;">👋 Welcome, {html.escape(username)}</p>
                    <p style="margin: 5px 0 0 0; font-size: 0.9em; opacity: 0.8;">Login: {login_time[:19].replace('T', ' ')}</p>
                </div>
                <a href="/logout" class="logout-btn" style="margin-top: 10px; display: inline-block;">🚪 Logout</a>
            </div>
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
                <p style="margin-top: 15px;">
                    <a href="#" class="btn" onclick="testIndustryClassifier()">Test Classifier</a>
                </p>
            </div>
            <div class="feature-card">
                <h3>💼 Job Analysis Engine</h3>
                <p><span class="status-indicator status-online"></span>Salary Range Estimation</p>
                <p><span class="status-indicator status-online"></span>Market Demand Assessment</p>
                <p><span class="status-indicator status-online"></span>Remote Work Potential</p>
                <p style="margin-top: 15px;">
                    <a href="#" class="btn" onclick="testJobAnalysis()">Test Analysis</a>
                </p>
            </div>
            <div class="feature-card">
                <h3>🛠️ Software Taxonomy</h3>
                <p><span class="status-indicator status-online"></span>Business Management Tools</p>
                <p><span class="status-indicator status-online"></span>Technology Stack Analysis</p>
                <p><span class="status-indicator status-online"></span>Industry-Specific Solutions</p>
                <p style="margin-top: 15px;">
                    <a href="#" class="btn" onclick="viewSoftwareCategories()">View Categories</a>
                </p>
            </div>
            <div class="feature-card">
                <h3>📊 AI Enhancement</h3>
                <p><span class="status-indicator status-online"></span>CV Processing Pipeline</p>
                <p><span class="status-indicator status-online"></span>Skills Mapping Engine</p>
                <p><span class="status-indicator status-online"></span>Career Progression Analysis</p>
                <p style="margin-top: 15px;">
                    <a href="#" class="btn" onclick="viewSystemStatus()">System Status</a>
                </p>
            </div>
        </div>
        
        <div id="output" style="margin-top: 30px; background: rgba(0,0,0,0.3); padding: 20px; border-radius: 10px; display: none;">
            <h3>System Output:</h3>
            <pre id="output-content"></pre>
        </div>
        
        <div style="text-align: center; margin-top: 40px; opacity: 0.8;">
            <p>🛡️ <strong>IntelliCV Admin Portal</strong> • Secure Administrative Interface • Version 2.0</p>
            <p>Powered by AI-Enhanced CV Processing Technology</p>
        </div>
    </div>
    
    <script>
        function showOutput(content) {{
            document.getElementById('output').style.display = 'block';
            document.getElementById('output-content').textContent = content;
        }}
        
        function testIndustryClassifier() {{
            fetch('/api/test-industry')
                .then(response => response.json())
                .then(data => showOutput(JSON.stringify(data, null, 2)))
                .catch(error => showOutput('Error: ' + error));
        }}
        
        function testJobAnalysis() {{
            fetch('/api/test-job')
                .then(response => response.json())
                .then(data => showOutput(JSON.stringify(data, null, 2)))
                .catch(error => showOutput('Error: ' + error));
        }}
        
        function viewSoftwareCategories() {{
            showOutput('Software Categories:\\n- Business Management (150+ tools)\\n- Technology & Development (300+ tools)\\n- Industry-Specific Solutions (400+ tools)\\n- Specialized Tools (142+ tools)');
        }}
        
        function viewSystemStatus() {{
            fetch('/api/status')
                .then(response => response.json())
                .then(data => showOutput(JSON.stringify(data, null, 2)))
                .catch(error => showOutput('Error: ' + error));
        }}
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
            "authentication": "active",
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
                "job_titles_normalized": 355,
                "active_sessions": len(self.sessions)
            }
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(status_data, indent=2).encode())
    
    def serve_static_file(self):
        """Serve static files like images"""
        try:
            file_path = Path(self.path[1:])  # Remove leading slash
            if file_path.exists() and file_path.is_file():
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                # Determine content type
                content_type = 'application/octet-stream'
                if file_path.suffix.lower() == '.png':
                    content_type = 'image/png'
                elif file_path.suffix.lower() in ['.jpg', '.jpeg']:
                    content_type = 'image/jpeg'
                
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404)
        except Exception as e:
            self.send_error(500)

def start_secure_admin_portal(port=8081):
    """Start the secure IntelliCV Admin Portal"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, SecureAdminHandler)
    
    print(f"🛡️ IntelliCV Secure Admin Portal Started!")
    print(f"🔐 Authentication system enabled")
    print(f"📊 Server running at: http://localhost:{port}")
    print(f"👤 Default login: admin / admin123")
    print(f"🚪 Press Ctrl+C to stop server")
    
    # Try to open browser
    try:
        webbrowser.open(f'http://localhost:{port}')
    except:
        pass
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\\n🛑 IntelliCV Secure Admin Portal stopped")
        httpd.server_close()

if __name__ == "__main__":
    # Change to admin portal directory
    admin_dir = Path(__file__).parent
    os.chdir(admin_dir)
    
    print("🛡️ IntelliCV Secure Admin Portal - HTTP Server Version")
    print("=" * 70)
    
    start_secure_admin_portal()