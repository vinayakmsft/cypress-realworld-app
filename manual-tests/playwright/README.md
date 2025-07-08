# Playwright Test Scripts for Cypress Real World App

This directory contains Playwright automation scripts based on the manual test scenarios defined in `test_scenarios.json`.

## 📁 Structure

```
playwright/
├── auth-signin.spec.js           # AUTH_002 - User Sign In tests
├── transaction-payment.spec.js   # TRANS_001 - Create Payment Transaction tests
├── playwright.config.js          # Playwright configuration
├── global-setup.js              # Global setup before all tests
├── global-teardown.js           # Global teardown after all tests
├── package.json                 # Playwright dependencies and scripts
├── screenshots/                 # Test failure screenshots
├── reports/                     # Test reports (HTML, JSON, XML)
└── test-results/               # Test artifacts and videos
```

## 🎯 Test Coverage

### AUTH_002 - User Sign In Tests
- **Main Test:** Valid credentials login flow
- **Mobile Test:** Login on mobile viewport
- **Remember Me:** Checkbox functionality verification

### TRANS_001 - Create Payment Transaction Tests
- **Main Test:** Complete payment transaction flow
- **Verification Test:** Transaction appears in personal feed
- **Mobile Test:** Payment transaction on mobile
- **Flow Test:** "Create Another Transaction" workflow

## 🚀 Quick Start

### Prerequisites
1. Ensure the Cypress Real World App is running:
   ```bash
   cd cypress-realworld-app
   npm run dev
   ```

2. Application should be accessible at `http://localhost:3000`

### Installation
```bash
cd manual-tests/playwright
npm install
npx playwright install
```

### Running Tests

#### Run All Tests
```bash
npm test
```

#### Run Specific Test Files
```bash
npm run test:auth         # Run authentication tests
npm run test:transactions # Run transaction tests
```

#### Run in Different Browsers
```bash
npm run test:chrome   # Chrome only
npm run test:firefox  # Firefox only
npm run test:safari   # Safari only
npm run test:mobile   # Mobile Chrome
```

#### Debug Mode
```bash
npm run test:debug    # Step-by-step debugging
npm run test:headed   # Run with browser UI visible
npm run test:ui       # Interactive UI mode
```

#### View Test Reports
```bash
npm run report        # Open HTML report
```

## 🔧 Configuration

### Playwright Config (`playwright.config.js`)
- **Base URL:** `http://localhost:3000`
- **Browsers:** Chrome, Firefox, Safari, Edge
- **Mobile:** iPhone 12, Pixel 5 viewports
- **Retries:** 2 on CI, 0 locally
- **Reporters:** HTML, JSON, JUnit XML, List
- **Screenshots:** On failure only
- **Videos:** Retained on failure

### Test Data Integration
Tests use the same test data from `../test_data.json`:
- **Valid User:** `Heath93` / `s3cret`
- **Test Recipients:** Names from seeded database
- **Transaction Amounts:** Various test amounts
- **Descriptions:** Descriptive test scenarios

## 📊 Test Reports

### HTML Report
- **Location:** `reports/html/index.html`
- **Features:** Interactive test results, screenshots, videos
- **Access:** `npm run report`

### JSON Report
- **Location:** `reports/results.json`
- **Usage:** CI/CD integration, custom reporting

### JUnit XML
- **Location:** `reports/results.xml`
- **Usage:** Jenkins, Azure DevOps integration

## 🎨 Best Practices Implemented

### 1. **Page Object Pattern**
```javascript
// Using data-test selectors for reliability
const usernameField = page.locator('[data-test="signin-username"]');
await usernameField.fill(testData.username);
```

### 2. **Explicit Waits**
```javascript
// Wait for API responses
await Promise.all([
  page.waitForResponse(response => 
    response.url().includes('/transactions') && response.request().method() === 'POST'
  ),
  payButton.click()
]);
```

### 3. **Assertions with Context**
```javascript
// Clear expectations with descriptive messages
await expect(page.locator('[data-test="transaction-list"]')).toBeVisible();
```

### 4. **Mobile-First Testing**
```javascript
// Responsive design testing
await page.setViewportSize({ width: 375, height: 667 });
```

### 5. **Error Handling**
```javascript
// Screenshot on failure
if (test.info().status !== test.info().expectedStatus) {
  await page.screenshot({ 
    path: `screenshots/failure-${Date.now()}.png`,
    fullPage: true 
  });
}
```

## 🔍 Debugging Tests

### 1. **Visual Debugging**
```bash
npm run test:headed    # See browser actions
npm run test:debug     # Step through test
```

### 2. **Console Logging**
Tests include detailed console output:
- Initial setup status
- Test step completion
- Balance verification
- Success confirmations

### 3. **Screenshots**
- Automatic on test failure
- Stored in `screenshots/` directory
- Timestamped filenames

### 4. **Videos**
- Recorded on failure
- Stored in `test-results/` directory
- Full test execution capture

## 🚨 Troubleshooting

### Common Issues

1. **Application Not Running**
   ```
   Error: connect ECONNREFUSED ::1:3000
   ```
   **Solution:** Start the app with `npm run dev`

2. **Selector Not Found**
   ```
   Error: Locator '[data-test="signin-username"]' not found
   ```
   **Solution:** Check if app loaded correctly, verify selectors

3. **Test Timeout**
   ```
   Error: Test timeout of 60000ms exceeded
   ```
   **Solution:** Check network, increase timeout in config

4. **Database State**
   ```
   Error: User not found in search results
   ```
   **Solution:** Ensure database is seeded with test data

### Environment Verification
```bash
# Check if app is running
curl http://localhost:3000

# Verify test environment
npx playwright --version
node --version
npm --version
```

## 📝 Test Mapping

| Manual Test ID | Playwright Test File | Test Function |
|----------------|---------------------|---------------|
| AUTH_002 | `auth-signin.spec.js` | User Sign In with Valid Credentials |
| TRANS_001 | `transaction-payment.spec.js` | Create Payment Transaction with Valid Data |

## 🔮 Future Enhancements

### Planned Test Additions
- **AUTH_001:** User Sign Up flow
- **TRANS_002:** Create Request Transaction
- **BANK_001:** Bank Account Management
- **NOTIF_001:** Notifications functionality

### Advanced Features
- **API Testing:** Direct backend validation
- **Performance Testing:** Load time measurements
- **Accessibility Testing:** A11y compliance checks
- **Visual Testing:** Screenshot comparisons

## 📞 Support

For issues with these Playwright tests:
1. Check the test output and screenshots
2. Verify application is running correctly
3. Review the HTML test report
4. Check the troubleshooting section above
5. Refer to [Playwright Documentation](https://playwright.dev/)

---

**Generated by:** Test Explorer Agent  
**Based on:** Manual test scenarios from `test_scenarios.json`  
**Last Updated:** [Current Date]
