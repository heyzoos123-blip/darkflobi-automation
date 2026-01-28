# Subscription System Architecture
**Detailed Technical Implementation Guide**

## Database Schema Implementation

### 1. Create Migration Files

```typescript
// lib/db/migrations/0009_add_subscriptions.sql
-- Subscription plans configuration
CREATE TABLE subscription_plans (
  id VARCHAR(50) PRIMARY KEY, -- 'free', 'starter', 'pro', 'enterprise'
  name VARCHAR(100) NOT NULL,
  price_cents INTEGER NOT NULL DEFAULT 0,
  billing_period VARCHAR(20) NOT NULL DEFAULT 'month', -- 'month', 'year'
  max_chats_per_month INTEGER DEFAULT -1, -- -1 = unlimited
  max_documents INTEGER DEFAULT -1,
  allowed_models TEXT[] DEFAULT '{}', -- JSON array of model IDs
  api_access BOOLEAN DEFAULT FALSE,
  priority_support BOOLEAN DEFAULT FALSE,
  custom_branding BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- User subscriptions
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES "User"(id) ON DELETE CASCADE,
  plan_id VARCHAR(50) REFERENCES subscription_plans(id),
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  -- 'active', 'canceled', 'past_due', 'unpaid', 'trialing'
  
  -- Stripe integration
  stripe_customer_id VARCHAR(255) UNIQUE,
  stripe_subscription_id VARCHAR(255) UNIQUE,
  stripe_product_id VARCHAR(255),
  stripe_price_id VARCHAR(255),
  
  -- Billing periods
  current_period_start TIMESTAMP NOT NULL,
  current_period_end TIMESTAMP NOT NULL,
  trial_end TIMESTAMP,
  
  -- Cancellation
  cancel_at_period_end BOOLEAN DEFAULT FALSE,
  canceled_at TIMESTAMP,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(user_id) -- One subscription per user
);

-- Usage tracking for billing and limits
CREATE TABLE usage_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES "User"(id) ON DELETE CASCADE,
  subscription_id UUID REFERENCES subscriptions(id) ON DELETE CASCADE,
  
  -- Resource tracking
  resource_type VARCHAR(50) NOT NULL, 
  -- 'chat_message', 'document_create', 'document_edit', 'api_call'
  resource_id UUID, -- chat.id, document.id, etc.
  
  -- Usage metrics
  tokens_used INTEGER DEFAULT 0,
  model_used VARCHAR(100),
  cost_cents INTEGER DEFAULT 0, -- Our cost for this usage
  
  -- Metadata
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Indexes for fast queries
  INDEX idx_usage_user_date (user_id, created_at),
  INDEX idx_usage_subscription_date (subscription_id, created_at),
  INDEX idx_usage_resource_type (resource_type, created_at)
);

-- Monthly usage aggregates (for performance)
CREATE TABLE usage_monthly_aggregates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES "User"(id) ON DELETE CASCADE,
  subscription_id UUID REFERENCES subscriptions(id) ON DELETE CASCADE,
  
  year_month VARCHAR(7) NOT NULL, -- '2024-01'
  
  -- Aggregated metrics
  total_chats INTEGER DEFAULT 0,
  total_documents INTEGER DEFAULT 0,
  total_api_calls INTEGER DEFAULT 0,
  total_tokens INTEGER DEFAULT 0,
  total_cost_cents INTEGER DEFAULT 0,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(user_id, year_month)
);

-- Insert default plans
INSERT INTO subscription_plans (id, name, price_cents, max_chats_per_month, max_documents, allowed_models, api_access) VALUES
('free', 'Free', 0, 5, 2, '["google/gemini-2.5-flash-lite"]', false),
('starter', 'Starter', 2900, 100, 10, '["google/gemini-2.5-flash-lite", "anthropic/claude-haiku-4.5", "openai/gpt-4.1-mini"]', false),
('pro', 'Pro', 7900, -1, -1, '["google/gemini-2.5-flash-lite", "anthropic/claude-haiku-4.5", "anthropic/claude-sonnet-4.5", "openai/gpt-4.1-mini", "openai/gpt-5.2", "google/gemini-3-pro-preview"]', true),
('enterprise', 'Enterprise', 19900, -1, -1, '["*"]', true);
```

