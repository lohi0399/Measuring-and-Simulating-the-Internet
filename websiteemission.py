import requests
from bs4 import BeautifulSoup

def get_co2_emission(url_to_check):
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

