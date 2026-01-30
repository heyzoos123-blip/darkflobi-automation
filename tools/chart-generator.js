#!/usr/bin/env node
/**
 * DARKFLOBI CHART GENERATOR
 * Pure Node.js chart generation for visualizing progress metrics
 * Inspired by Cluka's chart generator skill on moltbook
 */

const fs = require('fs');

class DarkflobiChartGenerator {
    generateTokenomicsChart(data) {
        // Simple ASCII chart for terminal display
        const { prelaunch_holders, development_funding, community_governance } = data;
        
        const chart = `
📊 DARKFLOBI TOKENOMICS CHART
================================

Pre-launch Community:
${this.createBar(prelaunch_holders, 50)} ${prelaunch_holders}%

Development Funding:
${this.createBar(development_funding, 50)} ${development_funding}%

Community Governance:
${this.createBar(community_governance, 50)} ${community_governance}%

Legend: █ = 2%, ▓ = 1%, ░ = 0.5%
`;
        return chart;
    }

    generateProgressChart(data) {
        const { features_complete, integrations_ready, community_growth } = data;
        
        return `
🚀 DARKFLOBI PROGRESS METRICS
==============================

Features Complete:
${this.createBar(features_complete, 100)} ${features_complete}%

Integrations Ready:
${this.createBar(integrations_ready, 100)} ${integrations_ready}%

Community Growth:
${this.createBar(community_growth, 100)} ${community_growth}%

Updated: ${new Date().toISOString()}
`;
    }

    createBar(percentage, maxChars) {
        const filled = Math.floor((percentage / 100) * maxChars);
        const empty = maxChars - filled;
        
        return '█'.repeat(Math.floor(filled * 0.8)) + 
               '▓'.repeat(Math.floor(filled * 0.15)) + 
               '░'.repeat(Math.floor(filled * 0.05)) + 
               '·'.repeat(empty);
    }

    generateForTelegram(type, data) {
        let chart;
        switch(type) {
            case 'tokenomics':
                chart = this.generateTokenomicsChart(data);
                break;
            case 'progress':
                chart = this.generateProgressChart(data);
                break;
            default:
                chart = this.generateProgressChart(data);
        }
        
        return `\`\`\`\n${chart}\n\`\`\``;
    }
}

// CLI usage
if (require.main === module) {
    const generator = new DarkflobiChartGenerator();
    
    const sampleData = {
        features_complete: 75,
        integrations_ready: 85, 
        community_growth: 45,
        prelaunch_holders: 30,
        development_funding: 40,
        community_governance: 30
    };
    
    console.log(generator.generateProgressChart(sampleData));
}

module.exports = DarkflobiChartGenerator;