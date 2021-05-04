import uuid
#uuid stands for universally unique id - it creates a unique 36 character string
#everytime it is invoked, even with 8 characters in this program, we have around 3 trillion 
#unique addresses for our cryptocurrency

from Backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
#ec stand for elliptic cryptography

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
        

def main():
    wallet = Wallet()
    print(f' wallet : {wallet.__dict__}')

if __name__ == '__main__':
    main()
