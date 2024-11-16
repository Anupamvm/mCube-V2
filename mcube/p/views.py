from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from ksneo.ksapi import login, getholdings 
import pandas as pd


def home(request):
    greeting = "Hello, this is the Portfolio app!"
    urls = [
        {"name": "login", "link": "/login", "description": "KS Login"},
        {"name": "holdings", "link": "/holdings", "description": "Get and save holdings"},
    ]

    html = f"{greeting}<br><br>"
    for url in urls:
        html += f"{url['name']}: <a href='{url['link']}'>{url['link']}</a> - {url['description']}<br>"
    
    return HttpResponse(html)


# View for login
def login_view(request):
    try:
        login()  # Call the login function
        return HttpResponse("Login successful and client initialized.")
    except Exception as e:
        return HttpResponse(f"Error during login: {e}", status=500)

# View for fetching holdings
def get_holdings_view(request):
    try:
        holdings_data = getholdings()  # Call the getholdings function
        df = pd.DataFrame(holdings_data)
        print(df)
        json_data = df.to_dict(orient="records")

        return JsonResponse(json_data, safe=False)
    except Exception as e:
        return HttpResponse(f"Error fetching holdings: {e}", status=500)
