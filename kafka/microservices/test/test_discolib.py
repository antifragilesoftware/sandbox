# -*- coding: utf-8 -*-
import asyncio
from unittest import mock

import asynctest
import pytest

import discolib


@pytest.mark.asyncio
async def test_service_is_always_registered_and_unregistered():
    async def hello():
        return "bingo!"

    coro = asyncio.coroutine(hello)
    
    with mock.patch('discolib.client') as client_func:
        client = asynctest.CoroutineMock()
        svc = mock.MagicMock()
        
        client_func.return_value = client
        client.agent.services.register.return_value = svc
        
        res = await discolib.service(coro(), id="svc1", name="svc",
                               tags=["a", "b"],
                               port=9000, address="localhost")
        assert res == "bingo!"
        
        client.agent.services.register.assert_called_once_with("svc", id="svc1",
                                                               tags=["a", "b"],
                                                               port=9000,
                                                               address="localhost")
        client.agent.services.deregister.assert_called_once_with(svc)

        
@pytest.mark.asyncio
async def test_service_is_always_unregistered_even_after_exception():
    async def hello():
        raise ValueError()

    coro = asyncio.coroutine(hello)
    
    with mock.patch('discolib.client') as client_func:
        client = asynctest.CoroutineMock()
        svc = mock.MagicMock()
        
        client_func.return_value = client
        client.agent.services.register.return_value = svc

        with pytest.raises(ValueError):
            await discolib.service(coro(), id="svc1", name="svc",
                               tags=["a", "b"],
                               port=9000, address="localhost")
        client.agent.services.deregister.assert_called_once_with(svc)

        
@pytest.mark.asyncio
async def test_service_discovery_can_be_empty():
    with mock.patch('discolib.client') as client_func:
        client = asynctest.CoroutineMock()
        client_func.return_value = client
        client.catalog.services.return_value = {}
        res = await discolib.discover_services(["tag1"])
        assert len(res) == 0

        
@pytest.mark.asyncio
async def test_service_discovery_tags_cannot_be_empty():
    with mock.patch('discolib.client') as client_func:
        client = asynctest.CoroutineMock()
        client_func.return_value = client
        client.catalog.services.return_value = {}
        with pytest.raises(ValueError):
            await discolib.discover_services([])

            
@pytest.mark.asyncio
async def test_service_discovery_tags_superset_are_allowed():
    with mock.patch('discolib.client') as client_func:
        client = asynctest.CoroutineMock()
        client_func.return_value = client
        client.catalog.services.return_value = {'svc1': ['tag1', 'tag2']}
        res = await discolib.discover_services(["tag1"])
        assert len(res) == 1
        assert "svc1" in res

        
@pytest.mark.asyncio
async def test_service_discovery_tags_subset_are_not_allowed():
    with mock.patch('discolib.client') as client_func:
        client = asynctest.CoroutineMock()
        client_func.return_value = client
        client.catalog.services.return_value = {'svc1': ['tag1']}
        res = await discolib.discover_services(["tag1", 'tag2'])
        assert len(res) == 0

        
@pytest.mark.asyncio
async def test_cannot_locate_service_without_a_name():
    with mock.patch('discolib.client') as client_func:
        client = asynctest.CoroutineMock()
        client_func.return_value = client
        with pytest.raises(ValueError):
            res = await discolib.locate_service("")

            
@pytest.mark.asyncio
async def test_locating_a_service_by_name():
    with mock.patch('discolib.client') as client_func:
        client = asynctest.CoroutineMock()
        client_func.return_value = client
        res = await discolib.locate_service("svc1")
        client.catalog.nodes.assert_called_once_with(service="svc1")

            
