from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os
from bs4 import BeautifulSoup
import re

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

print("Please log in manually, navigate to your 'My Wines' page, and click 'Show More' until all wines are visible.")
input("Press ENTER when you are done and ready to scrape...")

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Find each wine item
wine_items = soup.find_all("div", class_="activity-wine-card")

wine_data = []

for item in wine_items:
    # Image URL
    image_style = item.find("a", class_="wine-image-container")["style"]
    image_url = re.search(r"url\((.*?)\)", image_style).group(1)
    image_url = "https:" + image_url if image_url.startswith("//") else image_url

    # Winery
    winery_tag = item.find("a", href=re.compile("/wineries/"))
    winery = winery_tag.text.strip() if winery_tag else None

    # Name
    name_tag = item.find("p", class_="wine-name").find("a")
    name = name_tag.text.strip() if name_tag else None

    # Vintage
    vintage = item.get("data-year")

    # Region and Country
    region_country_links = item.select(".text-mini a")
    region = region_country_links[0].text.strip() if len(region_country_links) > 0 else None
    country = region_country_links[1].text.strip() if len(region_country_links) > 1 else None

    # Append extracted data to wine_data list
    wine_data.append({
        "image": image_url,
        "name": name,
        "winery": winery,
        "vintage": vintage,
        "region": region,
        "country": country
    })

# Save the data to a CSV file
df = pd.DataFrame(wine_data)
df.to_csv('wine_data.csv', index=False)
print("Wine data saved to wine_data.csv")
