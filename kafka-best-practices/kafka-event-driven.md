Kafka for event-driven communication between micro services (Spring Boot-based)

| **Component**            | **Tech Stack**                                         |
|--------------------------|--------------------------------------------------------|
| **Issue Service**        | Spring Boot + Kafka Producer                           |
| **Garbage Service**      | Spring Boot + Kafka Consumer                           |
| **Sewerage Service**     | Spring Boot + Kafka Consumer                           |
| **Dashboarding Service** | Spring Boot + Kafka Consumer + REST API                |
| **Kafka Topics**         | `issue.reported`, `task.scheduled`, `task.resolved`, `task.failed` |
| **Frontend Dashboard**   | React + Mapbox / Google Maps                           |
| **Database**             | MongoDB (flexible schema, geo indexing)                |
| **Containerization**     | Docker + Docker Compose                                |
| **Monitoring (optional)**| Grafana + Prometheus                                   |
