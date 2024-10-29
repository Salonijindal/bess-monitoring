Proposed Real-Time Data Processing Architecture

<img width="827" alt="Screenshot 2024-10-28 at 11 37 47 PM" src="https://github.com/user-attachments/assets/8826c48c-bfff-42df-a6c9-6de1533317fb">



1.Data Ingestion (MSK Kafka):
Use Amazon MSK (Kafka) as the primary data ingestion layer to handle real-time data from multiple BESS installations. Each BESS installation would produce telemetry data (e.g., voltage, temperature, current) and send it to Kafka topics on MSK.
Kafka enables high-throughput and low-latency ingestion, ensuring the system can handle a large volume of incoming data from multiple sources. 
![telemtry_data](https://github.com/user-attachments/assets/de36d484-d8c7-4bfc-b08b-5c9539ca7447)
![msk](https://github.com/user-attachments/assets/e6220401-e632-4ea6-9e37-0673b07dfd6d)



2.Real-Time Processing (EMR Spark Streaming):
Amazon EMR runs Spark Streaming jobs to process data from MSK in real time. The streaming job would:
Read the telemetry data from Kafka.
Apply any necessary transformations or computations (e.g., aggregating metrics, detecting thresholds for alerts).
Write the processed data to an S3 bucket for storage and further analysis.
EMR can scale to handle large amounts of data, making it suitable for high-frequency real-time processing.



3.Storage (S3 & Glue):
Amazon S3 stores the processed data in a structured format (e.g., Parquet) to enable fast querying.
AWS Glue Crawler catalogs the data in S3, creating a metadata catalog in the AWS Glue Data Catalog that Athena can query.
![crawler](https://github.com/user-attachments/assets/3c625bf6-1f5d-4978-b744-bef5443567c3)
![S3_bucket](https://github.com/user-attachments/assets/5463b548-4d50-49e0-b5a0-7ec30abf17eb)




4.Query and Analytics (Athena):
Use Amazon Athena to perform ad-hoc queries on the processed data stored in S3. This enables historical analysis, troubleshooting, and data visualization based on past data.
![json_stored_in_s3](https://github.com/user-attachments/assets/3dbf273d-98af-40d3-a5fc-bebaaf0b5529)



5. API Layer (API Gateway and Lambda):
API Gateway exposes RESTful APIs to allow the frontend to query the backend in real time.
AWS Lambda functions provide serverless compute to execute quick, event-driven queries against Athena for aggregated metrics and data analysis. They handle requests from API Gateway, format responses, and return relevant data to the frontend for display.![Api_gateway](https://github.com/user-attachments/assets/73852750-1ca0-455a-82b3-0949e6421722)
![Api_gateway](https://github.com/user-attachments/assets/e45b47e1-0529-485f-adc9-f0ff976fe0dd)



6.QuickSight for real time data visualization
![QuickStart](https://github.com/user-attachments/assets/7ea640cf-c7f8-4bbf-b13d-ef0cf2a16b42)



Proposed Solutions for high frequency and low latency architecture

![json_stored_in_s3](https://github.com/user-attachments/assets/3dbf273d-98af-40d3-a5fc-bebaaf0b5529)

