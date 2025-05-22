from django.shortcuts import render
from breeze_connect import BreezeConnect

# Create your views here.
from django.http import HttpResponse

def index(request):
    
    # Initialize SDK
    breeze = BreezeConnect(api_key="6561_m2784f16J&R88P3429@66Y89^46")

    # Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
    # Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.
    import urllib
    print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus("6561_m2784f16J&R88P3429@66Y89^46"))

    # Generate Session
    breeze.generate_session(api_secret="l6_(162788u1p629549_)499O158881c",
                            session_token="51234840")

    # Connect to websocket(it will connect to tick-by-tick data server)
    breeze.ws_connect()
    print(breeze.get_funds())
    # Callback to receive ticks.
    quote = breeze.get_quotes(stock_code="NIFTY",
                    exchange_code="NSE",
                    #expiry_date="2025-04-24T06:00:00.000Z",
                    product_type="cash",
                    right="",
                    strike_price="")
    print(quote)
    def on_ticks(ticks):
        print("Ticks: {}".format(ticks))

    # Assign the callbacks.
    breeze.on_ticks = on_ticks

    # ws_disconnect (it will disconnect from all actively connected servers)
    breeze.ws_disconnect()
    return HttpResponse("Hello, Breeze app is working!")
