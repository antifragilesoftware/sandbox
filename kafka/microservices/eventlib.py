# -*- coding: utf-8 -*-
import asyncio

from pykafka import KafkaClient

__all__ = ["consume_events"]

consumer_running = False


async def consume_events(topic, group, addr, callback, delay=0.01):
    """
    Connect to the Kafka endpoint and start consuming
    messages from the given `topic`.

    The given callback is applied on each
    message.

    If `callback` returns `False`, this will exit
    the consumer immediately.
    """
    global consumer_running
    client = KafkaClient(hosts=addr)
    topic = client.topics[topic]
    consumer = topic.get_simple_consumer()
    
    consumer_running = True
    while consumer_running:
        message = consumer.consume(block=False)
        if message is not None:
            running = await callback(message)
            if running is False:
                break
        else:
            await asyncio.sleep(delay)

            
def finish_consumer():
    """
    Notify the consumer's flag that it is
    not running any longer.

    The consumer will properly terminate at its
    next iteration.
    """
    global consumer_running
    consumer_running = False
