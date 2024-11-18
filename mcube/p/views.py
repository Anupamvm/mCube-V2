from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from ksneo.ksapi import ks_login, ks_getholdings, ks_updatemaster, ks_logout,ks_quote,ks_search_eq
import pandas as pd
from distutils.util import strtobool



def home(request):
    greeting = "Hello, this is the Portfolio app!"
    urls = [
        {"name": "login", "link": "/p/login", "description": "KS Login"},
        {"name": "holdings", "link": "/p/holdings", "description": "Get and save holdings"},
        {"name": "updatemaster", "link": "/p/master", "description": "Updates and saves all master files"},
        {"name": "getquote", "link": "/p/getquote", "description": "Get Quote"},
        {"name": "getquote", "link": "/p/getindex", "description": "Get Index"},
    ]

    html = f"{greeting}<br><br>"
    for url in urls:
        html += f"{url['name']}: <a href='{url['link']}'>{url['link']}</a> - {url['description']}<br>"
    
    return HttpResponse(html)


# View for login
def login_view(request):
    try:
        ks_login()  # Call the login function
        return HttpResponse("Login successful and client initialized.")
    except Exception as e:
        return HttpResponse(f"Error during login: {e}", status=500)

# View for fetching holdings
def get_holdings_view(request):
    try:
        holdings_data = ks_getholdings()  # Call the getholdings function
        df = pd.DataFrame(holdings_data)
        print(df)
        json_data = df.to_dict(orient="records")

        return JsonResponse(json_data, safe=False)
    except Exception as e:
        return HttpResponse(f"Error fetching holdings: {e}", status=500)
    
def update_master(request):
    try:
        ks_updatemaster()
        return HttpResponse("Masters updated and saved")
    except Exception as e:
        return HttpResponse(f"Error during updating master: {e}", status=500)


def get_quote(request):
    try:
        # Call the ks_quote function with the required parameters
        #Example: http://127.0.0.1:8000/p/getquote?symbol=NIFTY&segment=nse_fo&expiry=29NOV2024&option_type=CE&strike_price=24000&index=True
        #Example: http://127.0.0.1:8000/p/getquote?symbol=TCS&segment=nse_fo&expiry=29NOV2024&option_type=CE&strike_price=4000&index=False
        #Example: http://127.0.0.1:8000/p/getquote?symbol=Nifty%2050&segment=nse_cm&index=True

        symbol = request.GET.get('symbol', 'TCS')  # Default to 'YESBANK'
        index = request.GET.get('index', 'False')  # Default to 'YESBANK'

        segment = request.GET.get('segment', 'nse_cm')  # Default to 'nse_cm' or 'nse_fo'
        expiry = request.GET.get('expiry', '')  # Default to empty
        option_type = request.GET.get('option_type', '')  # Default to empty
        strike_price = request.GET.get('strike_price', '')  # Default to empty

        kscode = symbol
        if(not bool(strtobool(index)) or segment=="nse_fo"):
            kscode = ks_search_eq(
            symbol=symbol, exch_seg=segment,expirydate=expiry,optype=option_type,stkprice=strike_price
        )
        #def ks_quote(token, segment="nse_cm", index="False", login=False):
        ks_quote(kscode, segment,index,login=False)
        return HttpResponse("Quote successfully called.")
    except Exception as e:
        return HttpResponse(f"Error during quote fetch: {e}", status=500)
    
    
def search(request):
    try:
        # Extract parameters from the request's GET query string
        segment = request.GET.get('segment', 'nse_cm')  # Default to 'nse_cm' or 'nse_fo'
        symbol = request.GET.get('symbol', 'TCS')  # Default to 'YESBANK'
        expiry = request.GET.get('expiry', '')  # Default to empty
        option_type = request.GET.get('option_type', '')  # Default to empty
        strike_price = request.GET.get('strike_price', '')  # Default to empty

        # Call the ks_search function with the extracted parameters
        result = ks_search_eq(
            symbol=symbol, exch_seg=segment,expirydate=expiry,optype=option_type,stkprice=strike_price
        )
        # Return the result or a success message
        return HttpResponse(f"Search response: {result}")
    except Exception as e:
        return HttpResponse(f"Error during quote fetch: {e}", status=500)
