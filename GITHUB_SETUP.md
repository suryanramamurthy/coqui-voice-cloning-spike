# GitHub Repository Setup Instructions

Your local git repository is ready! Follow these steps to create the remote GitHub repository:

## Option 1: Using GitHub CLI (Recommended - Fastest)

If you have GitHub CLI installed:

```bash
# Create a new public repository on GitHub
gh repo create coqui-voice-cloning-spike --public --source=. --remote=origin --push

# Or for a private repository
gh repo create coqui-voice-cloning-spike --private --source=. --remote=origin --push
```

## Option 2: Using GitHub Web Interface (Manual)

### Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `coqui-voice-cloning-spike`
3. Description: "Voice cloning spike using Coqui TTS on macOS M3 Pro"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### Step 2: Connect Your Local Repository

After creating the repository on GitHub, run these commands:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/coqui-voice-cloning-spike.git

# Push your code to GitHub
git push -u origin main
```

## Verify Setup

After pushing, visit your repository at:
```
https://github.com/YOUR_USERNAME/coqui-voice-cloning-spike
```

## Current Repository Status

✅ Git initialized  
✅ Initial commit created (3 files, 426 insertions)  
✅ Branch: `main`  
✅ Files committed:
  - README.md
  - voice_cloning_demo.py
  - .gitignore

## What's Excluded (via .gitignore)

- Python virtual environment (`venv/`)
- Generated audio files (`*.wav`, `*.mp3`)
- Output directory
- Python cache files
- OS-specific files (`.DS_Store`)

## Future Updates

To push changes to GitHub:

```bash
git add .
git commit -m "Your commit message"
git push
```

## Need Help?

If you need to install GitHub CLI:
```bash
brew install gh
gh auth login  # Follow prompts to authenticate
```
