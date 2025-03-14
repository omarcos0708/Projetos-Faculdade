from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.models import Connection
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count
import os
from datetime import timedelta

pg_conn = Connection(conn_id='postgres_default', conn_type='postgres',
                     host='localhost', login='postgres', password='admin', schema='postgres_db')
hdfs_conn = Connection(conn_id='hdfs_default', conn_type='hdfs', host='hdfs-namenode', port=8020)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': days_ago(1),
}

dag = DAG(
    'processo_de_vendas',
    default_args=default_args,
    description='Processamento de dados de vendas',
    schedule_interval=timedelta(days=1),
)

def init_spark():
    spark = SparkSession.builder \
        .appName("ETL Project") \
        .getOrCreate()
    return spark

def extract_transform_load():
    spark = init_spark()

    # Leitura das tabelas do PostgreSQL
    url = 'jdbc:postgresql://localhost/postgres_db'
    properties = {'user': 'postgres', 'password': 'admin', 'driver': 'org.postgresql.Driver'}

    orders = spark.read.jdbc(url=url, table='orders', properties=properties)
    order_items = spark.read.jdbc(url=url, table='order_items', properties=properties)
    customers = spark.read.jdbc(url=url, table='customers', properties=properties)
    products = spark.read.jdbc(url=url, table='products', properties=properties)
    daily_sales = orders.join(order_items, "order_id") \
                        .groupBy("order_date") \
                        .agg(sum(col("price") * col("quantity")).alias("daily_sales"))
  
    top_products = order_items.groupBy("product_id") \
                              .agg(count("*").alias("total_sold")) \
                              .join(products, "product_id") \
                              .orderBy(col("total_sold").desc())
    low_stock_products = products.filter(col("stock") < 10)
    hdfs_path_bronze = "hdfs://hdfs-namenode:8020/user/postgres/data/bronze"
    hdfs_path_silver = "hdfs://hdfs-namenode:8020/user/postgres/data/silver"
    hdfs_path_gold = "hdfs://hdfs-namenode:8020/user/postgres/data/gold"
    daily_sales.write.mode("overwrite").parquet(hdfs_path_bronze + "/daily_sales")
    top_products.write.mode("overwrite").parquet(hdfs_path_bronze + "/top_products")
    low_stock_products.write.mode("overwrite").parquet(hdfs_path_bronze + "/low_stock_products")
    bronze_count = spark.read.parquet(hdfs_path_bronze + "/daily_sales").count()
    silver_count = spark.read.parquet(hdfs_path_silver + "/daily_sales").count()
    gold_count = spark.read.parquet(hdfs_path_gold + "/daily_sales").count()
    assert bronze_count > 0, "Erro: Dados inválidos na camada bronze"
    assert silver_count > 0, "Erro: Dados inválidos na camada silver"
    assert gold_count > 0, "Erro: Dados inválidos na camada gold"

    # Geração do relatório final de vendas
    final_report = spark.read.parquet(hdfs_path_gold + "/final_report")
    final_report.write.mode("overwrite").csv("/path/to/report/final_sales_report.csv")
extract_transform_load_task = PythonOperator(
    task_id='extract_transform_load',
    python_callable=extract_transform_load,
    dag=dag,
)
send_email = EmailOperator(
    task_id='send_email',
    to='cacocesar2020@gmail.com',
    subject='Relatório Vendas',
    html_content='<h3>Relatório de Vendas Marcos César</h3>',
    files=['/path/to/report/final_sales_report.csv'],
    dag=dag,
)
extract_transform_load_task >> send_email
