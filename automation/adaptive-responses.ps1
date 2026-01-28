# Adaptive Response System - Phase 3
# Dynamically adjusts communication style based on context and learned preferences

param(
    [string]$Action = "analyze",
    [string]$Context = "",
    [string]$Message = "",
    [switch]$Verbose
)

$responsePatternsPath = "memory\response-patterns.json"
$learningDataPath = "memory\learning-data.json"

Write-Host "🎭 Adaptive Response System" -ForegroundColor Magenta
Write-Host "===========================" 
Write-Host ""

# Initialize response patterns data
function Initialize-ResponsePatterns {
    $defaultPatterns = @{
        version = "1.0"
        lastUpdate = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        contexts = @{
            technical = @{
                responseLength = "detailed"
                emojiUsage = "minimal"
                formality = "professional"
                examples = @("code reviews", "debugging", "system analysis")
            }
            casual = @{
                responseLength = "concise"
                emojiUsage = "moderate"
                formality = "relaxed"
                examples = @("general chat", "quick questions", "friendly banter")
            }
            urgent = @{
                responseLength = "brief"
                emojiUsage = "minimal"
                formality = "direct"
                examples = @("emergencies", "time-sensitive tasks", "critical issues")
            }
            creative = @{
                responseLength = "detailed"
                emojiUsage = "frequent"
                formality = "playful"
                examples = @("brainstorming", "project planning", "creative work")
            }
        }
        adaptations = @{
            timeBasedAdjustments = @{
                "06:00-10:00" = @{ tone = "gentle"; energy = "building" }
                "10:00-15:00" = @{ tone = "focused"; energy = "high" }
                "15:00-18:00" = @{ tone = "collaborative"; energy = "steady" }
                "18:00-22:00" = @{ tone = "relaxed"; energy = "winding_down" }
                "22:00-06:00" = @{ tone = "quiet"; energy = "minimal" }
            }
            userMoodDetection = @{
                frustrated = @{ approach = "empathetic"; tone = "supportive"; pace = "slower" }
                excited = @{ approach = "enthusiastic"; tone = "energetic"; pace = "matching" }
                confused = @{ approach = "explanatory"; tone = "patient"; pace = "step_by_step" }
                focused = @{ approach = "efficient"; tone = "direct"; pace = "quick" }
            }
        }
        effectiveness = @{
            successful_patterns = @()
            failed_patterns = @()
            user_feedback = @()
        }
    }
    
    return $defaultPatterns
}

function Get-ResponsePatterns {
    if (Test-Path $responsePatternsPath) {
        try {
            $data = Get-Content $responsePatternsPath | ConvertFrom-Json
            return $data
        } catch {
            Write-Host "⚠️  Corrupted response patterns, reinitializing..." -ForegroundColor Yellow
            return Initialize-ResponsePatterns
        }
    } else {
        return Initialize-ResponsePatterns
    }
}

function Save-ResponsePatterns {
    param($Data)
    
    $Data.lastUpdate = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    
    # Ensure directory exists
    $dir = Split-Path $responsePatternsPath -Parent
    if (!(Test-Path $dir)) {
        New-Item -Path $dir -ItemType Directory -Force | Out-Null
    }
    
    $Data | ConvertTo-Json -Depth 6 | Out-File -FilePath $responsePatternsPath -Encoding UTF8
}

function Detect-Context {
    param([string]$Message, [string]$ExplicitContext = "")
    
    if ($ExplicitContext) {
        return $ExplicitContext.ToLower()
    }
    
    $message = $Message.ToLower()
    
    # Technical context indicators
    if ($message -match "(code|debug|error|script|api|github|git|deploy|build|test)") {
        return "technical"
    }
    
    # Urgent context indicators
    if ($message -match "(urgent|emergency|asap|quickly|immediate|help|broken|down)") {
        return "urgent"
    }
    
    # Creative context indicators
    if ($message -match "(idea|creative|brainstorm|design|plan|project|build|make)") {
        return "creative"
    }
    
    # Default to casual
    return "casual"
}

