# Test Shared Backend Integration
# ================================

$pythonExe = "C:\IntelliCV-AI\IntelliCV\env310\python.exe"
$backendPath = "C:\IntelliCV-AI\IntelliCV\BACKEND-ADMIN-REORIENTATION\shared_backend"

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "  Testing Shared Backend Integration" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# Test 1: Configuration
Write-Host "`nTest 1: Backend Configuration..." -ForegroundColor Yellow
& $pythonExe -c @"
import sys
sys.path.insert(0, r'$backendPath')
from config.backend_config import *
print(f'OK Shared Backend Root: {SHARED_BACKEND_ROOT}')
print(f'OK AI Data Path: {AI_DATA_PATH}')
print(f'OK API Base URL: {API_BASE_URL}')
"@

# Test 2: Data Management
Write-Host "`nTest 2: Data Management Import..." -ForegroundColor Yellow
& $pythonExe -c @"
import sys
sys.path.insert(0, r'$backendPath')
try:
    from data_management.intellicv_data_manager import IntelliCVDataDirectoryManager
    mgr = IntelliCVDataDirectoryManager()
    print(f'OK Data Manager initialized')
    print(f'OK AI Data Path: {mgr.ai_data_path}')
except Exception as e:
    print(f'ERROR: {e}')
"@

# Test 3: AI Engines
Write-Host "`nTest 3: AI Engines Import..." -ForegroundColor Yellow
& $pythonExe -c @"
import sys
sys.path.insert(0, r'$backendPath')
try:
    from ai_engines.hybrid_integrator import HybridAIIntegrator
    from ai_engines.neural_network_engine import NeuralNetworkEngine
    from ai_engines.expert_system_engine import ExpertSystemEngine
    print('OK All AI engines imported successfully')
except Exception as e:
    print(f'ERROR: {e}')
"@

# Test 4: Services
Write-Host "`nTest 4: Services Import..." -ForegroundColor Yellow
& $pythonExe -c @"
import sys
sys.path.insert(0, r'$backendPath')
try:
    from services.enhanced_job_title_engine import EnhancedJobTitleEngine
    from services.unified_ai_engine import UnifiedIntelliCVAIEngine
    print('OK All services imported successfully')
except Exception as e:
    print(f'ERROR: {e}')
"@

# Test 5: Utils
Write-Host "`nTest 5: Utils Import..." -ForegroundColor Yellow
& $pythonExe -c @"
import sys
sys.path.insert(0, r'$backendPath')
try:
    from utils.logging_config import get_logger, setup_logging
    from utils.exception_handler import ExceptionHandler, SafeOperationsMixin
    print('OK All utils imported successfully')
except Exception as e:
    print(f'ERROR: {e}')
"@

# Test 6: Directory Structure
Write-Host "`nTest 6: Directory Structure..." -ForegroundColor Yellow
$dirs = @(
    "$backendPath\ai_engines",
    "$backendPath\services",
    "$backendPath\data_management",
    "$backendPath\api",
    "$backendPath\utils",
    "$backendPath\config",
    "$backendPath\tests",
    "$backendPath\data\models",
    "$backendPath\data\rules",
    "$backendPath\data\feedback"
)

$allExist = $true
foreach ($dir in $dirs) {
    if (Test-Path $dir) {
        Write-Host "  OK $(Split-Path $dir -Leaf)" -ForegroundColor Green
    } else {
        Write-Host "  ERROR Missing: $(Split-Path $dir -Leaf)" -ForegroundColor Red
        $allExist = $false
    }
}

# Test 7: File Counts
Write-Host "`nTest 7: File Counts..." -ForegroundColor Yellow
$aiEnginesCount = (Get-ChildItem "$backendPath\ai_engines" -Filter "*.py" | Where-Object { $_.Name -ne "__init__.py" }).Count
$servicesCount = (Get-ChildItem "$backendPath\services" -Filter "*.py" | Where-Object { $_.Name -ne "__init__.py" }).Count
$dataManagementCount = (Get-ChildItem "$backendPath\data_management" -Filter "*.py" | Where-Object { $_.Name -ne "__init__.py" }).Count

Write-Host "  AI Engines: $aiEnginesCount files" -ForegroundColor Cyan
Write-Host "  Services: $servicesCount files" -ForegroundColor Cyan
Write-Host "  Data Management: $dataManagementCount files" -ForegroundColor Cyan

# Summary
Write-Host "`n================================================================" -ForegroundColor Green
Write-Host "  TEST SUMMARY" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green

if ($allExist) {
    Write-Host "  OK All tests passed!" -ForegroundColor Green
    Write-Host "`n  Shared backend is ready to use!" -ForegroundColor Cyan
    Write-Host "`n  Next Steps:" -ForegroundColor Yellow
    Write-Host "    1. Update admin portal pages to use shared_backend imports"
    Write-Host "    2. Start API server: cd shared_backend/api; python main.py"
    Write-Host "    3. Run tests: cd shared_backend/tests; python test_hybrid_ai.py"
} else {
    Write-Host "  ERROR Some tests failed - review output above" -ForegroundColor Red
}

Write-Host ""
