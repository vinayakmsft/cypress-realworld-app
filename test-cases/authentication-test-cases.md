# Authentication Test Cases

## Local Authentication Test Cases

### TC-AUTH-001: User Registration - Valid Data

**Objective**: Verify user can register with valid information
**Preconditions**: Application is running, database is seeded
**Test Data**:

- Username: testuser123
- Password: ValidPass123!
- First Name: John
- Last Name: Doe
- Email: john.doe@example.com
- Phone: 555-123-4567

**Test Steps**:

1. Navigate to registration page
2. Fill in all required fields with valid data
3. Click "Sign Up" button
4. Verify successful registration message
5. Verify redirect to onboarding/dashboard

**Expected Results**:

- User account created successfully
- User redirected to appropriate page
- Success message displayed
- User can login with created credentials

**Cypress Implementation**:

```typescript
it("should register user with valid data", () => {
  cy.visit("/signup");
  cy.getBySel("signup-first-name").type("John");
  cy.getBySel("signup-last-name").type("Doe");
  cy.getBySel("signup-username").type("testuser123");
  cy.getBySel("signup-password").type("ValidPass123!");
  cy.getBySel("signup-confirmPassword").type("ValidPass123!");
  cy.getBySel("signup-submit").click();

  cy.url().should("not.contain", "/signup");
  cy.getBySel("user-onboarding").should("be.visible");
});
```

---

### TC-AUTH-002: User Registration - Invalid Data

**Objective**: Verify proper validation for invalid registration data
**Test Data**: Various invalid inputs

**Test Steps**:

1. Navigate to registration page
2. Test each validation scenario:
   - Empty required fields
   - Invalid email format
   - Weak password
   - Password mismatch
   - Duplicate username
3. Verify appropriate error messages

**Expected Results**:

- Appropriate error messages displayed
- Form submission prevented
- User remains on registration page

**Cypress Implementation**:

```typescript
describe("Registration Validation", () => {
  beforeEach(() => {
    cy.visit("/signup");
  });

  it("should show error for empty required fields", () => {
    cy.getBySel("signup-submit").click();
    cy.getBySel("signup-first-name-error").should("contain", "First Name is required");
    cy.getBySel("signup-last-name-error").should("contain", "Last Name is required");
  });

  it("should validate password strength", () => {
    cy.getBySel("signup-password").type("weak");
    cy.getBySel("signup-password-error").should(
      "contain",
      "Password must be at least 4 characters"
    );
  });

  it("should validate password confirmation", () => {
    cy.getBySel("signup-password").type("ValidPass123!");
    cy.getBySel("signup-confirmPassword").type("DifferentPass123!");
    cy.getBySel("signup-confirmPassword-error").should("contain", "Password does not match");
  });
});
```

---

### TC-AUTH-003: User Login - Valid Credentials

**Objective**: Verify user can login with valid credentials
**Preconditions**: User account exists in database
**Test Data**: Existing user credentials

**Test Steps**:

1. Navigate to login page
2. Enter valid username and password
3. Click "Sign In" button
4. Verify successful login

**Expected Results**:

- User successfully logged in
- Redirected to dashboard/home page
- User session established
- Navigation shows logged-in state

**Cypress Implementation**:

```typescript
it("should login with valid credentials", () => {
  cy.database("find", "users").then((user: User) => {
    cy.visit("/signin");
    cy.getBySel("signin-username").type(user.username);
    cy.getBySel("signin-password").type("s3cret");
    cy.getBySel("signin-submit").click();

    cy.location("pathname").should("eq", "/");
    cy.getBySel("sidenav-user-full-name").should("contain", user.firstName);
  });
});
```

---

### TC-AUTH-004: User Login - Invalid Credentials

**Objective**: Verify proper handling of invalid login attempts
**Test Data**: Invalid credentials

**Test Steps**:

1. Navigate to login page
2. Enter invalid username/password combinations
3. Verify error handling

**Expected Results**:

- Login rejected
- Appropriate error message displayed
- User remains on login page
- No session established

**Cypress Implementation**:

