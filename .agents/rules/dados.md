---
trigger: model_decision
description: Regras para a área dados no projeto Steam Reviews Clustering.
---
# Regras de dados

Usar Pandas vetorizado; evitar iterrows/itertuples/apply(axis=1) e loops linha a linha. Polars: preferir expressões nativas `select`, `with_columns`, `filter`, `group_by`, joins, `LazyFrame`/scan para fluxos extensos, materialização somente quando necessária. Comparar resultados e custos dos motores e minimizar conversões. Ajustar pré-processamento em dados de treino ou folds apropriados para evitar leakage.

Fonte normativa adicional: `docs/fontes/regras_python_originais.txt` e `docs/fontes/escopo_steam_v32.md`.
