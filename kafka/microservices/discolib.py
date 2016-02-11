# -*- coding: utf-8 -*-
import asyncio
from functools import wraps, partial

from aioconsul import Consul

__all__ = ['service', 'discover_services', 'locate_service']

_client = None

def client():
    """
    Internal function to connect to the consul
    client lazily. Useful for testing purpose
    but also when module is only imported.
    """
    global _client
    if not _client:
        _client = Consul()
    return _client

    
async def service(coro, id, name, tags, port, address=None):
    """
    Service coroutine that will register before the
    given coroutine is executed and unregister right after
    it.
    """
    svc = await client().agent.services.register(name, id=id,
                                                 address=address,
                                                 port=port,
                                                 tags=tags)
    try:
        result = await asyncio.ensure_future(coro)
    finally:
        # we want to make sure the service is
        # unregistered even when it failed
        await client().agent.services.deregister(svc)

    return result


async def discover_services(tags):
    """
    Return the set of nodes that expose services
    registered with the provided set of tags.

    If the peer services have been registered with
    other tags as well, that is fine. But they need
    to have at least the tags provided in parameters.

    The returned set is a dictionary where the keys
    are the service names and their values is the node
    set where they are exposed.
    
    .. code-block:: python
    
        services = await discover_services(tags=["whatever"])
        for service, nodes in services.items():
            for node in nodes:
                print(service + " => " + node.address)
    """
    if not tags:
        raise ValueError("You must pass at least one tag")
    
    result = {}
    tags = set(tags)
    for service_name, service_tags in (await client().catalog.services()).items():
        if service_tags and set(service_tags).issuperset(tags):
            nodes = await client().catalog.nodes(service=service_name)
            result[service_name] = nodes
    return result


async def locate_service(name):
    """
    Return the set of nodes that expose the service
    identified by the given name.
    """
    if not name:
        raise ValueError("You must provide a service name")
    
    return await client().catalog.nodes(service=name)
