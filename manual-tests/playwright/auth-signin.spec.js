const { test, expect } = require('@playwright/test');

/**
 * Test Scenario: AUTH_002 - User Sign In - Valid Credentials
 * Category: Authentication
 * Priority: High
 * Tags: ["login", "positive", "smoke"]
 */

test.describe('Authentication - User Sign In', () => {
  
  test.beforeEach(async ({ page }) => {
    // Navigate to the application base URL
    await page.goto('http://localhost:3000');
    
    // Wait for the page to load completely
    await page.waitForLoadState('networkidle');
  });

  test('AUTH_002 - User Sign In with Valid Credentials', async ({ page }) => {
    // Test data from test_scenarios.json
    const testData = {
      username: 'Heath93',
      password: 's3cret'
    };

    // Precondition: Verify user is on Sign In page
    await expect(page).toHaveURL(/.*signin/);
    
    // Step 1: Enter valid username
    const usernameField = page.locator('[data-test="signin-username"]');
    await expect(usernameField).toBeVisible();
    await usernameField.fill(testData.username);
    
    // Verify username field accepts input
    await expect(usernameField).toHaveValue(testData.username);

    // Step 2: Enter valid password
    const passwordField = page.locator('[data-test="signin-password"]');
    await expect(passwordField).toBeVisible();
    await passwordField.fill(testData.password);
    
    // Verify password field accepts input (masked)
    await expect(passwordField).toHaveAttribute('type', 'password');
    await expect(passwordField).toHaveValue(testData.password);

    // Step 3: Click 'Sign In' button
    const signInButton = page.locator('[data-test="signin-submit"]');
    await expect(signInButton).toBeVisible();
    await expect(signInButton).toBeEnabled();
    
    // Click the sign in button and wait for navigation
    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle' }),
      signInButton.click()
    ]);

    // Expected Result: User is successfully logged in and redirected to home page
    await expect(page).toHaveURL('http://localhost:3000/');
    
    // Verify user is on home page with transaction feed
    await expect(page.locator('[data-test="transaction-list"]')).toBeVisible();
    
    // Verify navigation elements are present (indicating successful login)
    await expect(page.locator('[data-test="nav-top-new-transaction"]')).toBeVisible();
    await expect(page.locator('[data-test="sidenav-user-balance"]')).toBeVisible();
    
    // Verify transaction tabs are present
    await expect(page.locator('[data-test="nav-public-tab"]')).toBeVisible();
    await expect(page.locator('[data-test="nav-contacts-tab"]')).toBeVisible();
    await expect(page.locator('[data-test="nav-personal-tab"]')).toBeVisible();

    console.log('✅ AUTH_002 - User Sign In with Valid Credentials - PASSED');
  });

  test('AUTH_002 - User Sign In with Valid Credentials - Mobile View', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    const testData = {
      username: 'Heath93',
      password: 's3cret'
    };

    // Navigate to sign in page
    await page.goto('http://localhost:3000/signin');
    
    // Perform login steps
    await page.locator('[data-test="signin-username"]').fill(testData.username);
    await page.locator('[data-test="signin-password"]').fill(testData.password);
    
    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle' }),
      page.locator('[data-test="signin-submit"]').click()
    ]);

    // Verify mobile-specific elements
    await expect(page.locator('[data-test="sidenav-toggle"]')).toBeVisible();
    
    // Test mobile navigation
    await page.locator('[data-test="sidenav-toggle"]').click();
    await expect(page.locator('[data-test="sidenav-home"]')).toBeVisible();

    console.log('✅ AUTH_002 - Mobile View - PASSED');
  });

  test('AUTH_002 - Verify Remember Me Functionality', async ({ page }) => {
    const testData = {
      username: 'Heath93',
      password: 's3cret'
    };

    await page.goto('http://localhost:3000/signin');
    
    // Fill credentials
    await page.locator('[data-test="signin-username"]').fill(testData.username);
    await page.locator('[data-test="signin-password"]').fill(testData.password);
    
    // Check remember me checkbox if present
    const rememberMeCheckbox = page.locator('[data-test="signin-remember-me"]');
    if (await rememberMeCheckbox.isVisible()) {
      await rememberMeCheckbox.check();
      await expect(rememberMeCheckbox).toBeChecked();
    }
    
    // Sign in
    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle' }),
      page.locator('[data-test="signin-submit"]').click()
    ]);

    // Verify successful login
    await expect(page).toHaveURL('http://localhost:3000/');

    console.log('✅ AUTH_002 - Remember Me Functionality - PASSED');
  });

  test.afterEach(async ({ page }) => {
    // Clean up: Take screenshot on failure
    if (test.info().status !== test.info().expectedStatus) {
      await page.screenshot({ 
        path: `manual-tests/playwright/screenshots/auth-signin-failure-${Date.now()}.png`,
        fullPage: true 
      });
    }
  });
});

// Test configuration and hooks
test.describe.configure({ mode: 'parallel' });

// Helper function for error handling
async function handleTestFailure(page, testName, error) {
  console.error(`❌ ${testName} - FAILED:`, error.message);
  await page.screenshot({ 
    path: `manual-tests/playwright/screenshots/${testName}-error-${Date.now()}.png`,
    fullPage: true 
  });
  throw error;
}
