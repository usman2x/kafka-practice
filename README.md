This documentation provides a brief overview of Kafka commands, categorized by their functionality, along with scenarios where they are used. The commands are grouped into **Installation**, **Running Kafka**, **Topic Management**, **Producing and Consuming Messages**, **Consumer Group Management**, and **Replication and Broker Management**.

### **1. Installing Kafka on MacOS**

**Command:** Install Kafka using binary download and set the path in `.zshrc`.

- **Steps:**
  1. Download Kafka binaries from the [official Kafka website](https://kafka.apache.org/downloads).
  2. Extract the archive to a directory (e.g., `/Users/user/kafka`).
  3. Update the `.zshrc` file:
     ```
     export KAFKA_HOME=/Users/user/kafka
     export PATH=$PATH:$KAFKA_HOME/bin
     ```
  4. Reload the terminal or use `source ~/.zshrc` to apply changes.

### **2. Running Kafka Locally**

#### **Zookeeper and Kafka Server Commands**

1. **Start Zookeeper:**

   ```
   # Starts the Zookeeper server, which is required for Kafka to manage brokers and coordinate topics.
   # Initializing Zookeeper before starting Kafka brokers.
   
   zookeeper-server-start.sh /Users/user/kafka/config/zookeeper.properties
   ```

2. **Start Kafka Broker:**

   ```
   # Starts a Kafka broker using the specified configuration file.
   
   kafka-server-start.sh /Users/user/kafka/config/server.properties
   ```

#### **Topic Management Commands**

1. **List all topics:**

   ```
   kafka-topics.sh --list --bootstrap-server localhost:9092
   ```

2. **Describe a specific topic:**

   ```
   # Provides detailed information about a specific topic, including partitions, replicas, and leader brokers.
   
   kafka-topics.sh --describe --bootstrap-server localhost:9092 --topic <topic-name>
   ```

3. **Create a topic with multiple partitions:**

   ```
   # Creates a new topic with multiple partitions and a specified replication factor.
   # Creating a topic for testing partitioning and parallel processing.
   
   kafka-topics.sh --create --bootstrap-server localhost:9092 --topic multi-partition-topic --partitions 3 --replication-factor 1
   ```

4. **Delete a topic:**

   ```
   kafka-topics.sh --delete --topic <topic-name> --bootstrap-server localhost:9092
   ```

#### **Producer Commands**

1. **Produce messages to a topic:**
   ```
   kafka-console-producer.sh --broker-list localhost:9092 --topic multi-partition-topic --property parse.key=true --property key.separator=:
   ```
   - Ensure messages are in `key:value` format. Errors will be logged if the format is incorrect.

#### **Consumer Commands**

1. **Consume messages from a specific partition:**

   ```
   kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic multi-partition-topic --partition 0 --from-beginning
   ```

2. **Consume messages as part of a consumer group:**

   ```
   kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic multi-partition-topic --group my-consumer-group
   ```

3. **List consumer groups:**

   ```
   kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
   ```

4. **Describe a consumer group:**

   ```
   kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group my-consumer-group
   ```

5. **Reset consumer group offsets to the earliest:**

   ```
   # Resets the offset for a consumer group to the earliest message.
   
   kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-consumer-group --reset-offsets --to-earliest --execute --topic multi-partition-topic
   ```

   - After this, use the `describe` command to observe the updated offset.

#### **Replication and Multiple Brokers**

1. **Start a second broker:**

   ```
   # Starts a second Kafka broker to enable replication and fault tolerance.
   
   kafka-server-start.sh /Users/user/kafka/config/server-2.properties
   ```

2. **Connect to Zookeeper shell:**

   ```
   # Opens a shell to interact with Zookeeper for cluster management.
   # Managing Zookeeper and debugging cluster state.
   
   zookeeper-shell.sh localhost:2181
   ```

3. **Create a topic with replication factor:**

   ```
   # Creates a replicated topic with a specified replication factor to test fault tolerance in a multi-broker setup.
   
   kafka-topics.sh --create --topic replicated-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 2
   # Note: This will fail if only one broker is running. To resolve, start a second broker.
   ```

4. **Describe topic to view replicas:**

   ```
   # Shut down one broker to observe how Kafka handles replication.
   # Displays replication details, including leader and replicas for a topic.
   
   kafka-topics.sh --describe --topic replicated-topic --bootstrap-server localhost:9093

   # Verifying replication status and observing broker behavior during failures.
   ```
  

> Having multiple brokers in Kafka offers several key advantages: **Scalability** allows the system to handle higher data volumes by distributing partitions across brokers, ensuring load balancing (e.g., 12 partitions across 3 brokers). **Fault Tolerance** ensures uninterrupted service through replication; if one broker fails, another with replicated data takes over (e.g., replication factor of 2). **High Throughput** is achieved by parallel processing across brokers, reducing bottlenecks. **Reduced Latency** is possible as producers and consumers can connect to the nearest broker, minimizing delays in data transfer. These benefits make Kafka robust, efficient, and reliable for large-scale data streaming.

### **Command Categories and Scenarios**

| **Category**              | **Commands**                                                                     | **Scenarios**                                                                 |
| ------------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **Installation**          | Binary download, update `.zshrc`.                                                | Set up Kafka for the first time on MacOS.                                     |
| **Server Management**     | `zookeeper-server-start.sh`, `kafka-server-start.sh`.                            | Start essential services for Kafka operation.                                 |
| **Topic Management**      | `kafka-topics.sh --list`, `--describe`, `--create`, `--delete`.                  | Manage topics: create, describe, delete, and list.                            |
| **Producer Operations**   | `kafka-console-producer.sh`.                                                     | Send messages to Kafka topics, including key-value formatted data.            |
| **Consumer Operations**   | `kafka-console-consumer.sh`, `kafka-consumer-groups.sh`.                         | Consume messages from topics, manage consumer groups, and reset offsets.      |
| **Replication**           | `kafka-server-start.sh` for multiple brokers, `kafka-topics.sh` for replication. | Test topic replication and observe Kafka’s fault tolerance when brokers fail. |
| **Zookeeper Interaction** | `zookeeper-shell.sh`.                                                            | Interact with Zookeeper for cluster state management and troubleshooting.     |


### **Exercises**

Here are some intermediate-level exercises to deepen your understanding of Kafka and its features

### **1. Multi-Partition Topics and Consumer Groups**
- **Exercise**: Create a topic with multiple partitions (e.g., 3 partitions) and start multiple consumers in the same consumer group.
  - Produce messages to the topic and observe how Kafka distributes messages across partitions and consumers.
  - Add or remove consumers dynamically and see how Kafka rebalances the partitions among the group.
    

### **2. Custom Serialization and Deserialization**
- **Exercise**: Write a custom serializer and deserializer for a complex data type (e.g., a JSON object or a Protobuf message).
  - Create a Kafka producer that uses your custom serializer to send messages.
  - Create a Kafka consumer that uses your custom deserializer to read messages.


### **3. Kafka Streams Application**
- **Exercise**: Build a simple Kafka Streams application to process data in real-time.
  - For example, create a stream that reads from a topic, transforms the messages (e.g., convert text to uppercase), and writes the results to another topic.
  - Use the Kafka Streams DSL to define the processing logic.


### **4. Exactly-Once Semantics**
- **Exercise**: Configure a Kafka producer and consumer to achieve exactly-once semantics.
  - Enable idempotence and transactions in the producer.
  - Use a transactional consumer to read messages and commit offsets atomically.


### **5. Kafka Connect with File Source/Sink**
- **Exercise**: Set up Kafka Connect in standalone mode and use a file source connector to read data from a file and write it to a Kafka topic.
  - Then, use a file sink connector to write data from the Kafka topic to another file.
  - Experiment with different configurations (e.g., file formats, polling intervals).


### **6. Monitoring and Metrics**
- **Exercise**: Enable JMX for Kafka and use a monitoring tool (e.g., JConsole, Prometheus, or Grafana) to monitor Kafka metrics.
  - Track metrics like message throughput, latency, and broker performance.
  - Simulate high load and observe how Kafka handles it.

- **Learning Outcome**: Gain insights into Kafka's performance and monitoring capabilities.


### **7. Fault Tolerance and Recovery**
- **Exercise**: Simulate a broker failure and observe how Kafka recovers.
  - Stop the Kafka broker and see how producers and consumers behave.
  - Restart the broker and verify that it rejoins the cluster and resumes operations.


### **8. Log Compaction**
- **Exercise**: Create a log-compacted topic and experiment with key-value messages.
  - Produce messages with the same key and observe how Kafka retains only the latest value for each key.
  - Use a consumer to read the compacted log and verify the results.
    

### **9. Kafka Security (Optional)**
- **Exercise**: Enable SSL/TLS encryption and SASL authentication for your Kafka cluster.
  - Configure a producer and consumer to use the secure connection.
  - Test the setup by producing and consuming messages.


### **10. Kafka with Docker**
- **Exercise**: Set up a Kafka cluster using Docker and Docker Compose.
  - Create a multi-broker Kafka cluster with Zookeeper.
  - Experiment with scaling brokers and consumers.

- **Learning Outcome**: Learn how to containerize Kafka for easier deployment and testing.


### **11. Benchmarking Kafka**
- **Exercise**: Use Kafka's built-in performance tools (`kafka-producer-perf-test` and `kafka-consumer-perf-test`) to benchmark your cluster.
  - Measure throughput and latency under different workloads.
  - Experiment with different configurations (e.g., batch size, compression).
