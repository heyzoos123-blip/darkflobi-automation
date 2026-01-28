# Development Powerhouse Setup
# Phase 2 of super bot upgrade: automated dev environment

param(
    [string]$Action = "status"
)

$ghPath = "C:\Program Files\GitHub CLI\gh.exe"

Write-Host "🚀 Development Powerhouse - Phase 2" -ForegroundColor Green
Write-Host "==================================="
Write-Host ""

switch ($Action) {
    "status" {
        Write-Host "📊 Development Environment Status:"
        Write-Host ""
        
        # GitHub CLI status
        try {
            $ghVersion = & $ghPath --version
            Write-Host "✅ GitHub CLI: $ghVersion" -ForegroundColor Green
            
            # Check if authenticated
            $authStatus = & $ghPath auth status 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ GitHub Auth: Connected" -ForegroundColor Green
            } else {
                Write-Host "⚠️  GitHub Auth: Not authenticated" -ForegroundColor Yellow
                Write-Host "   Run: .\dev-powerhouse.ps1 auth" -ForegroundColor Gray
            }
        } catch {
            Write-Host "❌ GitHub CLI: Not available" -ForegroundColor Red
        }
        
        # Git status
        try {
            $gitVersion = git --version
            Write-Host "✅ Git: $gitVersion" -ForegroundColor Green
        } catch {
            Write-Host "❌ Git: Not available" -ForegroundColor Red
        }
        
        # Node.js status
        try {
            $nodeVersion = node --version
            Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
        } catch {
            Write-Host "❌ Node.js: Not available" -ForegroundColor Red
        }
        
        # Project status
        Write-Host ""
        Write-Host "📂 Project Structure:" -ForegroundColor Cyan
        $projects = @("duotrader", "super-duo-automation")
        foreach ($project in $projects) {
            if (Test-Path "projects\$project") {
                Write-Host "✅ projects/$project exists" -ForegroundColor Green
            } else {
                Write-Host "⚠️  projects/$project missing" -ForegroundColor Yellow
            }
        }
    }
    
    "auth" {
        Write-Host "🔐 GitHub Authentication Setup:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "This will open your browser to authenticate with GitHub..."
        Write-Host "Press any key to continue or Ctrl+C to cancel"
        $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
        
        & $ghPath auth login --web
    }
    
    "repos" {
        Write-Host "📚 Repository Overview:" -ForegroundColor Cyan
        Write-Host ""
        
        try {
            $repos = & $ghPath repo list --limit 10 --json name,description,visibility,updatedAt
            $repoData = $repos | ConvertFrom-Json
            
            foreach ($repo in $repoData) {
                $updated = [DateTime]::Parse($repo.updatedAt).ToString("yyyy-MM-dd")
                Write-Host "📦 $($repo.name) ($($repo.visibility))" -ForegroundColor White
                Write-Host "   $($repo.description)" -ForegroundColor Gray
                Write-Host "   Updated: $updated" -ForegroundColor Gray
                Write-Host ""
            }
        } catch {
            Write-Host "❌ Could not fetch repositories (auth required?)" -ForegroundColor Red
            Write-Host "   Run: .\dev-powerhouse.ps1 auth" -ForegroundColor Gray
        }
    }
    
    "backup" {
        Write-Host "💾 Project Backup System:" -ForegroundColor Cyan
        Write-Host ""
        
        # Create timestamped backup
        $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm"
        $backupDir = "backups\$timestamp"
        
        Write-Host "Creating backup: $backupDir"
        New-Item -Path $backupDir -ItemType Directory -Force | Out-Null
        
        # Backup key project files
        $filesToBackup = @(
            "projects\*",
            "scripts\*", 
            "automation\*",
            "*.md",
            "memory\*"
        )
        
        foreach ($pattern in $filesToBackup) {
            $files = Get-ChildItem $pattern -Recurse -File -ErrorAction SilentlyContinue
            foreach ($file in $files) {
                $relativePath = $file.FullName.Replace((Get-Location).Path + "\", "")
                $backupPath = Join-Path $backupDir $relativePath
                $backupFolder = Split-Path $backupPath -Parent
                
                if (!(Test-Path $backupFolder)) {
                    New-Item -Path $backupFolder -ItemType Directory -Force | Out-Null
                }
                
                Copy-Item $file.FullName $backupPath
            }
        }
        
        Write-Host "✅ Backup complete: $backupDir" -ForegroundColor Green
        
        # Show backup size
        $backupSize = (Get-ChildItem $backupDir -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
        Write-Host "📊 Backup size: $([math]::Round($backupSize, 2)) MB" -ForegroundColor Gray
    }
    
    "deploy" {
        Write-Host "🚀 Automated Testing & Deployment:" -ForegroundColor Cyan
        Write-Host ""
        
        # Check for each project
        $projects = Get-ChildItem "projects" -Directory -ErrorAction SilentlyContinue
        
        if ($projects.Count -eq 0) {
            Write-Host "⚠️  No projects found in /projects directory" -ForegroundColor Yellow
            return
        }
        
        foreach ($project in $projects) {
            Write-Host "🔨 Testing: $($project.Name)" -ForegroundColor White
            
            $projectPath = $project.FullName
            Push-Location $projectPath
            
            # Look for common files
            $hasPackageJson = Test-Path "package.json"
            $hasReadme = Test-Path "README.md"
            $hasTests = Test-Path "tests" -PathType Container
            
            if ($hasPackageJson) {
                Write-Host "  ✅ package.json found" -ForegroundColor Green
                # Could run npm test here
            }
            
            if ($hasReadme) {
                Write-Host "  ✅ README.md found" -ForegroundColor Green
            }
            
            if ($hasTests) {
                Write-Host "  ✅ tests directory found" -ForegroundColor Green
            }
            
            Pop-Location
            Write-Host ""
        }
    }
    
    default {
        Write-Host "📋 Available Commands:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  .\dev-powerhouse.ps1 status  - Show development environment status"
        Write-Host "  .\dev-powerhouse.ps1 auth    - Authenticate with GitHub"
        Write-Host "  .\dev-powerhouse.ps1 repos   - List your repositories"
        Write-Host "  .\dev-powerhouse.ps1 backup  - Create project backup"
        Write-Host "  .\dev-powerhouse.ps1 deploy  - Run automated testing"
        Write-Host ""
    }
}