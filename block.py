class Block:
    """
    Block : a unit of storage
    Store transactions in a blockchain that supports cryptocurrency
    """

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f'Block- data :{self.data}'
