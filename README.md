# MVP de Engenharia de Dados

# Daniel Lima

## Pipeline de Dados para Análise de Aprovação de Empréstimos

Este projeto foi desenvolvido como MVP da disciplina de Engenharia de Dados da Pós-Graduação em Ciência de Dados e Analytics da PUC-Rio.

O projeto apresenta a construção de um pipeline de dados no Databricks, utilizando arquitetura Medalhão (Bronze → Silver → Gold), PySpark, Spark SQL e Delta Lake para ingestão, tratamento, transformação, catalogação e análise de dados relacionados a solicitações de empréstimos.

---

## Etapas Realizadas

### 1. Contexto de Negócios e Perguntas

- 1.1 Introdução
- 1.2 Objetivo
- 1.3 Perguntas de Negócio
- 1.4 Fonte e Licença dos Dados

📓 [01 - Contexto e Objetivos](./notebooks/01_contexto_objetivos.ipynb)

---

### 2. Camada Bronze - Ingestão dos Dados

- 2.1 Objetivo
- 2.2 Carregamento dos Dados Brutos
- 2.3 Verificação Inicial dos Dados Carregados
  - 2.3.1 Resultado da Verificação Inicial
- 2.4 Persistência dos Dados da Camada Bronze
  - 2.4.1 Resultado da Persistência

📓 [02 - Bronze e Ingestão](./notebooks/02_bronze_ingestao.ipynb)

---

### 3. Qualidade e Transformação dos Dados

- 3.1 Análise de Qualidade dos Dados
- 3.2 Carregamento dos Dados para Análise
  - 3.2.1 Resultado do Carregamento dos Dados
- 3.3 Completude dos Dados
  - 3.3.1 Resultado da Análise de Completude
- 3.4 Consistência dos Dados
  - 3.4.1 Resultado da Análise de Consistência
- 3.5 Unicidade dos Dados
  - 3.5.1 Resultado da Análise de Unicidade
- 3.6 Acurácia dos Dados
  - 3.6.1 Resultado da Análise de Acurácia
- 3.7 Análise de Outliers
  - 3.7.1 Análise Visual
  - 3.7.2 Quantificação dos Outliers pelo IQR
  - 3.7.3 Resultado da Análise de Outliers
- 3.8 Transformação dos Dados para a Camada Silver
  - 3.8.1 Tratamento dos Valores Ausentes
    - 3.8.1.1 Resultado do Tratamento dos Valores Ausentes
  - 3.8.2 Padronização e Ajuste dos Dados
    - 3.8.2.1 Resultado da Padronização e Ajuste dos Dados
  - 3.8.3 Validação dos Dados Tratados
    - 3.8.3.1 Resultado da Validação dos Dados Tratados
  - 3.8.4 Persistência da Camada Silver
    - 3.8.4.1 Resultado da Persistência

📓 [03 - Silver e Transformação](./notebooks/03_silver_transformacao.ipynb)

---

### 4. Modelagem e Camada Gold

- 4.1 Definição da Modelagem
- 4.2 Carregamento dos Dados da Camada Silver
  - 4.2.1 Resultado do Carregamento dos Dados
- 4.3 Preparação dos Dados para a Camada Gold
  - 4.3.1 Criação dos Atributos para Análise
    - 4.3.1.1 Resultado da Criação dos Atributos
  - 4.3.2 Estrutura Final da Camada Gold
  - 4.3.3 Validação dos Novos Atributos
    - 4.3.3.1 Resultado da Validação dos Novos Atributos
- 4.4 Persistência da Camada Gold
  - 4.4.1 Resultado da Persistência
- 4.5 Catálogo de Dados
  - 4.5.1 Catálogo Técnico no Databricks
  - 4.5.2 Dicionário de Dados
    - 4.5.2.1 Resultado do Dicionário de Dados
  - 4.5.3 Linhagem das Tabelas
    - 4.5.3.1 Resultado da Linhagem das Tabelas

