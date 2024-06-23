import pandas as pd
import psycopg2
from psycopg2 import sql

# Configuração do banco de dados - PostgreSQL
db_config = {
    'dbname': 'Amazon',
    'user': 'postgres',
    'password': '123456',
    'host': 'localhost',
    'port': '5433'
}

# Caminho do CSV
csv_file_path = 'amazon.csv'
# Leitura do CSV usando pandas
df = pd.read_csv(csv_file_path, encoding='ISO-8859-1')

# Conexão ao banco de dados - PostgreSQL
try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("Conexão com o banco de dados estabelecida.")

    # Criando tabela
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS Sales (
        product_id VARCHAR(100),
        product_name VARCHAR(100),
        category VARCHAR(100),
        discounted_price VARCHAR(100),
        actual_price VARCHAR(100),
        discount_percentage VARCHAR(100),
        rating VARCHAR(50),
        rating_count VARCHAR(100),
        about_product VARCHAR(100),
        user_id VARCHAR(100),
        user_name VARCHAR(100),
        review_id VARCHAR(100),
        review_title VARCHAR(100),
        review_content VARCHAR(100),
        img_link VARCHAR(255),
        product_link VARCHAR(255)
    )
    '''
    cursor.execute(create_table_query)
    conn.commit()
    print("Tabela Sales criada com sucesso.")

    # Inserir dados no banco de dados
    for i, row in df.iterrows():
        insert_query = sql.SQL('''
        INSERT INTO Sales (product_id, product_name, category, discounted_price, actual_price, discount_percentage, rating, rating_count, about_product, user_id, user_name, review_id, review_title, review_content, img_link, product_link)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''')
        cursor.execute(insert_query, tuple(row))

    # Commit das inserções
    conn.commit()
    print("Dados inseridos com sucesso.")

except Exception as error:
    print(f"Erro ao conectar ou inserir dados: {error}")

finally:
    # Fechar a conexão
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
    print("Conexão com o banco de dados encerrada.")
