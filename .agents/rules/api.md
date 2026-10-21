---
trigger: model_decision
description: Regras para a área api no projeto Steam Reviews Clustering.
---
# Regras de api

FastAPI orquestra experimentos/consulta e valida configurações; MLflow Serving `/invocations` serve modelos publicados. POST para criar experimento é assíncrono, GET não deve iniciar treinamento. GET de reviews por cluster deve ter paginação, filtro, controle de acesso e não expor autor ou dados sensíveis indevidamente. Versões de combinações, dados, modelos e pipelines obrigatórias; publicação condicionada a aprovação.

Fonte normativa adicional: `docs/fontes/regras_python_originais.txt` e `docs/fontes/escopo_steam_v32.md`.
