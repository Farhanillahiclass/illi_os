# 🚀 GITHUB SETUP GUIDE - ILLI

## Quick Setup (2 minutes) - For ILLI OS

### Step 1: Create GitHub Repository

1. Go to **https://github.com/new**
2. Fill in the following:
   - **Repository name**: `illi_os` (or your preferred name)
   - **Description**: "ILLI OS v1.2.5 - Local offline desktop AI agent with Ghost-Protocol HUD"
   - **Visibility**: Choose **Public** or **Private** as you prefer (Private is recommended for initial development)
   - **Initialize with**: Leave unchecked (we already have files)
3. Click **"Create repository"**

### Step 2: Connect Local Repository to GitHub

After creating the repo on GitHub, you'll see a page with setup instructions. Copy your repository URL (looks like `https://github.com/YOUR_USERNAME/illi_os.git`).

In your terminal, run:
```powershell
```bash
cd "C:\Users\Muhammad Anas\f_illi"

# Add GitHub as remote origin
git remote add origin https://github.com/YOUR_USERNAME/illi_os.git

# Rename branch to main (if needed)
git branch -M main

# Push initial commit
git push -u origin main --force # Use --force only if you're sure you want to overwrite remote history
```

### Step 3: Verify Push

Check on GitHub that your repository now contains all the ILLI OS files.

---

## Using Automated Git Push Script

After your first setup, use the automated push script for easy commits:

### PowerShell (Windows):

```powershell
# Make script executable
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run with default message
.\scripts\git_auto_push.ps1

# Run with custom message
.\scripts\git_auto_push.ps1 -Message "Your commit message" -Branch main

# Force push (if needed)
.\scripts\git_auto_push.ps1 -Message "Force update" -Force
```

### Bash (Linux/Mac):

```bash
chmod +x scripts/git_auto_push.sh
./scripts/git_auto_push.sh "Your commit message" main
```

---

## Troubleshooting

### Issue: "fatal: not a git repository"
**Solution**: Navigate to the correct directory first:
```bash
cd "C:\Users\Muhammad Anas\f_illi"
```

### Issue: "Authentication failed"
**Solution**: 
- For HTTPS: Use personal access token instead of password
  - Go to GitHub → Settings → Developer settings → Personal access tokens
  - Create new token with `repo` scope
  - Use token as password when prompted

- For SSH (easier): 
  - Generate SSH key: `ssh-keygen -t ed25519 -C "your_email@example.com"`
  - Add public key to GitHub → Settings → SSH and GPG keys
  - Use SSH URL: `git@github.com:YOUR_USERNAME/illi_os.git`

### Issue: Files not pushing
**Solution**: Check git status first:
```bash
git status
git add -A
git commit -m "Your message"
git push origin main
```

---

## Branch Strategy

Recommended git workflow for ILLI OS:

```
main (production-ready)
  ├── develop (active development)
  │   ├── feature/advanced-automation
  │   ├── feature/ghost-protocol-ui
  │   └── bugfix/mic-calibration
  └── release/v1.2.5
```

Create branches for new features:

```bash
# Create and switch to new branch
git checkout -b feature/your-feature-name

# After changes, commit and push
git add -A
git commit -m "Add: Your feature description"
git push origin feature/your-feature-name

# Then create Pull Request on GitHub
```

---

## Protecting Your Repository

Recommended GitHub settings:

1. **Go to Settings → Branches → Add rule for `main`**:
   - ✅ Require pull request reviews
   - ✅ Dismiss stale pull request approvals
   - ✅ Require status checks to pass
   - ✅ Restrict who can push to matching branches

2. **Go to Settings → Secrets and variables → Actions**:
   - Don't commit API keys or credentials
   - Use GitHub Secrets for sensitive data

3. **Go to Settings → Collaborators**:
   - Add team members with appropriate permissions

---

## Continuous Integration (Optional)

Add `.github/workflows/test.yml` for automated testing:

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/
```

---

## Important Notes

- **Never commit**:
  - API keys or secrets
  - Virtual environment directories (`venv/`)
  - Database files with sensitive data
  - Browser profile caches

- **Always commit**:
  - Source code (`*.py`)
  - Configuration templates (without secrets)
  - Documentation (`*.md`)
  - `.gitignore` template
  - Requirements and setup files

- **Keep main branch clean**:
  - Only merge tested, working code
  - Use pull requests for all changes
  - Require code reviews

---

## Next Steps

1. ✅ Create GitHub repository
2. ✅ Push initial code
3. 📝 Add collaborators (if team project)
4. 🔄 Set up CI/CD pipelines
5. 📚 Add comprehensive documentation
6. 🐛 Create issue templates for bug reports
7. 🎯 Set up project boards for tracking

---

**Questions?** Check [GitHub Docs](https://docs.github.com) or the ILLI OS documentation.
