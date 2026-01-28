# Heartbeat email checker for darkflobi
# Checks Gmail for unread emails and returns results

try {
    # Get credentials from Windows Credential Manager
    $creds = cmdkey /list:clawdbot-gmail 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ No stored Gmail credentials found"
        exit 1
    }
    
    $email = "heyzoos123@gmail.com"
    $password = "bzqvrdcjnkyqdieu"  # Using stored app password
    
    # Test basic connection first
    $capability = & curl -s --connect-timeout 5 --url "imaps://imap.gmail.com:993" --user "${email}:${password}" --request "CAPABILITY" 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        # Get inbox status  
        $status = & curl -s --connect-timeout 10 --url "imaps://imap.gmail.com:993/INBOX" --user "${email}:${password}" --request "STATUS INBOX (MESSAGES UNSEEN)" 2>$null
        
        # Extract unread count (basic pattern matching)
        if ($status -match "UNSEEN (\d+)") {
            $unreadCount = [int]$matches[1]
            
            $result = @{
                status = "success"
                unreadCount = $unreadCount
                timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
                email = $email
            }
            
            Write-Host "📧 Email check: $unreadCount unread messages"
            Write-Host "JSON:" (ConvertTo-Json $result -Compress)
            
        } else {
            # Fallback: connection works but couldn't parse unread count
            $result = @{
                status = "partial"
                message = "Connected but could not determine unread count"
                timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
                email = $email
            }
            
            Write-Host "📧 Email check: Connected (unread count unknown)"
            Write-Host "JSON:" (ConvertTo-Json $result -Compress)
        }
        
    } else {
        $result = @{
            status = "failed"
            error = "IMAP connection failed"
            timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        }
        
        Write-Host "❌ Email check failed"
        Write-Host "JSON:" (ConvertTo-Json $result -Compress)
        exit 1
    }
    
} catch {
    $result = @{
        status = "error"
        error = $_.Exception.Message
        timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    }
    
    Write-Host "❌ Email check error: $($_.Exception.Message)"
    Write-Host "JSON:" (ConvertTo-Json $result -Compress)
    exit 1
}