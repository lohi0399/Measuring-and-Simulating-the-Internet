import requests
from bs4 import BeautifulSoup

def is_amp_enabled(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        
        # Check directly for '/amp/' substring in the HTML content
        if '/amp/' in html_content:
            return True
        
        # You can still parse with BeautifulSoup for more refined checks
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check for the 'amp' attribute in the <html> tag or other AMP characteristics
        if soup.find('html', attrs={'amp': True}) or soup.find('html', attrs={'⚡': True}):
            return True
        if has_amp_script(soup) or has_amp_boilerplate(soup) or has_amp_elements(soup):
            return True
        return False
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

# Add the helper functions here
def has_amp_script(soup):
    amp_scripts = soup.find_all('script', attrs={'src': lambda value: value and 'cdn.ampproject.org' in value})
    return bool(amp_scripts)

def has_amp_boilerplate(soup):
    amp_boilerplate = soup.find('style', attrs={'amp-boilerplate': True})
    return bool(amp_boilerplate)

def has_amp_elements(soup):
    amp_elements = soup.find_all(lambda tag: tag.name.startswith('amp-'))
    return bool(amp_elements)

# Example usage:
url = input("Enter the URL to check: ")
if is_amp_enabled(url):
    print("This site is AMP enabled.")
else:
    print("This site is not AMP enabled.")
    
    

# # URL of the page to check
# url = 'https://example.com'

# # Send the GET request
# response = requests.get(url)

# # Parse the HTML content
# soup = BeautifulSoup(response.content, 'html.parser')

# # Check for the AMP tag
# is_amp = bool(soup.find('html').get('amp')) or bool(soup.find('html').get('⚡'))

# print(f'The page is an AMP page: {is_amp}')
