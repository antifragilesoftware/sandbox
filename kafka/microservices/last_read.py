# -*- coding: utf-8 -*-
__doc__ == """
Simple view that exposes a REST API over HTTP
to retrieve the least of last read books from
a bookshelf.

To run it:

.. code-block:: python

   $ python --broker KAFKA_IP:9092 --topic my-topic --addr 127.0.0.1 --port 8080 

This will listen for HTTP request on `127.0.0.1:8080`
and will return a JSON encoded list of book
documents.
"""
import json

from aiohttp import web

# internal state
bookshelf = []

async def bookshelf_view(request):
    """
    View to see the current list of books
    in your bookshelf.
    """
    return web.Response(body=json.dumps(bookshelf).encode('utf-8'),
                        headers={"content-type": "application/json"})


async def event_handler(message):
    """
    Called whenever a new event was received from
    the event store.

    Simply store the event in a local state arena.
    """
    bookshelf.append(message.value.decode('utf-8'))

    
if __name__ == '__main__':
    import asyncio
    
    from viewlib import get_cli_parser, run_view

    loop = asyncio.get_event_loop()
    try:
        run_view(loop,
                 get_cli_parser().parse_args(),
                 view=bookshelf_view,
                 event_handler=event_handler
        )
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
