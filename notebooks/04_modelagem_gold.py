# Databricks notebook source
# MAGIC %md
# MAGIC # 4. Modelagem e Camada Gold

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4.1 Definição da Modelagem
# MAGIC
# MAGIC Nesta etapa será definida a estrutura dos dados que serão utilizados nas análises. A modelagem parte da tabela tratada na camada Silver e considera as perguntas de negócio definidas no início do projeto (item 1.3).
# MAGIC
# MAGIC Como o conjunto de dados está concentrado em uma única tabela, em que cada registro representa uma solicitação de empréstimo, optou-se por manter essa granularidade na camada Gold, sem a criação de tabelas fato e dimensão. Para o escopo deste trabalho, essa separação aumentaria a quantidade de tabelas sem acrescentar informações necessárias às análises propostas.
# MAGIC
# MAGIC A camada Gold será criada a partir dessa estrutura, mantendo os atributos necessários para as análises e acrescentando os campos derivados que forem necessários para responder às perguntas propostas.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4.2 Carregamento dos Dados da Camada Silver
# MAGIC
# MAGIC Para iniciar a modelagem da camada Gold, será utilizada a tabela `loan_approval_silver`, criada e persistida na etapa anterior. Essa tabela contém os dados já tratados e será utilizada como ponto de partida para a preparação dos dados analíticos.

# COMMAND ----------

# --- Carregamento da tabela persistida na camada Silver ---

df_silver = spark.table("workspace.default.loan_approval_silver")

# --- Verificação do carregamento ---

print(f"Quantidade de registros: {df_silver.count()}")
print(f"Quantidade de atributos: {len(df_silver.columns)}")

