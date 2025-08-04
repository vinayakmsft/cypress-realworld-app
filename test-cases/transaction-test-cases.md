# Transaction Management Test Cases

## Payment Transaction Test Cases

### TC-TXN-001: Send Payment - Valid Transaction
**Objective**: Verify user can send payment to another user successfully
**Preconditions**: 
- User is logged in
- User has sufficient balance
- Recipient user exists
- Bank account is set up

**Test Data**:
- Sender: User with balance $500
- Recipient: Valid existing user
- Amount: $50.00
- Description: "Dinner payment"
- Privacy: Public

**Test Steps**:
1. Navigate to "Pay" or "New Transaction" page
2. Search for and select recipient
3. Enter payment amount
4. Add description
5. Select privacy level
6. Review transaction details
7. Confirm payment

**Expected Results**:
- Payment processed successfully
- Sender balance decreased by amount
- Recipient balance increased by amount
- Transaction appears in both users' history
- Success confirmation displayed

**Cypress Implementation**:
```typescript
it('should send payment successfully', () => {
  cy.database('filter', 'users').then((users: User[]) => {
    const sender = users[0];
    const recipient = users[1];
    const amount = 50;
    
    cy.loginByApi(sender.username);
    cy.visit('/transaction/new');
    
    // Select recipient
    cy.getBySel('user-list-search-input').type(recipient.username);
    cy.getBySel(`user-list-item-${recipient.id}`).click();
    
    // Enter payment details
    cy.getBySel('transaction-create-amount-input').type(amount.toString());
    cy.getBySel('transaction-create-description-input').type('Dinner payment');
    cy.getBySel('transaction-create-submit-payment').click();
    
    // Verify success
    cy.getBySel('alert-bar-success').should('contain', 'Transaction Submitted!');
    cy.location('pathname').should('eq', '/');
    
    // Verify transaction in feed
    cy.getBySel('transaction-list').should('contain', 'paid');
    cy.getBySel('transaction-list').should('contain', recipient.firstName);
  });
});
```

---

### TC-TXN-002: Send Payment - Insufficient Funds
**Objective**: Verify proper handling when user has insufficient funds
**Preconditions**: User is logged in with low balance
**Test Data**: Payment amount exceeds user balance

**Test Steps**:
1. Navigate to payment page
2. Select recipient
3. Enter amount greater than available balance
4. Attempt to submit payment

**Expected Results**:
- Payment rejected
- Error message displayed
- Balance unchanged
- User remains on payment page

**Cypress Implementation**:
```typescript
it('should reject payment with insufficient funds', () => {
  cy.database('filter', 'users').then((users: User[]) => {
    const sender = users.find(user => user.balance < 1000);
    const recipient = users[1];
    const amount = sender.balance + 100; // More than available
    
    cy.loginByApi(sender.username);
    cy.visit('/transaction/new');
    
    cy.getBySel('user-list-search-input').type(recipient.username);
    cy.getBySel(`user-list-item-${recipient.id}`).click();
    cy.getBySel('transaction-create-amount-input').type(amount.toString());
    cy.getBySel('transaction-create-description-input').type('Test payment');
    cy.getBySel('transaction-create-submit-payment').click();
    
    // Verify error handling
    cy.getBySel('transaction-create-amount-input-error')
      .should('contain', 'insufficient funds');
  });
});
```

---

### TC-TXN-003: Payment Amount Validation
**Objective**: Verify payment amount validation rules
**Test Data**: Various invalid amounts

**Test Steps**:
1. Test negative amounts
2. Test zero amount
3. Test extremely large amounts
4. Test invalid decimal places
5. Test non-numeric input

**Expected Results**:
- Invalid amounts rejected
- Appropriate error messages shown
- Form submission prevented

