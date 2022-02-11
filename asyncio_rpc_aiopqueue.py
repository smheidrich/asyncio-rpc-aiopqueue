from asyncio_rpc.commlayers.base import AbstractRPCCommLayer
from asyncio_rpc.models import RPCBase
from aioprocessing import AioQueue
from typing import Tuple

class AiopQueueCommLayer(AbstractRPCCommLayer):
    """
    aioprocessing.Queue remote procedure call communication layer
    """
    @classmethod
    def create_pair(cls) \
    -> Tuple["AiopQueueCommLayer", "AiopQueueCommLayer"]:
        """Create connected pair of AiopQueueCommLayers"""
        q1, q2 = AioQueue(), AioQueue()
        return cls(q1, q2), cls(q2, q1)

    def __init__(self, in_queue: AioQueue, out_queue: AioQueue):
        self.in_queue = in_queue
        self.out_queue = out_queue

    async def do_subscribe(self):
        pass

    async def publish(self, rpc_instance: RPCBase, channel=None):
        """
        Publish implementation, publishes RPCBase instances.

        :return: the number of receivers
        """
        # rpc_instance should be a subclass of RPCBase
        # For now just check if instance of RPCBase
        assert isinstance(rpc_instance, RPCBase)

        self.out_queue.put(rpc_instance)

        return 1 # dummy


    async def subscribe(self, on_rpc_event_callback, channel=None):
        """
        Implementation for subscribe method, receives messages from
        subscription channel.

        Note: does block in while loop until .unsubscribe() is called.
        """
        try:
            self.subscribed = True
            # Inside a while loop, wait for incoming events.
            while True:
                event = await self.in_queue.coro_get()
                if event == "UNSUB":
                    break
                await on_rpc_event_callback(event, channel=channel)
        finally:
            # Close connections and cleanup
            self.subscribed = False

    async def unsubscribe(self):
        """
        Implementation for unsubscribe. Stops subscription and breaks
        out of the while loop in .subscribe()
        """
        if self.subscribed:
            self.in_queue.put("UNSUB")
            self.subscribed = False

    async def close(self):
        """
        Stop subscription & close everything
        """
        await self.unsubscribe()


class Unsubscribe(Exception):
    pass
