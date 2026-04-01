import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    """Fixture to initialize and quit the WebDriver."""
    # Selenium Manager will auto-download the appropriate driver
    options = Options()
    options.add_argument("--headless")  # run without UI
    options.add_argument("--no-sandbox")  # required in many CI environments
    options.add_argument("--disable-dev-shm-usage")  # overcome limited /dev/shm size on Linux

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_successful_login(driver):
    """Test successful login with valid credentials."""
    # Navigate to the login page
    driver.get("https://the-internet.herokuapp.com/login")

    # Find username and password fields and enter credentials
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    username_field.send_keys("tomsmith")
    password_field.send_keys("SuperSecretPassword!")

    # Click the login button
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # Wait for the success message to appear
    wait = WebDriverWait(driver, 10)
    success_message = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.success"))
    )

    # Assert that success message is displayed and contains expected text
    assert success_message.is_displayed(), "Success message is not displayed"
    assert "You logged into a secure area!" in success_message.text, \
        f"Expected success message, got: {success_message.text}"

    # Additional assertion: verify the logout button is present (confirms successful login)
    logout_button = driver.find_element(By.CSS_SELECTOR, "a[href='/logout']")
    assert logout_button.is_displayed(), "Logout button not found after login"


def test_unsuccessful_login(driver):
    """Test unsuccessful login with invalid credentials."""
    # Navigate to the login page
    driver.get("https://the-internet.herokuapp.com/login")

    # Test with invalid username
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    username_field.send_keys("invalid_user")
    password_field.send_keys("SuperSecretPassword!")

    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # Wait for the error message
    wait = WebDriverWait(driver, 10)
    error_message = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.error"))
    )

    # Assert that error message is displayed
    assert error_message.is_displayed(), "Error message is not displayed"
    assert "Your username is invalid!" in error_message.text, \
        f"Expected error message about invalid username, got: {error_message.text}"

    # Clear fields and test with invalid password
    driver.get("https://the-internet.herokuapp.com/login")  # Refresh to clear previous state

    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    username_field.send_keys("tomsmith")
    password_field.send_keys("wrong_password")

    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # Wait for the error message
    error_message = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.error"))
    )

    # Assert that error message for invalid password is displayed
    assert error_message.is_displayed(), "Error message is not displayed"
    assert "Your password is invalid!" in error_message.text, \
        f"Expected error message about invalid password, got: {error_message.text}"