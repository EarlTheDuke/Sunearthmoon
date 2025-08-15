#!/usr/bin/env python3
"""
Automatic Git operations script for Sun-Earth-Moon simulation project.
This script handles automatic commits and pushes to GitHub.
"""

import subprocess
import sys
import os
from datetime import datetime

def run_command(command, description=""):
    """Run a shell command and return the result."""
    print(f"\n🔄 {description}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Success: {description}")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"❌ Error: {description}")
            print(f"Error output: {result.stderr.strip()}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Exception running command: {e}")
        return False

def setup_git_config():
    """Set up Git configuration."""
    print("\n🔧 Setting up Git configuration...")
    
    commands = [
        ("git config user.name \"EarlTheDuke\"", "Setting Git username"),
        ("git config user.email \"earl@example.com\"", "Setting Git email (update with real email)"),
        ("git config init.defaultBranch main", "Setting default branch to main")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def check_repo_status():
    """Check repository status."""
    print("\n📊 Checking repository status...")
    
    commands = [
        ("git status --porcelain", "Checking for changes"),
        ("git remote -v", "Checking remote connections"),
        ("git branch", "Checking current branch")
    ]
    
    for command, description in commands:
        run_command(command, description)

def auto_commit_push(message=None):
    """Automatically commit and push changes."""
    if message is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Auto-commit: {timestamp}"
    
    print(f"\n🚀 Auto-committing with message: '{message}'")
    
    commands = [
        ("git add .", "Adding all changes"),
        (f"git commit -m \"{message}\"", "Committing changes"),
        ("git push origin main", "Pushing to GitHub")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            if "nothing to commit" in description or "up to date" in description:
                print("ℹ️  No changes to commit or already up to date")
                continue
            else:
                return False
    
    print("✅ Successfully committed and pushed changes!")
    return True

def create_github_repo():
    """Create GitHub repository (requires GitHub CLI)."""
    print("\n🏗️  Creating GitHub repository...")
    
    # Check if GitHub CLI is installed
    if not run_command("gh --version", "Checking GitHub CLI"):
        print("❌ GitHub CLI not found. Please install it from: https://cli.github.com/")
        print("Alternative: Create repository manually at https://github.com/new")
        return False
    
    # Create repository
    repo_name = "SunEarthmoon"
    description = "Realistic 3D Sun-Earth-Moon system simulation using precise ephemeris data"
    
    command = f"gh repo create {repo_name} --public --description \"{description}\" --source=."
    
    if run_command(command, "Creating GitHub repository"):
        print(f"✅ Repository created: https://github.com/EarlTheDuke/{repo_name}")
        return True
    else:
        print("❌ Failed to create repository. You may need to:")
        print("1. Install GitHub CLI: https://cli.github.com/")
        print("2. Login with: gh auth login")
        print("3. Or create manually at: https://github.com/new")
        return False

def setup_auto_push():
    """Set up automatic pushing for future changes."""
    print("\n⚙️  Setting up automatic Git operations...")
    
    # Add git hooks or setup instructions
    hooks_dir = ".git/hooks"
    if not os.path.exists(hooks_dir):
        os.makedirs(hooks_dir)
    
    # Create a simple pre-commit hook
    pre_commit_hook = os.path.join(hooks_dir, "pre-commit")
    
    hook_content = """#!/bin/sh
# Auto-commit hook for Sun-Earth-Moon simulation
echo "🔄 Running pre-commit checks..."
python -m py_compile sun_earth_moon_simulation.py
if [ $? -ne 0 ]; then
    echo "❌ Python syntax error detected!"
    exit 1
fi
echo "✅ Pre-commit checks passed!"
"""
    
    try:
        with open(pre_commit_hook, 'w') as f:
            f.write(hook_content)
        
        # Make it executable (Unix-like systems)
        if os.name != 'nt':  # Not Windows
            os.chmod(pre_commit_hook, 0o755)
        
        print("✅ Pre-commit hook installed")
        
    except Exception as e:
        print(f"⚠️  Could not create pre-commit hook: {e}")

def main():
    """Main function."""
    print("🌍 Sun-Earth-Moon Simulation - Auto Git Setup")
    print("=" * 50)
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("❌ Not in a Git repository. Please run 'git init' first.")
        return
    
    # Setup Git configuration
    setup_git_config()
    
    # Check repository status
    check_repo_status()
    
    # Try to create GitHub repository
    print("\n🤔 Would you like to create the GitHub repository automatically?")
    choice = input("Enter 'y' for yes, 'n' to skip: ").strip().lower()
    
    if choice == 'y':
        create_github_repo()
    else:
        print("ℹ️  Skipping GitHub repository creation.")
        print("   Create manually at: https://github.com/new")
        print("   Repository name: SunEarthmoon")
        print("   Then run: git remote add origin https://github.com/EarlTheDuke/SunEarthmoon.git")
    
    # Setup automatic operations
    setup_auto_push()
    
    # Initial commit and push
    print("\n🚀 Performing initial commit and push...")
    auto_commit_push("Initial commit: Sun-Earth-Moon simulation with precise ephemeris data")
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Update your email in Git config: git config user.email \"your-email@example.com\"")
    print("2. Run this script anytime to auto-commit and push changes")
    print("3. Your simulation is ready to run: python sun_earth_moon_simulation.py")

if __name__ == "__main__":
    main()
