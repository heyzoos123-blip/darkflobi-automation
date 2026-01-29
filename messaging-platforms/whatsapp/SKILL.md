# WhatsApp Integration Skill

**Purpose:** Direct WhatsApp messaging integration for personal AI assistant capabilities.

## 🚀 What This Enables

**Personal AI assistant on WhatsApp:** Send messages directly to your AI and get responses with full tool access, just like Telegram but on WhatsApp.

**QR Code authentication:** Simple one-time setup, then permanent access.

**Group support:** Can join WhatsApp groups and respond when mentioned.

**Media handling:** Send and receive images, documents, voice messages.

## 📱 Features

### Core Messaging
- Send/receive text messages
- Image handling (send/receive)
- Voice message support
- Document sharing
- Group chat participation
- Contact management

### AI Integration
- Full Clawdbot tool access via WhatsApp
- Persistent memory across WhatsApp chats
- Cron/scheduling through WhatsApp commands
- Browser automation triggered via WhatsApp
- Composio app integrations via WhatsApp

### Smart Features
- Typing indicators
- Message read receipts
- Contact presence detection
- Group mention detection
- Multi-device sync
- Message encryption (WhatsApp E2E)

## 🔧 Setup

### 1. Install Dependencies

```bash
cd /data/workspace/skills/whatsapp-integration
npm install @whiskeysockets/baileys qrcode-terminal
```

### 2. Configuration

```bash
# Edit config in whatsapp-config.js
{
  enabled: true,
  allowedDMs: ['*'],        // Allow all DMs, or specific phone numbers
  allowedGroups: [],        // Group JIDs to allow 
  respondToMentionsOnly: true,  // In groups, only respond when @mentioned
  qrCodeTimeout: 60000,     // QR code timeout (60 seconds)
  sessionDir: './auth_whatsapp'  // Where to store session data
}
```

### 3. First Run

```bash
# Start WhatsApp integration
node whatsapp-gateway.js

# 1. QR code will appear in terminal
# 2. Open WhatsApp on phone
# 3. Go to Settings > Linked Devices > Link a Device  
# 4. Scan the QR code
# 5. Session saved - no need to scan again
```

## 💬 Usage

### Direct Messaging
Just send a message to the linked WhatsApp number:

```
"Hey, what's the weather like today?"
"Create a GitHub issue for the new feature request"
"Send an email to the team about the project update"
"Take a screenshot of github.com"
"Remind me in 30 minutes to check on the deployment"
```

### Group Chat Usage
Add the bot to a WhatsApp group, then:

```
"@YourBotName what's our GitHub activity today?"
"@YourBotName schedule a team meeting for tomorrow"
"@YourBotName post a tweet about our progress"
```

### Commands
All standard Clawdbot commands work:

```
"/help"           - Show available commands
"/status"         - Show session status  
"/memory"         - View memory summary
"/new"           - Start fresh conversation
"/queue"         - Show processing queue
```

### Media Support

**Send images:**
```
[Image] "Analyze this screenshot"
[Image] "What's in this photo?"
[Document] "Review this PDF"
```

**Receive images:**
The bot can send screenshots, charts, QR codes, etc.

## 🔗 Integration with Clawdbot

### Message Tool Enhancement
WhatsApp gets added as a channel option:

```bash
# Send via WhatsApp  
message action=send channel=whatsapp target="+1234567890" message="Update from darkflobi! 🚀"

# Send to group
message action=send channel=whatsapp target="group_jid" message="Team update ready"
```

### Cross-Platform Messaging
Route messages across platforms:

```bash
# From Telegram → Forward to WhatsApp
# From WhatsApp → Post to Twitter  
# From Email → Send WhatsApp notification
```

### Session Continuity  
WhatsApp chats maintain context across:
- Memory persistence
- Tool access continuity
- Scheduling/cron jobs
- Multi-turn conversations

## 🛠️ Technical Implementation

### Architecture
```
WhatsApp Web ←→ Baileys Library ←→ WhatsApp Adapter ←→ Clawdbot Gateway
```

### Session Management
- Persistent authentication via stored credentials
- Multi-device support (phone + computer + bot)
- Connection recovery on network issues
- QR code renewal when needed

