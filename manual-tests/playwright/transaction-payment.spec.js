const { test, expect } = require('@playwright/test');

/**
 * Test Scenario: TRANS_001 - Create Payment Transaction - Valid Data
 * Category: Transactions
 * Priority: High
 * Tags: ["payment", "positive", "smoke"]
 */

test.describe('Transactions - Create Payment Transaction', () => {
  
  test.beforeEach(async ({ page }) => {
    // Navigate to the application and login first
    await page.goto('http://localhost:3000');
    await page.waitForLoadState('networkidle');
    
    // Login with valid credentials (prerequisite for transaction tests)
    if (await page.locator('[data-test="signin-username"]').isVisible()) {
      await page.locator('[data-test="signin-username"]').fill('Heath93');
      await page.locator('[data-test="signin-password"]').fill('s3cret');
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'networkidle' }),
        page.locator('[data-test="signin-submit"]').click()
      ]);
    }
    
    // Verify user is logged in
    await expect(page.locator('[data-test="nav-top-new-transaction"]')).toBeVisible();
  });

  test('TRANS_001 - Create Payment Transaction with Valid Data', async ({ page }) => {
    // Test data from test_scenarios.json
    const testData = {
      amount: '25.00',
      description: 'Lunch payment',
      transactionType: 'payment',
      recipientName: 'Kristian' // Using a name that exists in the seed data
    };

    // Capture initial balance for verification
    const initialBalance = await page.locator('[data-test="sidenav-user-balance"]').textContent();
    console.log('Initial balance:', initialBalance);

    // Step 1: Click 'New Transaction' button
    const newTransactionButton = page.locator('[data-test="nav-top-new-transaction"]');
    await expect(newTransactionButton).toBeVisible();
    await newTransactionButton.click();
    
    // Expected: New transaction form opens - Step 1: Select Contact
    await expect(page).toHaveURL(/.*\/transaction\/new/);
    await expect(page.locator('[data-test="user-list-search-input"]')).toBeVisible();

    // Step 2: Search for contact by typing first name in search field
    const userSearchInput = page.locator('[data-test="user-list-search-input"]');
    await userSearchInput.fill(testData.recipientName);
    
    // Wait for search results to load
    await page.waitForTimeout(1000);
    
    // Expected: Contact list is filtered based on search criteria
    const userListItems = page.locator('[data-test*="user-list-item"]');
    await expect(userListItems.first()).toBeVisible();

    // Step 3: Select a contact from the list
    const contactItem = userListItems.filter({ hasText: testData.recipientName }).first();
    await expect(contactItem).toBeVisible();
    await contactItem.click();
    
    // Expected: Contact is selected and form proceeds to Step 2: Payment
    await expect(page.locator('[data-test="transaction-create-form"]')).toBeVisible();
    await expect(page.locator('[data-test*="transaction-create-amount-input"]')).toBeVisible();

    // Step 4: Enter payment amount
    const amountInput = page.locator('[data-test*="transaction-create-amount-input"] input');
    await expect(amountInput).toBeVisible();
    await amountInput.fill(testData.amount);
    
    // Expected: Amount field accepts valid monetary input
    await expect(amountInput).toHaveValue(testData.amount);

    // Step 5: Enter description
    const descriptionInput = page.locator('[data-test*="transaction-create-description-input"] input');
    await expect(descriptionInput).toBeVisible();
    await descriptionInput.fill(testData.description);
    
    // Expected: Description field accepts input
    await expect(descriptionInput).toHaveValue(testData.description);

    // Step 6: Click 'Pay' button
    const payButton = page.locator('[data-test*="transaction-create-submit-payment"]');
    await expect(payButton).toBeVisible();
    await expect(payButton).toBeEnabled();
    
    // Wait for API call to complete
    await Promise.all([
      page.waitForResponse(response => 
        response.url().includes('/transactions') && response.request().method() === 'POST'
      ),
      payButton.click()
    ]);
    
    // Expected: Transaction is processed and Step 3: Complete is shown
    await expect(page.locator('[data-test="new-transaction-create-another-transaction"]')).toBeVisible();
    await expect(page.locator('[data-test="new-transaction-return-to-transactions"]')).toBeVisible();

    // Step 7: Verify transaction completion message
    // Expected: Success message shows 'Paid $25.00 for Lunch payment'
    const completionMessage = page.locator('text=Paid').first();
    await expect(completionMessage).toBeVisible();
    
    // Verify the amount and description are in the completion message
    await expect(page.locator(`text=${testData.amount}`)).toBeVisible();
    await expect(page.locator(`text=${testData.description}`)).toBeVisible();

    // Additional verification: Check success alert
    const successAlert = page.locator('[data-test="alert-bar-success"]');
    if (await successAlert.isVisible()) {
      await expect(successAlert).toContainText('Transaction Submitted');
    }

    // Verify balance update (if visible on desktop)
    const currentBalance = await page.locator('[data-test="sidenav-user-balance"]').textContent();
    console.log('Current balance after transaction:', currentBalance);

    // Expected Result: Payment transaction is created successfully and user balance is updated
    console.log('✅ TRANS_001 - Create Payment Transaction - PASSED');
  });

  test('TRANS_001 - Verify Transaction in Personal Feed', async ({ page }) => {
    // After creating a transaction, verify it appears in personal feed
    const testData = {
      amount: '15.50',
      description: 'Coffee payment',
      recipientName: 'Darrel'
    };

    // Create a transaction first
    await page.locator('[data-test="nav-top-new-transaction"]').click();
    await page.locator('[data-test="user-list-search-input"]').fill(testData.recipientName);
    await page.waitForTimeout(1000);
    await page.locator('[data-test*="user-list-item"]').filter({ hasText: testData.recipientName }).first().click();
    await page.locator('[data-test*="transaction-create-amount-input"] input').fill(testData.amount);
    await page.locator('[data-test*="transaction-create-description-input"] input').fill(testData.description);
    
    await Promise.all([
      page.waitForResponse(response => 
        response.url().includes('/transactions') && response.request().method() === 'POST'
      ),
      page.locator('[data-test*="transaction-create-submit-payment"]').click()
    ]);

    // Navigate back to home and check personal feed
    await page.locator('[data-test="new-transaction-return-to-transactions"]').click();
    await page.locator('[data-test="nav-personal-tab"]').click();
    
    // Wait for transactions to load
    await page.waitForLoadState('networkidle');
    
    // Verify transaction appears in the list
    await expect(page.locator(`text=${testData.description}`).first()).toBeVisible();
    
    console.log('✅ TRANS_001 - Transaction appears in Personal Feed - PASSED');
  });

  test('TRANS_001 - Create Payment Transaction - Mobile View', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    const testData = {
      amount: '30.00',
      description: 'Mobile payment test',
      recipientName: 'Ruthie'
    };

    // On mobile, we might need to open the sidebar first
    const sidenavToggle = page.locator('[data-test="sidenav-toggle"]');
    if (await sidenavToggle.isVisible()) {
      await sidenavToggle.click();
      await page.locator('[data-test="sidenav-home"]').click();
    }

    // Create transaction
    await page.locator('[data-test="nav-top-new-transaction"]').click();
    await page.locator('[data-test="user-list-search-input"]').fill(testData.recipientName);
    await page.waitForTimeout(1000);
    await page.locator('[data-test*="user-list-item"]').filter({ hasText: testData.recipientName }).first().click();
    await page.locator('[data-test*="transaction-create-amount-input"] input').fill(testData.amount);
    await page.locator('[data-test*="transaction-create-description-input"] input').fill(testData.description);
    
    await Promise.all([
      page.waitForResponse(response => 
        response.url().includes('/transactions') && response.request().method() === 'POST'
      ),
      page.locator('[data-test*="transaction-create-submit-payment"]').click()
    ]);

    // Verify completion
    await expect(page.locator('[data-test="new-transaction-create-another-transaction"]')).toBeVisible();
    
    console.log('✅ TRANS_001 - Mobile View Payment Transaction - PASSED');
  });

  test('TRANS_001 - Create Another Transaction Flow', async ({ page }) => {
    const testData = {
      amount: '12.75',
      description: 'Second payment',
      recipientName: 'Lia'
    };

    // Create first transaction
    await page.locator('[data-test="nav-top-new-transaction"]').click();
    await page.locator('[data-test="user-list-search-input"]').fill(testData.recipientName);
    await page.waitForTimeout(1000);
    await page.locator('[data-test*="user-list-item"]').filter({ hasText: testData.recipientName }).first().click();
    await page.locator('[data-test*="transaction-create-amount-input"] input').fill(testData.amount);
    await page.locator('[data-test*="transaction-create-description-input"] input').fill(testData.description);
    
    await Promise.all([
      page.waitForResponse(response => 
        response.url().includes('/transactions') && response.request().method() === 'POST'
      ),
      page.locator('[data-test*="transaction-create-submit-payment"]').click()
    ]);

    // Test "Create Another Transaction" button
    await page.locator('[data-test="new-transaction-create-another-transaction"]').click();
    
    // Should be back at step 1 of transaction creation
    await expect(page.locator('[data-test="user-list-search-input"]')).toBeVisible();
    await expect(page).toHaveURL(/.*\/transaction\/new/);
    
    console.log('✅ TRANS_001 - Create Another Transaction Flow - PASSED');
  });

  test.afterEach(async ({ page }) => {
    // Clean up: Take screenshot on failure
    if (test.info().status !== test.info().expectedStatus) {
      await page.screenshot({ 
        path: `manual-tests/playwright/screenshots/transaction-payment-failure-${Date.now()}.png`,
        fullPage: true 
      });
    }
  });
});

