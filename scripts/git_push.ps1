# PowerShell version of auto-git push
param(
  [string]$Branch = 'main',
  [string]$Message = 'chore: repo update'
)

git add -A
try { git commit -m $Message } catch { }
git branch -M $Branch
if (-not (git remote)) { Write-Host 'No git remote configured. Add remote with: git remote add origin <url>'; exit 0 }
git push -u origin $Branch
