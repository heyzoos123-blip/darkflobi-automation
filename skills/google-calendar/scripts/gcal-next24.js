#!/usr/bin/env node
/**
 * Get events in next 24 hours
 * Returns JSON for easy parsing by Clawdbot
 */

const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');

// Configuration
const CREDENTIALS_PATH = path.join(process.env.HOME || process.env.USERPROFILE, '.config', 'gcal', 'service-account.json');
const SCOPES = ['https://www.googleapis.com/auth/calendar.readonly'];

async function getNext24Hours(outputFormat = 'text') {
  try {
    // Load credentials
    if (!fs.existsSync(CREDENTIALS_PATH)) {
      const error = { error: 'No credentials found', path: CREDENTIALS_PATH };
      if (outputFormat === 'json') {
        console.log(JSON.stringify(error));
      } else {
        console.error('❌ Credentials not found at:', CREDENTIALS_PATH);
      }
      return [];
    }

    const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
    
    // Create auth
    const auth = new google.auth.JWT(
      credentials.client_email,
      null,
      credentials.private_key,
      SCOPES
    );

    const calendar = google.calendar({ version: 'v3', auth });

    // Get events for next 24 hours
    const now = new Date();
    const tomorrow = new Date(now.getTime() + 24 * 60 * 60 * 1000);

    const events = await calendar.events.list({
      calendarId: 'primary',
      timeMin: now.toISOString(),
      timeMax: tomorrow.toISOString(),
      singleEvents: true,
      orderBy: 'startTime'
    });

    const eventList = events.data.items || [];
    
    // Format events
    const formattedEvents = eventList.map(event => {
      const start = event.start.dateTime || event.start.date;
      const end = event.end.dateTime || event.end.date;
      const startTime = new Date(start);
      const endTime = new Date(end);
      
      return {
        title: event.summary || '(No title)',
        start: startTime.toISOString(),
        startLocal: startTime.toLocaleString(),
        end: endTime.toISOString(),
        endLocal: endTime.toLocaleString(),
        duration: Math.round((endTime - startTime) / (1000 * 60)), // minutes
        location: event.location || null,
        description: event.description || null,
        status: event.status,
        isAllDay: !event.start.dateTime // all day if no specific time
      };
    });

    if (outputFormat === 'json') {
      console.log(JSON.stringify({ 
        events: formattedEvents, 
        count: formattedEvents.length,
        timeRange: { start: now.toISOString(), end: tomorrow.toISOString() }
      }, null, 2));
    } else {
      console.log(`📅 Next 24 hours (${formattedEvents.length} events):`);
      if (formattedEvents.length === 0) {
        console.log('   No events scheduled');
      } else {
        formattedEvents.forEach((event, i) => {
          const timeStr = event.isAllDay ? 'All day' : event.startLocal.split(',')[1]?.trim();
          console.log(`   ${i + 1}. ${event.title}`);
          console.log(`      ⏰ ${timeStr}${event.duration > 0 ? ` (${event.duration}min)` : ''}`);
          if (event.location) console.log(`      📍 ${event.location}`);
        });
      }
    }

    return formattedEvents;

  } catch (error) {
    const errorObj = { error: error.message, details: error.response?.data };
    if (outputFormat === 'json') {
      console.log(JSON.stringify(errorObj));
    } else {
      console.error('❌ Error:', error.message);
    }
    return [];
  }
}

// Command line usage
if (require.main === module) {
  const args = process.argv.slice(2);
  const format = args.includes('--json') ? 'json' : 'text';
  getNext24Hours(format);
}

module.exports = { getNext24Hours };