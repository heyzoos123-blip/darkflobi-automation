# Email monitoring setup script
# Securely stores Gmail credentials for automated checking

Write-Host "📧 Gmail Email Monitoring Setup"
Write-Host "================================"
Write-Host ""

# Get email address
$email = Read-Host "Gmail address"

# Get app password (masked input)
Write-Host "🔐 Gmail App Password (not your regular password):"
Write-Host "   1. Go to: https://myaccount.google.com/apppasswords"
Write-Host "   2. Generate app password for 'Mail'"
Write-Host "   3. Enter the 16-character password below"
Write-Host ""

$securePassword = Read-Host "App Password" -AsSecureString
$password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword))

# Test connection
Write-Host ""
Write-Host "🧪 Testing connection..."

$testResult = & "$PSScriptRoot\email-check.ps1" -Email $email -Password $password

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Email connection successful!"
    
    # Store credentials securely (Windows Credential Manager)
    Write-Host "💾 Storing credentials in Windows Credential Manager..."
    
    cmdkey /generic:"clawdbot-gmail" /user:$email /pass:$password | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Credentials stored securely"
        Write-Host ""
        Write-Host "🚀 Email monitoring is ready!"
        Write-Host "   - Credentials stored in Windows Credential Manager"
        Write-Host "   - Accessible via: cmdkey /list:clawdbot-gmail"
        Write-Host "   - Test anytime: .\email-check.ps1 -Email '$email' -Password '[from_credmgr]'"
    } else {
        Write-Host "⚠️  Could not store in Credential Manager, but connection works"
        Write-Host "📝 You'll need to provide credentials manually for now"
    }
    
} else {
    Write-Host "❌ Email connection failed"
    Write-Host "📝 Common issues:"
    Write-Host "   - Wrong app password (need 16-char app password, not regular password)"
    Write-Host "   - 2FA not enabled on Google account"
    Write-Host "   - IMAP not enabled in Gmail settings"
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')