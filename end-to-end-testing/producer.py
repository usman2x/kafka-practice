from confluent_kafka import Producer
import time
import json
import argparse
import uuid
import statistics

latencies = []

def delivery_report(err, msg, send_time):
    ack_time = time.time()
    if err:
        print(f"Delivery failed: {err}")
    else:
        latency = ack_time - send_time
        latencies.append(latency)

def run_producer(brokers, topic, message_count, message_size, throughput, acks, linger_ms, batch_num_messages, compression):
    conf = {'bootstrap.servers': brokers,
            'acks': acks,
            "linger.ms": linger_ms,
            "batch.num.messages": batch_num_messages,
            "compression.type": compression}
    
    producer = Producer(**conf)

    print(f"Producing {message_count} messages to topic '{topic}' with size {message_size}B")

    start_time = time.time()

    for i in range(message_count):
        send_time = time.time()
        message = {
            "id": str(uuid.uuid4()),
            "send_timestamp": send_time,
            "payload": "x" * (message_size - 100)
        }
        producer.produce(topic, value=json.dumps(message), callback=lambda err, msg, st=send_time: delivery_report(err, msg, st))

        if throughput > 0:
            time.sleep(1 / throughput)

        if i % 1000 == 0:
            print(f"Sent {i} messages...")

        producer.poll(0)

    producer.flush()
    end_time = time.time()

    total_time = end_time - start_time
    total_msgs = len(latencies)
    throughput_actual = total_msgs / total_time if total_time > 0 else 0

    print("\n✅ Production complete.")
    print(f"Total messages produced: {total_msgs}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Throughput: {throughput_actual:.2f} messages/sec")

    if latencies:
        print(f"Latency (ms) - Avg: {statistics.mean(latencies)*1000:.2f}, "
              f"P50: {statistics.median(latencies)*1000:.2f}, "
              f"P95: {statistics.quantiles(latencies, n=100)[94]*1000:.2f}, "
              f"P99: {statistics.quantiles(latencies, n=100)[98]*1000:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--brokers', required=True)
    parser.add_argument('--topic', default='latency-test')
    parser.add_argument('--count', type=int, default=1000)
    parser.add_argument('--size', type=int, default=200)
    parser.add_argument('--throughput', type=int, default=1000)
    parser.add_argument('--acks', choices=['0', '1', 'all'], default='1', help='Acknowledgment level')
    parser.add_argument('--linger-ms', type=int, default=0, help='Delay to batch messages in ms (default: 0)')
    parser.add_argument('--batch-num-messages', type=int, default=1000, help='Max messages per batch (default: 10000)')
    parser.add_argument('--compression', choices=['none', 'gzip', 'snappy', 'lz4', 'zstd'], default='none', help='Compression type')

    args = parser.parse_args()


    run_producer(args.brokers, args.topic, args.count, args.size, args.throughput, args.acks,args.linger_ms,args.batch_num_messages,args.compression)
