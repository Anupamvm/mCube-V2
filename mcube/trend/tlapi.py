import requests
from bs4 import BeautifulSoup as bs

def login(url, login_route, headers, username, password):
    """
    Logs in to the given URL and returns the session object and login status.

    :param url: Base URL of the website
    :param login_route: Login route path
    :param headers: HTTP headers for the request
    :param username: Login username
    :param password: Login password
    :return: Tuple of session object and boolean login status
    """
    session = requests.Session()
    
    # Fetch the CSRF token
    response = session.get(url, headers=headers)
    if 'csrftoken' not in response.cookies:
        print("CSRF token not found!")
        return session, False
    
    csrf_token = response.cookies['csrftoken']
    print("CSRF Token:", csrf_token)
    
    # Login payload
    login_payload = {
        'login': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }
    
    # Login request
    login_response = session.post(url + login_route, headers=headers, data=login_payload)
    print("Login Status Code:", login_response.status_code)
    
    if login_response.status_code != 200:
        print("Login failed!")
        return session, False
    
    return session, True

def trenddata():
    """
    Fetches and processes trend data from the website.
    
    :return: List of dictionaries with conference call details.
    """
    URL = "https://trendlyne.com/"
    LOGIN_ROUTE = "accounts/login/"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'origin': URL,
        'referer': URL + LOGIN_ROUTE
    }
    USERNAME = "avmgp.in@gmail.com"
    PASSWORD = "LoveOnlyWork1!"
    
    # Perform login
    session, is_logged_in = login(URL, LOGIN_ROUTE, HEADERS, USERNAME, PASSWORD)
    if not is_logged_in:
        print("Exiting due to failed login.")
        return []
    
    # Fetch conference calls page
    page = session.get(URL + 'conference-calls/', headers=HEADERS)
    if page.status_code != 200:
        print("Failed to fetch conference calls page!")
        return []
    
    soup = bs(page.content, 'html.parser')
    conference_calls = []
    
    # Process and collect news links
    for anch in soup.find_all('a', attrs={'class': 'newslink'}):
        call_details = {
            "text": anch.text.strip(),
            "link": anch['href']
        }
        conference_calls.append(call_details)
    
    return conference_calls

if __name__ == "__main__":
    calls = trenddata()
    if calls:
        print("Conference Calls:")
        for call in calls:
            print(f"Text: {call['text']}, Link: {call['link']}")
    else:
        print("No conference calls found.")


#Data to download for Future Trades:
#Input Stock Code 
#https://trendlyne.com/tools/data-downloader/#stock-data-downloader Most important source. Get all data for watchlist stocks and porfolio stocks
#Trendlyne Score,  Valuation and Ratios, Relative Performance, Techicals, Support and Resistance, Forcaster, Forcaster Surprise, shareholding, F&O.
#Get hisotorical PE- Button to download excel next to graph
#News recent 6 months
#Earnings CAll - Recent 6 months
#Corporate annoncement non routine Last 6 months
#Research report AI summary Last 3 months
#Download daily data https://trendlyne.com/share-price/performance/1359/TATACONSUM/tata-consumer-products-ltd/ bottom of the page
#Insider Trading. https://trendlyne.com/equity/insider-trading-sast/all/TATACONSUM/1359/tata-consumer-products-ltd/
#Coporate action. Last 3 months next 3 months

#https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/consensus_highest_bullish-above-0/ Highest bullesimess






