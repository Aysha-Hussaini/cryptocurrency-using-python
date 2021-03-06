class TransactionPool:
    def __init__(self):
        self.transaction_map = {}


    def set_transaction(self, transaction):
        """
        Set a transaction in transaction pool.
        """
        self.transaction_map[transaction.id] = transaction

    def existing_transaction(self, address):
        """
        Find a transaction generated by the address in transaction pool.
        """
        for transaction in self.transaction_map.values():
            if transaction.input['address'] == address:
                return transaction 

            #if not found, 'None' will be returned

    def transaction_data(self):
        """
        Get all the transactions in transaction pool and return them in json serialized form.
        """
        return list (map( 
            lambda transaction : transaction.to_json(),
            self.transaction_map.values()))


    def clear_blockchain_transactions(self, blockchain):
        """
        Delete blockchain recorded transactions from the transaction pool.
        """   
        for block in blockchain.chain:
            for transaction in block.data:
                try:
                    del self.transaction_map[transaction['id']]
                    #using bracket syntax because it is in serialized form
                except KeyError:
                    pass





