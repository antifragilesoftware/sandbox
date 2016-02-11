# -*- coding: utf-8 -*-
__doc__ == """
Simple view that exposes a REST API over HTTP
to retrieve the least of last read books from
a bookshelf.

To run it:

.. code-block:: python

   $ python last_read.py --topic mytopic --broker <BROKER_ADDR>:9092 --port 8080 --name lastread --id lastread1 --tags book last

This will listen for HTTP request on `127.0.0.1:8080`
and will return a JSON encoded list of book
documents.

The service will be automatically registered to the local consul
agent (assuming running localhost:8500) using the
name, id and tags provided

When the process is terminated, the service is deregistered
automatically.
"""
import json

from aiohttp import web

from discolib import service


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
    import signal
    
    from viewlib import get_cli_parser, view, exit_view
    from discolib import service

    # let's parse the service instance settings
    args = get_cli_parser().parse_args()

    # everything will be dealt in this mainloop
    loop = asyncio.get_event_loop()

    # hook onto the usual termination signal
    # to deregister the service properly
    loop.add_signal_handler(signal.SIGINT,
                            asyncio.ensure_future,
                            exit_view())
    
    # run the view as a service until we exit it
    # the service will be advertised to the
    # discovery service and deregister once
    # we exit
    loop.run_until_complete(
        service(
            view(
                loop,
                args,
                view=bookshelf_view,
                event_handler=event_handler
            ),
            id=args.id,
            name=args.name,
            port=args.port,
            address=args.addr,
            tags=args.tags
        )
    )
        
