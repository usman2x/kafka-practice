## What is Strimzi?

Strimzi simplifies the process of running Apache Kafka within a Kubernetes cluster. It provides a set of Kubernetes Operators to manage Kafka clusters, topics, users, and other related components. Kubernetes Operators are custom controllers that extend Kubernetes functionality. The Strimzi Kafka Operator uses Custom Resource Definitions (CRDs) to define Kafka-related resources (e.g., Kafka clusters, topics, users).
The operator handles tasks such as deploying Kafka brokers, Zookeeper nodes, and other components, ensuring they are configured correctly and remain healthy. You define the desired state of your Kafka cluster using YAML files, and the operator ensures the actual state matches the desired state.

### Install Minikube

Minikube is a lightweight Kubernetes implementation that creates a local Kubernetes cluster for development and testing purposes. It allows developers to run Kubernetes locally on their machines without needing a full-fledged cluster.

All you need is Docker (or similarly compatible) container or a Virtual Machine environment, and Kubernetes is a single command away: `minikube start`

#### 1. Installation on macOS (Intel Processor)
To install Minikube on a Mac with an Intel processor, follow these steps:

1. Download the latest Minikube binary:
   ```sh
   curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-darwin-amd64
   ```
2. Install Minikube by moving it to a system-wide binary directory:
   ```sh
   sudo install minikube-darwin-amd64 /usr/local/bin/minikube
   ```

#### 2. Starting Minikube
To start Minikube, use the following command:
```sh
minikube start
```

```sh
# ALternatively, start Minikube with manual configuration using docker
minikube start --driver=docker --memory=4096 --cpus=4
```

Important Considerations:
- **Docker Desktop must be running** before executing `minikube start`, otherwise, you may encounter the following error:
  
  ❌ *Exiting due to DRV_DOCKER_NOT_RUNNING: Found docker, but the docker service isn't running. Try restarting the docker service.*

- This command automatically downloads `kubectl` if it's not already installed.

**Expected Output**

```plaintext
✨  Automatically selected the docker driver
📌  Using Docker Desktop driver with root privileges
👍  Starting "minikube" primary control-plane node in "minikube" cluster
🚜  Pulling base image v0.0.46 ...
💾  Downloading Kubernetes v1.32.0 preload ...
🔥  Creating docker container (CPUs=2, Memory=4000MB) ...
🐳  Preparing Kubernetes v1.32.0 on Docker 27.4.1 ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
🌟  Enabled addons: storage-provisioner, default-storageclass

❗  /usr/local/bin/kubectl is version 1.30.5, which may have incompatibilities with Kubernetes 1.32.0.
    ▪ Want kubectl v1.32.0? Try 'minikube kubectl -- get pods -A'
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default

```

> Minikube is not running, so first, try starting it using `minikube start` and check the status with `minikube status`. If it remains stuck, delete and restart Minikube using `minikube delete` followed by `minikube start`. For those using Docker as the virtual machine, ensure Docker is running by checking `docker ps`. If Docker is not running, start it and then retry `minikube start --driver=docker`. If Minikube still doesn't respond, check logs using `minikube logs` to identify any errors. Running `minikube start --alsologtostderr -v=8` can provide more debugging details. If the issue persists, restart Docker and try again.


#### 3. Verifying `kubectl`
`kubectl` is the command-line tool used to interact with Kubernetes clusters, including those created by Minikube. When Minikube is installed and started, it can automatically download and configure `kubectl` to work with the local Minikube cluster.

To check if `kubectl` is running correctly and Minikube is functioning as expected, use:
```sh
kubectl get nodes
```

### Install Strimzi Kafka Operator
Create the strimzi namespace (if not created) & Download and apply the latest Strimzi YAML
```
kubectl create namespace kafka
kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
```

After installation, check if the Strimzi Kafka operator is running:
```
kubectl get pods -n kafka
```
Expected output should show strimzi-cluster-operator running.

```
NAME                                        READY   STATUS    RESTARTS      AGE
strimzi-cluster-operator-76b947897f-2cs4h   1/1     Running   5 (54m ago)   4d19h
```

### Deploy a Kafka Cluster

Once the Strimzi Kafka Operator is installed, you can deploy a Kafka cluster using the following steps:


#### 1. Create a Kafka Cluster using Strimzi
First, create a YAML file (`kafka-cluster-ephemeral.yaml`) defining a simple Kafka cluster:

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-kafka-cluster
  namespace: kafka
