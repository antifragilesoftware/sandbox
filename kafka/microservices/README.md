A set of simple microservices that send and consume events
from a Kafka event store to simulate actions and events
on a virtual bookshelf.

Get started
===========

To run these services, you will first need to deploy a
Kafka event store as explained [here](https://github.com/antifragilesoftware/sandbox/tree/master/kafka#run-a-kafka-cluster-on-kubernetes).

Once that is setup, you can run the services against it.

Python requirements
-------------------

For the services written in Python, you will need
Python 3.5+ (not below):

On Ubuntu:

```
$ sudo apt-get install python3
$ sudo apt-get install python3-pip
```

On MacOSX:

```
$ brew install python3
```

Then, simply use pip to install the following packages:

* [aiohttp](http://aiohttp.readthedocs.org/en/stable/)
* [pykafka](http://pykafka.readthedocs.org/en/latest/)

Once installed, simply run each service according
to its inline documentation.