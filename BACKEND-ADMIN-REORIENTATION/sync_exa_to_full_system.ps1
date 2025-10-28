# ============================================================================
# Exa Integration Sync Script
# ============================================================================
# Copies Exa integration files from BACKEND-ADMIN-REORIENTATION to Full system
# Date: October 28, 2025
# ============================================================================

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "           EXA INTEGRATION - CROSS-PLATFORM SYNC                       " -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Paths
$source = "c:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION"
$dest = "c:\IntelliCV-AI\IntelliCV\SANDBOX\Full system"

# Track operations
$copied = 0
$skipped = 0
$errors = 0

# ============================================================================
# PHASE 1: Exa Service Files (shared_backend/services/exa_service/)
# ============================================================================

Write-Host "📦 PHASE 1: Exa Service Files" -ForegroundColor Yellow
Write-Host ""

$exaServiceDest = Join-Path $dest "shared_backend\services\exa_service"
if (!(Test-Path $exaServiceDest)) {
    New-Item -ItemType Directory -Path $exaServiceDest -Force | Out-Null
    Write-Host "  ✓ Created directory: shared_backend/services/exa_service" -ForegroundColor Green
}

$exaFiles = @(
    "shared_backend\services\exa_service\__init__.py",
    "shared_backend\services\exa_service\exa_client.py",
    "shared_backend\services\exa_service\company_enrichment.py",
    "shared_backend\services\exa_service\keyword_extractor.py",
    "shared_backend\services\exa_service\smart_search_orchestrator.py"
)

