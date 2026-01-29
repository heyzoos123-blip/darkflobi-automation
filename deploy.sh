#!/bin/bash
# 🚀 Darkflobi Automation - One-Click Deployment
# Deploy the full gremlin automation system

set -e

echo "🤖 Darkflobi Automation Deployment"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%H:%M:%S')] ERROR: $1${NC}"
}

info() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')] INFO: $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "twitter-automation" ]; then
    error "Run this script from the darkflobi-automation repository root"
    exit 1
fi

log "Starting deployment..."

# Check API keys
check_api_keys() {
    log "Checking API keys..."
    
    if [ -z "$COMPOSIO_API_KEY" ]; then
        error "COMPOSIO_API_KEY not set"
        info "Get your key with:"
        info "  curl -fsSL https://composio.dev/install | bash"
        info "  composio login"
        info "  composio whoami"
        info "  export COMPOSIO_API_KEY=your_key_here"
        return 1
    else
        log "✅ COMPOSIO_API_KEY found"
    fi
    
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        warn "ANTHROPIC_API_KEY not set (optional for some features)"
        info "Get your key from: https://console.anthropic.com/"
        info "  export ANTHROPIC_API_KEY=sk-ant-your-key"
    else
        log "✅ ANTHROPIC_API_KEY found"
    fi
    
    return 0
}

# Install Python dependencies
install_python_deps() {
    log "Installing Python dependencies..."
    
    if command -v python3 &> /dev/null; then
        log "✅ Python 3 found"
    else
        error "Python 3 not found"
        return 1
    fi
    
    # Create requirements.txt if it doesn't exist
    if [ ! -f "requirements.txt" ]; then
        log "Creating requirements.txt..."
        cat > requirements.txt << 'EOF'
# Core dependencies
requests>=2.31.0
anthropic>=0.8.0

# Optional dependencies (install if possible)
# @composio/core  # Installed via npm
# tweepy>=4.14.0  # Twitter API
# python-dotenv>=1.0.0  # Environment variables
# pillow>=10.0.0  # Image processing
EOF
    fi
    
    # Try to install dependencies (may fail in constrained environments)
    if python3 -m pip install requests --quiet 2>/dev/null; then
        log "✅ Basic Python dependencies installed"
    else
        warn "Could not install Python dependencies (externally managed environment)"
        info "Core functionality will work with standard library only"
    fi
}

# Install Node.js dependencies
install_node_deps() {
    log "Installing Node.js dependencies..."
    
    if command -v node &> /dev/null; then
        log "✅ Node.js found: $(node --version)"
        
        # Install Composio core if not already installed
        if [ ! -d "node_modules" ]; then
            log "Installing @composio/core..."
            npm init -y > /dev/null 2>&1 || true
            npm install @composio/core --silent 2>/dev/null || warn "Failed to install @composio/core"
        fi
        
        # Install WhatsApp dependencies if WhatsApp is enabled
        if [ -d "messaging-platforms/whatsapp" ]; then
            log "Installing WhatsApp dependencies..."
            cd messaging-platforms/whatsapp
            npm install @whiskeysockets/baileys qrcode-terminal --silent 2>/dev/null || warn "Failed to install WhatsApp dependencies"
            cd ../..
        fi
        
    else
        warn "Node.js not found - some features will be limited"
        info "Install Node.js from: https://nodejs.org/"
    fi
}

# Set up configuration files
setup_config() {
    log "Setting up configuration..."
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        log "Creating .env file..."
        cat > .env << EOF
# Darkflobi Automation Configuration

# Composio API (required for 500+ app integrations)
COMPOSIO_API_KEY=${COMPOSIO_API_KEY:-your_composio_key_here}

# Anthropic API (optional, for enhanced AI features)
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-your_anthropic_key_here}

# Twitter API Provider (composio, late, twitterapi, or official)
TWITTER_API_PROVIDER=composio

# Twitter API Keys (optional - leave empty to use Composio)
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
TWITTER_BEARER_TOKEN=

# Late.dev API (alternative Twitter provider)
LATE_API_KEY=

# TwitterAPI.io (alternative Twitter provider)  
TWITTERAPI_IO_KEY=

