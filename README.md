# MediaStream Analytics

This repository contains the architecture and codebase for the **MediaStream Analytics** project, which aims to deliver real-time and batch insights from media consumption data using AWS services.

## 📦 Project Structure

- `real_time/` – Python script to simulate and stream viewership logs to Amazon Kinesis.
- `batch/` – CSV files for ad revenue, channel metadata, and demographics.
- `glue_jobs/` – AWS Glue scripts for data transformation.
- `airflow_dags/` – Apache Airflow DAGs to orchestrate Glue jobs.
- `athena_queries/` – SQL queries for analytics using AWS Athena.
- `dashboards/` – QuickSight dashboard assets and configurations.

## 🚀 Technologies Used

- AWS Kinesis, EMR, S3, Glue, Athena, Snowflake, QuickSight
- Apache Airflow
- Python, Spark

## 📈 Business Goals

- Real-time and batch analytics for media decision-making.
- KPI dashboards for ad revenue, engagement, and demographics.

---

Feel free to contribute or customize the structure as needed.
