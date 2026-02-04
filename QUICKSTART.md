# Quick Start Guide

## 1️⃣ Get Your API Keys

1. Visit https://testnet.binancefuture.com
2. Sign up / Log in
3. Click on "API Key" in the top right
4. Generate new API key - save both the key and secret!

## 2️⃣ Install

```bash
cd trading_bot
pip install -r requirements.txt
```

## 3️⃣ Set Your Credentials

**Option A: Environment Variables (Recommended)**
```bash
export BINANCE_API_KEY='your_key_here'
export BINANCE_API_SECRET='your_secret_here'
```

**Option B: Pass in command**
```bash
python cli.py --api-key YOUR_KEY --api-secret YOUR_SECRET [other args...]
```

## 4️⃣ Run Your First Trade

**Market Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Limit Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 95000
```

## 5️⃣ Check Logs

Logs are saved in the `logs/` folder with timestamps.

---

## Common First-Time Issues

**"Insufficient balance"**
→ Get testnet USDT from the faucet on testnet.binancefuture.com

**"Invalid API key"**  
→ Make sure you're using TESTNET keys, not mainnet

**"Module not found"**
→ Run `pip install -r requirements.txt`

---

That's it! You're ready to go. Check the full README.md for more examples.
