from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.common.keys import Keys
import os

# Set up the Chrome WebDriver   
chromedriver_path = os.path.expanduser('~/Desktop/chromedriver-mac-arm64/chromedriver')  # Expand '~' to full path
service = Service(chromedriver_path)
chrome_options = webdriver.ChromeOptions()

# Add options to run Chrome in headless mode (optional)

# Start the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the Vivino login page
driver.get('https://www.vivino.com/DK/en')
wait = WebDriverWait(driver, 10)
# Handle cookie consent popup if it appears
try:
    cookie_popup = wait.until(EC.element_to_be_clickable((By.ID, 'didomi-notice-agree-button')))
    cookie_popup.click()
    print("Cookie consent popup dismissed.")
except Exception as e:
    print("No cookie consent popup found or an error occurred:", e)

# Proceed to click the login button
login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Log in"]')))
login_button.click()
time.sleep(2)  # Wait for the login modal to appear
# Locate the username (email) field and enter your username
email_field = driver.find_element(By.ID, "email")  # Using the ID selector
email_field.send_keys('cvk_christian@hotmail.com')

# Locate the "Continue" button and click it
try:
    # Wait for the "Continue" button to be clickable
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Continue')]"))
    )
    continue_button.click()
    print("Clicked the Continue button!")
except Exception as e:
    print("Error while clicking 'Continue' button:", e)

# Wait for you to manually log in
print("Please log in manually in the browser and then press Enter.")
input("Press Enter once you're logged in...")

# Navigate to your wines page (replace 'christiankjr5' with your actual username)
user_profile_url = 'https://www.vivino.com/users/christiankjr5/wines'
driver.get(user_profile_url)
time.sleep(10) # Wait for the page to load


# Click the "Show More" button to load more wines
try:
    while True:
        show_more_button = wait.until(
            EC.element_to_be_clickable((By.ID, 'btn-more'))
        )
        show_more_button.click()
        print("Clicked 'Show More' button.")
        time.sleep(2)  # Wait for new content to load
except Exception as e:
    print("No more 'Show More' button found or an error occurred:", e)

time.sleep(20)  # Wait for the page to load completely
breakpoint()
# Close the browser
driver.quit()
