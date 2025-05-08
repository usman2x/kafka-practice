# UI For Apache Kafka

Some Considerations before deep dive into Kafka-UI
* Kafka UI is a management tool, not a Kafka broker. It requires an existing Kafka cluster to connect to.
* It’s great for testing and exploring Kafka without writing code or using complex CLI commands.
* It supports creating topics, producing messages, and monitoring consumer lag.
* You can integrate it with Kafka Connect and Schema Registry for a more complete data pipeline.
* It doesn’t include built-in consumers, but you can easily create one using Java/Spring or any other Kafka client library.


Docker command is setting up the Kafka UI container and configuring it to connect to your local Kafka cluster
```
docker run -d \
  --name kafka-ui \
  -p 8080:8080 \
  -e KAFKA_CLUSTERS_0_NAME=local-kafka \
  -e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=host.docker.internal:9092 \
  ghcr.io/kafka-ui:latest
```

You can define multiple clusters in the environment variables:
```
environment:
  - KAFKA_CLUSTERS_0_NAME=dev-cluster
  - KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=localhost:9092
  - KAFKA_CLUSTERS_1_NAME=prod-cluster
  - KAFKA_CLUSTERS_1_BOOTSTRAPSERVERS=localhost:9093
```


If you want to add Schema Registry or Kafka Connect, just extend it like this
```
docker run -d --name kafka-ui -p 8080:8080 \
-e KAFKA_CLUSTERS_0_NAME=local-kafka \
-e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=host.docker.internal:9092 \
-e KAFKA_CLUSTERS_0_SCHEMAREGISTRY=http://host.docker.internal:8081 \
-e KAFKA_CLUSTERS_0_KAFKACONNECT_0_NAME=my-connect \
-e KAFKA_CLUSTERS_0_KAFKACONNECT_0_ADDRESS=http://host.docker.internal:8083 \
ghcr.io/kafka-ui:latest
```

Check if the Container is Running
`docker ps | grep kafka-ui`

Check if the Container Exists but is Stopped
`docker ps -a | grep kafka-ui`

Start an Existing (Stopped) Container
`docker start kafka-ui`

If you want to recreate it with updated settings:
```
docker stop kafka-ui
docker rm kafka-ui
```
Then, recreate it with your original docker run command.



