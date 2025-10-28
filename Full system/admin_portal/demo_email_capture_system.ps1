# =============================================================================
# Email Capture System Demo Script
# =============================================================================
# 
# Demonstrates the Multi-Provider Email Capture System for IntelliCV Admin Portal
# 
# This script shows how to:
# 1. Use existing Gmail and Yahoo app passwords
# 2. Configure new Outlook app password
# 3. Extract unique emails from all three providers
# 4. Export to CSV for Contact Communications
# 5. Target emails for app offers
#

Write-Host "📧 IntelliCV Multi-Provider Email Capture System Demo" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

# Check if the email capture system is available
$captureSystemPath = "C:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION\admin_portal\pages\05_1_Email_Capture_System.py"
$contactCommPath = "C:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION\admin_portal\pages\14_Contact_Communication.py"
$emailsDbPath = "C:\IntelliCV-AI\IntelliCV\ai_data_final\emails\emails_database.json"

Write-Host "🔍 Checking system components..." -ForegroundColor Yellow

if (Test-Path $captureSystemPath) {
    Write-Host "✅ Email Capture System page found" -ForegroundColor Green
} else {
    Write-Host "❌ Email Capture System page missing" -ForegroundColor Red
}

if (Test-Path $contactCommPath) {
    Write-Host "✅ Contact Communications page found" -ForegroundColor Green
} else {
    Write-Host "❌ Contact Communications page missing" -ForegroundColor Red
}

