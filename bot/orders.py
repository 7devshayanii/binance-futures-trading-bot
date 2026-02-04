"""
Order placement logic
Handles market and limit orders
"""

from binance.exceptions import BinanceAPIException
import logging

logger = logging.getLogger(__name__)


class OrderManager:
    def __init__(self, client):
        """Initialize with a BinanceClient instance"""
        self.client = client

    def place_market_order(self, symbol, side, quantity):
        """
        Place a market order
        Market orders execute immediately at current price
        """
        logger.info(f"Placing MARKET order: {side} {quantity} {symbol}")
        
        try:
            order = self.client.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            logger.info(f"Market order placed successfully: {order['orderId']}")
            return order
        
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error placing market order: {e}")
            raise

    def place_limit_order(self, symbol, side, quantity, price):
        """
        Place a limit order
        Limit orders only execute at specified price or better
        """
        logger.info(f"Placing LIMIT order: {side} {quantity} {symbol} @ {price}")
        
        try:
            # timeInForce GTC = Good Till Cancel (stays open until filled or cancelled)
            order = self.client.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC',
                quantity=quantity,
                price=price
            )
            logger.info(f"Limit order placed successfully: {order['orderId']}")
            return order
        
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error placing limit order: {e}")
            raise

    def format_order_response(self, order):
        """
        Format order response for clean output
        Makes it easier to read
        """
        output = []
        output.append("\n" + "="*50)
        output.append("ORDER EXECUTED SUCCESSFULLY")
        output.append("="*50)
        output.append(f"Order ID: {order.get('orderId', 'N/A')}")
        output.append(f"Symbol: {order.get('symbol', 'N/A')}")
        output.append(f"Side: {order.get('side', 'N/A')}")
        output.append(f"Type: {order.get('type', 'N/A')}")
        output.append(f"Status: {order.get('status', 'N/A')}")
        output.append(f"Quantity: {order.get('origQty', 'N/A')}")
        
        if 'executedQty' in order:
            output.append(f"Executed Qty: {order['executedQty']}")
        
        if 'avgPrice' in order and order['avgPrice'] != '0':
            output.append(f"Average Price: {order['avgPrice']}")
        elif 'price' in order:
            output.append(f"Limit Price: {order['price']}")
            
        output.append("="*50 + "\n")
        
        return "\n".join(output)
