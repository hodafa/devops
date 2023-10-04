#!/bin/python3
import psutil
import time
from confluent_kafka import Producer

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = '172.31.100.169:9092,172.31.101.10:9092,172.31.99.207:9092'
KAFKA_TOPIC = 'k8e_monitoring'

# get current CPU usage - 1
def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)  # Get CPU usage in the last 1 second
    return cpu_usage

# send data to Kafka topic - 2
def send_to_kafka(data):
    producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})
    producer.produce(KAFKA_TOPIC, value=str(data))
    producer.flush()

# Main function 1+2
def main():
    print('App is running and sending messages to Kafka. Press Ctrl+C to exit.')
    
    try:
        while True:
            cpu_level = get_cpu_usage()
            print(f'Current CPU Level: {cpu_level}%')
            send_to_kafka(cpu_level)  # Send CPU level to Kafka topic
            print('Message sent to Kafka successfully!')
            time.sleep(60)  # Sleep for 1 minute before the next reading

    except KeyboardInterrupt:
        print('Exiting...')

if __name__ == "__main__":
    main()

