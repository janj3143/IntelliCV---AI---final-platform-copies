# Update Admin Portal Pages to Use Shared Backend
# This script updates import statements in admin portal pages

param(
    [switch]$DryRun
)

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "  Updating Admin Portal Pages for Shared Backend" -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

$rootPath = "c:\IntelliCV-AI\IntelliCV\BACKEND-ADMIN-REORIENTATION"
$adminPages = Join-Path $rootPath "admin_portal\pages"

# Pages that need updating
$pagesToUpdate = @(
    "06_Complete_Data_Parser.py",
    "08_AI_Enrichment.py",
    "20_Job_Title_AI_Integration.py",
    "23_AI_Model_Training_Review.py"
)

# Function to add shared_backend to sys.path if not already present
function Add-SharedBackendPath {
    param([string]$filePath)
    
    $content = Get-Content $filePath -Raw
    
    # Check if sys.path modification is already there
    if ($content -match "shared_backend") {
        Write-Host "  Already has shared_backend path: $filePath" -ForegroundColor Yellow
        return $false
    }
    
    # Find where to insert (after imports, before class/function definitions)
    $lines = Get-Content $filePath
    $insertIndex = 0
    
    for ($i = 0; $i -lt $lines.Length; $i++) {
        if ($lines[$i] -match "^import " -or $lines[$i] -match "^from ") {
            $insertIndex = $i + 1
        }
        if ($lines[$i] -match "^(class |def |st\.)" -and $insertIndex -gt 0) {
            break
        }
    }
    
    # Insert the path modification code
    $pathCode = @"

# Add shared_backend to Python path for backend services
import sys
from pathlib import Path
backend_path = Path(__file__).parent.parent.parent / "shared_backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

"@
    
    if ($DryRun) {
        Write-Host "  [DRY RUN] Would add shared_backend path at line $insertIndex in: $filePath" -ForegroundColor Yellow
        return $true
    }
    
    $newLines = @()
    $newLines += $lines[0..($insertIndex - 1)]
    $newLines += $pathCode.Split("`n")
    $newLines += $lines[$insertIndex..($lines.Length - 1)]
    
    Set-Content -Path $filePath -Value ($newLines -join "`n")
    Write-Host "  Added shared_backend path to: $filePath" -ForegroundColor Green
    return $true
}

# Function to update import statements
function Update-Imports {
    param(
        [string]$filePath,
        [hashtable]$replacements
    )
    
    $content = Get-Content $filePath -Raw
    $updated = $false
    
    foreach ($old in $replacements.Keys) {
        $new = $replacements[$old]
        if ($content -match [regex]::Escape($old)) {
            if ($DryRun) {
                Write-Host "  [DRY RUN] Would replace '$old' with '$new' in: $filePath" -ForegroundColor Yellow
            } else {
                $content = $content -replace [regex]::Escape($old), $new
                $updated = $true
            }
        }
    }
    
    if ($updated -and -not $DryRun) {
        Set-Content -Path $filePath -Value $content -NoNewline
        Write-Host "  Updated imports in: $filePath" -ForegroundColor Green
    }
    
    return $updated
}

# Import replacements for each page
$importReplacements = @{
    # AI services -> AI engines
    "from ai_services.hybrid_integrator import" = "from ai_engines.hybrid_integrator import"
    "from ai_services.neural_network_engine import" = "from ai_engines.neural_network_engine import"
    "from ai_services.expert_system_engine import" = "from ai_engines.expert_system_engine import"
    "from ai_services.feedback_loop_engine import" = "from ai_engines.feedback_loop_engine import"
    "from ai_services.model_trainer import" = "from ai_engines.model_trainer import"
    
    # Backend services -> services
    "from backend.services.enhanced_job_title_engine import" = "from services.enhanced_job_title_engine import"
    "from backend.services.unified_ai_engine import" = "from services.unified_ai_engine import"
    "from backend.services.linkedin_industry_classifier import" = "from services.linkedin_industry_classifier import"
    
    # Backend data management -> data_management
    "from backend.data_management.intellicv_data_manager import" = "from data_management.intellicv_data_manager import"
    "from backend.data_management.ai_data_manager import" = "from data_management.ai_data_manager import"
    "from backend.data_management.complete_data_parser import" = "from data_management.complete_data_parser import"
    
    # Backend utils -> utils
    "from backend.utils.logging_config import" = "from utils.logging_config import"
    "from backend.utils.exception_handler import" = "from utils.exception_handler import"
    
    # Class name fixes
    "UnifiedAIEngine" = "UnifiedIntelliCVAIEngine"
}

# Process each page
$updatedPages = 0
foreach ($page in $pagesToUpdate) {
    $pagePath = Join-Path $adminPages $page
    
    if (-not (Test-Path $pagePath)) {
        Write-Host "`nWARNING: Page not found: $page" -ForegroundColor Red
        continue
    }
    
    Write-Host "`nProcessing: $page" -ForegroundColor Cyan
    
    # Step 1: Add shared_backend to path
    $pathAdded = Add-SharedBackendPath -filePath $pagePath
    
    # Step 2: Update imports
    $importsUpdated = Update-Imports -filePath $pagePath -replacements $importReplacements
    
    if ($pathAdded -or $importsUpdated) {
        $updatedPages++
    }
}

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "  Update Complete!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan

if ($DryRun) {
    Write-Host "`n  This was a DRY RUN. No files were modified." -ForegroundColor Yellow
    Write-Host "  Run without -DryRun to apply changes.`n" -ForegroundColor Yellow
} else {
    Write-Host "`n  Updated $updatedPages pages to use shared_backend.`n" -ForegroundColor Green
    Write-Host "  Next steps:" -ForegroundColor Cyan
    Write-Host "    1. Test each updated page in admin portal" -ForegroundColor White
    Write-Host "    2. Verify imports work correctly" -ForegroundColor White
    Write-Host "    3. Test AI functionality on each page`n" -ForegroundColor White
}
