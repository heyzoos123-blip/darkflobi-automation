# Automated Backup System
# Part of Phase 2: Development Powerhouse

param(
    [string]$Action = "create",
    [switch]$Verbose
)

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm"
$baseBackupDir = "backups"

Write-Host "💾 Automated Backup System" -ForegroundColor Cyan
Write-Host "===========================" 
Write-Host ""

# Ensure backup directory exists
if (!(Test-Path $baseBackupDir)) {
    New-Item -Path $baseBackupDir -ItemType Directory -Force | Out-Null
    Write-Host "📁 Created backups directory" -ForegroundColor Green
}

switch ($Action) {
    "create" {
        $backupDir = Join-Path $baseBackupDir $timestamp
        Write-Host "🚀 Creating backup: $timestamp" -ForegroundColor White
        
        New-Item -Path $backupDir -ItemType Directory -Force | Out-Null
        
        # Define what to backup
        $backupTargets = @(
            @{ Path = "projects\*"; Name = "Projects" },
            @{ Path = "scripts\*"; Name = "Scripts" },
            @{ Path = "automation\*"; Name = "Automation" },
            @{ Path = "*.md"; Name = "Documentation" },
            @{ Path = "memory\*"; Name = "Memory System" },
            @{ Path = "*.json"; Name = "Configuration" }
        )
        
        $totalFiles = 0
        $totalSize = 0
        
        foreach ($target in $backupTargets) {
            Write-Host "📦 Backing up: $($target.Name)..." -ForegroundColor Gray
            
            $files = Get-ChildItem $target.Path -Recurse -File -ErrorAction SilentlyContinue
            $count = 0
            
            foreach ($file in $files) {
                try {
                    $relativePath = $file.FullName.Replace((Get-Location).Path + "\", "")
                    $backupPath = Join-Path $backupDir $relativePath
                    $backupFolder = Split-Path $backupPath -Parent
                    
                    if (!(Test-Path $backupFolder)) {
                        New-Item -Path $backupFolder -ItemType Directory -Force | Out-Null
                    }
                    
                    Copy-Item $file.FullName $backupPath -Force
                    $totalSize += $file.Length
                    $count++
                    
                    if ($Verbose) {
                        Write-Host "  ✅ $relativePath" -ForegroundColor Green
                    }
                } catch {
                    if ($Verbose) {
                        Write-Host "  ❌ Failed: $($file.Name)" -ForegroundColor Red
                    }
                }
            }
            
            if ($count -gt 0) {
                Write-Host "  ✅ $count files backed up" -ForegroundColor Green
                $totalFiles += $count
            } else {
                Write-Host "  ⚠️  No files found" -ForegroundColor Yellow
            }
        }
        
        # Create backup manifest
        $manifest = @{
            timestamp = $timestamp
            totalFiles = $totalFiles
            totalSizeMB = [math]::Round($totalSize / 1MB, 2)
            targets = $backupTargets.Name
            createdBy = "darkflobi-automation"
        }
        
        $manifest | ConvertTo-Json -Depth 3 | Out-File -FilePath (Join-Path $backupDir "backup-manifest.json") -Encoding UTF8
        
        Write-Host ""
        Write-Host "✅ Backup completed!" -ForegroundColor Green
        Write-Host "📊 Stats: $totalFiles files, $([math]::Round($totalSize / 1MB, 2)) MB" -ForegroundColor White
        Write-Host "📍 Location: $backupDir" -ForegroundColor Gray
    }
    
    "list" {
        Write-Host "📋 Available Backups:" -ForegroundColor White
        Write-Host ""
        
        $backups = Get-ChildItem $baseBackupDir -Directory | Sort-Object Name -Descending
        
        if ($backups.Count -eq 0) {
            Write-Host "  No backups found" -ForegroundColor Gray
            return
        }
        
        foreach ($backup in $backups | Select-Object -First 10) {
            $manifestPath = Join-Path $backup.FullName "backup-manifest.json"
            
            if (Test-Path $manifestPath) {
                $manifest = Get-Content $manifestPath | ConvertFrom-Json
                Write-Host "  📦 $($backup.Name)" -ForegroundColor White
                Write-Host "     Files: $($manifest.totalFiles), Size: $($manifest.totalSizeMB) MB" -ForegroundColor Gray
            } else {
                # Legacy backup without manifest
                $size = (Get-ChildItem $backup.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
                Write-Host "  📦 $($backup.Name)" -ForegroundColor White
                Write-Host "     Size: $([math]::Round($size, 2)) MB" -ForegroundColor Gray
            }
        }
        
        if ($backups.Count -gt 10) {
            Write-Host "  ... and $($backups.Count - 10) older backups" -ForegroundColor Gray
        }
    }
    
    "cleanup" {
        Write-Host "🧹 Cleaning up old backups..." -ForegroundColor Yellow
        
        $backups = Get-ChildItem $baseBackupDir -Directory | Sort-Object CreationTime -Descending
        $toKeep = 5  # Keep 5 most recent backups
        
        if ($backups.Count -le $toKeep) {
            Write-Host "✅ No cleanup needed (have $($backups.Count), keeping $toKeep)" -ForegroundColor Green
            return
        }
        
        $toDelete = $backups | Select-Object -Skip $toKeep
        
        Write-Host "🗑️  Removing $($toDelete.Count) old backups..." -ForegroundColor White
        
        foreach ($backup in $toDelete) {
            Write-Host "  Deleting: $($backup.Name)" -ForegroundColor Gray
            Remove-Item $backup.FullName -Recurse -Force
        }
        
        Write-Host "✅ Cleanup complete! Kept $toKeep most recent backups" -ForegroundColor Green
    }
    
    default {
        Write-Host "📋 Available Commands:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  .\backup-system.ps1 create     - Create new backup"
        Write-Host "  .\backup-system.ps1 list       - List available backups"
        Write-Host "  .\backup-system.ps1 cleanup    - Remove old backups"
        Write-Host ""
        Write-Host "  Add -Verbose for detailed output"
    }
}