### 2. Update Drizzle Schema

```typescript
// lib/db/schema.ts - Add to existing file

export const subscriptionPlans = pgTable("subscription_plans", {
  id: varchar("id", { length: 50 }).primaryKey(),
  name: varchar("name", { length: 100 }).notNull(),
  priceCents: integer("price_cents").notNull().default(0),
  billingPeriod: varchar("billing_period", { length: 20 }).notNull().default("month"),
  maxChatsPerMonth: integer("max_chats_per_month").default(-1),
  maxDocuments: integer("max_documents").default(-1),
  allowedModels: text("allowed_models").array().default([]),
  apiAccess: boolean("api_access").default(false),
  prioritySupport: boolean("priority_support").default(false),
  customBranding: boolean("custom_branding").default(false),
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
});

export const subscriptions = pgTable("subscriptions", {
  id: uuid("id").primaryKey().defaultRandom(),
  userId: uuid("user_id").references(() => user.id, { onDelete: "cascade" }),
  planId: varchar("plan_id", { length: 50 }).references(() => subscriptionPlans.id),
  status: varchar("status", { length: 20 }).notNull().default("active"),
  
  // Stripe fields
  stripeCustomerId: varchar("stripe_customer_id", { length: 255 }).unique(),
  stripeSubscriptionId: varchar("stripe_subscription_id", { length: 255 }).unique(),
  stripeProductId: varchar("stripe_product_id", { length: 255 }),
  stripePriceId: varchar("stripe_price_id", { length: 255 }),
  
  // Billing
  currentPeriodStart: timestamp("current_period_start").notNull(),
  currentPeriodEnd: timestamp("current_period_end").notNull(),
  trialEnd: timestamp("trial_end"),
  
  // Cancellation
  cancelAtPeriodEnd: boolean("cancel_at_period_end").default(false),
  canceledAt: timestamp("canceled_at"),
  
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
}, (table) => ({
  uniqueUserId: unique().on(table.userId),
}));

export const usageLogs = pgTable("usage_logs", {
  id: uuid("id").primaryKey().defaultRandom(),
  userId: uuid("user_id").references(() => user.id, { onDelete: "cascade" }),
  subscriptionId: uuid("subscription_id").references(() => subscriptions.id, { onDelete: "cascade" }),
  
  resourceType: varchar("resource_type", { length: 50 }).notNull(),
  resourceId: uuid("resource_id"),
  
  tokensUsed: integer("tokens_used").default(0),
  modelUsed: varchar("model_used", { length: 100 }),
  costCents: integer("cost_cents").default(0),
  
  metadata: json("metadata").default({}),
  createdAt: timestamp("created_at").defaultNow(),
}, (table) => ({
  userDateIdx: index("idx_usage_user_date").on(table.userId, table.createdAt),
  subscriptionDateIdx: index("idx_usage_subscription_date").on(table.subscriptionId, table.createdAt),
  resourceTypeIdx: index("idx_usage_resource_type").on(table.resourceType, table.createdAt),
}));

export type SubscriptionPlan = InferSelectModel<typeof subscriptionPlans>;
export type Subscription = InferSelectModel<typeof subscriptions>;
export type UsageLog = InferSelectModel<typeof usageLogs>;
```

## Stripe Integration

### 1. Stripe Configuration

