#!/usr/bin/env python3
import argparse
import sys
import logging


# Local lightweight validators and logging setup to avoid importing the package
# which may depend on optional external libraries (kept minimal for CLI use)

def setup_logging():
    import logging
    import os
    from datetime import datetime
    if not os.path.exists('logs'):
        os.makedirs('logs')
    log_filename = f"logs/trading_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_filename}")
    return log_filename


def validate_symbol(symbol):
    if not symbol:
        raise ValueError("Symbol cannot be empty")
    symbol = symbol.upper()
    if not symbol.endswith('USDT'):
        logging.getLogger(__name__).warning(f"Symbol {symbol} doesn't end with USDT - might not work on USDT-M futures")
    return symbol


def validate_side(side):
    side = side.upper()
    if side not in ['BUY', 'SELL']:
        raise ValueError(f"Invalid side: {side}. Must be BUY or SELL")
    return side


def validate_order_type(order_type):
    order_type = order_type.upper()
    if order_type not in ['MARKET', 'LIMIT']:
        raise ValueError(f"Invalid order type: {order_type}. Must be MARKET or LIMIT")
    return order_type


def validate_quantity(quantity):
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        return qty
    except (ValueError, TypeError):
        raise ValueError(f"Invalid quantity: {quantity}")


def validate_price(price, order_type):
    if order_type == 'LIMIT':
        if price is None:
            raise ValueError("Price is required for LIMIT orders")
        try:
            p = float(price)
            if p <= 0:
                raise ValueError("Price must be positive")
            return p
        except (ValueError, TypeError):
            raise ValueError(f"Invalid price: {price}")
    return None if price is None else float(price)

logger = logging.getLogger(__name__)


def _format_price(p):
    if isinstance(p, float) and p.is_integer():
        return str(int(p))
    return str(p)


def print_order_summary(symbol, side, order_type, quantity, price=None):
    print("\n" + "="*50)
    print("ORDER REQUEST SUMMARY")
    print("="*50)
    print(f"Symbol: {symbol}")
    print(f"Side: {side}")
    print(f"Type: {order_type}")
    print(f"Quantity: {quantity}")
    if price is not None:
        print(f"Price: {_format_price(price)}")
    print("="*50 + "\n")


def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(
        description='Binance Futures Trading Bot - Place orders on testnet',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Place a market buy order
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
  
  # Place a limit sell order
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3000
        """
    )
    
    # Required arguments
    parser.add_argument('--symbol', required=True, help='Trading pair (e.g., BTCUSDT)')
    parser.add_argument('--side', required=True, choices=['BUY', 'SELL', 'buy', 'sell'],
                        help='Order side')
    parser.add_argument('--type', required=True, choices=['MARKET', 'LIMIT', 'market', 'limit'],
                        help='Order type', dest='order_type')
    parser.add_argument('--quantity', required=True, type=float, help='Order quantity')
    
    # Optional arguments
    parser.add_argument('--price', type=float, help='Limit price (required for LIMIT orders)')
    parser.add_argument('--api-key', help='Binance API key (or set BINANCE_API_KEY env var)')
    parser.add_argument('--api-secret', help='Binance API secret (or set BINANCE_API_SECRET env var)')
    parser.add_argument('--dry-run', action='store_true', help='Simulate order without contacting Binance')
    
    args = parser.parse_args()
    
    dry_run = args.dry_run

    import os
    api_key = args.api_key or os.getenv('BINANCE_API_KEY')
    api_secret = args.api_secret or os.getenv('BINANCE_API_SECRET')
    
    if not dry_run and (not api_key or not api_secret):
        print("\n❌ ERROR: API credentials not found!")
        print("Either provide --api-key and --api-secret, or set environment variables:")
        print("  export BINANCE_API_KEY='your_key'")
        print("  export BINANCE_API_SECRET='your_secret'\n")
        sys.exit(1)
    
    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, order_type)
        
        print_order_summary(symbol, side, order_type, quantity, price)
        
        logger.info("Initializing Binance client...")
        if dry_run:
            logger.info("Dry-run mode enabled")
            class _LocalMockClient:
                def futures_create_order(self, **kwargs):
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
            class _LocalOrderManager:
                def __init__(self, client):
                    self.client = client
                def place_market_order(self, symbol, side, quantity):
                    return self.client.futures_create_order(symbol=symbol, side=side, type='MARKET', quantity=quantity)
                def place_limit_order(self, symbol, side, quantity, price):
                    return self.client.futures_create_order(symbol=symbol, side=side, type='LIMIT', timeInForce='GTC', quantity=quantity, price=price)
                def format_order_response(self, order):
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
            client = _LocalMockClient()
            order_mgr = _LocalOrderManager(client)
        else:
            from bot import BinanceClient, OrderManager
            client = BinanceClient(api_key, api_secret)
            order_mgr = OrderManager(client)
        
        # Place the order
        if order_type == 'MARKET':
            order = order_mgr.place_market_order(symbol, side, quantity)
        else:
            order = order_mgr.place_limit_order(symbol, side, quantity, price)
        
        formatted_output = order_mgr.format_order_response(order)
        print(formatted_output)
        
        logger.info("Order completed successfully")
        
    except ValueError as e:
        print(f"\n❌ VALIDATION ERROR: {e}\n")
        logger.error(f"Validation error: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        logger.error(f"Failed to place order: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
