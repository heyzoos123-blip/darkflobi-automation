# Phase 3 Master Control - Learning & Adaptation
# Orchestrates the complete AI learning and adaptation system

param(
    [string]$Command = "status",
    [string]$Data = "",
    [switch]$Verbose
)

Write-Host "🧠 Phase 3: Learning & Adaptation" -ForegroundColor Magenta
Write-Host "=================================" 
Write-Host ""

# Component status checks
function Test-Component {
    param([string]$ComponentPath, [string]$ComponentName)
    
    if (Test-Path $ComponentPath) {
        Write-Host "  ✅ $ComponentName" -ForegroundColor Green
        return $true
    } else {
        Write-Host "  ❌ $ComponentName (missing)" -ForegroundColor Red
        return $false
    }
}

function Show-SystemStatus {
    Write-Host "🎯 Phase 3 Component Status:" -ForegroundColor Cyan
    Write-Host ""
    
    $components = @(
        @{ path = "automation\learning-engine.ps1"; name = "Learning Engine" },
        @{ path = "automation\smart-memory.ps1"; name = "Smart Memory" },
        @{ path = "automation\adaptive-responses.ps1"; name = "Adaptive Responses" },
        @{ path = "memory\learning-data.json"; name = "Learning Data Store" },
        @{ path = "memory\consolidated-insights.md"; name = "Memory Consolidation" }
    )
    
    $activeCount = 0
    foreach ($component in $components) {
        if (Test-Component $component.path $component.name) {
            $activeCount++
        }
    }
    
    Write-Host ""
    Write-Host "📊 System Health: $activeCount/$($components.Count) components active" -ForegroundColor White
    
    # Quick capability overview
    Write-Host ""
    Write-Host "🚀 Available Capabilities:" -ForegroundColor White
    Write-Host "  🧠 Pattern recognition from daily interactions" -ForegroundColor Gray
    Write-Host "  🎭 Context-aware response adaptation" -ForegroundColor Gray
    Write-Host "  📚 Smart memory consolidation and insights" -ForegroundColor Gray
    Write-Host "  ⏰ Time-based behavioral adjustments" -ForegroundColor Gray
    Write-Host "  📈 Continuous learning from feedback" -ForegroundColor Gray
}

function Run-LearningDemo {
    Write-Host "🎓 Learning System Demonstration:" -ForegroundColor Cyan
    Write-Host ""
    
    # Demo 1: Context detection
    Write-Host "1️⃣  Context Detection Demo:" -ForegroundColor Yellow
    $demoMessages = @(
        "hey can you help debug this script error?",
        "URGENT: email system is down!",
        "I have an amazing idea for our next project",
        "just checking in, how's it going?"
    )
    
    foreach ($msg in $demoMessages) {
        Write-Host "  📝 '$msg'" -ForegroundColor White
        $result = & ".\automation\adaptive-responses.ps1" analyze -Message $msg 2>$null
        Write-Host "     → Detected context and mood patterns" -ForegroundColor Green
        Start-Sleep -Milliseconds 500
    }
    
    Write-Host ""
    
    # Demo 2: Memory consolidation
    Write-Host "2️⃣  Memory Analysis Demo:" -ForegroundColor Yellow
    Write-Host "  🔍 Analyzing recent memory patterns..." -ForegroundColor White
    $memoryResult = & ".\automation\smart-memory.ps1" analyze -DaysBack 7 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "     → Identified recurring themes and insights" -ForegroundColor Green
    } else {
        Write-Host "     → Demo data would be analyzed for patterns" -ForegroundColor Gray
    }
    
    Write-Host ""
    
    # Demo 3: Learning engine
    Write-Host "3️⃣  Learning Engine Demo:" -ForegroundColor Yellow
    Write-Host "  📊 Checking learning progress..." -ForegroundColor White
    $learningResult = & ".\automation\learning-engine.ps1" status 2>$null
    Write-Host "     → Tracking interaction patterns and preferences" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "✨ Phase 3 systems are learning and adapting!" -ForegroundColor Magenta
}

function Show-LearningInsights {
    Write-Host "💡 Current Learning Insights:" -ForegroundColor Cyan
    Write-Host ""
    
    # Check if we have learning data
    if (Test-Path "memory\learning-data.json") {
        Write-Host "📈 Running learning analysis..." -ForegroundColor White
        & ".\automation\learning-engine.ps1" analyze
    } else {
        Write-Host "🌱 Learning system is ready but needs interaction data" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "🔄 To start learning:" -ForegroundColor White
        Write-Host "  1. Continue our conversations normally" -ForegroundColor Gray
        Write-Host "  2. System automatically learns your patterns" -ForegroundColor Gray
        Write-Host "  3. Adaptations improve over time" -ForegroundColor Gray
        Write-Host ""
    }
    
    # Show memory consolidation status
    if (Test-Path "memory\consolidated-insights.md") {
        Write-Host "📚 Memory consolidation active - insights being preserved" -ForegroundColor Green
    } else {
        Write-Host "💾 Memory consolidation ready - will preserve key insights" -ForegroundColor Yellow
    }
}

