"""
Binance Futures client wrapper
Handles connection and basic API calls
"""

from binance.client import Client
from binance.exceptions import BinanceAPIException
import logging

logger = logging.getLogger(__name__)


class BinanceClient:
    def __init__(self, api_key, api_secret):
        """Initialize Binance Futures client for testnet"""
        try:
            self.client = Client(api_key, api_secret, testnet=True)
            # Set to futures URL
            self.client.API_URL = 'https://testnet.binancefuture.com'
            logger.info("Connected to Binance Futures Testnet")
        except Exception as e:
            logger.error(f"Failed to initialize client: {e}")
            raise

    def get_account_info(self):
        """Get account balance and info - useful for testing connection"""
        try:
            return self.client.futures_account()
        except BinanceAPIException as e:
            logger.error(f"API Error getting account info: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting account info: {e}")
            raise

    def get_symbol_info(self, symbol):
        """Get trading rules for a symbol"""
        try:
            info = self.client.futures_exchange_info()
            for s in info['symbols']:
                if s['symbol'] == symbol:
                    return s
            return None
        except Exception as e:
            logger.error(f"Error getting symbol info: {e}")
            return None


class MockBinanceClient:
    """Mock client for dry-run/testing without contacting Binance"""

    def __init__(self):
        # OrderManager expects an object where .client.futures_create_order(...) exists
        # We'll set .client to self and implement the minimal methods used by the code.
        self.client = self

    def futures_create_order(self, **kwargs):
        # Return a synthetic order response that resembles Binance futures API
        import time
        order_type = kwargs.get('type')
        qty = kwargs.get('quantity')
        price = kwargs.get('price')
        executed = str(qty) if order_type == 'MARKET' else '0'
        avg_price = '100' if order_type == 'MARKET' else '0'

        return {
            'orderId': int(time.time()),
            'symbol': kwargs.get('symbol'),
            'side': kwargs.get('side'),
            'type': order_type,
            'status': 'FILLED' if order_type == 'MARKET' else 'NEW',
            'origQty': str(qty),
            'executedQty': executed,
            'price': str(price) if price is not None else '0',
            'avgPrice': avg_price
        }

    def futures_account(self):
        return {'assets': []}

    def futures_exchange_info(self):
        return {'symbols': []}
