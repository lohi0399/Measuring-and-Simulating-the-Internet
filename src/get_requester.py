import asyncio
import aiohttp
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup

from asyncio_throttle import Throttler
# This is an asynchronous code that will get the JSON data from the API and parse it into a CSV file.
def parse(htmls): # parse the JSON and write each entry to the main CSV file.
    data = []
    for code in htmls:
        try:
            data.append([
                code['url'],
                code['green'],
                code['bytes'],
                code['cleanerThan'],
                code['statistics']['adjustedBytes'],
                code['statistics']['energy'],
                code['statistics']['co2']['grid']['grams'],
                code['statistics']['co2']['grid']['litres'],
                code['statistics']['co2']['renewable']['grams'],
                code['statistics']['co2']['renewable']['litres'],
                code['timestamp']
            ])
        except (KeyError, aiohttp.ContentTypeError) as e:
            print(f'File {file} is empty. Skipping.{e}')

    data.insert(0, ['URL', 'Green Hosting', 'Bytes', 'Cleaner Than %', 'Stats_Adjusted Bytes', 'Stats_Energy', 'Stats_CO2_Grid_Grams', 'Stats_CO2_Grid_Litres', 'Stats_CO2_Renewable_Grams', 'Stats_CO2_Renewable_Litres'])

    with open('data\\csv\\main.csv', "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)


async def get(throttler, session: aiohttp.ClientSession, site: str): # Gets the JSON data from the API.
    async with throttler:
        url = f"https://api.websitecarbon.com/site?url={site}/"
        # url = f"https://api.websiteemissions.com/site?url={site}/"
        print(f"Requesting: {site}")
        resp = await session.request('GET', url=url)
        data = await resp.json(content_type='application/json')
        print(f"Received: {site}")
        return data


async def main(urls):
    tasks = []
    throttler = Throttler(rate_limit=100, period=15) # Throttles the outgoing requests to not overload the API.
    async with aiohttp.ClientSession() as session: # Gets an url and appends it to a task list.
        for c in urls:
            tasks.append(get(throttler, session=session, site=c))
        htmls = await asyncio.gather(*tasks, return_exceptions=True)
        parse(htmls)
        return htmls

def get_co2_emissions_db(url):
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


def get_co2_emission_websitemissions(url_to_check):
    # Assuming there's an API or form submission URL where data is sent
    form_url = 'https://websiteemissions.com/'  # Placeholder, change to actual URL
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    # Data payload as it would be submitted through the website form
    data = {
        'url': url_to_check
    }
    
    # Sending POST request
    response = requests.post(form_url, headers=headers, data=data)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extracting CO2 emission data
        result_header = soup.find("div", {"class": "carbon-results-monthly-header"})
        if result_header:
            return result_header.text
        else:
            return "No CO2 emission data found."
    else:
        return "Failed to fetch data, status code: " + str(response.status_code)

if __name__ == '__main__': # Start the program and get the JSON data from the API.
    urls = [] # The test_data.csv is a list of URLs sourced from the top-1m.csv file.
    with open('test_data.csv', newline='') as file:
        for row in csv.reader(file):
            urls.append(row[0])
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(urls))
    
#     website_url = input("Enter the website URL to check: ")
#     emissions_data = get_co2_emissions_db(website_url)
#     print('CO2 Emissions for the first visit:', emissions_data)