```typescript
// lib/stripe/config.ts
import Stripe from 'stripe';

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
  typescript: true,
});

export const STRIPE_CONFIG = {
  publishableKey: process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!,
  webhookSecret: process.env.STRIPE_WEBHOOK_SECRET!,
  successUrl: `${process.env.NEXT_PUBLIC_BASE_URL}/billing/success`,
  cancelUrl: `${process.env.NEXT_PUBLIC_BASE_URL}/billing/canceled`,
};

// Product and price mappings
export const STRIPE_PRODUCTS = {
  starter: {
    productId: 'prod_starter_123',
    priceId: 'price_starter_monthly_456',
  },
  pro: {
    productId: 'prod_pro_123', 
    priceId: 'price_pro_monthly_456',
  },
  enterprise: {
    productId: 'prod_enterprise_123',
    priceId: 'price_enterprise_monthly_456',
  },
} as const;
```

### 2. Subscription Service

```typescript
// lib/stripe/subscription-service.ts
import { stripe, STRIPE_PRODUCTS } from './config';
import { db } from '@/lib/db';
import { subscriptions, subscriptionPlans } from '@/lib/db/schema';
import { eq, and } from 'drizzle-orm';

export class SubscriptionService {
  // Create Stripe customer and subscription
  static async createSubscription(userId: string, planId: keyof typeof STRIPE_PRODUCTS, email: string) {
    try {
      // Get plan details
      const plan = await db.select().from(subscriptionPlans).where(eq(subscriptionPlans.id, planId)).limit(1);
      if (!plan[0]) throw new Error('Plan not found');

      // Create or get Stripe customer
      const customer = await stripe.customers.create({
        email,
        metadata: { userId },
      });

      // Create subscription with trial
      const subscription = await stripe.subscriptions.create({
        customer: customer.id,
        items: [{ price: STRIPE_PRODUCTS[planId].priceId }],
        trial_period_days: 7, // 7-day free trial
        payment_behavior: 'default_incomplete',
        payment_settings: { save_default_payment_method: 'on_subscription' },
        expand: ['latest_invoice.payment_intent'],
      });

      // Save to database
      await db.insert(subscriptions).values({
        userId,
        planId,
        status: 'trialing',
        stripeCustomerId: customer.id,
        stripeSubscriptionId: subscription.id,
        stripeProductId: STRIPE_PRODUCTS[planId].productId,
        stripePriceId: STRIPE_PRODUCTS[planId].priceId,
        currentPeriodStart: new Date(subscription.current_period_start * 1000),
        currentPeriodEnd: new Date(subscription.current_period_end * 1000),
        trialEnd: subscription.trial_end ? new Date(subscription.trial_end * 1000) : null,
      });

      return {
        subscriptionId: subscription.id,
        clientSecret: (subscription.latest_invoice as any)?.payment_intent?.client_secret,
      };
    } catch (error) {
      console.error('Failed to create subscription:', error);
      throw error;
    }
  }

  // Cancel subscription
  static async cancelSubscription(userId: string, cancelAtPeriodEnd = true) {
    const userSub = await db.select()
      .from(subscriptions)
      .where(eq(subscriptions.userId, userId))
      .limit(1);

    if (!userSub[0]) throw new Error('Subscription not found');

    if (cancelAtPeriodEnd) {
      await stripe.subscriptions.update(userSub[0].stripeSubscriptionId!, {
        cancel_at_period_end: true,
      });
      
      await db.update(subscriptions)
        .set({ cancelAtPeriodEnd: true })
        .where(eq(subscriptions.id, userSub[0].id));
    } else {
      await stripe.subscriptions.cancel(userSub[0].stripeSubscriptionId!);
      
      await db.update(subscriptions)
        .set({ status: 'canceled', canceledAt: new Date() })
        .where(eq(subscriptions.id, userSub[0].id));
    }
  }

  // Update subscription plan
  static async updateSubscription(userId: string, newPlanId: keyof typeof STRIPE_PRODUCTS) {
    const userSub = await db.select()
      .from(subscriptions)
      .where(eq(subscriptions.userId, userId))
      .limit(1);

    if (!userSub[0]) throw new Error('Subscription not found');

    // Update Stripe subscription
    const stripeSubscription = await stripe.subscriptions.retrieve(userSub[0].stripeSubscriptionId!);
    await stripe.subscriptions.update(userSub[0].stripeSubscriptionId!, {
      items: [{
        id: stripeSubscription.items.data[0].id,
        price: STRIPE_PRODUCTS[newPlanId].priceId,
      }],
      proration_behavior: 'create_prorations',
    });

    // Update database
    await db.update(subscriptions)
      .set({ 
        planId: newPlanId,
        stripeProductId: STRIPE_PRODUCTS[newPlanId].productId,
        stripePriceId: STRIPE_PRODUCTS[newPlanId].priceId,
      })
      .where(eq(subscriptions.id, userSub[0].id));
  }
}
```