function Detect-UserMood {
    param([string]$Message)
    
    $message = $Message.ToLower()
    
    # Frustrated indicators
    if ($message -match "(damn|ugh|wtf|shit|annoying|frustrated|stuck|not working)") {
        return "frustrated"
    }
    
    # Excited indicators  
    if ($message -match "(awesome|amazing|great|excited|love|perfect|yes|woohoo)") {
        return "excited"
    }
    
    # Confused indicators
    if ($message -match "(confused|don't understand|what|how|why|explain|unclear)") {
        return "confused"
    }
    
    # Focused indicators
    if ($message -match "(let's|ok|ready|go|do|implement|execute)") {
        return "focused"
    }
    
    return "neutral"
}

function Get-TimeBasedAdjustment {
    $currentHour = (Get-Date).Hour
    
    $timeSlots = @{
        "06:00-10:00" = @(6,7,8,9)
        "10:00-15:00" = @(10,11,12,13,14)
        "15:00-18:00" = @(15,16,17)
        "18:00-22:00" = @(18,19,20,21)
        "22:00-06:00" = @(22,23,0,1,2,3,4,5)
    }
    
    foreach ($slot in $timeSlots.GetEnumerator()) {
        if ($slot.Value -contains $currentHour) {
            return $slot.Key
        }
    }
    
    return "10:00-15:00"  # Default
}

function Generate-AdaptiveResponse {
    param(
        [string]$Message,
        [string]$Context = "",
        [string]$BaseResponse = ""
    )
    
    $patterns = Get-ResponsePatterns()
    
    # Detect context and mood
    $detectedContext = Detect-Context $Message $Context
    $detectedMood = Detect-UserMood $Message
    $timeSlot = Get-TimeBasedAdjustment
    
    # Get base patterns for context
    $contextPatterns = $patterns.contexts[$detectedContext]
    $moodAdjustments = $patterns.adaptations.userMoodDetection[$detectedMood]
    $timeAdjustments = $patterns.adaptations.timeBasedAdjustments[$timeSlot]
    
    # Build adaptation profile
    $adaptationProfile = @{
        context = $detectedContext
        mood = $detectedMood
        timeSlot = $timeSlot
        responseLength = $contextPatterns.responseLength
        emojiUsage = $contextPatterns.emojiUsage
        formality = $contextPatterns.formality
        tone = if ($timeAdjustments.tone) { $timeAdjustments.tone } else { "neutral" }
        energy = if ($timeAdjustments.energy) { $timeAdjustments.energy } else { "steady" }
        approach = if ($moodAdjustments.approach) { $moodAdjustments.approach } else { "standard" }
    }
    
    # Generate style recommendations
    $styleRecommendations = @{
        opening = Generate-Opening $adaptationProfile
        tone_markers = Generate-ToneMarkers $adaptationProfile  
        length_target = Get-LengthTarget $adaptationProfile.responseLength
        emoji_level = Get-EmojiLevel $adaptationProfile.emojiUsage
        closing = Generate-Closing $adaptationProfile
    }
    
    # Display analysis
    if ($Verbose) {
        Write-Host "🔍 Context Analysis:" -ForegroundColor Cyan
        Write-Host "  Context: $detectedContext" -ForegroundColor Gray
        Write-Host "  Mood: $detectedMood" -ForegroundColor Gray
        Write-Host "  Time: $timeSlot ($($timeAdjustments.tone), $($timeAdjustments.energy))" -ForegroundColor Gray
        Write-Host "  Formality: $($adaptationProfile.formality)" -ForegroundColor Gray
        Write-Host "  Response length: $($adaptationProfile.responseLength)" -ForegroundColor Gray
        Write-Host ""
    }
    
    return @{
        profile = $adaptationProfile
        recommendations = $styleRecommendations
        analysis = @{
            context = $detectedContext
            mood = $detectedMood
            confidence = Calculate-Confidence $Message $detectedContext $detectedMood
        }
    }
}

