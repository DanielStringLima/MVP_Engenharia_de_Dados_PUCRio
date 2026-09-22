# MVP de Engenharia de Dados

## Pipeline de Dados para Análise de Aprovação de Empréstimos

Este projeto foi desenvolvido como MVP da disciplina de Engenharia de Dados da Pós-Graduação em Ciência de Dados e Analytics da PUC-Rio.

O trabalho apresenta a construção de um pipeline de dados utilizando o Databricks, seguindo a arquitetura Medalhão (Bronze, Silver e Gold). O objetivo é organizar, tratar e transformar os dados de solicitações de empréstimos para possibilitar análises relacionadas à aprovação das solicitações.

## Objetivo

O objetivo do projeto é construir um pipeline de dados que permita analisar características relacionadas à aprovação ou reprovação de solicitações de empréstimos.

A análise busca responder às seguintes perguntas:

1. A renda do solicitante apresenta relação com a aprovação do crédito?
2. O histórico de crédito é um fator relevante para a aprovação da solicitação?
3. O valor solicitado do empréstimo apresenta relação com a decisão de aprovação?
4. Como o comprometimento estimado da renda familiar se comporta entre solicitações aprovadas e reprovadas?
5. Qual é a relação entre o comprometimento estimado da renda familiar e a aprovação das solicitações de empréstimo?
6. Quais variáveis estão mais associados à aprovação das solicitações de empréstimo?

## Fonte dos Dados

Foi utilizado o **Loan Approval Prediction Dataset**, disponibilizado publicamente na plataforma Kaggle.

O conjunto contém informações sobre solicitações de empréstimos, incluindo características como renda do solicitante, renda do cônjuge, valor solicitado, prazo, histórico de crédito, área da propriedade e situação final da solicitação.

A fonte e a licença do conjunto de dados foram verificadas e documentadas durante o desenvolvimento do projeto.

## Arquitetura do Pipeline

O pipeline foi desenvolvido no Databricks seguindo a arquitetura Medalhão:

**Bronze → Silver → Gold**

### Camada Bronze

Responsável pela ingestão e persistência dos dados brutos, preservando a estrutura original da fonte.

### Camada Silver

Responsável pelo tratamento e preparação dos dados, incluindo:

- tratamento de valores ausentes;
- padronização dos dados;
- adequação dos tipos;
- remoção de coluna auxiliar;
- validações de qualidade.

### Camada Gold

Responsável pela preparação dos dados utilizados nas análises. Nesta camada foram criados atributos derivados, entre eles:

- `Renda_Familiar`;
- `Parcela_Mensal_Estimada`;
- `Percentual_Comprometimento_Renda`.

O fluxo de dados utilizado no projeto pode ser representado por:

`Dataset original → Bronze → Silver → Gold → Análises`

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
│   ├── Imagem_07_catalogo_estrutura_gold.png
│   ├── Imagem_08_taxa_aprovacao_por_faixa_renda.png
│   ├── Imagem_09_aprovacao_por_historico_credito.png
│   ├── Imagem_10_taxa_aprovacao_por_valor_solicitado.png
│   ├── Imagem_11_taxa_aprovacao_por_comprometimento_renda.png
│   ├── Imagem_12_relacao_renda_valor_solicitado.png
│   └── Imagem_13_forca_associacao_aprovacao.png
│
└── README.md
```

## Organização dos Notebooks

O desenvolvimento foi dividido em cinco notebooks:

### [01 - Contexto e Objetivos](notebooks/01_contexto_objetivos.ipynb)

Apresentação do problema, fonte dos dados, questões de análise e contexto do projeto.

### [02 - Bronze e Ingestão](notebooks/02_bronze_ingestao.ipynb)

Ingestão do conjunto de dados, verificações iniciais e persistência da camada Bronze.

### [03 - Silver e Transformação](notebooks/03_silver_transformacao.ipynb)

Tratamento, padronização, validação e persistência dos dados na camada Silver.

### [04 - Modelagem Gold](notebooks/04_modelagem_gold.ipynb)

Criação dos atributos derivados, estruturação da camada Gold, catálogo de dados e documentação da linhagem das tabelas.

### [05 - Análise dos Resultados](notebooks/05_analise_resultados.ipynb)
Análises destinadas a responder às perguntas definidas no início do projeto.

## Principais Resultados

As análises mostraram que o **Histórico de Crédito** apresentou a associação mais expressiva com a aprovação das solicitações, com coeficiente de Pearson de aproximadamente **0,5406**.

Entre as variáveis categóricas analisadas pelo V de Cramér, a **Área da Propriedade** apresentou a maior medida de associação, com aproximadamente **0,1415**.

A análise da relação entre renda do solicitante e valor solicitado também mostrou associação positiva entre essas duas variáveis, sendo mais forte entre as solicitações aprovadas (**0,6135**) do que entre as reprovadas (**0,4803**).

Por outro lado, renda e valor solicitado, quando avaliados individualmente em relação à aprovação, apresentaram associações baixas.

Para as variáveis numéricas foi utilizada a correlação de Pearson, enquanto para as variáveis categóricas foi utilizado o V de Cramér. Como são medidas diferentes, seus valores devem ser interpretados dentro de cada método. Os resultados indicam associações estatísticas observadas nos dados, não significando que uma variável seja necessariamente responsável pela aprovação ou reprovação.

## Evidências

As evidências da execução do pipeline e das análises estão disponíveis na pasta [`evidencias`](./evidencias).

Entre elas estão registros da persistência das camadas Bronze, Silver e Gold, catálogo das tabelas e resultados gráficos das análises realizadas.

## Autor

**Daniel Lima**

MVP desenvolvido para a Pós-Graduação em Ciência de Dados e Analytics da PUC-Rio.
