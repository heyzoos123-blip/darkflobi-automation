# Automated Testing & Deployment System
# Part of Phase 2: Development Powerhouse

param(
    [string]$Project = "all",
    [string]$Action = "test",
    [switch]$Verbose
)

$ghPath = "C:\Program Files\GitHub CLI\gh.exe"

Write-Host "🚀 Deployment Automation" -ForegroundColor Cyan
Write-Host "========================" 
Write-Host ""

# Get available projects
$projectsDir = "projects"
if (!(Test-Path $projectsDir)) {
    Write-Host "📁 Creating projects directory..." -ForegroundColor Gray
    New-Item -Path $projectsDir -ItemType Directory -Force | Out-Null
}

$projects = Get-ChildItem $projectsDir -Directory -ErrorAction SilentlyContinue

if ($projects.Count -eq 0) {
    Write-Host "⚠️  No projects found in /$projectsDir directory" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🏗️  Create a project structure like:" -ForegroundColor Gray
    Write-Host "   projects/duotrader/"
    Write-Host "   projects/super-duo/"
    Write-Host ""
    return
}

function Test-Project {
    param($ProjectPath, $ProjectName)
    
    Write-Host "🔨 Testing: $ProjectName" -ForegroundColor White
    
    Push-Location $ProjectPath
    
    $results = @{
        name = $ProjectName
        hasPackageJson = Test-Path "package.json"
        hasReadme = Test-Path "README.md"
        hasTests = Test-Path "tests" -PathType Container
        hasGitRepo = Test-Path ".git" -PathType Container
        hasDockerfile = Test-Path "Dockerfile"
        testsPassed = $false
        buildSucceeded = $false
        errors = @()
    }
    
    # Check package.json and run tests
    if ($results.hasPackageJson) {
        Write-Host "  ✅ package.json found" -ForegroundColor Green
        
        try {
            if ($Verbose) { Write-Host "  🔄 Running npm install..." -ForegroundColor Gray }
            $installOutput = npm install 2>&1
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  ✅ Dependencies installed" -ForegroundColor Green
                
                # Try to run tests if available
                $packageJson = Get-Content "package.json" | ConvertFrom-Json
                if ($packageJson.scripts.test) {
                    if ($Verbose) { Write-Host "  🧪 Running tests..." -ForegroundColor Gray }
                    $testOutput = npm test 2>&1
                    
                    if ($LASTEXITCODE -eq 0) {
                        Write-Host "  ✅ Tests passed" -ForegroundColor Green
                        $results.testsPassed = $true
                    } else {
                        Write-Host "  ❌ Tests failed" -ForegroundColor Red
                        $results.errors += "Tests failed"
                        if ($Verbose) { Write-Host "     $testOutput" -ForegroundColor Gray }
                    }
                }
                
                # Try to build if available
                if ($packageJson.scripts.build) {
                    if ($Verbose) { Write-Host "  🏗️  Running build..." -ForegroundColor Gray }
                    $buildOutput = npm run build 2>&1
                    
                    if ($LASTEXITCODE -eq 0) {
                        Write-Host "  ✅ Build succeeded" -ForegroundColor Green
                        $results.buildSucceeded = $true
                    } else {
                        Write-Host "  ❌ Build failed" -ForegroundColor Red
                        $results.errors += "Build failed"
                        if ($Verbose) { Write-Host "     $buildOutput" -ForegroundColor Gray }
                    }
                }
            } else {
                Write-Host "  ❌ npm install failed" -ForegroundColor Red
                $results.errors += "npm install failed"
                if ($Verbose) { Write-Host "     $installOutput" -ForegroundColor Gray }
            }
        } catch {
            Write-Host "  ❌ Node.js project error: $($_.Exception.Message)" -ForegroundColor Red
            $results.errors += $_.Exception.Message
        }
    }
    
    # Check other indicators
    if ($results.hasReadme) {
        Write-Host "  ✅ README.md found" -ForegroundColor Green
    }
    
    if ($results.hasTests) {
        Write-Host "  ✅ tests directory found" -ForegroundColor Green
    }
    
    if ($results.hasGitRepo) {
        Write-Host "  ✅ Git repository" -ForegroundColor Green
        
        # Check git status
        try {
            $gitStatus = git status --porcelain 2>$null
            if ($LASTEXITCODE -eq 0) {
                if ($gitStatus) {
                    Write-Host "  ⚠️  Uncommitted changes" -ForegroundColor Yellow
                } else {
                    Write-Host "  ✅ Working directory clean" -ForegroundColor Green
                }
            }
        } catch {
            # Silently skip git status errors
        }
    }
    
    if ($results.hasDockerfile) {
        Write-Host "  ✅ Dockerfile found" -ForegroundColor Green
    }
    
    Pop-Location
    Write-Host ""
    
    return $results
}

