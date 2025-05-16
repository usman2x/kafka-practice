# Kafka Producer Performance Testing

Kafka producer performance testing is crucial for evaluating the throughput, latency, and scalability of your Kafka cluster under different workloads. It helps you:

* Measure Throughput : Determine how many messages per second your Kafka cluster can handle.
* Analyze Latency : Understand the time taken for messages to be sent and acknowledged by the broker.
* Validate Configuration : Test the impact of broker and producer configurations (e.g., compression, batch size, replication) on performance.
* Plan Capacity : Identify bottlenecks and plan for scaling your Kafka infrastructure to meet production demands.

```
kafka-producer-perf-test.sh \
  --topic performance-test \
  --num-records 1000000 \
  --record-size 1024 \
  --throughput -1 \
  --producer-props bootstrap.servers=localhost:9092

# --topic performance-test: The Kafka topic to send messages to.
# --num-records 1000000: Total number of records to send.
# --record-size 1024: Size of each record in bytes (1 KB).
# --throughput -1: Unlimited throughput (-1 means no limit).
# --producer-props bootstrap.servers=localhost:9092: Kafka broker address.
```

To create multiple Kafka topics with varying configurations (partitions and replication factors), you can use the kafka-topics.sh script. 
Below is an example of how to create three topics (topic-1, topic-2, topic-3) with different settings:

**1. Topic-1 : 6 partitions, replication factor of 3, Good for high-throughput, fault-tolerant scenarios.** 

```
kafka-topics.sh --bootstrap-server localhost:9092 \
  --create --topic topic-1 \
  --partitions 6 \
  --replication-factor 3
```

**Topic-2 : 12 partitions, replication factor of 2, Optimized for high parallelism with moderate fault tolerance.**

```
kafka-topics.sh --bootstrap-server localhost:9092 \
  --create --topic topic-2 \
  --partitions 12 \
  --replication-factor 2
```

**Topic-3 : 3 partitions, replication factor of 1, Suitable for low-latency, single-broker setups.**

```
kafka-topics.sh --bootstrap-server localhost:9092 \
  --create --topic topic-3 \
  --partitions 3 \
  --replication-factor 1
```

Once the topics are created, you can run performance tests on each topic to evaluate how their configurations (partitions and replication factors) impact throughput, latency, and scalability.

1. Test Each Topic Individually : Run the kafka-producer-perf-test tool for each topic.
2. Adjust Parameters : Customize parameters like --num-records, --record-size, and --throughput to simulate different workloads.
3. Analyze Results : Compare the performance metrics (throughput, latency) across topics to understand the impact of partitions and replication factors.

# Key Observations

**Impact of Partitions :**
* More partitions generally allow higher parallelism, which can increase throughput.
* However, too many partitions may lead to increased overhead and latency.
  
**Impact of Replication Factor :**
* Higher replication factors improve fault tolerance but reduce write throughput due to the need for replication across brokers.

**Acknowledgment Mode :**
* Adjust acknowledgment settings (acks) to balance durability and performance `--producer-props acks=all`

1. **`acks=0`**
- The producer sends messages without waiting for any acknowledgment from the broker.  
- Provides the highest throughput and lowest latency but no guarantee of message delivery.  
- Suitable for non-critical use cases where occasional data loss is acceptable.

---

2. **`acks=1`**
- The producer waits for an acknowledgment from the leader broker only.  
- Balances performance and durability but risks data loss if the leader crashes before replication.  
- Ideal for general-purpose use cases requiring moderate reliability.

---

3. **`acks=all`**
- The producer waits for acknowledgments from all in-sync replicas (ISRs).  
- Ensures the highest level of durability and fault tolerance at the cost of higher latency.  
- Best suited for mission-critical applications where data loss must be avoided.