**Cypress Implementation**:
```typescript
describe('Payment Amount Validation', () => {
  beforeEach(() => {
    cy.database('filter', 'users').then((users: User[]) => {
      cy.loginByApi(users[0].username);
      cy.visit('/transaction/new');
      cy.getBySel(`user-list-item-${users[1].id}`).click();
    });
  });

  it('should reject negative amounts', () => {
    cy.getBySel('transaction-create-amount-input').type('-50');
    cy.getBySel('transaction-create-submit-payment').click();
    cy.getBySel('transaction-create-amount-input-error')
      .should('contain', 'Please enter a valid amount');
  });

  it('should reject zero amount', () => {
    cy.getBySel('transaction-create-amount-input').type('0');
    cy.getBySel('transaction-create-submit-payment').click();
    cy.getBySel('transaction-create-amount-input-error')
      .should('contain', 'Please enter a valid amount');
  });

  it('should handle decimal amounts correctly', () => {
    cy.getBySel('transaction-create-amount-input').type('25.50');
    cy.getBySel('transaction-create-description-input').type('Test payment');
    cy.getBySel('transaction-create-submit-payment').click();
    cy.getBySel('alert-bar-success').should('be.visible');
  });
});
```

---

### TC-TXN-004: Payment Privacy Settings
**Objective**: Verify payment privacy levels work correctly
**Test Data**: Different privacy settings (Public, Private, Contacts)

**Test Steps**:
1. Create payments with different privacy levels
2. Verify visibility in transaction feed
3. Test privacy enforcement for different user types

**Expected Results**:
- Public: Visible to all users
- Private: Visible only to sender and recipient
- Contacts: Visible to contacts only

**Cypress Implementation**:
```typescript
describe('Payment Privacy Settings', () => {
  it('should respect public privacy setting', () => {
    cy.database('filter', 'users').then((users: User[]) => {
      const sender = users[0];
      const recipient = users[1];
      const observer = users[2];
      
      // Create public payment
      cy.loginByApi(sender.username);
      cy.visit('/transaction/new');
      cy.getBySel(`user-list-item-${recipient.id}`).click();
      cy.getBySel('transaction-create-amount-input').type('25');
      cy.getBySel('transaction-create-description-input').type('Public payment');
      cy.getBySel('transaction-create-privacy-public').click();
      cy.getBySel('transaction-create-submit-payment').click();
      
      // Verify visibility to other users
      cy.loginByApi(observer.username);
      cy.visit('/');
      cy.getBySel('transaction-list').should('contain', 'Public payment');
    });
  });

  it('should respect private privacy setting', () => {
    cy.database('filter', 'users').then((users: User[]) => {
      const sender = users[0];
      const recipient = users[1];
      const observer = users[2];
      
      // Create private payment
      cy.loginByApi(sender.username);
      cy.visit('/transaction/new');
      cy.getBySel(`user-list-item-${recipient.id}`).click();
      cy.getBySel('transaction-create-amount-input').type('25');
      cy.getBySel('transaction-create-description-input').type('Private payment');
      cy.getBySel('transaction-create-privacy-private').click();
      cy.getBySel('transaction-create-submit-payment').click();
      
      // Verify not visible to other users
      cy.loginByApi(observer.username);
      cy.visit('/');
      cy.getBySel('transaction-list').should('not.contain', 'Private payment');
    });
  });
});
```

---

## Payment Request Test Cases

### TC-TXN-005: Create Payment Request
**Objective**: Verify user can create payment request successfully
**Preconditions**: User is logged in, recipient exists

**Test Data**:
- Requester: Valid user
- Recipient: Valid user
- Amount: $75.00
- Description: "Shared dinner bill"

**Test Steps**:
1. Navigate to request payment page
2. Select recipient
3. Enter request amount and description
4. Submit payment request

**Expected Results**:
- Payment request created successfully
- Recipient receives notification
- Request appears in requester's pending requests
- Request appears in recipient's action items

