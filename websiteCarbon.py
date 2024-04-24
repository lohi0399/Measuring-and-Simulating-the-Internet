import requests

def get_carbon_emissions(url):
    # URL of the websitecarbon.com checker
    # checker_url = 'https://api.websitecarbon.com/site?url='
    checker_url = 'https://api.ecograder.com/site?url='

    # Make a request to the Website Carbon Calculator API
    response = requests.get(checker_url + url)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        return "Error: Failed to retrieve data."

# Example use:
if __name__ == "__main__":
    # Input website URL
    website_url = input("Enter the website URL to check: ")
    result = get_carbon_emissions(website_url)

    if isinstance(result, dict):
        # Extracting CO2 emissions in grams from the grid source
        co2_emissions = result['statistics']['co2']['grid']['grams']
        print(f"Average CO2 emissions per view (grid energy) for {website_url}: {co2_emissions:.2f} grams")
    else:
        print(result)
