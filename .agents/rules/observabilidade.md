---
trigger: model_decision
description: Regras para a área observabilidade no projeto Steam Reviews Clustering.
---
# Regras de observabilidade

Entregar 12 dashboards OBS-01..OBS-12 no Grafana: operacional, coleta, Bronze, Silver/Gold, Pandas/Polars, ML, temporal, MLflow, FastAPI/filas, infraestrutura, logs e saúde da observabilidade. Prometheus métricas; Alloy → Loki logs estruturados com IDs de correlação; p50/p95/p99 por histograma, throughput, taxas erro, qualidade, freshness, drift e SLO. Etiquetas por jogo/motor/framework/algoritmo/técnica de pré-processamento com cardinalidade controlada; IDs únicos e textos nunca como labels. Alertas diários baseados em deadline de coleta, não tráfego constante.

Fonte normativa adicional: `docs/fontes/regras_python_originais.txt` e `docs/fontes/escopo_steam_v32.md`.
