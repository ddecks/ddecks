# Stripe Integration Plan — Devin Decker Volleyball

## Business Context
- **Business type**: Volleyball coaching (private sessions, group training, video analysis)
- **Domain**: midnight-dmdecke.com
- **Integration goal**: Accept payments for coaching services; satisfy Stripe business verification

## Recommended Approach: Stripe Payment Links + Checkout

For a coaching business that doesn't yet have complex needs, Payment Links are the fastest path:

1. **Payment Links** — No code needed, create in Stripe Dashboard
   - Private Session: $75/hr
   - Group Training: $40/person
   - Video Analysis: $50/session
   
2. **Checkout Sessions** (optional upgrade) — Custom server-side flow
   - More control over the experience
   - Can embed directly in the Hugo site
   - Supports subscriptions (monthly coaching plans)

## Architecture

```
Hugo Site (static, GitHub Pages)
  └── Links to Stripe Payment Links (zero-code)
  └── OR links to a small serverless function for Checkout Sessions

Option A: Payment Links (recommended to start)
  [Hugo site] → [Stripe-hosted Payment Link page] → [Payment complete]

Option B: Checkout Sessions (for later)
  [Hugo site] → [AWS Lambda / Vercel function] → [Stripe Checkout] → [Webhook → confirm]
```

## Implementation Steps

### Phase 1 (Now): Payment Links
1. Create products in Stripe Dashboard (or via API — see create-products.js)
2. Generate Payment Links for each product
3. Add link buttons to the Hugo coaching site
4. Stripe handles all checkout UX, receipts, etc.

### Phase 2 (Later): Checkout Sessions
1. Deploy a small serverless API (Lambda or Vercel)
2. Create Checkout Sessions dynamically
3. Handle webhooks for fulfillment
4. Add subscription plans for recurring coaching

## Files
- `create-products.js` — Script to create Stripe products/prices via API
- `payment-links.md` — Instructions for creating Payment Links in Dashboard
- `checkout-session/` — (future) Serverless function for custom checkout

## Keys
Store in environment variables — never commit to repo:
```bash
export STRIPE_SECRET_KEY=sk_test_...
export STRIPE_PUBLISHABLE_KEY=pk_test_...
```

Switch to live keys after verification is complete.
