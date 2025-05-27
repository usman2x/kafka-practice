#!/bin/bash

# Create a Kafka topic named 'latency-test' with 10 partitions and a replication factor of 3
kafka-topics.sh --create --topic latency-test --partitions 10 --replication-factor 3 --bootstrap-server localhost:9092

# Produce messages to the 'latency-test' topic
python producer.py \
 --brokers localhost:9092,localhost:9093,localhost:9094 \
 --topic latency-test \
 --count 10000 \
 --size 500 \
 --throughput 500 \
 --acks all

# Consume messages from the 'latency-test' topic
python consumer.py \
  --brokers localhost:9092,localhost:9093,localhost:9094 \
  --topic latency-test \
  --group-id latency-group \
  --max-messages 1000
