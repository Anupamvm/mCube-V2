from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, this is the Future app!")


def verifyTrade(request):

    #Stock Related Data
    #Get all data from trendline
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

    #Nifty50 Related Data from Trendlyne
    #Nifty Techincal Data from Trendlyne
    #Gift Nifty
    #OHCL Nifty 50 at 9:15, 9:30, 9:40 from KNeo
    #Last 60 days Nifty 50 data and look at last 5 days, 3 days and get directions
    #https://trendlyne.com/macro-data/fii-dii/latest/snapshot-pastmonth
    


    #Run algorithm to understand the trades
    #Define benchmarks and probability outputs
    #Allow/Disallow trade

    '''
    Algorithm:
        - First check for momentum. Above 200dma, above 20dma, above 100 dma
        - Check returns last 1 week, last 2 weeks last 1 month
        - Check technical analysis for all parameters and over all parameters
        - Check f&O data and open interest data.
        - Check market trend. Last 1 week, 2 week, 3 week
        - Check shareholdings of FII and DII actions
        - Check reports statistics from trendlyine
        - Check PE and historical PE

        - Check industry competition trend. Last 1 week, 2 week, 3 week, 1 month
        - Check news and present. Needs manual clearance.
        - Check for result commentry and present summary. Needs manual clearnace
        - Check for recent reportrs and present summary. Needs manual clearance
        - Corporate action next 30 days and past 30 days
        - Overall nifty trend 1 weekm 2 week,  3week, 1 month
        - Fii and DII inflows in Nifty in general

    '''

    return HttpResponse("Verified trade")