"""
Input validation functions
Keeps the main code clean
"""

import logging

logger = logging.getLogger(__name__)


def validate_symbol(symbol):
    """Check if symbol format is valid"""
    if not symbol:
        raise ValueError("Symbol cannot be empty")
    
    # Basic format check - should be uppercase and end with USDT for futures
    symbol = symbol.upper()
    if not symbol.endswith('USDT'):
        logger.warning(f"Symbol {symbol} doesn't end with USDT - might not work on USDT-M futures")
    
    return symbol


def validate_side(side):
    """Validate order side"""
    side = side.upper()
    if side not in ['BUY', 'SELL']:
        raise ValueError(f"Invalid side: {side}. Must be BUY or SELL")
    return side


def validate_order_type(order_type):
    """Validate order type"""
    order_type = order_type.upper()
    if order_type not in ['MARKET', 'LIMIT']:
        raise ValueError(f"Invalid order type: {order_type}. Must be MARKET or LIMIT")
    return order_type


def validate_quantity(quantity):
    """Validate quantity is positive"""
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        return qty
    except (ValueError, TypeError):
        raise ValueError(f"Invalid quantity: {quantity}")


def validate_price(price, order_type):
    """Validate price (required for LIMIT orders)"""
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
