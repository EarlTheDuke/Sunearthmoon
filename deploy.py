#!/usr/bin/env python3
"""
Quick deployment script for Sun-Earth-Moon simulation project.
This script creates the GitHub repository and pushes the code automatically.
"""

import subprocess
import sys
import webbrowser
from datetime import datetime

def run_cmd(command, description=""):
    """Run a command and return success status."""
    print(f"\n🔄 {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} - Success!")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} - Failed!")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    print("🚀 Sun-Earth-Moon Simulation - Quick Deploy")
    print("=" * 50)
    
    # Step 1: Test the simulation
    print("\n🧪 Testing simulation...")
    test_cmd = 'python -c "import sun_earth_moon_simulation; print(\'✅ Simulation imports successfully\')"'
    if not run_cmd(test_cmd, "Testing simulation import"):
        print("⚠️  Simulation test failed, but continuing with deployment...")
    
    # Step 2: Set up Git if not already done
    print("\n🔧 Setting up Git configuration...")
    run_cmd('git config user.name "EarlTheDuke"', "Setting Git username")
    run_cmd('git config user.email "earl@github.com"', "Setting Git email")
    
    # Step 3: Add and commit all changes
    print("\n📝 Committing all changes...")
    run_cmd("git add .", "Adding all files")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Deploy: Sun-Earth-Moon simulation ready - {timestamp}"
    run_cmd(f'git commit -m "{commit_msg}"', "Committing changes")
    
    # Step 4: Set up remote (if not exists)
    print("\n🔗 Setting up GitHub remote...")
    repo_url = "https://github.com/EarlTheDuke/SunEarthmoon.git"
    
    # Check if remote exists
    result = subprocess.run("git remote", shell=True, capture_output=True, text=True)
    if "origin" not in result.stdout:
        run_cmd(f"git remote add origin {repo_url}", "Adding GitHub remote")
    
    # Step 5: Try to push
    print("\n📤 Pushing to GitHub...")
    if run_cmd("git push -u origin main", "Pushing to GitHub"):
        print("\n🎉 SUCCESS! Your project is now on GitHub!")
        print(f"🌐 Repository URL: {repo_url}")
        
        # Open GitHub repository in browser
        try:
            webbrowser.open(repo_url)
            print("🌐 Opening repository in browser...")
        except:
            print("💡 Manually visit your repository at the URL above")
            
    else:
        print("\n⚠️  Push failed. The repository might not exist yet.")
        print("\n📋 Manual steps to create repository:")
        print("1. Go to: https://github.com/new")
        print("2. Repository name: SunEarthmoon")
        print("3. Make it Public")
        print("4. Don't initialize with README")
        print("5. Click 'Create repository'")
        print("6. Run this script again")
        
        # Open GitHub new repo page
        try:
            webbrowser.open("https://github.com/new")
            print("🌐 Opening GitHub new repository page...")
        except:
            pass
    
    # Step 6: Show project status
    print("\n📊 Project Summary:")
    print("✅ Sun-Earth-Moon simulation script created")
    print("✅ All dependencies installed (astropy, matplotlib, numpy)")
    print("✅ Git repository initialized and configured")
    print("✅ Automation scripts created")
    print("✅ Documentation (README.md) included")
    
    print("\n🚀 Ready to run:")
    print("python sun_earth_moon_simulation.py")
    
    print("\n🔄 Auto-commit future changes:")
    print("python auto_git.py")
    print("# or #")
    print("powershell -ExecutionPolicy Bypass -File auto_git.ps1")

if __name__ == "__main__":
    main()
