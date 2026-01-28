# Revenue Analytics Dashboard Specifications

## EXECUTIVE DASHBOARD (CEO View)

### Key Metrics Display (Top Row)
```
🎯 Current MRR: $2,847 / $4,900 target (58%)
📈 MoM Growth: +23.4% 
💰 ARPU: $47 (target: $50-80)
⭐ NPS Score: 72 (target: >70)
```

### Revenue Trend Chart (Main Visual)
- **Time Period:** Last 12 months + 6 month projection
- **Metrics Shown:**
  - Total MRR (primary line)
  - New MRR (green area)
  - Expansion MRR (blue area) 
  - Churn MRR (red area)
- **Annotations:** Major feature launches, marketing campaigns

### Customer Cohort Analysis
- **Retention Curves:** Monthly cohorts over 12 months
- **Revenue Cohorts:** How much each cohort generates over time
- **Churn Prediction:** ML model scoring at-risk customers

---

## OPERATIONAL DASHBOARD (Revenue Analytics Team)

### Real-Time Metrics Panel
```typescript
interface DashboardMetrics {
  realTime: {
    activeTrials: number;
    todaySignups: number;
    todayChurn: number;
    currentMRR: number;
    todayRevenue: number;
  };
  
  trends: {
    mrrGrowthRate: number; // 30-day
    churnRate: number; // monthly
    conversionRate: number; // trial to paid
    avgDaysToConvert: number;
  };
  
  targets: {
    monthlyMRRTarget: number;
    daysToTarget: number;
    requiredDailyGrowth: number;
  };
}
```

### Customer Segmentation Grid
| Segment | Count | ARPU | LTV | Churn Risk | Actions |
|---------|-------|------|-----|------------|---------|
| High-Value Power Users | 12 | $98 | $450 | Low | Upsell to Enterprise |
| Growing Teams | 34 | $65 | $320 | Medium | Add team features |
| Price-Sensitive | 67 | $22 | $180 | High | Retention campaign |
| Trial Users | 89 | $0 | - | - | Conversion campaign |

### Usage Analytics
```sql
-- Daily active usage by plan
SELECT 
  sp.name as plan_name,
  DATE(ur.recorded_at) as usage_date,
  COUNT(DISTINCT ur.user_id) as active_users,
  SUM(ur.quantity) as total_usage,
  AVG(ur.quantity) as avg_usage_per_user
FROM usage_records ur
JOIN users u ON ur.user_id = u.id
JOIN subscription_plans sp ON u.current_plan = sp.id
WHERE ur.recorded_at >= NOW() - INTERVAL '30 days'
GROUP BY sp.name, DATE(ur.recorded_at)
ORDER BY usage_date DESC;
```

---

## CUSTOMER SUCCESS DASHBOARD

### Health Score Tracking
```typescript
function calculateHealthScore(user: User): number {
  const metrics = {
    usageConsistency: getUsageConsistency(user.id), // 0-30
    featureAdoption: getFeatureAdoption(user.id),    // 0-25
    supportTickets: getSupportScore(user.id),       // 0-20
    paymentHealth: getPaymentHealth(user.id),       // 0-25
  };
  
  return metrics.usageConsistency + metrics.featureAdoption + 
         metrics.supportTickets + metrics.paymentHealth;
}
```

### Churn Prevention Alerts
- **High Risk (Score < 30):** Immediate intervention required
- **Medium Risk (Score 30-60):** Schedule check-in call
- **Healthy (Score > 60):** Upsell opportunity

### Expansion Revenue Opportunities
- Users approaching plan limits (usage > 80%)
- Teams with >1 active user (upgrade to Business)
- Power users on Starter plan (upgrade to Professional)

---

## FINANCIAL REPORTING VIEWS

### Monthly Recurring Revenue Breakdown
```typescript
interface MRRBreakdown {
  newMRR: number;        // New customer subscriptions
  expansionMRR: number;  // Upgrades & add-ons
  contractionMRR: number; // Downgrades
  churnMRR: number;      // Cancelled subscriptions
  netNewMRR: number;     // Total change
}
```

### Customer Lifetime Value Analysis
```sql
-- CLV calculation by plan
WITH customer_lifetimes AS (
  SELECT 
    u.current_plan,
    u.id as user_id,
    MIN(s.current_period_start) as first_payment,
    MAX(s.current_period_end) as last_payment,
    COUNT(DISTINCT DATE_TRUNC('month', be.processed_at)) as active_months,
    SUM(be.amount_cents) / 100.0 as total_revenue
  FROM users u
  JOIN subscriptions s ON u.id = s.user_id  
  JOIN billing_events be ON u.id = be.user_id
  WHERE be.event_type = 'payment_success'
  GROUP BY u.current_plan, u.id
)
SELECT 
  current_plan,
  AVG(total_revenue) as avg_clv,
  AVG(active_months) as avg_lifetime_months,
  AVG(total_revenue / active_months) as avg_monthly_value
FROM customer_lifetimes
GROUP BY current_plan;
```

---

## DASHBOARD IMPLEMENTATION STACK

### Frontend (Next.js Dashboard)
```typescript
// Dashboard pages structure
pages/
  dashboard/
    index.tsx           // Executive overview
    revenue.tsx         // Revenue analytics  
    customers.tsx       // Customer analytics
    usage.tsx          // Usage analytics
    billing.tsx        // Billing & payments
    
components/
  charts/
    MRRChart.tsx       // Main revenue trend
    CohortChart.tsx    // Retention analysis
    FunnelChart.tsx    // Conversion funnel
    
  metrics/
    MetricCard.tsx     // KPI cards
    HealthScore.tsx    // Customer health
    AlertPanel.tsx     // Urgent actions
```

### Real-Time Updates (WebSocket)
```typescript
// Live metric updates
const dashboardSocket = {
  events: [
    'mrr_updated',
    'new_signup', 
    'subscription_changed',
    'payment_received',
    'churn_alert'
  ],
  updateFrequency: '30s' // Balance performance vs real-time
};
```

### Data Refresh Schedule
- **Real-time:** Current MRR, active trials, today's signups
- **Hourly:** Usage metrics, health scores
- **Daily:** Cohort analysis, CLV calculations  
- **Weekly:** Churn predictions, trend analysis

---

## AUTOMATED REPORTING

### Daily CEO Report (Email)
- Yesterday's key metrics
- Weekly trends
- Urgent alerts requiring attention
- Progress toward monthly target

### Weekly Business Review
- Detailed MRR analysis
- Customer success metrics
- Top opportunities and risks
- Competitive intelligence updates

### Monthly Board Metrics
- Comprehensive revenue performance
- Customer metrics and trends
- Financial projections update
- Strategic recommendations