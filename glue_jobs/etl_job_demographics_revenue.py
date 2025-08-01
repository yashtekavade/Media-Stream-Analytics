from pyspark.sql import SparkSession

# Initialize SparkSession with Iceberg support
spark = SparkSession.builder \
    .appName("Glue Iceberg Table CDC") \
    .config("spark.sql.catalog.glue_catalog", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.glue_catalog.catalog-impl", "org.apache.iceberg.aws.glue.GlueCatalog") \
    .config("spark.sql.catalog.glue_catalog.warehouse", "s3://tbsm-icebergtable/") \
    .config("spark.sql.catalog.glue_catalog.io-impl", "org.apache.iceberg.aws.s3.S3FileIO") \
    .getOrCreate()

# Create Glue database if not exists
spark.sql("CREATE DATABASE IF NOT EXISTS glue_catalog.tbsm_icebergdb")

# Read demographics CSV from S3
df = spark.read.option("header", True).csv("s3://tbsm-calm/ice/demographics.csv")
df.show()

# Create Iceberg table if not exists
spark.sql("""
CREATE TABLE IF NOT EXISTS glue_catalog.tbsm_icebergdb.demographics (
    user_id STRING,
    gender STRING,
    age_group STRING,
    region STRING,
    subscription_type STRING
)
USING ICEBERG
""")

# Register DataFrame as temporary view
df.createOrReplaceTempView("updates")

# Perform MERGE (upsert) into Iceberg table
spark.sql("""
MERGE INTO glue_catalog.tbsm_icebergdb.demographics AS target
USING updates AS source
ON target.user_id = source.user_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
""")

print("✅ Merge operation completed successfully.")
