# GitHub Authentication (gh) and Personal Access Token (PAT)

This file explains two recommended ways to authenticate and push your project to GitHub from Windows: using the `gh` (GitHub CLI) tool, or creating a Personal Access Token (PAT).

1) Recommended — GitHub CLI (`gh`)

- Install `gh`:
  - via winget: `winget install --id GitHub.cli -e --source winget`
  - or download: https://github.com/cli/cli#installation
- Login interactively (this opens a browser):
  ```powershell
  gh auth login
  ```
- Create the remote repo and push in one command (from project folder):
  ```powershell
  gh repo create Aparna3622/AI-ML-Project --public --source=. --remote=origin --push
  ```

2) Alternative — Personal Access Token (PAT)

- Generate a PAT: https://github.com/settings/tokens → `Generate new token` → select `repo` scopes, copy token.
- Configure Git to use the credential manager (recommended):
  - Install Git for Windows (includes Git Credential Manager) so Windows securely stores credentials.
  - After installing Git, run a normal `git push` and enter your username (`<your-github-username>`) and the PAT as the password when prompted.

- Quick (less secure) example using environment variable (only use temporarily):
  ```powershell
  $env:GITHUB_PAT = Read-Host "Enter PAT (will be stored only for this session)"
  git remote add origin https://$($env:GITHUB_PAT)@github.com/YourUser/YourRepo.git
  git push -u origin main
  Remove-Item Env:\GITHUB_PAT
  ```
  Warning: embedding PAT in URLs or environment variables can expose it — prefer `gh auth login` or the credential manager.

Notes
- If `git` is not installed, install Git for Windows: https://git-scm.com/download/win and restart PowerShell.
- On Windows, using `gh auth login` or the Git Credential Manager is the safest practice.
