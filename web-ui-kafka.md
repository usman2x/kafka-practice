# UI For Apache Kafka

Docker command is setting up the Kafka UI container and configuring it to connect to your local Kafka cluster
```
docker run -d \
  --name kafka-ui \
  -p 8080:8080 \
  -e KAFKA_CLUSTERS_0_NAME=local-kafka \
  -e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=host.docker.internal:9092 \
  provectuslabs/kafka-ui:latest
```

If you want to add Schema Registry or Kafka Connect, just extend it like this
```
docker run -d --name kafka-ui -p 8080:8080 \
-e KAFKA_CLUSTERS_0_NAME=local-kafka \
-e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=host.docker.internal:9092 \
-e KAFKA_CLUSTERS_0_SCHEMAREGISTRY=http://host.docker.internal:8081 \
-e KAFKA_CLUSTERS_0_KAFKACONNECT_0_NAME=my-connect \
-e KAFKA_CLUSTERS_0_KAFKACONNECT_0_ADDRESS=http://host.docker.internal:8083 \
provectuslabs/kafka-ui:latest
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



