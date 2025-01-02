import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from constants import (
    valid_username, invalid_username, valid_password, invalid_password,
    upper_valid_password, upper_valid_username,
    ERROR_MESSAGE_CLASS, REDIRECT_URL, LOGIN_URL, USERNAME_FIELD_ID,
    PASSWORD_FIELD_ID, LOGIN_BUTTON_NAME
)

@pytest.fixture(scope="function")
def driver():
    # Specify the path to the Edge WebDriver executable
    #driver_path = "path/to/edgedriver_win64/msedgedriver.exe"
    driver = webdriver.Edge()#(executable_path=driver_path)
    yield driver
    driver.quit()

@pytest.mark.parametrize("username, password, expected", [
    (valid_username, valid_password, "Home"),
    (valid_username, invalid_password, REDIRECT_URL),
    ("", "", REDIRECT_URL),
    (invalid_username, valid_password, REDIRECT_URL),
    (invalid_username, invalid_password, REDIRECT_URL),
    (upper_valid_username, valid_password, "Home"),
    (valid_username, upper_valid_password, REDIRECT_URL),
])

def test_login_scenarios(driver, username, password, expected):
    driver.get(LOGIN_URL)

    # Find the username and password fields and enter the credentials
    username_field = driver.find_element(By.ID, USERNAME_FIELD_ID)
    password_field = driver.find_element(By.ID, PASSWORD_FIELD_ID)
    # Clear the fields before entering new text
    username_field.clear()
    password_field.clear()
    username_field.send_keys(username)
    password_field.send_keys(password)
    #username_field.send_keys({your_username})
    #password_field.send_keys({your_password})
    # Debug prints to verify clearing
    print(f"Username field after clear: '{username_field.get_attribute('value')}'")
    print(f"Password field after clear: '{password_field.get_attribute('value')}'")


    # Find the login button and click it
    login_button = driver.find_element(By.NAME, LOGIN_BUTTON_NAME)
    login_button.click()
    
    # Verify the login result
    if expected == "Home":
        assert expected in driver.title
    elif expected == REDIRECT_URL:
        assert expected in driver.current_url
    else:
        error_message = driver.find_element(By.CLASS_NAME, ERROR_MESSAGE_CLASS)
        assert expected in error_message.text.lower()