spec:
  kafka:
    replicas: 3
    version: 3.6.0  
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    storage:
      type: ephemeral  
  zookeeper:
    replicas: 3
    storage:
      type: ephemeral
  entityOperator:
    topicOperator: {}
    userOperator: {}
```

> **Note:**  
> - This is a basic **ephemeral** cluster (data will be lost if pods restart).  
> - For a production setup, use **persistent-claim** storage instead of ephemeral.

---

#### 2. Apply the Kafka Cluster Configuration
Run the following command to deploy the Kafka cluster:

```sh
kubectl apply -f kafka-cluster-ephemeral.yaml -n kafka
```

You should see the output `kafka.kafka.strimzi.io/my-kafka-cluster created`

---

#### 3. Verify Kafka Deployment
Check the status of the deployed Kafka cluster:

```sh
kubectl get pods -n kafka
```

You should see pods running for:

```
user@192 strimzi % kubectl get pods -n kafka                      
NAME                                        READY   STATUS              RESTARTS      AGE
my-kafka-cluster-zookeeper-0                0/1     ContainerCreating   0             5s
my-kafka-cluster-zookeeper-1                0/1     ContainerCreating   0             5s
my-kafka-cluster-zookeeper-2                0/1     ContainerCreating   0             5s
strimzi-cluster-operator-76b947897f-2cs4h   1/1     Running             5 (98m ago)   4d20h
```

To check the Kafka resource status:

```sh
kubectl get kafka -n kafka
```

If there's no output, your Kafka resource wasn’t created properly.
If it exists but is stuck in a particular state, describe it:

```sh
kubectl describe kafka my-kafka-cluster -n kafka
```

Look for errors in the output.

Try deleting and redeploying

```
kubectl delete -f kafka-cluster-ephemeral.yaml -n kafka
kubectl apply -f kafka-cluster-ephemeral.yaml -n kafka
```

To verify Kafka’s bootstrap service, run:
```
kubectl get svc -n kafka
```

#### 4. Create a Kafka Topic
To create a topic, define a `KafkaTopic` resource in a new YAML file (`kafka-topic.yaml`):

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: hello-world-topic
  namespace: kafka
  labels:
    strimzi.io/cluster: my-kafka-cluster
spec:
  partitions: 1
  replicas: 1
  config:
    retention.ms: 7200000
    segment.bytes: 1073741824
```

Apply the topic configuration:

```sh
kubectl apply -f kafka-topic.yaml -n kafka
```

To verify the topic creation:

```sh
kubectl get kafkatopics -n kafka
```

---

#### 5. Producing & Consuming Messages
To test Kafka, you can run a producer and consumer inside the cluster.

**Start a Kafka Producer**

```sh
# Send Messages
kubectl -n kafka run kafka-producer -ti --image=quay.io/strimzi/kafka:latest-kafka-3.8.0 --rm=true --restart=Never -- bin/kafka-console-producer.sh --broker-list my-kafka-cluster-kafka-bootstrap:9092 --topic hello-world-topic
```

Type messages and press **Enter** to send them.

Follow Troubleshooting steps if Kafka Producer Not Running

- Checked Logs for Errors
   ```sh
   kubectl logs kafka-producer -n kafka
   ```

- Inspected the Pod for Additional Details
   ```sh
   kubectl describe pod kafka-producer -n kafka
   ```

- Try pulling the Required Kafka Image Manually
   ```sh
   docker pull quay.io/strimzi/kafka:latest-kafka-3.8.0
   ```

- Retry to Send Messages

**Start a Kafka Consumer**
Open another terminal and run:

```sh
# Receive Messages
kubectl -n kafka run kafka-consumer -ti --image=quay.io/strimzi/kafka:latest-kafka-3.8.0 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server my-kafka-cluster-kafka-bootstrap:9092 --topic hello-world-topic --from-beginning
```

You should see the messages from the producer.

---

### Open Questions

1. What are the differences in nods, pods, deployments and namespaces
2. Why do we need namespace?

### Cheet Sheet
1. `kubectl get namespaces`
2. `kubectl get deployments`
3. `kubectl get nodes`
4. `kubectl get pods`


### Troubleshooting Guide

#### 1. Unable to connect to the server: net/http: TLS handshake timeout


### References
1. https://strimzi.io/docs/operators/latest/overview 
