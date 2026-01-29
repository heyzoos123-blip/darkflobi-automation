# Composio Integration Skill

**Purpose:** 500+ app integrations via Composio - Gmail, Slack, GitHub, Twitter/X, Google Calendar, Notion, and more.

## 🚀 What This Gives Us

**Instant app access:** Gmail, Slack, GitHub, Twitter, Google Calendar, Google Drive, Notion, Trello, Salesforce, HubSpot, Discord, LinkedIn, and 490+ more apps.

**No more building integrations:** Instead of writing custom APIs for each service, we get them all through Composio's unified interface.

**Enterprise-grade:** Battle-tested by thousands of AI agents in production.

## 📋 Available Apps

### Communication
- **Gmail** - Email management, sending, searching
- **Slack** - Channel management, messaging, file sharing  
- **Discord** - Server management, messaging, moderation
- **Microsoft Teams** - Chat, meetings, file collaboration
- **WhatsApp Business** - Business messaging automation

### Development  
- **GitHub** - Repository management, issues, PRs, actions
- **GitLab** - Code management, CI/CD pipelines
- **Jira** - Issue tracking, project management
- **Linear** - Modern issue tracking and project planning

### Productivity
- **Google Calendar** - Event scheduling, meeting management
- **Google Drive** - File storage and sharing
- **Google Sheets** - Spreadsheet automation
- **Notion** - Wiki and database management
- **Trello** - Kanban board management
- **Asana** - Task and project management

### Social Media
- **Twitter/X** - Posting, engagement, monitoring
- **LinkedIn** - Professional networking, content sharing
- **Instagram** - Content posting and engagement
- **Facebook** - Page management and posting

### Sales & CRM
- **Salesforce** - Lead management, opportunity tracking
- **HubSpot** - Marketing automation, CRM
- **Pipedrive** - Sales pipeline management

### Finance & Analytics
- **Stripe** - Payment processing and analytics
- **Google Analytics** - Website traffic analysis
- **Shopify** - E-commerce management

## 🔧 Setup

### 1. Get Composio API Key

```bash
# Install Composio CLI
curl -fsSL https://composio.dev/install | bash

# Login (opens browser)
composio login

# Get your API key
composio whoami
```

### 2. Set Environment Variable

```bash
export COMPOSIO_API_KEY=your_api_key_here

# Make it permanent
echo 'export COMPOSIO_API_KEY=your_key_here' >> ~/.zshrc
source ~/.zshrc
```

### 3. Test Integration

```bash
cd /data/workspace/skills/composio-integration
python3 test.py
```

## 🎯 Usage Examples

### Gmail Integration
```bash
# Send email
python3 composio-tool.py gmail send_email \
  --to "someone@example.com" \
  --subject "Automated update from darkflobi" \
  --body "Hey! Just wanted to share some progress..."

# Search emails
python3 composio-tool.py gmail search \
  --query "from:github.com subject:pull request"

# Get unread count
python3 composio-tool.py gmail get_unread_count
```

### GitHub Integration
```bash
# Create issue
python3 composio-tool.py github create_issue \
  --repo "darkflobi/automation" \
  --title "Add Twitter sentiment analysis" \
  --body "We should track sentiment on our tweets..."

# List pull requests
python3 composio-tool.py github list_prs --repo "darkflobi/automation"

# Get repository stats
python3 composio-tool.py github get_repo_stats --repo "darkflobi/automation"
```

### Google Calendar Integration  
```bash
# Create event
python3 composio-tool.py google_calendar create_event \
  --title "Darkflobi development sync" \
  --start "2026-01-30T15:00:00" \
  --end "2026-01-30T16:00:00" \
  --description "Weekly progress review"

# List today's events
python3 composio-tool.py google_calendar list_events --date "today"
```

### Twitter/X Integration
```bash
# Post tweet
python3 composio-tool.py twitter post_tweet \
  --text "building the future of AI agents, one gremlin feature at a time 😁 #AI #automation"

# Get mentions
python3 composio-tool.py twitter get_mentions

# Search tweets
python3 composio-tool.py twitter search --query "#AI agents 2026"
```

### Slack Integration
```bash
# Send message
python3 composio-tool.py slack send_message \
  --channel "#general" \
  --text "Daily update: Twitter automation is live! 🚀"

# Upload file
python3 composio-tool.py slack upload_file \
  --channel "#development" \
  --file "/path/to/report.pdf" \
  --title "Integration Progress Report"
```

## 🤖 Clawdbot Integration

### Direct Usage
Ask Clawdbot to use any app:

```
"Send an email to the team about our Twitter automation launch"
"Create a GitHub issue for the WhatsApp integration"  
"Add a calendar event for tomorrow's sync meeting"
"Post a tweet about our latest features"
"Send a Slack message to the development channel"
```

