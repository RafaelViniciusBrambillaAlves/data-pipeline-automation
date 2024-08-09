# project

docker compose up -d

docker exec -it kafka-connect kafka-console-consumer --bootstrap-server broker:29092 --topic csv-topic --from-beginning

docker exec -it data-pipeline-automation-spark-master-1 bash
cd /opt/bitnami/spark/pyspark
pip install py4j
pip install cassandra-driver
python main.py

docker exec -it cassandra bash  
cqlsh
USE amazon; 


# Data Pipeline Automation

Este projeto é um estudo para uma solução de automação para processamento de dados que envolve extração, transformação e carregamento (ETL) de dados usando uma combinação de PostgreSQL, Apache Airflow, Kafka, PySpark e Cassandra. O fluxo de dados é configurado para extrair dados de um banco de dados PostgreSQL, processá-los e carregá-los em um banco de dados Cassandra.

-->> Diagrama do fluxo que eu fiz

## Tecnologias Utilizadas

- **PostgreSQL**: Banco de dados relacional onde os dados originais estão armazenados.
- **Apache Airflow**: Orquestrador de workflows que automatiza a extração dos dados.
- **Kafka**: Sistema de mensageria usado para transmitir dados em tempo real.
- **PySpark**: Framework para processamento distribuído de dados.
- **Cassandra**: Banco de dados NoSQL onde os dados processados são armazenados.

## Estrutura do Projeto

1. **Extração de Dados**: Dados são extraídos do PostgreSQL usando Airflow e salvos como arquivos CSV localmente, organizados por data.
2. **Kafka Connect**: Conector que lê os arquivos CSV e publica os dados em um tópico Kafka (`csv-topic`).
3. **PySpark**: Script PySpark que consome dados do tópico Kafka, realiza transformações e carrega os dados no Cassandra.
4. **Cassandra**: Banco de dados onde os dados processados são armazenados.

## Requisitos

- Docker
- Docker Compose
- Python 3.x

## Configuração e Execução

1. **Inicie os containers**:
   ```bash
   docker compose up -d 

2. **Execute o script PySpark**
Conecte-se ao contêiner do Spark e execute o script PySpark para processar os dados:

docker exec -it data-pipeline-automation-spark-master-1 bash
cd /opt/bitnami/spark/pyspark
pip install py4j
pip install cassandra-driver
python main.py

3. **Extraia os dados do Airflow**
Acesse localhost:8080 
Rode a dag

4. **Verifique o resultado final no Cassandara**

Conecte-se ao contêiner do Cassandra e verifique os dados processados:
docker exec -it cassandra bash  
cqlsh
USE amazon;
## Para contar o número de linhas na tabela sales, execute:
SELECT COUNT(*) FROM sales;

