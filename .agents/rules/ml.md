---
trigger: model_decision
description: Regras para a área ml no projeto Steam Reviews Clustering.
---
# Regras de ml

Clustering não supervisionado de atributos numéricos/categóricos sem usar textos. Implementar adapters sklearn e PyCaret com recursos nativos comprovados. Algoritmos KMeans, MiniBatchKMeans, DBSCAN, HDBSCAN, Agglomerative; selecionar métricas Silhouette, DBI, CHI, ARI/NMI quando computáveis, junto de tamanhos/ruído/interpretabilidade. Nunca supor predict() para algoritmos transdutivos; estratégia explícita de inferência ou erro de capacidade. Pré-processamento uma vez só; registrar todos artefatos e assinaturas no MLflow.

Fonte normativa adicional: `docs/fontes/regras_python_originais.txt` e `docs/fontes/escopo_steam_v32.md`.
