import asyncio
import time
import sys
from rpcudp.protocol import RPCProtocol

async def create_semaphore(protocol, address, ident: int, maxState: int = 1):
    creationResult = await protocol.create_semaphore(address, ident, maxState)
    print(creationResult[1] if creationResult[0] else "No response received.")

    # creationResult = await protocol.create_semaphore(address, ident, maxState)
    # print(result[1] if result[0] else "No response received.")    

async def acquire(protocol, address, ident: int, state: int = 1):
    acquireResult = await protocol.acquire(address, ident, state)
    print(acquireResult[1] if acquireResult[0] else "No response received.")

async def release(protocol, address, ident: int, state: int = 1):
    releaseResult = await protocol.release(address, ident, state)
    print(releaseResult[1] if releaseResult[0] else "No response received.")

# Start local UDP server to be able to handle responses
loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(RPCProtocol, local_addr=('127.0.0.1', sys.argv[1]))
transport, protocol = loop.run_until_complete(listen)

# Call remote UDP server to say hi

func1 = create_semaphore(protocol, ('127.0.0.1', 1234), 1, 2)
loop.run_until_complete(func1)

func2 = acquire(protocol, ('127.0.0.1', 1234), 1)
loop.run_until_complete(func2)

time.sleep(2)

func3 = release(protocol, ('127.0.0.1', 1234), 1)
loop.run_until_complete(func3)


#loop.run_forever()