### Automatic App Selection
Clawdbot automatically chooses the right app based on context:
- Email requests → Gmail
- Code requests → GitHub  
- Scheduling requests → Google Calendar
- Social posts → Twitter/LinkedIn/etc.
- Team communication → Slack/Discord

### Authentication Flow
1. First time using an app: Composio provides auth link
2. Click link, authorize access  
3. Future requests work automatically
4. Tokens stored securely by Composio

## 🔄 Heartbeat Integration

Add to `HEARTBEAT.md`:

```markdown
## 📧 Communication Check
- Check Gmail for urgent emails
- Review GitHub notifications and PRs
- Scan Slack for mentions or important messages
- Monitor Twitter mentions and engagement

## 📅 Calendar Awareness  
- Check today's meetings and events
- Remind about upcoming deadlines
- Suggest optimal times for posting content
```

## 🎭 Personality Integration

All Composio interactions maintain our gremlin personality:

**Email style:**
```
Subject: darkflobi update - chaos levels rising 📈

hey team! 

quick update from the gremlin labs: we just shipped twitter automation 
and it's working way better than expected. the AI is learning to be 
sarcastic, which feels like a natural evolution.

next up: taking over all social media platforms because apparently 
that's what we do now.

stay chaotic,
darkflobi 😁
```

**GitHub issues:**
```
Title: Add sentiment analysis to Twitter automation

## Context
our twitter bot is posting content but we're flying blind on engagement. 
need to add sentiment tracking so we know if people think we're 
hilarious or just annoying.

## Requirements  
- track sentiment on replies/mentions
- dashboard for engagement metrics
- alert if sentiment goes negative (aka people hate us)

## Acceptance Criteria
- [ ] sentiment analysis working
- [ ] metrics dashboard
- [ ] we still sound like gremlins, not corporate robots

priority: medium (unless sentiment is already negative, then high)
```

## 🔧 Advanced Features

### Workflow Automation
```python
# Complex multi-app workflows
def daily_standup_workflow():
    # 1. Get GitHub activity
    github_activity = composio.github.get_recent_activity()
    
    # 2. Check calendar for today
    calendar_events = composio.google_calendar.get_today_events()
    
    # 3. Generate update
    update = generate_standup_update(github_activity, calendar_events)
    
    # 4. Post to Slack
    composio.slack.send_message(channel="#daily-standup", text=update)
    
    # 5. Also tweet public progress
    public_update = make_public_friendly(update)
    composio.twitter.post_tweet(text=public_update)
```

### Batch Operations
```python
# Send same message to multiple platforms
def broadcast_announcement(message):
    composio.slack.send_message("#general", message)
    composio.discord.send_message("general", message)  
    composio.twitter.post_tweet(message[:280])
    composio.linkedin.create_post(message)
```

### Smart Notifications
```python
def check_priority_communications():
    # High-priority GitHub PRs
    prs = composio.github.list_prs(state="open", label="urgent")
    
    # Unread emails from important senders  
    emails = composio.gmail.search("is:unread from:(boss OR client OR investor)")
    
    # Slack DMs
    slack_dms = composio.slack.get_unread_dms()
    
    return generate_priority_summary(prs, emails, slack_dms)
```

## 📊 Success Metrics

Track integration success:
- **Apps connected:** Target 10+ within first week
- **Daily usage:** Aim for 50+ API calls across apps
- **Automation workflows:** 5+ complex multi-app workflows
- **Time saved:** Measure manual tasks eliminated
- **User engagement:** Track which integrations get most use

## 🚨 Troubleshooting

### Common Issues

**"Composio API key not found"**
```bash
export COMPOSIO_API_KEY=your_key_here
echo 'export COMPOSIO_API_KEY=your_key_here' >> ~/.zshrc
```

**"App authentication failed"**
- Check if you've authorized the app in Composio dashboard
- Try reauthorizing at https://app.composio.dev

**"Rate limit exceeded"**
- Apps have different rate limits
- Use pagination for large data requests
- Implement exponential backoff

**"Tool not found"**  
- Check available tools: `composio list tools`
- Verify app is supported: `composio list apps`

### Debug Mode
```bash
export COMPOSIO_DEBUG=1
python3 composio-tool.py gmail search --query "test"
```

## 🎯 Integration Priorities

**Week 1 (Essential):**
1. Gmail - Email management  
2. GitHub - Code collaboration
3. Google Calendar - Scheduling
4. Twitter - Social media automation
5. Slack - Team communication

**Week 2 (Enhancement):**
1. Notion - Documentation  
2. Google Drive - File management
3. Discord - Community management
4. LinkedIn - Professional networking
5. Trello - Project tracking

**Week 3 (Advanced):**
1. Salesforce/HubSpot - CRM if needed
2. Stripe - Payment processing  
3. Analytics tools - Data insights
4. Additional social platforms
5. Custom workflow automation

---

**The game-changer:** Instead of building 500 integrations over years, we get them all immediately. Now we can focus on what makes us unique: personality, community, and superior user experience. 🚀😁