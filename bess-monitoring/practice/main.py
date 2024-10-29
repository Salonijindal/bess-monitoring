from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, FloatType, StringType
from pyspark.sql.functions import from_json, col, date_format

# from lib.logger import Log4j

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("BESS Telemetry Streaming") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .getOrCreate()
    
    # logger = Log4j(spark)
    
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
        # StructField("alerts", StringType(), True),
    ])
        
    kafka_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "b-1.bessmonitoringmsk.4u6ji5.c4.kafka.ca-central-1.amazonaws.com:9092,b-2.bessmonitoringmsk.4u6ji5.c4.kafka.ca-central-1.amazonaws.com:9092,b-3.bessmonitoringmsk.4u6ji5.c4.kafka.ca-central-1.amazonaws.com:9092") \
        .option("subscribe", "bess-monitoring-topic") \
        .option("startingOffsets", "earliest") \
        .load()
    print(type(kafka_df))
    # kafka_df.printSchema()
    value_df = kafka_df.select(from_json(col("value").cast("string"), schema).alias("value"))
    print(value_df.head())

    # Define the S3 output path
    output_path = "s3://bess-monitoring-s3/bess/"

    # Write to S3 in partitioned format
    # query = value_df.writeStream \
    #     .format("parquet") \
    #     .outputMode("append") \
    #     .option("path", output_path) \
    #     .option("checkpointLocation", "s3://bess-monitoring-s3/checkpoints/telemetry-data") \
    #     .trigger(processingTime="1 minute") \
    #     .start()
    # query = value_df.writeStream \
    #     .format("console") \
    #     .option("checkpointLocation", "s3://bess-monitoring-s3/checkpoints/telemetry-data") \
    #     .start()

    print("Step 3")

    query.awaitTermination()
    