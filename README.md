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
   kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-consumer-group --reset-offsets --to-earliest --execute --topic multi-partition-topic
   ```

   - After this, use the `describe` command to observe the updated offset.

#### **Replication and Multiple Brokers**

1. **Start a second broker:**

   ```
   kafka-server-start.sh /Users/user/kafka/config/server-2.properties
   ```

2. **Connect to Zookeeper shell:**

   ```
   zookeeper-shell.sh localhost:2181
   ```

3. **Create a topic with replication factor:**

   ```
   kafka-topics.sh --create --topic replicated-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 2
   ```

   - Note: This will fail if only one broker is running. To resolve, start a second broker.

4. **Describe topic to view replicas:**

   ```
   kafka-topics.sh --describe --topic replicated-topic --bootstrap-server localhost:9093
   ```

   - Shut down one broker to observe how Kafka handles replication.

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
