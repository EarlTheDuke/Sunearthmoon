#!/usr/bin/env python3
"""
Quick Git push script that doesn't hang
"""

import subprocess
import sys

def run_git_command(command, description):
    """Run a git command and return immediately when done."""
    print(f"🔄 {description}")
    print(f"Command: {command}")
    
    try:
        # Run command and wait for completion
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS!")
            if result.stdout.strip():
                print("Output:")
                print(result.stdout.strip())
        else:
            print(f"❌ {description} - FAILED!")
            if result.stderr.strip():
                print("Error:")
                print(result.stderr.strip())
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT after 30 seconds")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def quick_push(commit_message=None):
    """Quickly add, commit, and push changes."""
    
    if commit_message is None:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Quick update: {timestamp}"
    
    print("🚀 Quick Git Push")
    print("=" * 30)
    
    # Step 1: Add all changes
    if not run_git_command("git add .", "Adding all changes"):
        return False
    
    # Step 2: Commit changes
    if not run_git_command(f'git commit -m "{commit_message}"', "Committing changes"):
        print("ℹ️  No changes to commit (already up to date)")
    
    # Step 3: Push to GitHub
    if not run_git_command("git push origin main", "Pushing to GitHub"):
        return False
    
    # Step 4: Verify completion
    if not run_git_command("git status --porcelain", "Verifying clean status"):
        return False
    
    print("\n🎉 COMPLETE! All changes pushed to GitHub successfully!")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        success = quick_push(message)
    else:
        success = quick_push()
    
    if success:
        print("✅ Repository updated: https://github.com/EarlTheDuke/Sunearthmoon")
    else:
        print("❌ Push failed - check the errors above")