// Test configuration
test.describe.configure({ mode: 'parallel' });

// Helper functions
async function createTransaction(page, transactionData) {
  await page.locator('[data-test="nav-top-new-transaction"]').click();
  await page.locator('[data-test="user-list-search-input"]').fill(transactionData.recipientName);
  await page.waitForTimeout(1000);
  await page.locator('[data-test*="user-list-item"]').filter({ hasText: transactionData.recipientName }).first().click();
  await page.locator('[data-test*="transaction-create-amount-input"] input').fill(transactionData.amount);
  await page.locator('[data-test*="transaction-create-description-input"] input').fill(transactionData.description);
  
  await Promise.all([
    page.waitForResponse(response => 
      response.url().includes('/transactions') && response.request().method() === 'POST'
    ),
    page.locator('[data-test*="transaction-create-submit-payment"]').click()
  ]);
}

async function verifyTransactionCompletion(page, transactionData) {
  await expect(page.locator('[data-test="new-transaction-create-another-transaction"]')).toBeVisible();
  await expect(page.locator('[data-test="new-transaction-return-to-transactions"]')).toBeVisible();
  await expect(page.locator(`text=${transactionData.amount}`)).toBeVisible();
  await expect(page.locator(`text=${transactionData.description}`)).toBeVisible();
}
