---
trigger: model_decision
description: Regras para a área infra no projeto Steam Reviews Clustering.
---
# Regras de infra

Inspecionar **antes** o Docker Compose da raiz e services, redes, volumes existentes. Adicionar mínimo necessário sem duplicar MinIO, MLflow, Grafana, Prometheus, Loki, Alloy ou banco. Nunca `docker compose down -v`, prune, apagamento de buckets ou deploy sem autorização. Evidenciar alterações em diff.

Fonte normativa adicional: `docs/fontes/regras_python_originais.txt` e `docs/fontes/escopo_steam_v32.md`.
