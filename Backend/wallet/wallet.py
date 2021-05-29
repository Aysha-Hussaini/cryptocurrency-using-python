import uuid
#uuid stands for universally unique id - it creates a unique 36 character string
#everytime it is invoked, even with 8 characters in this program, we have around 3 trillion 
#unique addresses for our cryptocurrency
import json

from Backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
#ec stand for elliptic cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

class Wallet:
    """
    Each miner have their own wallet.
    It keeps track of miners balance.
    Allows a miner to authorize transactions.
    """

    def __init__(self):
        self.address = str(uuid.uuid4())[0:8]
        self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()

    def sign(self, data):
        """
        Generate signature based on data using local private key.
        """

        return self.private_key.sign(json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256()))

    @staticmethod
    def verify_sign(public_key, data, signature):
        """
        Verify signature based on original public key and data.
        """
        try:
            public_key.verify(
                signature, 
                json.dumps(data).encode('utf-8'), 
                ec.ECDSA(hashes.SHA256()) )
            return True
        except InvalidSignature:
            return False
        



def main():
    wallet = Wallet()
    print(f' wallet : {wallet.__dict__}')

    data = {'foo': 'bar'}
    signature = wallet.sign(data)
    print(f'signature : {signature}')

    should_be_valid = wallet.verify_sign(wallet.public_key, data, signature)
    print(f'should_be_valid:{should_be_valid}')

    should_not_be_valid = wallet.verify_sign(Wallet().public_key, data, signature)
    print(f'should_not_be_valid:{should_not_be_valid}')

if __name__ == '__main__':
    main()
