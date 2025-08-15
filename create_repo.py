#!/usr/bin/env python3
"""
GitHub Repository Creation Script
Creates a GitHub repository using the GitHub API
"""

import requests
import json
import webbrowser
import subprocess
import sys

def create_github_repo():
    """Create GitHub repository using API or open browser for manual creation."""
    
    print("🚀 Creating GitHub Repository: SunEarthmoon")
    print("=" * 50)
    
    repo_data = {
        "name": "SunEarthmoon",
        "description": "Realistic 3D Sun-Earth-Moon system simulation using precise ephemeris data from astropy",
        "private": False,
        "auto_init": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }
    
    print("📋 Repository Configuration:")
    print(f"Name: {repo_data['name']}")
    print(f"Description: {repo_data['description']}")
    print(f"Public: {not repo_data['private']}")
    print(f"Auto-init: {repo_data['auto_init']}")
    
    # Since we don't have authentication set up, let's open the browser
    # and provide the exact settings needed
    
    print("\n🌐 Opening GitHub to create repository...")
    print("\nPlease create the repository with these EXACT settings:")
    print("Repository name: SunEarthmoon")
    print("Description: Realistic 3D Sun-Earth-Moon system simulation using precise ephemeris data from astropy")
    print("Visibility: Public")
    print("Initialize repository: UNCHECKED (we have our own files)")
    print("Add .gitignore: None (we have our own)")
    print("Add a license: None (can add later)")
    
    try:
        # Open GitHub new repository page
        webbrowser.open("https://github.com/new")
        print("✅ GitHub new repository page opened in browser")
        
        # Wait for user confirmation
        input("\nPress Enter after you've created the repository on GitHub...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error opening browser: {e}")
        print("Please manually go to: https://github.com/new")
        return False

def push_to_github():
    """Push the repository to GitHub."""
    
    print("\n📤 Pushing to GitHub...")
    
    commands = [
        ("git remote -v", "Checking remote configuration"),
        ("git push -u origin main", "Pushing to GitHub")
    ]
    
    for command, description in commands:
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
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    return True

def main():
    """Main function."""
    
    # Step 1: Create the repository
    if create_github_repo():
        print("\n✅ Repository should now be created on GitHub")
        
        # Step 2: Push the code
        if push_to_github():
            print("\n🎉 SUCCESS! Your project is now on GitHub!")
            
            repo_url = "https://github.com/EarlTheDuke/SunEarthmoon"
            print(f"🌐 Repository URL: {repo_url}")
            
            # Open the repository
            try:
                webbrowser.open(repo_url)
                print("🌐 Opening your new repository in browser...")
            except:
                print("💡 Manually visit your repository at the URL above")
            
            print("\n📊 Project Summary:")
            print("✅ GitHub repository created: SunEarthmoon")
            print("✅ All code pushed to GitHub")
            print("✅ Repository is public and accessible")
            print("✅ Ready for collaboration and sharing")
            
            return repo_url
        else:
            print("\n⚠️  Push failed. Please check the repository was created correctly.")
            return None
    else:
        print("\n❌ Repository creation failed.")
        return None

if __name__ == "__main__":
    result = main()
    if result:
        print(f"\n🔗 Your project link: {result}")
    else:
        print("\n❌ Setup incomplete. Please try again.")
