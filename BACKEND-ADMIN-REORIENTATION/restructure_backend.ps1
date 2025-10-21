# Backend Restructuring - Quick Start Script
# Run this to begin the restructuring process

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "BACKEND RESTRUCTURING - STEP 1: MOVE BACKEND TO ROOT LEVEL" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

$reorientationRoot = "C:\IntelliCV-AI\IntelliCV\BACKEND-ADMIN-REORIENTATION"
$currentBackend = "$reorientationRoot\admin_portal\backend"
$newBackend = "$reorientationRoot\backend"

# Check if current backend exists
if (Test-Path $currentBackend) {
    Write-Host "✓ Current backend found at: $currentBackend" -ForegroundColor Green
    
    # Check if new backend already exists
    if (Test-Path $newBackend) {
        Write-Host "⚠ Backend already exists at root level: $newBackend" -ForegroundColor Yellow
        $response = Read-Host "Do you want to replace it? (y/n)"
        if ($response -ne 'y') {
            Write-Host "❌ Operation cancelled" -ForegroundColor Red
            exit
        }
        Remove-Item $newBackend -Recurse -Force
        Write-Host "✓ Removed existing backend" -ForegroundColor Green
    }
    
    # Move backend to root
    Write-Host ""
    Write-Host "Moving backend to root level..." -ForegroundColor Yellow
    Move-Item $currentBackend $newBackend
    Write-Host "✓ Backend moved to: $newBackend" -ForegroundColor Green
    
} else {
    Write-Host "✓ Backend already at root level" -ForegroundColor Green
}

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "STEP 2: CREATE SERVICE CATEGORY DIRECTORIES" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

$serviceDirs = @(
    "$newBackend\services\data_management",
    "$newBackend\services\cv_processing",
    "$newBackend\services\classification",
    "$newBackend\services\enrichment",
    "$newBackend\services\auth",
    "$newBackend\services\admin_only\email_integration",
    "$newBackend\services\admin_only\batch_operations",
    "$newBackend\services\admin_only\system_monitoring"
)

foreach ($dir in $serviceDirs) {
    if (!(Test-Path $dir)) {
        New-Item $dir -ItemType Directory -Force | Out-Null
        Write-Host "✓ Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "✓ Already exists: $dir" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "STEP 3: UPDATE API DIRECTORY STRUCTURE" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

$apiDirs = @(
    "$newBackend\api\routes",
    "$newBackend\api\middleware",
    "$newBackend\api\models"
)

foreach ($dir in $apiDirs) {
    if (!(Test-Path $dir)) {
        New-Item $dir -ItemType Directory -Force | Out-Null
        Write-Host "✓ Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "✓ Already exists: $dir" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "STEP 4: CREATE DIRECTORY STRUCTURE SUMMARY" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

Write-Host "Backend Directory Structure:" -ForegroundColor Yellow
Write-Host ""
tree /F $newBackend /A

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "RESTRUCTURING COMPLETE!" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Review the new backend structure" -ForegroundColor White
Write-Host "  2. Update import paths in admin_portal pages" -ForegroundColor White
Write-Host "  3. Split services into SHARED/ADMIN/USER" -ForegroundColor White
Write-Host "  4. Create API route separation (admin/user/shared)" -ForegroundColor White
Write-Host "  5. Test all functionality" -ForegroundColor White
Write-Host ""

Write-Host "To update import paths, run:" -ForegroundColor Yellow
Write-Host "  .\update_import_paths.ps1" -ForegroundColor Cyan
Write-Host ""
