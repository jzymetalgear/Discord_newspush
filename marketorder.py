import alpaca_trade_api as tradeapi
import requests
import config

# Access Alpaca API credentials
APCA_API_KEY_ID = config.APCA_API_KEY_ID
APCA_API_SECRET_KEY = config.APCA_API_SECRET_KEY
APCA_API_BASE_URL = config.APCA_API_BASE_URL  # Replace with the Alpaca V2 API base URL

# Access Telegram bot credentials
TELEGRAM_BOT_TOKEN = config.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID = config.TELEGRAM_CHAT_ID

# Initialize Alpaca API with V2 version
api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL, api_version='v2')

# Function to send a message via Telegram bot
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send Telegram message: {response.text}")

# Function to place a limit order and send a Telegram message
def place_limit_order(symbol, quantity, side, limit_price):
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=quantity,
            side=side,
            type='limit',
            time_in_force='gtc',
            limit_price=str(limit_price)
        )
        message = f"Limit order for {quantity} shares of {symbol} placed successfully at limit price ${limit_price}."
        print(message)
        send_telegram_message(message)
    except Exception as e:
        message = f"Failed to place limit order for {quantity} shares of {symbol}: {str(e)}"
        print(message)
        send_telegram_message(message)

# Example usage: Place a limit order to buy 10 shares of AAPL with a limit price of $180
place_limit_order('AAPL', 10, 'buy', 180.0)
