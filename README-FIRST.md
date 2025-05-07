# Alfred Documentation GitHub Setup

## Creating the GitHub Repository

1. Visit https://github.com/new
2. Enter repository name: **alfred-documentation**
3. Choose visibility (Public or Private)
4. **IMPORTANT:** Leave "Add a README file" UNCHECKED
5. Click "Create repository"

## Pushing Your Local Repository

After creating the GitHub repository, run these commands in your terminal:

```bash
cd /home/locotoki/alfred-docs-repo
git remote add origin https://github.com/locotoki/alfred-documentation.git
git push -u origin main
```

## Authentication Methods

If you're using:

### Personal Access Token
When prompted, enter your GitHub username and your personal access token as the password.

### SSH Authentication
If you prefer SSH, use this command instead:
```bash
git remote set-url origin git@github.com:locotoki/alfred-documentation.git
git push -u origin main
```

## After Successful Push

Visit your GitHub repository at:
https://github.com/locotoki/alfred-documentation

To enable GitHub Pages for documentation website:
1. Go to repository Settings → Pages
2. Source: select "Deploy from a branch" 
3. Branch: select "main", folder: "/ (root)"
4. Click Save

Your documentation will be available at https://locotoki.github.io/alfred-documentation/