### 3. Webhook Handler

```typescript
// app/api/stripe/webhook/route.ts
import { NextRequest } from 'next/server';
import { stripe } from '@/lib/stripe/config';
import { db } from '@/lib/db';
import { subscriptions } from '@/lib/db/schema';
import { eq } from 'drizzle-orm';

export async function POST(request: NextRequest) {
  const body = await request.text();
  const signature = request.headers.get('stripe-signature');

  if (!signature) {
    return new Response('No signature', { status: 400 });
  }

  try {
    const event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );

    switch (event.type) {
      case 'customer.subscription.created':
      case 'customer.subscription.updated':
        await handleSubscriptionUpdate(event.data.object);
        break;
        
      case 'customer.subscription.deleted':
        await handleSubscriptionDeleted(event.data.object);
        break;
        
      case 'invoice.payment_succeeded':
        await handlePaymentSucceeded(event.data.object);
        break;
        
      case 'invoice.payment_failed':
        await handlePaymentFailed(event.data.object);
        break;
        
      default:
        console.log(`Unhandled event type: ${event.type}`);
    }

    return new Response('OK', { status: 200 });
  } catch (error) {
    console.error('Webhook error:', error);
    return new Response('Webhook error', { status: 400 });
  }
}

async function handleSubscriptionUpdate(subscription: any) {
  await db.update(subscriptions)
    .set({
      status: subscription.status,
      currentPeriodStart: new Date(subscription.current_period_start * 1000),
      currentPeriodEnd: new Date(subscription.current_period_end * 1000),
      cancelAtPeriodEnd: subscription.cancel_at_period_end,
      canceledAt: subscription.canceled_at ? new Date(subscription.canceled_at * 1000) : null,
    })
    .where(eq(subscriptions.stripeSubscriptionId, subscription.id));
}

async function handleSubscriptionDeleted(subscription: any) {
  await db.update(subscriptions)
    .set({
      status: 'canceled',
      canceledAt: new Date(),
    })
    .where(eq(subscriptions.stripeSubscriptionId, subscription.id));
}
```

## Usage Tracking System

### 1. Usage Tracker Service

