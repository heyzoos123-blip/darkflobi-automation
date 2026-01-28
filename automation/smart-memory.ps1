# Smart Memory Consolidation - Phase 3
# Automatically organizes, consolidates and learns from memory files

param(
    [string]$Action = "consolidate",
    [int]$DaysBack = 7,
    [switch]$DryRun,
    [switch]$Verbose
)

$memoryDir = "memory"
$consolidatedPath = "memory\consolidated-insights.md"
$learningDataPath = "memory\learning-data.json"

Write-Host "🧠 Smart Memory Consolidation" -ForegroundColor Magenta
Write-Host "=============================" 
Write-Host ""

function Get-MemoryFiles {
    param([int]$DaysBack)
    
    $cutoffDate = (Get-Date).AddDays(-$DaysBack)
    $files = @()
    
    if (Test-Path $memoryDir) {
        $memoryFiles = Get-ChildItem "$memoryDir\*.md" | Where-Object { 
            $_.Name -match "\d{4}-\d{2}-\d{2}\.md" -and $_.LastWriteTime -gt $cutoffDate
        } | Sort-Object Name
        
        $files += $memoryFiles
    }
    
    return $files
}

function Extract-KeyEvents {
    param($Content)
    
    $events = @()
    $lines = $Content -split "`n"
    
    foreach ($line in $lines) {
        $trimmed = $line.Trim()
        
        # Look for important markers
        if ($trimmed -match "^(##|###|\*\*|\d+\.|\-|\•)" -and $trimmed.Length -gt 10) {
            # Skip very generic headers
            if ($trimmed -notmatch "^(## \d{4}-\d{2}-\d{2}|### morning|### afternoon|### evening)$") {
                $events += @{
                    text = $trimmed
                    type = if ($trimmed -match "✅|completed|done|finished") { "achievement" }
                           elseif ($trimmed -match "❌|failed|error|problem") { "issue" }
                           elseif ($trimmed -match "🎯|goal|plan|next") { "goal" }
                           elseif ($trimmed -match "💡|learned|insight|discovery") { "learning" }
                           else { "event" }
                }
            }
        }
    }
    
    return $events
}

function Identify-Patterns {
    param($Events)
    
    $patterns = @{
        recurring_themes = @{}
        achievement_types = @{}
        common_issues = @{}
        learning_areas = @{}
    }
    
    foreach ($event in $Events) {
        $text = $event.text.ToLower()
        
        # Extract keywords (simple approach)
        $keywords = @()
        if ($text -match "email") { $keywords += "email" }
        if ($text -match "github|git|repo") { $keywords += "development" }
        if ($text -match "backup|save") { $keywords += "backup" }
        if ($text -match "weather") { $keywords += "weather" }
        if ($text -match "automation|script") { $keywords += "automation" }
        if ($text -match "learning|ai|bot") { $keywords += "ai_development" }
        if ($text -match "trade|trading|solana") { $keywords += "trading" }
        
        foreach ($keyword in $keywords) {
            if ($patterns.recurring_themes.ContainsKey($keyword)) {
                $patterns.recurring_themes[$keyword]++
            } else {
                $patterns.recurring_themes[$keyword] = 1
            }
        }
        
        # Categorize by event type
        $eventType = $event.type
        if ($patterns.achievement_types.ContainsKey($eventType)) {
            $patterns.achievement_types[$eventType]++
        } else {
            $patterns.achievement_types[$eventType] = 1
        }
    }
    
    return $patterns
}

