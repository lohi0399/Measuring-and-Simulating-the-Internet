from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def get_co2_emissions(url):
    # Path to your ChromeDriver (downloaded separately)
    chrome_driver_path = r'C:\Users\loghi\OneDrive\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe'  # Update this to your actual ChromeDriver path

    # Path to the Brave browser executable
    brave_path = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'

    # Set up the Selenium WebDriver
    options = Options()
    options.binary_location = brave_path  # Set path to Brave binary
    options.headless = True  # Runs Chrome in headless mode if desired

    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Navigate to the Digital Beacon page
        driver.get('https://digitalbeacon.co')

        # Find the input box and submit button
        input_box = driver.find_element(By.NAME, 'url')
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

        # Enter the URL and submit the form
        input_box.send_keys(url)
        submit_button.click()

        # Wait for the emissions score to load
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.stats p.h2'))
        )

        # Give some time for all data to load properly
        time.sleep(5)

        # Extract the CO2 data
        co2_data = driver.find_element(By.CSS_SELECTOR, 'div.stats p.h2').text
        return co2_data

    finally:
        driver.quit()

# Example use
# if __name__ == "__main__":
#     website_url = input("Enter the website URL to check: ")
#     emissions_data = get_co2_emissions(website_url)
#     print('CO2 Emissions for the first visit:', emissions_data)
