import uuid
#uuid stands for universally unique id - it creates a unique 36 character string
#everytime it is invoked, even with 8 characters in this program, we have around 3 trillion 
#unique addresses for our cryptocurrency
import json

from Backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
#ec- elliptic cryptography
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
#dss- digital signature standard

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
        self.serialize_public_key()

    def sign(self, data):
        """
        Generate signature based on data using local private key.
        """

        return decode_dss_signature(self.private_key.sign(
            json.dumps(data).encode('utf-8'), 
            ec.ECDSA(hashes.SHA256())))

    def serialize_public_key(self):
        """
        Reset public key to it's serialized version.
        """
        # self.public_key_bytes = self.public_key.public_bytes(
        #     encoding = serialization.Encoding.PEM, 
        #     format = serialization.PublicFormat.SubjectPublicKeyInfo
        #     )
        #     #PEM Format : ---- Begin public key
        #     #                   khjhgfrtyujhb
        #     #             ---- End Public Key

        #     #encoding creates byte string , decoding removes 'b from the key

        # decoded_public_key = self.public_key.decode('utf-8')
        # self.public_key = decoded_public_key

        self.public_key = self.public_key.public_bytes(
            encoding = serialization.Encoding.PEM, 
            format = serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

     

    @staticmethod
    def verify_sign(public_key, data, signature):
        """
        Verify signature based on original public key and data.
        Verify method takes public_key in it's original form so we have to specify 
        deserialize method.
        """
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )
        
        (r, s) = signature

        try:
            deserialized_public_key.verify(
                encode_dss_signature(r, s), 
                json.dumps(data).encode('utf-8'), 
                ec.ECDSA(hashes.SHA256()) )
            return True
        except InvalidSignature:
            return False

    @staticmethod
    def calculate_balance(blockchain, address):
        """
        Calculate balance of given address wallet considering transaction data within blockchain.

        Balance is found by adding the output values that belongs to the address 
        since the most recent transaction by the address.
        """
        balance = STARTING_BALANCE

        for block in blockchain.chain:
            for transaction in block.data:
                # using bracket syntax insead of transaction.input
                # because the transactions are stored in serialized form in the blocks 
                if transaction['input']['address'] == address:
                    # Any time wallet address conducts a new transaction, it resets it's balance
                    balance = transaction['output'][address]
                elif address in transaction['output']:
                    balance += transaction['output'][address]

        return balance            



        



def main():
    wallet = Wallet()
    print(f' wallet : {wallet.__dict__}')

    data = {'foo': 'bar'}
    signature = wallet.sign(data)
    print(f'decoded_signature : {signature}')

    should_be_valid = wallet.verify_sign(wallet.public_key, data, signature)
    print(f'should_be_valid:{should_be_valid}')

    should_not_be_valid = wallet.verify_sign(Wallet().public_key, data, signature)
    print(f'should_not_be_valid:{should_not_be_valid}')

if __name__ == '__main__':
    main()
