from confluent_kafka import Consumer, KafkaError
import time
import json
import argparse
import statistics

latencies = []

def run_consumer(brokers, topic, group_id, max_messages):
    conf = {
        'bootstrap.servers': brokers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,
    }

    consumer = Consumer(conf)
    consumer.subscribe([topic])
    print(f"Consuming from topic '{topic}' with group '{group_id}'...")

    count = 0
    start_time = time.time()

    try:
        while count < max_messages:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Error: {msg.error()}")
                    continue

            try:
                payload = json.loads(msg.value().decode('utf-8'))
                send_time = payload.get("send_timestamp")
                receive_time = time.time()
                if send_time:
                    latencies.append(receive_time - send_time)
            except Exception as e:
                print(f"Failed to parse message: {e}")

            count += 1
            if count % 100 == 0:
                print(f"Consumed {count} messages...")

    finally:
        end_time = time.time()
        consumer.close()

        total_time = end_time - start_time
        throughput = count / total_time if total_time > 0 else 0

        print("\n✅ Consumption complete.")
        print(f"Total messages consumed: {count}")
        print(f"Total time: {total_time:.2f} seconds")
        print(f"Throughput: {throughput:.2f} messages/sec")

        if latencies:
            print(f"Latency (ms) - Avg: {statistics.mean(latencies)*1000:.2f}, "
                  f"P50: {statistics.median(latencies)*1000:.2f}, "
                  f"P95: {statistics.quantiles(latencies, n=100)[94]*1000:.2f}, "
                  f"P99: {statistics.quantiles(latencies, n=100)[98]*1000:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--brokers', required=True)
    parser.add_argument('--topic', default='latency-test')
    parser.add_argument('--group-id', default='latency-consumer-group')
    parser.add_argument('--max-messages', type=int, default=1000)
    args = parser.parse_args()

    run_consumer(args.brokers, args.topic, args.group_id, args.max_messages)
