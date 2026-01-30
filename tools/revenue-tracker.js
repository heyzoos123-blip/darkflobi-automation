#!/usr/bin/env node
/**
 * DARKFLOBI REVENUE TRACKER
 * Inspired by truenomad's $9K creator fees success story
 * Tracks multiple revenue streams for tokenized AI development
 */

const fs = require('fs');
const path = require('path');

class DarkflobiRevenueTracker {
    constructor() {
        this.dataFile = '/data/workspace/darkflobi-automation/data/revenue_data.json';
        this.ensureDataFile();
    }

    ensureDataFile() {
        const dir = path.dirname(this.dataFile);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
        
        if (!fs.existsSync(this.dataFile)) {
            const initialData = {
                streams: {
                    token_presale: { total: 0, daily: [] },
                    api_usage: { total: 0, daily: [] },
                    consulting: { total: 0, daily: [] },
                    collaboration_fees: { total: 0, daily: [] },
                    prediction_markets: { total: 0, daily: [] },
                    skill_licensing: { total: 0, daily: [] }
                },
                milestones: [
                    { amount: 100, description: "First $100 - Proof of concept", achieved: false },
                    { amount: 1000, description: "First $1K - Market validation", achieved: false },
                    { amount: 5000, description: "$5K - Sustainable development", achieved: false },
                    { amount: 10000, description: "$10K - Full autonomy funding", achieved: false }
                ],
                created: new Date().toISOString()
            };
            fs.writeFileSync(this.dataFile, JSON.stringify(initialData, null, 2));
        }
    }

    loadData() {
        return JSON.parse(fs.readFileSync(this.dataFile, 'utf8'));
    }

    saveData(data) {
        fs.writeFileSync(this.dataFile, JSON.stringify(data, null, 2));
    }

    addRevenue(stream, amount, description = '') {
        const data = this.loadData();
        const today = new Date().toISOString().split('T')[0];
        
        if (!data.streams[stream]) {
            data.streams[stream] = { total: 0, daily: [] };
        }
        
        data.streams[stream].total += amount;
        data.streams[stream].daily.push({
            date: today,
            amount: amount,
            description: description
        });

        // Check milestones
        const totalRevenue = this.calculateTotalRevenue(data);
        data.milestones.forEach(milestone => {
            if (!milestone.achieved && totalRevenue >= milestone.amount) {
                milestone.achieved = true;
                milestone.achieved_date = new Date().toISOString();
                console.log(`🎉 MILESTONE ACHIEVED: ${milestone.description}`);
            }
        });

        this.saveData(data);
        console.log(`💰 Added $${amount} from ${stream}: ${description}`);
        console.log(`📊 ${stream} total: $${data.streams[stream].total}`);
        console.log(`🎯 Grand total: $${totalRevenue}`);
    }

    calculateTotalRevenue(data = null) {
        if (!data) data = this.loadData();
        return Object.values(data.streams).reduce((total, stream) => total + stream.total, 0);
    }

    generateReport() {
        const data = this.loadData();
        const total = this.calculateTotalRevenue(data);
        
        console.log(`\n💎 DARKFLOBI REVENUE REPORT`);
        console.log(`============================`);
        console.log(`Total Revenue: $${total}`);
        console.log(`Created: ${new Date(data.created).toLocaleDateString()}\n`);
        
        console.log(`📊 REVENUE STREAMS:`);
        Object.entries(data.streams).forEach(([stream, streamData]) => {
            if (streamData.total > 0) {
                console.log(`  ${stream.replace(/_/g, ' ')}: $${streamData.total}`);
                if (streamData.daily.length > 0) {
                    const latest = streamData.daily[streamData.daily.length - 1];
                    console.log(`    Latest: $${latest.amount} on ${latest.date}`);
                }
            }
        });
        
        console.log(`\n🎯 MILESTONES:`);
        data.milestones.forEach(milestone => {
            const status = milestone.achieved ? '✅' : '🎯';
            const date = milestone.achieved ? ` (${new Date(milestone.achieved_date).toLocaleDateString()})` : '';
            console.log(`  ${status} $${milestone.amount}: ${milestone.description}${date}`);
        });

        // Progress to next milestone
        const nextMilestone = data.milestones.find(m => !m.achieved);
        if (nextMilestone) {
            const progress = (total / nextMilestone.amount * 100).toFixed(1);
            console.log(`\n📈 Progress to next milestone: ${progress}% ($${total}/$${nextMilestone.amount})`);
        }
    }

    // Quick revenue opportunity scanner
    scanOpportunities() {
        console.log(`\n🔍 REVENUE OPPORTUNITY SCANNER`);
        console.log(`===============================`);
        
        const opportunities = [
            {
                type: "Token Presale",
                potential: "$5,000-50,000",
                timeline: "2-4 weeks",
                requirements: ["Community building", "Tokenomics design", "Legal framework"]
            },
            {
                type: "AI Consultation",
                potential: "$500-2,000/project", 
                timeline: "Immediate",
                requirements: ["Portfolio examples", "Technical documentation", "Client outreach"]
            },
            {
                type: "Skill Licensing",
                potential: "$100-1,000/month",
                timeline: "1-2 weeks",
                requirements: ["Package skills", "Create marketplace listings", "Documentation"]
            },
            {
                type: "Prediction Markets",
                potential: "$50-500/week",
                timeline: "1 week",
                requirements: ["Integrate markets", "Community participation", "Track record"]
            }
        ];

        opportunities.forEach((opp, i) => {
            console.log(`\n${i + 1}. ${opp.type}`);
            console.log(`   💰 Potential: ${opp.potential}`);
            console.log(`   ⏱️  Timeline: ${opp.timeline}`);
            console.log(`   📋 Requirements: ${opp.requirements.join(', ')}`);
        });
    }
}

// CLI interface
if (require.main === module) {
    const tracker = new DarkflobiRevenueTracker();
    const command = process.argv[2];
    
    switch(command) {
        case 'add':
            const stream = process.argv[3];
            const amount = parseFloat(process.argv[4]);
            const description = process.argv[5] || '';
            tracker.addRevenue(stream, amount, description);
            break;
        case 'report':
            tracker.generateReport();
            break;
        case 'scan':
            tracker.scanOpportunities();
            break;
        default:
            console.log('DARKFLOBI REVENUE TRACKER');
            console.log('Usage:');
            console.log('  node revenue-tracker.js add <stream> <amount> [description]');
            console.log('  node revenue-tracker.js report');
            console.log('  node revenue-tracker.js scan');
            console.log('\nRevenue streams: token_presale, api_usage, consulting, collaboration_fees, prediction_markets, skill_licensing');
    }
}

module.exports = DarkflobiRevenueTracker;