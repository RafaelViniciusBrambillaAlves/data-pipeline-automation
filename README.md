# 🛠️ Data Pipeline Automation

Este projeto é um estudo para automação do processamento de dados, abrangendo as etapas de extração, transformação e carregamento (ETL) utilizando PostgreSQL, Apache Airflow, Kafka, PySpark e Cassandra. O fluxo de dados é projetado para extrair dados de um banco de dados PostgreSQL, processá-los e carregá-los em um banco de dados Cassandra.

<img src="https://github.com/user-attachments/assets/e2b36c11-87bf-4b8a-a0c1-9e71ccf061f4" width="500" height="200"  alt="Image description">

## 🎯 Estrutura do Projeto

1. **Extração de Dados**:
  - Os dados são extraídos do PostgreSQL utilizando o Apache Airflow.
  - Esses dados são salvos localmente como arquivos CSV, organizados por data.
2. **Kafka Connect**: 
  - Um conector Kafka lê os arquivos CSV extraídos e os publica em um tópico Kafka (csv-topic).
  - O Kafka Connect está configurado para utilizar plugins como SpoolDir para ler arquivos CSV e DataStax Cassandra para carregar dados processados no Cassandra.
3. **PySpark**: 
  - PySpark consome os dados do tópico Kafka, processa-os, e os prepara para o armazenamento.
  - O processamento pode incluir limpeza, transformação e agregação de dados conforme a necessidade.
4. **Cassandra**: 
  - Após o processamento, os dados são enviados ao Cassandra, onde são armazenados e disponibilizados para consulta.
  - O Cassandra é configurado para armazenar grandes volumes de dados, aproveitando a escalabilidade horizontal.

## 👷 Serviços Configurados no Docker Compose

O projeto utiliza uma configuração Docker Compose para orquestrar os seguintes serviços:

- **PostgreSQL (db1):** Banco de dados usado pelo Apache Airflow para armazenar metadados e também pelos fluxos de trabalho para a extração de dados.

- **Apache Airflow (airflow-webserver, airflow-scheduler, airflow-init):**
  - O `airflow-webserver` fornece a interface de usuário.
  - O `airflow-scheduler` gerencia a execução das DAGs.
  - O `airflow-init` realiza a configuração inicial do Airflow.

- **Zookeeper (zookeeper) e Kafka Broker (broker):**
  - `Zookeeper` gerencia o cluster Kafka.
  - `Kafka Broker` gerencia o sistema de mensageria, permitindo a transmissão de dados entre produtores e consumidores.

- **Kafka Connect (kafka-connect):** Configurado para utilizar o conector SpoolDir para leitura dos arquivos CSV e o conector DataStax Cassandra para carregar dados no Cassandra.

- **Schema Registry (schema-registry):** Gerencia os esquemas de dados transmitidos pelos tópicos Kafka.

- **Kafka Control Center (control-center):** Interface para monitoramento e gerenciamento do cluster Kafka.

- **Spark Master (spark-master) e Spark Worker (spark-worker):** Configurados para processamento distribuído de dados utilizando PySpark.

- **Cassandra (cassandra_db):** Banco de dados NoSQL usado para armazenar os dados processados.

- **PostgreSQL (postgres):** Banco de dados usado pelo Airflow.

## 🤖 Configuração e Execução
1. **Arquivos**
   Insira o arquivo config_data.csv dentro da pasta data/current_data

2. **Inicie os containers**:
   ```bash
   docker compose up -d 

3. **Execute o script PySpark**
Conecte-se ao contêiner do Spark e execute o script PySpark para processar os dados:

```bash
docker exec -it data-pipeline-automation-spark-master-1 bash
cd /opt/bitnami/spark/pyspark
pip install py4j
pip install cassandra-driver
python main.py
```

4. **Extraia os dados do Airflow**
Acesse localhost:8080 
Rode a dag

5. **Verifique o resultado final no Cassandara**

Conecte-se ao contêiner do Cassandra e verifique os dados processados:
```bash
docker exec -it cassandra bash  
cqlsh
USE amazon;
## Para contar o número de linhas na tabela sales, execute:
SELECT COUNT(*) FROM sales;
```

## 🚀 Conclusão

Este projeto demonstra a automação de um pipeline de dados completo, desde a extração até o armazenamento em um banco de dados NoSQL, utilizando ferramentas amplamente adotadas na indústria. A configuração Docker Compose simplifica a orquestração dos serviços, enquanto Apache Airflow, Kafka, PySpark, e Cassandra trabalham juntos para garantir um fluxo de dados eficiente e escalável.

### Próximos Passos

- **Monitoramento e Alertas**: Implementar ferramentas de monitoramento e alertas para garantir a robustez e a eficiência do pipeline.
- **Escalabilidade**: Explorar a escalabilidade horizontal do Cassandra e do Spark para lidar com volumes de dados ainda maiores.
- **Segurança**: Adicionar medidas de segurança, como autenticação e criptografia, para proteger os dados sensíveis durante o processo.
- **Documentação**: Continuar aprimorando a documentação do projeto, incluindo detalhes sobre a configuração dos conectores Kafka e melhores práticas para o uso do PySpark.

Esse projeto serve como um estudo para um ponto de partida para a criação de pipelines de dados automatizados em ambientes de produção, permitindo o processamento de grandes volumes de dados de maneira eficiente e escalável.

## 🔨 Linguagens, Tecnologias e Bibliotecas Utilizadas

<div style="display: flex; flex-direction: row;">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png" alt="Descrição da Imagem" width="40">
  <img src="https://github.com/user-attachments/assets/e4183d59-0f47-4d7e-a773-0943ff36fb1f" alt="Descrição da Imagem" width="80">
  <img src="https://static-00.iconduck.com/assets.00/airflow-icon-2048x2048-ptyvisqh.png" alt="Descrição da Imagem" width="40">
  <img src="https://blog.geekhunter.com.br/wp-content/uploads/2020/09/apache-kafka.png" alt="Descrição da Imagem" width="40">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Apache_Spark_logo.svg/1280px-Apache_Spark_logo.svg.png" alt="Descrição da Imagem" width="80">
  <img src="https://download.logo.wine/logo/Apache_Cassandra/Apache_Cassandra-Logo.wine.png" alt="Descrição da Imagem" width="80">
  <img src="https://cdn.icon-icons.com/icons2/2415/PNG/512/postgresql_plain_wordmark_logo_icon_146390.png" alt="Descrição da Imagem" width="40">
  <img src="https://logosmarcas.net/wp-content/uploads/2021/03/Docker-Logo.png" alt="Descrição da Imagem" width="80"> 
</div>
