---
trigger: model_decision
description: Regras para a área configuracao no projeto Steam Reviews Clustering.
---
# Regras de configuracao

Opções variáveis **somente YAML**: appids, filtros, coleta, motores, frameworks, etapas, atributos, combinações, outliers, imputação, escalonadores, PCA, algoritmos, tuning, drift, métricas, alertas, thresholds e regras de negócio. Validar schemas e valores, recusar técnicas incompatíveis. Sem `eval/exec` para configurações. Segredos por variável de ambiente/secret manager e nunca em YAML versionado.

Fonte normativa adicional: `docs/fontes/regras_python_originais.txt` e `docs/fontes/escopo_steam_v32.md`.
