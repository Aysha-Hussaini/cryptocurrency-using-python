import time
from Backend.blockchain.blockchain import Blockchain
from Backend.config import SECONDS

blockchain = Blockchain()

times = []

for i in range(100):
    start_time = time.time_ns()
    blockchain.add_block(i)
    end_time = time.time_ns()

    time_to_mine = (end_time - start_time) / SECONDS
    times.append(time_to_mine)

    average_time = sum(times) / len(times)
    print(f'start: {start_time}, end: {end_time}')
    print(f'Hash of Mined Block: {blockchain.chain[-1].hash}')
    print(f'New Block Difficulty : {blockchain.chain[-1].difficulty} ')
    print (f'Time to mine new block : {time_to_mine}s ')
    print(f'Average time to add blocks : {average_time}s \n ')
