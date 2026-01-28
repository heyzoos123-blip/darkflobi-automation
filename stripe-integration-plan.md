# Stripe Integration & Billing Architecture

## STRIPE WEBHOOK ARCHITECTURE

### Core Webhooks to Handle
```typescript
// Critical events for billing system
const criticalWebhooks = [
  'customer.subscription.created',
  'customer.subscription.updated', 
  'customer.subscription.deleted',
  'invoice.payment_succeeded',
  'invoice.payment_failed',
  'customer.created',
  'customer.updated',
  'checkout.session.completed'
]
```

### Webhook Processing Flow
1. **Receive Webhook** → Verify signature → Queue for processing
2. **Process Payment** → Update user billing status → Log transaction
3. **Handle Failures** → Retry logic → Alert system → Grace period
4. **Update Usage** → Reset quotas → Enable/disable features

---

## DATABASE SCHEMA DESIGN

### Core Billing Tables

```sql
-- Users table (existing - add billing fields)
ALTER TABLE users ADD COLUMN stripe_customer_id VARCHAR(255);
ALTER TABLE users ADD COLUMN subscription_status VARCHAR(50) DEFAULT 'inactive';
ALTER TABLE users ADD COLUMN current_plan VARCHAR(50) DEFAULT 'free';
ALTER TABLE users ADD COLUMN billing_cycle_start DATE;
ALTER TABLE users ADD COLUMN billing_cycle_end DATE;

-- Subscriptions table
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  stripe_subscription_id VARCHAR(255) UNIQUE,
  plan_name VARCHAR(50) NOT NULL,
  status VARCHAR(50) NOT NULL,
  current_period_start TIMESTAMP,
  current_period_end TIMESTAMP,
  cancel_at_period_end BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Usage tracking table
CREATE TABLE usage_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  resource_type VARCHAR(50), -- 'messages', 'api_calls', 'custom_models'
  quantity INTEGER NOT NULL,
  billing_period VARCHAR(7), -- YYYY-MM format
  recorded_at TIMESTAMP DEFAULT NOW()
);

-- Billing history
CREATE TABLE billing_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  event_type VARCHAR(50), -- 'payment_success', 'payment_failed', 'upgrade', 'downgrade'
  amount_cents INTEGER,
  stripe_invoice_id VARCHAR(255),
  processed_at TIMESTAMP DEFAULT NOW()
);

-- Plan configurations
CREATE TABLE subscription_plans (
  id VARCHAR(50) PRIMARY KEY, -- 'starter', 'professional', etc.
  name VARCHAR(100) NOT NULL,
  price_cents INTEGER NOT NULL,
  billing_interval VARCHAR(20) DEFAULT 'month',
  features JSONB, -- feature flags and limits
  message_limit INTEGER,
  api_limit INTEGER,
  team_member_limit INTEGER DEFAULT 1,
  is_active BOOLEAN DEFAULT true
);
```

### Indexes for Performance
```sql
CREATE INDEX idx_usage_user_period ON usage_records(user_id, billing_period);
CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe ON subscriptions(stripe_subscription_id);
CREATE INDEX idx_billing_events_user ON billing_events(user_id);
```

---

## USAGE METERING SYSTEM

### Real-time Usage Tracking
```typescript
// Usage tracking middleware
export async function trackUsage(
  userId: string, 
  resourceType: 'messages' | 'api_calls' | 'custom_models',
  quantity: number = 1
) {
  const currentPeriod = getCurrentBillingPeriod(userId);
  
  // Atomic increment
  await db.execute(sql`
    INSERT INTO usage_records (user_id, resource_type, quantity, billing_period)
    VALUES (${userId}, ${resourceType}, ${quantity}, ${currentPeriod})
    ON CONFLICT (user_id, resource_type, billing_period) 
    DO UPDATE SET quantity = usage_records.quantity + ${quantity}
  `);
  
  // Check limits and update user status
  await checkUsageLimits(userId, resourceType);
}
```

### Quota Enforcement
```typescript
export async function checkQuota(userId: string, resourceType: string): Promise<boolean> {
  const user = await getUserWithSubscription(userId);
  const currentUsage = await getCurrentUsage(userId, resourceType);
  const limit = getPlanLimit(user.current_plan, resourceType);
  
  return currentUsage < limit;
}
```

---

## BILLING AUTOMATION

### Monthly Billing Cycle
1. **Usage Aggregation** (Last day of month)
2. **Overage Calculation** (If usage > plan limits)
3. **Invoice Generation** (Via Stripe)
4. **Payment Processing** (Automated)
5. **Quota Reset** (First day of new month)

### Overage Billing
```typescript
async function processOverageCharges(userId: string) {
  const usage = await getMonthlyUsage(userId);
  const plan = await getUserPlan(userId);
  
  const overages = calculateOverages(usage, plan);
  
  if (overages.totalCents > 0) {
    await stripe.invoiceItems.create({
      customer: user.stripe_customer_id,
      amount: overages.totalCents,
      currency: 'usd',
      description: `Usage overages for ${getCurrentMonth()}`
    });
  }
}
```

---

## PAYMENT FAILURE HANDLING

### Grace Period Strategy
- **Day 1-3:** Soft limits (warnings, reduced features)
- **Day 4-7:** Hard limits (read-only mode)
- **Day 8+:** Account suspension

### Automated Recovery
```typescript
async function handlePaymentFailure(subscriptionId: string) {
  // 1. Update subscription status
  await updateSubscriptionStatus(subscriptionId, 'past_due');
  
  // 2. Enable grace period
  await enableGracePeriod(userId, 7); // 7 days
  
  // 3. Retry payment (Stripe Smart Retries)
  // 4. Send dunning emails
  await sendPaymentFailureNotification(userId);
  
  // 5. Schedule account suspension if not resolved
  await scheduleAccountReview(userId, 7);
}
```