📓 [04 - Modelagem Gold](./notebooks/04_modelagem_gold.ipynb)

---

### 5. Análise dos Dados e Resultados

- 5.1 Carregamento dos Dados para Análise
  - 5.1.1 Resultado do Carregamento dos Dados
- 5.2 Relação entre Renda e Aprovação
  - 5.2.1 Resultado da Análise
- 5.3 Influência do Histórico de Crédito na Aprovação
  - 5.3.1 Resultado da Análise
- 5.4 Relação entre Valor Solicitado e Aprovação
  - 5.4.1 Resultado da Análise
- 5.5 Comprometimento Estimado da Renda Familiar
  - 5.5.1 Resultado da Análise
- 5.6 Relação entre Renda e Valor Solicitado
  - 5.6.1 Resultado da Análise
- 5.7 Variáveis Associadas à Aprovação
  - 5.7.1 Resultado da Análise
- 5.8 Síntese dos Resultados

### 6. Conclusão

- 6.1 Considerações Finais
- 6.2 Limitações do Projeto
- 6.3 Trabalhos Futuros
- 6.4 Autoavaliação

A conclusão e a autoavaliação estão apresentadas ao final do notebook:

📓 [05 - Análise dos Resultados](./notebooks/05_analise_resultados.ipynb)

---

## Contexto de Negócios e Perguntas

O projeto tem como objetivo construir um pipeline de dados para organizar, tratar e analisar informações relacionadas à aprovação ou reprovação de solicitações de empréstimos.

A análise foi orientada pelas seguintes perguntas de negócio:

1. A renda do solicitante apresenta relação com a aprovação do crédito?
2. O histórico de crédito é um fator relevante para a aprovação da solicitação?
3. O valor solicitado do empréstimo apresenta relação com a decisão de aprovação?
4. Como o comprometimento estimado da renda familiar se comporta entre solicitações aprovadas e reprovadas?
5. Qual é a relação entre o comprometimento estimado da renda familiar e a aprovação das solicitações de empréstimo?
6. Quais variáveis estão mais associadas à aprovação das solicitações de empréstimo?

Foi utilizado o **Loan Approval Prediction Dataset**, disponibilizado publicamente na plataforma Kaggle. A fonte e a licença do conjunto de dados estão documentadas no primeiro notebook e nas evidências do projeto.

---

## Carga dos Dados

A carga dos dados foi realizada no ambiente Databricks. Os dados brutos foram ingeridos e persistidos na camada Bronze, preservando a estrutura original da fonte.

---

## Modelagem e Catálogo de Dados

O pipeline foi estruturado segundo a arquitetura Medalhão:

`Bronze → Silver → Gold`

As tabelas foram persistidas no Databricks e disponibilizadas no catálogo:

- `loan_approval_bronze_raw`
- `loan_approval_silver`
- `loan_approval_gold`

O catálogo de dados, o dicionário dos campos e a linhagem das tabelas são apresentados no notebook de modelagem.

---

## Pipeline de Dados

O processo foi dividido em cinco notebooks para separar as diferentes responsabilidades do pipeline:

`Dataset original → Bronze → Silver → Gold → Análises`

Os notebooks disponibilizados neste repositório permitem acompanhar todas as etapas de construção do pipeline.

📂 [Acessar os notebooks](./notebooks)

---

## Qualidade de Dados

Foram realizadas verificações de qualidade relacionadas à completude, consistência, unicidade, acurácia e presença de outliers. Os tratamentos e validações realizados estão documentados no notebook da camada Silver.

---

## Análise de Dados

As análises foram realizadas a partir dos dados preparados na camada Gold e estruturadas de acordo com as perguntas de negócio definidas no início do projeto.

Entre os principais resultados observados:

