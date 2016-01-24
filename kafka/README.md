Run a Kafka cluster on Kubernetes
=================================

This guide will set a [Kafka](http://kafka.apache.org/) cluster
on an existing infrastructure. The cluster will be orchestrated
by [Kubernetes](http://kubernetes.io/).

Setup the infrastructure
------------------------

The first step is to setup an infrastructure according to
your requirements. Currently, this guide documents:

* Local deployment
* AWS deployment

This will setup the Kubernetes environment on the
infrastructure.

Run the Kafka cluster on Kubernetes
-----------------------------------

Once your Kubernetes cluster is created, you may create
the Kafka cluster.

Ensure the kubernetes cli uses the right backend:

```
$ export KUBERNETES_PROVIDER=aws
```


The first step is to create the service that will
allow you to connect from the outside world to
the Kafka cluster running in your infrastructure.

This must be done beofre running the actual containers
in order for them to get the appropriate
[environment variables](http://kubernetes.io/v1.1/docs/user-guide/services.html#environment-variables).

```
$ kubectl.sh create -f specs/kafka-service.yaml
service "kafka-service" created
```

On AWS, this will create a EC2 Load Balancer with two listeners
for port `2181` (zookeeper) and `9092` (kafka) so that
you can now connect to each.


Before you can run the containers, you must
edit the `specs/kafka-cluster.yaml` file to
set the appropriate value for the `KAFKA_ADVERTISED_HOST_NAME`
variable. This must be set properly so that your
kafka client can interact with the cluster.

On AWS, you must set that value to the domain
given to you by Amazon for the Load Balencer.

Next, you can create the Kubernetes replication controller
that will pilot the kakfa and zookeeper containers:

```
$ kubectl.sh create -f specs/kafka-cluster.yaml
replicationcontroller "kafka-controller" created
```

Monitor the status of the replication controller:

```
$ kubectl.sh get rc
CONTROLLER         CONTAINER(S)   IMAGE(S)                 SELECTOR    REPLICAS   AGE
kafka-controller   kafka          ches/kafka               app=kafka   1          22m
                   zookeeper      jplock/zookeeper:3.4.6  
```

Monitor the status of the pods owning the containers:

```
$ kubectl.sh get pods
NAME                     READY     STATUS    RESTARTS   AGE
kafka-controller-kugyh   2/2       Running   0          24m
```

At this stage, the Kafka and Zookeeper processes should be
running and listening for connection:

```
$ kubectl.sh logs kafka-controller-kugyh -c zookeeper
...
2016-01-23 13:29:52,532 [myid:] - INFO  [main:NIOServerCnxnFactory@94] - binding to port 0.0.0.0/0.0.0.0:2181
...
```

```
$ kubectl.sh logs kafka-controller-kugyh -c kafka
...
[2016-01-23 13:31:42,074] INFO Awaiting socket connections on 0.0.0.0:9092. (kafka.network.Acceptor)
...
```


You may now connect to the Kafka service through the
address used for the service. On AWS, this is the domain
of the Load Balancer.

