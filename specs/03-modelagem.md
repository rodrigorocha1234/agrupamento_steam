# SPEC 03 — Machine Learning

3 variantes: A experiência, B repercussão, C combinado. Treinamento separado por jogo e conjunto; evitar leakage de `appid` no input em análise comparativa inicial. `voted_up` apenas para pós-análise nos experimentos A/B. Booleanos representados com codificação explícita e ponderação de escalas. Evitar redundância de features altamente correlacionadas.

Preprocessamento numérico: log1p opcional para assimetria, Standard/MinMax/Robust/Power; categóricos OneHot; PCA nenhum/2/3/95% quando tecnicamente possível. Treinadores Strategy; scoring interno, busca Grid ou Random reproduzível. Métricas Silhouette↑, Davies-Bouldin↓, Calinski-Harabasz↑, estabilidade ARI/NMI, cobertura/ruído para DBSCAN/HDBSCAN. Não usar Folds supervisionados como padrão de clustering: avaliação por reamostragem/estabilidade e particionamentos comparáveis.

Protocolo: separar janelas temporais para diagnóstico de drift, sem afirmar previsão causal; selecionar por métrica multiobjetivo e interpretabilidade, não apenas Silhouette. MLflow para parâmetros, features, seed, versões, métricas e artefatos. Perfis definidos apenas após fitting, não rótulos verdadeiros.
