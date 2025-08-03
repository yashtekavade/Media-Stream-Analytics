# Media Stream Analytics

A real-time media streaming analytics platform built on AWS services for processing and analyzing viewership data.

## 🏗️ Architecture Overview

This project implements a complete data pipeline for media streaming analytics using:

- **Amazon Kinesis** - Real-time data streaming
- **AWS Glue** - ETL processing and data transformation
- **AWS Lambda** - Serverless compute for triggers
- **Apache Airflow** - Workflow orchestration
- **Snowflake** - Data warehousing
- **Amazon EMR Spark** - Distributed data processing

## 📁 Project Structure

```
Media-Stream-Analytics/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── docs/                    # Documentation
│   └── Version_1_AWS_Project_2.pdf
├── src/                     # Source code
│   ├── airflow/            # Airflow DAGs
│   │   └── dags/
│   │       └── media_analytics_dag.py
│   ├── kinesis/            # Kinesis streaming components
│   │   ├── data_generator.py     # Generates sample data
│   │   └── stream_processor.py   # Processes Kinesis streams
│   ├── glue/               # AWS Glue ETL jobs
│   │   └── etl_job.py
│   ├── lambda/             # Lambda functions
│   │   ├── requirements.txt
│   │   └── trigger_airflow_dag.py
│   └── data_generation/    # Data generation utilities
│       └── generate_media_data.py
└── infrastructure/         # Infrastructure setup
    └── snowflake_setup.txt
```

## 🚀 Features

- **Real-time Data Ingestion**: Continuous streaming of viewership data via Kinesis
- **ETL Processing**: Automated data transformation using AWS Glue
- **Workflow Orchestration**: Managed data pipelines with Apache Airflow
- **Scalable Processing**: Distributed computing with EMR Spark
- **Data Warehousing**: Optimized storage and querying with Snowflake
- **Serverless Triggers**: Event-driven processing with Lambda functions

## 📊 Data Flow

1. **Data Generation** → Media viewership data is generated and streamed
2. **Kinesis Ingestion** → Real-time data streaming to Kinesis Data Streams
3. **Lambda Trigger** → Serverless functions trigger downstream processing
4. **Glue ETL** → Data transformation and cleaning
5. **EMR Spark** → Large-scale data processing
6. **Snowflake** → Data warehousing and analytics
7. **Airflow Orchestration** → Workflow management and scheduling

## 🛠️ Setup Instructions

### Prerequisites

- AWS Account with appropriate permissions
- Python 3.8+
- Apache Airflow
- Snowflake account

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yashtekavade/Media-Stream-Analytics.git
   cd Media-Stream-Analytics
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS credentials**
   ```bash
   aws configure
   ```

4. **Set up Kinesis Data Stream**
   - Create a Kinesis Data Stream named `viewership-stream`
   - Configure appropriate shard count based on expected throughput

5. **Deploy Glue Job**
   - Upload the Glue ETL script to S3
   - Create AWS Glue job with appropriate IAM roles

6. **Configure Airflow**
   - Deploy DAGs to your Airflow environment
   - Set up AWS connections in Airflow

7. **Set up Snowflake**
   - Follow instructions in `infrastructure/snowflake_setup.txt`

## 🔧 Usage

### Running Data Generation
```bash
python src/data_generation/generate_media_data.py
```

### Streaming Data to Kinesis
```bash
python src/kinesis/data_generator.py
```

### Triggering Airflow DAG
Deploy the Lambda function and configure appropriate triggers, or manually trigger via Airflow UI.

## 📋 Components Description

### Kinesis Components
- **data_generator.py**: Streams viewership data to Kinesis
- **stream_processor.py**: Processes data from Kinesis using EMR Spark

### Airflow DAGs
- **media_analytics_dag.py**: Orchestrates the complete ETL pipeline

### AWS Glue
- **etl_job.py**: Performs data transformation and loading

### Lambda Functions
- **trigger_airflow_dag.py**: Triggers Airflow workflows based on events

## 🔍 Monitoring & Logging

- Monitor Kinesis streams via CloudWatch
- Track Glue job execution in AWS Glue console
- Monitor Airflow DAG runs in Airflow UI
- View Lambda function logs in CloudWatch Logs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 📞 Contact

For questions or support, please reach out to the project maintainer.

---

**Note**: Make sure to configure all AWS services with appropriate IAM roles and security groups before running the pipeline.