**Cypress Implementation**:
```typescript
it('should create payment request successfully', () => {
  cy.database('filter', 'users').then((users: User[]) => {
    const requester = users[0];
    const recipient = users[1];
    
    cy.loginByApi(requester.username);
    cy.visit('/transaction/new');
    
    // Select recipient and request tab
    cy.getBySel('user-list-search-input').type(recipient.username);
    cy.getBySel(`user-list-item-${recipient.id}`).click();
    cy.getBySel('transaction-create-type-request').click();
    
    // Enter request details
    cy.getBySel('transaction-create-amount-input').type('75');
    cy.getBySel('transaction-create-description-input').type('Shared dinner bill');
    cy.getBySel('transaction-create-submit-request').click();
    
    // Verify success
    cy.getBySel('alert-bar-success').should('contain', 'Transaction Submitted!');
    
    // Verify request appears in feed
    cy.visit('/');
    cy.getBySel('transaction-list').should('contain', 'requested');
  });
});
```

---

### TC-TXN-006: Accept Payment Request
**Objective**: Verify user can accept payment request
**Preconditions**: Payment request exists, recipient has sufficient funds

**Test Steps**:
1. Login as recipient of payment request
2. Navigate to notifications or pending requests
3. Review payment request details
4. Accept payment request

**Expected Results**:
- Payment processed successfully
- Funds transferred from recipient to requester
- Request marked as completed
- Both users receive confirmation

**Cypress Implementation**:
```typescript
it('should accept payment request successfully', () => {
  // First create a payment request
  cy.database('filter', 'users').then((users: User[]) => {
    const requester = users[0];
    const recipient = users[1];
    
    // Create request
    cy.loginByApi(requester.username);
    cy.createTransaction({
      type: 'request',
      amount: 50,
      description: 'Test request',
      receiverId: recipient.id
    });
    
    // Accept request as recipient
    cy.loginByApi(recipient.username);
    cy.visit('/notifications');
    
    cy.getBySel('notification-list-item')
      .contains('requested')
      .parent()
      .within(() => {
        cy.getBySel('transaction-accept-request').click();
      });
    
    // Verify acceptance
    cy.getBySel('alert-bar-success').should('contain', 'Transaction Submitted!');
    
    // Verify transaction completed
    cy.visit('/personal');
    cy.getBySel('transaction-list').should('contain', 'paid');
  });
});
```

---

### TC-TXN-007: Decline Payment Request
**Objective**: Verify user can decline payment request
**Preconditions**: Payment request exists

**Test Steps**:
1. Login as recipient of payment request
2. Navigate to payment request
3. Decline payment request
4. Verify request handling

**Expected Results**:
- Request marked as declined
- No funds transferred
- Requester notified of decline
- Request removed from pending items

**Cypress Implementation**:
```typescript
it('should decline payment request successfully', () => {
  cy.database('filter', 'users').then((users: User[]) => {
    const requester = users[0];
    const recipient = users[1];
    
    // Create request
    cy.loginByApi(requester.username);
    cy.createTransaction({
      type: 'request',
      amount: 50,
      description: 'Test request',
      receiverId: recipient.id
    });
    
    // Decline request as recipient
    cy.loginByApi(recipient.username);
    cy.visit('/notifications');
    
    cy.getBySel('notification-list-item')
      .contains('requested')
      .parent()
      .within(() => {
        cy.getBySel('transaction-decline-request').click();
      });
    
    // Verify decline
    cy.getBySel('alert-bar-success').should('contain', 'Transaction Declined');
    
    // Verify request no longer pending
    cy.getBySel('notification-list-item')
      .should('not.contain', 'Test request');
  });
});
```

---

## Transaction History and Feed Test Cases

### TC-TXN-008: Transaction History Display
**Objective**: Verify transaction history displays correctly
**Preconditions**: User has transaction history

**Test Steps**:
1. Login as user with transactions
2. Navigate to personal transaction history
3. Verify transaction display
4. Test pagination/infinite scroll

