import asyncio
import time
from rpcudp.protocol import RPCProtocol

semaphoresDictionary = {}
semaphoreCreateLock = asyncio.Lock()
semaphoreAcquireLock = asyncio.Lock()
semaphoreReleaseLock = asyncio.Lock()

class RPCServer(RPCProtocol):


    async def rpc_create(self, address, ident: int, maxState: int = 1):
        async with semaphoreCreateLock:
            if ident in semaphoresDictionary:
                return False
            else:
                semaphoresDictionary[ident] = asyncio.Semaphore(maxState)
                print("!!!New sempahore with [id={0}|state={1}]".format(ident, maxState))
                return True
    
    async def rpc_acquire(self, address, ident: int, state: int = 1):
        exists = False
        async with semaphoreCreateLock:
            exist = ident in semaphoresDictionary
        async with semaphoreAcquireLock:
            if exist:
                for i in range(state):
                    await semaphoresDictionary[ident].acquire()
                    print("@@@Sempahore acquired [id={0}|state={1}]".format(ident, state))
                return True
                
            else:
                return False
    
    async def rpc_release(self, address, ident: int, state: int = 1):
        exists = False
        async with semaphoreCreateLock:
            exists = ident in semaphoresDictionary    
        async with semaphoreReleaseLock:
            if exists:
                for i in range(state):
                    semaphoresDictionary[ident].release()
                    print("***Sempahore released [id={0}|state={1}]".format(ident, state))
                print("--------------------------------------------------")
                return True
            else:
                return False


# start a server on UDP port 1234
loop = asyncio.get_event_loop()
listen = loop.create_datagram_endpoint(RPCServer, local_addr=('127.0.0.1', 1234))
transport, protocol = loop.run_until_complete(listen)
loop.run_forever()