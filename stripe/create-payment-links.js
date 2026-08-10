#!/usr/bin/env node
/**
 * Create Stripe Payment Links for DDV Coaching products
 * Run: node create-payment-links.js
 */

const https = require('https');

const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;
if (!STRIPE_SECRET_KEY) {
  console.error('Error: Set STRIPE_SECRET_KEY environment variable');
  process.exit(1);
}

function stripeRequest(method, path, data) {
  return new Promise((resolve, reject) => {
    const postData = data ? new URLSearchParams(flattenObject(data)).toString() : '';
    const options = {
      hostname: 'api.stripe.com',
      path: `/v1${path}`,
      method,
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
          reject(new Error(`Stripe: ${parsed.error?.message || body}`));
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

function flattenObject(obj, prefix = '') {
  const result = {};
  for (const [key, value] of Object.entries(obj)) {
    const newKey = prefix ? `${prefix}[${key}]` : key;
    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      Object.assign(result, flattenObject(value, newKey));
    } else {
      result[newKey] = value;
    }
  }
  return result;
}

async function main() {
  console.log('=== Creating Payment Links ===\n');

  // List prices to get the IDs
  const prices = await stripeRequest('GET', '/prices?limit=10&active=true', null);
  
  const results = [];
  for (const price of prices.data) {
    if (!price.metadata || price.product) {
      // Get product name
      const product = await stripeRequest('GET', `/products/${price.product}`, null);
      
      if (product.metadata?.business === 'ddv-coaching') {
        const link = await stripeRequest('POST', '/payment_links', {
          'line_items[0][price]': price.id,
          'line_items[0][quantity]': '1',
          'after_completion[type]': 'redirect',
          'after_completion[redirect][url]': 'https://midnight-dmdecke.com/?payment=success',
        });
        
        console.log(`${product.name}: ${link.url}`);
        results.push({ name: product.name, url: link.url, price: price.unit_amount / 100 });
      }
    }
  }

  console.log('\n=== Payment Links Created ===');
  console.log('\nAdd these to your Hugo site:');
  for (const r of results) {
    console.log(`  ${r.name} ($${r.price}): ${r.url}`);
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
