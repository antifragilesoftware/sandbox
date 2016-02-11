# -*- coding: utf-8 -*-
import argparse
import asyncio

from aiohttp import web
from pykafka import KafkaClient

__all__ = ["get_cli_parser", "view", "exit_view"]

# we could probably do better than having a global
# flag hanging around
view_running = False


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
    global view_running
    client = KafkaClient(hosts=addr)
    topic = client.topics[topic]
    consumer = topic.get_simple_consumer()
    
    view_running = True
    while view_running:
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

    messaging = parser.add_argument_group('Messaging parameters')
    messaging.add_argument('--topic', dest='topic', action='store',
                            help='kafka topic to consume from',
                            required=True)
    messaging.add_argument('--group', dest='group', action='store',
                            help='kafka group to consume from')
    messaging.add_argument('--broker', dest='broker', action='store',
                            help='kafka broker address', required=True)
    
    endpoint = parser.add_argument_group('Service parameters')
    endpoint.add_argument('--addr', dest='addr', action='store',
                          help='address to bind to',
                          default='127.0.0.1')
    endpoint.add_argument('--port', dest='port',
                          action='store', type=int,
                          help='port to listen on', default=8080)
    endpoint.add_argument('--name', dest='name', action='store',
                          help='published service name')
    endpoint.add_argument('--id', dest='id', action='store',
                          help='published service id')
    endpoint.add_argument('--tags', dest='tags', action='store',
                          help='published service tags', nargs='*')
    return parser


def view(loop, args, view, event_handler):
    """
    Setup the view and event consumer.
    """
    coroutines = [
        consume_events(topic=args.topic.encode('utf-8'),
                       group=args.group,
                       addr=args.broker,
                       callback=event_handler),
        webserver(loop, view, addr=args.addr, port=args.port)
    ]
    return asyncio.wait(coroutines, loop=loop)
    

async def exit_view():
    """
    Simply turn the global running flag to `False`
    so that the event consuming coroutine
    can terminate.
    """
    global view_running
    view_running = False
