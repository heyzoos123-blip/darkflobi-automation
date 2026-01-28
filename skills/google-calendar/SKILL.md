---
name: google-calendar
description: Google Calendar integration for checking events, scheduling, and calendar awareness.
metadata: {"clawdbot":{"emoji":"📅","requires":{"apis":["google-calendar"]}}}
---

# Google Calendar Integration

Access Google Calendar via API to check upcoming events, schedule meetings, and provide calendar-aware assistance.

## Setup

### 1. Google Cloud Project Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable Google Calendar API
4. Create credentials (OAuth2 or Service Account)

### 2. Authentication
For personal use (OAuth2):
```bash
# Store credentials in secure location
echo "client_id=your_client_id" > ~/.config/gcal/credentials
echo "client_secret=your_client_secret" >> ~/.config/gcal/credentials
```

For automation (Service Account):
```bash
# Download service account JSON key
# Store as ~/.config/gcal/service-account.json
```

### 3. Quick Test
```bash
# Test connection (will need token exchange first time)
node scripts/gcal-test.js
```

## Usage

### List Today's Events
```bash
node scripts/gcal-today.js
```

### List Next 24 Hours
```bash
node scripts/gcal-next24.js
```

### Schedule Event
```bash
node scripts/gcal-create.js --title "Meeting" --start "2026-01-28T14:00:00" --duration 60
```

## API Integration

The skill provides these functions for Clawdbot:
- `getUpcomingEvents(hours=24)` - Get events in next N hours
- `getTodaysEvents()` - Get today's schedule
- `createEvent(title, start, end, description)` - Schedule new event
- `searchEvents(query, days=7)` - Search recent/upcoming events

## Scripts

- `scripts/gcal-auth.js` - Handle OAuth flow
- `scripts/gcal-today.js` - Today's agenda
- `scripts/gcal-next24.js` - Next 24 hours
- `scripts/gcal-create.js` - Create new events
- `scripts/gcal-test.js` - Connection test

## Security Notes

- Store credentials securely (not in repo)
- Use service account for automation
- Limit API scope to calendar.readonly for read-only access
- Consider using application-specific passwords