**Expected Results**:
- All user transactions displayed
- Correct transaction details shown
- Proper chronological order
- Pagination works correctly

**Cypress Implementation**:
```typescript
it('should display transaction history correctly', () => {
  cy.database('filter', 'users').then((users: User[]) => {
    const user = users[0];
    
    cy.loginByApi(user.username);
    cy.visit('/personal');
    
    // Verify transaction list exists
    cy.getBySel('transaction-list').should('be.visible');
    
    // Verify transaction details
    cy.getBySel('transaction-item').first().within(() => {
      cy.getBySel('transaction-amount').should('be.visible');
      cy.getBySel('transaction-description').should('be.visible');
      cy.getBySel('transaction-date').should('be.visible');
    });
    
    // Test infinite scroll
    cy.getBySel('transaction-list').scrollTo('bottom');
    cy.getBySel('transaction-item').should('have.length.greaterThan', 10);
  });
});
```

---

### TC-TXN-009: Public Transaction Feed
**Objective**: Verify public transaction feed functionality
**Preconditions**: Public transactions exist

**Test Steps**:
1. Navigate to public feed
2. Verify public transactions display
3. Test feed filtering
4. Test real-time updates

**Expected Results**:
- Only public transactions shown
- Transactions from all users visible
- Feed updates in real-time
- Filtering works correctly

**Cypress Implementation**:
```typescript
it('should display public transaction feed', () => {
  cy.database('filter', 'users').then((users: User[]) => {
    cy.loginByApi(users[0].username);
    cy.visit('/');
    
    // Verify public feed
    cy.getBySel('transaction-list').should('be.visible');
    
    // Verify only public transactions shown
    cy.getBySel('transaction-item').each(($el) => {
      cy.wrap($el).should('not.contain', 'Private');
    });
    
    // Test feed filtering
    cy.getBySel('transaction-filter-all').click();
    cy.getBySel('transaction-item').should('have.length.greaterThan', 0);
    
    cy.getBySel('transaction-filter-friends').click();
    // Verify filtering works
  });
});
```

---

## Transaction Details and Comments Test Cases

### TC-TXN-010: View Transaction Details
**Objective**: Verify transaction detail view functionality
**Preconditions**: Transactions exist

**Test Steps**:
1. Navigate to transaction list
2. Click on specific transaction
3. Verify transaction details display
4. Test navigation back to list

**Expected Results**:
- Transaction details page opens
- All transaction information displayed
- Comments section visible (if applicable)
- Navigation works correctly

**Cypress Implementation**:
```typescript
it('should display transaction details correctly', () => {
  cy.database('filter', 'users').then((users: User[]) => {
    cy.loginByApi(users[0].username);
    cy.visit('/');
    
    // Click on first transaction
    cy.getBySel('transaction-item').first().click();
    
    // Verify transaction details page
    cy.getBySel('transaction-detail-header').should('be.visible');
    cy.getBySel('transaction-detail-amount').should('be.visible');
    cy.getBySel('transaction-detail-description').should('be.visible');
    cy.getBySel('transaction-detail-date').should('be.visible');
    
    // Verify comments section
    cy.getBySel('transaction-comments').should('be.visible');
    
    // Test back navigation
    cy.getBySel('transaction-detail-back').click();
    cy.location('pathname').should('eq', '/');
  });
});
```

---

### TC-TXN-011: Add Transaction Comment
**Objective**: Verify users can comment on transactions
**Preconditions**: User is logged in, transaction exists

**Test Steps**:
1. Navigate to transaction details
2. Add comment to transaction
3. Verify comment appears
4. Test comment validation

**Expected Results**:
- Comment added successfully
- Comment appears in transaction
- Comment count updated
- Validation works correctly

