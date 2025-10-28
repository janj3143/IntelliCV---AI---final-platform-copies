# PowerShell Script: IntelliCV Platform Tidy-Up & Data Transfer
# This script will:
# 1. Copy all essential platform files/folders into Full system
# 2. Move excess/legacy files/folders into Sandbox Backup data - old
# 3. Leave Full system clean and runnable

# --- CONFIGURE PATHS ---
$SANDBOX = "c:\IntelliCV-AI\IntelliCV\SANDBOX"
$FULL_SYSTEM = "$SANDBOX\Full system"
$BACKUP = "$SANDBOX\Sandbox Backup data - old"

# --- ESSENTIALS ---
$essentials = @(
    "admin_portal",
    "user_portal_final",
    "ai_data_final",
    "backend",
    "api",
    "services",
    "modules",
    "components",
    "utilities",
    "utils",
    "shared",
    "config",
    "data",
    "db",
    "monitoring",
    "nginx",
    "static",
    "logs",
    "docs",
    "fragments",
    "pgadmin",
    "redis",
    ".vscode",
    "__pycache__",
    ".gitignore",
    "requirements.txt",
    "Dockerfile",
    "docker-compose.yml"
)

# --- COPY ESSENTIALS TO FULL SYSTEM ---
foreach ($item in $essentials) {
    $src = Join-Path $SANDBOX $item
    $dst = Join-Path $FULL_SYSTEM $item
    if (Test-Path $src) {
        if ((Get-Item $src).PSIsContainer) {
            Copy-Item $src $FULL_SYSTEM -Recurse -Force
        } else {
            Copy-Item $src $FULL_SYSTEM -Force
        }
    }
}

# --- IDENTIFY & MOVE EXCESS FILES/FOLDERS ---
$excess = Get-ChildItem $SANDBOX | Where-Object {
    $essentials -notcontains $_.Name -and $_.Name -ne "Full system" -and $_.Name -ne "Sandbox Backup data - old"
}
foreach ($item in $excess) {
    $src = $item.FullName
    $dst = Join-Path $BACKUP $item.Name
    Move-Item $src $dst -Force
}

Write-Host "IntelliCV platform tidy-up and data transfer complete."