# Main execution
switch ($Action) {
    "test" {
        $allResults = @()
        
        if ($Project -eq "all") {
            foreach ($proj in $projects) {
                $result = Test-Project $proj.FullName $proj.Name
                $allResults += $result
            }
        } else {
            $targetProject = $projects | Where-Object { $_.Name -eq $Project }
            if ($targetProject) {
                $result = Test-Project $targetProject.FullName $targetProject.Name
                $allResults += $result
            } else {
                Write-Host "❌ Project '$Project' not found" -ForegroundColor Red
                Write-Host "Available projects: $($projects.Name -join ', ')" -ForegroundColor Gray
                return
            }
        }
        
        # Summary
        Write-Host "📊 Test Summary:" -ForegroundColor Cyan
        Write-Host "================" 
        
        $passed = ($allResults | Where-Object { $_.errors.Count -eq 0 }).Count
        $total = $allResults.Count
        
        foreach ($result in $allResults) {
            $status = if ($result.errors.Count -eq 0) { "✅" } else { "❌" }
            Write-Host "  $status $($result.name)" -ForegroundColor White
            
            if ($result.errors.Count -gt 0) {
                foreach ($error in $result.errors) {
                    Write-Host "     - $error" -ForegroundColor Red
                }
            }
        }
        
        Write-Host ""
        Write-Host "Results: $passed/$total projects passed" -ForegroundColor White
    }
    
    "status" {
        Write-Host "📊 Project Status Overview:" -ForegroundColor White
        Write-Host ""
        
        foreach ($proj in $projects) {
            Write-Host "📦 $($proj.Name)" -ForegroundColor White
            
            $projectPath = $proj.FullName
            
            # Quick checks
            $hasPackage = Test-Path (Join-Path $projectPath "package.json")
            $hasReadme = Test-Path (Join-Path $projectPath "README.md")
            $hasGit = Test-Path (Join-Path $projectPath ".git")
            
            Write-Host "  Node.js: $(if ($hasPackage) { "✅" } else { "❌" })" -NoNewline
            Write-Host "  README: $(if ($hasReadme) { "✅" } else { "❌" })" -NoNewline  
            Write-Host "  Git: $(if ($hasGit) { "✅" } else { "❌" })" -ForegroundColor Gray
            
            # Last modified
            $lastWrite = (Get-ChildItem $projectPath -Recurse -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1).LastWriteTime
            if ($lastWrite) {
                Write-Host "  Last modified: $($lastWrite.ToString('yyyy-MM-dd HH:mm'))" -ForegroundColor Gray
            }
            
            Write-Host ""
        }
    }
    
    default {
        Write-Host "📋 Available Commands:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  .\deploy-automation.ps1 test [project]    - Run tests (default: all projects)"
        Write-Host "  .\deploy-automation.ps1 status           - Show project status"
        Write-Host ""
        Write-Host "  Add -Verbose for detailed output"
        Write-Host ""
        Write-Host "Available projects: $($projects.Name -join ', ')" -ForegroundColor Gray
    }
}