```typescript
describe("Login Validation", () => {
  beforeEach(() => {
    cy.visit("/signin");
  });

  it("should reject invalid username", () => {
    cy.getBySel("signin-username").type("nonexistentuser");
    cy.getBySel("signin-password").type("anypassword");
    cy.getBySel("signin-submit").click();

    cy.getBySel("signin-error").should("contain", "Username or password is invalid");
    cy.location("pathname").should("eq", "/signin");
  });

  it("should reject invalid password", () => {
    cy.database("find", "users").then((user: User) => {
      cy.getBySel("signin-username").type(user.username);
      cy.getBySel("signin-password").type("wrongpassword");
      cy.getBySel("signin-submit").click();

      cy.getBySel("signin-error").should("contain", "Username or password is invalid");
    });
  });
});
```

---

### TC-AUTH-005: Session Management - Remember Me

**Objective**: Verify "Remember Me" functionality works correctly
**Preconditions**: User account exists

**Test Steps**:

1. Login with "Remember Me" checked
2. Verify session cookie expiration
3. Close browser and reopen
4. Verify user still logged in

**Expected Results**:

- Session persists across browser sessions
- Cookie has appropriate expiration
- User remains logged in

**Cypress Implementation**:

```typescript
it("should remember user for 30 days", () => {
  cy.database("find", "users").then((user: User) => {
    cy.login(user.username, "s3cret", { rememberUser: true });

    // Verify session cookie
    cy.getCookie("connect.sid").should("have.property", "expiry");

    // Simulate browser restart
    cy.clearCookies();
    cy.visit("/");
    // Additional verification steps...
  });
});
```

---

### TC-AUTH-006: User Logout

**Objective**: Verify user can logout successfully
**Preconditions**: User is logged in

**Test Steps**:

1. Click logout button/link
2. Verify logout confirmation
3. Verify session termination

**Expected Results**:

- User successfully logged out
- Session terminated
- Redirected to login page
- Protected pages inaccessible

**Cypress Implementation**:

```typescript
it("should logout user successfully", () => {
  cy.database("find", "users").then((user: User) => {
    cy.login(user.username, "s3cret");

    // Logout
    cy.getBySel("sidenav-signout").click();

    // Verify logout
    cy.location("pathname").should("eq", "/signin");

    // Verify protected page access
    cy.visit("/personal");
    cy.location("pathname").should("eq", "/signin");
  });
});
```

---

## OAuth Provider Test Cases

### TC-AUTH-007: Auth0 Authentication Flow

**Objective**: Verify Auth0 OAuth flow works correctly
**Preconditions**: Auth0 configuration is set up

**Test Steps**:

1. Navigate to login page
2. Click "Sign in with Auth0"
3. Complete Auth0 authentication
4. Verify successful return to application

**Expected Results**:

- Auth0 login page opens
- User can authenticate with Auth0
- Successfully redirected back to app
- User session established

**Cypress Implementation**:

```typescript
it("should authenticate with Auth0", () => {
  cy.visit("/signin");
  cy.getBySel("auth-provider-auth0").click();

  // Handle Auth0 popup/redirect
  cy.origin("https://dev-auth0-domain.auth0.com", () => {
    cy.get("#username").type(Cypress.env("AUTH0_USERNAME"));
    cy.get("#password").type(Cypress.env("AUTH0_PASSWORD"));
    cy.get('button[type="submit"]').click();
  });

  // Verify return to app
  cy.location("pathname").should("eq", "/");
  cy.getBySel("user-profile").should("be.visible");
});
```

---

### TC-AUTH-008: OAuth Provider Error Handling

**Objective**: Verify proper handling of OAuth authentication errors
**Test Data**: Invalid OAuth scenarios

**Test Steps**:

1. Initiate OAuth flow
2. Simulate various error conditions:
   - User cancels authentication
   - Network error during OAuth
   - Invalid OAuth response
3. Verify error handling

**Expected Results**:

- Appropriate error messages displayed
- User returned to login page
- No partial authentication state

---

## API Authentication Test Cases

### TC-API-AUTH-001: JWT Token Validation

**Objective**: Verify API endpoints properly validate JWT tokens
**Test Data**: Valid and invalid JWT tokens

**Test Steps**:

1. Make API request with valid token
2. Make API request with invalid token
3. Make API request with expired token
4. Verify responses

**Expected Results**:

- Valid token: Request succeeds
- Invalid token: 401 Unauthorized
- Expired token: 401 Unauthorized

**Cypress Implementation**:

