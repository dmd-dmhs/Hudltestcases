import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import (
    LOGIN_URL, COOKIE_REJECT_ID, HUDL_DROPDOWN_SELECT_ID, LOGIN_BUTTON_SELECT_ID, REDIRECT_URL
) 

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Edge()
    yield driver
    driver.quit()

@pytest.mark.parametrize("link_text, expected_partial_url", [
    ("Forgot your password?", "https://www.hudl.com/authentication"),
    ("reset your password here", "https://www.hudl.com/autentication"),
    ("Sign-up today!", REDIRECT_URL)
])

def test_links(driver, link_text, expected_partial_url):
    driver.get(LOGIN_URL)

    # Find the link by its text and click it
    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, link_text))
    )
    link.click()
     
    # Verify the URL of the new page contains the expected partial URL
    assert expected_partial_url in driver.current_url