foreach ($file in $exaFiles) {
    $srcFile = Join-Path $source $file
    $destFile = Join-Path $dest $file
    
    if (Test-Path $srcFile) {
        try {
            # Ensure destination directory exists
            $destDir = Split-Path $destFile -Parent
            if (!(Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            
            Copy-Item -Path $srcFile -Destination $destFile -Force
            Write-Host "  ✓ Copied: $(Split-Path $file -Leaf)" -ForegroundColor Green
            $copied++
        } catch {
            Write-Host "  ✗ Failed: $(Split-Path $file -Leaf) - $($_.Exception.Message)" -ForegroundColor Red
            $errors++
        }
    } else {
        Write-Host "  ⊘ Not found: $(Split-Path $file -Leaf)" -ForegroundColor Yellow
        $skipped++
    }
}

Write-Host ""

# ============================================================================
# PHASE 2: Database Schemas (shared_backend/database/schemas/)
# ============================================================================

Write-Host "📦 PHASE 2: Database Schemas" -ForegroundColor Yellow
Write-Host ""

$schemaDest = Join-Path $dest "shared_backend\database\schemas"
if (!(Test-Path $schemaDest)) {
    New-Item -ItemType Directory -Path $schemaDest -Force | Out-Null
    Write-Host "  ✓ Created directory: shared_backend/database/schemas" -ForegroundColor Green
}

$schemaFiles = @(
    "shared_backend\database\schemas\exa_schema.sql"
)

foreach ($file in $schemaFiles) {
    $srcFile = Join-Path $source $file
    $destFile = Join-Path $dest $file
    
    if (Test-Path $srcFile) {
        try {
            $destDir = Split-Path $destFile -Parent
            if (!(Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            
            Copy-Item -Path $srcFile -Destination $destFile -Force
            Write-Host "  ✓ Copied: $(Split-Path $file -Leaf)" -ForegroundColor Green
            $copied++
        } catch {
            Write-Host "  ✗ Failed: $(Split-Path $file -Leaf) - $($_.Exception.Message)" -ForegroundColor Red
            $errors++
        }
    } else {
        Write-Host "  ⊘ Not found: $(Split-Path $file -Leaf)" -ForegroundColor Yellow
        $skipped++
    }
}

Write-Host ""

# ============================================================================
# PHASE 3: Database Connectors (shared_backend/database/)
# ============================================================================

Write-Host "📦 PHASE 3: Database Connectors" -ForegroundColor Yellow
Write-Host ""

$dbFiles = @(
    "shared_backend\database\exa_db.py"
)

foreach ($file in $dbFiles) {
    $srcFile = Join-Path $source $file
    $destFile = Join-Path $dest $file
    
    if (Test-Path $srcFile) {
        try {
            $destDir = Split-Path $destFile -Parent
            if (!(Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            
            Copy-Item -Path $srcFile -Destination $destFile -Force
            Write-Host "  ✓ Copied: $(Split-Path $file -Leaf)" -ForegroundColor Green
            $copied++
        } catch {
            Write-Host "  ✗ Failed: $(Split-Path $file -Leaf) - $($_.Exception.Message)" -ForegroundColor Red
            $errors++
        }
    } else {
        Write-Host "  ⊘ Not found: $(Split-Path $file -Leaf)" -ForegroundColor Yellow
        $skipped++
    }
}

Write-Host ""

# ============================================================================
# PHASE 4: Workers and Queue System (shared_backend/)
# ============================================================================

Write-Host "📦 PHASE 4: Background Workers & Queues" -ForegroundColor Yellow
Write-Host ""

$workerFiles = @(
    "shared_backend\workers\exa_worker.py",
    "shared_backend\queue\exa_queue.py"
)

foreach ($file in $workerFiles) {
    $srcFile = Join-Path $source $file
    $destFile = Join-Path $dest $file
    
    if (Test-Path $srcFile) {
        try {
            $destDir = Split-Path $destFile -Parent
            if (!(Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            
            Copy-Item -Path $srcFile -Destination $destFile -Force
            Write-Host "  ✓ Copied: $(Split-Path $file -Leaf)" -ForegroundColor Green
            $copied++
        } catch {
            Write-Host "  ✗ Failed: $(Split-Path $file -Leaf) - $($_.Exception.Message)" -ForegroundColor Red
            $errors++
        }
    } else {
        Write-Host "  ⊘ Not found: $(Split-Path $file -Leaf)" -ForegroundColor Yellow
        $skipped++
    }
}

Write-Host ""

# ============================================================================
# PHASE 5: Admin Portal Page (admin_portal/pages/)
# ============================================================================

Write-Host "📦 PHASE 5: Admin Portal Page 27" -ForegroundColor Yellow
Write-Host ""

$adminFiles = @(
    "admin_portal\pages\27_Exa_Web_Intelligence.py"
)

foreach ($file in $adminFiles) {
    $srcFile = Join-Path $source $file
    $destFile = Join-Path $dest $file
    
    if (Test-Path $srcFile) {
        try {
            $destDir = Split-Path $destFile -Parent
            if (!(Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            
            Copy-Item -Path $srcFile -Destination $destFile -Force
            Write-Host "  ✓ Copied: $(Split-Path $file -Leaf)" -ForegroundColor Green
            $copied++
        } catch {
            Write-Host "  ✗ Failed: $(Split-Path $file -Leaf) - $($_.Exception.Message)" -ForegroundColor Red
            $errors++
        }
    } else {
        Write-Host "  ⊘ Not found: $(Split-Path $file -Leaf)" -ForegroundColor Yellow
        $skipped++
    }
}

Write-Host ""

# ============================================================================
# PHASE 6: Test Files
# ============================================================================

Write-Host "📦 PHASE 6: Test Suites" -ForegroundColor Yellow
Write-Host ""

$testFiles = @(
    "test_exa_integration.py",
    "test_jd_keyword_search.py"
)

foreach ($file in $testFiles) {
    $srcFile = Join-Path $source $file
    $destFile = Join-Path $dest $file
    
    if (Test-Path $srcFile) {
        try {
            Copy-Item -Path $srcFile -Destination $destFile -Force
            Write-Host "  ✓ Copied: $file" -ForegroundColor Green
            $copied++
        } catch {
            Write-Host "  ✗ Failed: $file - $($_.Exception.Message)" -ForegroundColor Red
            $errors++
        }
    } else {
        Write-Host "  ⊘ Not found: $file" -ForegroundColor Yellow
        $skipped++
    }
}

Write-Host ""

# ============================================================================
# PHASE 7: Documentation
# ============================================================================

Write-Host "📦 PHASE 7: Documentation Files" -ForegroundColor Yellow
Write-Host ""

$docFiles = @(
    "EXA_DEEP_WEB_INTEGRATION_PLAN.md",
    "PHASE_1_FOUNDATION_COMPLETE.md",
    "PHASES_1_TO_5_COMPLETE.md",
    "EXA_COST_OPTIMIZATION_GUIDE.md",
    "TWO_TIER_SEARCH_QUICK_REFERENCE.md",
    "JD_KEYWORD_EXTRACTION_GUIDE.md",
    "JD_KEYWORD_ARCHITECTURE.md",
    "JD_FOCUSED_IMPLEMENTATION_SUMMARY.md"
)

foreach ($file in $docFiles) {
    $srcFile = Join-Path $source $file
    $destFile = Join-Path $dest $file
    
    if (Test-Path $srcFile) {
        try {
            Copy-Item -Path $srcFile -Destination $destFile -Force
            Write-Host "  ✓ Copied: $file" -ForegroundColor Green
            $copied++
        } catch {
            Write-Host "  ✗ Failed: $file - $($_.Exception.Message)" -ForegroundColor Red
            $errors++
        }
    } else {
        Write-Host "  ⊘ Not found: $file" -ForegroundColor Yellow
        $skipped++
    }
}

Write-Host ""

# ============================================================================
# PHASE 8: Environment Configuration
# ============================================================================

Write-Host "📦 PHASE 8: Environment Configuration" -ForegroundColor Yellow
Write-Host ""

# Copy .env template (don't overwrite if exists)
$srcEnv = Join-Path $source ".env"
$destEnv = Join-Path $dest ".env.exa_template"

if (Test-Path $srcEnv) {
    try {
        Copy-Item -Path $srcEnv -Destination $destEnv -Force
        Write-Host "  ✓ Copied: .env → .env.exa_template (template)" -ForegroundColor Green
        Write-Host "    Note: Merge with existing .env manually" -ForegroundColor Yellow
        $copied++
    } catch {
        Write-Host "  ✗ Failed: .env template - $($_.Exception.Message)" -ForegroundColor Red
        $errors++
    }
} else {
    Write-Host "  ⊘ Not found: .env" -ForegroundColor Yellow
    $skipped++
}

Write-Host ""

# ============================================================================
# SUMMARY
# ============================================================================

Write-Host "═══════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                        SYNC COMPLETE!                                 " -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Summary:" -ForegroundColor Yellow
Write-Host "  ✓ Files copied:  $copied" -ForegroundColor Green
Write-Host "  ⊘ Files skipped: $skipped" -ForegroundColor Yellow
Write-Host "  ✗ Errors:        $errors" -ForegroundColor $(if ($errors -gt 0) { "Red" } else { "Green" })
Write-Host ""
Write-Host "📁 Destination: $dest" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Review .env.exa_template and merge with existing .env" -ForegroundColor White
Write-Host "  2. Install dependencies: pip install exa-py spacy openai" -ForegroundColor White
Write-Host "  3. Run database schema: psql < shared_backend/database/schemas/exa_schema.sql" -ForegroundColor White
Write-Host "  4. Test integration: python test_exa_integration.py" -ForegroundColor White
Write-Host ""

# Return summary object
return @{
    Copied = $copied
    Skipped = $skipped
    Errors = $errors
    SourcePath = $source
    DestinationPath = $dest
}
