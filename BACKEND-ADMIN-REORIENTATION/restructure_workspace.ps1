# ============================================================================
# IntelliCV Backend-Admin Restructuring Script  
# ============================================================================
# Purpose: Restructure workspace to separate shared backend from admin portal
# Date: October 15, 2025
# ============================================================================

param(
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Stop"

function Write-Success { param($msg) Write-Host "OK $msg" -ForegroundColor Green }
function Write-Info { param($msg) Write-Host "INFO $msg" -ForegroundColor Cyan }
function Write-Warning { param($msg) Write-Host "WARN $msg" -ForegroundColor Yellow }
function Write-Step { param($msg) Write-Host "`n>> $msg" -ForegroundColor Magenta }

# Configuration
$rootPath = "C:\IntelliCV-AI\IntelliCV\BACKEND-ADMIN-REORIENTATION"
$adminPortalPath = "$rootPath\admin_portal"
$sharedBackendPath = "$rootPath\shared_backend"
$userPortalPath = "$rootPath\user_portal"

Write-Host "`n================================================================" -ForegroundColor Yellow
Write-Host "  IntelliCV Backend-Admin Restructuring Script" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Yellow

if ($DryRun) {
    Write-Warning "DRY RUN MODE - No actual changes will be made"
}

# ============================================================================
# STEP 1: Create New Directory Structure
# ============================================================================

Write-Step "STEP 1: Creating new directory structure"

$directories = @(
    "$sharedBackendPath\api",
    "$sharedBackendPath\services",
    "$sharedBackendPath\ai_engines",
    "$sharedBackendPath\data_management",
    "$sharedBackendPath\utils",
    "$sharedBackendPath\config",
    "$sharedBackendPath\tests",
    "$sharedBackendPath\logs",
    "$sharedBackendPath\data\models",
    "$sharedBackendPath\data\rules",
    "$sharedBackendPath\data\feedback",
    "$adminPortalPath\pages\admin_only",
    "$adminPortalPath\pages\shared_interfaces",
    "$userPortalPath\pages",
    "$userPortalPath\components"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        if (-not $DryRun) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Success "Created: $dir"
        } else {
            Write-Info "Would create: $dir"
        }
    } else {
        Write-Info "Already exists: $dir"
    }
}

# ============================================================================
# STEP 2: Move Backend AI Services
# ============================================================================

Write-Step "STEP 2: Moving backend AI services to shared_backend/ai_engines"

$aiServices = @(
    "hybrid_integrator.py",
    "neural_network_engine.py",
    "expert_system_engine.py",
    "feedback_loop_engine.py",
    "model_trainer.py"
)

$sourceAI = "$adminPortalPath\backend\ai_services"
$destAI = "$sharedBackendPath\ai_engines"

if (Test-Path $sourceAI) {
    foreach ($file in $aiServices) {
        $source = "$sourceAI\$file"
        $dest = "$destAI\$file"
        
        if (Test-Path $source) {
            if (-not $DryRun) {
                Copy-Item $source $dest -Force
                Write-Success "Copied: $file"
            } else {
                Write-Info "Would copy: $file"
            }
        }
    }
}

# ============================================================================
# STEP 3: Move REST API
# ============================================================================

Write-Step "STEP 3: Moving REST API to shared_backend/api"

$apiFiles = @("main.py", "requirements.txt", "README.md")
$sourceAPI = "$adminPortalPath\backend\api"
$destAPI = "$sharedBackendPath\api"

if (Test-Path $sourceAPI) {
    foreach ($file in $apiFiles) {
        $source = "$sourceAPI\$file"
        $dest = "$destAPI\$file"
        
        if (Test-Path $source) {
            if (-not $DryRun) {
                Copy-Item $source $dest -Force
                Write-Success "Copied: $file"
            } else {
                Write-Info "Would copy: $file"
            }
        }
    }
}

# ============================================================================
# STEP 4: Move Data Management Services
# ============================================================================

Write-Step "STEP 4: Moving data management services"

$dataServices = @(
    "intellicv_data_manager.py",
    "ai_data_manager.py",
    "complete_data_parser.py"
)

$sourceServices = "$adminPortalPath\services"
$destDataMgmt = "$sharedBackendPath\data_management"