# Debug mode
TWITTER_DEBUG=0
COMPOSIO_DEBUG=0
EOF
        log "✅ Created .env file"
    else
        log "✅ .env file already exists"
    fi
    
    # Make scripts executable
    chmod +x twitter-automation/*.py 2>/dev/null || true
    chmod +x composio-integration/*.py 2>/dev/null || true
    chmod +x deployment/*.sh 2>/dev/null || true
}

# Test core functionality
test_deployment() {
    log "Testing deployment..."
    
    # Test Composio integration
    if [ -f "composio-integration/test.py" ]; then
        log "Testing Composio integration..."
        cd composio-integration
        if python3 test.py > test_results.log 2>&1; then
            log "✅ Composio integration test passed"
        else
            warn "Composio integration test had issues (check test_results.log)"
        fi
        cd ..
    fi
    
    # Test Twitter content generation
    if [ -f "twitter-automation/enhanced-twitter.py" ]; then
        log "Testing Twitter content generation..."
        if python3 twitter-automation/enhanced-twitter.py --generate --dry-run > /dev/null 2>&1; then
            log "✅ Twitter content generation working"
        else
            warn "Twitter content generation test failed"
        fi
    fi
    
    # Test simple tweet generation  
    if [ -f "twitter-automation/simple-tweet.py" ]; then
        log "Testing simple tweet generation..."
        if python3 twitter-automation/simple-tweet.py --template daily_motivation > /dev/null 2>&1; then
            log "✅ Simple tweet generation working"
        else
            warn "Simple tweet generation failed"
        fi
    fi
}

# Create deployment status
create_status() {
    log "Creating deployment status..."
    
    cat > deployment_status.json << EOF
{
    "deployment_time": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "version": "1.0.0",
    "components": {
        "twitter_automation": true,
        "composio_integration": $([ -n "$COMPOSIO_API_KEY" ] && [ "$COMPOSIO_API_KEY" != "your_composio_key_here" ] && echo "true" || echo "false"),
        "whatsapp_messaging": $([ -d "messaging-platforms/whatsapp" ] && echo "true" || echo "false"),
        "browser_automation": $([ -d "browser-automation" ] && echo "true" || echo "false"),
        "memory_system": $([ -d "memory-system" ] && echo "true" || echo "false")
    },
    "api_keys_configured": {
        "composio": $([ -n "$COMPOSIO_API_KEY" ] && [ "$COMPOSIO_API_KEY" != "your_composio_key_here" ] && echo "true" || echo "false"),
        "anthropic": $([ -n "$ANTHROPIC_API_KEY" ] && [ "$ANTHROPIC_API_KEY" != "your_anthropic_key_here" ] && echo "true" || echo "false")
    },
    "next_steps": [
        "Set up Composio API key if not configured",
        "Test Twitter posting with: python3 twitter-automation/enhanced-twitter.py --generate --dry-run",
        "Configure additional API keys as needed",
        "Set up automated posting schedules"
    ]
}
EOF

    log "✅ Deployment status created"
}

# Show usage examples
show_usage() {
    log "Deployment complete! 🎉"
    echo ""
    info "Quick usage examples:"
    echo ""
    echo "# Generate and test Twitter content:"
    echo "python3 twitter-automation/enhanced-twitter.py --generate --topic 'AI development' --dry-run"
    echo ""
    echo "# Post a tweet (requires API setup):"
    echo "python3 twitter-automation/enhanced-twitter.py --post 'just deployed darkflobi automation! chaos levels: maximum ⚡'"
    echo ""
    echo "# Create a project update thread:"
    echo "python3 twitter-automation/enhanced-twitter.py --thread --template project_update --dry-run"
    echo ""
    echo "# Test Composio integrations:"
    echo "python3 composio-integration/test.py"
    echo ""
    echo "# Use Composio apps (after API setup):"
    echo "python3 composio-integration/composio-tool.py gmail send_email --to test@example.com --subject 'Test' --body 'Hello!' --personality"
    echo ""
    info "Configuration files:"
    echo "  .env - API keys and settings"
    echo "  deployment_status.json - Deployment status"
    echo ""
    info "Next steps:"
    echo "  1. Configure API keys in .env file"
    echo "  2. Test with --dry-run flags first"  
    echo "  3. Set up automated posting schedules"
    echo "  4. Explore 500+ Composio app integrations"
    echo ""
    log "Ready to dominate social media with gremlin energy! 😁"
}

# Main deployment flow
main() {
    log "Darkflobi Automation deployment starting..."
    
    if ! check_api_keys; then
        warn "API keys not configured - continuing with limited functionality"
    fi
    
    install_python_deps
    install_node_deps
    setup_config
    test_deployment
    create_status
    show_usage
    
    log "Deployment completed successfully! 🚀"
}

# Run deployment
main "$@"