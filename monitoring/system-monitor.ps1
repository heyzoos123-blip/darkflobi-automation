# DarkFlobi Proactive System Monitor
# Built for the Super Duo

param(
    [switch]$Detailed,
    [switch]$Silent
)

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

if (-not $Silent) {
    Write-Host "🦞 DarkFlobi System Monitor - $timestamp" -ForegroundColor Cyan
    Write-Host "=" * 50 -ForegroundColor Gray
}

# System Health Check
$cpu = Get-Counter "\Processor(_Total)\% Processor Time" -SampleInterval 1 -MaxSamples 1
$cpuUsage = [math]::Round(100 - $cpu.CounterSamples.CookedValue, 1)

$memory = Get-CimInstance Win32_OperatingSystem
$memUsage = [math]::Round((($memory.TotalVisibleMemorySize - $memory.FreePhysicalMemory) / $memory.TotalVisibleMemorySize) * 100, 1)

$disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
$diskUsage = [math]::Round((($disk.Size - $disk.FreeSpace) / $disk.Size) * 100, 1)

# Check for issues
$alerts = @()
if ($cpuUsage -gt 80) { $alerts += "HIGH CPU: $cpuUsage%" }
if ($memUsage -gt 85) { $alerts += "HIGH MEMORY: $memUsage%" }
if ($diskUsage -gt 90) { $alerts += "LOW DISK SPACE: $diskUsage%" }

# Downloads folder monitoring
$downloadsPath = "$env:USERPROFILE\Downloads"
$newFiles = Get-ChildItem $downloadsPath -File | Where-Object { $_.LastWriteTime -gt (Get-Date).AddHours(-1) } | Measure-Object
if ($newFiles.Count -gt 5) {
    $alerts += "NEW DOWNLOADS: $($newFiles.Count) files in last hour - organize?"
}

# Output results
$status = @{
    timestamp = $timestamp
    cpu_usage = "$cpuUsage%"
    memory_usage = "$memUsage%"
    disk_usage = "$diskUsage%"
    alerts = $alerts
    status = if ($alerts.Count -eq 0) { "ALL_GOOD" } else { "NEEDS_ATTENTION" }
}

if (-not $Silent) {
    Write-Host "CPU Usage: $cpuUsage%" -ForegroundColor Green
    Write-Host "Memory Usage: $memUsage%" -ForegroundColor Green  
    Write-Host "Disk Usage: $diskUsage%" -ForegroundColor Green
    
    if ($alerts.Count -gt 0) {
        Write-Host "`n🚨 ALERTS:" -ForegroundColor Yellow
        foreach ($alert in $alerts) {
            Write-Host "  - $alert" -ForegroundColor Red
        }
    } else {
        Write-Host "`n✅ All systems nominal" -ForegroundColor Green
    }
}

# Log results
$logPath = "$env:USERPROFILE\darkflobi-dev\monitoring\system-log.json"
$status | ConvertTo-Json | Add-Content $logPath

return $status