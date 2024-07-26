import logging
from pyspark.sql import SparkSession
from data_processing import process_and_display_data, create_selection_df_from_kafka
from cassandra_utils import create_cassandra_keyspace_and_table
import time

# Configure logging
logging.basicConfig(level=logging.INFO)

def create_spark_connection():
    """
    Creates a Spark session with the necessary configurations for Kafka and Cassandra.
    
    Returns:
        SparkSession: Configured Spark session or None if an error occurs.
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
        logging.error(f"Couldn't create the spark session due to exception {e}")
        return None

def connect_to_kafka(spark_conn):
    """
    Connects to Kafka and creates a DataFrame from the specified topic.

    Args:
        spark_conn (SparkSession): Spark session to use for connecting to Kafka.
    
    Returns:
        DataFrame: DataFrame created from Kafka topic or None if an error occurs.
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

if __name__ == "__main__":
    # Create Spark connection
    spark_conn = create_spark_connection()

    if spark_conn is not None:
        logging.info('Spark connected successfully')
        spark_df = connect_to_kafka(spark_conn)

        if spark_df is not None:
            # Check and create keyspace and table if they do not exist
            create_cassandra_keyspace_and_table()

            # Create and process DataFrame
            create_selection_df_from_kafka(spark_df)

            time.sleep(600)
        else:
            logging.error("Could not connect to Kafka.")
    else:
        logging.error("Could not create Spark connection.")