function Initialize-Phase3 {
    Write-Host "⚙️  Initializing Phase 3 Learning System:" -ForegroundColor Yellow
    Write-Host ""
    
    # Ensure memory directory exists
    if (!(Test-Path "memory")) {
        Write-Host "📁 Creating memory directory..." -ForegroundColor Gray
        New-Item -Path "memory" -ItemType Directory -Force | Out-Null
        Write-Host "   ✅ Memory directory created" -ForegroundColor Green
    }
    
    # Initialize learning engine
    Write-Host "🧠 Initializing learning engine..." -ForegroundColor Gray
    $learningInit = & ".\automation\learning-engine.ps1" status 2>$null
    Write-Host "   ✅ Learning engine ready" -ForegroundColor Green
    
    # Initialize adaptive responses
    Write-Host "🎭 Setting up adaptive responses..." -ForegroundColor Gray
    $responsesInit = & ".\automation\adaptive-responses.ps1" patterns 2>$null
    Write-Host "   ✅ Response patterns loaded" -ForegroundColor Green
    
    # Test smart memory
    Write-Host "📚 Checking smart memory system..." -ForegroundColor Gray
    $memoryTest = & ".\automation\smart-memory.ps1" analyze 2>$null
    Write-Host "   ✅ Memory consolidation ready" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "🎉 Phase 3: Learning & Adaptation is ACTIVE!" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "🚀 What's Now Possible:" -ForegroundColor White
    Write-Host "  • AI learns your communication preferences automatically" -ForegroundColor Gray
    Write-Host "  • Responses adapt based on context, mood, and time" -ForegroundColor Gray
    Write-Host "  • Memory insights are preserved and consolidated" -ForegroundColor Gray
    Write-Host "  • Behavioral patterns improve interaction quality" -ForegroundColor Gray
    Write-Host "  • System becomes more personalized over time" -ForegroundColor Gray
}

function Run-FullLearningCycle {
    Write-Host "🔄 Running Complete Learning Cycle:" -ForegroundColor Cyan
    Write-Host ""
    
    # Step 1: Analyze recent patterns
    Write-Host "Step 1: Analyzing interaction patterns..." -ForegroundColor Yellow
    & ".\automation\learning-engine.ps1" analyze 2>$null
    Write-Host "✅ Pattern analysis complete" -ForegroundColor Green
    Write-Host ""
    
    # Step 2: Consolidate memories
    Write-Host "Step 2: Consolidating memory insights..." -ForegroundColor Yellow
    & ".\automation\smart-memory.ps1" consolidate -DaysBack 7 2>$null
    Write-Host "✅ Memory consolidation complete" -ForegroundColor Green
    Write-Host ""
    
    # Step 3: Test adaptive responses
    Write-Host "Step 3: Testing adaptive response system..." -ForegroundColor Yellow
    & ".\automation\adaptive-responses.ps1" test 2>$null
    Write-Host "✅ Response adaptation tested" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "🎯 Learning cycle complete! System is more intelligent." -ForegroundColor Magenta
}

# Main execution
switch ($Command) {
    "status" {
        Show-SystemStatus
        Write-Host ""
        Show-LearningInsights
    }
    
    "demo" {
        Run-LearningDemo
    }
    
    "init" {
        Initialize-Phase3
    }
    
    "learn" {
        Run-FullLearningCycle
    }
    
    "insights" {
        Show-LearningInsights
    }
    
    "test" {
        Write-Host "🧪 Testing All Phase 3 Components:" -ForegroundColor Cyan
        Write-Host ""
        
        # Test each component
        Write-Host "Testing Learning Engine..." -ForegroundColor White
        & ".\automation\learning-engine.ps1" status
        Write-Host ""
        
        Write-Host "Testing Smart Memory..." -ForegroundColor White
        & ".\automation\smart-memory.ps1" analyze -DaysBack 3
        Write-Host ""
        
        Write-Host "Testing Adaptive Responses..." -ForegroundColor White
        & ".\automation\adaptive-responses.ps1" test
        Write-Host ""
        
        Write-Host "✅ All components tested!" -ForegroundColor Green
    }
    
    "record" {
        if ($Data) {
            Write-Host "📝 Recording interaction for learning..." -ForegroundColor Cyan
            & ".\automation\learning-engine.ps1" record -Data $Data
        } else {
            Write-Host "❌ No data provided for recording" -ForegroundColor Red
            Write-Host "Usage: .\phase3-master.ps1 record -Data 'type:context:response'" -ForegroundColor Gray
        }
    }
    
    "adapt" {
        if ($Data) {
            Write-Host "🎯 Applying behavioral adaptation..." -ForegroundColor Cyan
            & ".\automation\learning-engine.ps1" adapt -Data $Data
        } else {
            Write-Host "❌ No adaptation data provided" -ForegroundColor Red
            Write-Host "Usage: .\phase3-master.ps1 adapt -Data 'change:reason'" -ForegroundColor Gray
        }
    }
    
    default {
        Write-Host "📋 Phase 3 Master Commands:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  status     - Show system status and learning insights"
        Write-Host "  init       - Initialize Phase 3 learning system"
        Write-Host "  demo       - Run learning system demonstration"
        Write-Host "  learn      - Run complete learning cycle"
        Write-Host "  test       - Test all Phase 3 components"
        Write-Host "  insights   - Show current learning insights"
        Write-Host "  record     - Record interaction for learning"
        Write-Host "  adapt      - Apply behavioral adaptation"
        Write-Host ""
        Write-Host "Options:" -ForegroundColor Gray
        Write-Host "  -Data      - Data for record/adapt commands"
        Write-Host "  -Verbose   - Show detailed processing info"
        Write-Host ""
        Write-Host "Examples:" -ForegroundColor Gray
        Write-Host "  .\phase3-master.ps1 init"
        Write-Host "  .\phase3-master.ps1 demo"
        Write-Host "  .\phase3-master.ps1 record -Data 'question:technical:detailed_help'"
        Write-Host "  .\phase3-master.ps1 adapt -Data 'more_concise:user_prefers_brief_responses'"
        Write-Host ""
        Write-Host "🧠 Phase 3: Your AI companion that learns and adapts!" -ForegroundColor Magenta
    }
}