import pandas as pd
import folium
from folium import Map
import requests
from selenium.webdriver.common.by import By
import time

# Load your scraped data
df = pd.read_csv('wine_data.csv')

# Function to geocode a region + country to lat/lon
def geocode_location(region, country):
    query = f"{region}, {country}"
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json"
    try:
        response = requests.get(url, headers={'User-Agent': 'WineMapper'})
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except:
        return None, None
    return None, None

def search_google_for_address(driver, winery, region, country):
    query = f"{winery}, {region}, {country} address"
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    driver.get(search_url)
    time.sleep(3)  # Give page time to load

    try:
        # Google typically places the address in this kind of element
        address_element = driver.find_element(By.CSS_SELECTOR, '[data-attrid="kc:/location/location:address"]')
        return address_element.text.split("Adresse:")[-1].strip()
    except Exception as e:
        print(f"Address not found for: {winery} — {e}")
        return None

class WineMap()

# Create map
wine_map = folium.Map(location=[20, 0], zoom_start=2)

for _, row in df.iterrows():
    lat, lon = geocode_location(row['region'], row['country'])
    if lat and lon:
        popup_html = f"""
        <b>{row['name']} ({row['vintage']})</b><br>
        <i>{row['winery']}</i><br>
        {row['region']}, {row['country']}<br>
        <img src="{row['image']}" width="100">
        """
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(wine_map)

wine_map.save('my_wine_map.html')