display(df_silver.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.2.1 Resultado do Carregamento dos Dados
# MAGIC
# MAGIC A tabela `loan_approval_silver` foi carregada corretamente, mantendo os 614 registros e os 13 atributos definidos na etapa anterior.
# MAGIC
# MAGIC A partir desses dados será feita a preparação da camada Gold, mantendo somente as transformações necessárias para responder às perguntas de negócio do projeto.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4.3 Preparação dos Dados para a Camada Gold
# MAGIC
# MAGIC Nesta etapa serão criados os atributos necessários para analisar o comprometimento estimado da renda familiar.
# MAGIC
# MAGIC A renda familiar será obtida pela soma da renda do solicitante com a renda do cônjuge. Como `LoanAmount` está expresso em milhares de unidades monetárias, seu valor será multiplicado por 1.000 antes do cálculo mensal, de forma a utilizar a mesma unidade monetária das variáveis de renda.
# MAGIC
# MAGIC Também será calculado um valor mensal estimado do empréstimo, dividindo o valor solicitado pelo prazo da operação. Como a base não informa a taxa de juros, esse valor não representa a parcela real do empréstimo. O cálculo será utilizado apenas como uma estimativa para comparar o comprometimento da renda entre as solicitações aprovadas e reprovadas.
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.3.1 Criação dos Atributos para Análise
# MAGIC
# MAGIC Serão criados os atributos `Renda_Familiar`, `Parcela_Mensal_Estimada` e `Percentual_Comprometimento_Renda` para complementar as informações disponíveis e permitir a análise proposta.

# COMMAND ----------

# --- Importação das funções utilizadas ---
from pyspark.sql import functions as F

# --- Criação dos atributos para análise ---

df_gold = (
    df_silver
    .withColumn(
        "Renda_Familiar",
        F.col("ApplicantIncome") + F.col("CoapplicantIncome")
    )
    .withColumn(
        "Parcela_Mensal_Estimada",
        F.round(
            (F.col("LoanAmount") * 1000) / F.col("Loan_Amount_Term"), 2
        )
    )
    .withColumn(
        "Percentual_Comprometimento_Renda",
        F.round(
            (F.col("Parcela_Mensal_Estimada") / F.col("Renda_Familiar")) * 100, 2
        )
    )
)

# --- Visualização dos atributos criados ---

display(
    df_gold.select(
        "Loan_ID",
        "ApplicantIncome",
        "CoapplicantIncome",
        "Renda_Familiar",
        "LoanAmount",
        "Loan_Amount_Term",
        "Parcela_Mensal_Estimada",
        "Percentual_Comprometimento_Renda",
        "Loan_Status"
    ).limit(10)
)

# COMMAND ----------

# --- Verificação de renda familiar igual a zero ---

renda_zero = df_gold.filter(F.col("Renda_Familiar") == 0).count()

print(f"Registros com renda familiar igual a zero: {renda_zero}")

# COMMAND ----------

# MAGIC %md
# MAGIC #### 4.3.1.1 Resultado da Criação dos Atributos
# MAGIC
# MAGIC Os três novos atributos foram calculados para todos os registros. Também foi verificado se existiam casos com renda familiar igual a zero, o que poderia impedir o cálculo do percentual de comprometimento, mas nenhum registro apresentou essa condição.
# MAGIC
# MAGIC Os valores de `Parcela_Mensal_Estimada` e `Percentual_Comprometimento_Renda` foram arredondados para duas casas decimais para facilitar sua leitura e interpretação nas análises.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.3.2 Estrutura Final da Camada Gold
# MAGIC
# MAGIC A estrutura final da camada Gold manterá os 13 atributos já disponíveis nos dados tratados e acrescentará os três atributos criados na etapa 4.3.1. Dessa forma, a tabela poderá ser utilizada para responder às perguntas de negócio sem eliminar informações que ainda possam ser úteis durante as análises.
# MAGIC
# MAGIC Ao todo, a camada Gold será composta por 16 atributos, mantendo cada registro no nível de uma solicitação de empréstimo.

# COMMAND ----------

# --- Estrutura final da camada Gold ---

print(f"Quantidade de registros: {df_gold.count()}")
print(f"Quantidade de atributos: {len(df_gold.columns)}")

df_gold.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.3.3 Validação dos Novos Atributos
# MAGIC
# MAGIC Antes de persistir a camada Gold, será feita uma verificação dos atributos criados nesta etapa. O objetivo é conferir se os cálculos não geraram valores nulos e observar os valores mínimos e máximos encontrados.

# COMMAND ----------

# --- Validação dos atributos criados ---

colunas_gold = [
    "Renda_Familiar",
    "Parcela_Mensal_Estimada",
    "Percentual_Comprometimento_Renda"
]

resultado_validacao = []

for coluna in colunas_gold:
    resultado = df_gold.select(
        F.min(coluna).alias("Minimo"),
        F.max(coluna).alias("Maximo")
    ).first()

    nulos = df_gold.filter(F.col(coluna).isNull()).count()

    resultado_validacao.append(
        (coluna, float(resultado["Minimo"]), float(resultado["Maximo"]), nulos)
    )

# --- Criação da tabela para visualização ---

df_validacao_gold = spark.createDataFrame(
    resultado_validacao,
    ["Atributo", "Minimo", "Maximo", "Valores_Nulos"]
)

display(df_validacao_gold)

# COMMAND ----------

# MAGIC %md
# MAGIC #### 4.3.3.1 Resultado da Validação dos Novos Atributos
# MAGIC
# MAGIC A validação não identificou valores nulos nos três atributos criados. A renda familiar variou entre 1.442 e 81.000, enquanto a parcela mensal estimada ficou entre 25 e 9.250.
# MAGIC
# MAGIC O percentual de comprometimento da renda variou entre 0,70% e 123,69%. Valores acima de 100% foram mantidos, pois representam situações em que a parcela estimada supera a renda familiar informada. Esses casos serão considerados posteriormente na análise dos resultados.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4.4 Persistência da Camada Gold
# MAGIC
# MAGIC Com a estrutura e os novos atributos validados, os dados serão persistidos em formato Delta para formar a camada Gold do pipeline.

# COMMAND ----------

# --- Persistência dos dados na camada Gold ---

(
    df_gold.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.default.loan_approval_gold")
)

# --- Validação da tabela Gold persistida ---

df_gold_validacao = spark.table("workspace.default.loan_approval_gold")

print(f"Registros persistidos: {df_gold_validacao.count()}")
print(f"Atributos persistidos: {len(df_gold_validacao.columns)}")

display(df_gold_validacao.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.4.1 Resultado da Persistência
# MAGIC
# MAGIC A camada Gold foi persistida com sucesso em formato Delta, mantendo os 614 registros e os 16 atributos definidos durante a modelagem.
# MAGIC
# MAGIC Após a gravação, a tabela foi carregada novamente para conferir o resultado da persistência e a disponibilidade dos dados para as próximas análises.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4.5 Catálogo de Dados
# MAGIC
# MAGIC O catálogo de dados será utilizado para documentar e facilitar a consulta à estrutura construída ao longo do pipeline. A documentação será apresentada tanto pela estrutura técnica das tabelas registradas no Databricks quanto pelo dicionário dos atributos utilizados na camada Gold.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.5.1 Catálogo Técnico no Databricks
# MAGIC
# MAGIC As tabelas criadas nas camadas Bronze, Silver e Gold foram registradas no catálogo do Databricks dentro do schema `default`. Por meio do Catalog Explorer foi possível consultar as tabelas, seus atributos, tipos de dados e demais informações relacionadas à estrutura e ao armazenamento.
# MAGIC
# MAGIC A verificação também permitiu confirmar que a tabela Gold está armazenada em formato Delta. As evidências dessa estrutura foram registradas por meio de capturas de tela da plataforma.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.5.2 Dicionário de Dados
# MAGIC
# MAGIC O dicionário de dados apresenta a descrição dos 16 atributos disponíveis na camada Gold, incluindo os atributos originais mantidos durante o tratamento e os três atributos criados durante a modelagem.
# MAGIC
# MAGIC Além da descrição, serão apresentados o tipo de dado, o domínio ou unidade de cada atributo e sua origem, facilitando a compreensão da estrutura utilizada nas análises.

# COMMAND ----------

# --- Criação do dicionário de dados ---

dados_catalogo = [
    ("Loan_ID", "string", "Identificador único da solicitação", "Texto", "Base original"),
    ("Gender", "string", "Gênero do solicitante", "Male / Female", "Base original"),
    ("Married", "string", "Estado civil do solicitante", "Yes / No", "Base original"),
    ("Dependents", "string", "Quantidade de dependentes", "0 / 1 / 2 / 3+", "Base original"),
    ("Education", "string", "Nível de escolaridade", "Graduate / Not Graduate", "Base original"),
    ("Self_Employed", "string", "Indica se trabalha por conta própria", "Yes / No", "Base original"),
    ("ApplicantIncome", "integer", "Renda mensal do solicitante", "Unidades monetárias /mês", "Base original"),
    ("CoapplicantIncome", "double", "Renda mensal do cônjuge ou co-solicitante", "Unidades monetárias /mês", "Base original"),
    ("LoanAmount", "double", "Valor solicitado do empréstimo", "Milhares de unidades monetárias", "Base original"),
    ("Loan_Amount_Term", "integer", "Prazo do empréstimo", "Meses", "Base original"),
    ("Credit_History", "integer", "Indicador de histórico de crédito", "0 / 1", "Base original"),
    ("Property_Area", "string", "Área de localização do imóvel", "Rural / Semiurban / Urban", "Base original"),
    ("Loan_Status", "string", "Situação da solicitação", "Y / N", "Base original"),
    ("Renda_Familiar", "double", "Soma das rendas do solicitante e do cônjuge", "Unidades monetárias / mês", "Derivado"),
    ("Parcela_Mensal_Estimada", "double", "Valor mensal estimado do empréstimo sem juros", "Unidades monetárias / mês", "Derivado"),
    ("Percentual_Comprometimento_Renda", "double", "Percentual estimado da renda familiar comprometida", "Percentual (%)", "Derivado")
]

df_catalogo = spark.createDataFrame(
    dados_catalogo,
    ["Atributo", "Tipo", "Descricao", "Dominio_Unidade", "Origem"]
)

display(df_catalogo)

# COMMAND ----------

# MAGIC %md
# MAGIC #### 4.5.2.1 Resultado do Dicionário de Dados
# MAGIC
# MAGIC O dicionário reúne os 16 atributos da camada Gold, apresentando seus tipos, descrições, domínios ou unidades e respectivas origens.
# MAGIC
# MAGIC Dos 16 atributos documentados, 13 são provenientes da base original e três foram derivados durante a preparação da camada Gold: `Renda_Familiar`, `Parcela_Mensal_Estimada` e `Percentual_Comprometimento_Renda`.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.5.3 Linhagem das Tabelas
# MAGIC
# MAGIC Para complementar o catálogo de dados, será documentada a linhagem das tabelas utilizadas no pipeline, identificando a origem de cada camada e as principais transformações realizadas entre Bronze, Silver e Gold.

# COMMAND ----------

# --- Criação da documentação de linhagem do pipeline ---

dados_linhagem = [
    (
        "loan_approval_bronze",
        "Bronze",
        "Dataset original",
        "Ingestão e persistência dos dados brutos, preservando a estrutura original da fonte"
    ),
    (
        "loan_approval_silver",
        "Silver",
        "loan_approval_bronze",
        "Remoção de coluna auxiliar, tratamento de valores nulos, padronização e adequação dos tipos de dados"
    ),
    (
        "loan_approval_gold",
        "Gold",
        "loan_approval_silver",
        "Criação de Renda_Familiar, Parcela_Mensal_Estimada e Percentual_Comprometimento_Renda"
    )
]

df_linhagem = spark.createDataFrame(
    dados_linhagem,
    ["Tabela", "Camada", "Origem", "Transformacoes_Principais"]
)

display(df_linhagem)

# COMMAND ----------

# MAGIC %md
# MAGIC #### 4.5.3.1 Resultado da Linhagem das Tabelas
# MAGIC
# MAGIC A linhagem evidencia o fluxo dos dados desde o dataset original até as camadas Bronze, Silver e Gold. A camada Bronze preserva os dados ingeridos em sua estrutura original, a Silver concentra os tratamentos e as padronizações realizadas, enquanto a Gold disponibiliza os atributos derivados utilizados nas análises.