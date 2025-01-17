### **Kafka on Docker Cheat Sheet**

---

### **1. Basic Commands**
- **Start Kafka Cluster**:
  ```bash
  docker-compose up -d
  ```
  - Starts Kafka brokers (`kafka1`, `kafka2`, `kafka3`).
  - Expects a `docker-compose.yml` file.

- **Stop Kafka Cluster**:
  ```bash
  docker-compose down
  ```

- **List Running Containers**:
  ```bash
  docker ps
  ```

- **List All Containers**:
  ```bash
  docker ps -a
  ```

---

### **2. Kafka CLI Commands**

- **Create a Topic**:
  ```bash
  docker exec -it kafka1 kafka-topics --create \
    --topic test-replication \
    --bootstrap-server localhost:9092 \
    --partitions 3 \
    --replication-factor 3
  ```

- **Describe a Topic**:
  ```bash
  docker exec -it kafka1 kafka-topics --describe \
    --topic test-replication \
    --bootstrap-server localhost:9092
  ```

- **Produce Messages**:
  ```bash
  docker exec -it kafka1 kafka-console-producer \
    --topic test-replication \
    --bootstrap-server localhost:9092
  ```

- **Consume Messages**:
  ```bash
  docker exec -it kafka1 kafka-console-consumer \
    --topic test-replication \
    --bootstrap-server localhost:9092 \
    --from-beginning
  ```

---

### **3. Kafka Cluster Metadata**
- **Describe Cluster**:
  ```bash
  docker exec -it kafka1 kafka-admin-client --bootstrap-server localhost:9092 --describe-cluster
  ```

- **Check Broker List**:
  ```bash
  docker exec -it kafka1 kafka-broker-api-versions --bootstrap-server localhost:9092
  ```

---

### **4. Replication Factor**
- **Check Replication**:
  ```bash
  docker exec -it kafka1 kafka-topics --describe --bootstrap-server localhost:9092
  ```
  - Shows replication details (Leader, Replicas, In-Sync Replicas).

- **Test Broker Failure**:
  - Stop one broker (e.g., `kafka2`):
    ```bash
    docker stop kafka2
    ```
  - Verify partition reassignment using:
    ```bash
    docker exec -it kafka1 kafka-topics --describe --bootstrap-server localhost:9092
    ```

---


### **6. Docker Management**
- **Exit Docker Container**:
  ```bash
  exit
  ```
  OR
  ```bash
  Ctrl + P, Ctrl + Q
  ```
- **Stop a Container**:
  ```bash
  docker stop <container_name>
  ```

- **Remove a Container**:
  ```bash
  docker rm <container_name>
  ```
