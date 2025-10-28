# PowerShell Script: Backend Tidy-Up & Synchronization
# This script will:
# 1. Cross-check BACKEND-ADMIN-REORIENTATION and Full system for required folders/files
# 2. Move non-essential, backup, zip, and miscellaneous files/folders from BACKEND-ADMIN-REORIENTATION to Sandbox Backup data - old
# 3. Synchronize missing essentials between Full system and BACKEND-ADMIN-REORIENTATION
# 4. Delete duplicated admin/user folders from Sandbox core, backup, and Full system

# --- CONFIGURE PATHS ---
$SANDBOX = "c:\IntelliCV-AI\IntelliCV\SANDBOX"
$FULL_SYSTEM = "$SANDBOX\Full system"
$BACKEND = "$SANDBOX\BACKEND-ADMIN-REORIENTATION"
$BACKUP = "$SANDBOX\Sandbox Backup data - old"

# --- GET ESSENTIALS FROM FULL SYSTEM ---
$essentials = Get-ChildItem $FULL_SYSTEM | Select-Object -ExpandProperty Name

# --- MOVE NON-ESSENTIALS FROM BACKEND TO BACKUP ---
$backend_items = Get-ChildItem $BACKEND | Where-Object { $_.Name -ne "admin_portal" -and $_.Name -ne "user_portal_final" -and $_.Name -ne "ai_data_final" }
foreach ($item in $backend_items) {
    if ($essentials -notcontains $item.Name -or $item.Name -match "backup|Backups|Backup|\.zip|\.bak|\.tar|\.gz|\.rar|\.7z|__pycache__|logs|benchmarks|examples|MIGRATION_LOGS|scripts|tests|Markdowns|Backup_old_redundant_files") {
        $src = $item.FullName
        $dst = Join-Path $BACKUP $item.Name
        Move-Item $src $dst -Force
    }
}

# --- SYNC MISSING ESSENTIALS FROM BACKEND TO FULL SYSTEM ---
foreach ($item in $essentials) {
    $src = Join-Path $BACKEND $item
    $dst = Join-Path $FULL_SYSTEM $item
    if ((Test-Path $src) -and (-not (Test-Path $dst))) {
        if ((Get-Item $src).PSIsContainer) {
            Copy-Item $src $FULL_SYSTEM -Recurse -Force
        } else {
            Copy-Item $src $FULL_SYSTEM -Force
        }
    }
}

# --- DELETE DUPLICATED ADMIN/USER FOLDERS FROM SANDBOX CORE, BACKUP, FULL SYSTEM ---
$dupFolders = @("admin_portal", "user_portal_final")
foreach ($folder in $dupFolders) {
    $core = Join-Path $SANDBOX $folder
    $backup = Join-Path $BACKUP $folder
    $full = Join-Path $FULL_SYSTEM $folder
    if (Test-Path $core) { Remove-Item $core -Recurse -Force }
    if (Test-Path $backup) { Remove-Item $backup -Recurse -Force }
    # Do not delete from Full system, as it is the canonical location
}

Write-Host "Backend tidy-up and synchronization complete."