### Message Processing
```javascript
// Incoming WhatsApp message
{
  chatId: "1234567890@s.whatsapp.net",
  text: "Hey bot, what's the weather?", 
  isGroup: false,
  sender: "1234567890@s.whatsapp.net",
  image: null, // or base64 image data
  mentions: [], // @mentions in groups
  timestamp: "2026-01-29T20:30:00Z"
}

// Processed by Clawdbot
// Response sent back via WhatsApp
```

### Media Handling
```javascript
// Image processing
if (message.image) {
  const imageData = {
    data: buffer.toString('base64'),
    mediaType: 'image/jpeg'
  }
  
  // Pass to vision model for analysis
  const analysis = await analyzeImage(imageData)
  await sendWhatsAppMessage(chatId, analysis)
}
```

## 🎭 Personality Integration

All WhatsApp responses maintain gremlin personality:

**Casual responses:**
```
"hey! checking the weather for you... ⚡"
"github shows 3 open PRs - want me to summarize them? 🤖"
"just sent that email. corporate speak translated to human 😁"
```

**Group interactions:**
```
"@flobi yep, that GitHub deploy looks solid 👍"
"meeting scheduled! calendar chaos managed ⚙️"
"screenshot incoming... *gremlin camera noises* 📸"
```

**Error handling:**
```
"oops, something went wrong. probably my fault 🤖"
"github's being moody today. trying again..."
"that didn't work. let me chaos-debug this ⚡"
```

## 🔐 Security & Privacy

### Authentication
- WhatsApp E2E encryption maintained
- Session tokens stored locally only
- No message content stored on external servers
- QR code expires after 60 seconds

### Access Control
```javascript
// Only respond to allowed contacts
allowedDMs: ['+1234567890', '+0987654321'], // or ['*'] for all

// Only join specific groups  
allowedGroups: ['group-jid-1@g.us', 'group-jid-2@g.us'],

// Group behavior
respondToMentionsOnly: true // Only respond when @mentioned in groups
```

### Message Filtering
```javascript
// Skip messages from unknown contacts
if (!isAllowedSender(message.sender)) {
  return // Ignore silently
}

// Skip spam patterns
if (containsSpam(message.text)) {
  return // Don't respond to spam
}
```

## 📊 Usage Analytics

Track WhatsApp bot usage:
- **Messages processed** per day
- **Response time** averages  
- **Tool usage** frequency
- **Group vs DM** distribution
- **Media messages** handling
- **Error rates** and types

## 🔄 Heartbeat Integration

Add to `HEARTBEAT.md`:

```markdown
## 📱 WhatsApp Check
- Monitor connection status
- Check for authentication expiry  
- Review group invitations
- Track message processing queue
- Alert on connection failures
```

## 🚨 Troubleshooting

### Common Issues

**QR Code not appearing:**
```bash
# Clear session and retry
rm -rf auth_whatsapp/
node whatsapp-gateway.js
```

**Connection lost:**
```bash
# Check WhatsApp Web on phone
# Unlink and relink if needed
# Restart the gateway
```

**Bot not responding in groups:**
```bash
# Make sure bot is mentioned: @BotName
# Check group is in allowedGroups list
# Verify respondToMentionsOnly setting
```

**Session expired:**
```bash
# Delete auth folder and re-authenticate  
# QR code will appear for new linking
```

**Message not sending:**
```bash
# Check recipient number format: +1234567890
# Verify contact exists in WhatsApp
# Check rate limits (WhatsApp has anti-spam)
```

### Debug Mode
```bash
export WHATSAPP_DEBUG=1
node whatsapp-gateway.js
```

## 🎯 Roadmap

### Phase 1 (Complete)
- [x] Basic text messaging
- [x] QR code authentication  
- [x] Group chat support
- [x] Clawdbot integration

### Phase 2 (Current)  
- [x] Image handling
- [x] Voice message support
- [x] Document sharing
- [x] Typing indicators

### Phase 3 (Planned)
- [ ] WhatsApp Business API integration
- [ ] Broadcast lists support
- [ ] Status/Story posting
- [ ] WhatsApp Pay integration (if relevant)
- [ ] Multi-account management

---

**The game-changer:** Now people can interact with darkflobi directly through WhatsApp - the world's most popular messaging app. Full AI capabilities in a familiar interface everyone already uses daily. 📱⚡