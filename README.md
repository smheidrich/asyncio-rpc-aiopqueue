
# asyncio-rpc-aiopqueue

[![pipeline status](https://gitlab.com/smheidrich/asyncio-rpc-aiopqueue/badges/main/pipeline.svg?style=flat-square)](https://gitlab.com/smheidrich/asyncio-rpc-aiopqueue/-/commits/main)
[![docs](https://img.shields.io/badge/docs-online-brightgreen?style=flat-square)](https://smheidrich.gitlab.io/asyncio-rpc-aiopqueue/)

multiprocessing commlayer for [nens/asyncio-rpc][1] using [aioprocessing][2]'s
`AioQueue`.

Allows using asyncio-rpc for local interprocess communication with and between
processes spawned using Python's multiprocessing module. Internally, this uses
`aioprocessing.AioQueue`, which spawns threads in order to make blocking
`multiprocessing.Queue` calls fit for use with asyncio, so be aware of that.

## Installation

```bash
pip install git+https://gitlab.com/smheidrich/asyncio-rpc-aiopqueue.git
```

## Usage

See the decorator example (adapted from asyncio-rpc's own decorator example) in
`examples/decorators_aiopqueue`. In contrast to asyncio-rpc's example, client
and server here are called from within the same script (`client.py`).

Usage is fairly analogous to that of the Redis commlayer, except:

1. You create a pair of endpoints using [`AiopQueueCommLayer.create_pair()`][3]
   or, if you want to use your own queue, create them separately using the
   [regular constructor][4].
2. You leave out all the serialization stuff because this is done via ordinary
   pickling.
3. In contrast to "proper" RPC, in this use case you'll probably want to
   provide an RPC method that makes the server shut down. This is a bit tricky
   to do in asyncio-rpc. See the aforementioned example for how to do this
   (method was adapted from asyncio-rpc's tests).

## Documentation

The online documentation including the API reference can be found
[here](https://smheidrich.gitlab.io/asyncio-rpc-aiopqueue/).


[1]: https://github.com/nens/asyncio-rpc
[2]: https://github.com/dano/aioprocessing
[3]: https://smheidrich.gitlab.io/asyncio-rpc-aiopqueue/api.html#asyncio_rpc_aiopqueue.AiopQueueCommLayer.create_pair
[4]: https://smheidrich.gitlab.io/asyncio-rpc-aiopqueue/api.html#asyncio_rpc_aiopqueue.AiopQueueCommLayer
