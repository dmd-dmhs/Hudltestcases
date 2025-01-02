import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSessionIdException
from constants import (
    IDENTITY_LOGIN_URL, COOKIE_REJECT_ID, HUDL_DROPDOWN_SELECT_ID, LOGIN_BUTTON_SELECT_ID
) 

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Edge()
    yield driver
    driver.quit()

@pytest.mark.parametrize("provider, expected_partial_url", [
    ("google", "accounts.google.com"),
    ("facebook", "facebook.com"),
    ("apple", "appleid.apple.com")
])

def test_social_logins(driver, provider, expected_partial_url):
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
  
    # Find the login button by its data-provider attribute
    login_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-provider='{provider}']"))
    )
    
    # Scroll to the login button to make it visible
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
    
    # Click the login button
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-provider='{provider}']"))
    ).click()
    
    # Verify the URL of the new page contains the expected partial URL
    assert expected_partial_url in driver.current_url
