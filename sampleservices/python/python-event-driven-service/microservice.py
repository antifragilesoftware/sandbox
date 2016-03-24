# -*- coding: utf-8 -*-
__doc__ = """
A simple Kafka consumer that print message
values as they arrive.

Simply run it as follows:

$ python microservice.py --topic my-topic

The default broker's address is `localhost:9092`.
This can changed through the `--broker` parameter.

If you want to build it as a Docker container:

$ docker build -t micro .
$ docker run --rm micro --broker <ADVERTIZED_NAME>:9092 --topic my-topic
"""
import argparse
import time

from pykafka import KafkaClient
from pykafka.exceptions import ConsumerStoppedException


def consume_events(consumer):
    """
    Consume messages from the topic set to this `consumer`.
    """
    try:
        while True:
            message = consumer.consume()
            if message is not None:
                print(message.value)
    except ConsumerStoppedException:
        pass
        
        
def stop_consuming_events(consumer):
    """
    Notify the consumer's flag that it is
    not running any longer.

    The consumer will properly terminate at its
    next iteration.
    """
    consumer.stop()

    # wait for the consumer to actually close down
    # sadly, pykafka doesn't give us a mean to
    # query for the status
    time.sleep(0.2)

        
def parse_commandline():
    """
    Parse the command line arguments to retrieve the
    broker's address and the topic/group to
    consume from.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', dest='topic', action='store',
                        help='kafka topic to consume from')
    parser.add_argument('--group', dest='group', action='store',
                        help='kafka group to consume from')
    parser.add_argument('--broker', dest='broker',
                        action='store', default='localhost:9092',
                        help='kafka broker address')
    return parser.parse_args()
    
        
def run():
    """
    Consume messages from a Kafka broker and
    process them as they arrive.
    """
    args = parse_commandline()

    # connect to the broker and get our topic consumer ready
    client = KafkaClient(hosts=args.broker)
    topic = args.topic.encode('utf-8')
    group = args.group.encode('utf-8') if args.group else None
    consumer = client.topics[topic].get_simple_consumer(consumer_group=group)

    try:
        consume_events(consumer)
    except KeyboardInterrupt:
        pass
    finally:
        # let's try to terminate cleanly
        stop_consuming_events(consumer)

        
if __name__ == '__main__':
    run()
