from pyspark.sql import SparkSession, DataFrame 
from pyspark.sql.functions import col, regexp_replace, when, round
from datetime import datetime
import sys, os
import tempfile
import pandas

def create_spark_session(master_url: str, app_name: str) -> SparkSession:
    """
    Cria uma sessão Spark com a configuração fornecida.

    Parâmetros:
    master_url (str): URL do master Spark.
    app_name (str): Nome da aplicação Spark.

    Retorna:
    SparkSession: Instância da sessão Spark.
    """
    try:
        spark = SparkSession.builder \
            .master(master_url) \
            .appName(app_name) \
            .getOrCreate()
        print("Sessão Spark criada com sucesso.")
        return spark
    except Exception as e:
        print(f"Erro ao criar a sessão Spark: {e}")
        sys.exit(1)

def read_csv(spark: SparkSession, file_path: str) -> DataFrame:
    """
    Lê um arquivo CSV em um DataFrame Spark.

    Parâmetros:
    spark (SparkSession): Instância da sessão Spark.
    file_path (str): Caminho para o arquivo CSV.

    Retorna:
    DataFrame: DataFrame Spark com os dados do CSV.
    """
    try:
        df = spark.read.csv(file_path, header=True, inferSchema=True)
        print(f"Arquivo CSV lido com sucesso do caminho: {file_path}")
        return df
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        sys.exit(1)

def process_data(df: DataFrame) -> DataFrame:
    """
    Processa os dados do DataFrame: remove duplicatas, limpa e converte colunas.

    Parâmetros:
    df (DataFrame): DataFrame Spark com os dados a serem processados.

    Retorna:
    DataFrame: DataFrame Spark processado.
    """
    # Remover duplicatas
    df_copy = df.dropDuplicates()
    print("Duplicatas removidas.")

    # Limpar e converter a coluna "discounted_price"
    df_copy = df_copy.withColumn("discounted_price",
        regexp_replace(
            regexp_replace(col("discounted_price"), "â¹", ""),
            ",", ""
        ).cast("float")
                                )

    # Limpar e converter a coluna "actual_price"
    df_copy = df_copy.withColumn("actual_price",
        regexp_replace(
            regexp_replace(col("actual_price"), "â¹", ''),
            ",", ""
        ).cast("float")
    )

    # Limpar e converter a coluna "discount_percentage"
    df_copy = df_copy.withColumn("discount_percentage",
        regexp_replace(
            col("discount_percentage"), '%', ''
        ).cast("float")
    )

    # Ajustar a coluna "rating"
    df_copy = df_copy.withColumn("rating", col("rating").cast("float"))
    df_copy = df_copy.withColumn("rating", round(col("rating"), 2))
    df_copy = df_copy.withColumn("rating", when(col("product_id") == "B08L12N5H1", 3.9).otherwise(col("rating")))

    # Exibir as avaliações únicas
    unique_ratings = df_copy.select(col("rating")).distinct()
    unique_ratings_list = [row["rating"] for row in unique_ratings.collect()]

    # Limpar e converter a coluna "rating_count"
    df_copy = df_copy.withColumn("rating_count",
        regexp_replace(
            col("rating_count"), ',', ''
        ).cast("float")
    )

    print("Dados processados com sucesso.")
    return df_copy

def save_csv(df: DataFrame, file_path: str):
    """
    Salva o DataFrame em um arquivo CSV.

    Parâmetros:a
    df (DataFrame): DataFrame Spark a ser salvo.
    file_path (str): Caminho onde o arquivo CSV será salvo.
    """
    try:
        
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Diretório criado: {dir_path}")
        
        # Salva o DataFrame como CSV
        df.toPandas().to_csv(file_path)
        print(f"Arquivo CSV salvo com sucesso em: {file_path}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo CSV: {e}")
        sys.exit(1)


def main():
    """
    Função principal para executar o processamento dos dados.
    """
    # Configurações iniciais
    master_url = "spark://spark-master:7077"
    app_name = "SparkProcessWeb"

    # Criar sessão Spark
    spark = create_spark_session(master_url, app_name)

    # Definir o caminho para o arquivo CSV com base na data de hoje
    today_date = datetime.today().strftime('%Y%m%d')
    read_file_path = f"/data/not-process/{today_date}/public-sales.csv"
    save_file_path = f"/data/processed/{today_date}/public-sales.csv"
    save_file_path = f"/data/processed/20240703/public-sales.csv"

    # Ler o arquivo CSV
    df = read_csv(spark, read_file_path)

    # Processar os dados
    df_processed = process_data(df)
    
    # Salvar o DataFrame processado em um novo arquivo CSV
    save_csv(df_processed, save_file_path)
    
    # Encerrar a sessão Spark
    spark.stop()

if __name__ == "__main__":
    main()
