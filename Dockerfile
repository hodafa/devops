# Use the official Python 3.9 image for the desired platform
FROM --platform=linux/amd64 python:3.9

# Set environment variables for AWS credentials and region
ENV AWS_ACCESS=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET=${AWS_SECRET_ACCESS_KEY}
ENV AWS_DEFAULT_REGION="eu-west-1"

# Install required packages
RUN pip install confluent-kafka boto3

# Copy the Python script into the container
COPY kafka_to_s3.py /app/kafka_to_s3.py

# Set the working directory
WORKDIR /app

# Run the Python script
CMD ["python", "kafka_to_s3.py"]

