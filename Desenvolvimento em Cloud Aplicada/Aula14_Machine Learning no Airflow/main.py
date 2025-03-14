from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from sklearn.linear_model import LogisticRegression
import pandas as pd
import joblib
import boto3
from sklearn.metrics import accuracy_score, roc_auc_score

def carregar_dados_treinamento():
    X_train = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})
    y_train = pd.Series([0, 1, 0])
    return X_train, y_train

def carregar_dados_teste():
    X_test = pd.DataFrame({"feature1": [1, 2], "feature2": [4, 5]})
    y_test = pd.Series([0, 1])
    return X_test, y_test

# Definição da DAG
dag = DAG(
    'pipeline_machine_learning',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
    },
    description='Pipeline de machine learning',
    start_date=days_ago(1),
    schedule_interval=None,
)

# Treinar um modelo de machine learning
def treinar_modelo():
    """
    Esta função treina um modelo de machine learning, como a regressão logística.
    """
    X_train, y_train = carregar_dados_treinamento()  
    modelo = LogisticRegression()
    modelo.fit(X_train, y_train)
    joblib.dump(modelo, '/home/cacoc/projeto/saved_model.pkl')

treinar_modelo_task = PythonOperator(
    task_id='treinar_modelo',
    python_callable=treinar_modelo,
    dag=dag,
)

# Validar métricas do modelo
def validar_metricas():
    """
    Esta função valida métricas do modelo, como acurácia e área sob a curva ROC.
    """
    X_test, y_test = carregar_dados_teste()  # Função para carregar dados de teste
    modelo = joblib.load('/home/cacoc/projeto/saved_model.pkl')
    y_pred = modelo.predict(X_test)

    acuracia = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred)
    print(f"Acurácia: {acuracia}, AUC: {auc}")

validar_metricas_task = PythonOperator(
    task_id='validar_metricas',
    python_callable=validar_metricas,
    dag=dag,
)

# Selecionar o melhor modelo
def selecionar_melhor_modelo():
    """
    Esta função seleciona o melhor modelo com base nas métricas avaliadas.
    """
    # Lógica para selecionar o melhor modelo com base nas métricas avaliadas
    melhor_modelo = joblib.load('/home/cacoc/projeto/saved_model.pkl')
    # Pode-se adicionar lógica mais complexa para seleção de modelos

selecionar_melhor_modelo_task = PythonOperator(
    task_id='selecionar_melhor_modelo',
    python_callable=selecionar_melhor_modelo,
    dag=dag,
)

# Publicar o modelo escolhido
def publicar_modelo():
    """
    Esta função publica o modelo escolhido em um ambiente de armazenamento como o S3.
    """
    # Exemplo de código para enviar o modelo para o S3
    s3 = boto3.client('s3')
    s3.upload_file('/home/cacoc/projeto/saved_model.pkl', 'meu-bucket', 'modelos/saved_model.pkl')

publicar_modelo_task = PythonOperator(
    task_id='publicar_modelo',
    python_callable=publicar_modelo,
    dag=dag,
)

# Definição de Dependências
treinar_modelo_task >> validar_metricas_task >> selecionar_melhor_modelo_task >> publicar_modelo_task
