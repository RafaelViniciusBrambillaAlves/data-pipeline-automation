from pyspark.sql import DataFrame
import logging

def connect_to_kafka(spark_conn):
    """
    Connects to a Kafka topic and reads the data stream.
    
    Args:
        spark_conn (SparkSession): The Spark session to use for reading the Kafka stream.
    
    Returns:
        DataFrame: The DataFrame containing the Kafka stream data.
    """
    try:
        spark_df = spark_conn.readStream \
            .format('kafka') \
            .option('kafka.bootstrap.servers', 'broker:29092') \
            .option('subscribe', 'csv-topic') \
            .option('startingOffsets', 'earliest') \
            .load()
        
        logging.info("Kafka dataframe created successfully")
        return spark_df
    except Exception as e:
        logging.warning(f"Kafka dataframe could not be created because: {e}")
        return None
