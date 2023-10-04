#!/bin/python3
import time
from confluent_kafka import Consumer, KafkaError
import boto3
import os

# Kafka configuration
kafka_bootstrap_servers = '172.31.100.169:9092,172.31.101.10:9092,172.31.99.207:9092'
kafka_topic = 'k8e_monitoring'

# AWS S3 configuration
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_default_region = os.getenv('AWS_DEFAULT_REGION')
s3_bucket_name = 'elementor-data-candidates-bucket'
s3_folder = 'hodaf-cpu'

# Kafka consumer configuration
conf = {
    'bootstrap.servers': kafka_bootstrap_servers,
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe([kafka_topic])

# AWS S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  region_name=aws_default_region)

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            # End of partition event - not an error
            continue
        else:
            print(msg.error())
            break

    kafka_message_value = msg.value().decode('utf-8')

    timestamp = int(time.time())  # Get current timestamp
    file_name = f'{timestamp}.txt'

    # Upload data 
    s3_object_key = f'{s3_folder}/{file_name}'
    s3.put_object(Body=kafka_message_value, Bucket=s3_bucket_name, Key=s3_object_key)
    print(f'Successfully uploaded message to S3 file: {file_name}')

    # Sleep for 60 seconds 
    time.sleep(60)

consumer.close()

