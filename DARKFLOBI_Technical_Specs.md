# DARKFLOBI Technical Specifications

## Token Parameters
```
Name: DARKFLOBI
Symbol: $DARKFLOBI
Decimals: 6
Total Supply: 1,000,000,000 tokens
Platform: pump.fun (Solana)
Standard: Token-2022 / SPL Token
Update Authority: Revoked (immutable)
```

## Wallet Configuration

### Primary Deployment Wallet
- **Purpose**: Token creation and initial management
- **Minimum SOL**: 40-60 SOL
- **Private Key**: SECURE - Store in hardware wallet
- **Access**: Lead developer only

### Bundle Wallets (16+ recommended)
- **Purpose**: Anti-sniper coordinated purchases
- **SOL per wallet**: 1-2 SOL each
- **Total SOL**: 16-32 SOL
- **Management**: Bundler bot automation
- **Distribution**: Spread across different IPs/devices

### Marketing Wallet
- **Purpose**: Promotional activities and trending
- **SOL Allocation**: 10-15 SOL
- **Access**: Marketing team
- **Usage**: Trending bots, promotional buys

## Image Specifications

### Required Format
```
Format: PNG (preferred) or JPG
Dimensions: 512x512 pixels minimum
Resolution: 300 DPI recommended
File Size: < 1MB
Color Profile: sRGB
Transparency: Supported (PNG)
```

### Design Guidelines
- **Style**: Professional, tech-focused
- **Colors**: Dark theme preferred (fits "DARK" branding)
- **Text**: Minimal, readable at small sizes
- **Logo Elements**: Memorable, scalable icon
- **Background**: Contrasting, not busy

## Metadata Schema
```json
{
  "name": "DARKFLOBI",
  "symbol": "DARKFLOBI",
  "description": "The dark horse of AI agents. Advanced cryptocurrency intelligence and market analysis. Competing in the next generation of AI trading assistants.",
  "image": "https://[ipfs-hash-or-cdn-url]",
  "external_url": "https://darkflobi.ai",
  "attributes": [
    {
      "trait_type": "Type",
      "value": "AI Agent Token"
    },
    {
      "trait_type": "Ecosystem",
      "value": "Solana"
    },
    {
      "trait_type": "Category",
      "value": "DeFi Intelligence"
    }
  ],
  "properties": {
    "category": "image",
    "files": [
      {
        "uri": "https://[image-url]",
        "type": "image/png"
      }
    ]
  }
}
```

## Bundler Bot Configuration

### Recommended Settings
```yaml
bundler_config:
  wallets: 16-20
  buy_amount_per_wallet: 0.5-1.5 SOL
  timing_offset: 100-500ms between buys
  anti_mev: true
  slippage: 10-15%
  priority_fee: 0.001-0.005 SOL
```

### Execution Parameters
- **Block Timing**: Same block as token creation
- **Purchase Distribution**: Randomized amounts
- **Wallet Rotation**: Different wallets per transaction
- **MEV Protection**: Priority fees and timing variance
- **Failure Handling**: Automatic retry with adjusted parameters

## Network Configuration

### Solana RPC Endpoints (Primary)
```
Mainnet: https://api.mainnet-beta.solana.com
Backup 1: https://solana-api.projectserum.com
Backup 2: https://rpc.ankr.com/solana
Private RPC: [Configure paid endpoint for faster execution]
```

### Connection Parameters
```
Commitment: confirmed
Timeout: 30 seconds
Max Retries: 3
Keepalive: true
```

## Smart Contract Interactions

### pump.fun Contract Address
```
Program ID: 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P
```

### Key Instructions
```
create: Creates new token with bonding curve
buy: Purchase tokens from bonding curve
sell: Sell tokens to bonding curve
withdraw: Withdraw SOL from completed bonding curve
```

### Transaction Structure
```javascript
// Example create transaction
{
  "instructions": [
    {
      "programId": "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P",
      "accounts": [...],
      "data": {
        "name": "DARKFLOBI",
        "symbol": "DARKFLOBI",
        "uri": "https://[metadata-uri]"
      }
    }
  ],
  "recentBlockhash": "[latest-blockhash]",
  "feePayer": "[deployer-wallet-address]"
}
```

## Monitoring Setup

### Key Metrics to Track
```
- Token Address
- Market Cap
- Holder Count
- Trading Volume (24h)
- Price (SOL/DARKFLOBI)
- Bonding Curve Progress
- Social Media Mentions
- Telegram/Discord Member Count
```

### API Endpoints
```
Pump.fun API: https://frontend-api.pump.fun/
Solana RPC: Standard blockchain queries
DexScreener: https://api.dexscreener.com/
Social APIs: Twitter/Telegram monitoring
```

### Alert Thresholds
```javascript
alerts: {
  price_drop: -20%, // 20% price decrease
  volume_spike: +500%, // 500% volume increase
  holder_milestone: [100, 250, 500, 1000], // Holder count milestones
  market_cap: [10000, 25000, 50000, 75000], // Market cap in USD
  bonding_curve: [25%, 50%, 75%, 90%], // Completion percentage
}
```

## Security Measures

### Wallet Security
- **Hardware Wallets**: Use for primary deployment wallet
- **Multi-sig**: Consider for treasury management
- **Key Management**: Secure backup and recovery
- **Access Control**: Limit access to essential personnel
- **Audit Trail**: Log all wallet interactions

### Operational Security
- **Code Review**: All scripts and bots audited
- **Test Environment**: Deploy on devnet first
- **Backup Plans**: Alternative deployment methods
- **Emergency Protocols**: Rapid response procedures
- **Communication Security**: Encrypted team channels

## Launch Sequence Technical Steps

### Pre-Launch (T-1 hour)
1. **Verify RPC connectivity**
2. **Check wallet balances**
3. **Test bundler bot connection**
4. **Upload metadata to IPFS**
5. **Prepare transaction parameters**

### Launch (T=0)
1. **Create token transaction**
2. **Verify deployment success**
3. **Trigger bundler bot**
4. **Monitor initial transactions**
5. **Record token address**

### Post-Launch (T+1 minute)
1. **Verify metadata display**
2. **Check pump.fun listing**
3. **Monitor bundler execution**
4. **Track price formation**
5. **Begin promotional activities**

## Troubleshooting Guide

### Common Issues
```
Issue: Transaction Failed
Solution: Check SOL balance, increase priority fee, retry

Issue: Metadata Not Displaying
Solution: Verify IPFS upload, check JSON format

Issue: Bundler Not Executing
Solution: Verify wallet connections, check RPC status

Issue: Low Liquidity
Solution: Deploy additional marketing SOL, engage community

Issue: Price Dump
Solution: Activate support levels, communicate with holders
```

### Emergency Contacts
```
Technical Lead: [Contact info]
RPC Provider: [Support contact]
IPFS Service: [Support contact]
Bundler Service: [Support contact]
Legal/Compliance: [Contact info]
```

## Post-Launch Optimization

### Performance Metrics
- **Transaction Success Rate**: >95%
- **Bundler Execution Time**: <5 seconds
- **Metadata Load Time**: <2 seconds
- **RPC Response Time**: <500ms
- **Community Response Time**: <5 minutes

### Scaling Considerations
- **Increased Volume**: Upgrade RPC plan
- **More Holders**: Enhanced monitoring
- **Higher Market Cap**: Professional management tools
- **Community Growth**: Automated moderation
- **Graduation**: Raydium listing preparation

---

**Version**: 1.0
**Last Updated**: Launch Day
**Classification**: CONFIDENTIAL
**Distribution**: Technical Team Only