function Generate-Insights {
    param($Patterns, $Events)
    
    $insights = @()
    
    # Theme analysis
    $topThemes = $Patterns.recurring_themes.GetEnumerator() | 
                 Sort-Object Value -Descending | 
                 Select-Object -First 5
    
    if ($topThemes) {
        $themeText = ($topThemes | ForEach-Object { "$($_.Key) ($($_.Value)x)" }) -join ", "
        $insights += "**Top focus areas:** $themeText"
    }
    
    # Achievement analysis
    $achievements = $Patterns.achievement_types.GetEnumerator() | Sort-Object Value -Descending
    if ($achievements) {
        $achievementText = ($achievements | ForEach-Object { "$($_.Key): $($_.Value)" }) -join ", "
        $insights += "**Activity breakdown:** $achievementText"
    }
    
    # Progress assessment
    $achievementEvents = $Events | Where-Object { $_.type -eq "achievement" }
    $issueEvents = $Events | Where-Object { $_.type -eq "issue" }
    
    if ($achievementEvents.Count -gt 0) {
        $ratio = if ($issueEvents.Count -gt 0) { 
            [math]::Round($achievementEvents.Count / ($achievementEvents.Count + $issueEvents.Count) * 100, 1) 
        } else { 100 }
        $insights += "**Success rate:** $ratio% ($($achievementEvents.Count) achievements, $($issueEvents.Count) issues)"
    }
    
    # Learning trajectory
    $learningEvents = $Events | Where-Object { $_.type -eq "learning" }
    if ($learningEvents.Count -gt 0) {
        $insights += "**Learning velocity:** $($learningEvents.Count) insights gained"
    }
    
    return $insights
}

function Create-ConsolidatedEntry {
    param($DateRange, $Insights, $KeyEvents)
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $entry = @"
## Consolidated Analysis: $DateRange
*Generated: $timestamp*

### Key Insights
$(($Insights | ForEach-Object { "- $_" }) -join "`n")

### Significant Events
$(($KeyEvents | Select-Object -First 10 | ForEach-Object { "- $($_.text)" }) -join "`n")

### Pattern Summary
- **Total events analyzed:** $($KeyEvents.Count)
- **Analysis period:** $DateRange
- **Consolidation method:** Automated pattern recognition

---

"@
    
    return $entry
}

