/**
 * Global Setup for Playwright Tests
 * This file runs once before all tests
 */

async function globalSetup(config) {
  console.log('🚀 Starting global setup for Cypress Real World App tests...');
  
  // Log test environment details
  console.log('📋 Test Environment Configuration:');
  console.log(`   - Base URL: ${config.use.baseURL}`);
  console.log(`   - Browser projects: ${config.projects.map(p => p.name).join(', ')}`);
  console.log(`   - Parallel workers: ${config.workers || 'auto'}`);
  console.log(`   - Retries: ${config.retries}`);
  
  // Verify application is accessible
  try {
    const { chromium } = require('@playwright/test');
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    console.log('🔍 Checking application availability...');
    await page.goto(config.use.baseURL, { waitUntil: 'networkidle' });
    
    // Verify the app is running
    const title = await page.title();
    console.log(`   ✅ Application is accessible - Title: ${title}`);
    
    // Check if sign-in page is available
    if (await page.locator('[data-test="signin-username"]').isVisible()) {
      console.log('   ✅ Sign-in page is accessible');
    }
    
    await browser.close();
  } catch (error) {
    console.error('❌ Application setup check failed:', error.message);
    console.error('   Please ensure the application is running on http://localhost:3000');
    throw error;
  }
  
  // Create directories for test artifacts
  const fs = require('fs');
  const path = require('path');
  
  const dirs = [
    'manual-tests/playwright/screenshots',
    'manual-tests/playwright/reports',
    'manual-tests/playwright/test-results'
  ];
  
  dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
      console.log(`   📁 Created directory: ${dir}`);
    }
  });
  
  console.log('✅ Global setup completed successfully');
  console.log('');
}

module.exports = globalSetup;
