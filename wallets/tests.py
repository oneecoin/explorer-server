from django.test import TestCase
from hashlib import sha256
from .models import Wallet


class WalletTest(TestCase):
    private_key = "307702010104207f2175b6e420ab2a995add6d45eef4de9b73418984a3b3c5601f472b89054976a00a06082a8648ce3d030107a1440342000413390be6f2805a24070a0eb890008a64dfae722911f7bceb466925652d73315a14a195f336d954644b2c2548a478582c3584ea52afbe992b163733fec374ea8e"
    public_key = "13390be6f2805a24070a0eb890008a64dfae722911f7bceb466925652d73315a14a195f336d954644b2c2548a478582c3584ea52afbe992b163733fec374ea8e"

    simple_password = "hello"

    def setUp(self):
        wallet = Wallet.objects.create()
        wallet.private_key_hash = sha256(self.private_key.encode()).digest()
        wallet.public_key = self.public_key
        self.wallet = wallet

    def test_simple_password(self):
        # creating simple password
        self.wallet.create_simple_password(self.simple_password, self.private_key)

        # check simple password
        self.assertTrue(self.wallet.check_simple_password(self.simple_password))
        self.assertEqual(
            self.wallet.get_private_key(self.simple_password).decode(), self.private_key
        )
