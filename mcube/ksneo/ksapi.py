import neo_api_client
from neo_api_client import NeoAPI
import pandas as pd
from django.conf import settings
from p.models import Holding
import logging

logger = logging.getLogger(__name__)

client = None

def on_message(message):
    logger.info(f"Message: {message}")

def on_error(error_message):
    logger.error(f"Error: {error_message}")

def on_close(message):
    logger.info(f"Connection closed: {message}")

def on_open(message):
    logger.info(f"Connection opened: {message}")

def login():
    global client
    try:
        client = NeoAPI(
            consumer_key=settings.KSNEO.get("CONSUMER_KEY"),
            consumer_secret=settings.KSNEO.get("CONSUMER_SECRET"),
            environment='prod'
        )
        client.login(
            pan=settings.KSNEO.get("PAN"),
            password=settings.KSNEO.get("PASSWORD")
        )
        client.session_2fa(OTP=settings.KSNEO.get("MPIN"))

        client.on_message = on_message
        client.on_error = on_error
        client.on_close = on_close
        client.on_open = on_open
        logger.info("Login successful and client initialized.")
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise

def logout():
    client.logout()

def verifylogin():
    if client is None:
        raise Exception("Client is not initialized. Please login first.")
    return True

from p.models import Holding
import logging

logger = logging.getLogger(__name__)

from datetime import datetime
from p.models import Holding
import logging

logger = logging.getLogger(__name__)

def parse_date(date_string):
    """
    Parse a date string in the format '26-DEC-2024' to 'YYYY-MM-DD'.
    """
    try:
        return datetime.strptime(date_string, "%d-%b-%Y").date()
    except (ValueError, TypeError):
        # Return None if the date is invalid or not provided
        return None

from datetime import datetime
from p.models import Holding
import logging

logger = logging.getLogger(__name__)

def parse_date(date_string):
    """
    Parse a date string in the format '26-DEC-2024' to 'YYYY-MM-DD'.
    """
    try:
        return datetime.strptime(date_string, "%d-%b-%Y").date()
    except (ValueError, TypeError):
        # Return None if the date is invalid or not provided
        return None

def getholdings():
    global client
    verifylogin()
    try:
        # Fetch holdings data
        holdings_response = client.holdings()
        
        # Delete all existing records in the Holding table
        Holding.objects.all().delete()
        logger.info("All existing holdings have been deleted.")
        
        # Extract the 'data' key
        holdings_data = holdings_response.get("data", [])
        
        if not holdings_data:
            logger.info("No holdings data found.")
            return

        # Save each holding to the database
        for holding in holdings_data:
            # Set display_symbol to symbol if display_symbol is None
            display_symbol = holding.get("displaySymbol") or holding.get("symbol")
            print(display_symbol)
            # Save the holding
            Holding.objects.create(
                display_symbol=display_symbol,
                average_price=holding.get("averagePrice"),
                quantity=holding.get("quantity"),
                exchange_segment=holding.get("exchangeSegment"),
                exchange_identifier=holding.get("exchangeIdentifier"),
                holding_cost=holding.get("holdingCost"),
                market_value=holding.get("mktValue"),
                scrip_id=holding.get("scripId"),
                instrument_token=holding.get("instrumentToken"),
                instrument_type=holding.get("instrumentType"),
                is_alternate_scrip=holding.get("isAlternateScrip"),
                closing_price=holding.get("closingPrice"),
                symbol=holding.get("symbol"),
                sellable_quantity=holding.get("sellableQuantity"),
                expiry_date=parse_date(holding.get("expiryDate")),
                strike_price=holding.get("strikePrice"),
                opt_type=holding.get("optType"),
            )
        logger.info("All holdings have been saved successfully.")
        return holdings_data

    except Exception as e:
        logger.error(f"Error fetching or saving holdings: {e}")
        raise




#logout - return status
#savequote - Async call
#placeorder - reuturn status
#getpositions - return live positions 
#updateholding - Update db - holding
#updatewatchlist - Update db - watchlist
#searchscript - return script token
#updatescriptmasters - Update files

