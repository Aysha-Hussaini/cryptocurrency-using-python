import uuid
import time 

from Backend.wallet.wallet import Wallet

class Transaction():
    """
    Documents exchange of currency from sender to one or more recipients
    """

    def __init__(self, 
            sender_wallet=None, 
            recipient=None, 
            amount=None,
            id=None,
            input=None,
            output=None
            #None represents a variable that hasn't been given a default value
    ):
        self.id = id or str(uuid.uuid4())[0:8]
        self.output = output or self.create_output(
            sender_wallet,
            recipient,
            amount
        )
        self.input = input or self.create_input(sender_wallet, self.output)

    def create_output(self, sender_wallet, recipient, amount):
        """
        Structure the output data for transaction.
        """
        if amount > sender_wallet.balance:
            raise Exception("Amount exceeds sender wallet's balance !")
        
        output = {}
        output[recipient] = amount
        output[sender_wallet.address] = sender_wallet.balance - amount

        return output

    def create_input(self, sender_wallet, output):
        """
        Structure the input data for transaction. 
        Sign the transaction and include sender's public key and address.
        (Others can verify the sign using public key)
        """

        return {
            'timestamp' : time.time_ns(),
            'amount' : sender_wallet.balance,
            'address' : sender_wallet.address,
            'public_key' : sender_wallet.public_key,
            'signature' : sender_wallet.sign(output)
        }

    def update(self, sender_wallet, recipient, amount):
        """
        Update the transaction with an existing or new recipient. 
        """
        if amount > sender_wallet.balance:
            raise Exception ("Amount exceeds sender wallet's balance !")

        if recipient in self.output:
            self.output[recipient] == self.output[recipient] + amount
        else:
            self.output[recipient] = amount 

        self.output[sender_wallet.address] = \
            self.output[sender_wallet.address] - amount

        self.input = self.create_input(sender_wallet, self.output) 

    def to_json(self):
        """
        Serialize the data into it's dictionary representation
        """
        return self.__dict__

    @staticmethod
    def from_json(transaction_json):
        """
        Deserialize the transaction data in json form into transaction instance.
        """
        return Transaction(
            **transaction_json
        )
    
    @staticmethod
    def validate_transaction(transaction):
        """
        Validate the transaction.
        Raise an exception for invalid transaction.
        """
        output_total = sum(transaction.output.values())
        
        if output_total != transaction.input['amount']:
            raise Exception ("Invalid transaction output values")

        if not Wallet.verify_sign(
            transaction.input['public_key'],
            transaction.output, 
            transaction.input['signature']
        ):
            raise Exception("Invalid transaction signature")

   
def main():
    sender_wallet = Wallet()

    transaction = Transaction(sender_wallet, 'recipient', 12)
    

    transaction_json = transaction.to_json()
    restored_json = transaction.from_json(transaction_json)

    print(f' transaction_json : {transaction_json}')
    print(f' restored_json.__dict__ : {restored_json.__dict__}')

if __name__ == "__main__":
    main()