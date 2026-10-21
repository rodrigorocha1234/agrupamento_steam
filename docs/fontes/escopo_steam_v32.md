# Steam Reviews Clustering — Atualização v3.1

Observabilidade completa | Grafana | Prometheus | Loki | Alloy | MinIO | MLflow | FastAPI

O projeto passará a ter **dashboards obrigatórios de observabilidade no Grafana**, cobrindo todas as etapas: coleta diária da Steam, Data Lake Bronze/Silver/Gold, processamento Pandas/Polars, treinamento PyCaret/scikit-learn, inferência MLflow e endpoints FastAPI.

Além de mostrar os clusters e as interpretações de negócio, o Grafana permitirá responder:

- A coleta diária da Steam terminou corretamente?
- Quantas avaliações foram coletadas, atualizadas ou rejeitadas?
- Qual é o atraso dos dados no Data Lake?
- Qual motor, Pandas ou Polars, consome mais tempo e memória?
- Quanto tempo levam o pré-processamento, o tuning e o treinamento?
- Qual é a latência p50, p95 e p99 da API?
- Os modelos estão recebendo dados diferentes daqueles usados no treinamento?
- Algum serviço apresentou falhas, indisponibilidade ou consumo excessivo de recursos?

## 1. Arquitetura de observabilidade

Steam Collector

Data Lake / MinIO

Pandas / Polars

PyCaret / sklearn

MLflow Serving

FastAPI / Workers

**Instrumentação**

Prometheus Client · Métricas dos serviços · Logs estruturados

**Prometheus**

Armazenamento e consulta de métricas

**Alloy → Loki**

Coleta, transporte e consulta de logs

**Grafana**

Dashboards · PromQL · LogQL · Alertas

O Alloy será utilizado para coletar e encaminhar logs e, quando apropriado, métricas. O Prometheus armazenará as séries temporais operacionais, enquanto o Loki armazenará os logs. O Grafana consultará essas fontes.

## 2. Dashboards que serão adicionados

| ID     | Dashboard Grafana           | Objetivo                                      |
| ------ | --------------------------- | --------------------------------------------- |
| OBS-01 | Visão geral operacional     | Saúde geral dos serviços e pipelines          |
| OBS-02 | Steam API Collector         | Coleta, requisições, falhas e cobertura       |
| OBS-03 | Data Lake Bronze            | Ingestão, volume, uploads e integridade       |
| OBS-04 | Data Lake Silver/Gold       | Qualidade, transformações e atualizações      |
| OBS-05 | Processamento Pandas/Polars | Desempenho e utilização de recursos           |
| OBS-06 | Machine Learning            | Treinamento, tuning, avaliação e estabilidade |
| OBS-07 | Clustering Temporal         | Drift, transições e monitoramento dos grupos  |
| OBS-08 | MLflow Serving              | Inferência, latência e disponibilidade        |
| OBS-09 | FastAPI                     | Endpoints, throughput, erros e filas          |
| OBS-10 | Infraestrutura              | CPU, memória, disco, MinIO e contêineres      |
| OBS-11 | Logs e Diagnóstico          | Falhas correlacionadas com execuções          |
| OBS-12 | Qualidade do Monitoramento  | Saúde do Prometheus, Loki, Alloy e exporters  |

Os painéis de observabilidade serão separados dos dashboards analíticos e executivos, mas poderão compartilhar filtros por jogo, ambiente e framework.

---

## 3. Métricas obrigatórias por componente

### OBS-01 — Visão geral operacional

# 99,9%

Disponibilidade de referência

# 18 min

Duração da última coleta

# 98,5%

Cobertura da revisitação

# 0,8%

Erros da API

Valores fictícios para ilustrar o formato do dashboard; não são medições do projeto.

Indicadores de destaque: serviços disponíveis, pipelines concluídos, última coleta bem-sucedida, atraso dos dados, falhas recentes, alertas ativos e latência dos principais endpoints.

### OBS-02 — Steam API Collector

| Métrica                          | Nome Prometheus proposto                         | Visualização         |
| -------------------------------- | ------------------------------------------------ | -------------------- |
| Requisições totais               | `steam_api_requests_total`                       | Série temporal       |
| Latência das requisições         | `steam_api_request_duration_seconds`             | p50/p95/p99          |
| Respostas HTTP 429               | `steam_api_rate_limits_total`                    | Contador e taxa      |
| Retentativas                     | `steam_api_retries_total`                        | Série temporal       |
| Reviews processadas              | `steam_reviews_collected_total`                  | Barras por resultado |
| Páginas recebidas                | `steam_api_pages_total`                          | Contador             |
| Falhas de coleta                 | `steam_collection_failures_total`                | Série temporal       |
| Duração do ciclo                 | `steam_collection_duration_seconds`              | Histograma           |
| Última coleta concluída          | `steam_collection_last_success_unixtime_seconds` | Idade da coleta      |
| Cobertura da revisitação         | `steam_reviews_revisit_coverage_ratio`           | Percentual           |
| Reviews pendentes de revisitação | `steam_reviews_revisit_backlog`                  | Indicador            |

**Interpretação operacional:** se o volume coletado cair e simultaneamente houver crescimento de erros HTTP 429, a causa pode ser limitação de requisições, e não redução na quantidade de avaliações publicadas.

A coleta diária deverá ser monitorada por sucesso e pontualidade de cada execução, não por taxa constante de requisições ao longo das 24 horas.

### OBS-03 e OBS-04 — Data Lake