```typescript
// lib/usage/usage-tracker.ts
import { db } from '@/lib/db';
import { usageLogs, usageMonthlyAggregates, subscriptions, subscriptionPlans } from '@/lib/db/schema';
import { eq, and, gte, sql } from 'drizzle-orm';

export interface UsageContext {
  userId: string;
  resourceType: 'chat_message' | 'document_create' | 'document_edit' | 'api_call';
  resourceId?: string;
  tokensUsed?: number;
  modelUsed?: string;
  costCents?: number;
  metadata?: Record<string, any>;
}

export class UsageTracker {
  // Log usage event
  static async logUsage(context: UsageContext) {
    const { userId, resourceType, resourceId, tokensUsed = 0, modelUsed, costCents = 0, metadata = {} } = context;
    
    // Get user's subscription
    const userSub = await this.getUserSubscription(userId);
    if (!userSub) {
      console.warn(`No subscription found for user ${userId}`);
      return;
    }

    // Log the usage
    await db.insert(usageLogs).values({
      userId,
      subscriptionId: userSub.id,
      resourceType,
      resourceId,
      tokensUsed,
      modelUsed,
      costCents,
      metadata,
    });

    // Update monthly aggregates
    await this.updateMonthlyAggregate(userId, userSub.id, resourceType, tokensUsed, costCents);
  }

  // Check if user can perform action based on their plan limits
  static async checkUsageLimit(userId: string, resourceType: string): Promise<{
    allowed: boolean;
    remainingUsage?: number;
    upgradeRequired?: boolean;
  }> {
    const userSub = await this.getUserSubscription(userId);
    if (!userSub) return { allowed: false, upgradeRequired: true };

    const plan = await db.select().from(subscriptionPlans).where(eq(subscriptionPlans.id, userSub.planId)).limit(1);
    if (!plan[0]) return { allowed: false };

    const currentMonth = new Date().toISOString().slice(0, 7); // 'YYYY-MM'
    
    switch (resourceType) {
      case 'chat_message':
        if (plan[0].maxChatsPerMonth === -1) return { allowed: true }; // Unlimited
        
        const chatUsage = await this.getMonthlyUsage(userId, currentMonth, 'total_chats');
        const remaining = plan[0].maxChatsPerMonth - chatUsage;
        
        return {
          allowed: remaining > 0,
          remainingUsage: Math.max(0, remaining),
          upgradeRequired: remaining <= 0,
        };
        
      case 'document_create':
        if (plan[0].maxDocuments === -1) return { allowed: true };
        
        // Count total documents (not monthly)
        const docCount = await db.select({ count: sql<number>`count(*)` })
          .from(document)
          .where(eq(document.userId, userId));
          
        const docsRemaining = plan[0].maxDocuments - docCount[0].count;
        
        return {
          allowed: docsRemaining > 0,
          remainingUsage: Math.max(0, docsRemaining),
          upgradeRequired: docsRemaining <= 0,
        };
        
      default:
        return { allowed: true };
    }
  }

  // Get user's current subscription with plan details
  private static async getUserSubscription(userId: string) {
    const result = await db.select()
      .from(subscriptions)
      .where(and(
        eq(subscriptions.userId, userId),
        eq(subscriptions.status, 'active')
      ))
      .limit(1);
      
    return result[0] || null;
  }

  // Update monthly usage aggregates
  private static async updateMonthlyAggregate(
    userId: string, 
    subscriptionId: string, 
    resourceType: string, 
    tokensUsed: number, 
    costCents: number
  ) {
    const yearMonth = new Date().toISOString().slice(0, 7);
    
    const incrementField = resourceType === 'chat_message' ? 'total_chats' :
                          resourceType.includes('document') ? 'total_documents' :
                          resourceType === 'api_call' ? 'total_api_calls' : null;
    
    if (!incrementField) return;

    // Upsert monthly aggregate
    await db.insert(usageMonthlyAggregates)
      .values({
        userId,
        subscriptionId,
        yearMonth,
        [incrementField]: 1,
        totalTokens: tokensUsed,
        totalCostCents: costCents,
      })
      .onConflictDoUpdate({
        target: [usageMonthlyAggregates.userId, usageMonthlyAggregates.yearMonth],
        set: {
          [incrementField]: sql`${usageMonthlyAggregates[incrementField]} + 1`,
          totalTokens: sql`${usageMonthlyAggregates.totalTokens} + ${tokensUsed}`,
          totalCostCents: sql`${usageMonthlyAggregates.totalCostCents} + ${costCents}`,
          updatedAt: new Date(),
        },
      });
  }

  // Get monthly usage for a specific metric
  private static async getMonthlyUsage(userId: string, yearMonth: string, metric: string): Promise<number> {
    const result = await db.select({ value: usageMonthlyAggregates[metric] })
      .from(usageMonthlyAggregates)
      .where(and(
        eq(usageMonthlyAggregates.userId, userId),
        eq(usageMonthlyAggregates.yearMonth, yearMonth)
      ))
      .limit(1);
      
    return result[0]?.value || 0;
  }
}
```

