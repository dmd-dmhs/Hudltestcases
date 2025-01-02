import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import (
    valid_username, invalid_username, valid_password, invalid_password,
    upper_valid_password, upper_valid_username,
    COOKIE_REJECT_ID, HUDL_DROPDOWN_SELECT_ID, LOGIN_BUTTON_SELECT_ID,
    USERNAME_FIELD_ID, PASSWORD_FIELD_ID, LOGIN_BUTTON_NAME,
    ERROR_MESSAGE_CLASS, ERROR_MESSAGE_ID, REDIRECT_URL, 
    PW_REDIRECT_URL, IDENTITY_LOGIN_BUTTON_NAME, IDENTITY_LOGIN_URL,
    IDENTITY_PASSWORD_FIELD_ID, IDENTITY_USERNAME_FIELD_ID,
)

LOGOUT_BUTTON_ID = "Log Out"

@pytest.fixture(scope="function")
def driver():
    # Specify the path to the Edge WebDriver executable
    #driver_path = "path/to/edgedriver_win64/msedgedriver.exe"
    driver = webdriver.Edge()#(executable_path=driver_path)
    yield driver
    driver.quit()

@pytest.mark.parametrize("username, password, expected", [
    (valid_username, invalid_password, "aria-invalid"),
    ("", "", REDIRECT_URL),
    (valid_username, "", PW_REDIRECT_URL),
    (invalid_username, valid_password, "aria-invalid"),
    (invalid_username, invalid_password, "aria-invalid"),
    (upper_valid_username, valid_password, "Home"),
    (valid_username, upper_valid_password, "aria-invalid"),
    (valid_username, valid_password, "Home")
])

def test_login_scenarios(driver, username, password, expected):
    driver.get(IDENTITY_LOGIN_URL)

    # Handle cookies popup if present
    try:
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.ID, COOKIE_REJECT_ID))
        ).click()
    except:
        pass  # If the popup is not present, continue
    
    # Click on the login button to reveal the dropdown
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-qa-id='{LOGIN_BUTTON_SELECT_ID}']"))
    ).click()
    
    # Select the Hudl login option from the dropdown
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-qa-id='{HUDL_DROPDOWN_SELECT_ID}']"))
    ).click()

    # Find the username and password fields and enter the credentials
    username_field = driver.find_element(By.ID, IDENTITY_USERNAME_FIELD_ID)
 
    # Clear the fields before entering new text
    username_field.clear()

    # Enter the username
    username_field.send_keys(username)

    # Find the login button and click it
    login_button = driver.find_element(By.NAME, IDENTITY_LOGIN_BUTTON_NAME)
    login_button.click()

    try:
        # Find the password fields and enter the credentials
        password_field = driver.find_element(By.ID, IDENTITY_PASSWORD_FIELD_ID)
        # Clear the fields before entering new text
        password_field.clear()
        password_field.send_keys(password)

        # Find the login button and click it
        login_button = driver.find_element(By.NAME, IDENTITY_LOGIN_BUTTON_NAME)
        login_button.click()

    except:
        pass  # If the password field is not present, continue

    # Verify the login result
    if expected == "Home":
        assert expected in driver.title
        # Log out after successful login
        WebDriverWait(driver, 20).until(
#            EC.element_to_be_clickable((By.ID, PROFILE_DROPDOWN_TITLE_ID))
            EC.element_to_be_clickable((By.CLASS_NAME, "hui-globalusermenu"))
        ).click()
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, LOGOUT_BUTTON_ID))
        ).click()    
    elif expected == "aria-invalid":
        password_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, IDENTITY_PASSWORD_FIELD_ID))
        )
        assert password_field.get_attribute("aria-invalid") == "true"
        error_message = driver.find_element(By.ID, ERROR_MESSAGE_ID)
        assert "Your email or password is incorrect. Try again." in error_message.text
    elif expected == REDIRECT_URL:
        assert expected in driver.current_url
    elif expected == PW_REDIRECT_URL:
        assert expected in driver.current_url
    else:
        error_message = driver.find_element(By.CLASS_NAME, ERROR_MESSAGE_CLASS)
        assert expected in error_message.text.lower()