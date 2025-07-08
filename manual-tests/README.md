# Manual Test Suite - Cypress Real World App

## Overview

This manual test suite provides comprehensive test coverage for the Cypress Real World App, a payment application demonstrating real-world usage patterns. The suite includes 27 detailed test scenarios covering all major application features.

## Project Structure

```
manual-tests/
├── test_scenarios.json          # Complete test scenarios in JSON format
├── selectors.json              # Element selectors for test automation
├── page_objects.py             # Page Object Model classes (Python/Selenium)
├── test_data.json              # Test data and validation rules
├── test_execution_report.md    # Test execution report template
└── README.md                   # This file
```

## Application Features Covered

### 🔐 Authentication (4 tests)
- **AUTH_001:** User Sign Up - Valid Registration
- **AUTH_002:** User Sign In - Valid Credentials  
- **AUTH_003:** User Sign In - Invalid Credentials
- **AUTH_004:** User Sign Out

### 💰 Transactions (9 tests)
- **TRANS_001:** Create Payment Transaction - Valid Data
- **TRANS_002:** Create Request Transaction - Valid Data
- **TRANS_003:** View Transaction Details
- **TRANS_004:** Like a Transaction
- **TRANS_005:** Comment on Transaction
- **TRANS_006:** Accept Transaction Request
- **TRANS_007:** Reject Transaction Request
- **TRANS_008:** Transaction Form Validation - Empty Fields
- **TRANS_009:** Transaction Form Validation - Invalid Amount

### 🏦 Bank Accounts (3 tests)
- **BANK_001:** Add Bank Account - Valid Data
- **BANK_002:** Delete Bank Account
- **BANK_003:** Bank Account Form Validation - Empty Fields

### 🧭 Navigation (2 tests)
- **NAV_001:** Navigate Between Transaction Feeds
- **NAV_002:** Mobile Navigation - Drawer Toggle

### 🔔 Notifications (1 test)
- **NOTIF_001:** View Notifications

### ⚙️ User Settings (2 tests)
- **SETTINGS_001:** Update User Settings - Valid Data
- **SETTINGS_002:** User Settings Form Validation - Invalid Email

### 🔍 Filters (2 tests)
- **FILTER_001:** Filter Transactions by Date Range
- **FILTER_002:** Filter Transactions by Amount Range

### 📄 Pagination (1 test)
- **PAGINATION_001:** Transaction Feed Pagination

### 📱 Responsive Design (1 test)
- **RESPONSIVE_001:** Mobile Responsive Design

### 🔒 Security (1 test)
- **SECURITY_001:** Unauthorized Access Protection

### 💳 Balance Management (1 test)
- **BALANCE_001:** User Balance Display and Updates

## Test Data

### Default User Credentials
- **Username:** Heath93
- **Password:** s3cret

### Test Environment
- **Application URL:** http://localhost:3000
- **API URL:** http://localhost:3001
- **Database:** JSON file (data/database.json)

## Test Execution Instructions

### Prerequisites
1. Ensure the application is running on localhost:3000
2. Backend API is running on localhost:3001
3. Database is seeded with test data
4. Browser is configured for testing

### Manual Test Execution Steps

1. **Setup**
   - Open browser and navigate to http://localhost:3000
   - Ensure clean state (clear cache/cookies if needed)
   - Verify application loads correctly

2. **Authentication Tests**
   - Start with sign-up tests using new user data
   - Test sign-in with valid and invalid credentials
   - Verify sign-out functionality

3. **Core Functionality Tests**
   - Test transaction creation (payments and requests)
   - Test transaction interactions (like, comment, accept/reject)
   - Test bank account management
   - Test user settings updates

4. **Navigation and UI Tests**
   - Test navigation between different feeds
   - Test mobile responsive design
   - Test filters and pagination

5. **Security and Edge Cases**
   - Test unauthorized access protection
   - Test form validation with invalid data
   - Test error handling scenarios

### Test Data Usage

The `test_data.json` file contains:
- **Valid user credentials** for successful login tests
- **Invalid data** for negative testing scenarios
- **Transaction data** for payment and request scenarios
- **Bank account data** for banking feature tests
- **Validation rules** for form testing

### Page Object Model

The `page_objects.py` file provides:
- **Reusable page classes** for each application page
- **Element locators** using data-test attributes
- **Action methods** for common interactions
- **Assertion helpers** for validation

## Test Reporting

### Execution Report
Use the `test_execution_report.md` template to document:
- Test execution results
- Bug reports and issues
- Environment details
- Screenshots and evidence

### Test Metrics
Track the following metrics:
- **Total test cases:** 27
- **Pass rate:** Target 100%
- **Execution time:** ~2-3 hours for full suite
- **Coverage:** All major user journeys

## Best Practices

### Test Execution
1. **Execute tests in order** - Authentication first, then core features
2. **Use fresh data** - Reset database state between test runs
3. **Document issues** - Screenshot failures and unexpected behavior
4. **Verify preconditions** - Ensure setup steps are completed

### Test Data Management
1. **Use provided test data** - Leverage the structured test data file
2. **Reset state** - Clear data between test runs when needed
3. **Isolate tests** - Each test should be independent

### Bug Reporting
1. **Include screenshots** - Visual evidence of issues
2. **Provide steps** - Clear reproduction steps
3. **Specify environment** - Browser, OS, and app version details
4. **Categorize severity** - Critical, High, Medium, Low

## Automation Integration

### Selector Strategy
- **Primary:** data-test attributes (e.g., `[data-test='signin-username']`)
- **Secondary:** CSS selectors for dynamic elements
- **Fallback:** XPath for complex scenarios

### Page Object Benefits
- **Maintainability:** Changes to UI require updates in single location
- **Reusability:** Common actions shared across tests
- **Readability:** Tests focus on business logic, not technical details

### Test Data Integration
- **Centralized data:** All test data in single JSON file
- **Environment-specific:** Easy to modify for different environments
- **Validation rules:** Built-in validation for form testing

## Known Limitations

1. **Test data dependency** - Tests require specific database state
2. **Network dependency** - Application must be running locally
3. **Browser compatibility** - Some features may behave differently across browsers
4. **Mobile testing** - Responsive tests require mobile viewport or device testing

## Maintenance

### Regular Updates
- **Update selectors** when UI changes
- **Refresh test data** when application data model changes
- **Review test scenarios** to ensure coverage of new features

### Test Review
- **Quarterly review** of test scenarios for relevance
- **Monthly review** of test data for accuracy
- **Continuous monitoring** of test execution results

## Support

For questions or issues with this test suite:
1. Check the existing test documentation
2. Review the application's Cypress test examples
3. Consult the Cypress Real World App documentation
4. Contact the QA team for guidance

---

**Version:** 1.0  
**Last Updated:** [Current Date]  
**Author:** Test Explorer Agent  
**Reviewed By:** QA Team
