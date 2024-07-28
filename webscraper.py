import requests
from bs4 import BeautifulSoup

def generate_data():
    url = "https://olympics.com/en/olympic-games/beijing-2022/medals"
    
    # Set up a session
    session = requests.Session()
    
    # Add headers to mimic a browser
    headers = { # hard-coded headers to allow the program to access the site
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = session.get(url, headers=headers, timeout=60)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        countries = soup.find_all('span', {'data-cy': 'country-name'}) #search for the correct span tags in the site's html 
        
        if not countries: #error message
            print("No countries found. The website structure might have changed.")
            return {}
        
        results = {}
        for i, country in enumerate(countries, start=1): #iterating through dictionary of country names and their medals
            country_name = country.text.strip()
            
            gold = soup.find('div', {'data-medal-id': f'gold-medals-row-{i}'})
            silver = soup.find('div', {'data-medal-id': f'silver-medals-row-{i}'})
            bronze = soup.find('div', {'data-medal-id': f'bronze-medals-row-{i}'})
            
            gold_count = gold.find('span', {'data-cy': 'medal-main'}).text.strip() if gold else '0'
            silver_count = silver.find('span', {'data-cy': 'medal-main'}).text.strip() if silver else '0'
            bronze_count = bronze.find('span', {'data-cy': 'medal-main'}).text.strip() if bronze else '0'
            
            gold_count = '0' if gold_count == '-' else gold_count #replace '-' from html with 0 for the medal number
            silver_count = '0' if silver_count == '-' else silver_count
            bronze_count = '0' if bronze_count == '-' else bronze_count
            
            results[country_name] = {
                'gold': gold_count,
                'silver': silver_count,
                'bronze': bronze_count
            }
        # Sort the results alphabetically by country name
        sorted_results = dict(sorted(results.items()))
        return sorted_results
    
    except requests.RequestException as e:
        print(f"An error occurred while fetching the webpage: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return {}