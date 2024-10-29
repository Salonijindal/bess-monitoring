from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.types import StructType, StructField, LongType, DoubleType, FloatType, StringType
import json

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

kafka_bootstrap_servers = "b-3.bessmonitoringmsk.4u6ji5.c4.kafka.ca-central-1.amazonaws.com:9092," \
                          "b-2.bessmonitoringmsk.4u6ji5.c4.kafka.ca-central-1.amazonaws.com:9092," \
                          "b-1.bessmonitoringmsk.4u6ji5.c4.kafka.ca-central-1.amazonaws.com:9092"

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", "bess-monitoring-topic") \
    .load()

print('Step 1')

telemetry_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("year", date_format(col("timestamp"), "yyyy")) \
    .withColumn("month", date_format(col("timestamp"), "MM")) \
    .withColumn("day", date_format(col("timestamp"), "dd")) \
    .withColumn("hour", date_format(col("timestamp"), "HH")) \
    .withColumn("minute", date_format(col("timestamp"), "mm")) \
    .withColumn("second", date_format(col("timestamp"), "ss"))

print("Step 2")

df.printSchema()