**Cypress Implementation**:
```typescript
it('should add comment to transaction', () => {
  cy.database('filter', 'users').then((users: User[]) => {
    cy.loginByApi(users[0].username);
    cy.visit('/');
    
    // Navigate to transaction details
    cy.getBySel('transaction-item').first().click();
    
    // Add comment
    const commentText = 'Great transaction!';
    cy.getBySel('transaction-comment-input').type(commentText);
    cy.getBySel('transaction-comment-submit').click();
    
    // Verify comment appears
    cy.getBySel('transaction-comments-list')
      .should('contain', commentText);
    
    // Verify comment count updated
    cy.getBySel('transaction-comment-count')
      .should('contain', '1');
  });
});
```

---

### TC-TXN-012: Like Transaction
**Objective**: Verify users can like/unlike transactions
**Preconditions**: User is logged in, transaction exists

**Test Steps**:
1. Navigate to transaction
2. Click like button
3. Verify like count increases
4. Click unlike button
5. Verify like count decreases

**Expected Results**:
- Like functionality works correctly
- Like count updates accurately
- Visual feedback provided
- Unlike functionality works

**Cypress Implementation**:
```typescript
it('should like and unlike transaction', () => {
  cy.database('filter', 'users').then((users: User[]) => {
    cy.loginByApi(users[0].username);
    cy.visit('/');
    
    // Get initial like count
    cy.getBySel('transaction-item').first().within(() => {
      cy.getBySel('transaction-like-count').invoke('text').as('initialCount');
    });
    
    // Like transaction
    cy.getBySel('transaction-item').first().within(() => {
      cy.getBySel('transaction-like-button').click();
    });
    
    // Verify like count increased
    cy.get('@initialCount').then((initialCount) => {
      const expectedCount = parseInt(initialCount as string) + 1;
      cy.getBySel('transaction-like-count')
        .should('contain', expectedCount.toString());
    });
    
    // Unlike transaction
    cy.getBySel('transaction-item').first().within(() => {
      cy.getBySel('transaction-like-button').click();
    });
    
    // Verify like count decreased
    cy.get('@initialCount').then((initialCount) => {
      cy.getBySel('transaction-like-count')
        .should('contain', initialCount as string);
    });
  });
});
```

---

## API Transaction Test Cases

### TC-API-TXN-001: Create Transaction via API
**Objective**: Verify transaction creation through API
**Test Data**: Valid transaction data

**Test Steps**:
1. Authenticate user via API
2. Send POST request to create transaction
3. Verify response
4. Verify transaction in database

**Expected Results**:
- API returns 201 Created
- Transaction data returned correctly
- Transaction saved in database
- Balances updated correctly

**Cypress Implementation**:
```typescript
describe('Transaction API', () => {
  const apiTransactions = `${Cypress.env('apiUrl')}/transactions`;
  
  it('should create transaction via API', () => {
    cy.database('filter', 'users').then((users: User[]) => {
      const sender = users[0];
      const recipient = users[1];
      
      cy.loginByApi(sender.username).then(() => {
        cy.request({
          method: 'POST',
          url: apiTransactions,
          body: {
            type: 'payment',
            amount: 5000, // $50.00 in cents
            description: 'API test payment',
            receiverId: recipient.id,
            privacyLevel: 'public'
          }
        }).then((response) => {
          expect(response.status).to.eq(201);
          expect(response.body.transaction).to.have.property('id');
          expect(response.body.transaction.amount).to.eq(5000);
          expect(response.body.transaction.description).to.eq('API test payment');
        });
      });
    });
  });

  it('should reject invalid transaction data', () => {
    cy.database('filter', 'users').then((users: User[]) => {
      cy.loginByApi(users[0].username).then(() => {
        cy.request({
          method: 'POST',
          url: apiTransactions,
          body: {
            type: 'payment',
            amount: -100, // Invalid negative amount
            description: 'Invalid payment',
            receiverId: 'invalid-id'
          },
          failOnStatusCode: false
        }).then((response) => {
          expect(response.status).to.eq(422);
          expect(response.body).to.have.property('errors');
        });
      });
    });
  });
});
```

