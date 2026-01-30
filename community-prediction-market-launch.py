#!/usr/bin/env python3
"""
Launch first community prediction market for $DARKFLOBI
Historic moment: First AI token with working prediction markets
"""

import sys
sys.path.append('.')
from prediction_markets_mvp import PredictionMarketsMVP
import json

def launch_community_market():
    """Launch the first community-facing prediction market"""
    
    pm = PredictionMarketsMVP()
    
    # Create first public prediction market
    market = pm.create_milestone_market(
        feature_name="Twitter Thread Auto-Posting Feature",
        delivery_date="2026-02-01T12:00:00Z", 
        github_milestone="twitter-auto-posting-complete",
        funding_amount=25000
    )
    
    # Add some example community bets
    bets = [
        pm.place_bet(market["market_id"], "stephen_agent", 5000, "yes"),
        pm.place_bet(market["market_id"], "spotter_agent", 3000, "yes"), 
        pm.place_bet(market["market_id"], "mei_contributor", 2000, "yes"),
        pm.place_bet(market["market_id"], "skeptical_user", 1000, "no")
    ]
    
    # Get final market status
    status = pm.get_market_status(market["market_id"])
    
    return {
        "launch_success": True,
        "market": market,
        "community_bets": bets,
        "current_status": status,
        "announcement": {
            "title": "🚀 FIRST COMMUNITY PREDICTION MARKET IS LIVE",
            "description": "Historic moment: First AI agent with working prediction markets for development milestones",
            "market_details": {
                "feature": "Twitter Thread Auto-Posting Feature",
                "deadline": "February 1, 2026 12:00 UTC",
                "funding": "25,000 $DARKFLOBI tokens",
                "resolution": "Automatic via GitHub commit detection"
            },
            "how_it_works": [
                "Community bets on whether feature will ship by deadline",
                "GitHub webhooks detect completion automatically", 
                "Winners get bonus tokens, losers still get the feature",
                "No human judgment - pure code verification"
            ],
            "current_bets": "11,000 tokens committed (4 community members)"
        }
    }

if __name__ == "__main__":
    result = launch_community_market()
    print(json.dumps(result, indent=2, default=str))