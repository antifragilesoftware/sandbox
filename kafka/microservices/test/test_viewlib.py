# -*- coding: utf-8 -*-
import asyncio
import time
from unittest import mock

import aiohttp
import pykafka
import pytest

import eventlib

def source():
    for i in range(10):
        yield i

class FakeConsumer(mock.MagicMock):
    def consume(block=True):
        if self._running:
            return 0
    
        
@pytest.mark.asyncio
async def test_consumer_will_exit_on_a_stop_iteration(event_loop):
    async def event_processor(message):
        await asyncio.sleep(0.1)
        print("bimm")

    gen = iter(source())
    with mock.patch('eventlib.KafkaClient', spec=pykafka.KafkaClient) as KafkaClient:
        client = KafkaClient.return_value
        client.topics = {'my-topic': mock.MagicMock(spec=pykafka.topic.Topic)}
        client.topics['my-topic'].get_simple_consumer.return_value = FakeConsumer(_running=True)
        asyncio.ensure_future(eventlib.consume_events('my-topic', 'my-group', 'dummyaddr:9092',
                                                      event_processor))
        await asyncio.sleep(0.2)
        print("ja")
        await eventlib.stop_consuming_events('my-topic')

    assert next(gen) == 1
    assert eventlib.has_consumer('my-topic') == False
    

        
@pytest.mark.asyncio
async def test_consumer_will_wait_when_no_messages(event_loop):
    processed_message = None
    received_message_time = None
    async def event_processor(message):
        global processed_message
        global received_message_time
        
        processed_message = message
        received_message_time = time.time()

    start = time.time()
    with mock.patch('eventlib.KafkaClient') as KafkaClient:
        # that first result will trigger the internal delay
        # within the consumer
        KafkaClient.return_value.topics['my-topic'].get_simple_consumer.return_value.consume.side_effect = [None, "second"]
        asyncio.ensure_future(eventlib.consume_events('my-topic', 'my-group', 'dummyaddr:9092',
                                                      event_processor, delay=1))
        await asyncio.sleep(0.05)
        await eventlib.stop_consuming_events('my-topic')
        
    await asyncio.sleep(0.5)
    assert processed_message == "second"
    assert 0.9 <= received_message_time - start <= 1.1
    
