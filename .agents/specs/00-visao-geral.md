# Especificação principal — Steam Reviews Clustering v3.2

**Estado:** BASE DE REQUISITOS, implementação sujeita à inspeção do repositório e aprovação.

## Objetivo
Reviews de jogos Steam com filtro `brazilian`, coletadas diariamente e revisitadas, sem PLN. Perfis por combinação selecionável de dados numéricos, categóricos e derivados; resultados de negócio e comparações temporal, entre jogos e entre técnicas.

## Capítulos de referência (18)
01 Planejamento; 02 API Steam; 03 Data Lake; 04 Processamento Pandas/Polars; 05 Qualidade e EDA; 06 Engenharia de atributos; 07 Pré-processamento YAML; 08 PyCaret/sklearn; 09 Clustering e tuning; 10 Análise temporal; 11 MLflow; 12 FastAPI; 13 Visualizações; 14 Negócio; 15 Observabilidade; 16 Infraestrutura; 17 Testes/governança; 18 Entregáveis.

## Invariantes
- Sem análise de sentimentos/PLN; texto da review pode ser consultado com acesso controlado.
- Multiple appids; conjuntos individual, conjunto e comparativo; filtro de idioma não é nacionalidade.
- Snapshots da mesma review apenas em datas **realmente observadas**; cobertura de revisitação monitorada.
- Bronze JSON bruto, Silver histórico normalizado, Gold features/perfis/artefatos analíticos; persistência S3/MinIO.
- Framework por YAML: sklearn/PyCaret; motor tabular: Pandas/Polars; combinação de 2 a 6 atributos, conforme configuração.
- Train/tune/assess, MLflow Tracking/Registry/Serving, FastAPI de orquestração; inferência apenas para modelo compatível e aprovado.
- Grafana 12 painéis operacionais separados dos dashboards analíticos e executivos.

## Gates
G0 leitura do Compose existente; G1 aprovação das specs; G2 revisão de arquitetura; G3 aprovação da publicação após QA.

Requisito original integral: `docs/fontes/escopo_steam_v32.md`.
