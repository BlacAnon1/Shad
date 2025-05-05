import requests

class TatumAPI:
    def __init__(self, api_key): self.api_key = api_key
    def get_balance(self, address, coin): return requests.get(f"https://api.tatum.io/v3/{coin}/address/{address}/balance", headers={"x-api-key": self.api_key}).json()

tatum = TatumAPI("your_tatum_api_key")  # Replace with your Tatum key
