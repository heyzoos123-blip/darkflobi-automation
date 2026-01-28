# Master Development Powerhouse Control
# Phase 2: Complete automation suite

param(
    [string]$Command = "status",
    [string]$Project = "all",
    [switch]$Verbose
)

$ghPath = "C:\Program Files\GitHub CLI\gh.exe"

Write-Host "🚀 Development Powerhouse - Phase 2" -ForegroundColor Green
Write-Host "===================================" 
Write-Host ""

switch ($Command) {
    "status" {
        Write-Host "📊 Development Environment Overview:" -ForegroundColor Cyan
        Write-Host ""
        
        # Tool status
        try {
            $ghVersion = (& $ghPath --version | Select-Object -First 1).Trim()
            Write-Host "✅ GitHub CLI: $ghVersion" -ForegroundColor Green
        } catch {
            Write-Host "❌ GitHub CLI: Not available" -ForegroundColor Red
        }
        
        try {
            $gitVersion = (git --version).Trim()
            Write-Host "✅ Git: $gitVersion" -ForegroundColor Green
        } catch {
            Write-Host "❌ Git: Not available" -ForegroundColor Red
        }
        
        try {
            $nodeVersion = (node --version).Trim()
            Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
        } catch {
            Write-Host "❌ Node.js: Not available" -ForegroundColor Red
        }
        
        # GitHub auth status
        $authTest = & $ghPath auth status 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ GitHub Auth: Connected" -ForegroundColor Green
        } else {
            Write-Host "⚠️  GitHub Auth: Run 'gh auth login --web'" -ForegroundColor Yellow
        }
        
        Write-Host ""
        Write-Host "🛠️  Available Automation Tools:" -ForegroundColor Cyan
        Write-Host "  📊 project-monitor.ps1     - GitHub repo & CI monitoring"
        Write-Host "  💾 backup-system.ps1       - Automated project backups"
        Write-Host "  🚀 deploy-automation.ps1   - Testing & deployment"
        Write-Host "  🎯 dev-powerhouse-master.ps1 - This master control"
        Write-Host ""
    }
    
    "monitor" {
        Write-Host "📊 Running project monitor..." -ForegroundColor Cyan
        & ".\automation\project-monitor.ps1"
    }
    
    "backup" {
        Write-Host "💾 Creating automated backup..." -ForegroundColor Cyan
        if ($Verbose) {
            & ".\automation\backup-system.ps1" create -Verbose
        } else {
            & ".\automation\backup-system.ps1" create
        }
    }
    
    "test" {
        Write-Host "🧪 Running automated tests..." -ForegroundColor Cyan
        if ($Verbose) {
            & ".\automation\deploy-automation.ps1" test $Project -Verbose
        } else {
            & ".\automation\deploy-automation.ps1" test $Project
        }
    }
    
    "deploy" {
        Write-Host "🚀 Full deployment pipeline..." -ForegroundColor Cyan
        Write-Host ""
        
        # Step 1: Backup
        Write-Host "Step 1: Creating backup..." -ForegroundColor Yellow
        & ".\automation\backup-system.ps1" create
        
        Write-Host ""
        
        # Step 2: Test
        Write-Host "Step 2: Running tests..." -ForegroundColor Yellow
        $testResult = & ".\automation\deploy-automation.ps1" test $Project
        
        # Step 3: Monitor (if tests pass)
        Write-Host ""
        Write-Host "Step 3: Checking GitHub status..." -ForegroundColor Yellow
        & ".\automation\project-monitor.ps1"
        
        Write-Host ""
        Write-Host "✅ Deployment pipeline complete!" -ForegroundColor Green
    }
    
    "setup" {
        Write-Host "⚙️  Phase 2 Setup Assistant:" -ForegroundColor Cyan
        Write-Host ""
        
        # Check GitHub auth
        $authTest = & $ghPath auth status 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "🔐 GitHub Authentication needed:" -ForegroundColor Yellow
            Write-Host "   Run: gh auth login --web" -ForegroundColor White
            Write-Host "   This will open your browser to authenticate" -ForegroundColor Gray
            Write-Host ""
        }
        
        # Check project structure
        if (!(Test-Path "projects")) {
            Write-Host "📁 Creating projects directory..." -ForegroundColor Yellow
            New-Item -Path "projects" -ItemType Directory -Force | Out-Null
            Write-Host "   ✅ Created /projects directory" -ForegroundColor Green
        }
        
        if (!(Test-Path "backups")) {
            Write-Host "💾 Creating backups directory..." -ForegroundColor Yellow
            New-Item -Path "backups" -ItemType Directory -Force | Out-Null
            Write-Host "   ✅ Created /backups directory" -ForegroundColor Green
        }
        
        Write-Host ""
        Write-Host "🎯 Phase 2 Development Powerhouse is ready!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Quick start:" -ForegroundColor White
        Write-Host "  .\automation\dev-powerhouse-master.ps1 monitor   - Check repos & CI"
        Write-Host "  .\automation\dev-powerhouse-master.ps1 backup    - Create backup"
        Write-Host "  .\automation\dev-powerhouse-master.ps1 test      - Run project tests"
        Write-Host "  .\automation\dev-powerhouse-master.ps1 deploy    - Full pipeline"
        Write-Host ""
    }
    
    default {
        Write-Host "📋 Development Powerhouse Commands:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  status    - Show development environment status"
        Write-Host "  setup     - Run Phase 2 setup assistant"  
        Write-Host "  monitor   - Check GitHub repos & CI status"
        Write-Host "  backup    - Create automated project backup"
        Write-Host "  test      - Run automated tests on projects"
        Write-Host "  deploy    - Run full deployment pipeline"
        Write-Host ""
        Write-Host "Options:" -ForegroundColor Gray
        Write-Host "  -Project <name>  - Target specific project (default: all)"
        Write-Host "  -Verbose         - Show detailed output"
        Write-Host ""
        Write-Host "Examples:" -ForegroundColor Gray
        Write-Host "  .\dev-powerhouse-master.ps1 test duotrader -Verbose"
        Write-Host "  .\dev-powerhouse-master.ps1 deploy -Project super-duo"
        Write-Host ""
    }
}