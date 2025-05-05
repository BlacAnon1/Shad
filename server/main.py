from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from web3 import Web3
import uvicorn
import requests
from python_jose import jwt
from python_fernet import Fernet
from typing import Optional

app = FastAPI()

# Hardcoded Config
MONGO_URL = "mongodb://localhost:27017/neuracoin"
REDIS_URL = "redis://localhost:6379"
TATUM_API_KEY = "your_tatum_api_key"  # Replace with your Tatum key
WIREX_API_KEY = "your_wirex_api_key"  # Replace with your Wirex key
SUMSUB_API_KEY = "your_sumsub_api_key"  # Replace with your Sumsub key
COINGECKO_API = "https://api.coingecko.com/api/v3"
JWT_SECRET = "your_jwt_secret_32_chars"  # Replace with 32-char secret
FERNET_KEY = b"your_fernet_key_32_bytes=="  # Replace with 32-byte key
PAYOUT_WALLET = "0xYourUSDTWalletAddress"  # Replace with your USDT wallet
DOMAIN = "neuracoin.org"

# MongoDB
client = MongoClient(MONGO_URL)
db = client["neuracoin"]

# Fernet Encryption
fernet = Fernet(FERNET_KEY)

# Tatum Mock (Simplified)
class Tatum:
    def __init__(self, api_key): self.api_key = api_key
    def create_wallet(self, coin="ETH"): return {"address": f"0x{hash(coin)}", "key": "private_key"}
    def deposit(self, wallet, amount, coin): return f"tx_{hash(wallet+str(amount))}"
    def send_usdt(self, to, amount): return requests.post("https://api.tatum.io/v3/ledger/transaction", json={"to": to, "amount": amount, "currency": "USDT"}, headers={"x-api-key": self.api_key}).json()

tatum = Tatum(TATUM_API_KEY)

# Wirex Mock
class Wirex:
    def __init__(self, api_key): self.api_key = api_key
    def issue_card(self, user_id, card_type="virtual"): return f"card_{hash(user_id+card_type)}"
    def topup_card(self, card_id, amount): return f"topup_{card_id}_{amount}"

wirex = Wirex(WIREX_API_KEY)

class User(BaseModel):
    email: str
    plan: str = "free"

class TopUp(BaseModel):
    email: str
    amount: float
    coin: str
    to_card: Optional[bool] = False

@app.post("/register")
async def register(user: User):
    if db.users.find_one({"email": user.email}): raise HTTPException(400, "User exists")
    wallet = tatum.create_wallet()
    card = wirex.issue_card(user.email, "virtual") if user.plan != "free" else None
    db.users.insert_one({
        "email": user.email,
        "plan": user.plan,
        "wallet": fernet.encrypt(str(wallet).encode()).decode(),
        "card": card,
        "kyc": False
    })
    token = jwt.encode({"email": user.email}, JWT_SECRET, algorithm="HS256")
    return {"token": token}

@app.post("/topup")
async def topup(data: TopUp):
    user = db.users.find_one({"email": data.email})
    if not user: raise HTTPException(404, "User not found")
    tx = tatum.deposit(user["wallet"], data.amount, data.coin)
    fee = data.amount * 0.01  # 1% top-up fee
    db.transactions.insert_one({"email": data.email, "amount": data.amount, "fee": fee, "coin": data.coin, "tx": tx})
    if data.to_card and user["card"]:
        wirex.topup_card(user["card"], data.amount - fee)
    return {"tx_id": tx}

@app.get("/payout")
async def payout():
    revenue = sum(t["fee"] for t in db.transactions.find())
    if revenue > 0:
        tx = tatum.send_usdt(PAYOUT_WALLET, revenue)
        db.transactions.update_many({}, {"$set": {"paid_out": True}})
        return {"tx_id": tx}
    return {"message": "No revenue"}

@app.get("/prices")
async def prices():
    coins = ["bitcoin", "ethereum", "tether", "solana", "binancecoin", "ripple"]
    data = requests.get(f"{COINGECKO_API}/simple/price?ids={','.join(coins)}&vs_currencies=usd").json()
    return data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
