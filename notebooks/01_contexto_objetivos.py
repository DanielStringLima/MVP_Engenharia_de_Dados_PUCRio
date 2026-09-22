# Databricks notebook source
# MAGIC %md
# MAGIC # Idenficação
# MAGIC MVP: Engenharia de Dados
# MAGIC
# MAGIC Nome: DANIEL LIMA
# MAGIC
# MAGIC Matrícula: 4052025002392
# MAGIC
# MAGIC Dataset: Loan Approval Prediction Dataset

# COMMAND ----------

# MAGIC %md
# MAGIC # 1. Contexto de Negócios e Perguntas

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1.1 Introdução
# MAGIC
# MAGIC A concessão de crédito exige uma análise criteriosa do perfil dos solicitantes, cruzando dados cadastrais, indicadores financeiros e o histórico de pagamento para mitigar riscos e fundamentar a tomada de decisão. 
# MAGIC
# MAGIC Entre as informações que podem fazer parte dessa análise estão a renda do solicitante, seu histórico de crédito, o valor solicitado e outras características cadastrais e financeiras. A análise desses dados permite compreender melhor o perfil das solicitações e identificar fatores que podem estar relacionados às decisões de aprovação.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1.2 Objetivo
# MAGIC
# MAGIC O objetivo deste MVP é construir um pipeline de dados no Databricks, partindo de um conjunto de dados brutos sobre solicitações de crédito e passando pelas etapas de ingestão, armazenamento, tratamento, modelagem e disponibilização dos dados para análise.
# MAGIC
# MAGIC O pipeline foi estruturado de forma a preservar os dados brutos, realizar tratamentos de qualidade e disponibilizar dados preparados para responder às perguntas de negócio relacionadas à concessão de crédito.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1.3 Perguntas de Negócio
# MAGIC
# MAGIC A partir dos dados disponíveis, foram definidas as seguintes perguntas para orientar a construção do pipeline e a análise dos dados:
# MAGIC
# MAGIC 1. A renda do solicitante apresenta relação com a aprovação do crédito?
# MAGIC
# MAGIC 2. O histórico de crédito é um fator relevante para a aprovação da solicitação?
# MAGIC
# MAGIC 3. O valor solicitado do empréstimo apresenta relação com a decisão de aprovação?
# MAGIC
# MAGIC 4. Como o comprometimento estimado da renda familiar se comporta entre solicitações aprovadas e reprovadas?
# MAGIC
# MAGIC 5. Qual é a relação entre o comprometimento estimado da renda familiar e a aprovação das solicitações de empréstimo?
# MAGIC
# MAGIC 6. Quais variáveis estão mais associados à aprovação das solicitações de empréstimo?

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1.4 Fonte e Licença dos Dados
# MAGIC
# MAGIC O conjunto de dados utilizado neste trabalho é o Loan Approval Prediction Dataset, disponibilizado na plataforma Kaggle. A base é composta por informações relacionadas a solicitações de crédito, reunindo características cadastrais e financeiras dos solicitantes e o resultado da solicitação.
# MAGIC
# MAGIC O dataset utilizado possui 614 registros e 13 variáveis, incluindo características cadastrais e financeiras dos solicitantes e a situação final da solicitação de empréstimo (Loan_ID, Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area e Loan_Status). A descrição detalhada dos atributos e seus respectivos tipos de dados será apresentada posteriormente no catálogo de dados. O arquivo é disponibilizado em formato CSV e foi utilizado como fonte de dados brutos para a construção do pipeline.
# MAGIC
# MAGIC Na página do dataset no Kaggle, a base é disponibilizada sob a licença Database Contents License (DbCL) v1.0, da Open Data Commons. Essa licença estabelece as condições para utilização do conteúdo disponibilizado na base de dados.