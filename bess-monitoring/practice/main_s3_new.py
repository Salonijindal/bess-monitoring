import argparse
import logging

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, FloatType, StringType
from pyspark.sql.functions import from_json, col

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KafkaToSparkLog")

def log_row(row):
    logger.info(f"Kafka Message ROW - {row}")

def transform_data(data_source: str, output_uri: str) -> None:
    with SparkSession.builder.appName("BESS Telemetry Streaming") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.InstanceProfileCredentialsProvider") \
        .config("spark.hadoop.fs.s3a.attempts.maximum", "10") \
        .config("spark.hadoop.fs.s3a.retry.interval", "2000") \
        .config("spark.hadoop.fs.s3a.connection.timeout", "6000000") \
        .config("spark.hadoop.fs.s3a.retry.interval", "2000") \
        .config("spark.yarn.executor.memoryOverhead", "1024") \
        .config("spark.kafka.consumer.session.timeout.ms", "120000") \
        .config("spark.kafka.consumer.request.timeout.ms", "90000") \
        .config("spark.kafka.consumer.fetch.max.wait.ms", "60000") \
        .getOrCreate() as spark:
        
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
        logger.info("Kafka Message Test")
        kafka_df = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "b-1.bessmonitoringmsk.4u6ji5.c4.kafka.ca-central-1.amazonaws.com:9092,b-2.bessmonitoringmsk.4u6ji5.c4.kafka.ca-central-1.amazonaws.com:9092,b-3.bessmonitoringmsk.4u6ji5.c4.kafka.ca-central-1.amazonaws.com:9092") \
            .option("subscribe", "bess-monitoring-topic") \
            .option("startingOffsets", "latest") \
            .option("kafka.retries", "5") \
            .option("kafka.retry.backoff.ms", "2000") \
            .load()
        logger.info("Kafka Message Test before printschema")
        kafka_df.printSchema()
        # kafka_df.show(truncate=False)
        print(type(kafka_df))
        value_df = kafka_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
        value_df.printSchema()
        # value_df.show(truncate=False)
        query = value_df \
            .writeStream \
            .format("console") \
            .start()
        # query = value_df.writeStream \
        #     .format("parquet") \
        #     .outputMode("append") \
        #     .option("path", output_uri) \
        #     .option("checkpointLocation", "s3a://bess-monitoring-s3/checkpoints/telemetry-data") \
        #     .trigger(processingTime="10 seconds") \
        #     .start()
        query.awaitTermination()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_source')
    parser.add_argument('--output_uri')
    args = parser.parse_args()
    # print(f"arguments testing: {args.data_source}")
    transform_data(args.data_source, args.output_uri)
