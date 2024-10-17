import logging
from pyspark.sql.functions import from_json, col, regexp_replace, when, round
from pyspark.sql.types import StructType, StructField, StringType, ArrayType

def process_and_display_data(sel):
    """
    Processes the data and performs several transformations, then outputs the data to various sinks.
    
    Args:
        sel (DataFrame): DataFrame with selected data from Kafka.
    """
    # Transform data
    sel_transformed = sel.withColumn("discounted_price",
        regexp_replace(
            regexp_replace(col("discounted_price"), "â¹", ""),
            ",", ""
        ).cast("float")
    ).withColumn("actual_price",
        regexp_replace(
            regexp_replace(col("actual_price"), "â¹", ''),
            ",", ""
        ).cast("float")
    ).withColumn("discount_percentage",
        regexp_replace(col("discount_percentage"), '%', '').cast("float")
    ).withColumn("rating",
        round(
            when(col("product_id") == "B08L12N5H1", 3.9).otherwise(col("rating").cast("float")),
            2
        )
    ).withColumn("rating_count",
        regexp_replace(col("rating_count"), ',', '').cast("float")
    )

    # Display transformed data
    query_transformed = sel_transformed.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", "false") \
        .option("checkpointLocation", "/tmp/transformed-console-checkpoint") \
        .start()

    # Send to Kafka topic
    kafka_query = sel_transformed.selectExpr("CAST(product_id AS STRING) AS key", "to_json(struct(*)) AS value") \
        .writeStream \
        .outputMode("append") \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "broker:29092") \
        .option("topic", "kafka-topic") \
        .option("checkpointLocation", "/tmp/kafka-checkpoint") \
        .start()

    # Write to Cassandra
    def write_to_cassandra(df, epoch_id):
        df.write \
            .format("org.apache.spark.sql.cassandra") \
            .options(table="sales", keyspace="amazon") \
            .mode("append") \
            .save()

    cassandra_query = sel_transformed.writeStream \
        .foreachBatch(write_to_cassandra) \
        .option("checkpointLocation", "/tmp/cassandra-checkpoint") \
        .start()

    query_transformed.awaitTermination()
    kafka_query.awaitTermination()
    cassandra_query.awaitTermination()

def create_selection_df_from_kafka(spark_df):
    """
    Creates a DataFrame from the Kafka DataFrame by selecting and structuring the required fields.
    
    Args:
        spark_df (DataFrame): DataFrame created from Kafka topic.
    """
    schema = StructType([
        StructField("schema", StructType([
            StructField("type", StringType(), True),
            StructField("fields", ArrayType(StructType([
                StructField("type", StringType(), True),
                StructField("optional", StringType(), True),
                StructField("field", StringType(), True)
            ])), True),
            StructField("optional", StringType(), True),
            StructField("name", StringType(), True)
        ]), True),
        StructField("payload", StructType([
            StructField("product_id", StringType(), True),
            StructField("product_name", StringType(), True),
            StructField("category", StringType(), True),
            StructField("discounted_price", StringType(), True),
            StructField("actual_price", StringType(), True),
            StructField("discount_percentage", StringType(), True),
            StructField("rating", StringType(), True),
            StructField("rating_count", StringType(), True),
            StructField("about_product", StringType(), True),
            StructField("user_id", StringType(), True),
            StructField("user_name", StringType(), True),
            StructField("review_id", StringType(), True),
            StructField("review_title", StringType(), True),
            StructField("review_content", StringType(), True),
            StructField("img_link", StringType(), True),
            StructField("product_link", StringType(), True)
        ]), True)
    ])

    sel = spark_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col('value'), schema).alias('data')).select("data.payload.*")

    # Process and display data
    process_and_display_data(sel)
