#!/usr/bin/env node
/**
 * Google Calendar API Test Script
 * Tests connection and lists next few events
 */

const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');

// Configuration
const CREDENTIALS_PATH = path.join(process.env.HOME || process.env.USERPROFILE, '.config', 'gcal', 'service-account.json');
const SCOPES = ['https://www.googleapis.com/auth/calendar.readonly'];

async function testCalendarConnection() {
  try {
    console.log('🔌 Testing Google Calendar connection...');
    
    // Check if credentials exist
    if (!fs.existsSync(CREDENTIALS_PATH)) {
      console.error('❌ Credentials not found at:', CREDENTIALS_PATH);
      console.log('📝 Setup required:');
      console.log('1. Create Google Cloud project');
      console.log('2. Enable Calendar API');
      console.log('3. Create service account');
      console.log('4. Download JSON key to:', CREDENTIALS_PATH);
      process.exit(1);
    }

    // Load credentials
    const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
    
    // Create JWT auth
    const auth = new google.auth.JWT(
      credentials.client_email,
      null,
      credentials.private_key,
      SCOPES
    );

    // Initialize Calendar API
    const calendar = google.calendar({ version: 'v3', auth });

    // Test with a simple query - get calendar list
    console.log('📅 Fetching calendar list...');
    const calendarList = await calendar.calendarList.list();
    
    if (calendarList.data.items && calendarList.data.items.length > 0) {
      console.log('✅ Connection successful!');
      console.log(`📋 Found ${calendarList.data.items.length} calendars:`);
      
      calendarList.data.items.forEach((cal, i) => {
        console.log(`  ${i + 1}. ${cal.summary} (${cal.id})`);
      });

      // Test getting events from primary calendar
      console.log('\n📅 Getting next 5 events from primary calendar...');
      const events = await calendar.events.list({
        calendarId: 'primary',
        timeMin: new Date().toISOString(),
        maxResults: 5,
        singleEvents: true,
        orderBy: 'startTime'
      });

      const eventList = events.data.items;
      if (eventList && eventList.length > 0) {
        console.log(`📋 Next ${eventList.length} events:`);
        eventList.forEach((event, i) => {
          const start = event.start.dateTime || event.start.date;
          console.log(`  ${i + 1}. ${event.summary} - ${new Date(start).toLocaleString()}`);
        });
      } else {
        console.log('📋 No upcoming events found');
      }

    } else {
      console.log('⚠️  No calendars found - check permissions');
    }

  } catch (error) {
    console.error('❌ Connection failed:', error.message);
    if (error.response && error.response.data) {
      console.error('   Details:', JSON.stringify(error.response.data, null, 2));
    }
    process.exit(1);
  }
}

if (require.main === module) {
  testCalendarConnection();
}

module.exports = { testCalendarConnection };