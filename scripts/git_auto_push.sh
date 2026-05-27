#!/bin/bash
# ILLI OS - Automated Git Push Script (Bash)
# Usage: ./git_auto_push.sh "Your commit message" [branch_name] [--force]

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Functions
status_msg() {
    echo -e "${CYAN}[$(date +'%H:%M:%S')] $1${NC}"
}

error_msg() {
    echo -e "${RED}[$(date +'%H:%M:%S')] $1${NC}"
}

success_msg() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] $1${NC}"
}

warning_msg() {
    echo -e "${YELLOW}[$(date +'%H:%M:%S')] $1${NC}"
}

# Parse arguments
MESSAGE="${1:-}"
BRANCH="${2:-main}"
FORCE_FLAG=false

if [[ "$1" == "--force" ]] || [[ "$2" == "--force" ]] || [[ "$3" == "--force" ]]; then
    FORCE_FLAG=true
fi

# Print header
echo -e "${MAGENTA}╔════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║  ILLI OS v1.2.5 - Git Auto-Push      ║${NC}"
echo -e "${MAGENTA}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if git is available
if ! command -v git &> /dev/null; then
    error_msg "Git not found. Please install Git and try again."
    exit 1
fi

# Get repository root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
if [ -z "$REPO_ROOT" ]; then
    error_msg "Not a git repository: $(pwd)"
    exit 1
fi

cd "$REPO_ROOT"
status_msg "Repository: $REPO_ROOT"

# Check git status
STATUS=$(git status --porcelain)
if [ -z "$STATUS" ]; then
    success_msg "Repository is clean. No changes to commit."
    exit 0
fi

warning_msg "Changes detected:"
echo "$STATUS"
echo ""

# Get or prompt for commit message
if [ -z "$MESSAGE" ]; then
    status_msg "Enter commit message (press Enter for default):"
    read -p "> " MESSAGE
    
    if [ -z "$MESSAGE" ]; then
        MESSAGE="ILLI OS v1.2.5: Automated commit - $(date +'%Y-%m-%d %H:%M:%S')"
    fi
fi

status_msg "Commit Message: $MESSAGE"
echo ""

# Stage all changes
status_msg "Staging all changes..."
if ! git add -A; then
    error_msg "Failed to stage changes"
    exit 1
fi

# Commit
status_msg "Committing changes..."
if ! git commit -m "$MESSAGE"; then
    error_msg "Commit failed. Changes not staged?"
    exit 1
fi

success_msg "Commit successful!"
echo ""

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
status_msg "Current branch: $CURRENT_BRANCH"

# Verify branch name
if [ "$CURRENT_BRANCH" != "$BRANCH" ]; then
    warning_msg "Switching to branch: $BRANCH"
    if ! git checkout "$BRANCH" -q; then
        error_msg "Failed to checkout branch: $BRANCH"
        exit 1
    fi
fi

# Pull latest from remote
status_msg "Pulling latest changes from remote..."
if ! git pull origin "$BRANCH" --quiet 2>/dev/null; then
    warning_msg "Pull returned a warning, continuing..."
fi

# Push to remote
status_msg "Pushing to remote repository..."
if [ "$FORCE_FLAG" = true ]; then
    if git push origin "$BRANCH" --force; then
        success_msg "✓ Push successful (force)!"
    else
        error_msg "✗ Push failed (force)"
        status_msg "Retry with: git push origin $BRANCH --force"
        exit 1
    fi
else
    if git push origin "$BRANCH"; then
        success_msg "✓ Push successful!"
    else
        error_msg "✗ Push failed. Check your network connection and permissions."
        status_msg "Retry with: git push origin $BRANCH"
        exit 1
    fi
fi

success_msg "Repository is now synchronized with remote."
echo ""

echo -e "${MAGENTA}╔════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║  Operation Complete                   ║${NC}"
echo -e "${MAGENTA}╚════════════════════════════════════════╝${NC}"