- o **Histórico de Crédito** apresentou a associação mais expressiva com a aprovação, com coeficiente de Pearson de aproximadamente **0,5406**;
- entre as variáveis categóricas analisadas pelo **V de Cramér**, a **Área da Propriedade** apresentou a maior medida de associação, aproximadamente **0,1415**;
- a relação entre renda e valor solicitado apresentou associação positiva, sendo mais forte entre as solicitações aprovadas (**0,6135**) do que entre as reprovadas (**0,4803**);
- renda e valor solicitado, quando avaliados individualmente em relação à aprovação, apresentaram associações baixas.


---

## Autoavaliação

O projeto permitiu desenvolver um pipeline completo utilizando arquitetura Medalhão no Databricks, contemplando ingestão, persistência, qualidade, transformação, modelagem, catálogo, linhagem e análise dos dados.

As principais limitações estão relacionadas ao tamanho e à quantidade de informações disponíveis no conjunto de dados. Como trabalhos futuros, o pipeline pode ser ampliado com novas fontes de dados, automação das etapas, monitoramento de qualidade e inclusão de informações adicionais relacionadas ao risco de crédito.

---

## Evidências

As evidências da execução do pipeline e das análises estão disponíveis na pasta [`evidencias`](./evidencias).

```text
evidencias/
├── Imagem_01_evidencia_persistencia_tabela_bronze.png
├── Imagem_02_fonte_licenca_dataset_kaggle.png
├── Imagem_03_completude_dados_bronze.png
├── Imagem_04_evidencia_persistencia_tabela_silver.png
├── Imagem_05_evidencia_persistencia_tabela_gold.png
├── Imagem_06_catalogo_tabelas_pipeline.png
├── Imagem_07_linhagem_pipeline_bronze_silver_gold.png
├── Imagem_08_catalogo_estrutura_gold.png
├── Imagem_09_taxa_aprovacao_por_faixa_renda.png
├── Imagem_10_aprovacao_por_historico_credito.png
├── Imagem_11_taxa_aprovacao_por_valor_solicitado.png
├── Imagem_12_taxa_aprovacao_por_comprometimento_renda.png
├── Imagem_13_relacao_renda_valor_solicitado.png
└── Imagem_14_forca_associacao_aprovacao.png
```

---

## Estrutura do Repositório

```text
MVP_Engenharia_de_Dados_PUCRio/
│
├── notebooks/
│   ├── 01_contexto_objetivos.ipynb
│   ├── 02_bronze_ingestao.ipynb
│   ├── 03_silver_transformacao.ipynb
│   ├── 04_modelagem_gold.ipynb
│   └── 05_analise_resultados.ipynb
│
├── evidencias/
│   ├── Imagem_01_evidencia_persistencia_tabela_bronze.png
│   ├── Imagem_02_fonte_licenca_dataset_kaggle.png
│   ├── Imagem_03_completude_dados_bronze.png
│   ├── Imagem_04_evidencia_persistencia_tabela_silver.png
│   ├── Imagem_05_evidencia_persistencia_tabela_gold.png
│   ├── Imagem_06_catalogo_tabelas_pipeline.png
│   ├── Imagem_07_linhagem_pipeline_bronze_silver_gold.png
│   ├── Imagem_08_catalogo_estrutura_gold.png
│   ├── Imagem_09_taxa_aprovacao_por_faixa_renda.png
│   ├── Imagem_10_aprovacao_por_historico_credito.png
│   ├── Imagem_11_taxa_aprovacao_por_valor_solicitado.png
│   ├── Imagem_12_taxa_aprovacao_por_comprometimento_renda.png
│   ├── Imagem_13_relacao_renda_valor_solicitado.png
│   └── Imagem_14_forca_associacao_aprovacao.png
│
└── README.md
```

---

## Tecnologias Utilizadas

- Databricks
- Apache Spark
- PySpark
- Spark SQL
- Delta Lake
- Python
- Pandas
- Matplotlib
- SciPy
- GitHub

---
