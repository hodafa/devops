## Introduction
This repository contains a Python application that monitors CPU usage and sends the data to a Kafka topic. Additionally, it includes configurations for Kafka, Kafka-S3 integration, and Kubernetes deployment files. The repository provides Helm charts for simplified deployment. The applications and services are containerized and stored on Docker Hub for easy access.

### Application Overview
- `my-python-app-chart`: Helm chart for the Python CPU monitoring application.
- `statefulset.yaml` and `svc-kafka.yaml`: Kubernetes configurations for Kafka deployment.
- `kafka-connect.yaml`: Configuration for Kafka Connect service.
- `kafka-client.yaml`: Client configuration for Kafka.
- `kafka_to_s3.py`: Python script for consuming messages from Kafka and storing them in AWS S3.
- `Dockerfile` for `kafka_to_s3.py`: Dockerfile for building the Kafka to S3 Python application.
- `kafka-s3-app-deployment.yaml`: Deployment configuration for the Kafka-S3 integration application.


## Stage 1: Deploying CPU Monitoring App
To deploy the CPU monitoring application, use the Helm chart provided in the repository.

## **Stage 2: Setting Up Kafka**
For Kafka deployment, use the following Kubernetes manifests:

Deploy Kafka StatefulSet and Service
kubectl apply -f statefulset.yaml
kubectl apply -f svc-kafka.yaml


## **Stage 3: Kafka-S3 Integration Deployment**
For deploying the Kafka-S3 integration application, use the following configuration:
located in the same dir where Dockerfile is
the real values will be in .env file
(or we can place it in other dir, but then specify the location inside dockerfile)
we can generate .env file on startup, having the values in Vault or similar

Deploy Kafka-S3 Integration App
kubectl apply -f kafka-s3-app-deployment.yaml




## Additional Information
The Kafka-S3 integration application is available as a Docker image on Docker Hub: Docker Image Link
Ensure that appropriate configurations (e.g., AWS credentials, Kafka connection details) are set in the kafka_to_s3.py script before deployment.

##kafka-connect
due to time shortage (from my side, there were some unexpected day-job errands), I havent reach the final step with  kafka-connect (where the data is actually saved on S3) 
I did go over the documentation, and were able to start all the necessary components, however it seems like the last point is to pass the source/sink configuration  # Source Connector Configuration (Reading from Kafka){  "name": "kafka-source-connector",  "config": {    "connector.class": "io.confluent.connect.kafka.KafkaSourceConnector",    "tasks.max": "1",    "topics": "test",  # Specify the source topic here     "key.converter": "org.apache.kafka.connect.converters.ByteArrayConverter",    "value.converter": "org.apache.kafka.connect.converters.ByteArrayConverter",    "key.converter.schemas.enable": "false",    "value.converter.schemas.enable": "false"  }} # Sink Connector Configuration (Writing to AWS S3){  "name": "s3-sink-connector",  "config": {    "connector.class": "io.confluent.connect.s3.S3SinkConnector",    "tasks.max": "1",    "topics": "test",  # Specify the source topic here     "s3.bucket.name": "test-bucket",  # Specify your AWS S3 bucket name     "s3.region": "us-east-1",  # Specify your AWS region     "storage.class": "io.confluent.connect.s3.storage.S3Storage",    "format.class": "io.confluent.connect.s3.format.avro.AvroFormat",    "schema.generator.class": "io.confluent.connect.storage.hive.schema.DefaultSchemaGenerator",    "flush.size": "1000",    "rotate.interval.ms": "60000",    "schema.compatibility": "BACKWARD",    "partitioner.class": "io.confluent.connect.storage.partitioner.TimeBasedPartitioner",    "path.format": "'year'=YYYY/'month'=MM/'day'=dd/'hour'=HH/'minute'=mm",    "locale": "US",    "timezone": "UTC"  }} )