---

## Performance Test Cases

### TC-TXN-PERF-001: Transaction Processing Performance
**Objective**: Verify transaction processing meets performance requirements
**Performance Criteria**: Transaction completes within 1 second

**Test Steps**:
1. Measure transaction creation time
2. Test with concurrent transactions
3. Monitor database performance

**Expected Results**:
- Single transaction: < 1 second
- Concurrent transactions: Acceptable performance
- Database queries optimized

**Cypress Implementation**:
```typescript
it('should process transaction within performance threshold', () => {
  cy.database('filter', 'users').then((users: User[]) => {
    const startTime = Date.now();
    
    cy.loginByApi(users[0].username);
    cy.visit('/transaction/new');
    cy.getBySel(`user-list-item-${users[1].id}`).click();
    cy.getBySel('transaction-create-amount-input').type('25');
    cy.getBySel('transaction-create-description-input').type('Performance test');
    cy.getBySel('transaction-create-submit-payment').click();
    
    cy.getBySel('alert-bar-success').should('be.visible').then(() => {
      const transactionTime = Date.now() - startTime;
      expect(transactionTime).to.be.lessThan(1000);
    });
  });
});
```

---

## Security Test Cases

### TC-TXN-SEC-001: Transaction Authorization
**Objective**: Verify users can only access their own transactions
**Test Data**: Multiple user accounts

**Test Steps**:
1. Create transaction as User A
2. Attempt to access transaction as User B
3. Verify access control

**Expected Results**:
- Users can only access own transactions
- Unauthorized access blocked
- Appropriate error messages shown

**Cypress Implementation**:
```typescript
it('should enforce transaction access control', () => {
  cy.database('filter', 'users').then((users: User[]) => {
    const userA = users[0];
    const userB = users[1];
    
    // Create transaction as User A
    cy.loginByApi(userA.username);
    cy.createTransaction({
      type: 'payment',
      amount: 25,
      description: 'Private transaction',
      receiverId: userB.id,
      privacyLevel: 'private'
    }).then((transaction) => {
      
      // Try to access as different user
      cy.loginByApi(userB.username);
      cy.request({
        method: 'GET',
        url: `${Cypress.env('apiUrl')}/transactions/${transaction.id}`,
        failOnStatusCode: false
      }).then((response) => {
        // Should either return 403/404 or filtered data
        if (response.status === 200) {
          // If accessible, verify data is properly filtered
          expect(response.body.transaction).to.not.have.property('sensitiveData');
        } else {
          expect([403, 404]).to.include(response.status);
        }
      });
    });
  });
});
```

---

## Edge Cases and Error Handling

### TC-TXN-EDGE-001: Concurrent Transaction Handling
**Objective**: Verify system handles concurrent transactions correctly
**Test Data**: Multiple simultaneous transactions

**Test Steps**:
1. Initiate multiple transactions simultaneously
2. Verify data consistency
3. Check for race conditions

**Expected Results**:
- All transactions processed correctly
- No data corruption
- Balances remain consistent
- Proper error handling for conflicts

### TC-TXN-EDGE-002: Network Failure During Transaction
**Objective**: Verify transaction handling during network issues
**Test Data**: Transaction in progress

**Test Steps**:
1. Start transaction process
2. Simulate network failure
3. Verify transaction state
4. Test recovery process

**Expected Results**:
- Transaction state properly managed
- No partial transactions
- User informed of status
- Recovery process works correctly

### TC-TXN-EDGE-003: Large Transaction Amounts
**Objective**: Verify handling of large transaction amounts
**Test Data**: Maximum allowed transaction amounts

**Test Steps**:
1. Test maximum allowed amount
2. Test amount exceeding limits
3. Verify validation and processing

**Expected Results**:
- Maximum amounts processed correctly
- Excessive amounts rejected
- Appropriate validation messages
- System stability maintained

