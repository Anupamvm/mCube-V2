import os
import argparse
import csv
import json
from neo_api_client import NeoAPI
import json
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values


#python3 get_quote.py --symbol "Nifty 50" --exchange "nse_cm" --index "True" --login "true"
#python3 get_quote.py --symbol "42948" --exchange "nse_fo" --index "False" --login "true"
#python3 get_quote.py --symbol "11536" --exchange "nse_cm" --index "False" --login "true"

# Set the maximum threads for NumExpr
os.environ["NUMEXPR_MAX_THREADS"] = "8"  # Adjust as needed for your system

# Filepath for the CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "quotes_response.csv")

# Database connection settings
DB_SETTINGS = {
    'dbname': 'mcube',
    'user': 'anupamvm',
    'password': 'Anupamvm1!',
    'host': 'localhost',
    'port': '5432',
}

def save_to_database(quote_data):
    """
    Save the parsed quote data to the PostgreSQL database.
    """
    try:
        # Establish database connection
        connection = psycopg2.connect(**DB_SETTINGS)
        cursor = connection.cursor()

        # Insert query for the r_quote table
        insert_query = """
        INSERT INTO r_quote (
            last_traded_price, last_traded_quantity, lower_circuit_limit, 
            upper_circuit_limit, week_52_high, week_52_low, multiplier, 
            precision, change, net_change_percentage, open_interest, 
            total_traded_value, total_buy_quantity, total_sell_quantity, 
            buy_price, sell_price, buy_quantity, instrument_token, 
            exchange_segment, trading_symbol, request_type, open_price, 
            high_price, low_price, close_price, quote_type, timestamp, 
            prev_day_close, last_traded_time
        )
        VALUES (
            %(last_traded_price)s, %(last_traded_quantity)s, %(lower_circuit_limit)s, 
            %(upper_circuit_limit)s, %(week_52_high)s, %(week_52_low)s, %(multiplier)s, 
            %(precision)s, %(change)s, %(net_change_percentage)s, %(open_interest)s, 
            %(total_traded_value)s, %(total_buy_quantity)s, %(total_sell_quantity)s, 
            %(buy_price)s, %(sell_price)s, %(buy_quantity)s, %(instrument_token)s, 
            %(exchange_segment)s, %(trading_symbol)s, %(request_type)s, %(open_price)s, 
            %(high_price)s, %(low_price)s, %(close_price)s, %(quote_type)s, %(timestamp)s, 
            %(prev_day_close)s, %(last_traded_time)s
        )
        """

        # Execute query with the quote_data dictionary
        cursor.execute(insert_query, quote_data)
        connection.commit()

        print("[INFO]: Quote data inserted successfully.")

    except Exception as e:
        print(f"[ERROR]: Unable to save data to the database: {e}")
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def process_quote_message(message):
    """
    Process the incoming quote message and extract relevant fields to save to the database.
    """
    try:
        # Check if the message is a string; if not, assume it's already a dictionary
        if isinstance(message, str):
            data = json.loads(message)
        elif isinstance(message, dict):
            data = message
        else:
            raise ValueError("Invalid message format. Expected a JSON string or dictionary.")

        # Extract quote details
        quotes = data.get("data", [])
        for quote in quotes:
            # Ensure all NOT NULL fields have default placeholders
            quote_data = {
                "last_traded_price": float(quote.get("last_traded_price", 0)),
                "last_traded_quantity": int(quote.get("last_traded_quantity", 0)),
                "lower_circuit_limit": float(quote.get("lower_circuit_limit", 0)),
                "upper_circuit_limit": float(quote.get("upper_circuit_limit", 0)),
                "week_52_high": float(quote.get("52week_high", 0)),
                "week_52_low": float(quote.get("52week_low", 0)),
                "multiplier": int(quote.get("multiplier", 1)),
                "precision": int(quote.get("precision", 2)),
                "change": float(quote.get("change", 0)),
                "net_change_percentage": float(quote.get("net_change_percentage", 0)),
                "open_interest": int(quote.get("open_interest", 0)),
                "total_traded_value": float(quote.get("total_traded_value", 0)),
                "total_buy_quantity": int(quote.get("total_buy_quantity", 0)),
                "total_sell_quantity": int(quote.get("total_sell_quantity", 0)),
                "buy_price": float(quote.get("buy_price", 0)),
                "sell_price": float(quote.get("sell_price", 0)),
                "buy_quantity": int(quote.get("buy_quantity", 0)),
                "instrument_token": quote.get("instrument_token") or "NULL",
                "exchange_segment": quote.get("exchange_segment") or "NULL",
                "trading_symbol": quote.get("trading_symbol") or quote.get("instrument_token") or "NULL",
                "request_type": quote.get("request_type") or "NULL",
                "open_price": float(quote.get("ohlc", {}).get("open", 0)),
                "high_price": float(quote.get("ohlc", {}).get("high", 0)),
                "low_price": float(quote.get("ohlc", {}).get("low", 0)),
                "close_price": float(quote.get("ohlc", {}).get("close", 0)),
                "quote_type": data.get("type") or "NULL",
                "timestamp": datetime.now(),
                "prev_day_close": float(quote.get("prev_day_close", 0)),
                "last_traded_time": datetime.strptime(
                    quote.get("last_traded_time", datetime.now().isoformat()), "%d/%m/%Y %H:%M:%S"
                ) if quote.get("last_traded_time") else None,
            }

            # Save to the database
            save_to_database(quote_data)

    except Exception as e:
        print(f"[ERROR]: Unable to process quote message: {e}")





def save_to_file(message):
    """
    Save the entire message as JSON into the CSV file.
    """
    try:
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


def save_to_db(message):
    """
    Save the processed message to the database.
    """
    try:
        # Assuming `process_quote_message` is the function that processes and saves to DB
        process_quote_message(message)
        print(f"[Res]: Message saved to the database.")
    except Exception as e:
        print(f"[Error]: Unable to save to the database: {e}")


def on_message(message):
    """
    Handle the incoming message by saving to both file and database.
    """
    # Print the full message
    print('[Res]:', message)

    # Save to file
    save_to_file(message)

    # Save to database
    save_to_db(message)



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
