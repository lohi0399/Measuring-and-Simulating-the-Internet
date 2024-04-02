import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up the Selenium browser options
options = Options()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--disable-gpu')  # Disable GPU (might be required for headless mode)
options.add_argument('--no-sandbox')  # Disable the sandbox (might be required on some systems)
options.add_argument('start-maximized')  #
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')

# Set up the Selenium driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Function to get AMP URLs from Google search results
def get_amp_urls(search_query):
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Sleep to allow the page to load; adjust as necessary
    
    amp_urls = []
    return amp_urls

keywords = []  
amp_links = []
for keyword in keywords:
    links = get_amp_urls(keyword)
    amp_links.extend(links)
    time.sleep(10)  # Sleep to avoid being blocked by Google; adjust as necessary

# Save the URLs to a file
with open('amp_urls.txt', 'w') as file:
    for link in amp_links:
        file.write(link + "\n")

# Clean up: close the browser window
driver.quit()
