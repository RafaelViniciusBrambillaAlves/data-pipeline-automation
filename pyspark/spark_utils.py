from pyspark.sql import SparkSession
import logging

def create_spark_connection():
    """
    Creates a Spark session with the necessary configurations for connecting to Kafka and Cassandra.
    
    Returns:
        SparkSession: The configured Spark session.
    """
    try:
        s_conn = SparkSession.builder \
            .appName('SparkDataStreaming') \
            .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,com.datastax.spark:spark-cassandra-connector_2.12:3.3.0') \
            .config('spark.cassandra.connection.host', 'cassandra') \
            .getOrCreate()

        s_conn.sparkContext.setLogLevel("ERROR")
        logging.info("Spark connection created successfully!")
        return s_conn
    except Exception as e:
        logging.error(f"Couldn't create the Spark session due to exception: {e}")
        return None