foreach ($file in $dataServices) {
    $source = "$sourceServices\$file"
    $dest = "$destDataMgmt\$file"
    
    if (Test-Path $source) {
        if (-not $DryRun) {
            Copy-Item $source $dest -Force
            Write-Success "Copied: $file"
        } else {
            Write-Info "Would copy: $file"
        }
    }
}

# ============================================================================
# STEP 5: Move Shared AI Services
# ============================================================================

Write-Step "STEP 5: Moving shared AI services"

$sharedServices = @(
    "enhanced_job_title_engine.py",
    "linkedin_industry_classifier.py",
    "unified_ai_engine.py"
)

$destServices = "$sharedBackendPath\services"

foreach ($file in $sharedServices) {
    $source = "$sourceServices\$file"
    $dest = "$destServices\$file"
    
    if (Test-Path $source) {
        if (-not $DryRun) {
            Copy-Item $source $dest -Force
            Write-Success "Copied: $file"
        } else {
            Write-Info "Would copy: $file"
        }
    }
}

# ============================================================================
# STEP 6: Move Shared Utils
# ============================================================================

Write-Step "STEP 6: Moving shared utilities"

$utilFiles = @("logging_config.py", "exception_handler.py")
$sourceUtils = "$adminPortalPath\utils"
$destUtils = "$sharedBackendPath\utils"

foreach ($file in $utilFiles) {
    $source = "$sourceUtils\$file"
    $dest = "$destUtils\$file"
    
    if (Test-Path $source) {
        if (-not $DryRun) {
            Copy-Item $source $dest -Force
            Write-Success "Copied: $file"
        } else {
            Write-Info "Would copy: $file"
        }
    }
}

# ============================================================================
# STEP 7: Move Tests
# ============================================================================

Write-Step "STEP 7: Moving tests"

$testFiles = @("test_hybrid_ai.py")
$sourceTests = "$adminPortalPath\backend\tests"
$destTests = "$sharedBackendPath\tests"

if (Test-Path $sourceTests) {
    foreach ($file in $testFiles) {
        $source = "$sourceTests\$file"
        $dest = "$destTests\$file"
        
        if (Test-Path $source) {
            if (-not $DryRun) {
                Copy-Item $source $dest -Force
                Write-Success "Copied: $file"
            } else {
                Write-Info "Would copy: $file"
            }
        }
    }
}

# ============================================================================
# STEP 8: Create Init Files
# ============================================================================

Write-Step "STEP 8: Creating __init__.py files"

$initDirs = @(
    "$sharedBackendPath",
    "$sharedBackendPath\api",
    "$sharedBackendPath\services",
    "$sharedBackendPath\ai_engines",
    "$sharedBackendPath\data_management",
    "$sharedBackendPath\utils",
    "$sharedBackendPath\tests"
)

foreach ($dir in $initDirs) {
    $initFile = "$dir\__init__.py"
    if (-not (Test-Path $initFile)) {
        if (-not $DryRun) {
            "" | Out-File -FilePath $initFile -Encoding UTF8
            Write-Success "Created: __init__.py in $(Split-Path $dir -Leaf)"
        } else {
            Write-Info "Would create: __init__.py in $(Split-Path $dir -Leaf)"
        }
    }
}

# ============================================================================
# Summary
# ============================================================================

Write-Host "`n================================================================" -ForegroundColor Green
Write-Host "  RESTRUCTURING COMPLETE!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green

Write-Host "`nNew Structure Created:" -ForegroundColor Cyan
Write-Host "  shared_backend/       - Shared services for admin & user"
Write-Host "    - api/              - REST API server"
Write-Host "    - ai_engines/       - 7 AI engines"
Write-Host "    - services/         - Business logic"
Write-Host "    - data_management/  - Data processing"
Write-Host "  admin_portal/         - Admin interface"
Write-Host "  user_portal/          - User interface (future)"

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Review the new structure"
Write-Host "  2. Update import paths in pages"
Write-Host "  3. Test backend integration"

if ($DryRun) {
    Write-Host "`nThis was a DRY RUN - no actual changes were made" -ForegroundColor Yellow
    Write-Host "Run without -DryRun to apply changes" -ForegroundColor Yellow
}

Write-Host ""
