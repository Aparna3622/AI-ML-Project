# Push this project to your GitHub repository

Replace `<your-remote-url>` with `https://github.com/Aparna3622/AI-ML-Project.git` (or your chosen remote).

Commands to run from `C:\Users\Admin\Desktop\AI`:

```powershell
git init
git add .
git commit -m "Initial commit: Health Prediction App"
git branch -M main
git remote add origin https://github.com/Aparna3622/AI-ML-Project.git
git push -u origin main
```

If you prefer SSH, replace the remote URL accordingly.

If push fails due to authentication, ensure your Git credentials are configured or use GitHub CLI:

```powershell
gh auth login
gh repo create Aparna3622/AI-ML-Project --public --source=. --remote=origin --push
```
