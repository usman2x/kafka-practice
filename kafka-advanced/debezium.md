# Debezium
Debezium is a distributed platform that captures row-level changes in databases and streams them as events to Apache Kafka, enabling applications to react to these changes in real-time. It acts as a change data capture (CDC) solution by monitoring database transaction logs (or equivalent) and transforming these changes into structured events that can be consumed by other system.

**Understand the Data Flow**
Debezium captures CDC (Change Data Capture) events from the source and emits insert/update/delete messages to Kafka topics. These events are typically consumed and applied by downstream systems.

### Q1: Data is being deleted in the source DB but NOT deleted in the destination. What should I do?

**Step 1: Confirm Debezium Emits Delete Events**

* In the Debezium connector config:

```json
"delete.enabled": true,
"tombstones.on.delete": true
```

* These settings:

  * Emit a `"delete"` event
  * Optionally emit a **tombstone** message (`value: null`) for log compaction

**Step 2: Check Delete Events in Kafka**

Run this command:

```bash
kafka-console-consumer.sh \
  --topic dbserver1.inventory.customers \
  --from-beginning \
  --property print.key=true \
  --property print.value=true \
  --bootstrap-server localhost:9092
```

Look for delete events like:

```json
{
  "op": "d",
  "before": { "id": 42, "name": "John" },
  "after": null
}
```

And tombstone messages:

```json
{
  "key": { "id": 42 },
  "value": null
}
```

**Step 3: Check Sink Connector Configuration**

If using JDBC Sink for destination DB:

```json
"insert.mode": "upsert",
"delete.enabled": true,
"pk.mode": "record_key",
"pk.fields": "id"
```

**Other sinks (like Elasticsearch or custom consumers)** must be configured to:

* Support `value: null` (tombstones)
* Perform deletes when receiving delete or tombstone events

### Q2: What is the format of data Debezium uses to send events?

By default, Debezium uses **JSON (or Avro/Protobuf if configured)**. Here's the structure of a change event:

```json
{
  "before": { "id": 1, "name": "Alice" },
  "after": { "id": 1, "name": "Alicia" },
  "op": "u",               // c = create, u = update, d = delete
  "source": {
    "db": "inventory",
    "table": "customers"
  },
  "ts_ms": 1720117200000
}
```

On **delete**:

```json
{
  "before": { "id": 1, "name": "Alice" },
  "after": null,
  "op": "d"
}
```


### Q3: How to ensure event data message validation (no corrupted data)?

**Use Schema Validation via Confluent Schema Registry**

Debezium with Avro:

```json
"value.converter": "io.confluent.connect.avro.AvroConverter",
"value.converter.schema.registry.url": "http://localhost:8081"
```

This ensures:

* All messages follow a **schema**
* Any corrupted message (schema mismatch or invalid fields) is rejected

**Enable Dead Letter Queue (DLQ) in Kafka Connect**

If corrupted messages are received:

```json
"errors.tolerance": "all",
"errors.deadletterqueue.topic.name": "dlq-topic",
"errors.log.enable": true
```

All problematic events go to `dlq-topic` for later inspection.

**Use Custom Deserialization Exception Handler**

Kafka Streams or Kafka Consumer:

```java
props.put(StreamsConfig.DEFAULT_DESERIALIZATION_EXCEPTION_HANDLER_CLASS_CONFIG,
          LogAndContinueExceptionHandler.class);
```

### Q4: How to check data quality and consistency in Debezium?**

**A. Verify Source and Destination Row Counts**

Run SQL on source and destination:

```sql
-- On source
SELECT COUNT(*) FROM customers;

-- On destination
SELECT COUNT(*) FROM customers;
```

Mismatch? Investigate further.

**B. Compare Specific Rows**

```sql
-- On source
SELECT * FROM customers WHERE id = 101;

-- On destination
SELECT * FROM customers WHERE id = 101;
```

**C. Use Debezium Heartbeat Topic**

Configure:

```json
"heartbeat.interval.ms": 10000,
"heartbeat.topics.prefix": "__debezium_heartbeat"
```

Watch the topic:

```bash
kafka-console-consumer.sh \
  --topic __debezium_heartbeat.dbserver1 \
  --from-beginning \
  --bootstrap-server localhost:9092
```

Confirms the connector is alive and not stalled.


**D. Use Checksums for Field-Level Validation**

Create a hash of important fields:

```sql
-- Source
SELECT id, md5(concat_ws('|', name, email, status)) AS checksum FROM customers;

-- Destination
SELECT id, md5(concat_ws('|', name, email, status)) AS checksum FROM customers;
```

Mismatch = data corruption or sync failure.
