from django.db import models
from cryptography.fernet import Fernet
from hashlib import sha256


class Wallet(models.Model):
    private_key_hash = models.BinaryField(max_length=64)
    public_key = models.CharField(max_length=128)

    encrypted_private_key = models.BinaryField(null=True, blank=True)

    def check_simple_password(self, password):
        f = Fernet(password)
        private_key = f.decrypt(self.encrypted_private_key)
        hash = sha256(private_key).digest()
        return hash == self.private_key_hash

    def create_simple_password(self, password, private_key):
        hash = sha256(private_key).digest()
        if hash == self.private_key_hash:
            f = Fernet(password)
            self.encrypted_private_key = f.encrypt(bytes(private_key))
        else:
            raise Exception("private key not correct")
