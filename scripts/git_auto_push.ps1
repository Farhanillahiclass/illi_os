# ILLI OS - Automated Git Push Script
# Usage: .\git_auto_push.ps1 -Message "Your commit message" -Branch main
# Or use defaults with interactive prompt

param(
    [string]$Message = "",
    [string]$Branch = "main",
    [switch]$Force = $false
)

function Write-Status {
    param([string]$Text, [string]$Color = "Cyan")
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Text" -ForegroundColor $Color
}

function Write-Error-Status {
    param([string]$Text)
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Text" -ForegroundColor Red
}

Write-Status "╔════════════════════════════════════════╗" "Magenta"
Write-Status "║  ILLI OS v1.2.5 - Git Auto-Push      ║" "Magenta"
Write-Status "╚════════════════════════════════════════╝" "Magenta"
Write-Host ""

# Check if git is available
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error-Status "Git not found in PATH. Please install Git and try again."
    exit 1
}

# Get current directory
$CurrentDir = Get-Location
$RepoRoot = git rev-parse --show-toplevel 2>$null

if ($null -eq $RepoRoot) {
    Write-Error-Status "Not a git repository: $CurrentDir"
    exit 1
}

Set-Location $RepoRoot
Write-Status "Repository: $RepoRoot"

# Check git status
$Status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($Status)) {
    Write-Status "Repository is clean. No changes to commit." "Green"
    exit 0
}

Write-Status "Changes detected:" "Yellow"
Write-Host $Status
Write-Host ""

# Interactive message input if not provided
if ([string]::IsNullOrWhiteSpace($Message)) {
    Write-Status "Enter commit message (or press Enter for default):" "Cyan"
    $UserMessage = Read-Host "Message"
    
    if ([string]::IsNullOrWhiteSpace($UserMessage)) {
        $Message = "ILLI OS v1.2.5: Automated commit - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    } else {
        $Message = $UserMessage
    }
}

Write-Status "Commit Message: $Message"

# Stage all changes
Write-Status "Staging all changes..." "Cyan"
git add -A
$StageResult = $LASTEXITCODE
if ($StageResult -ne 0) {
    Write-Error-Status "Failed to stage changes"
    exit 1
}

# Commit
Write-Status "Committing changes..." "Cyan"
git commit -m $Message
$CommitResult = $LASTEXITCODE
if ($CommitResult -ne 0) {
    Write-Error-Status "Commit failed. Changes not staged?"
    exit 1
}

Write-Status "Commit successful!" "Green"

# Get current branch
$CurrentBranch = git rev-parse --abbrev-ref HEAD
Write-Status "Current branch: $CurrentBranch"

# Verify branch name
if ($CurrentBranch -ne $Branch) {
    Write-Status "Switching to branch: $Branch" "Yellow"
    git checkout $Branch -q
    $CheckoutResult = $LASTEXITCODE
    if ($CheckoutResult -ne 0) {
        Write-Error-Status "Failed to checkout branch: $Branch"
        exit 1
    }
}

# Pull latest from remote
Write-Status "Pulling latest changes from remote..." "Cyan"
git pull origin $Branch --quiet
$PullResult = $LASTEXITCODE
if ($PullResult -ne 0) {
    Write-Status "Pull returned a warning, continuing..." "Yellow"
}

# Push to remote
Write-Status "Pushing to remote repository..." "Cyan"
if ($Force) {
    git push origin $Branch --force
} else {
    git push origin $Branch
}

$PushResult = $LASTEXITCODE
if ($PushResult -eq 0) {
    Write-Status "✓ Push successful!" "Green"
    Write-Status "Repository is now synchronized with remote." "Green"
} else {
    Write-Error-Status "✗ Push failed. Check your network connection and permissions."
    Write-Status "You can retry with: git push origin $Branch"
    exit 1
}

Write-Host ""
Write-Status "╔════════════════════════════════════════╗" "Magenta"
Write-Status "║  Operation Complete                   ║" "Magenta"
Write-Status "╚════════════════════════════════════════╝" "Magenta"
