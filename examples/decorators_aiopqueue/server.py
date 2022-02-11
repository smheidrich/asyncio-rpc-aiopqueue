import asyncio
from typing import List
from asyncio_rpc.server import RPCServer, DefaultExecutor
from asyncio_rpc.models import RPCCall


def rpc_method(func):
    """
    Server side decorator for methods
    that need to be exposed via RPC.
    """
    def rpc_method(*args, **kwargs):
        return func(*args, **kwargs)
    rpc_method._is_rpc_method = True
    return rpc_method


class Service:
    def __init__(self, server):
        self.server = server

    @rpc_method
    def multiply(self, x, y):
        return x * y

    @rpc_method
    def quit(self):
        self.server.queue.put_nowait(b'END')
        # assumption: this only gets called from within an async function
        # (namely rpc_call below), so there is a running event loop we can use
        # to schedule async functions
        loop = asyncio.get_running_loop()
        asyncio.run_coroutine_threadsafe(
            self.server.rpc_commlayer.unsubscribe(), loop)

    def not_decorated_method(self, x, y):
        return x * y


class DecoratorFilterExecutor(DefaultExecutor):
    async def rpc_call(self, stack: List[RPCCall] = []):
        """
        Process incoming rpc call stack.
        The stack can contain multiple chained function calls for example:
            node.filter(id=1).reproject_to('4326').data
        """

        resource = self.instance

        for rpc_func_call in stack:
            assert isinstance(rpc_func_call, RPCCall)

            # Try to get the function/property from self.instance
            instance_attr = getattr(resource, rpc_func_call.func_name)

            if not hasattr(instance_attr, '_is_rpc_method'):
                raise AttributeError(
                    "%s is not a RPC method" % rpc_func_call.func_name)

            if callable(instance_attr):
                # Function
                resource = instance_attr(
                    *rpc_func_call.func_args,
                    **rpc_func_call.func_kwargs)
            else:
                # Asume property
                resource = instance_attr

        return resource


async def main(commlayer):
    rpc_server = RPCServer(commlayer)

    # Register the Service above with the the default executor in
    # the TEST namespace
    executor = DecoratorFilterExecutor(
        namespace="TEST", instance=Service(rpc_server))

    # Register executor
    rpc_server.register(executor)

    print('Start serving')
    await rpc_server.serve()
    print("Done serving")

def process_target(commlayer):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(commlayer))
