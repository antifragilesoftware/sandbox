# -*- coding: utf-8 -*-
import argparse
import asyncio

from aiohttp import web
from pykafka import KafkaClient

__all__ = ["run_view", "get_cli_parser"]


async def webserver(loop, view, addr, port):
    """
    Initialize the HTTP server and start responding
    to requests.
    """
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', view)

    srv = await loop.create_server(app.make_handler(),
                                   addr, port)
    return srv


async def consume_events(topic, group, addr, callback, delay=0.01):
    """
    Connect to the Kafka endpoint and start consuming
    messages from the given `topic`.

    The given callback is applied on each
    message.

    If `callback` returns `False`, this will exit
    the consumer immediately.
    """
    client = KafkaClient(hosts=addr)
    topic = client.topics[topic]
    consumer = topic.get_simple_consumer()
    while True:
        message = consumer.consume(block=False)
        if message is not None:
            running = await callback(message)
            if running is False:
                break
        else:
            await asyncio.sleep(delay)

     
def get_cli_parser():
    """
    Create and return a command line parser
    that can be extended to add more options
    and  processed to extract parameters from the cli.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', dest='topic', action='store',
                        help='kafka topic to consume from',
                        required=True)
    parser.add_argument('--group', dest='group', action='store',
                        help='kafka group to consume from')
    parser.add_argument('--broker', dest='broker', action='store',
                        help='kafka broker address', required=True)
    parser.add_argument('--addr', dest='addr', action='store',
                        help='address to bind to',
                        default='127.0.0.1')
    parser.add_argument('--port', dest='port', action='store',
                        help='port to listen on', default=8080)
    return parser


def run_view(loop, args, view, event_handler):
    """
    Run the view and event consumer asynchronously
    within the given main asyncio loop.
    """
    coroutines = [
        consume_events(topic=args.topic.encode('utf-8'),
                       group=args.group,
                       addr=args.broker,
                       callback=event_handler),
        webserver(loop, view, addr=args.addr, port=args.port)
    ]
    loop.run_until_complete(asyncio.wait(coroutines, loop=loop))
    