### 2. Usage Middleware

```typescript
// lib/middleware/usage-middleware.ts
import { NextRequest, NextResponse } from 'next/server';
import { getSession } from '@/lib/auth/session';
import { UsageTracker } from '@/lib/usage/usage-tracker';

export async function withUsageTracking(
  request: NextRequest,
  resourceType: string,
  handler: (request: NextRequest) => Promise<NextResponse>
) {
  const session = await getSession();
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Check usage limits before processing
  const usageCheck = await UsageTracker.checkUsageLimit(session.user.id, resourceType);
  
  if (!usageCheck.allowed) {
    return NextResponse.json({
      error: 'Usage limit exceeded',
      upgradeRequired: usageCheck.upgradeRequired,
      remainingUsage: usageCheck.remainingUsage,
    }, { status: 429 });
  }

  // Process the request
  const response = await handler(request);
  
  // If successful, log the usage
  if (response.status < 400) {
    await UsageTracker.logUsage({
      userId: session.user.id,
      resourceType,
      // Extract additional context from request/response as needed
    });
  }

  // Add usage headers
  response.headers.set('X-Remaining-Usage', String(usageCheck.remainingUsage || -1));
  
  return response;
}
```

## API Routes with Usage Tracking

### 1. Enhanced Chat API

```typescript
// app/api/chat/route.ts
import { withUsageTracking } from '@/lib/middleware/usage-middleware';
import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  return withUsageTracking(request, 'chat_message', async (req) => {
    // Your existing chat logic here
    const { messages, model } = await req.json();
    
    // ... AI processing ...
    
    // Enhanced logging will happen automatically via middleware
    return NextResponse.json({ response: aiResponse });
  });
}
```

### 2. Subscription Management API

```typescript
// app/api/subscription/route.ts
import { NextRequest } from 'next/server';
import { getSession } from '@/lib/auth/session';
import { SubscriptionService } from '@/lib/stripe/subscription-service';

export async function POST(request: NextRequest) {
  const session = await getSession();
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { planId } = await request.json();
  
  try {
    const result = await SubscriptionService.createSubscription(
      session.user.id,
      planId,
      session.user.email
    );
    
    return NextResponse.json(result);
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 400 });
  }
}

export async function DELETE(request: NextRequest) {
  const session = await getSession();
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    await SubscriptionService.cancelSubscription(session.user.id);
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 400 });
  }
}
```

## Frontend Components

### 1. Subscription Plans Component

