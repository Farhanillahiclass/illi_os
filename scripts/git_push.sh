#!/bin/bash
# Safe auto-git push script
set -e
BRANCH=${1:-main}
MSG=${2:-"chore: repo update"}

git add -A
git commit -m "$MSG" || true
git branch -M $BRANCH || true
if [ -z "$(git remote)" ]; then
  echo "No git remote configured. Add remote with: git remote add origin <url>"
  exit 0
fi
git push -u origin $BRANCH
