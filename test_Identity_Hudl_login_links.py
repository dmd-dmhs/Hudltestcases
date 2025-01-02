import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import (
    IDENTITY_LOGIN_URL, COOKIE_REJECT_ID, HUDL_DROPDOWN_SELECT_ID, LOGIN_BUTTON_SELECT_ID,
    IDENTITY_USERNAME_FIELD_ID, IDENTITY_LOGIN_BUTTON_NAME, valid_username
) 

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Edge()
    yield driver
    driver.quit()

@pytest.mark.parametrize("username, link_text, expected_partial_url", [
    (valid_username,"Forgot Password","https://identity.hudl.com/u/reset-password" ),
    (None, "Privacy Policy", "https://www.hudl.com/privacy"),
    (None,"Terms of Service", "https://www.hudl.com/terms"),
#    (valid_username,"Forgot Password","https://identity.hudl.com/u/reset-password" ),
    (None,"Create Account", "https://identity.hudl.com/u/signup/identifier"),
])

def test_links(driver, username, link_text, expected_partial_url):
    print(IDENTITY_LOGIN_URL)
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

    
    if username:
        # Find the username and password fields and enter the credentials
        username_field = driver.find_element(By.ID, IDENTITY_USERNAME_FIELD_ID)
 
        # Clear the fields before entering new text
        username_field.clear()

        # Enter the username
        username_field.send_keys(username)

        # Find the login button and click it
        login_button = driver.find_element(By.NAME, IDENTITY_LOGIN_BUTTON_NAME)
        login_button.click()
    else:
        pass

    # Find the link by its text and click it
    link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, link_text))
    )
    link.click()

    try:
        # Switch to the new window/tab
        driver.switch_to.window(driver.window_handles[-1])
    except:
        pass

    # Verify the URL of the new page contains the expected partial URL
    assert expected_partial_url in driver.current_url
    
    try:
        # Close the new window/tab and switch back to the original
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        pass