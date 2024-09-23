# Pinterest Data Pipeline

## Table of Contents

1. [Project Description](#project-description)
2. [Installation Instructions](#installation-instructions)
3. [Usage Instructions](#usage-instructions)
   - [S3 Objects](#s3-objects)
   - [S3 Batch Processing](#s3-batch-processing)
   - [Databricks Spark](#databricks-spark)
   - [Airflow DAG](#airflow-dag)
   - [Streaming](#streaming)
4. [File Structure](#file-structure)
5. [License](#license)

## Project Description

The Pinterest Data Pipeline is designed to process and analyze data resembling the data received by the Pinterest API when a post request is made by a user uploading data to Pinterest. The project involves setting up various AWS services and tools to manage, store, and analyze data, including Apache Kafka, Amazon MSK, AWS S3, Databricks, and Airflow.

### What the Project Does

- **Data Ingestion:** Simulates data ingestion from Pinterest API into Kafka topics.
- **Data Storage:** Stores data in AWS S3 buckets for both batch and streaming processing.
- **Data Processing:** Utilizes Databricks for batch and streaming data processing.
- **Data Management:** Configures Airflow for orchestrating workflows and scheduling tasks.

### What I Learned

- Configuring and using Amazon MSK with Apache Kafka.
- Setting up and managing AWS S3 for data storage.
- Integrating AWS API Gateway with Kafka using Kafka REST Proxy.
- Performing batch and streaming data processing with Databricks.
- Orchestrating workflows with Apache Airflow on AWS MWAA.

## Installation Instructions

1. **Install Apache Kafka on Client EC2:**
   - Download the Kafka version 2.13-2.8.1 from the [Apache Kafka website](https://kafka.apache.org/downloads).
   - Extract and install Kafka following the instructions [here](https://kafka.apache.org/quickstart).

2. **Install IAM MSK Authentication Package:**
   - If using Python, install the package with `pip`:
     ```bash
     pip3 install aws-msk-iam-auth
     ```

3. **Configure Kafka Client:**
   - Edit the `client.properties` file to include the necessary configurations for AWS IAM authentication.

4. **Set Up S3 Bucket:**
   - Ensure your AWS S3 bucket is configured to receive data from the MSK cluster.

## Usage Instructions

### S3 Objects

1. **Kafka Topics Creation:**
   - Create the following topics:
     ```bash
     ./bin/kafka-topics.sh --create --bootstrap-server b-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098 --replication-factor 3 --partitions 3 --topic 1226d593b7e7.pin
     ./bin/kafka-topics.sh --create --bootstrap-server b-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098 --replication-factor 3 --partitions 3 --topic 1226d593b7e7.geo
     ./bin/kafka-topics.sh --create --bootstrap-server b-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098 --replication-factor 3 --partitions 3 --topic 1226d593b7e7.user
     ```

2. **API and Kafka REST Proxy Integration:**
   - Set up an API in AWS API Gateway to send data to the MSK cluster.
   - Configure Kafka REST Proxy on your EC2 client to handle HTTP requests and interact with Kafka topics.

### S3 Batch Processing

1. **Mount S3 Bucket to Databricks:**
   - Mount the S3 bucket to your Databricks account.
   - Read data from the S3 bucket and perform batch processing using Spark.

### Databricks Spark

1. **Configure Databricks for Spark Processing:**
   - Load data into Databricks and perform transformations.
   - Save the processed data into Delta tables.

### Airflow DAG

1. **Orchestrate Workflows with Airflow:**
   - Upload a Directed Acyclic Graph (DAG) to the AWS MWAA environment.
   - Schedule and trigger the DAG to run at specified intervals.

### Streaming

1. **Read and Process Streaming Data:**
   - Configure your REST API to interact with Kinesis streams.
   - Process streaming data in Databricks and store results in Delta tables.

## File Structure

- `kafka_2.13-2.8.1/` - Directory containing Kafka binaries and configuration files.
- `s3/` - Contains configuration and setup files for AWS S3 integration.
- `databricks/` - Databricks notebooks and scripts for batch and streaming processing.
- `airflow/` - Airflow DAG files for orchestrating workflows.
- `user_posting_emulation.py` - Script for emulating user data posting to the API.

## License

This project is licensed under the [MIT License](LICENSE).
