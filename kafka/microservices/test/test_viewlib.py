# -*- coding: utf-8 -*-
import asyncio
from unittest import mock

import pytest

import viewlib

def test_parse_kafka_broker_address_is_mandatory():
    parser = viewlib.get_cli_parser()
    with pytest.raises(SystemExit) as excinfo:
        parser.parse_args(['--topic', 'test'])

        
def test_parse_kafka_topic_is_mandatory():
    parser = viewlib.get_cli_parser()
    with pytest.raises(SystemExit) as excinfo:
        parser.parse_args(['--broker', 'addr'])

        
def test_parse_default_service_listening_address_is_localhost():
    parser = viewlib.get_cli_parser()
    args = parser.parse_args(['--broker', 'addr', '--topic', 'test'])
    assert args.addr == '127.0.0.1'

    
def test_parse_default_service_listening_port_is_localhost():
    parser = viewlib.get_cli_parser()
    args = parser.parse_args(['--broker', 'addr', '--topic', 'test'])
    assert args.port == 8080

    
@pytest.mark.asyncio
async def test_webserver_is_created(event_loop):
    async def dummy_view(request):
        await asyncio.sleep(1, loop=event_loop)
    
    srv = await viewlib.webserver(event_loop, dummy_view, '127.0.0.1', 8080)
    assert isinstance(srv, asyncio.AbstractServer)

    
@pytest.mark.asyncio
async def test_can_exit_from_consumer_loop(event_loop):
    async def event_processor(message):
        assert message == "hello world"
        
        # tell the consumer to exit
        # TODO: might not be the cleanest chain of responsibility
        return False

    with mock.patch('viewlib.KafkaClient') as KafkaClient:
        # that is an ugly line but it means we can
        # directly access the object that will be used
        # internally to the coroutine
        KafkaClient.return_value.topics['my-topic'].get_simple_consumer.return_value.consume.return_value = "hello world"
        await viewlib.consume_events('my-topic', 'dummyaddr:9092', event_processor)
    

@pytest.mark.asyncio
async def test_consumer_loop_will_wait_before_next_iteration(event_loop):
    # this test needs some loving as we need to
    # check the coroutine does sleep indeed
    
    async def event_processor(message):
        assert message == "hello world"
        return False

    with mock.patch('viewlib.KafkaClient') as KafkaClient:
        # the first call to the inner consume method
        # will get None which will provoke the pause.
        # The second call will get the message leading
        # to our event handler to return False that will
        # exist the consumer
        KafkaClient.return_value.topics['my-topic'].get_simple_consumer.return_value.consume.side_effect = [None, "hello world"]
        await viewlib.consume_events('my-topic', 'dummyaddr:9092', event_processor)
    
