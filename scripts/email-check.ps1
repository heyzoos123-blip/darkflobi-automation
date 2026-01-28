# Simple Gmail IMAP checker using curl
# Checks for unread emails and returns count + recent subjects

param(
    [string]$Email = "",
    [string]$Password = "",  # Use app password for Gmail
    [int]$MaxResults = 5
)

# Gmail IMAP settings
$ImapServer = "imaps://imap.gmail.com:993"
$InboxFolder = "INBOX"

if (-not $Email -or -not $Password) {
    Write-Host "❌ Email credentials required"
    Write-Host "📝 Usage: .\email-check.ps1 -Email 'user@gmail.com' -Password 'app_password'"
    Write-Host "🔐 Generate app password: https://myaccount.google.com/apppasswords"
    exit 1
}

try {
    Write-Host "📧 Checking Gmail IMAP for unread emails..."
    
    # Search for unread emails
    $searchQuery = "UNSEEN"
    $curlCommand = "curl -s --url ""$ImapServer/$InboxFolder"" --user ""$Email`:$Password"" -X ""SEARCH $searchQuery"""
    
    $unreadResults = Invoke-Expression $curlCommand 2>$null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ IMAP connection failed - check credentials/app password"
        exit 1
    }

    # Parse unread count
    if ($unreadResults -match "\* SEARCH (.*)") {
        $unreadIds = $matches[1].Trim().Split(' ') | Where-Object { $_ -ne "" }
        $unreadCount = $unreadIds.Count
        
        Write-Host "📬 Found $unreadCount unread emails"
        
        if ($unreadCount -gt 0) {
            # Get recent email subjects
            $recentIds = $unreadIds | Select-Object -Last $MaxResults
            
            foreach ($id in $recentIds) {
                if ($id -and $id.Trim() -ne "") {
                    $fetchCmd = "curl -s --url ""$ImapServer/$InboxFolder"" --user ""$Email`:$Password"" -X ""FETCH $id (ENVELOPE)"""
                    $envelope = Invoke-Expression $fetchCmd 2>$null
                    
                    # Extract subject from envelope (basic regex)
                    if ($envelope -match 'ENVELOPE.*?"([^"]*)".*?"([^"]*)"') {
                        $from = $matches[1]
                        $subject = $matches[2]
                        Write-Host "  📨 From: $from"
                        Write-Host "      Subject: $subject"
                        Write-Host ""
                    }
                }
            }
        }
        
        # Return JSON for automation
        $result = @{
            unreadCount = $unreadCount
            timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
            status = "success"
        }
        
        Write-Host "JSON:" (ConvertTo-Json $result -Compress)
        
    } else {
        Write-Host "📭 No unread emails found"
        $result = @{
            unreadCount = 0
            timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
            status = "success"
        }
        Write-Host "JSON:" (ConvertTo-Json $result -Compress)
    }
    
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)"
    $result = @{
        error = $_.Exception.Message
        timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        status = "failed"
    }
    Write-Host "JSON:" (ConvertTo-Json $result -Compress)
    exit 1
}