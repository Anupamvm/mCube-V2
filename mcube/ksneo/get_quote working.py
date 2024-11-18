import os
import argparse
import csv
import json
from neo_api_client import NeoAPI

# Set the maximum threads for NumExpr
os.environ["NUMEXPR_MAX_THREADS"] = "8"  # Adjust as needed for your system

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

def main(symbol, exchange, index, login, session_token, sid, server_id):
    try:
        if login.lower() == "true":
            # Perform login-based quote retrieval
            client = NeoAPI(
                consumer_key="NkmJfGnAehLpdDm3wSPFR7iCMj4a",
                consumer_secret="H8Q60_oBa2PkSOBJXnk7zbOvGqUa",
                environment='prod'
            )
            client.login(pan="AAQHA1835B", password="Anupamvm2@")
            client.session_2fa(OTP="284321")

            client.on_message = on_message
            client.on_error = on_error
        else:
            # Use session-based quote retrieval
            client = NeoAPI(
                consumer_key="NkmJfGnAehLpdDm3wSPFR7iCMj4a",
                consumer_secret="H8Q60_oBa2PkSOBJXnk7zbOvGqUa",
                environment='prod',
                access_token=session_token
            )
            client.on_message = on_message
            client.on_error = on_error

        # Define instrument tokens dynamically
        inst_tokens = [{"instrument_token": symbol, "exchange_segment": exchange}]

        # Fetch quotes
        client.quotes(
            instrument_tokens=inst_tokens,
            quote_type="",
            isIndex=index.lower() == "true",
            session_token=session_token,
            sid=sid,
            server_id=server_id
        )
    except Exception as e:
        print(f"Exception during quote retrieval: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch market data for a symbol.")
    parser.add_argument("--symbol", type=str, required=True, help="Instrument token or symbol name")
    parser.add_argument("--exchange", type=str, required=True, help="Exchange segment (e.g., nse_cm)")
    parser.add_argument("--index", type=str, required=True, help="Specify whether the symbol is an index (true/false)")
    parser.add_argument("--login", type=str, required=True, help="Specify whether to login (true/false)")
    parser.add_argument("--session_token", type=str, help="Session token (required if login is false)")
    parser.add_argument("--sid", type=str, help="SID (required if login is false)")
    parser.add_argument("--server_id", type=str, help="Server ID (required if login is false)")
    args = parser.parse_args()

    main(
        symbol=args.symbol,
        exchange=args.exchange,
        index=args.index,
        login=args.login,
        session_token=args.session_token,
        sid=args.sid,
        server_id=args.server_id
    )
