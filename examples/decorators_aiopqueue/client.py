import asyncio
from uuid import uuid4
from argparse import ArgumentParser
from asyncio_rpc.client import RPCClient
from asyncio_rpc.models import RPCCall, RPCStack
from asyncio_rpc.commlayers.aiopqueue import AiopQueueCommLayer
from aioprocessing import AioProcess
import server


# variant of the decorators example using AiopQueueCommLayer


def rpc_method(func):
    """
    Decorator function that can be used to decorate
    (proxy) functions client side. It uses the same code as in
    the basic example for executing the rpc call.

    Note: it has drawbacks, see below under multiply.
    """
    def rpc_method(self, *args, **kwargs):
        rpc_func_call = RPCCall(func.__name__, args, kwargs)
        rpc_func_stack = RPCStack(
            uuid4().hex, self.namespace, 300, [rpc_func_call])
        return self.client.rpc_call(rpc_func_stack)
    rpc_method._is_rpc_method = True
    return rpc_method


class ServiceClient:
    def __init__(self, client: RPCClient, namespace=None):
        assert namespace is not None
        assert client is not None
        self.client = client
        self.namespace = namespace

    @rpc_method
    async def multiply(self, x, y):
        """
        The decorator takes care of sending the function
        name & params to the RPCServer

        Note:
        A (big) drawback of the decorator is that wrapped function
        do not seem to return anything. Think well
        before applying it everywhere....
        """

    @rpc_method
    async def not_decorated_method(self, x, y):
        """
        This method is not decorated and therefore
        should not trigger a RPC call
        """

    @rpc_method
    async def quit(self):
        """
        Make the server stop serving (useful only for multiprocessing server)
        """


async def main(commlayer):
    # start client
    rpc_client = RPCClient(client_commlayer)

    service_client = ServiceClient(rpc_client, 'TEST')

    result = await service_client.multiply(100, 100)

    print(result)

    try:
        await service_client.not_decorated_method(100, 100)
    except AttributeError as e:
        print(e)

    await service_client.quit()

    await proc.coro_join()


if __name__ == '__main__':
    parser = ArgumentParser()
    args = parser.parse_args()

    client_commlayer, server_commlayer = AiopQueueCommLayer.create_pair()

    # start multiprocessing process running the server (has to happen BEFORE
    # starting the asyncio event loop to prevent having a copy of it in the new
    # process when using 'fork'-type multiprocessing; using 'forkserver' or
    # 'spawn' would circumvent this limitation)
    proc = AioProcess(target=server.process_target, args=[server_commlayer])
    proc.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(client_commlayer))
