from django.db import models
from cryptography.fernet import Fernet
from hashlib import sha256
import base64


class Wallet(models.Model):
    private_key_hash = models.BinaryField(max_length=64)
    public_key = models.CharField(max_length=128)

    encrypted_private_key = models.BinaryField(null=True, blank=True)

    # exposed function

    def create_simple_password(self, password: str, private_key: str):
        if self.validate_private_key(private_key.encode()):
            f = Fernet(self.encode_passowrd(password))
            self.encrypted_private_key = f.encrypt(private_key.encode())
            self.save()
        else:
            raise Exception(
                f"current: {self.private_key_hash.hex()}, got:{sha256(private_key.encode()).digest().hex()}"
            )

    def get_private_key(self, password: str):
        """retreives private key from simple password. should decode it"""
        f = Fernet(self.encode_passowrd(password))
        private_key = f.decrypt(bytes(self.encrypted_private_key))
        return private_key

    def validate_private_key(self, private_key: bytes):
        hash = sha256(private_key).digest()
        return hash.hex() == self.private_key_hash.hex()

    # util function

    def encode_passowrd(self, password: str):
        encoded_bytes = base64.urlsafe_b64encode(password.rjust(32, "0").encode())
        return encoded_bytes.decode()
