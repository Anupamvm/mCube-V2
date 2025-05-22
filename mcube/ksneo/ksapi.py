import neo_api_client
from neo_api_client import NeoAPI
import pandas as pd
from django.conf import settings
from p.models import Holding
import logging
import os
import requests
import shutil
from datetime import datetime
import subprocess


logger = logging.getLogger(__name__)

# Global client instance
client = None
session_token = None
sid = None
server_id = None

# Callbacks
def on_message(message):
    logger.info(f"Message received: {message}")
    print('[Res]:', message)

def on_error(error_message):
    logger.error(f"Error occurred: {error_message}")
    print('[Error]:', error_message)

def on_close(message):
    logger.info(f"Connection closed: {message}")

def on_open(message):
    logger.info(f"Connection opened: {message}")

# Login function
def ks_login():
    
    global client
    global session_token
    global sid 
    global server_id
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
        session = client.session_2fa(OTP=settings.KSNEO.get("MPIN"))

        session_token = session.get("data", {}).get("token", "")
        sid = session.get("data", {}).get("sid", "")
        server_id = session.get("data", {}).get("hsServerId", "")

        # Attach callbacks
        client.on_message = on_message
        client.on_error = on_error
        client.on_close = on_close
        client.on_open = on_open

        logger.info("Login successful and client initialized.")
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise

# Logout function
def ks_logout():
    global client
    try:
        if client:
            client.logout()
            logger.info("Logout successful.")
        else:
            logger.warning("Client not initialized.")
    except Exception as e:
        logger.error(f"Error during logout: {e}")

# Verify login
def verifylogin():
    if client is None:
        raise Exception("Client is not initialized. Please login first.")
    return True

# Parse date utility
def parse_date(date_string):
    try:
        return datetime.strptime(date_string, "%d-%b-%Y").date()
    except (ValueError, TypeError):
        return None

# Fetch holdings and update database
def ks_getholdings():
    global client
    verifylogin()
    try:
        holdings_response = client.holdings()
        Holding.objects.all().delete()
        logger.info("All existing holdings have been deleted.")

        holdings_data = holdings_response.get("data", [])
        if not holdings_data:
            logger.info("No holdings data found.")
            return

        for holding in holdings_data:
            display_symbol = holding.get("displaySymbol") or holding.get("symbol")
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

# Update script master
def ks_updatemaster():
    verifylogin()
    scriptdata = client.scrip_master()
    files_paths = scriptdata.get('filesPaths', [])
    base_folder = scriptdata.get('baseFolder', '')

    target_folder = os.path.join("mcube", "ksneo", "ks_master")
    os.makedirs(target_folder, exist_ok=True)
    shutil.rmtree(target_folder)
    os.makedirs(target_folder)

    for file_path in files_paths:
        file_url = f"{base_folder}/{file_path}" if not file_path.startswith('http') else file_path
        try:
            response = requests.get(file_url, stream=True)
            response.raise_for_status()
            file_name = os.path.basename(file_url)
            file_save_path = os.path.join(target_folder, file_name)
            with open(file_save_path, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
            logger.info(f"Downloaded: {file_name}")
        except requests.RequestException as e:
            logger.error(f"Failed to download {file_url}: {e}")

    logger.info(f"All files have been saved in the '{target_folder}' folder.")

def ks_search_eq(symbol="TCS", exch_seg="nse_cm",expirydate="",optype="",stkprice=""):
    verifylogin()
    try:
        # Perform search
        search = client.search_scrip(
            exchange_segment=exch_seg, symbol=symbol, expiry=expirydate, option_type=optype, strike_price=stkprice
        )
        logger.info(f"Raw search result: {search}")

        # Convert to DataFrame
        df = pd.DataFrame(search if isinstance(search, list) else [search])

        # Add conditional filtering logic
        if exch_seg == "nse_cm":
            # For NSE Cash Market, validate trading symbol as '{symbol}-EQ'
            filtered = df[
                (df['pGroup'] == 'EQ') &
                (df['pTrdSymbol'] == f"{symbol}-EQ")
            ]
        else:
            # For other segments, filter only by 'EQ' group
            filtered = df.iloc[:1]


        # Check for results and return
        if not filtered.empty:
            return filtered.iloc[0]['pSymbol']  # Return the first match

        raise ValueError(f"No matching EQ symbol found for {symbol} in {exch_seg}")
    except Exception as e:
        logger.error(f"Error during search: {e}")
        raise



# Fetch quotes with callbacks
def ks_quote(token, segment="nse_cm", index="False", login=False):
    global client
    global session_token
    global sid 
    global server_id
    try:
        # Get the absolute path to get_quote.py in the ksneo folder
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current file's directory
        script_path = os.path.join(base_dir, "get_quote.py")

        # Check if the file exists
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"get_quote.py not found at {script_path}")

        # Prepare the command
        cmd = [
            "python3", script_path, "--symbol", str(token), "--exchange", segment, "--index", index, "--login", str(login).lower()
        ]

        # If not logging in, add session details
        if not (session_token.strip() and sid.strip() and server_id.strip()):
            print("********************************")
            print(session_token)
            print(sid)
            print(server_id)
            raise ValueError("Missing session_token, sid, or server_id for quote retrieval without login.")
        cmd.extend(["--session_token", session_token, "--sid", sid, "--server_id", server_id])

        # Run the script as a subprocess
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Log the output and error streams
        if result.returncode == 0:
            logger.info(f"Subprocess output: {result.stdout}")
        else:
            logger.error(f"Subprocess error: {result.stderr}")
            raise Exception(f"Subprocess failed: {result.stderr}")
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error when calling get Quote API: {e}")
        raise


#logout - return status
#savequote - Async call
#placeorder - reuturn status
#getpositions - return live positions 
#updateholding - Update db - holding
#updatewatchlist - Update db - watchlist
#searchscript - return script token
#updatescriptmasters - Update files

