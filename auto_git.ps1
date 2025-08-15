# Sun-Earth-Moon Simulation - Auto Git Operations (PowerShell)
# This script handles automatic Git operations for the project

Write-Host "🌍 Sun-Earth-Moon Simulation - Auto Git Operations" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Function to run commands with error handling
function Invoke-GitCommand {
    param(
        [string]$Command,
        [string]$Description
    )
    
    Write-Host "`n🔄 $Description" -ForegroundColor Yellow
    Write-Host "Running: $Command" -ForegroundColor Gray
    
    try {
        $result = Invoke-Expression $Command 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Success: $Description" -ForegroundColor Green
            if ($result) {
                Write-Host "Output: $result" -ForegroundColor White
            }
            return $true
        } else {
            Write-Host "❌ Error: $Description" -ForegroundColor Red
            Write-Host "Error: $result" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Exception: $_" -ForegroundColor Red
        return $false
    }
}

# Check if we're in a Git repository
if (-not (Test-Path ".git")) {
    Write-Host "❌ Not in a Git repository. Initializing..." -ForegroundColor Red
    git init
    git branch -M main
}

# Configure Git
Write-Host "`n🔧 Configuring Git..." -ForegroundColor Cyan
Invoke-GitCommand "git config user.name 'EarlTheDuke'" "Setting Git username"
Invoke-GitCommand "git config user.email 'earl@example.com'" "Setting Git email (update with real email)"

# Check repository status
Write-Host "`n📊 Repository Status:" -ForegroundColor Cyan
git status

# Add and commit changes
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$commitMessage = "Auto-commit: $timestamp"

Write-Host "`n🚀 Committing changes..." -ForegroundColor Cyan
git add .

$statusOutput = git status --porcelain
if ($statusOutput) {
    Invoke-GitCommand "git commit -m '$commitMessage'" "Committing changes"
} else {
    Write-Host "ℹ️  No changes to commit" -ForegroundColor Blue
}

# Check if remote exists
$remotes = git remote
if (-not $remotes -contains "origin") {
    Write-Host "`n🔗 Adding GitHub remote..." -ForegroundColor Cyan
    $repoUrl = "https://github.com/EarlTheDuke/SunEarthmoon.git"
    Invoke-GitCommand "git remote add origin $repoUrl" "Adding remote origin"
}

# Push to GitHub
Write-Host "`n📤 Pushing to GitHub..." -ForegroundColor Cyan
$pushResult = git push origin main 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
} else {
    Write-Host "❌ Push failed. You may need to:" -ForegroundColor Red
    Write-Host "1. Create the repository at: https://github.com/new" -ForegroundColor Yellow
    Write-Host "2. Repository name: SunEarthmoon" -ForegroundColor Yellow
    Write-Host "3. Set it as public" -ForegroundColor Yellow
    Write-Host "4. Don't initialize with README (we have our own)" -ForegroundColor Yellow
    Write-Host "`nError details: $pushResult" -ForegroundColor Red
}

Write-Host "`n✅ Auto Git operations completed!" -ForegroundColor Green
Write-Host "`n📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Update your email: git config user.email your-actual-email@example.com" -ForegroundColor White
Write-Host "2. Run the simulation: python sun_earth_moon_simulation.py" -ForegroundColor White
Write-Host "3. Run this script anytime to auto-commit changes" -ForegroundColor White

Read-Host "`nPress Enter to continue..."
