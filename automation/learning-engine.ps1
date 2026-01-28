# Learning Engine - Phase 3: AI Pattern Recognition & Adaptation
# Learns your routines, preferences, and adapts behavior over time

param(
    [string]$Action = "status",
    [string]$Data = "",
    [switch]$Verbose
)

$learningDataPath = "memory\learning-data.json"
$patternsPath = "memory\patterns.json"

Write-Host "🧠 Learning Engine - Phase 3" -ForegroundColor Magenta
Write-Host "============================" 
Write-Host ""

# Initialize learning data structure
function Initialize-LearningData {
    $defaultData = @{
        version = "1.0"
        lastUpdate = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        userPreferences = @{
            communicationStyle = "casual"  # casual, technical, formal
            responseLength = "concise"     # brief, concise, detailed
            emojiUsage = "moderate"        # minimal, moderate, frequent
            timeZone = "America/New_York"
            workingHours = @{
                start = "09:00"
                end = "18:00"
                workDays = @("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
            }
        }
        patterns = @{
            dailyRoutines = @{}
            interactionTimes = @()
            topicPreferences = @{}
            taskPatterns = @{}
            responseEffectiveness = @{}
        }
        adaptations = @{
            responseStyleAdjustments = @()
            proactiveTimingPreferences = @()
            topicInterestLevels = @{}
        }
        learningStats = @{
            totalInteractions = 0
            patternsIdentified = 0
            adaptationsMade = 0
            accuracyScore = 0.0
        }
    }
    
    return $defaultData
}

function Get-LearningData {
    if (Test-Path $learningDataPath) {
        try {
            $data = Get-Content $learningDataPath | ConvertFrom-Json
            return $data
        } catch {
            Write-Host "⚠️  Corrupted learning data, reinitializing..." -ForegroundColor Yellow
            return Initialize-LearningData
        }
    } else {
        return Initialize-LearningData
    }
}

function Save-LearningData {
    param($Data)
    
    $Data.lastUpdate = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    
    # Ensure directory exists
    $dir = Split-Path $learningDataPath -Parent
    if (!(Test-Path $dir)) {
        New-Item -Path $dir -ItemType Directory -Force | Out-Null
    }
    
    $Data | ConvertTo-Json -Depth 6 | Out-File -FilePath $learningDataPath -Encoding UTF8
}

function Record-Interaction {
    param(
        [string]$Type,
        [string]$Context,
        [string]$Response,
        [string]$Feedback = ""
    )
    
    $data = Get-LearningData
    
    $interaction = @{
        timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        type = $Type
        context = $Context
        response = $Response
        feedback = $Feedback
        dayOfWeek = (Get-Date).DayOfWeek.ToString()
        hour = (Get-Date).Hour
    }
    
    # Track interaction times
    $data.patterns.interactionTimes += $interaction.timestamp
    
    # Update stats
    $data.learningStats.totalInteractions++
    
    # Analyze patterns
    $hourKey = "hour_$($interaction.hour)"
    if ($data.patterns.dailyRoutines.ContainsKey($hourKey)) {
        $data.patterns.dailyRoutines[$hourKey]++
    } else {
        $data.patterns.dailyRoutines[$hourKey] = 1
    }
    
    Save-LearningData $data
    
    if ($Verbose) {
        Write-Host "📝 Recorded interaction: $Type at $($interaction.timestamp)" -ForegroundColor Gray
    }
}

function Analyze-Patterns {
    $data = Get-LearningData
    
    Write-Host "🔍 Pattern Analysis:" -ForegroundColor Cyan
    Write-Host ""
    
    # Most active hours
    $hourlyActivity = @{}
    foreach ($key in $data.patterns.dailyRoutines.Keys) {
        if ($key -match "hour_(\d+)") {
            $hour = [int]$matches[1]
            $hourlyActivity[$hour] = $data.patterns.dailyRoutines[$key]
        }
    }
    
    if ($hourlyActivity.Count -gt 0) {
        $topHours = $hourlyActivity.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 3
        Write-Host "📊 Most Active Hours:" -ForegroundColor White
        foreach ($hour in $topHours) {
            $timeStr = "{0:D2}:00" -f $hour.Key
            Write-Host "  🕐 $timeStr - $($hour.Value) interactions" -ForegroundColor Gray
        }
        Write-Host ""
    }
    
    # Interaction frequency
    $totalInteractions = $data.learningStats.totalInteractions
    if ($totalInteractions -gt 0) {
        $recentInteractions = ($data.patterns.interactionTimes | Where-Object { 
            $timestamp = [DateTime]::ParseExact($_, "yyyy-MM-dd HH:mm:ss", $null)
            $timestamp -gt (Get-Date).AddDays(-7)
        }).Count
        
        Write-Host "📈 Activity Summary:" -ForegroundColor White
        Write-Host "  Total interactions: $totalInteractions" -ForegroundColor Gray
        Write-Host "  Last 7 days: $recentInteractions" -ForegroundColor Gray
        Write-Host "  Daily average: $([math]::Round($recentInteractions/7, 1))" -ForegroundColor Gray
        Write-Host ""
    }
    
    # Identify patterns and suggest adaptations
    $suggestions = @()
    
    # Peak activity time suggestions
    if ($hourlyActivity.Count -gt 0) {
        $peakHour = ($hourlyActivity.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 1).Key
        $suggestions += "Consider proactive check-ins around ${peakHour}:00 (your most active hour)"
    }
    
    # Working hours detection
    $workHours = $hourlyActivity.GetEnumerator() | Where-Object { $_.Key -ge 9 -and $_.Key -le 17 }
    $nonWorkHours = $hourlyActivity.GetEnumerator() | Where-Object { $_.Key -lt 9 -or $_.Key -gt 17 }
    
    $workTotal = ($workHours | Measure-Object Value -Sum).Sum
    $nonWorkTotal = ($nonWorkHours | Measure-Object Value -Sum).Sum
    
    if ($workTotal -gt 0 -and $nonWorkTotal -gt 0) {
        if ($nonWorkTotal -gt $workTotal) {
            $suggestions += "You're more active outside 9-5 hours - adjusting 'working hours' concept"
        }
    }
    
    if ($suggestions.Count -gt 0) {
        Write-Host "💡 Learning Insights:" -ForegroundColor Yellow
        foreach ($suggestion in $suggestions) {
            Write-Host "  • $suggestion" -ForegroundColor White
        }
        Write-Host ""
    }
    
    return $data
}

function Adapt-Behavior {
    param([string]$Adaptation, [string]$Reason)
    
    $data = Get-LearningData
    
    $adaptationRecord = @{
        timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        adaptation = $Adaptation
        reason = $Reason
        effectiveness = 0.0  # To be updated based on future feedback
    }
    
    $data.adaptations.responseStyleAdjustments += $adaptationRecord
    $data.learningStats.adaptationsMade++
    
    Save-LearningData $data
    
    Write-Host "🎯 Behavioral Adaptation Applied:" -ForegroundColor Green
    Write-Host "  Change: $Adaptation" -ForegroundColor White
    Write-Host "  Reason: $Reason" -ForegroundColor Gray
    Write-Host ""
}

function Generate-PersonalityProfile {
    $data = Get-LearningData
    
    Write-Host "👤 Your Interaction Profile:" -ForegroundColor Cyan
    Write-Host ""
    
    # Communication style analysis
    $prefs = $data.userPreferences
    Write-Host "🗣️  Communication Style: $($prefs.communicationStyle)" -ForegroundColor White
    Write-Host "📏 Response Length: $($prefs.responseLength)" -ForegroundColor White
    Write-Host "😄 Emoji Usage: $($prefs.emojiUsage)" -ForegroundColor White
    Write-Host ""
    
    # Activity patterns
    $totalInteractions = $data.learningStats.totalInteractions
    if ($totalInteractions -gt 10) {
        Write-Host "📊 Activity Patterns:" -ForegroundColor White
        
        # Day/night preference
        $morningHours = @(6,7,8,9,10,11)
        $afternoonHours = @(12,13,14,15,16,17)
        $eveningHours = @(18,19,20,21,22)
        $nightHours = @(23,0,1,2,3,4,5)
        
        $patterns = $data.patterns.dailyRoutines
        $morningCount = $morningHours | ForEach-Object { if ($patterns["hour_$_"]) { $patterns["hour_$_"] } else { 0 } } | Measure-Object -Sum | Select-Object -ExpandProperty Sum
        $afternoonCount = $afternoonHours | ForEach-Object { if ($patterns["hour_$_"]) { $patterns["hour_$_"] } else { 0 } } | Measure-Object -Sum | Select-Object -ExpandProperty Sum
        $eveningCount = $eveningHours | ForEach-Object { if ($patterns["hour_$_"]) { $patterns["hour_$_"] } else { 0 } } | Measure-Object -Sum | Select-Object -ExpandProperty Sum
        $nightCount = $nightHours | ForEach-Object { if ($patterns["hour_$_"]) { $patterns["hour_$_"] } else { 0 } } | Measure-Object -Sum | Select-Object -ExpandProperty Sum
        
        $timePrefs = @{
            "Morning Person" = $morningCount
            "Afternoon Active" = $afternoonCount  
            "Evening Engaged" = $eveningCount
            "Night Owl" = $nightCount
        }
        
        $topTimeSlot = ($timePrefs.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 1)
        Write-Host "  ⏰ You're a: $($topTimeSlot.Key)" -ForegroundColor Green
        Write-Host ""
    }
    
    # Learning stats
    Write-Host "📈 Learning Progress:" -ForegroundColor White
    Write-Host "  Interactions analyzed: $($data.learningStats.totalInteractions)" -ForegroundColor Gray
    Write-Host "  Patterns identified: $($data.learningStats.patternsIdentified)" -ForegroundColor Gray
    Write-Host "  Adaptations made: $($data.learningStats.adaptationsMade)" -ForegroundColor Gray
    Write-Host ""
}

# Main execution
switch ($Action) {
    "status" {
        $data = Get-LearningData
        
        Write-Host "🎯 Learning Engine Status:" -ForegroundColor White
        Write-Host "  Version: $($data.version)" -ForegroundColor Gray
        Write-Host "  Last update: $($data.lastUpdate)" -ForegroundColor Gray
        Write-Host "  Total interactions: $($data.learningStats.totalInteractions)" -ForegroundColor Gray
        Write-Host ""
        
        if ($data.learningStats.totalInteractions -eq 0) {
            Write-Host "🌱 Learning engine initialized but no data yet" -ForegroundColor Yellow
            Write-Host "   Start by recording some interactions!" -ForegroundColor Gray
        } else {
            Generate-PersonalityProfile
        }
    }
    
    "record" {
        if ($Data) {
            $parts = $Data -split ":"
            if ($parts.Count -ge 3) {
                Record-Interaction $parts[0] $parts[1] $parts[2] 
                Write-Host "✅ Interaction recorded" -ForegroundColor Green
            } else {
                Write-Host "❌ Format: record 'type:context:response'" -ForegroundColor Red
            }
        } else {
            Write-Host "❌ No data provided for recording" -ForegroundColor Red
        }
    }
    
    "analyze" {
        Analyze-Patterns | Out-Null
    }
    
    "adapt" {
        if ($Data) {
            $parts = $Data -split ":"
            if ($parts.Count -ge 2) {
                Adapt-Behavior $parts[0] $parts[1]
            } else {
                Write-Host "❌ Format: adapt 'change:reason'" -ForegroundColor Red
            }
        } else {
            Write-Host "❌ No adaptation data provided" -ForegroundColor Red
        }
    }
    
    "profile" {
        Generate-PersonalityProfile
    }
    
    "reset" {
        Write-Host "🔄 Resetting learning data..." -ForegroundColor Yellow
        $newData = Initialize-LearningData
        Save-LearningData $newData
        Write-Host "✅ Learning data reset to defaults" -ForegroundColor Green
    }
    
    default {
        Write-Host "📋 Learning Engine Commands:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  status     - Show learning engine status"
        Write-Host "  record     - Record interaction (format: 'type:context:response')"
        Write-Host "  analyze    - Analyze patterns and generate insights"
        Write-Host "  adapt      - Apply behavioral adaptation (format: 'change:reason')"
        Write-Host "  profile    - Generate your interaction profile"
        Write-Host "  reset      - Reset all learning data"
        Write-Host ""
        Write-Host "Examples:" -ForegroundColor Gray
        Write-Host "  .\learning-engine.ps1 record 'question:weather:provided_forecast'"
        Write-Host "  .\learning-engine.ps1 adapt 'more_concise:user_prefers_brief_responses'"
        Write-Host ""
    }
}