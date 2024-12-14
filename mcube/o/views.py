from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, this is the Options app!")


def getNiftyShortStrangle(request):

    #Nifty50 Related Data from Trendlyne
    #Nifty Techincal Data from Trendlyne
    #OHCL Nifty 50 at 9:15, 9:30, 9:40 from KNeo
    #Last 60 days Nifty 50 data and look at last 5 days, 3 days and get directions
    #https://trendlyne.com/macro-data/fii-dii/latest/snapshot-pastmonth
    '''
    My alogrithm for options selling
    
    If any position is open dont trade
    
    If detta last 3 day trades is greater than 1% on a single day dont trade
    If delta from last 5 days is greater than 2% dont trade
    If global major markets delta is greater than 1.5% dont trade

    Get OCHL at 9:15, 9:30, 9:40
    If delta from previous day close to today open is greater than 0.5% dont trade
    If delta first 15 mins greater than 0.5 points dont trade
    If delta first 25 mins greater than 0.4 points dont trade

    Get spot price
    Calculate delta:
        - # of days to expiry *DailyDelta
        - AvgDailyDelta = Avg daily delta last 20 days * 1.5
        - Daily delta calcuation= Tradablerating depending on open. 1-4 and range accordingly. 
        - If AvgDailtyDelta > DailyDelta. Increase daily delta
        - Adjust delta for major event
        - Adjust delta for vix. 11-13. More than 13 one strike for each 0.5 point
        - Adjust for support and Resistance (Only call/put accordingly)
        - Check for 20dma, 100dma, 200dma levels
        - Adjust for psychological support and Resistance- For eg. 24200, 24000,24500,23800(Only call/put accordingly)
        - Adjust techical Analysis strike price in the direction(Only call/put accordingly)
        - Adjust for live price of option lot. (Only call/put/both accordingly)

    Calulate position size
        - Get margin
        - Get per lot margin
        - Place order for 50% of margin

    ''' 
    
    return HttpResponse ("Stort strange initiated")