| Métrica                   | Bronze | Silver | Gold |
| ------------------------- | ------ | ------ | ---- |
| Registros processados     | Sim    | Sim    | Sim  |
| Volume de dados gravados  | Sim    | Sim    | Sim  |
| Duração de processamento  | Sim    | Sim    | Sim  |
| Falhas de leitura/escrita | Sim    | Sim    | Sim  |
| Duplicidades              | —      | Sim    | Sim  |
| Valores ausentes          | —      | Sim    | Sim  |
| Registros inválidos       | —      | Sim    | Sim  |
| Freshness dos datasets    | Sim    | Sim    | Sim  |
| Integridade e linhagem    | Sim    | Sim    | Sim  |
| Partições não atualizadas | —      | Sim    | Sim  |

Métricas propostas:

```
steam_lake_records_total
steam_lake_bytes_written_total
steam_lake_operation_duration_seconds
steam_lake_errors_total
steam_data_invalid_records_total
steam_data_duplicate_records_total
steam_data_null_ratio
steam_dataset_last_success_unixtime_seconds
steam_data_quality_score
```

O indicador `steam_data_quality_score` será um score próprio do projeto, com fórmula e critérios documentados, e não uma métrica nativa do MinIO.

### OBS-05 — Pandas versus Polars

| Indicador                    | Finalidade                            |
| ---------------------------- | ------------------------------------- |
| Tempo de leitura Parquet     | Desempenho de I/O                     |
| Tempo de filtros             | Eficiência das consultas              |
| Tempo de agregações          | Desempenho analítico                  |
| Tempo de engenharia temporal | Custo de processamento longitudinal   |
| Pico de memória RSS          | Consumo máximo de memória do processo |
| CPU utilizada                | Custo computacional                   |
| Registros por segundo        | Throughput                            |
| Erros de processamento       | Confiabilidade                        |
| Divergências entre motores   | Equivalência de resultados            |

Para essas comparações, os dashboards deverão permitir filtrar por `motor=pandas` ou `motor=polars`, usando os mesmos datasets e transformações.

### OBS-06 — Machine Learning

| Etapa                  | Métricas obrigatórias                         |
| ---------------------- | --------------------------------------------- |
| Pré-processamento      | Duração, registros de entrada/saída, falhas   |
| Transformações         | Tempo por técnica e valores inválidos         |
| PCA                    | Tempo e variância explicada                   |
| Tuning                 | Tentativas, duração, configurações inválidas  |
| Treinamento            | Duração, memória, CPU, falhas                 |
| Avaliação              | Silhouette, Davies-Bouldin, Calinski-Harabasz |
| Estabilidade           | ARI/NMI entre agrupamentos comparáveis        |
| Qualidade dos clusters | Tamanhos, ruídos e grupos degenerados         |
| Publicação             | Sucesso, falhas e versão ativa                |

O MLflow continuará armazenando o histórico detalhado dos experimentos. O Prometheus receberá métricas operacionais e um conjunto controlado de indicadores dos modelos aprovados.

O MLflow também possui coleta de métricas de sistema, como CPU, memória, rede e disco, durante as execuções de experimentos.

### OBS-07 — Clustering Temporal

| Métrica                   | Significado                                    |
| ------------------------- | ---------------------------------------------- |
| Distribuição dos clusters | Participação de cada grupo                     |
| Taxa de transições        | Proporção de avaliações que mudaram de cluster |
| Distância ao centróide    | Mudança de posicionamento no KMeans            |
| Frequência de ruído       | Avaliações sem grupo atribuído                 |
| Drift dos atributos       | Mudança nas distribuições de entrada           |
| Drift de clusters         | Alteração na distribuição dos grupos           |
| Cobertura temporal        | Avaliações efetivamente acompanhadas           |
| Atraso dos snapshots      | Tempo desde a última observação válida         |

O dashboard também deverá distinguir mudanças causadas por dados novos daquelas causadas por troca da versão do modelo.

### OBS-08 e OBS-09 — MLflow Serving e FastAPI

Métricas obrigatórias:

- Requisições por segundo.
- Tempo de resposta p50, p95 e p99.
- Taxa de erros HTTP 4xx e 5xx separadamente.
- Falhas de validação dos atributos.
- Combinações inexistentes ou não publicadas.
- Duração do pré-processamento e da inferência.
- Tempo de consulta ao catálogo de modelos.
- Modelos disponíveis e indisponíveis.
- Quantidade de reviews classificadas por requisição.
- Tamanho das filas de treinamento e tempo de espera.
- Requisições em execução.
- Quantidade de falhas de carregamento de modelos.

Será possível identificar separadamente gargalos do FastAPI, da resolução de combinações e do MLflow Serving.

### OBS-10 a OBS-12 — Infraestrutura e diagnóstico

Monitorar CPU, memória, disco, armazenamento MinIO, operações S3, conexões, reinicializações, saúde dos contêineres, disponibilidade dos serviços, erros de envio de logs e falhas dos próprios componentes de observabilidade.

O Loki e o Alloy disponibilizam métricas internas que também poderão ser monitoradas pelo Prometheus.

# Steam Reviews Clustering — Brasil

Versão 3.2 — Sumário completo e consolidado do projeto

**Engenharia de Dados · Data Lake · Machine Learning não supervisionado · Clustering temporal · MLflow · FastAPI · Grafana**

## 1. Visão geral

O projeto terá como finalidade coletar diariamente avaliações de jogos da Steam escritas em português brasileiro, armazenar seu histórico em um Data Lake e aplicar técnicas de Machine Learning não supervisionado para identificar e acompanhar perfis de avaliações.

O usuário poderá escolher dinamicamente os atributos dos agrupamentos, os motores de processamento, os frameworks de Machine Learning e as técnicas de pré-processamento por meio de arquivos YAML e de requisições FastAPI.