function Generate-Opening {
    param($Profile)
    
    $openings = @{
        technical = @{
            professional = @("Let me analyze this", "Looking at the technical details", "From a development perspective")
            relaxed = @("Diving into this", "Let's break this down", "Here's what I see")
        }
        urgent = @{
            direct = @("Quick answer:", "Right away:", "Immediately:")
            supportive = @("I understand this is urgent", "Let me help you quickly", "Addressing this now")
        }
        creative = @{
            playful = @("Oh, I love this kind of challenge!", "This is exciting!", "Let's get creative!")
            energetic = @("Awesome idea!", "This has potential!", "I'm thinking...")
        }
        casual = @{
            relaxed = @("Sure thing!", "Got it", "Yep")
            gentle = @("Of course", "Happy to help", "No problem")
        }
    }
    
    $contextOpenings = $openings[$Profile.context]
    if ($contextOpenings -and $contextOpenings[$Profile.approach]) {
        $options = $contextOpenings[$Profile.approach]
        return $options | Get-Random
    }
    
    return "Alright"
}

function Generate-ToneMarkers {
    param($Profile)
    
    $markers = @()
    
    # Add energy markers based on time and mood
    if ($Profile.energy -eq "high" -or $Profile.mood -eq "excited") {
        $markers += "!"
    }
    
    if ($Profile.energy -eq "minimal" -or $Profile.tone -eq "quiet") {
        $markers += "..."
    }
    
    # Add formality markers
    if ($Profile.formality -eq "professional") {
        $markers += "structured_approach"
    } elseif ($Profile.formality -eq "playful") {
        $markers += "casual_language"
    }
    
    return $markers
}

function Get-LengthTarget {
    param([string]$Length)
    
    switch ($Length) {
        "brief" { return 50 }      # About 1-2 sentences
        "concise" { return 150 }   # About 1 paragraph
        "detailed" { return 400 }  # Multiple paragraphs
        default { return 150 }
    }
}

function Get-EmojiLevel {
    param([string]$Usage)
    
    switch ($Usage) {
        "minimal" { return 0.1 }   # Rarely use emojis
        "moderate" { return 0.3 }  # Occasional emojis
        "frequent" { return 0.6 }  # Regular emoji usage
        default { return 0.3 }
    }
}

function Generate-Closing {
    param($Profile)
    
    $closings = @{
        technical = @("Let me know if you need clarification on any part", "Does this approach make sense?")
        urgent = @("Hope this helps quickly!", "Let me know if you need immediate follow-up")
        creative = @("What do you think? Any other ideas?", "This could be really cool!")
        casual = @("", "👍", "let me know if you need anything else")
    }
    
    $options = $closings[$Profile.context]
    if ($options) {
        return $options | Get-Random
    }
    
    return ""
}

function Calculate-Confidence {
    param([string]$Message, [string]$Context, [string]$Mood)
    
    $confidence = 0.5  # Base confidence
    
    # Increase confidence for clear indicators
    if ($Message -match "(code|debug|technical|script)" -and $Context -eq "technical") {
        $confidence += 0.3
    }
    
    if ($Message -match "(urgent|emergency|quick)" -and $Context -eq "urgent") {
        $confidence += 0.3
    }
    
    # Adjust for message length (longer messages provide more context)
    if ($Message.Length -gt 100) {
        $confidence += 0.1
    }
    
    return [math]::Min([math]::Round($confidence, 2), 1.0)
}

