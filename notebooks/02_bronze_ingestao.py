# Databricks notebook source
# MAGIC %md
# MAGIC # 2. Camada Bronze - Ingestão dos Dados

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.1 Objetivo
# MAGIC Esta etapa tem como objetivo realizar o carregamento dos dados brutos no ambiente Databricks, constituindo a camada Bronze do pipeline.
# MAGIC
# MAGIC O conjunto de dados utilizado é o Loan Approval Prediction Dataset. Esse dataset contém informações cadastrais e financeiras relacionadas a solicitações de crédito. O arquivo original foi armazenado em um Volume do Unity Catalog, preservando os dados conforme disponibilizados na fonte.
# MAGIC
# MAGIC Nesta etapa não foram realizadas transformações nos dados. O objetivo é manter uma representação dos dados brutos, garantindo sua rastreabilidade para as etapas posteriores do pipeline.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.2 Carregamento dos Dados Brutos
# MAGIC Após o armazenamento do arquivo original no Volume do Unity Catalog, os dados são carregados no notebook utilizando o Apache Spark.
# MAGIC
# MAGIC O arquivo CSV é lido diretamente do Volume do Unity Catalog, sendo a primeira linha utilizada como cabeçalho e realizada a identificação automática dos tipos de dados. Neste momento, nenhuma transformação ou tratamento é aplicado aos registros.
# MAGIC
# MAGIC A visualização inicial permite verificar se o arquivo foi carregado corretamente.

# COMMAND ----------

# --- Caminho do arquivo bruto armazenado no Volume do Unity Catalog ---
caminho_arquivo = "/Volumes/workspace/default/loan_approval_bronze/loan_prediction.csv"

# --- Leitura do arquivo CSV utilizando Apache Spark ---
df_bronze = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(caminho_arquivo)
)

# --- Visualização dos primeiros registros ---
display(df_bronze)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.3 Verificação Inicial dos Dados Carregados
# MAGIC
# MAGIC Após o carregamento, é realizada uma verificação inicial da estrutura dos dados brutos, com o objetivo de conferir a quantidade de registros, atributos e os tipos de dados identificados automaticamente pelo Apache Spark.
# MAGIC

# COMMAND ----------

# --- Quantidade de registros ---
quantidade_registros = df_bronze.count()

# --- Quantidade de colunas ---
quantidade_colunas = len(df_bronze.columns)

print(f"Quantidade de registros: {quantidade_registros}")
print(f"Quantidade de colunas: {quantidade_colunas}")

# --- Estrutura e tipos de dados identificados ---
df_bronze.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2.3.1 Resultado da Verificação Inicial
# MAGIC
# MAGIC A verificação identificou 614 registros e 14 colunas na estrutura carregada pelo Apache Spark.
# MAGIC
# MAGIC Dessas 14 colunas, 13 correspondem aos atributos do conjunto de dados utilizado na análise de crédito. A coluna adicional _c0 representa um índice sequencial associado aos registros do arquivo de origem e não possui significado para o contexto do problema.
# MAGIC
# MAGIC Também foi possível verificar os tipos de dados identificados automaticamente pelo Spark. Atributos categóricos, como Gender, Married e Education , foram reconhecidos corretamente como texto (string), enquanto atributos numéricos, como ApplicantIncome, CoapplicantIncome e LoanAmount, foram identificados corretamente como tipos numéricos.
# MAGIC
# MAGIC A coluna _c0 foi mantida nesta etapa para preservar a estrutura dos dados na camada Bronze e removida posteriormente durante o processo de tratamento e preparação da camada Silver.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.4 Persistência dos Dados da Camada Bronze
# MAGIC
# MAGIC Após o carregamento e a verificação inicial, os dados brutos são persistidos no Unity Catalog como uma tabela no formato Delta.
# MAGIC
# MAGIC A persistência permite que os dados permaneçam armazenados na plataforma e possam ser acessados posteriormente pelas demais etapas do pipeline, sem depender exclusivamente do DataFrame criado durante a execução do notebook.

# COMMAND ----------

# --- Persistência dos dados da camada Bronze ---

(
    df_bronze.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.default.loan_approval_bronze_raw")
)

print("Tabela Bronze persistida com sucesso.")

# COMMAND ----------

# --- Validação da tabela Bronze persistida ---

df_bronze_validacao = spark.table("workspace.default.loan_approval_bronze_raw")

print(f"Registros persistidos: {df_bronze_validacao.count()}")
print(f"Atributos persistidos: {len(df_bronze_validacao.columns)}")

display(df_bronze_validacao.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2.4.1 Resultado da Persistência
# MAGIC
# MAGIC A tabela loan_approval_bronze_raw foi persistida com sucesso no Unity Catalog utilizando o formato Delta.
# MAGIC
# MAGIC Com a persistência, os dados da camada Bronze passam a permanecer armazenados no ambiente Databricks e podem ser utilizados pelas etapas posteriores do pipeline sem depender exclusivamente do DataFrame criado durante a execução do notebook.