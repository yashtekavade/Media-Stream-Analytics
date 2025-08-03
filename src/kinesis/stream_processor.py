from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, split
from pyspark.sql.types import *
 
# 1. Define the schema of the CSV-style records
schema = StructType([
    StructField("session_id", StringType()),
    StructField("user_id", StringType()),
    StructField("channel_id", StringType()),
    StructField("channel_name", StringType()),
    StructField("show_name", StringType()),
    StructField("genre", StringType()),
    StructField("timestamp", StringType()),
    StructField("duration_minutes", IntegerType()),
    StructField("region", StringType()),
    StructField("subscription_type", StringType()),
    StructField("device", StringType()),
    StructField("platform", StringType()),
    StructField("is_live", StringType()),
    StructField("ads_watched", IntegerType()),
    StructField("ad_revenue", FloatType()),
    StructField("engagement_score", FloatType()),
    StructField("buffer_count", IntegerType()),
    StructField("completion_percentage", FloatType())
])
 
# 2. Initialize Spark Session
print("🚀 Initializing Spark session...")
spark = SparkSession.builder \
    .appName("KinesisToS3AndSnowflake") \
    .getOrCreate()
 
print("✅ Spark session initialized.")
 
# 3. Read from Kinesis
print("🔄 Connecting to Kinesis...")
df_raw = spark.readStream \
    .format("kinesis") \
    .option("streamName", "viewership-stream") \
    .option("endpointUrl", "https://kinesis.ap-southeast-2.amazonaws.com") \
    .option("region", "ap-southeast-2") \
    .option("startingPosition", "LATEST") \
    .load()
print("✅ Connected to Kinesis.")
 
# 4. Convert and split raw records
df_string = df_raw.withColumn("data_string", expr("CAST(data AS STRING)"))
df_split = df_string.withColumn("fields", split(col("data_string"), ","))
 
# 5. Assign to structured schema
df_parsed = df_split.select(
    col("fields").getItem(0).alias("session_id"),
    col("fields").getItem(1).alias("user_id"),
    col("fields").getItem(2).alias("channel_id"),
    col("fields").getItem(3).alias("channel_name"),
    col("fields").getItem(4).alias("show_name"),
    col("fields").getItem(5).alias("genre"),
    col("fields").getItem(6).alias("timestamp"),
    col("fields").getItem(7).cast("int").alias("duration_minutes"),
    col("fields").getItem(8).alias("region"),
    col("fields").getItem(9).alias("subscription_type"),
    col("fields").getItem(10).alias("device"),
    col("fields").getItem(11).alias("platform"),
    col("fields").getItem(12).alias("is_live"),
    col("fields").getItem(13).cast("int").alias("ads_watched"),
    col("fields").getItem(14).cast("float").alias("ad_revenue"),
    col("fields").getItem(15).cast("float").alias("engagement_score"),
    col("fields").getItem(16).cast("int").alias("buffer_count"),
    col("fields").getItem(17).cast("float").alias("completion_percentage")
)
 
# 6. Function to write batch to S3 and Snowflake
def write_batch(batch_df, epoch_id):
    print(f"🔁 Processing batch {epoch_id}...")
 
    record_count = batch_df.count()
    print(f"📦 Records in batch: {record_count}")
 
    if record_count == 0:
        print("⚠️ Empty batch. Skipping writes.")
        return
 
    try:
        # Snowflake options
        snowflake_options = {
            "sfURL": "vdhiuox-lib93136.snowflakecomputing.com",
            "sfUser": "YASHTEKAVADE",
            "sfPassword": "Yashvardhan@420",
            "sfDatabase": "TBSM_DB",
            "sfSchema": "PUBLIC",
            "sfWarehouse": "COMPUTE_WH",
            "sfRole": "ACCOUNTADMIN"
        }
 
        print("⛅ Writing to Snowflake...")
        batch_df.write \
            .format("net.snowflake.spark.snowflake") \
            .options(**snowflake_options) \
            .option("dbtable", "VIEWERSHIP_LOGS") \
            .mode("append") \
            .save()
        print("✅ Write to Snowflake succeeded.")
 
    except Exception as e:
        print("❌ Error writing to Snowflake:", e)
 
    try:
        print("📤 Writing to S3...")
        batch_df.write \
            .format("csv") \
            .mode("append") \
            .save("s3://tbsm-encore/view/")
        print("✅ Write to S3 succeeded.")
 
    except Exception as e:
        print("❌ Error writing to S3:", e)
 
# 7. Start the streaming query
print("📡 Starting streaming query...")
query = df_parsed.writeStream \
    .foreachBatch(write_batch) \
    .outputMode("append") \
    .option("checkpointLocation", "s3://tbsm-encore/dag/") \
    .trigger(processingTime="10 seconds") \
    .start()
 
print("✅ Streaming started.")
query.awaitTermination()



# Install all dependencies
# sudo wget https://repo1.maven.org/maven2/net/snowflake/spark-snowflake_2.12/2.11.0-spark_3.3/spark-snowflake_2.12-2.11.0-spark_3.3.jar -P /usr/lib/spark/jars/
# sudo wget https://repo1.maven.org/maven2/net/snowflake/snowflake-jdbc/3.13.30/snowflake-jdbc-3.13.30.jar -P /usr/lib/spark/jars/
# sudo wget https://awslabs-code-us-east-1.s3.amazonaws.com/spark-sql-kinesis-connector/spark-streaming-sql-kinesis-connector_2.12-1.2.1.jar -P /usr/lib/spark/jars/
# sudo chmod 755 /usr/lib/spark/jars/spark-streaming-sql-kinesis-connector_2.12-1.2.1.jar
# then run the file
# spark-submit   --master local[*]   --jars /usr/lib/spark/jars/snowflake-jdbc-3.13.30.jar,/usr/lib/spark/jars/spark-snowflake_2.12-2.9.0-spark_3.1.jar   --packages com.qubole.spark:spark-sql-kinesis_2.12:1.2.0_spark-3.0 kinesis_to_snowflake_s3.py

