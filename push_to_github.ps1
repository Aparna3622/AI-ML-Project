<#
PowerShell helper to push this project to GitHub.
Usage:
  - Run from the project folder: `.	ools\push_to_github.ps1` or `.\
eset path`.
  - It prefers `gh` if available. Otherwise it guides through git init/add/commit/remote/push.

Edit the `$RepoFullName` variable below to match your GitHub repo (username/repo).
#>

param()

$RepoFullName = "Aparna3622/AI-ML-Project"  # change if needed

function Use-GH {
    gh auth status 2>$null
    return $LASTEXITCODE -eq 0
}

if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "GitHub CLI detected. Creating repo and pushing using gh..." -ForegroundColor Green
    gh auth status || gh auth login
    gh repo create $RepoFullName --public --source=. --remote=origin --push
    exit $LASTEXITCODE
}

Write-Host "GitHub CLI not found; falling back to plain git commands." -ForegroundColor Yellow

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "git not found. Please install Git for Windows and restart PowerShell." -ForegroundColor Red
    Exit 1
}

git init
git add .
git commit -m "Initial commit: Health Prediction App"
git branch -M main

$remote = "https://github.com/$RepoFullName.git"
Write-Host "Adding remote origin -> $remote"
git remote add origin $remote

Write-Host "Now attempting to push to origin/main. You will be prompted for credentials if needed." -ForegroundColor Cyan
git push -u origin main

Write-Host "Done. If push failed due to authentication, consider installing the GitHub CLI (gh) or using a PAT (see GIT_AUTH.md)." -ForegroundColor Green