```typescript
// components/subscription/pricing-plans.tsx
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CheckIcon } from 'lucide-react';

const plans = [
  {
    id: 'starter',
    name: 'Starter',
    price: 29,
    description: 'Perfect for individuals getting started with AI',
    features: [
      '100 AI conversations/month',
      'Basic models (Gemini Flash, Claude Haiku)',
      '10 documents',
      'Email support',
      '7-day free trial',
    ],
    popular: false,
  },
  {
    id: 'pro',
    name: 'Pro',
    price: 79,
    description: 'Best for professionals and growing teams',
    features: [
      'Unlimited AI conversations',
      'All premium models (GPT-5, Claude Opus)',
      'Unlimited documents',
      'Priority support',
      'API access',
      'Advanced analytics',
    ],
    popular: true,
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: 199,
    description: 'For organizations with advanced needs',
    features: [
      'Everything in Pro',
      'Custom model fine-tuning',
      'White-label branding',
      'Dedicated support',
      'SLA guarantees',
      'Custom integrations',
    ],
    popular: false,
  },
];

export function PricingPlans() {
  const [loading, setLoading] = useState<string | null>(null);

  const handleSubscribe = async (planId: string) => {
    setLoading(planId);
    try {
      const response = await fetch('/api/subscription', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ planId }),
      });

      const result = await response.json();
      
      if (result.clientSecret) {
        // Redirect to Stripe Checkout or handle payment
        window.location.href = `/billing/checkout?session_id=${result.subscriptionId}`;
      }
    } catch (error) {
      console.error('Subscription error:', error);
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto">
      {plans.map((plan) => (
        <Card key={plan.id} className={`relative ${plan.popular ? 'border-primary shadow-lg' : ''}`}>
          {plan.popular && (
            <Badge className="absolute -top-2 left-1/2 -translate-x-1/2">
              Most Popular
            </Badge>
          )}
          <CardHeader>
            <CardTitle className="text-2xl">{plan.name}</CardTitle>
            <div className="text-4xl font-bold">
              ${plan.price}
              <span className="text-sm text-muted-foreground">/month</span>
            </div>
            <p className="text-muted-foreground">{plan.description}</p>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3 mb-6">
              {plan.features.map((feature) => (
                <li key={feature} className="flex items-start gap-2">
                  <CheckIcon className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <span className="text-sm">{feature}</span>
                </li>
              ))}
            </ul>
            <Button
              className="w-full"
              variant={plan.popular ? 'default' : 'outline'}
              onClick={() => handleSubscribe(plan.id)}
              disabled={loading === plan.id}
            >
              {loading === plan.id ? 'Processing...' : 'Start Free Trial'}
            </Button>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
```

### 2. Usage Dashboard Component

```typescript
// components/subscription/usage-dashboard.tsx
'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';

interface UsageData {
  plan: string;
  chatsUsed: number;
  chatsLimit: number;
  documentsUsed: number;
  documentsLimit: number;
  tokensUsed: number;
  billingPeriodEnd: string;
}

export function UsageDashboard() {
  const [usage, setUsage] = useState<UsageData | null>(null);

  useEffect(() => {
    fetch('/api/subscription/usage')
      .then(res => res.json())
      .then(setUsage);
  }, []);

  if (!usage) return <div>Loading...</div>;

  const chatProgress = usage.chatsLimit === -1 ? 0 : (usage.chatsUsed / usage.chatsLimit) * 100;
  const docProgress = usage.documentsLimit === -1 ? 0 : (usage.documentsUsed / usage.documentsLimit) * 100;

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            Current Plan: {usage.plan}
            <Badge variant="secondary">
              Renews {new Date(usage.billingPeriodEnd).toLocaleDateString()}
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Chat Usage */}
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm font-medium">Chat Conversations</span>
              <span className="text-sm text-muted-foreground">
                {usage.chatsUsed} / {usage.chatsLimit === -1 ? '∞' : usage.chatsLimit}
              </span>
            </div>
            <Progress value={chatProgress} className="h-2" />
            {chatProgress > 80 && (
              <p className="text-sm text-amber-600 mt-1">
                You're approaching your monthly limit. Consider upgrading.
              </p>
            )}
          </div>

          {/* Document Usage */}
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm font-medium">Documents Created</span>
              <span className="text-sm text-muted-foreground">
                {usage.documentsUsed} / {usage.documentsLimit === -1 ? '∞' : usage.documentsLimit}
              </span>
            </div>
            <Progress value={docProgress} className="h-2" />
          </div>

          {/* Token Usage */}
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm font-medium">Total Tokens Used</span>
              <span className="text-sm text-muted-foreground">
                {usage.tokensUsed.toLocaleString()}
              </span>
            </div>
            <p className="text-xs text-muted-foreground">
              Tokens measure the amount of text processed by AI models
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
```

This detailed architecture provides the complete foundation for implementing a subscription system that can achieve the $4,900/month revenue target. The system is designed for scalability, reliability, and ease of implementation by the development team.