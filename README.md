# Binance Futures Trading Bot

A simple Python trading bot for placing orders on Binance Futures Testnet (USDT-M). Built for learning and testing trading strategies in a safe environment.

## Features

- ✅ Place MARKET and LIMIT orders
- ✅ Support for BUY and SELL sides
- ✅ Clean CLI interface with validation
- ✅ Comprehensive logging to files
- ✅ Proper error handling
- ✅ Works on Binance Futures Testnet

## Setup

### 1. Get Testnet Credentials

1. Go to [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Register/login with your email
3. Generate API Key and Secret from the dashboard

### 2. Install Dependencies

```bash
# Clone or download this repo
cd trading_bot

# Install required packages
pip install -r requirements.txt
```

### 3. Set Environment Variables

The easiest way is to set your API credentials as environment variables:

```bash
export BINANCE_API_KEY='your_testnet_api_key_here'
export BINANCE_API_SECRET='your_testnet_api_secret_here'
```

Alternatively, you can pass them directly via command line (see examples below).

## How to Run

### Basic Command Structure

```bash
python cli.py --symbol SYMBOL --side SIDE --type TYPE --quantity QTY [--price PRICE]
```

### Examples

**Market Order (Buy)**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Market Order (Sell)**
```bash
python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.01
```

**Limit Order (Buy)**
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 95000
```

**Limit Order (Sell)**
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3500
```

**With API credentials in command**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 \
  --api-key YOUR_KEY --api-secret YOUR_SECRET
```

## Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--symbol` | Yes | Trading pair symbol | BTCUSDT, ETHUSDT |
| `--side` | Yes | Order side | BUY or SELL |
| `--type` | Yes | Order type | MARKET or LIMIT |
| `--quantity` | Yes | Amount to trade | 0.001 |
| `--price` | For LIMIT | Price for limit orders | 95000 |
| `--api-key` | Optional | API key (or use env var) | - |
| `--api-secret` | Optional | API secret (or use env var) | - |

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py          # Package initialization
│   ├── client.py            # Binance API client wrapper
│   ├── orders.py            # Order placement logic
│   ├── validators.py        # Input validation
│   └── logging_config.py    # Logging setup
├── cli.py                   # Command-line interface
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── logs/                   # Log files (created automatically)
```

## Logging

All operations are logged to both:
- Console output (for immediate feedback)
- Log files in `logs/` directory (for review)

Log files are named with timestamps: `trading_bot_YYYYMMDD_HHMMSS.log`

Each log contains:
- Connection attempts
- Order requests
- API responses
- Errors and exceptions

## Error Handling

The bot handles various error scenarios:

- ❌ Missing or invalid API credentials
- ❌ Invalid symbol formats
- ❌ Invalid side (must be BUY/SELL)
- ❌ Invalid order type (must be MARKET/LIMIT)
- ❌ Missing price for LIMIT orders
- ❌ Negative or zero quantities/prices
- ❌ Binance API errors (insufficient balance, etc.)
- ❌ Network failures

## Assumptions & Notes

1. **Testnet Only**: This bot is configured for Binance Futures Testnet only
2. **USDT-M Futures**: Works with USDT-margined futures contracts
3. **Time in Force**: Limit orders use GTC (Good Till Cancel) by default
4. **No leverage setting**: Uses account default leverage
5. **Minimum quantities**: Check Binance rules for minimum order sizes per symbol

## Common Issues

**"Invalid API key"**
- Make sure you're using Testnet API credentials, not mainnet
- Check that credentials are correctly copied

**"Insufficient balance"**
- Get testnet funds from the Binance Futures Testnet dashboard
- Check your testnet wallet balance

**"Invalid symbol"**
- Use uppercase (BTCUSDT not btcusdt)
- Check the symbol exists on Futures Testnet

## Testing Checklist

- [x] Market BUY order
- [x] Market SELL order  
- [x] Limit BUY order
- [x] Limit SELL order
- [x] Error handling for missing price on LIMIT
- [x] Input validation
- [x] Logging to files

## Dependencies

- `python-binance==1.0.19` - Official Binance API wrapper

## Safety Notes

⚠️ This is for TESTNET only - no real money involved
⚠️ Never commit API keys to git
⚠️ Always test on testnet before using any strategy on mainnet

## Next Steps

Want to enhance this bot? Consider adding:
- Order cancellation
- Position tracking
- Stop-loss orders
- Better CLI with interactive prompts
- Configuration file support
- Multiple order types (OCO, trailing stop, etc.)

---

Built as a learning project for algorithmic trading basics.
