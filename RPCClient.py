import asyncio
import time
import sys
from rpcudp.protocol import RPCProtocol


# Start local UDP server to be able to handle responses
loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(RPCProtocol, local_addr=('127.0.0.1', sys.argv[1]))
transport, protocol = loop.run_until_complete(listen)
server_ip = '127.0.0.1'
server_port = 1234

async def create(protocol, address, ident: int, maxState: int = 1):
    creationResult = await protocol.create(address, ident, maxState)
    if not(creationResult[0]):
        print("No response received.")
    else:
        if creationResult[1]:
            print("C[{0}|{1}]".format(ident,maxState))
        else:
            print("Semaphore {0} already exists".format(ident))


async def acquire(protocol, address, ident: int, state: int = 1):
    acquireResult = await protocol.acquire(address, ident, state)
    if not(acquireResult[0]):
        print("No response received.")
    else:
        if acquireResult[1]:
            print("P[{0}|{1}]".format(ident,state))
        else:
            print("Semaphore {0} does not exist".format(ident))

async def release(protocol, address, ident: int, state: int = 1):
    releaseResult = await protocol.release(address, ident, state)
    if not(releaseResult[0]):
        print("No response received.")
    else:
        if releaseResult[1]:
            print("V[{0}|{1}]".format(ident,state))
        else:
            print("Semaphore {0} does not exist".format(ident))

def semaphoreCreate(ident: int, maxState: int = 1):
    func1 = create(protocol, (server_ip, server_port), ident, maxState)
    loop.run_until_complete(func1)

def semaphoreAcquire(ident: int, state: int = 1):
    func2 = acquire(protocol, (server_ip, server_port), ident, state)
    loop.run_until_complete(func2)

def semaphoreRelease(ident: int, state: int = 1):
    func3 = release(protocol, (server_ip, server_port), ident, state)
    loop.run_until_complete(func3)


semaphoreCreate(2,1)

while(True):
    semaphoreAcquire(2,1)

    time.sleep(2)

    semaphoreRelease(2,1)