```typescript
describe("API Authentication", () => {
  it("should accept valid JWT token", () => {
    cy.loginByApi("testuser").then(() => {
      cy.request({
        method: "GET",
        url: "/api/users/profile",
        headers: {
          Authorization: `Bearer ${window.localStorage.getItem("authToken")}`,
        },
      }).then((response) => {
        expect(response.status).to.eq(200);
        expect(response.body).to.have.property("user");
      });
    });
  });

  it("should reject invalid JWT token", () => {
    cy.request({
      method: "GET",
      url: "/api/users/profile",
      headers: {
        Authorization: "Bearer invalid-token",
      },
      failOnStatusCode: false,
    }).then((response) => {
      expect(response.status).to.eq(401);
    });
  });
});
```

---

## Security Test Cases

### TC-AUTH-SEC-001: Password Security

**Objective**: Verify password security requirements
**Test Data**: Various password combinations

**Test Steps**:

1. Test password complexity requirements
2. Verify password hashing
3. Test password change functionality
4. Verify password history (if applicable)

**Expected Results**:

- Weak passwords rejected
- Passwords properly hashed in database
- Password changes require current password
- Password history enforced

---

### TC-AUTH-SEC-002: Session Security

**Objective**: Verify session security measures
**Test Data**: Session tokens and cookies

**Test Steps**:

1. Verify session token randomness
2. Test session timeout
3. Verify secure cookie flags
4. Test concurrent session handling

**Expected Results**:

- Session tokens are cryptographically secure
- Sessions timeout appropriately
- Cookies have secure flags set
- Concurrent sessions handled properly

---

## Performance Test Cases

### TC-AUTH-PERF-001: Login Performance

**Objective**: Verify login performance meets requirements
**Performance Criteria**: Login completes within 2 seconds

**Test Steps**:

1. Measure login time for valid credentials
2. Test with multiple concurrent logins
3. Monitor server response times

**Expected Results**:

- Single login: < 2 seconds
- Concurrent logins: Acceptable degradation
- Server response: < 500ms

**Cypress Implementation**:

```typescript
it("should login within performance threshold", () => {
  const startTime = Date.now();

  cy.database("find", "users").then((user: User) => {
    cy.visit("/signin");
    cy.getBySel("signin-username").type(user.username);
    cy.getBySel("signin-password").type("s3cret");
    cy.getBySel("signin-submit").click();

    cy.location("pathname")
      .should("eq", "/")
      .then(() => {
        const loginTime = Date.now() - startTime;
        expect(loginTime).to.be.lessThan(2000);
      });
  });
});
```

---

## Accessibility Test Cases

### TC-AUTH-A11Y-001: Keyboard Navigation

**Objective**: Verify authentication forms are keyboard accessible
**Test Data**: Keyboard navigation patterns

**Test Steps**:

1. Navigate login form using only keyboard
2. Verify tab order
3. Test form submission with keyboard
4. Verify focus management

**Expected Results**:

- All form elements accessible via keyboard
- Logical tab order
- Form submittable with Enter key
- Focus properly managed

**Cypress Implementation**:

```typescript
it("should support keyboard navigation", () => {
  cy.visit("/signin");

  // Test tab order
  cy.get("body").tab();
  cy.focused().should("have.attr", "data-test", "signin-username");

  cy.focused().tab();
  cy.focused().should("have.attr", "data-test", "signin-password");

  cy.focused().tab();
  cy.focused().should("have.attr", "data-test", "signin-submit");

  // Test form submission with Enter
  cy.getBySel("signin-username").type("testuser{enter}");
  // Verify form submission behavior
});
```

---

## Mobile Test Cases

### TC-AUTH-MOB-001: Mobile Login Experience

**Objective**: Verify authentication works on mobile devices
**Test Data**: Mobile viewport configurations

**Test Steps**:

1. Set mobile viewport
2. Test login form usability
3. Verify touch interactions
4. Test virtual keyboard behavior

**Expected Results**:

- Form elements properly sized for mobile
- Touch targets meet accessibility guidelines
- Virtual keyboard doesn't obscure form
- Responsive design works correctly

**Cypress Implementation**:

```typescript
describe("Mobile Authentication", () => {
  beforeEach(() => {
    cy.viewport("iphone-x");
  });

  it("should work on mobile viewport", () => {
    cy.visit("/signin");

    // Verify mobile-friendly form
    cy.getBySel("signin-username").should("be.visible");
    cy.getBySel("signin-password").should("be.visible");
    cy.getBySel("signin-submit").should("be.visible");

    // Test touch interaction
    cy.getBySel("signin-username").click();
    cy.focused().should("have.attr", "data-test", "signin-username");
  });
});
```
