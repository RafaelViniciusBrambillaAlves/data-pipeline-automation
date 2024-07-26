from cassandra.cluster import Cluster
import logging

def create_cassandra_keyspace_and_table():
    """
    Creates the Cassandra keyspace and table if they do not exist.
    """
    try:
        cluster = Cluster(['cassandra'])
        session = cluster.connect()

        # Create keyspace
        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS amazon 
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
        """)

        # Use keyspace
        session.execute("USE amazon;")

        # Create table
        session.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                product_id text PRIMARY KEY,
                product_name text,
                category text,
                discounted_price float,
                actual_price float,
                discount_percentage float,
                rating float,
                rating_count float,
                about_product text,
                user_id text,
                user_name text,
                review_id text,
                review_title text,
                review_content text,
                img_link text,
                product_link text
            );
        """)

        logging.info("Cassandra keyspace and table created successfully!")
    except Exception as e:
        logging.error(f"Error creating Cassandra keyspace/table: {e}")
