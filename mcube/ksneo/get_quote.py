import os
import argparse
import csv
import json
from neo_api_client import NeoAPI

# Set the maximum threads for NumExpr
os.environ["NUMEXPR_MAX_THREADS"] = "8"  # Adjust as needed for your system

# Assigning each key from the KSNEO dictionary to a separate variable
CONSUMER_KEY = "NkmJfGnAehLpdDm3wSPFR7iCMj4a"
CONSUMER_SECRET = "H8Q60_oBa2PkSOBJXnk7zbOvGqUa"
USERNAME = "CLIENT46778"
PASSWORD = "Anupamvm2@"
PAN = "AAQHA1835B"
MPIN = "284321"

# Filepath for the CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "quotes_response.csv")

def on_message(message):
    # Print the full message
    print('[Res]:', message)

    try:
        # Write the entire message as JSON into the CSV
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write headers only if the file is empty
            if file.tell() == 0:
                writer.writerow(["response"])  # Single column for JSON strings

            # Write the JSON string
            writer.writerow([json.dumps(message)])

        print(f"[Res]: Full response dumped to {CSV_FILE}")
    except Exception as e:
        print(f"[Error]: Unable to write to CSV file: {e}")

def on_error(message):
    print('[OnError]:', message)

def str_to_bool(value):
    """Convert a string to boolean."""
    if value.lower() in {'true', '1', 'yes', 'y'}:
        return True
    elif value.lower() in {'false', '0', 'no', 'n'}:
        return False
    else:
        raise argparse.ArgumentTypeError(f"Invalid boolean value: {value}")

def main(symbol, exchange, index="false"):
    index = str_to_bool(index)  # Convert the index value to a boolean
    client = NeoAPI(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        environment='prod'
    )
    client.login(
        pan=PAN,
        password=PASSWORD
    )
    client.session_2fa(OTP=MPIN)

    # Setup Callbacks for websocket events (Optional)
    client.on_message = on_message
    client.on_error = on_error

    # Define instrument tokens dynamically
    inst_tokens = [{"instrument_token": symbol, "exchange_segment": exchange}]

    try:
        # Fetch quotes
        client.quotes(instrument_tokens=inst_tokens, quote_type="", isIndex=index)
        client.logout()
    except Exception as e:
        print("Exception when calling get Quote api->quotes: %s\n" % e)
        client.logout()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch market data for a symbol.")
    parser.add_argument("--symbol", type=str, required=True, help="Instrument token of the symbol")
    parser.add_argument("--exchange", type=str, required=True, help="Exchange segment for the symbol")
    parser.add_argument("--index", type=str, required=True, help="Specify whether the symbol is an index (e.g., true/false)")
    args = parser.parse_args()

    main(symbol=args.symbol, exchange=args.exchange, index=args.index)
