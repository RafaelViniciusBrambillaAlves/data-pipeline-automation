import psycopg2
from psycopg2 import OperationalError
import os

def check_table_exists(table_name: str):
    """
    Check if the table exists in the database

    Args:
        table_name (str): Table's name
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host="db1",
            user="postgres",
            password="123456",
            port="5432",
            dbname="Amazon"
        )
        cursor = conn.cursor()
        query = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name=%s);"
        cursor.execute(query, (table_name,))
        exists = cursor.fetchone()[0]
        if exists:
            print(f"Table {table_name} exists.")
        else:
            print(f"Table {table_name} does not exist.")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    finally:
        if conn:
            cursor.close()
            conn.close()

def extract_data(query: str, output_path: str):
    """
    Extract data from database

    Args:
        query (str): SQL command to select the data in the database
        output_path (str): destination path to save csv file
    """
    conn = None
    try:
        # Garantir que o diretório exista
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        conn = psycopg2.connect(
            host="db1",
            user="postgres",
            password="123456",
            port="5432",
            dbname="Amazon"
        )
        cursor = conn.cursor()
        cursor.execute(query)
        colnames = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        with open(output_path, 'w') as file:
            # Write the header
            file.write(','.join('"{}"'.format(col) for col in colnames) + '\n')
            # Write the data rows
            for row in rows:
                file.write(','.join('"{}"'.format(str(cell).replace('"', '""')) if isinstance(cell, str) else str(cell) for cell in row) + '\n')
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    finally:
        if conn:
            cursor.close()
            conn.close()
