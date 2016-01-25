Kubernetes cluster
==================

Requirements
------------

* An [AWS account](https://console.aws.amazon.com) with enough permissions to manage EC2 services
* Create a IAM role which has the `AmazonEC2FullAccess` policy.

Setup the AWS cli
-----------------

1. Install Python 2.7 or above on your local machine:

On Ubuntu:

```
$ sudo apt-get install python
$ sudo apt-get install python-pip
```

On MacOSX:

```
$ brew install python
```

2. Install the [aws cli](https://aws.amazon.com/fr/cli/):

On Ubuntu:

```
$ sudo pip install awscli
```

On MacOSX:

```
$ pip install awscli
```

Note that you may want to create a virtual environment
first if you rather not clutter the system-wide environment.


3. Configure the AWS cli so with your AWS credentials:

```
$ aws configure
AWS Access Key ID: XXXX
AWS Secret Access Key: XXXX
Default region name: eu-west-1a
Default output format
```

Set the appropriate values for each field, only leaving the last one empty.

Those information are stored in `~/.kube/config`.


Setup the kubernetes cli
------------------------

1. Get kubernetes on your local machine (a newer version may be available):

```
$ curl -o kubernetes.tar.gz https://github.com/kubernetes/kubernetes/releases/download/v1.1.4/kubernetes.tar.gz
```

2. Unpack it:

```
$ tar zxf kubernetes.tar.gz
```

This will create the kubernetes directory.

3. Edit your profile and change your `PATH` yo point at the `kubernetes/cluster` directory.

4. Edit `kubernetes/cluster/aws/config-default.sh` and
change the settings accordingly to your environment. Mostly, make sure
you point at the correct AWS region using the `ZONE` and `AWS_S3_REGION` variables.

You may also want to change the size of your cluster and the
capacity of each node by editing the `NUM_MINIONS` and `MINION_SIZE`
variables.

Create the kubernetes cluster
-----------------------------

1. Ensure the kubernetes cli uses the right backend:

```
$ export KUBERNETES_PROVIDER=aws
```

Always set that variable befre running kubernetes cli.

2. Create the cluster as follows:
```
$ `pwd`/kubernetes/cluster/kube-up.sh
```
Wait for 15 minutes before the cluster is ready. At that point,
you should have one master node and a number of minion nodes
available on AWS.

Destroy the cluster
-------------------

Run the following command:
```
$ `pwd`/kubernetes/cluster/kube-down.sh
```

WARNING: This will destroy all the EC2 instances that were
created during the cluster creation.