# Main execution
switch ($Action) {
    "consolidate" {
        Write-Host "🔍 Analyzing memory files from last $DaysBack days..." -ForegroundColor White
        
        $memoryFiles = Get-MemoryFiles $DaysBack
        
        if ($memoryFiles.Count -eq 0) {
            Write-Host "⚠️  No memory files found in the specified range" -ForegroundColor Yellow
            return
        }
        
        Write-Host "📚 Found $($memoryFiles.Count) memory files to analyze:" -ForegroundColor Gray
        foreach ($file in $memoryFiles) {
            Write-Host "  • $($file.Name)" -ForegroundColor Gray
        }
        Write-Host ""
        
        # Extract and analyze all events
        $allEvents = @()
        foreach ($file in $memoryFiles) {
            $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
            if ($content) {
                $events = Extract-KeyEvents $content
                $allEvents += $events
                
                if ($Verbose) {
                    Write-Host "📄 $($file.Name): $($events.Count) events extracted" -ForegroundColor Gray
                }
            }
        }
        
        if ($allEvents.Count -eq 0) {
            Write-Host "⚠️  No significant events found to consolidate" -ForegroundColor Yellow
            return
        }
        
        Write-Host "🎯 Extracted $($allEvents.Count) significant events" -ForegroundColor Green
        
        # Identify patterns
        $patterns = Identify-Patterns $allEvents
        
        # Generate insights
        $insights = Generate-Insights $patterns $allEvents
        
        # Create consolidated entry
        $dateRange = "$($memoryFiles[0].BaseName) to $($memoryFiles[-1].BaseName)"
        $consolidatedEntry = Create-ConsolidatedEntry $dateRange $insights $allEvents
        
        if ($DryRun) {
            Write-Host "🔍 DRY RUN - Would add this to consolidated insights:" -ForegroundColor Yellow
            Write-Host $consolidatedEntry -ForegroundColor Gray
        } else {
            # Append to consolidated insights file
            if (Test-Path $consolidatedPath) {
                $existingContent = Get-Content $consolidatedPath -Raw
                $newContent = $consolidatedEntry + "`n" + $existingContent
            } else {
                $header = @"
# Consolidated Memory Insights
*Auto-generated analysis of daily memory patterns*

This file contains automated consolidations of daily memories, identifying patterns, themes, and learning progressions over time.

"@
                $newContent = $header + "`n" + $consolidatedEntry
            }
            
            $newContent | Out-File -FilePath $consolidatedPath -Encoding UTF8
            
            Write-Host "✅ Consolidated insights saved to: $consolidatedPath" -ForegroundColor Green
        }
        
        # Display insights
        Write-Host ""
        Write-Host "💡 Key Insights:" -ForegroundColor Cyan
        foreach ($insight in $insights) {
            Write-Host "  $insight" -ForegroundColor White
        }
    }
    
    "analyze" {
        Write-Host "📊 Memory Analysis Report:" -ForegroundColor Cyan
        Write-Host ""
        
        $memoryFiles = Get-MemoryFiles $DaysBack
        
        if ($memoryFiles.Count -eq 0) {
            Write-Host "⚠️  No memory files found" -ForegroundColor Yellow
            return
        }
        
        # Quick stats
        $totalSize = ($memoryFiles | Measure-Object Length -Sum).Sum
        Write-Host "📚 Memory Stats:" -ForegroundColor White
        Write-Host "  Files: $($memoryFiles.Count)" -ForegroundColor Gray
        Write-Host "  Size: $([math]::Round($totalSize/1KB, 1)) KB" -ForegroundColor Gray
        Write-Host "  Date range: $($memoryFiles[0].BaseName) to $($memoryFiles[-1].BaseName)" -ForegroundColor Gray
        Write-Host ""
        
        # Extract all events for analysis
        $allEvents = @()
        foreach ($file in $memoryFiles) {
            $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
            if ($content) {
                $events = Extract-KeyEvents $content
                $allEvents += $events
            }
        }
        
        if ($allEvents.Count -gt 0) {
            $patterns = Identify-Patterns $allEvents
            
            Write-Host "🔍 Pattern Analysis:" -ForegroundColor White
            Write-Host "  Total events: $($allEvents.Count)" -ForegroundColor Gray
            
            if ($patterns.recurring_themes.Count -gt 0) {
                Write-Host "  Top themes:" -ForegroundColor Gray
                $topThemes = $patterns.recurring_themes.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 5
                foreach ($theme in $topThemes) {
                    Write-Host "    • $($theme.Key): $($theme.Value) mentions" -ForegroundColor Gray
                }
            }
            
            if ($patterns.achievement_types.Count -gt 0) {
                Write-Host "  Event types:" -ForegroundColor Gray
                foreach ($type in $patterns.achievement_types.GetEnumerator()) {
                    Write-Host "    • $($type.Key): $($type.Value)" -ForegroundColor Gray
                }
            }
        }
    }
    
    "cleanup" {
        Write-Host "🧹 Memory Cleanup Analysis:" -ForegroundColor Yellow
        
        if (!(Test-Path $memoryDir)) {
            Write-Host "⚠️  Memory directory not found" -ForegroundColor Yellow
            return
        }
        
        $allFiles = Get-ChildItem "$memoryDir\*.md"
        $oldFiles = $allFiles | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) }
        
        Write-Host "📊 Memory directory status:" -ForegroundColor White
        Write-Host "  Total files: $($allFiles.Count)" -ForegroundColor Gray
        Write-Host "  Files >30 days old: $($oldFiles.Count)" -ForegroundColor Gray
        
        if ($oldFiles.Count -gt 0) {
            $oldSize = ($oldFiles | Measure-Object Length -Sum).Sum
            Write-Host "  Old files size: $([math]::Round($oldSize/1KB, 1)) KB" -ForegroundColor Gray
            
            if (!$DryRun) {
                Write-Host "  Note: Use consolidate action to preserve insights before cleanup" -ForegroundColor Yellow
            }
        }
    }
    
    default {
        Write-Host "📋 Smart Memory Commands:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  consolidate    - Analyze and consolidate recent memories"
        Write-Host "  analyze        - Analyze memory patterns without consolidating"
        Write-Host "  cleanup        - Show memory cleanup opportunities"
        Write-Host ""
        Write-Host "Options:" -ForegroundColor Gray
        Write-Host "  -DaysBack <n>  - Days to look back (default: 7)"
        Write-Host "  -DryRun        - Preview without making changes"
        Write-Host "  -Verbose       - Show detailed processing info"
        Write-Host ""
        Write-Host "Examples:" -ForegroundColor Gray
        Write-Host "  .\smart-memory.ps1 consolidate -DaysBack 14"
        Write-Host "  .\smart-memory.ps1 analyze -DaysBack 30 -Verbose"
        Write-Host ""
    }
}