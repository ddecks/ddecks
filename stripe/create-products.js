#!/usr/bin/env node
/**
 * Create Stripe products and prices for DDV Coaching
 * Run: node create-products.js
 * 
 * This creates the products in your Stripe account that you can then
 * use to generate Payment Links from the Dashboard.
 */

const https = require('https');

const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;
if (!STRIPE_SECRET_KEY) {
  console.error('Error: Set STRIPE_SECRET_KEY environment variable');
  process.exit(1);
}

function stripeRequest(method, path, data) {
  return new Promise((resolve, reject) => {
    const postData = data ? new URLSearchParams(data).toString() : '';
    const options = {
      hostname: 'api.stripe.com',
      path: `/v1${path}`,
      method: method,
      headers: {
        'Authorization': `Bearer ${STRIPE_SECRET_KEY}`,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': Buffer.byteLength(postData),
      },
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        const parsed = JSON.parse(body);
        if (res.statusCode >= 400) {
          reject(new Error(`Stripe API error: ${parsed.error?.message || body}`));
        } else {
          resolve(parsed);
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

async function createProduct(name, description, priceInCents, recurring = false) {
  console.log(`Creating product: ${name}...`);
  
  const product = await stripeRequest('POST', '/products', {
    name,
    description,
    'metadata[business]': 'ddv-coaching',
  });

  const priceData = {
    product: product.id,
    'unit_amount': priceInCents.toString(),
    currency: 'usd',
  };

  if (recurring) {
    priceData['recurring[interval]'] = 'month';
  }

  const price = await stripeRequest('POST', '/prices', priceData);

  console.log(`  ✓ Product: ${product.id}`);
  console.log(`  ✓ Price: ${price.id} ($${priceInCents / 100}${recurring ? '/mo' : ''})`);
  console.log('');

  return { product, price };
}

async function main() {
  console.log('=== Creating DDV Coaching Products ===\n');

  try {
    await createProduct(
      'Private Coaching Session',
      '1-on-1 on-sand beach volleyball coaching. Technique, strategy, and positioning tailored to your goals.',
      7500 // $75
    );

    await createProduct(
      'Group Training Session',
      'Small group session (2-6 players) with structured drills and competitive game situations.',
      4000 // $40 per person
    );

    await createProduct(
      'Video Analysis',
      'Detailed breakdown of your match footage with personalized feedback and training recommendations.',
      5000 // $50
    );

    await createProduct(
      'Monthly Coaching Plan',
      'Ongoing coaching: 4 private sessions/month + unlimited video review + priority scheduling.',
      25000, // $250/month
      true // recurring
    );

    console.log('=== All products created! ===');
    console.log('\nNext steps:');
    console.log('1. Go to https://dashboard.stripe.com/test/products');
    console.log('2. Click on each product → "Create payment link"');
    console.log('3. Copy the payment link URLs');
    console.log('4. Add them to your Hugo site coaching section');

  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

main();
