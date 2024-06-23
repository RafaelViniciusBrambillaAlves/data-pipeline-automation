import pandas as pd
import psycopg2
from psycopg2 import sql

db_config = {
    'dbname': 'Amazon',
    'user': 'postgres',
    'password': '123456',
    'host': 'localhost',
    'port': '5433'
}

try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("Conexão com o banco de dados estabelecida.")

    table = 'sales'

    query = f'''
            SELECT * FROM {table}
            '''
    
    query = cursor.mogrify(query)
    query = query.decode('utf-8')

    with open('out.csv', 'w') as f:
        cursor.copy_expert("COPY ({}) TO STDOUT WITH CSV HEADER".format(query), f)
    print("Query results exported to CSV!")

except Exception as error:
    print(f"Erro ao conectar ou inserir dados: {error}")