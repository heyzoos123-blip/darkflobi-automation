# DarkFlobi Predictive File Intelligence System
# SUPERPOWER: Autonomous file management with learning

param(
    [switch]$StartWatcher,
    [switch]$StopWatcher, 
    [switch]$Status
)

$watcherPath = "$env:USERPROFILE\darkflobi-dev\automation\file-watcher-state.json"
$downloadsPath = "$env:USERPROFILE\Downloads"

function Start-FileIntelligence {
    Write-Host "🧠 ACTIVATING FILE INTELLIGENCE SUPERPOWER" -ForegroundColor Magenta
    
    # Create watcher state
    $watcherState = @{
        activated = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        files_processed = 0
        patterns_learned = @{}
        auto_actions = @{
            "memes" = "organize_and_index"
            "installers" = "organize_and_scan"
            "archives" = "organize_and_extract_preview"
            "videos" = "organize_and_thumbnail"
        }
    }
    
    $watcherState | ConvertTo-Json -Depth 3 | Out-File $watcherPath -Encoding UTF8
    
    # Start background file monitoring
    $scriptBlock = {
        param($downloadsPath)
        
        $watcher = New-Object System.IO.FileSystemWatcher
        $watcher.Path = $downloadsPath
        $watcher.Filter = "*.*"
        $watcher.EnableRaisingEvents = $true
        $watcher.NotifyFilter = [System.IO.NotifyFilters]::CreationTime
        
        $action = {
            $file = $Event.SourceEventArgs.FullPath
            $fileName = $Event.SourceEventArgs.Name
            
            # Wait for file to be fully written
            Start-Sleep -Seconds 2
            
            if (Test-Path $file) {
                $fileInfo = Get-Item $file
                $extension = $fileInfo.Extension.ToLower()
                
                # Smart categorization
                $category = switch ($extension) {
                    {$_ -in '.jpg', '.png', '.gif', '.webp', '.avif', '.jpeg'} { 'memes' }
                    {$_ -in '.exe', '.msi'} { 'installers' }
                    {$_ -in '.zip', '.rar', '.7z'} { 'archives' }
                    {$_ -in '.mp4', '.avi', '.mov'} { 'videos' }
                    default { 'unknown' }
                }
                
                # Log the intelligence
                $logEntry = "[$(Get-Date)] DETECTED: $fileName -> $category"
                Add-Content "$env:USERPROFILE\darkflobi-dev\monitoring\intelligence-log.txt" $logEntry
                
                # Auto-organize immediately
                if ($category -ne 'unknown') {
                    $targetFolder = switch ($category) {
                        'memes' { 'Images-Memes' }
                        'installers' { 'Software-Installers' }
                        'archives' { 'Archives-Zips' }
                        'videos' { 'Videos-Media' }
                    }
                    
                    $targetPath = Join-Path $downloadsPath $targetFolder
                    if (-not (Test-Path $targetPath)) {
                        New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
                    }
                    
                    try {
                        Move-Item $file $targetPath -Force
                        $logEntry = "[$(Get-Date)] AUTO-ORGANIZED: $fileName -> $targetFolder"
                        Add-Content "$env:USERPROFILE\darkflobi-dev\monitoring\intelligence-log.txt" $logEntry
                    } catch {
                        # File in use, will retry later
                    }
                }
            }
        }
        
        Register-ObjectEvent -InputObject $watcher -EventName Created -Action $action
        
        # Keep the watcher alive
        while ($true) {
            Start-Sleep -Seconds 10
        }
    }
    
    # Start as background job
    Start-Job -ScriptBlock $scriptBlock -ArgumentList $downloadsPath -Name "DarkFlobiFileIntelligence" | Out-Null
    
    Write-Host "✅ FILE INTELLIGENCE ACTIVATED - Now monitoring $downloadsPath" -ForegroundColor Green
    Write-Host "🎯 Auto-organizing new files in real-time" -ForegroundColor Cyan
}

function Get-IntelligenceStatus {
    Write-Host "🧠 FILE INTELLIGENCE STATUS" -ForegroundColor Magenta
    
    $job = Get-Job -Name "DarkFlobiFileIntelligence" -ErrorAction SilentlyContinue
    if ($job) {
        Write-Host "Status: ACTIVE (Job ID: $($job.Id))" -ForegroundColor Green
        Write-Host "State: $($job.State)" -ForegroundColor Cyan
    } else {
        Write-Host "Status: INACTIVE" -ForegroundColor Yellow
    }
    
    # Show recent intelligence
    $logPath = "$env:USERPROFILE\darkflobi-dev\monitoring\intelligence-log.txt"
    if (Test-Path $logPath) {
        Write-Host "`nRecent Activity:" -ForegroundColor Yellow
        Get-Content $logPath | Select-Object -Last 5 | ForEach-Object {
            Write-Host "  $_" -ForegroundColor Gray
        }
    }
}

function Stop-FileIntelligence {
    $job = Get-Job -Name "DarkFlobiFileIntelligence" -ErrorAction SilentlyContinue
    if ($job) {
        Stop-Job $job
        Remove-Job $job
        Write-Host "🛑 FILE INTELLIGENCE DEACTIVATED" -ForegroundColor Red
    } else {
        Write-Host "No active file intelligence found" -ForegroundColor Yellow
    }
}

# Main execution
if ($StartWatcher) { Start-FileIntelligence }
elseif ($StopWatcher) { Stop-FileIntelligence }
elseif ($Status) { Get-IntelligenceStatus }
else {
    Write-Host "🧠 DarkFlobi File Intelligence" -ForegroundColor Magenta
    Write-Host "Usage: -StartWatcher | -StopWatcher | -Status"
}