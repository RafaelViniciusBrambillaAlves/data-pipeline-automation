import pandas as pd
import psycopg2

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

# Conexão ao banco de dados - PostgreSQL
try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("Conexão com o banco de dados estabelecida.")

    # Leitura do CSV usando pandas
    df = pd.read_csv(csv_file_path, encoding='ISO-8859-1')

    # Criando a tabela Sales com tamanhos ajustados
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS Sales (
        product_id TEXT,
        product_name TEXT,
        category TEXT,
        discounted_price TEXT,
        actual_price TEXT,
        discount_percentage TEXT,
        rating TEXT,
        rating_count TEXT,
        about_product TEXT,
        user_id TEXT,
        user_name TEXT,
        review_id TEXT,
        review_title TEXT,
        review_content TEXT,
        img_link TEXT,
        product_link TEXT
    )
    '''
    cursor.execute(create_table_query)
    conn.commit()
    print("Tabela Sales criada com sucesso.")

    # Inserir dados no banco de dados
    for index, row in df.iterrows():
        try:
            insert_query = """
                INSERT INTO Sales (product_id, product_name, category, discounted_price, actual_price, discount_percentage, rating, rating_count, about_product, user_id, user_name, review_id, review_title, review_content, img_link, product_link)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            data_tuple = tuple(row)
            cursor.execute(insert_query, data_tuple)
            conn.commit()
        except Exception as e:
            conn.rollback()  
            print(f'Erro ao inserir a linha {index + 1}: {e}') 

    print("Dados inseridos com sucesso.")

except Exception as error:
    print(f"Erro ao conectar ou inserir dados: {error}")

finally:
    # Fechar a conexão
    if 'cursor' in locals() and cursor is not None:
        cursor.close()
    if 'conn' in locals() and conn is not None:
        conn.close()
    print("Conexão com o banco de dados encerrada.")
