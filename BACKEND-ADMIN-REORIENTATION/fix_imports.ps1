# Fix imports in shared_backend to use new module names
# This script updates all import statements after restructuring

param(
    [switch]$DryRun
)

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "  Fixing Shared Backend Imports" -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

$rootPath = "c:\IntelliCV-AI\IntelliCV\BACKEND-ADMIN-REORIENTATION"
$sharedBackend = Join-Path $rootPath "shared_backend"

# Function to update imports in a file
function Update-Imports {
    param(
        [string]$filePath,
        [string]$oldPattern,
        [string]$newPattern
    )
    
    if (Test-Path $filePath) {
        $content = Get-Content $filePath -Raw
        $newContent = $content -replace $oldPattern, $newPattern
        
        if ($content -ne $newContent) {
            if ($DryRun) {
                Write-Host "  [DRY RUN] Would update: $filePath" -ForegroundColor Yellow
            } else {
                Set-Content -Path $filePath -Value $newContent -NoNewline
                Write-Host "  Updated: $filePath" -ForegroundColor Green
            }
            return $true
        }
    }
    return $false
}

# Step 1: Update ai_services -> ai_engines in shared_backend
Write-Host "Step 1: Updating ai_services imports to ai_engines..." -ForegroundColor Cyan
$updated = 0
Get-ChildItem -Path $sharedBackend -Filter "*.py" -Recurse | ForEach-Object {
    if (Update-Imports -filePath $_.FullName -oldPattern "from ai_services\." -newPattern "from ai_engines.") {
        $updated++
    }
    if (Update-Imports -filePath $_.FullName -oldPattern "import ai_services\." -newPattern "import ai_engines.") {
        $updated++
    }
}
Write-Host "  Updated $updated files`n" -ForegroundColor Green

# Step 2: Update relative imports to absolute in ai_engines
Write-Host "Step 2: Updating relative imports in ai_engines..." -ForegroundColor Cyan
$aiEnginesPath = Join-Path $sharedBackend "ai_engines"
$patterns = @{
    "from neural_network_engine import" = "from ai_engines.neural_network_engine import"
    "from expert_system_engine import" = "from ai_engines.expert_system_engine import"
    "from feedback_loop_engine import" = "from ai_engines.feedback_loop_engine import"
    "from model_trainer import" = "from ai_engines.model_trainer import"
    "from hybrid_integrator import" = "from ai_engines.hybrid_integrator import"
}

$updated = 0
Get-ChildItem -Path $aiEnginesPath -Filter "*.py" | ForEach-Object {
    foreach ($pattern in $patterns.Keys) {
        if (Update-Imports -filePath $_.FullName -oldPattern [regex]::Escape($pattern) -newPattern $patterns[$pattern]) {
            $updated++
        }
    }
}
Write-Host "  Updated $updated imports`n" -ForegroundColor Green

# Step 3: Update services imports
Write-Host "Step 3: Updating imports in services..." -ForegroundColor Cyan
$servicesPath = Join-Path $sharedBackend "services"
$updated = 0

# Update ai_services to ai_engines in services
Get-ChildItem -Path $servicesPath -Filter "*.py" | ForEach-Object {
    if (Update-Imports -filePath $_.FullName -oldPattern "from ai_services\." -newPattern "from ai_engines.") {
        $updated++
    }
    
    # Update backend.services to just services
    if (Update-Imports -filePath $_.FullName -oldPattern "from backend\.services\." -newPattern "from services.") {
        $updated++
    }
    
    # Update backend.data_management to just data_management
    if (Update-Imports -filePath $_.FullName -oldPattern "from backend\.data_management\." -newPattern "from data_management.") {
        $updated++
    }
}
Write-Host "  Updated $updated imports`n" -ForegroundColor Green

# Step 4: Update data_management imports
Write-Host "Step 4: Updating imports in data_management..." -ForegroundColor Cyan
$dataPath = Join-Path $sharedBackend "data_management"
$updated = 0

Get-ChildItem -Path $dataPath -Filter "*.py" | ForEach-Object {
    # Update backend.utils to just utils
    if (Update-Imports -filePath $_.FullName -oldPattern "from backend\.utils\." -newPattern "from utils.") {
        $updated++
    }
    
    # Update backend.data_management to just data_management
    if (Update-Imports -filePath $_.FullName -oldPattern "from backend\.data_management\." -newPattern "from data_management.") {
        $updated++
    }
}
Write-Host "  Updated $updated imports`n" -ForegroundColor Green

# Step 5: Update API imports
Write-Host "Step 5: Updating imports in API..." -ForegroundColor Cyan
$apiPath = Join-Path $sharedBackend "api"
$mainPy = Join-Path $apiPath "main.py"
$updated = 0

if (Update-Imports -filePath $mainPy -oldPattern "from ai_services\." -newPattern "from ai_engines.") {
    $updated++
}
if (Update-Imports -filePath $mainPy -oldPattern "from backend\.services\." -newPattern "from services.") {
    $updated++
}
if (Update-Imports -filePath $mainPy -oldPattern "from backend\.data_management\." -newPattern "from data_management.") {
    $updated++
}
if (Update-Imports -filePath $mainPy -oldPattern "from backend\.utils\." -newPattern "from utils.") {
    $updated++
}
Write-Host "  Updated $updated imports`n" -ForegroundColor Green

# Step 6: Update tests
Write-Host "Step 6: Updating imports in tests..." -ForegroundColor Cyan
$testsPath = Join-Path $sharedBackend "tests"
$updated = 0

Get-ChildItem -Path $testsPath -Filter "*.py" | ForEach-Object {
    if (Update-Imports -filePath $_.FullName -oldPattern "from ai_services\." -newPattern "from ai_engines.") {
        $updated++
    }
    if (Update-Imports -filePath $_.FullName -oldPattern "from backend\.services\." -newPattern "from services.") {
        $updated++
    }
}
Write-Host "  Updated $updated imports`n" -ForegroundColor Green

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "  Import Fix Complete!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan

if ($DryRun) {
    Write-Host "`n  This was a DRY RUN. No files were modified." -ForegroundColor Yellow
    Write-Host "  Run without -DryRun to apply changes.`n" -ForegroundColor Yellow
} else {
    Write-Host "`n  All imports have been updated for the new structure.`n" -ForegroundColor Green
    Write-Host "  Run test_shared_backend.ps1 again to verify.`n" -ForegroundColor Cyan
}
