"""
Cypress Real World App - Page Object Model Classes

This module contains Page Object Model (POM) classes for the Cypress Real World App.
Each class represents a specific page or component and encapsulates its elements and actions.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator):
        """Find a single element."""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        """Find multiple elements."""
        return self.driver.find_elements(*locator)
    
    def click(self, locator):
        """Click an element."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def send_keys(self, locator, text):
        """Send text to an element."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """Get text from an element."""
        element = self.find_element(locator)
        return element.text
    
    def is_element_present(self, locator, timeout=5):
        """Check if element is present."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_clickable(self, locator, timeout=10):
        """Wait for element to be clickable."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )


class SignInPage(BasePage):
    """Page object for the Sign In page."""
    
    # Locators
    USERNAME_INPUT = (By.CSS_SELECTOR, "[data-test='signin-username']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-test='signin-password']")
    SIGNIN_BUTTON = (By.CSS_SELECTOR, "[data-test='signin-submit']")
    SIGNUP_LINK = (By.CSS_SELECTOR, "[data-test='signin-signup']")
    REMEMBER_ME_CHECKBOX = (By.CSS_SELECTOR, "[data-test='signin-remember-me']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='signin-error']")
    
    def enter_username(self, username):
        """Enter username."""
        self.send_keys(self.USERNAME_INPUT, username)
    
    def enter_password(self, password):
        """Enter password."""
        self.send_keys(self.PASSWORD_INPUT, password)
    
    def click_signin_button(self):
        """Click the sign in button."""
        self.click(self.SIGNIN_BUTTON)
    
    def click_signup_link(self):
        """Click the sign up link."""
        self.click(self.SIGNUP_LINK)
    
    def check_remember_me(self):
        """Check the remember me checkbox."""
        self.click(self.REMEMBER_ME_CHECKBOX)
    
    def login(self, username, password, remember_me=False):
        """Perform login with credentials."""
        self.enter_username(username)
        self.enter_password(password)
        if remember_me:
            self.check_remember_me()
        self.click_signin_button()
    
    def get_error_message(self):
        """Get error message text."""
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_displayed(self):
        """Check if error message is displayed."""
        return self.is_element_present(self.ERROR_MESSAGE)


class SignUpPage(BasePage):
    """Page object for the Sign Up page."""
    
    # Locators
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "[data-test='signup-first-name']")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "[data-test='signup-last-name']")
    USERNAME_INPUT = (By.CSS_SELECTOR, "[data-test='signup-username']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-test='signup-password']")
    CONFIRM_PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-test='signup-confirm-password']")
    SIGNUP_BUTTON = (By.CSS_SELECTOR, "[data-test='signup-submit']")
    SIGNIN_LINK = (By.CSS_SELECTOR, "[data-test='signup-signin']")
    
    def enter_first_name(self, first_name):
        """Enter first name."""
        self.send_keys(self.FIRST_NAME_INPUT, first_name)
    
    def enter_last_name(self, last_name):
        """Enter last name."""
        self.send_keys(self.LAST_NAME_INPUT, last_name)
    
    def enter_username(self, username):
        """Enter username."""
        self.send_keys(self.USERNAME_INPUT, username)
    
    def enter_password(self, password):
        """Enter password."""
        self.send_keys(self.PASSWORD_INPUT, password)
    
    def enter_confirm_password(self, confirm_password):
        """Enter confirm password."""
        self.send_keys(self.CONFIRM_PASSWORD_INPUT, confirm_password)
    
    def click_signup_button(self):
        """Click the sign up button."""
        self.click(self.SIGNUP_BUTTON)
    
    def click_signin_link(self):
        """Click the sign in link."""
        self.click(self.SIGNIN_LINK)
    
    def sign_up(self, first_name, last_name, username, password, confirm_password):
        """Perform sign up with user details."""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_username(username)
        self.enter_password(password)
        self.enter_confirm_password(confirm_password)
        self.click_signup_button()


class DashboardPage(BasePage):
    """Page object for the main dashboard/home page."""
    
    # Locators
    APP_LOGO = (By.CSS_SELECTOR, "[data-test='app-name-logo']")
    NEW_TRANSACTION_BUTTON = (By.CSS_SELECTOR, "[data-test='nav-top-new-transaction']")
    NOTIFICATIONS_BUTTON = (By.CSS_SELECTOR, "[data-test='nav-top-notifications']")
    NOTIFICATION_COUNT = (By.CSS_SELECTOR, "[data-test='nav-top-notifications-count']")
    SIDENAV_TOGGLE = (By.CSS_SELECTOR, "[data-test='sidenav-toggle']")
    USER_BALANCE = (By.CSS_SELECTOR, "[data-test='sidenav-user-balance']")
    
    # Transaction tabs
    PUBLIC_TAB = (By.CSS_SELECTOR, "[data-test='nav-public-tab']")
    CONTACTS_TAB = (By.CSS_SELECTOR, "[data-test='nav-contacts-tab']")
    PERSONAL_TAB = (By.CSS_SELECTOR, "[data-test='nav-personal-tab']")
    
    # Transaction list
    TRANSACTION_LIST = (By.CSS_SELECTOR, "[data-test='transaction-list']")
    TRANSACTION_ITEMS = (By.CSS_SELECTOR, "[data-test*='transaction-item']")
    EMPTY_LIST = (By.CSS_SELECTOR, "[data-test*='empty-list']")
    
    def click_new_transaction(self):
        """Click the new transaction button."""
        self.click(self.NEW_TRANSACTION_BUTTON)
    
    def click_notifications(self):
        """Click the notifications button."""
        self.click(self.NOTIFICATIONS_BUTTON)
    
    def click_public_tab(self):
        """Click the public transactions tab."""
        self.click(self.PUBLIC_TAB)
    
    def click_contacts_tab(self):
        """Click the contacts transactions tab."""
        self.click(self.CONTACTS_TAB)
    
    def click_personal_tab(self):
        """Click the personal transactions tab."""
        self.click(self.PERSONAL_TAB)
    
    def get_notification_count(self):
        """Get notification count."""
        return self.get_text(self.NOTIFICATION_COUNT)
    
    def get_user_balance(self):
        """Get user balance."""
        return self.get_text(self.USER_BALANCE)
    
    def get_transaction_items(self):
        """Get all transaction items."""
        return self.find_elements(self.TRANSACTION_ITEMS)
    
    def click_transaction_item(self, index=0):
        """Click a transaction item by index."""
        transactions = self.get_transaction_items()
        if transactions and len(transactions) > index:
            transactions[index].click()
    
    def toggle_sidenav(self):
        """Toggle the side navigation."""
        self.click(self.SIDENAV_TOGGLE)
    
    def is_empty_list_displayed(self):
        """Check if empty list message is displayed."""
        return self.is_element_present(self.EMPTY_LIST)


class NewTransactionPage(BasePage):
    """Page object for the new transaction page."""
    
    # Locators
    USER_SEARCH_INPUT = (By.CSS_SELECTOR, "[data-test='user-list-search-input']")
    USER_LIST_ITEMS = (By.CSS_SELECTOR, "[data-test*='user-list-item']")
    AMOUNT_INPUT = (By.CSS_SELECTOR, "[data-test*='transaction-create-amount-input']")
    DESCRIPTION_INPUT = (By.CSS_SELECTOR, "[data-test*='transaction-create-description-input']")
    SUBMIT_PAYMENT_BUTTON = (By.CSS_SELECTOR, "[data-test*='transaction-create-submit-payment']")
    SUBMIT_REQUEST_BUTTON = (By.CSS_SELECTOR, "[data-test*='transaction-create-submit-request']")
    CREATE_ANOTHER_BUTTON = (By.CSS_SELECTOR, "[data-test='new-transaction-create-another-transaction']")
    RETURN_TO_TRANSACTIONS_BUTTON = (By.CSS_SELECTOR, "[data-test='new-transaction-return-to-transactions']")
    
    def search_user(self, search_term):
        """Search for a user."""
        self.send_keys(self.USER_SEARCH_INPUT, search_term)
    
    def select_user_by_name(self, name):
        """Select a user by name."""
        user_locator = (By.XPATH, f"//div[contains(@data-test, 'user-list-item') and contains(text(), '{name}')]")
        self.click(user_locator)
    
    def enter_amount(self, amount):
        """Enter transaction amount."""
        self.send_keys(self.AMOUNT_INPUT, amount)
    
    def enter_description(self, description):
        """Enter transaction description."""
        self.send_keys(self.DESCRIPTION_INPUT, description)
    
    def click_submit_payment(self):
        """Click submit payment button."""
        self.click(self.SUBMIT_PAYMENT_BUTTON)
    
    def click_submit_request(self):
        """Click submit request button."""
        self.click(self.SUBMIT_REQUEST_BUTTON)
    
    def create_payment_transaction(self, recipient_name, amount, description):
        """Create a payment transaction."""
        self.search_user(recipient_name)
        self.select_user_by_name(recipient_name)
        self.enter_amount(amount)
        self.enter_description(description)
        self.click_submit_payment()
    
    def create_request_transaction(self, recipient_name, amount, description):
        """Create a request transaction."""
        self.search_user(recipient_name)
        self.select_user_by_name(recipient_name)
        self.enter_amount(amount)
        self.enter_description(description)
        self.click_submit_request()
    
    def click_create_another(self):
        """Click create another transaction button."""
        self.click(self.CREATE_ANOTHER_BUTTON)
    
    def click_return_to_transactions(self):
        """Click return to transactions button."""
        self.click(self.RETURN_TO_TRANSACTIONS_BUTTON)


class TransactionDetailPage(BasePage):
    """Page object for the transaction detail page."""
    
    # Locators
    TRANSACTION_HEADER = (By.CSS_SELECTOR, "[data-test='transaction-detail-header']")
    TRANSACTION_AMOUNT = (By.CSS_SELECTOR, "[data-test*='transaction-amount']")
    TRANSACTION_DESCRIPTION = (By.CSS_SELECTOR, "[data-test='transaction-description']")
    LIKE_BUTTON = (By.CSS_SELECTOR, "[data-test*='transaction-like-button']")
    LIKE_COUNT = (By.CSS_SELECTOR, "[data-test*='transaction-like-count']")
    ACCEPT_REQUEST_BUTTON = (By.CSS_SELECTOR, "[data-test*='transaction-accept-request']")
    REJECT_REQUEST_BUTTON = (By.CSS_SELECTOR, "[data-test*='transaction-reject-request']")
    COMMENT_INPUT = (By.CSS_SELECTOR, "[data-test='transaction-comment-input']")
    COMMENT_SUBMIT_BUTTON = (By.CSS_SELECTOR, "[data-test='transaction-comment-submit']")
    
    def get_transaction_amount(self):
        """Get transaction amount."""
        return self.get_text(self.TRANSACTION_AMOUNT)
    
    def get_transaction_description(self):
        """Get transaction description."""
        return self.get_text(self.TRANSACTION_DESCRIPTION)
    
    def click_like_button(self):
        """Click the like button."""
        self.click(self.LIKE_BUTTON)
    
    def get_like_count(self):
        """Get like count."""
        return self.get_text(self.LIKE_COUNT)
    
    def click_accept_request(self):
        """Click accept request button."""
        self.click(self.ACCEPT_REQUEST_BUTTON)
    
    def click_reject_request(self):
        """Click reject request button."""
        self.click(self.REJECT_REQUEST_BUTTON)
    
    def add_comment(self, comment):
        """Add a comment to the transaction."""
        self.send_keys(self.COMMENT_INPUT, comment)
        self.click(self.COMMENT_SUBMIT_BUTTON)
    
    def is_accept_button_present(self):
        """Check if accept button is present."""
        return self.is_element_present(self.ACCEPT_REQUEST_BUTTON)
    
    def is_reject_button_present(self):
        """Check if reject button is present."""
        return self.is_element_present(self.REJECT_REQUEST_BUTTON)


class BankAccountsPage(BasePage):
    """Page object for the bank accounts page."""
    
    # Locators
    CREATE_BUTTON = (By.CSS_SELECTOR, "[data-test='bankaccount-new']")
    BANK_NAME_INPUT = (By.CSS_SELECTOR, "[data-test='bankaccount-bankName-input']")
    ROUTING_NUMBER_INPUT = (By.CSS_SELECTOR, "[data-test='bankaccount-routingNumber-input']")
    ACCOUNT_NUMBER_INPUT = (By.CSS_SELECTOR, "[data-test='bankaccount-accountNumber-input']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "[data-test='bankaccount-submit']")
    BANK_ACCOUNT_LIST = (By.CSS_SELECTOR, "[data-test='bankaccount-list']")
    DELETE_BUTTONS = (By.CSS_SELECTOR, "[data-test*='bankaccount-delete']")
    
    def click_create_button(self):
        """Click the create bank account button."""
        self.click(self.CREATE_BUTTON)
    
    def enter_bank_name(self, bank_name):
        """Enter bank name."""
        self.send_keys(self.BANK_NAME_INPUT, bank_name)
    
    def enter_routing_number(self, routing_number):
        """Enter routing number."""
        self.send_keys(self.ROUTING_NUMBER_INPUT, routing_number)
    
    def enter_account_number(self, account_number):
        """Enter account number."""
        self.send_keys(self.ACCOUNT_NUMBER_INPUT, account_number)
    
    def click_submit(self):
        """Click submit button."""
        self.click(self.SUBMIT_BUTTON)
    
    def create_bank_account(self, bank_name, routing_number, account_number):
        """Create a new bank account."""
        self.click_create_button()
        self.enter_bank_name(bank_name)
        self.enter_routing_number(routing_number)
        self.enter_account_number(account_number)
        self.click_submit()
    
    def delete_first_bank_account(self):
        """Delete the first bank account in the list."""
        delete_buttons = self.find_elements(self.DELETE_BUTTONS)
        if delete_buttons:
            delete_buttons[0].click()


class UserSettingsPage(BasePage):
    """Page object for the user settings page."""
    
    # Locators
    SETTINGS_FORM = (By.CSS_SELECTOR, "[data-test='user-settings-form']")
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "[data-test*='user-settings-firstName-input']")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "[data-test*='user-settings-lastName-input']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "[data-test*='user-settings-email-input']")
    PHONE_NUMBER_INPUT = (By.CSS_SELECTOR, "[data-test*='user-settings-phoneNumber-input']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "[data-test='user-settings-submit']")
    
    def enter_first_name(self, first_name):
        """Enter first name."""
        self.send_keys(self.FIRST_NAME_INPUT, first_name)
    
    def enter_last_name(self, last_name):
        """Enter last name."""
        self.send_keys(self.LAST_NAME_INPUT, last_name)
    
    def enter_email(self, email):
        """Enter email."""
        self.send_keys(self.EMAIL_INPUT, email)
    
    def enter_phone_number(self, phone_number):
        """Enter phone number."""
        self.send_keys(self.PHONE_NUMBER_INPUT, phone_number)
    
    def click_submit(self):
        """Click submit button."""
        self.click(self.SUBMIT_BUTTON)
    
    def update_user_settings(self, first_name=None, last_name=None, email=None, phone_number=None):
        """Update user settings."""
        if first_name:
            self.enter_first_name(first_name)
        if last_name:
            self.enter_last_name(last_name)
        if email:
            self.enter_email(email)
        if phone_number:
            self.enter_phone_number(phone_number)
        self.click_submit()


class NavigationComponent(BasePage):
    """Component for navigation actions."""
    
    # Locators
    SIDENAV_TOGGLE = (By.CSS_SELECTOR, "[data-test='sidenav-toggle']")
    SIDENAV_HOME = (By.CSS_SELECTOR, "[data-test='sidenav-home']")
    SIDENAV_MY_ACCOUNT = (By.CSS_SELECTOR, "[data-test='sidenav-my-account']")
    SIDENAV_BANK_ACCOUNTS = (By.CSS_SELECTOR, "[data-test='sidenav-bank-accounts']")
    SIDENAV_NOTIFICATIONS = (By.CSS_SELECTOR, "[data-test='sidenav-notifications']")
    SIDENAV_USER_SETTINGS = (By.CSS_SELECTOR, "[data-test='sidenav-user-settings']")
    SIDENAV_LOGOUT = (By.CSS_SELECTOR, "[data-test='sidenav-signout']")
    
    def open_sidenav(self):
        """Open the side navigation."""
        self.click(self.SIDENAV_TOGGLE)
    
    def navigate_to_home(self):
        """Navigate to home page."""
        self.click(self.SIDENAV_HOME)
    
    def navigate_to_my_account(self):
        """Navigate to my account page."""
        self.click(self.SIDENAV_MY_ACCOUNT)
    
    def navigate_to_bank_accounts(self):
        """Navigate to bank accounts page."""
        self.click(self.SIDENAV_BANK_ACCOUNTS)
    
    def navigate_to_notifications(self):
        """Navigate to notifications page."""
        self.click(self.SIDENAV_NOTIFICATIONS)
    
    def navigate_to_user_settings(self):
        """Navigate to user settings page."""
        self.click(self.SIDENAV_USER_SETTINGS)
    
    def logout(self):
        """Logout the user."""
        self.click(self.SIDENAV_LOGOUT)


class NotificationPage(BasePage):
    """Page object for the notifications page."""
    
    # Locators
    NOTIFICATIONS_LIST = (By.CSS_SELECTOR, "[data-test='notifications-list']")
    NOTIFICATION_ITEMS = (By.CSS_SELECTOR, "[data-test*='notification-list-item']")
    MARK_AS_READ_BUTTONS = (By.CSS_SELECTOR, "[data-test*='notification-mark-read']")
    
    def get_notification_items(self):
        """Get all notification items."""
        return self.find_elements(self.NOTIFICATION_ITEMS)
    
    def click_notification_item(self, index=0):
        """Click a notification item by index."""
        notifications = self.get_notification_items()
        if notifications and len(notifications) > index:
            notifications[index].click()
    
    def mark_first_notification_as_read(self):
        """Mark the first notification as read."""
        mark_read_buttons = self.find_elements(self.MARK_AS_READ_BUTTONS)
        if mark_read_buttons:
            mark_read_buttons[0].click()


class AlertComponent(BasePage):
    """Component for alert messages."""
    
    # Locators
    SUCCESS_ALERT = (By.CSS_SELECTOR, "[data-test='alert-bar-success']")
    ERROR_ALERT = (By.CSS_SELECTOR, "[data-test='alert-bar-error']")
    WARNING_ALERT = (By.CSS_SELECTOR, "[data-test='alert-bar-warning']")
    INFO_ALERT = (By.CSS_SELECTOR, "[data-test='alert-bar-info']")
    
    def get_success_message(self):
        """Get success alert message."""
        return self.get_text(self.SUCCESS_ALERT)
    
    def get_error_message(self):
        """Get error alert message."""
        return self.get_text(self.ERROR_ALERT)
    
    def is_success_alert_displayed(self):
        """Check if success alert is displayed."""
        return self.is_element_present(self.SUCCESS_ALERT)
    
    def is_error_alert_displayed(self):
        """Check if error alert is displayed."""
        return self.is_element_present(self.ERROR_ALERT)
    
    def wait_for_success_alert(self, timeout=10):
        """Wait for success alert to appear."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.SUCCESS_ALERT)
        )
    
    def wait_for_error_alert(self, timeout=10):
        """Wait for error alert to appear."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.ERROR_ALERT)
        )
