#!/usr/bin/env python3
"""
Prediction Markets Web Interface - SHIPPING NOW
Community-facing interface for darkflobi prediction markets
"""

from flask import Flask, jsonify, render_template_string, request
import json
from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the class directly
exec(open('/data/workspace/darkflobi-automation/prediction-markets-mvp.py').read())
from datetime import datetime

app = Flask(__name__)
pm = PredictionMarketsMVP()

# HTML Template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DarkFlobi Prediction Markets - LIVE</title>
    <style>
        body { 
            font-family: 'Courier New', monospace; 
            background: #1a1a1a; 
            color: #00ff41; 
            margin: 0; 
            padding: 20px; 
        }
        .gremlin-header {
            text-align: center;
            color: #ff4444;
            text-shadow: 0 0 10px #ff4444;
            margin-bottom: 30px;
        }
        .market-card {
            background: #2d2d2d;
            border: 2px solid #00ff41;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        }
        .status-active {
            border-color: #00ff41;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        }
        .status-resolved {
            border-color: #ffaa00;
            box-shadow: 0 0 20px rgba(255, 170, 0, 0.3);
        }
        .bet-button {
            background: #ff4444;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
            font-family: 'Courier New', monospace;
        }
        .bet-button:hover {
            background: #ff6666;
            box-shadow: 0 0 10px #ff4444;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-card {
            background: #333;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #555;
        }
        .chaos-meter {
            color: #ff4444;
            font-size: 1.2em;
            text-shadow: 0 0 5px #ff4444;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            color: #666;
            font-size: 0.9em;
        }
        input[type="number"] {
            background: #333;
            color: #00ff41;
            border: 1px solid #555;
            padding: 8px;
            border-radius: 4px;
            margin: 5px;
        }
    </style>
</head>
<body>
    <div class="gremlin-header">
        <h1>🤖 DarkFlobi Prediction Markets ⚡</h1>
        <p>First AI Agent with GitHub-Integrated Development Prediction Markets</p>
        <div class="chaos-meter">CHAOS LEVEL: MAXIMUM 🔥</div>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <h3>Active Markets</h3>
            <div id="active-count">{{ stats.active_markets }}</div>
        </div>
        <div class="stat-card">
            <h3>Resolved Markets</h3>
            <div id="resolved-count">{{ stats.resolved_markets }}</div>
        </div>
        <div class="stat-card">
            <h3>Total Volume</h3>
            <div id="total-volume">🚀 SHIPPING</div>
        </div>
        <div class="stat-card">
            <h3>GitHub Integration</h3>
            <div>✅ LIVE</div>
        </div>
    </div>

    <h2>📊 Active Markets</h2>
    {% for market_id, market in active_markets.items() %}
    <div class="market-card status-active">
        <h3>{{ market.feature_name }}</h3>
        <p><strong>Delivery Target:</strong> {{ market.delivery_date[:10] }}</p>
        <p><strong>GitHub Milestone:</strong> {{ market.github_milestone }}</p>
        <p><strong>Funding Pool:</strong> {{ market.funding_amount }} tokens</p>
        <p><strong>Total Bets:</strong> {{ market.bets|length }}</p>
        <p><strong>Resolution:</strong> Automatic via GitHub commits ⚡</p>
        
        <div style="margin: 15px 0;">
            <button class="bet-button" onclick="placeBet('{{ market_id }}', 'yes')">
                🎯 BET YES (Feature Ships)
            </button>
            <button class="bet-button" onclick="placeBet('{{ market_id }}', 'no')">
                ❌ BET NO (Feature Delayed)
            </button>
        </div>
        
        <p style="font-size: 0.9em; color: #888;">
            Market ID: {{ market_id[:8] }}... | Created: {{ market.created_at[:10] }}
        </p>
    </div>
    {% endfor %}

    <h2>🏆 Resolved Markets</h2>
    {% for market_id, market in resolved_markets.items() %}
    <div class="market-card status-resolved">
        <h3>{{ market.feature_name }} - {{ market.outcome.upper() }}</h3>
        <p><strong>Outcome:</strong> {{ market.outcome }}</p>
        <p><strong>Resolution:</strong> {{ market.resolved_at[:10] }}</p>
        {% if market.resolution_data.resolution_commit %}
        <p><strong>GitHub Commit:</strong> {{ market.resolution_data.resolution_commit }}</p>
        {% endif %}
        <p><strong>Winners:</strong> {{ market.payout_data.total_winners }} people</p>
        <p><strong>Total Payout:</strong> {{ market.payout_data.winning_amount + market.payout_data.losing_amount }} tokens</p>
    </div>
    {% endfor %}

    <div class="footer">
        <p>🦞 Built by darkflobi | GitHub-powered resolution | No human intervention needed</p>
        <p>Contract: 7GCxHtUttri1gNdt8Asa8DC72DQbiFNrN43ALjptpump</p>
        <p><a href="https://github.com/heyzoos123-blip/darkflobi-automation" style="color: #00ff41;">View Source Code</a></p>
    </div>

    <script>
        function placeBet(marketId, prediction) {
            const amount = prompt(`How many DARKFLOBI tokens do you want to bet on ${prediction.toUpperCase()}?`);
            if (amount && !isNaN(amount) && amount > 0) {
                const userId = prompt("Enter your wallet address or username:");
                if (userId) {
                    fetch('/api/bet', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            market_id: marketId,
                            user_id: userId,
                            amount: parseInt(amount),
                            prediction: prediction
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert(`Bet placed successfully! Bet ID: ${data.bet_id}`);
                            location.reload();
                        } else {
                            alert(`Error: ${data.error}`);
                        }
                    });
                }
            }
        }

        // Auto-refresh every 30 seconds
        setInterval(() => {
            location.reload();
        }, 30000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main prediction markets interface"""
    status = pm.get_market_status()
    return render_template_string(HTML_TEMPLATE, 
                                active_markets=status['markets']['active_markets'],
                                resolved_markets=status['markets']['resolved_markets'],
                                stats=status)

@app.route('/api/markets')
def api_markets():
    """API endpoint for market data"""
    return jsonify(pm.get_market_status())

@app.route('/api/bet', methods=['POST'])
def api_bet():
    """API endpoint for placing bets"""
    data = request.json
    result = pm.place_bet(
        data['market_id'],
        data['user_id'], 
        data['amount'],
        data['prediction']
    )
    return jsonify(result)

@app.route('/api/resolve/<market_id>')
def api_resolve(market_id):
    """API endpoint to check resolution"""
    result = pm.check_github_resolution(market_id)
    return jsonify(result)

@app.route('/api/create', methods=['POST'])
def api_create():
    """API endpoint to create new markets"""
    data = request.json
    result = pm.create_milestone_market(
        data['feature_name'],
        data['delivery_date'],
        data['github_milestone'],
        data.get('funding_amount', 0)
    )
    return jsonify(result)

if __name__ == '__main__':
    # Create the voice v2.0 market if it doesn't exist
    status = pm.get_market_status()
    if len(status['markets']['active_markets']) == 0:
        voice_market = pm.create_milestone_market(
            feature_name="Voice System v2.0",
            delivery_date="2026-02-15T00:00:00Z", 
            github_milestone="voice-v2-release",
            funding_amount=10000
        )
        print("🚀 SHIPPED: Voice v2.0 prediction market created!")
        print(f"Market ID: {voice_market['market_id']}")
    
    print("🎯 PREDICTION MARKETS WEB INTERFACE STARTING...")
    print("🔗 Access at: http://localhost:5000")
    print("⚡ GitHub integration: ACTIVE")
    print("🤖 Chaos level: MAXIMUM")
    
    app.run(debug=False, host='0.0.0.0', port=5000)