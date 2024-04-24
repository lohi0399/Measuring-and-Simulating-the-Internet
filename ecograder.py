import requests
from bs4 import BeautifulSoup
import json

# Function to get CSRF token
def get_csrf_token(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    csrf_token = soup.find('meta', attrs={'name': 'csrf_token'})['content']
    return csrf_token

# Function to get CO2 emissions data
def get_co2_emissions(url):
    with requests.Session() as session:
        # First, get the CSRF token
        initial_page = session.get('https://ecograder.com')
        csrf_token = get_csrf_token(initial_page.text)
        
        form_action_url = 'https://ecograder.com/scanning'
        payload = {
            '_token': csrf_token,
            'site_submitted': url
        }
        
        # Send the POST request
        response = session.post(form_action_url, data=payload)
        
        if response.status_code == 200:
            # Here, you would parse the successful HTML response to extract the data you need
            # You'll need to inspect the actual HTML you get back to determine how to do this
            soup = BeautifulSoup(response.text, 'html.parser')
            # Assuming 'div' with an id of 'results' contains the CO2 data
            co2_data_div = soup.find('div', id='app')  
            
            if co2_data_div:
                # Extract the JSON-like string from the 'data-page' attribute
                data_page_content = co2_data_div.get('data-page')
                
                # Convert the JSON-like string to a dictionary
                data_page_json = json.loads(data_page_content)
                
                # Extract the CO2 emissions score
                emissions_score = data_page_json.get('props', {}).get('report', {}).get('response', {}).get('emissions_score', 'No emissions data found')
                
                print(emissions_score)
            return emissions_score
        else:
            return 'Failed to retrieve data, status code: {}'.format(response.status_code)

# Example use
if __name__ == "__main__":
    website_url = input("Enter the website URL to check: ")
    emissions_data = get_co2_emissions(website_url)
    print(emissions_data)
