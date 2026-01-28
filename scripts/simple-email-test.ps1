# Simple email connection test
param(
    [string]$Email,
    [string]$Password
)

Write-Host "📧 Testing Gmail IMAP connection..."
Write-Host "Email: $Email"

try {
    # Simple IMAP connection test
    $server = "imap.gmail.com"
    $port = 993
    
    # Use curl to test basic connection
    $result = & curl -s --connect-timeout 10 --url "imaps://$server:$port" --user "${Email}:${Password}" --request "CAPABILITY"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ IMAP connection successful!"
        Write-Host "Response: $result"
        
        # Now try to get inbox info
        $inbox = & curl -s --connect-timeout 10 --url "imaps://$server:$port/INBOX" --user "${Email}:${Password}" --request "SELECT INBOX"
        Write-Host "📬 Inbox info: $inbox"
        
    } else {
        Write-Host "❌ IMAP connection failed (exit code: $LASTEXITCODE)"
        Write-Host "Response: $result"
    }
    
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)"
}