**O projeto não utilizará processamento de linguagem natural (PLN).** O texto original das avaliações será disponibilizado para consulta e leitura humana, mas ficará fora do treinamento.

A interface oficial de origem será `IUserReviewsService/GetAppReviews`, que disponibiliza campos como `playtime_at_review`, `comment_count`, `votes_up`, `timestamp_created` e `timestamp_updated`. [partner.steamgames.com](https://partner.steamgames.com/doc/webapi/IUserReviewsService?l=english)

Exemplo principal do projeto

```
{
  "atributos": [
    "playtime_at_review",
    "comment_count"
  ],
  "motor": "polars",
  "framework": "sklearn",
  "algoritmo": "kmeans"
}
```

Essa combinação poderá ser treinada, avaliada, publicada e consultada pela API. Os resultados incluirão gráficos, tabelas, histórico temporal, reviews pertencentes aos clusters e interpretações para a equipe de negócio.

## 2. Sumário geral — 18 capítulos

| Capítulo | Área                    | Conteúdo                                        |
| -------- | ----------------------- | ----------------------------------------------- |
| 01       | Planejamento            | Objetivos, escopo, hipóteses e requisitos       |
| 02       | API Steam               | Documentação, atributos e estratégias de coleta |
| 03       | Data Lake               | MinIO, Bronze, Silver e Gold                    |
| 04       | Processamento de Dados  | Pandas, Polars e Strategy                       |
| 05       | Qualidade e EDA         | Limpeza, validação e análise exploratória       |
| 06       | Engenharia de Atributos | Variáveis originais, derivadas e combinações    |
| 07       | Pré-processamento       | Técnicas configuráveis via YAML                 |
| 08       | Frameworks ML           | PyCaret e scikit-learn                          |
| 09       | Clustering              | Algoritmos, tuning e avaliação                  |
| 10       | Análise Temporal        | Snapshots, janelas, transições e drift          |
| 11       | MLflow                  | Experimentos, Registry e Serving                |
| 12       | FastAPI                 | Criação dinâmica de clusters e consultas        |
| 13       | Visualizações           | Gráficos, tabelas e dashboards analíticos       |
| 14       | Inteligência de Negócio | Perfis, interpretações e relatórios             |
| 15       | Observabilidade         | Prometheus, Grafana, Loki e Alloy               |
| 16       | Infraestrutura          | Docker Compose, serviços e configurações        |
| 17       | Testes e Governança     | Qualidade, segurança e reprodutibilidade        |
| 18       | Entregáveis             | Resultados finais e etapas de implantação       |

---

# 3. Detalhamento dos capítulos

## Capítulo 01 — Planejamento e requisitos

1.1. Contextualização das avaliações da Steam\
1.2. Objetivo geral e objetivos específicos\
1.3. Definição das perguntas de negócio\
1.4. Hipóteses sobre experiência e engajamento\
1.5. Delimitação da população de avaliações\
1.6. Escopo de Machine Learning não supervisionado\
1.7. Exclusão de técnicas de PLN\
1.8. Regras de negócio funcionais e não funcionais\
1.9. Critérios de sucesso e qualidade\
1.10. Limitações dos dados e riscos do projeto

O filtro de idioma identifica avaliações em português brasileiro, não necessariamente jogadores residentes no Brasil.

## Capítulo 02 — API Steam e coleta diária

2.1. Estudo do endpoint `IUserReviewsService/GetAppReviews`\
2.2. Autenticação, limites e parâmetros da API\
2.3. Configuração de um ou vários `appid`\
2.4. Filtro de idioma português brasileiro\
2.5. Paginação por cursor\
2.6. Coleta inicial de avaliações históricas\
2.7. Coleta incremental diária\
2.8. Revisitação de avaliações antigas\
2.9. Captura de avaliações atualizadas\
2.10. Controle de falhas, retentativas e HTTP 429\
2.11. Identificação de avaliações novas e já conhecidas\
2.12. Controle de cobertura da coleta\
2.13. Histórico de execução dos coletores\
2.14. Agendamento diário e recuperação de execuções interrompidas\
2.15. Monitoramento de latência e disponibilidade da API Steam

**Regra crítica:** coletar avaliações novas diariamente não garante atualizar comentários e votos das avaliações antigas. O projeto deverá possuir uma estratégia de revisitação, registrando quais avaliações foram efetivamente observadas em cada data.

## Capítulo 03 — Construção do Data Lake

3.1. Arquitetura S3 utilizando MinIO\
3.2. Criação e configuração dos buckets\
3.3. Bronze — respostas originais\
3.4. Silver — dados normalizados e históricos\
3.5. Gold — datasets e resultados analíticos\
3.6. Particionamento por jogo e data\
3.7. Preservação do histórico de snapshots\
3.8. Persistência em JSON comprimido e Parquet\
3.9. Idempotência e deduplicação\
3.10. Versionamento de datasets\
3.11. Linhagem e rastreabilidade\
3.12. Estratégias de reprocessamento\
3.13. Controle de integridade dos arquivos\
3.14. Métricas de armazenamento e atualização\
3.15. Políticas de retenção e permissões

### Estrutura física proposta

```
MinIO / S3
│
├── steam-bronze/
│   └── reviews/
│       └── appid=427520/
│           └── data_coleta=2026-10-21/
│               └── execucao_id=.../
│                   ├── pagina_001.json.gz
│                   ├── pagina_002.json.gz
│                   └── manifesto.json
│
├── steam-silver/
│   ├── reviews_normalizadas/
│   ├── reviews_historico/
│   ├── reviews_snapshots/
│   │   └── appid=427520/
│   │       └── data_coleta=2026-10-21/
│   │           └── parte-0001.parquet
│   ├── reviews_atual/
│   ├── execucoes_coleta/
│   └── qualidade_dados/
│
└── steam-gold/
    ├── atributos_estaticos/
    ├── atributos_temporais/
    ├── datasets_treinamento/
    │   └── combinacao_id=C001/
    │       └── dataset_versao=.../
    ├── resultados_clusters/
    │   └── combinacao_id=C001/
    │       └── modelo_versao=3/
    ├── transicoes_clusters/
    ├── perfis_clusters/
    ├── estatisticas_clusters/
    └── indicadores_negocio/
```

O Bronze preservará a resposta original da Steam. O Silver manterá o histórico validado. O Gold será responsável por fornecer datasets versionados para treinamento, análise temporal e dashboards.

## Capítulo 04 — Motores de processamento Pandas/Polars

4.1. Configuração do motor por YAML\
4.2. Pandas como motor de processamento\
4.3. Polars como motor de processamento\
4.4. Execução Lazy e Eager, conforme disponibilidade\
4.5. Implementação do padrão Strategy\
4.6. Adaptadores de entrada e saída\
4.7. Leitura e escrita de Parquet\
4.8. Filtros, joins, agregações e transformações vetorizadas\
4.9. Engenharia temporal com funções de janela\
4.10. Conversão para dados compatíveis com ML\
4.11. Benchmark Pandas × Polars\
4.12. Testes de equivalência de resultados

O motor poderá ser selecionado globalmente, por etapa do Data Lake ou por experimento.

## Capítulo 05 — Qualidade dos dados e EDA

5.1. Validação de schemas e tipos\
5.2. Identificação de valores ausentes\
5.3. Detecção de valores negativos e inválidos\
5.4. Deduplicação de observações\
5.5. Classificação das variáveis\
5.6. Distribuições e estatísticas descritivas\
5.7. Correlações entre atributos\
5.8. Identificação de assimetria e outliers\
5.9. Comparação exploratória entre jogos\
5.10. Análise de dados por período\
5.11. Análise da cobertura dos snapshots\
5.12. Indicadores e dashboards de qualidade

## Capítulo 06 — Engenharia e combinações de atributos

6.1. Catálogo de atributos disponíveis\
6.2. Conversão de minutos para horas\
6.3. Atributos numéricos, categóricos e binários\
6.4. Criação de variáveis derivadas\
6.5. Criação de variáveis temporais\
6.6. Seleção manual de atributos\
6.7. Combinações configuradas em YAML\
6.8. Combinações solicitadas dinamicamente pela FastAPI\
6.9. Validação de combinações permitidas\
6.10. Verificação de redundância entre atributos\
6.11. Comparação entre combinações\
6.12. Versionamento de atributos e definições

### Combinações iniciais

| ID   | Atributos                                       | Análise                        |
| ---- | ----------------------------------------------- | ------------------------------ |
| C001 | `playtime_at_review` × `comment_count`          | Experiência e discussão        |
| C002 | `playtime_at_review` × `votes_up`               | Experiência e utilidade        |
| C003 | `comment_count` × `votes_up`                    | Discussão e utilidade          |
| C004 | `playtime_forever` × `votes_funny`              | Tempo total e humor            |
| C005 | `num_reviews` × `votes_up`                      | Histórico do autor e utilidade |
| C006 | Horas × comentários × votos úteis               | Engajamento multidimensional   |
| C007 | `delta_comentarios_7d` × `delta_votos_uteis_7d` | Evolução semanal               |

## Capítulo 07 — Pré-processamento configurável no YAML

7.1. Tratamento de valores ausentes\
7.2. Imputação por média, mediana, moda e KNN\
7.3. Detecção de outliers por IQR\
7.4. Detecção de outliers por Z-Score e MAD\
7.5. Detecção multivariada por Isolation Forest\
7.6. Preservação, remoção ou winsorização de extremos\
7.7. Transformação `log1p`\
7.8. Transformações Yeo-Johnson e Box-Cox\
7.9. QuantileTransformer\
7.10. StandardScaler\
7.11. MinMaxScaler\
7.12. RobustScaler\
7.13. MaxAbsScaler\
7.14. Normalizer\
7.15. OneHotEncoder e OrdinalEncoder\
7.16. Discretização e binning\
7.17. Filtros de variância e correlação\
7.18. PCA e TruncatedSVD\
7.19. Peso configurável por atributo\
7.20. Comparação entre pipelines de pré-processamento\
7.21. Persistência do pipeline ajustado no MLflow

As transformações deverão ser aplicadas uma única vez, evitando duplicação entre o pipeline compartilhado e o pré-processamento nativo do framework.

## Capítulo 08 — Frameworks de Machine Learning

8.1. Seleção de PyCaret ou scikit-learn pelo YAML\
8.2. Implementação de adaptadores para cada framework\
8.3. Treinamento utilizando recursos nativos do scikit-learn\
8.4. Treinamento utilizando `ClusteringExperiment` do PyCaret\
8.5. Compatibilidade com pipelines personalizados\
8.6. Padronização dos contratos de entrada e saída\
8.7. Comparação entre frameworks\
8.8. Isolamento de dependências e versões\
8.9. Registro do framework utilizado no MLflow\
8.10. Compatibilidade com inferência de novas avaliações

O PyCaret oferece funções de criação, atribuição e predição de clusters, mas a predição depende de o estimador possuir suporte adequado. [pycaret.readthedocs.io](https://pycaret.readthedocs.io/en/latest/api/clustering.html)

## Capítulo 09 — Algoritmos de clustering, tuning e avaliação

9.1. KMeans\
9.2. MiniBatchKMeans\
9.3. DBSCAN\
9.4. HDBSCAN\
9.5. Agglomerative Clustering\
9.6. Algoritmos adicionais compatíveis\
9.7. Tuning de hiperparâmetros\
9.8. Grid Search\
9.9. Random Search\
9.10. Seleção automática ou manual da quantidade de clusters\
9.11. Silhouette Score\
9.12. Davies-Bouldin Index\
9.13. Calinski-Harabasz Index\
9.14. Estabilidade por reamostragem\
9.15. Análise de grupos pequenos e degenerados\
9.16. Análise de ruídos e anomalias\
9.17. Comparação de modelos e configurações\
9.18. Seleção de modelos candidatos à publicação

A seleção não dependerá de uma única métrica. Serão considerados qualidade, estabilidade, representatividade dos grupos e interpretabilidade.

## Capítulo 10 — Clustering temporal

10.1. Armazenamento de snapshots diários\
10.2. Histórico por `recommendationid`\
10.3. Construção de variáveis temporais\
10.4. Variações de comentários entre coletas\
10.5. Variações de votos úteis\
10.6. Variação de horas acumuladas\
10.7. Janelas de 1, 7, 14 e 30 dias\
10.8. Clustering com atributos temporais\
10.9. Monitoramento de clusters fixos\
10.10. Transições entre grupos\
10.11. Matrizes de transição\
10.12. Comparação de períodos\
10.13. Drift dos atributos\
10.14. Drift da distribuição dos clusters\
10.15. Controle de cobertura histórica\
10.16. Rastreabilidade da versão do modelo

## Capítulo 11 — MLflow e ciclo de vida dos modelos

11.1. MLflow Tracking\
11.2. Registro de parâmetros de treinamento\
11.3. Registro de métricas e artefatos\
11.4. Registro das versões dos datasets\
11.5. Model Registry\
11.6. Pipeline completo de pré-processamento e modelo\
11.7. Assinaturas de entrada e saída\
11.8. Modelos PyFunc personalizados\
11.9. Aprovação e publicação dos modelos\
11.10. Aliases para versões aprovadas\
11.11. MLflow Serving via `/invocations`\
11.12. Inferência individual e em lote\
11.13. Versionamento e rollback\
11.14. Monitoramento de inferência\
11.15. Controle de retreinamento

O endpoint nativo `/invocations` receberá os atributos e retornará as atribuições de clusters de modelos publicados. [mlflow.org](https://mlflow.org/docs/latest/ml/deployment/deploy-model-locally/)

## Capítulo 12 — FastAPI e criação dinâmica de clusters

12.1. Configuração das regras de criação via YAML\
12.2. Catálogo de atributos disponíveis\
12.3. Criação dinâmica de combinações\
12.4. Seleção de Pandas ou Polars\
12.5. Seleção de PyCaret ou scikit-learn\
12.6. Seleção das técnicas de pré-processamento\
12.7. Seleção do algoritmo de clustering\
12.8. Configuração de hiperparâmetros\
12.9. Solicitação de treinamento de experimentos\
12.10. Execução de experimentos em fila\
12.11. Consulta do andamento das execuções\
12.12. Consulta de métricas e resultados\
12.13. Consulta de pontos para gráficos X/Y\
12.14. Consulta de reviews por cluster\
12.15. Consulta de históricos das avaliações\
12.16. Comparação de combinações\
12.17. Consulta de perfis e interpretações\
12.18. Aprovação e publicação de modelos\
12.19. Integração com MLflow Serving\
12.20. Autenticação, limites e validação das requisições

### Contratos principais da API

| Método | Endpoint                                        | Finalidade                     |
| ------ | ----------------------------------------------- | ------------------------------ |
| GET    | `/api/v1/clustering/atributos`                  | Atributos permitidos           |
| GET    | `/api/v1/clustering/regras`                     | Regras YAML efetivas           |
| POST   | `/api/v1/clustering/experimentos`               | Criar experimento              |
| GET    | `/api/v1/clustering/experimentos/{id}`          | Status e métricas              |
| GET    | `/api/v1/clustering/experimentos/{id}/clusters` | Clusters encontrados           |
| GET    | `/api/v1/clustering/experimentos/{id}/grafico`  | Dados para gráficos            |
| GET    | `/api/v1/clustering/experimentos/{id}/reviews`  | Avaliações agrupadas           |
| GET    | `/api/v1/reviews/{id}/historico`                | Histórico diário               |
| GET    | `/api/v1/clusters/transicoes`                   | Migrações entre grupos         |
| GET    | `/api/v1/combinacoes/{id}/interpretacao`        | Interpretação executiva        |
| POST   | `/api/v1/clusters/prever`                       | Inferência de novas avaliações |
| POST   | `/api/v1/clustering/experimentos/{id}/publicar` | Publicação de modelo           |

A criação de experimentos ficará separada da inferência, evitando que uma consulta de gráfico dispare treinamento desnecessário.

## Capítulo 13 — Visualizações e dashboards analíticos

13.1. Scatter plot bidimensional\
13.2. Scatter plot tridimensional\
13.3. Gráficos com os valores originais\
13.4. Gráficos após pré-processamento\
13.5. PCA 2D e 3D\
13.6. Heatmap de características dos clusters\
13.7. Boxplots e violin plots\
13.8. Silhouette Plot\
13.9. Dendrogramas\
13.10. Distribuição e representatividade dos clusters\
13.11. Séries temporais de engajamento\
13.12. Matrizes de transição\
13.13. Gráficos de drift\
13.14. Comparação entre jogos\
13.15. Comparação entre algoritmos e pré-processamentos\
13.16. Tabelas detalhadas com filtros\
13.17. Consulta dos textos originais das reviews\
13.18. Exportação dos resultados

### Exemplo: `playtime_at_review` × `comment_count`

Simulação ilustrativa de 15 avaliações divididas em três perfis hipotéticos. Não representa execução real de KMeans.

Poucas horas

Experientes

Alta discussão

03060901200150300450600

Dados e clusters fictícios. Na execução real, os pontos serão coloridos conforme os resultados registrados no Data Lake Gold.

## Capítulo 14 — Interpretação para a equipe de negócio

14.1. Caracterização estatística dos clusters\
14.2. Nomeação descritiva dos perfis\
14.3. Participação percentual de cada grupo\
14.4. Comparação de médias e medianas\
14.5. Experiência × discussão\
14.6. Experiência × utilidade\
14.7. Discussão × votos úteis\
14.8. Perfis multidimensionais de engajamento\
14.9. Evolução diária e semanal dos perfis\
14.10. Interpretação das migrações\
14.11. Comparação de comunidades entre jogos\
14.12. Consulta e leitura humana das reviews\
14.13. Hipóteses e oportunidades de investigação\
14.14. Limitações e incertezas\
14.15. Relatórios executivos e versionamento das interpretações

### Exemplo de resultado executivo

| Cluster            | Participação | Horas médias | Comentários médios |
| ------------------ | ------------ | ------------ | ------------------ |
| 0 — Poucas horas   | 30%          | 35 h         | 2                  |
| 1 — Experientes    | 45%          | 380 h        | 6                  |
| 2 — Alta discussão | 25%          | 220 h        | 68                 |

Valores simulados para ilustrar a interpretação de 10.000 avaliações.

**Exemplo de conclusão para a equipe de negócio:** o grupo mais representativo reúne avaliações publicadas após muitas horas de jogo, mas que receberam poucos comentários. Outro grupo concentra avaliações com mais discussões, mesmo sem apresentar as maiores médias de tempo jogado.

A equipe poderá investigar se esses perfis diferem em recomendações positivas, votos úteis, datas de publicação e comportamento temporal. O clustering, por si só, não estabelece causalidade nem revela o sentimento dos textos.

---

# 4. Capítulo 15 — Observabilidade completa no Grafana

Este capítulo passa a ser um requisito obrigatório do projeto, não apenas uma funcionalidade complementar.

## 15.1. Arquitetura

Steam Collector

Data Lake / MinIO

Pandas / Polars

PyCaret / sklearn

MLflow Serving

FastAPI / Workers

**Instrumentação**

Métricas Prometheus · Logs estruturados · Metadados de execução

**Prometheus**

Séries temporais e regras de alerta

**Alloy → Loki**

Coleta e consulta de logs

**Grafana**

Dashboards operacionais · Diagnóstico · Alertas

O Alloy permite centralizar a coleta de telemetria e integrar métricas e logs com os respectivos backends. [grafana.com](https://grafana.com/docs/alloy/latest/introduction/)

## 15.2. Catálogo dos 12 dashboards de observabilidade

| ID     | Dashboard                | Indicadores principais                               |
| ------ | ------------------------ | ---------------------------------------------------- |
| OBS-01 | Saúde Operacional        | Disponibilidade, execuções, erros, alertas ativos    |
| OBS-02 | Steam Collector          | Latência, HTTP 429, requisições, reviews e cobertura |
| OBS-03 | Data Lake Bronze         | Volume ingerido, uploads, duração e integridade      |
| OBS-04 | Data Lake Silver/Gold    | Registros inválidos, duplicados, atrasos e qualidade |
| OBS-05 | Pandas × Polars          | Tempo de execução, CPU, memória e throughput         |
| OBS-06 | Machine Learning         | Pré-processamento, tuning, treinamento e métricas    |
| OBS-07 | Clustering Temporal      | Drift, ruídos, distribuição e transições             |
| OBS-08 | MLflow Serving           | Latência p50/p95/p99, erros e inferências            |
| OBS-09 | FastAPI e Filas          | Endpoints, requisições, erros e tempo de espera      |
| OBS-10 | Infraestrutura           | CPU, RAM, disco, MinIO e contêineres                 |
| OBS-11 | Logs e Diagnóstico       | Logs estruturados, exceções e falhas por etapa       |
| OBS-12 | Saúde da Observabilidade | Prometheus, Loki, Alloy e exporters                  |

## 15.3. Métricas instrumentadas

Os nomes abaixo são **métricas personalizadas propostas para implementação**, não métricas que já existam automaticamente nas bibliotecas.

| Componente    | Métrica                                          | Tipo      |
| ------------- | ------------------------------------------------ | --------- |
| Coleta        | `steam_api_requests_total`                       | Counter   |
| Coleta        | `steam_api_request_duration_seconds`             | Histogram |
| Coleta        | `steam_api_rate_limits_total`                    | Counter   |
| Coleta        | `steam_collection_last_success_unixtime_seconds` | Gauge     |
| Coleta        | `steam_reviews_revisit_coverage_ratio`           | Gauge     |
| Data Lake     | `steam_lake_records_total`                       | Counter   |
| Data Lake     | `steam_lake_operation_duration_seconds`          | Histogram |
| Qualidade     | `steam_data_invalid_records_total`               | Counter   |
| Qualidade     | `steam_data_null_ratio`                          | Gauge     |
| Processamento | `steam_processing_duration_seconds`              | Histogram |
| Processamento | `steam_processing_memory_peak_bytes`             | Gauge     |
| ML            | `steam_ml_training_duration_seconds`             | Histogram |
| ML            | `steam_ml_experiments_total`                     | Counter   |
| ML            | `steam_ml_cluster_noise_ratio`                   | Gauge     |
| Serving       | `steam_serving_request_duration_seconds`         | Histogram |
| Serving       | `steam_serving_requests_total`                   | Counter   |
| FastAPI       | `steam_http_requests_total`                      | Counter   |
| Workers       | `steam_training_queue_depth`                     | Gauge     |
| Temporal      | `steam_cluster_distribution_ratio`               | Gauge     |
| Temporal      | `steam_cluster_transition_ratio`                 | Gauge     |
| Temporal      | `steam_feature_drift_score`                      | Gauge     |

### Percentis de latência

O Grafana apresentará p50, p95 e p99 para a API Steam, FastAPI, inferência MLflow e etapas relevantes de processamento.

Exemplo de PromQL para p95 usando histograma clássico:

```
histogram_quantile(
  0.95,
  sum by (le) (
    rate(steam_serving_request_duration_seconds_bucket[5m])
  )
)
```

Os histogramas são apropriados para agregar tempos de resposta e calcular percentis entre instâncias; a implementação escolherá buckets coerentes com os SLOs definidos. [prometheus.io](https://prometheus.io/docs/practices/histograms/)

## 15.4. Alertas operacionais

| Alerta                           | Condição proposta                    | Severidade   |
| -------------------------------- | ------------------------------------ | ------------ |
| Coleta diária não concluída      | Última execução excedeu o prazo      | Crítica      |
| Steam API com falhas             | Erros acima do limite configurado    | Atenção      |
| HTTP 429 elevado                 | Rate limiting persistente            | Atenção      |
| Data Lake desatualizado          | Freshness ultrapassou o prazo        | Crítica      |
| Qualidade insuficiente           | Registros inválidos acima do limite  | Atenção      |
| Pipeline interrompido            | Execução falhou                      | Crítica      |
| Memória elevada                  | Consumo acima do limite              | Atenção      |
| Treinamento excessivamente lento | Duração acima do SLO                 | Atenção      |
| Serving indisponível             | Endpoint de saúde falha              | Crítica      |
| Latência p95 elevada             | SLO de resposta violado              | Atenção      |
| Drift significativo              | Limite estatístico ultrapassado      | Investigação |
| Falha no envio de logs           | Alloy/Loki com problemas de ingestão | Atenção      |

Os limites serão configuráveis no YAML. Como a coleta ocorre uma vez ao dia, seus alertas deverão considerar horários esperados e sucesso das execuções, e não exigir tráfego constante.

## 15.5. Regras de instrumentação

O projeto deverá utilizar identificadores de correlação nos logs, como `execucao_id`, `experimento_id` e `request_id`.

Para evitar excesso de séries no Prometheus, identificadores únicos de reviews, requisições ou experimentos não serão utilizados como labels de alta cardinalidade. Esses dados permanecerão nos logs e no MLflow.

Os dashboards permitirão filtrar, quando apropriado, por ambiente, serviço, jogo, etapa, motor, framework e algoritmo. Textos das avaliações e identificadores pessoais não serão registrados em métricas ou logs operacionais.

---

# 5. Capítulo 16 — Infraestrutura e organização do projeto

16.1. Estrutura do código Python\
16.2. Separação das responsabilidades em módulos\
16.3. Configuração centralizada em YAML\
16.4. Interfaces Strategy para Pandas e Polars\
16.5. Adaptadores para PyCaret e scikit-learn\
16.6. Integração MinIO/S3\
16.7. Serviços MLflow Tracking e Serving\
16.8. Serviço FastAPI\
16.9. Workers de treinamento e coleta\
16.10. Banco de metadados e estado das execuções\
16.11. Prometheus, Loki, Alloy e Grafana\
16.12. Provisionamento dos dashboards\
16.13. Docker Compose\
16.14. Gerenciamento de credenciais\
16.15. Configurações de desenvolvimento e produção

### Estrutura de diretórios proposta

```
steam-reviews-clustering/
│
├── app/
│   ├── coleta_steam/
│   ├── acesso_dados/
│   ├── motor_processamento/
│   ├── qualidade_dados/
│   ├── engenharia_atributos/
│   ├── preprocessamento_dados/
│   ├── framework_ml/
│   ├── agrupamento_modelos/
│   ├── avaliacao_modelos/
│   ├── analise_temporal/
│   ├── registro_mlflow/
│   ├── api_negocio/
│   ├── interpretacao_negocio/
│   ├── metricas_observabilidade/
│   └── orquestracao_tarefas/
│
├── config/
│   ├── projeto.yaml
│   ├── steam.yaml
│   ├── datalake.yaml
│   ├── processamento.yaml
│   ├── preprocessamento.yaml
│   ├── machine_learning.yaml
│   ├── clustering.yaml
│   ├── temporal.yaml
│   ├── serving.yaml
│   └── observabilidade.yaml
│
├── infra/
│   ├── prometheus/
│   ├── grafana/
│   │   ├── dashboards/
│   │   │   ├── observabilidade/
│   │   │   ├── analiticos/
│   │   │   └── executivos/
│   │   └── provisioning/
│   ├── loki/
│   ├── alloy/
│   └── mlflow/
│
├── tests/
├── docs/
├── Dockerfile
├── compose.yaml
├── pyproject.toml
└── README.md
```

Os dados históricos ficarão nos buckets do Data Lake, e os artefatos de modelos terão armazenamento gerenciado pelo MLflow. Não será necessário utilizar diretórios locais permanentes para armazenar os resultados analíticos.

# 6. Capítulo 17 — Testes, segurança e governança

17.1. Testes unitários\
17.2. Testes de integração com a API Steam\
17.3. Testes de processamento Bronze/Silver/Gold\
17.4. Testes de equivalência Pandas/Polars\
17.5. Testes dos adaptadores PyCaret/scikit-learn\
17.6. Testes de pré-processamento\
17.7. Testes de reprodutibilidade de clustering\
17.8. Testes de cobertura temporal\
17.9. Testes dos contratos FastAPI\
17.10. Testes de inferência MLflow\
17.11. Testes de carga e desempenho\
17.12. Validação das métricas de observabilidade\
17.13. Segurança dos endpoints\
17.14. Controle de acesso aos dados e textos\
17.15. Governança e aprovação dos modelos\
17.16. Documentação e manutenção

# 7. Capítulo 18 — Entregáveis e critérios de aceite

| Entregável              | Critério de aceite                                            |
| ----------------------- | ------------------------------------------------------------- |
| Coletor Steam           | Coleta diária rastreável, com falhas e cobertura documentadas |
| Data Lake               | Bronze, Silver e Gold operacionais                            |
| Pandas/Polars           | Motor selecionável por YAML                                   |
| PyCaret/sklearn         | Framework selecionável por YAML                               |
| Pré-processamento       | Técnicas combináveis e reproduzíveis                          |
| Clustering              | Treinamento, tuning e avaliação                               |
| Clustering temporal     | Snapshots, transições e métricas de evolução                  |
| MLflow                  | Registro, publicação e serving                                |
| FastAPI                 | Criação e consulta dinâmica de clusters                       |
| Dashboard analítico     | Gráficos e tabelas por combinação                             |
| Dashboard executivo     | Perfis e interpretações de negócio                            |
| Grafana Observabilidade | 12 dashboards operacionais                                    |
| Alertas                 | Alertas de coleta, dados, modelos e infraestrutura            |
| Documentação            | Arquitetura, YAML, APIs e metodologia                         |
| Testes                  | Verificações automatizadas dos componentes críticos           |

---

# 8. Exemplo integrado de configuração YAML

O arquivo abaixo resume as principais decisões configuráveis. Os parâmetros específicos de cada técnica ficarão nos arquivos especializados.

```
projeto:
  nome: steam_reviews_clustering
  idioma: brazilian
  utilizar_pln: false

coleta:
  frequencia: diaria
  appids: [427520]
  preservar_historico: true
  revisitar_reviews: true

datalake:
  armazenamento: minio
  buckets:
    bronze: steam-bronze
    silver: steam-silver
    gold: steam-gold

processamento:
  motor_padrao: polars
  motores_permitidos: [pandas, polars]

machine_learning:
  framework_padrao: sklearn
  frameworks_permitidos: [sklearn, pycaret]

clustering_api:
  permitir_combinacoes_dinamicas: true

  atributos:
    minimo: 2
    maximo: 6
    permitidos:
      - playtime_at_review
      - playtime_forever
      - comment_count
      - votes_up
      - votes_funny
      - num_reviews

  preprocessamento:
    ausentes: remover
    outliers: preservar
    transformacao: log1p
    escalonamento: robust
    pca: false

  algoritmos:
    permitidos:
      - kmeans
      - minibatch_kmeans
      - dbscan
      - hdbscan
      - agglomerative

  avaliacao:
    metricas:
      - silhouette
      - davies_bouldin
      - calinski_harabasz
    estabilidade: true

  treinamento:
    modo: fila
    publicacao_automatica: false

temporal:
  ativado: true
  janelas_dias: [1, 7, 14, 30]
  acompanhar_transicoes: true
  monitorar_drift: true

mlflow:
  tracking: true
  registry: true
  serving: true

fastapi:
  ativado: true
  prefixo: /api/v1

observabilidade:
  ativado: true

  servicos:
    prometheus: true
    grafana: true
    loki: true
    alloy: true

  metricas:
    latencia_percentis: [50, 95, 99]
    throughput: true
    taxa_erros: true
    cpu: true
    memoria: true
    cobertura_coleta: true
    freshness_dados: true
    qualidade_dados: true
    duracao_treinamento: true
    desempenho_serving: true
    drift: true

  dashboards:
    coletor_steam: true
    datalake_bronze: true
    datalake_silver_gold: true
    processamento: true
    machine_learning: true
    clustering_temporal: true
    mlflow_serving: true
    fastapi: true
    infraestrutura: true
    logs: true
    saude_observabilidade: true
    visao_geral: true

  alertas:
    coleta_atrasada: true
    api_indisponivel: true
    qualidade_insuficiente: true
    latencia_elevada: true
    drift_detectado: true
```

Esses nomes são parte do contrato de configuração proposto e deverão ser implementados e validados pelo projeto; não são opções nativas universais das ferramentas.

## 9. Resultado esperado para a equipe de negócio

A plataforma deverá permitir uma consulta como:

> Mostre os agrupamentos de avaliações de Factorio utilizando horas jogadas no momento da review e quantidade de comentários, com pré-processamento logarítmico e RobustScaler. Apresente os três principais perfis, suas avaliações, a evolução dos últimos sete dias e a interpretação de cada grupo.

O resultado reunirá o gráfico de dispersão, a tabela de reviews, as estatísticas dos clusters, as mudanças temporais e a interpretação de negócio.

Em paralelo, os dashboards de observabilidade permitirão verificar se a coleta do jogo ocorreu corretamente, se o dataset está atualizado, quanto tempo o treinamento consumiu e se os endpoints de consulta e inferência estão funcionando dentro dos limites definidos.

**Esta versão 3.2 consolida o projeto em 18 capítulos, com Data Lake histórico, escolha de Pandas/Polars e PyCaret/scikit-learn, pré-processamento via YAML, clustering dinâmico e temporal, MLflow/FastAPI e 12 dashboards obrigatórios de observabilidade no Grafana.**