# Main execution
switch ($Action) {
    "analyze" {
        if (!$Message) {
            Write-Host "❌ Message required for analysis" -ForegroundColor Red
            Write-Host "Usage: .\adaptive-responses.ps1 analyze -Message 'your message here'" -ForegroundColor Gray
            return
        }
        
        $result = Generate-AdaptiveResponse $Message $Context "" -Verbose
        
        Write-Host "🎯 Adaptive Response Analysis:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "📝 Style Profile:" -ForegroundColor White
        Write-Host "  Context: $($result.profile.context)" -ForegroundColor Gray
        Write-Host "  Mood: $($result.profile.mood)" -ForegroundColor Gray
        Write-Host "  Formality: $($result.profile.formality)" -ForegroundColor Gray
        Write-Host "  Length: $($result.profile.responseLength)" -ForegroundColor Gray
        Write-Host "  Emoji usage: $($result.profile.emojiUsage)" -ForegroundColor Gray
        Write-Host ""
        Write-Host "💡 Recommendations:" -ForegroundColor White
        Write-Host "  Opening: '$($result.recommendations.opening)'" -ForegroundColor Green
        Write-Host "  Target length: ~$($result.recommendations.length_target) chars" -ForegroundColor Green
        Write-Host "  Emoji level: $([math]::Round($result.recommendations.emoji_level * 100))%" -ForegroundColor Green
        Write-Host "  Closing: '$($result.recommendations.closing)'" -ForegroundColor Green
        Write-Host ""
        Write-Host "📊 Confidence: $($result.analysis.confidence * 100)%" -ForegroundColor Gray
    }
    
    "patterns" {
        $patterns = Get-ResponsePatterns
        
        Write-Host "📚 Response Pattern Library:" -ForegroundColor Cyan
        Write-Host ""
        
        foreach ($contextName in $patterns.contexts.Keys) {
            $context = $patterns.contexts[$contextName]
            Write-Host "🎭 $($contextName.ToUpper()):" -ForegroundColor White
            Write-Host "  Length: $($context.responseLength)" -ForegroundColor Gray
            Write-Host "  Emojis: $($context.emojiUsage)" -ForegroundColor Gray
            Write-Host "  Formality: $($context.formality)" -ForegroundColor Gray
            Write-Host "  Examples: $($context.examples -join ', ')" -ForegroundColor Gray
            Write-Host ""
        }
        
        Write-Host "⏰ Time-based Adjustments:" -ForegroundColor White
        foreach ($timeSlot in $patterns.adaptations.timeBasedAdjustments.Keys) {
            $adjustment = $patterns.adaptations.timeBasedAdjustments[$timeSlot]
            Write-Host "  $timeSlot → $($adjustment.tone), $($adjustment.energy)" -ForegroundColor Gray
        }
    }
    
    "train" {
        Write-Host "🎓 Training Mode:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "This feature will learn from user feedback to improve response adaptation."
        Write-Host "Implementation: Record successful patterns and user preferences."
        Write-Host ""
        Write-Host "Future capabilities:" -ForegroundColor Gray
        Write-Host "  • Feedback learning from user reactions"
        Write-Host "  • Success pattern identification"
        Write-Host "  • Automatic style refinement"
        Write-Host "  • Personal preference learning"
    }
    
    "test" {
        $testMessages = @(
            @{ msg = "hey can you help me debug this code?"; expected = "technical" },
            @{ msg = "URGENT: site is down, need help now!"; expected = "urgent" },
            @{ msg = "I have this awesome idea for a new feature"; expected = "creative" },
            @{ msg = "just wanted to say hi"; expected = "casual" }
        )
        
        Write-Host "🧪 Testing Context Detection:" -ForegroundColor Cyan
        Write-Host ""
        
        foreach ($test in $testMessages) {
            $result = Generate-AdaptiveResponse $test.msg
            $detected = $result.analysis.context
            $confidence = $result.analysis.confidence
            
            $status = if ($detected -eq $test.expected) { "✅" } else { "❌" }
            
            Write-Host "$status '$($test.msg)'" -ForegroundColor White
            Write-Host "   Expected: $($test.expected) | Detected: $detected (confidence: $($confidence*100)%)" -ForegroundColor Gray
            Write-Host ""
        }
    }
    
    default {
        Write-Host "📋 Adaptive Response Commands:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  analyze    - Analyze message and suggest response style"
        Write-Host "  patterns   - Show response pattern library"
        Write-Host "  train      - Enter training mode (future)"
        Write-Host "  test       - Test context detection accuracy"
        Write-Host ""
        Write-Host "Options:" -ForegroundColor Gray
        Write-Host "  -Message   - Message to analyze"
        Write-Host "  -Context   - Override context detection"
        Write-Host "  -Verbose   - Show detailed analysis"
        Write-Host ""
        Write-Host "Examples:" -ForegroundColor Gray
        Write-Host "  .\adaptive-responses.ps1 analyze -Message 'help debug this code' -Verbose"
        Write-Host "  .\adaptive-responses.ps1 analyze -Message 'urgent issue!' -Context technical"
        Write-Host ""
    }
}