if (Test-Path $emailsDbPath) {
    Write-Host "✅ Emails database found" -ForegroundColor Green
    
    # Show database stats
    $emailsData = Get-Content $emailsDbPath | ConvertFrom-Json
    $totalEmails = $emailsData.Count
    $gmailCount = ($emailsData | Where-Object { $_.domain -like "*gmail*" }).Count
    $yahooCount = ($emailsData | Where-Object { $_.domain -like "*yahoo*" }).Count
    $outlookCount = ($emailsData | Where-Object { $_.domain -like "*outlook*" -or $_.domain -like "*hotmail*" -or $_.domain -like "*live*" }).Count
    
    Write-Host "📊 Database Statistics:" -ForegroundColor Cyan
    Write-Host "   📧 Total emails: $totalEmails" -ForegroundColor White
    Write-Host "   📮 Gmail: $gmailCount" -ForegroundColor White
    Write-Host "   📮 Yahoo: $yahooCount" -ForegroundColor White
    Write-Host "   📮 Outlook: $outlookCount" -ForegroundColor White
} else {
    Write-Host "❌ Emails database not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "📋 System Overview:" -ForegroundColor Cyan
Write-Host "   🔧 Page 05.1: Email Capture System - Configure accounts and capture emails" -ForegroundColor White
Write-Host "   📞 Page 14: Contact Communications - Import and manage captured emails" -ForegroundColor White
Write-Host "   📊 CSV Export: Export emails for marketing campaigns and app offers" -ForegroundColor White

Write-Host ""
Write-Host "⚙️ Configuration Requirements:" -ForegroundColor Yellow
Write-Host "   📮 Gmail: Use existing app password (2FA required)" -ForegroundColor White
Write-Host "   📮 Yahoo: Use existing app password (2FA required)" -ForegroundColor White
Write-Host "   📮 Outlook: Generate NEW app password for this system" -ForegroundColor White

Write-Host ""
Write-Host "🎯 App Offer Targeting Features:" -ForegroundColor Magenta
Write-Host "   ✅ Mark captured emails for app offers" -ForegroundColor White
Write-Host "   ✅ Filter by provider for targeted campaigns" -ForegroundColor White
Write-Host "   ✅ Export CSV with marketing consent fields" -ForegroundColor White
Write-Host "   ✅ Integration with Contact Communications page" -ForegroundColor White

Write-Host ""
Write-Host "📤 CSV Export Options:" -ForegroundColor Green
Write-Host "   📊 All providers combined" -ForegroundColor White
Write-Host "   📮 Provider-specific exports (Gmail, Yahoo, Outlook)" -ForegroundColor White
Write-Host "   🎯 App offer target lists" -ForegroundColor White
Write-Host "   📧 Marketing campaign lists with consent tracking" -ForegroundColor White

Write-Host ""
Write-Host "🚀 Quick Start Guide:" -ForegroundColor Cyan
Write-Host "   1. Open Admin Portal and navigate to Page 05.1 (Email Capture System)" -ForegroundColor White
Write-Host "   2. Configure your Gmail, Yahoo, and Outlook accounts with app passwords" -ForegroundColor White
Write-Host "   3. Run multi-provider capture to extract unique emails" -ForegroundColor White
Write-Host "   4. Export emails to CSV for Contact Communications" -ForegroundColor White
Write-Host "   5. Import CSV in Page 14 (Contact Communications) for marketing campaigns" -ForegroundColor White

Write-Host ""
Write-Host "💡 Usage Examples:" -ForegroundColor Yellow

# CSV Export Utility Demo
$csvUtilityPath = "C:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION\admin_portal\utilities\csv_email_export.py"

if (Test-Path $csvUtilityPath) {
    Write-Host "   📊 CSV Export Utility available:" -ForegroundColor Green
    Write-Host "      python csv_email_export.py --stats" -ForegroundColor Gray
    Write-Host "      python csv_email_export.py --provider gmail yahoo --output ./exports" -ForegroundColor Gray
    Write-Host "      python csv_email_export.py --app-offers" -ForegroundColor Gray
    Write-Host "      python csv_email_export.py --separate" -ForegroundColor Gray
} else {
    Write-Host "   ⚠️ CSV Export Utility not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔗 Integration Points:" -ForegroundColor Cyan
Write-Host "   📧 emails_database.json ←→ Email Capture System" -ForegroundColor White
Write-Host "   📤 CSV Exports ←→ Contact Communications" -ForegroundColor White
Write-Host "   🎯 App Offers ←→ Marketing Campaigns" -ForegroundColor White
Write-Host "   📊 Analytics ←→ Campaign Performance" -ForegroundColor White

Write-Host ""
Write-Host "🔐 Security Features:" -ForegroundColor Red
Write-Host "   ✅ App passwords only (no regular passwords)" -ForegroundColor White
Write-Host "   ✅ SSL/TLS encrypted connections" -ForegroundColor White
Write-Host "   ✅ GDPR-compliant consent tracking" -ForegroundColor White
Write-Host "   ✅ Secure credential handling" -ForegroundColor White

Write-Host ""
Write-Host "📈 Expected Results:" -ForegroundColor Green
Write-Host "   📧 Thousands of unique emails from your accounts" -ForegroundColor White
Write-Host "   📊 Provider breakdown and domain analysis" -ForegroundColor White
Write-Host "   🎯 Targeted lists for app promotion campaigns" -ForegroundColor White
Write-Host "   📞 Ready-to-use contact lists for marketing" -ForegroundColor White

Write-Host ""
Write-Host "🎉 Ready to capture emails from Gmail, Yahoo, and Outlook!" -ForegroundColor Green
Write-Host "   Launch the Admin Portal to get started with email capture." -ForegroundColor White

# Optionally launch the admin portal
$response = Read-Host "`n🚀 Launch Admin Portal now? (y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host "🚀 Launching IntelliCV Admin Portal..." -ForegroundColor Cyan
    
    $portalScript = "C:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION\admin_portal\launch_admin_portal.ps1"
    if (Test-Path $portalScript) {
        & $portalScript
    } else {
        Write-Host "❌ Admin portal launch script not found" -ForegroundColor Red
        Write-Host "💡 Navigate to the admin_portal directory and run: streamlit run main.py" -ForegroundColor Yellow
    }
}