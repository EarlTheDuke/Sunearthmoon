# GitHub Repository Setup Script
# This script creates the repository and pushes the code

Write-Host "🚀 Setting up GitHub Repository: SunEarthmoon" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Repository details
$repoName = "SunEarthmoon"
$description = "Realistic 3D Sun-Earth-Moon system simulation using precise ephemeris data from astropy"
$repoUrl = "https://github.com/EarlTheDuke/$repoName.git"

Write-Host "`n📋 Repository Configuration:" -ForegroundColor Yellow
Write-Host "Name: $repoName" -ForegroundColor White
Write-Host "Description: $description" -ForegroundColor White
Write-Host "URL: $repoUrl" -ForegroundColor White

# Step 1: Open GitHub to create repository
Write-Host "`n🌐 Opening GitHub new repository page..." -ForegroundColor Cyan
Start-Process "https://github.com/new"

Write-Host "`n📝 Please create the repository with these settings:" -ForegroundColor Yellow
Write-Host "Repository name: $repoName" -ForegroundColor Green
Write-Host "Description: $description" -ForegroundColor Green
Write-Host "Visibility: Public ✓" -ForegroundColor Green
Write-Host "Initialize repository: UNCHECKED ✗" -ForegroundColor Red
Write-Host "Add .gitignore: None ✗" -ForegroundColor Red
Write-Host "Add a license: None ✗" -ForegroundColor Red

# Wait for user to create repository
Read-Host "`nPress Enter after you've created the repository on GitHub"

# Step 2: Configure Git remote (in case it is not set)
Write-Host "`n🔗 Configuring Git remote..." -ForegroundColor Cyan
$remoteCheck = git remote
if ($remoteCheck -notcontains "origin") {
    git remote add origin $repoUrl
    Write-Host "✅ Remote 'origin' added" -ForegroundColor Green
} else {
    Write-Host "✅ Remote 'origin' already exists" -ForegroundColor Green
}

# Step 3: Push to GitHub
Write-Host "`n📤 Pushing to GitHub..." -ForegroundColor Cyan

try {
    # First, ensure we're on main branch
    git checkout main 2>$null
    if ($LASTEXITCODE -ne 0) {
        git checkout -b main
    }
    
    # Push to GitHub
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n🎉 SUCCESS! Your project is now on GitHub!" -ForegroundColor Green
        Write-Host "🌐 Repository URL: $repoUrl" -ForegroundColor Cyan
        
        # Open the repository
        Start-Process $repoUrl
        Write-Host "🌐 Opening your repository in browser..." -ForegroundColor Cyan
        
        Write-Host "`n📊 Project Summary:" -ForegroundColor Yellow
        Write-Host "✅ GitHub repository created: $repoName" -ForegroundColor Green
        Write-Host "✅ All code pushed to GitHub" -ForegroundColor Green
        Write-Host "✅ Repository is public and accessible" -ForegroundColor Green
        Write-Host "✅ Ready for collaboration and sharing" -ForegroundColor Green
        
        Write-Host "`n🔗 Your project link: $repoUrl" -ForegroundColor Magenta
        
    } else {
        Write-Host "`n❌ Push failed. Please check:" -ForegroundColor Red
        Write-Host "1. Repository was created on GitHub" -ForegroundColor Yellow
        Write-Host "2. Repository name is exactly: $repoName" -ForegroundColor Yellow
        Write-Host "3. Repository is public" -ForegroundColor Yellow
        Write-Host "4. Repository was NOT initialized with README" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "`n❌ Error during push: $_" -ForegroundColor Red
}

Write-Host "`n🚀 Setup complete! Your Sun-Earth-Moon simulation is ready!" -ForegroundColor Green
Read-Host "Press Enter to continue"
