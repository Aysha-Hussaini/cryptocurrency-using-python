import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from Backend.blockchain.block import Block
from Backend.wallet.transaction import Transaction

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-16e4cd48-a5fc-11eb-86bf-e27ecfa4e4f1'
pnconfig.publish_key = 'pub-c-3b858d1b-d3d0-4275-970a-50daefe8213c'

CHANNELS = {
    'TEST' : 'TEST',
    'BLOCK' : 'BLOCK',
    'TRANSACTION' : 'TRANSACTION'
}

class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain 
        self.transaction_pool = transaction_pool


    def message(self, pubnub, message_object):
        print(f'\n-- Channel : {message_object.channel} | Message : {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:] #copy
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                print(f'-- Successfully completed replacement of chain')
            except Exception as e:
                print(f'\n --Did not replace the chain :{e}')

        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print( '\n Set the new transaction in transaction pool')



class PubSub():
    """
    Handles the publish/subscribe layer of application.
    Provides communication between the nodes of blockchain network.
    """
    def __init__(self, blockchain, transaction_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, message):
        """
        Publish the message_object to the channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast a block object to all nodes
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())

    def broadcast_transaction(self, transaction):
        """
        Broadcast a transaction to all nodes.
        """
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())

def main():
    #Delaying so that subscribtion is done before publish
    time.sleep(1)
    pubsub = PubSub()

    pubsub.publish(CHANNELS['TEST'], {'foo' : 'bar'})
    

if __name__ == "__main__":
    main()



