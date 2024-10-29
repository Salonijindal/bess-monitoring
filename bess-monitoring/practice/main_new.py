import boto3
import json
from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, date_format
from pyspark.sql.types import StructType, StructField, StringType, FloatType

s3 = boto3.client('s3')

# Initialize Spark session
spark = SparkSession.builder \
    .appName("BESS Telemetry Streaming") \
    .getOrCreate()

# Define schema for telemetry data
schema = StructType([
    StructField("device_id", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("voltage", FloatType(), True),
    StructField("current", FloatType(), True),
    StructField("temperature", FloatType(), True),
    StructField("state_of_charge", FloatType(), True),
    StructField("power_output", FloatType(), True),
    StructField("frequency", FloatType(), True),
    StructField("status", StringType(), True),
    StructField("alerts", StringType(), True),
])

# Define MSK servers as a comma-separated list
kafka_bootstrap_servers = "b-3.bessmonitoringmsk.4u6ji5.c4.kafka.ca-central-1.amazonaws.com:9092," \
                          "b-2.bessmonitoringmsk.4u6ji5.c4.kafka.ca-central-1.amazonaws.com:9092," \
                          "b-1.bessmonitoringmsk.4u6ji5.c4.kafka.ca-central-1.amazonaws.com:9092"
# Read data from MSK
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", "bess-monitoring-topic") \
    .load()

# Parse telemetry data
telemetry_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Process data - Example: filter high temperature
high_temp_df = telemetry_df.filter(col("temperature") > 35)

# Write processed data to console (for testing) or S3
query = high_temp_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .start()


# Define partition keys
# now = datetime.now()
# partition_path = f"year={now.year}/month={now.month:02}/day={now.day:02}/hour={now.hour:02}/minute={now.minute:02}/second={now.second:02}"

# # Save as a JSON file (batch of 10ms data for that second)
# file_name = f"telemetry-{now.strftime('%Y-%m-%d-%H-%M-%S')}.json"
# s3.put_object(
#     Bucket='bess-monitoring-s3',
#     Key=f"telemetry-data/{partition_path}/{file_name}",
#     Body=json.dumps(data)
# )

print("Step 1")

# Parse telemetry data and extract timestamp as a date type for partitioning
# telemetry_df = df.selectExpr("CAST(value AS STRING)") \
#     .select(from_json(col("value"), schema).alias("data")) \
#     .select("data.*") \
#     .withColumn("year", date_format(col("timestamp"), "yyyy")) \
#     .withColumn("month", date_format(col("timestamp"), "MM")) \
#     .withColumn("day", date_format(col("timestamp"), "dd")) \
#     .withColumn("hour", date_format(col("timestamp"), "HH")) \
#     .withColumn("minute", date_format(col("timestamp"), "mm")) \
#     .withColumn("second", date_format(col("timestamp"), "ss"))

# print(f"Step 2", telemetry_df)

# Define the S3 output path
# output_path = "s3://bess-monitoring-s3/bess/"

# Write to S3 in partitioned format
# query = telemetry_df.writeStream \
#     .format("parquet") \
#     .outputMode("append") \
#     .option("path", output_path) \
#     .option("checkpointLocation", "s3://bess-monitoring-s3/checkpoints/telemetry-data") \
#     .partitionBy("year", "month", "day", "hour", "minute", "second") \
#     .start()

print("Step 3")

query.awaitTermination()