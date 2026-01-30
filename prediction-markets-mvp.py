#!/usr/bin/env python3
"""
Prediction Markets MVP for AI Development Milestones
First implementation of GitHub-integrated prediction markets
"""

import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import hashlib

class PredictionMarketsMVP:
    def __init__(self):
        self.github_webhook_url = "https://api.github.com/repos/heyzoos123-blip/darkflobi-automation"
        self.state_file = Path("/data/workspace/memory/prediction-markets-state.json")
        self.markets = self.load_markets()
    
    def load_markets(self):
        """Load existing prediction markets"""
        if self.state_file.exists():
            with open(self.state_file) as f:
                return json.load(f)
        return {
            "active_markets": {},
            "resolved_markets": {},
            "pending_verification": {}
        }
    
    def save_markets(self):
        """Save markets state"""
        self.state_file.parent.mkdir(exist_ok=True, parents=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.markets, f, indent=2, default=str)
    
    def create_milestone_market(self, 
                              feature_name: str, 
                              delivery_date: str, 
                              github_milestone: str,
                              funding_amount: int = 0):
        """Create a new prediction market for a development milestone"""
        
        market_id = hashlib.md5(f"{feature_name}_{delivery_date}".encode()).hexdigest()
        
        market = {
            "id": market_id,
            "feature_name": feature_name,
            "delivery_date": delivery_date,
            "github_milestone": github_milestone,
            "funding_amount": funding_amount,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "resolution_criteria": {
                "type": "github_commit",
                "repository": "heyzoos123-blip/darkflobi-automation",
                "milestone_marker": github_milestone,
                "verification_method": "commit_message_scan"
            },
            "bets": {},
            "total_volume": 0
        }
        
        self.markets["active_markets"][market_id] = market
        self.save_markets()
        
        return {
            "success": True,
            "market_id": market_id,
            "market": market,
            "message": f"Created prediction market: {feature_name} by {delivery_date}"
        }
    
    def place_bet(self, market_id: str, user_id: str, amount: int, prediction: str):
        """Place a bet on a prediction market"""
        
        if market_id not in self.markets["active_markets"]:
            return {"success": False, "error": "Market not found"}
        
        bet_id = hashlib.md5(f"{market_id}_{user_id}_{datetime.now()}".encode()).hexdigest()
        
        bet = {
            "id": bet_id,
            "user_id": user_id,
            "amount": amount,
            "prediction": prediction,  # "yes" or "no"
            "timestamp": datetime.now().isoformat()
        }
        
        market = self.markets["active_markets"][market_id]
        market["bets"][bet_id] = bet
        market["total_volume"] += amount
        
        self.save_markets()
        
        return {
            "success": True,
            "bet_id": bet_id,
            "market_id": market_id,
            "message": f"Bet placed: {amount} tokens on {prediction}"
        }
    
    def check_github_resolution(self, market_id: str):
        """Check if a market can be resolved based on GitHub commits"""
        
        if market_id not in self.markets["active_markets"]:
            return {"success": False, "error": "Market not found"}
        
        market = self.markets["active_markets"][market_id]
        milestone = market["resolution_criteria"]["milestone_marker"]
        
        try:
            # For MVP: Check recent git commits locally
            repo_path = Path("/data/workspace/darkflobi-automation")
            if repo_path.exists():
                result = subprocess.run(
                    ["git", "log", "--oneline", "-20"], 
                    cwd=repo_path, 
                    capture_output=True, 
                    text=True
                )
                
                if result.returncode == 0:
                    commits = result.stdout.strip().split('\n')
                    
                    for commit_line in commits:
                        if milestone.lower() in commit_line.lower():
                            # Milestone achieved!
                            commit_hash = commit_line.split()[0]
                            return self.resolve_market(market_id, "yes", {
                                "resolution_commit": commit_hash,
                                "commit_message": commit_line,
                                "commit_date": datetime.now().isoformat(),
                                "verification_method": "git_log_scan"
                            })
            
            # Check if deadline passed without resolution
            delivery_date = datetime.fromisoformat(market["delivery_date"].replace('Z', '+00:00'))
            if datetime.now() > delivery_date:
                return self.resolve_market(market_id, "no", {
                    "reason": "deadline_passed",
                    "deadline": market["delivery_date"],
                    "resolution_date": datetime.now().isoformat()
                })
            
            return {"success": True, "status": "pending", "message": "Market still active"}
            
        except Exception as e:
            return {"success": False, "error": f"GitHub check failed: {str(e)}"}
    
    def resolve_market(self, market_id: str, outcome: str, resolution_data: dict):
        """Resolve a prediction market"""
        
        if market_id not in self.markets["active_markets"]:
            return {"success": False, "error": "Market not found"}
        
        market = self.markets["active_markets"][market_id]
        market["status"] = "resolved"
        market["outcome"] = outcome
        market["resolution_data"] = resolution_data
        market["resolved_at"] = datetime.now().isoformat()
        
        # Calculate payouts
        winners = []
        losers = []
        total_winning_bets = 0
        total_losing_bets = 0
        
        for bet in market["bets"].values():
            if bet["prediction"] == outcome:
                winners.append(bet)
                total_winning_bets += bet["amount"]
            else:
                losers.append(bet)
                total_losing_bets += bet["amount"]
        
        # Calculate payout ratios
        payout_data = {
            "total_winners": len(winners),
            "total_losers": len(losers),
            "winning_amount": total_winning_bets,
            "losing_amount": total_losing_bets,
            "winner_payouts": {}
        }
        
        if total_winning_bets > 0:
            for winner in winners:
                payout_ratio = winner["amount"] / total_winning_bets
                payout = winner["amount"] + (total_losing_bets * payout_ratio)
                payout_data["winner_payouts"][winner["user_id"]] = {
                    "original_bet": winner["amount"],
                    "payout": payout,
                    "profit": payout - winner["amount"]
                }
        
        market["payout_data"] = payout_data
        
        # Move to resolved markets
        self.markets["resolved_markets"][market_id] = market
        del self.markets["active_markets"][market_id]
        
        self.save_markets()
        
        return {
            "success": True,
            "market_id": market_id,
            "outcome": outcome,
            "resolution_data": resolution_data,
            "payout_data": payout_data,
            "message": f"Market resolved: {outcome}"
        }
    
    def get_market_status(self, market_id: str = None):
        """Get status of markets"""
        
        if market_id:
            # Specific market
            for market_type in ["active_markets", "resolved_markets"]:
                if market_id in self.markets[market_type]:
                    return {
                        "success": True,
                        "market": self.markets[market_type][market_id],
                        "type": market_type
                    }
            return {"success": False, "error": "Market not found"}
        
        # All markets summary
        return {
            "success": True,
            "active_markets": len(self.markets["active_markets"]),
            "resolved_markets": len(self.markets["resolved_markets"]),
            "markets": self.markets
        }
    
    def run_resolution_check(self):
        """Check all active markets for resolution"""
        results = []
        
        for market_id in list(self.markets["active_markets"].keys()):
            result = self.check_github_resolution(market_id)
            results.append({
                "market_id": market_id,
                "result": result
            })
        
        return results

# Example usage and testing
if __name__ == "__main__":
    pm = PredictionMarketsMVP()
    
    # Create example market
    market = pm.create_milestone_market(
        feature_name="Voice System v2.0",
        delivery_date="2026-02-15T00:00:00Z",
        github_milestone="voice-v2-release",
        funding_amount=10000
    )
    
    print("Created market:", json.dumps(market, indent=2))
    
    # Check status
    status = pm.get_market_status()
    print("Market status:", json.dumps(status, indent=2, default=str))