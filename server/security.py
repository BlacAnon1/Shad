from python_fernet import Fernet

class VoidCipher:
    def __init__(self, key): self.fernet = Fernet(key)
    def encrypt(self, data: str): return self.fernet.encrypt(data.encode()).decode()
    def decrypt(self, data: str): return self.fernet.decrypt(data.encode()).decode()

cipher = VoidCipher(b"your_fernet_key_32_bytes==")  # Replace with 32-byte key
