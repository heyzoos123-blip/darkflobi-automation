# Project Monitoring & CI Status
# Part of Phase 2: Development Powerhouse

$ghPath = "C:\Program Files\GitHub CLI\gh.exe"

Write-Host "📊 Project Monitor Dashboard" -ForegroundColor Cyan
Write-Host "============================" 
Write-Host ""

# Check authentication first
$authTest = & $ghPath auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  GitHub authentication required" -ForegroundColor Yellow
    Write-Host "   Run: gh auth login --web" -ForegroundColor Gray
    Write-Host ""
    return
}

Write-Host "✅ GitHub authenticated" -ForegroundColor Green
Write-Host ""

try {
    # Get user repos
    Write-Host "📚 Your Recent Repositories:" -ForegroundColor White
    $repos = & $ghPath repo list --limit 5 --json name,description,visibility,pushedAt,isPrivate
    $repoData = $repos | ConvertFrom-Json
    
    foreach ($repo in $repoData) {
        $pushed = [DateTime]::Parse($repo.pushedAt).ToString("MM/dd HH:mm")
        $privacy = if ($repo.isPrivate) { "🔒" } else { "🌍" }
        
        Write-Host "  $privacy $($repo.name)" -ForegroundColor White
        if ($repo.description) {
            Write-Host "    $($repo.description)" -ForegroundColor Gray
        }
        Write-Host "    Last push: $pushed" -ForegroundColor Gray
        Write-Host ""
    }
    
    # Check recent workflow runs (if any repos have actions)
    Write-Host "🔄 Recent CI/CD Activity:" -ForegroundColor White
    
    foreach ($repo in $repoData | Select-Object -First 3) {
        try {
            $runs = & $ghPath run list --repo $repo.name --limit 3 --json status,conclusion,workflowName,createdAt 2>$null
            if ($LASTEXITCODE -eq 0 -and $runs) {
                $runsData = $runs | ConvertFrom-Json
                
                if ($runsData.Count -gt 0) {
                    Write-Host "  📦 $($repo.name):" -ForegroundColor White
                    
                    foreach ($run in $runsData) {
                        $status = switch ($run.conclusion) {
                            "success" { "✅" }
                            "failure" { "❌" }
                            "cancelled" { "⚠️" }
                            default { "🔄" }
                        }
                        
                        $created = [DateTime]::Parse($run.createdAt).ToString("MM/dd HH:mm")
                        Write-Host "    $status $($run.workflowName) - $created" -ForegroundColor Gray
                    }
                    Write-Host ""
                }
            }
        } catch {
            # Silently skip repos without workflows
        }
    }
    
} catch {
    Write-Host "❌ Error fetching data: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "🔧 Development Commands:" -ForegroundColor Yellow
Write-Host "  gh repo list                 - List all repositories"
Write-Host "  gh issue list --repo REPO    - View issues for a repo"
Write-Host "  gh pr list --repo REPO       - View pull requests"
Write-Host "  gh run list --repo REPO      - View CI/CD runs"
Write-Host ""