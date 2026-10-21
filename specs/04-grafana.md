# SPEC 04 — Observabilidade e dashboards

**10 dashboards**: 01 Geral, 02 Steam API, 03 Bronze/Silver/Gold, 04 Qualidade, 05 ML/Tuning, 06 Métricas Clustering, 07 Distribuição Clusters, 08 Infraestrutura, 09 Logs/Erros, 10 Drift.

- Histograma `steam_request_duration_seconds{resultado}` e p50/p95/p99 por `histogram_quantile`; counters `steam_requests_total`, `steam_http_errors_total{status}`, `steam_rate_limits_total`, `steam_retries_total`, `steam_reviews_collected_total{appid}`.
- Pipeline: `pipeline_stage_duration_seconds{etapa}`, `pipeline_stage_errors_total{etapa}`, throughput, qualidade e frescor. ML: duração por algoritmo, falhas, métricas por experimento no MLflow, somente agregações estáveis em Prometheus. `ml_cluster_size{appid,cluster}` somente se cardinalidade limitada.
- Prometheus scrapes, provision Grafana por JSON/datasources, Alloy → Loki logs JSON, alertas por erro HTTP, p95, qualidade dados e serviços. Incluir CPU/memória com exporters se disponíveis.
- Drift: PSI/Jensen-Shannon/KS conforme atributo e referência de coleta, com tamanho de amostra mínimo. Drift não é prova de deterioração do modelo, gerar diagnóstico.
- Sem steamid, recommendationid ou run_id como labels. Alertas definidos em YAML e aplicados por camada de provisionamento; segredos env.
