from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")

# Path to chromedriver

service = Service(os.path.expanduser('~/Desktop/chromedriver-mac-arm64/chromedriver'))  # Expand '~' to full path  # Replace with the correct path to chromedriver

# Start WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Go to the login page
driver.get('https://www.vivino.com/users/sign_in')

# Wait for the email input field to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))  # Wait for email input field to appear

# Locate the email input field and enter your email
email_field = driver.find_element(By.ID, "email")  # Using the ID selector
email_field.send_keys('your-email@example.com')  # Replace with your email

# Locate and click the "Continue" button
try:
    # Wait until the continue button is clickable
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Fortsæt')]"))
    )
    continue_button.click()  # Click the button to proceed to the next step
    print("Clicked the Continue button!")
except Exception as e:
    print("Error while clicking 'Continue' button:", e)

# Wait for the password field to load after clicking "Continue"
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "user[password]")))  # Wait for password field to appear

# Now locate the password field and enter your password
password_field = driver.find_element(By.NAME, "user[password]")  # Adjust based on actual selector
password_field.send_keys('your-password')  # Replace with your password
print("Entered password!")

# Optionally, submit the form (if there’s a submit button after entering the password)
try:
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()  # Submit the login form
    print("Submitted login form!")
except Exception as e:
    print("Error while submitting login form:", e)

# Wait for the page to load after login
time.sleep(5)

# Now you can navigate to other pages or perform any actions on the site
print("Login successful!")

# For example, go to the user's wine list page
driver.get('https://www.vivino.com/users/your-username/wines')

# Wait and interact with the page as needed
time.sleep(5)

# Close the browser
driver.quit()
