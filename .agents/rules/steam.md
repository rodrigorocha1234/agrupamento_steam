---
trigger: model_decision
description: Regras para a área steam no projeto Steam Reviews Clustering.
---
# Regras de steam

Sem PLN no treinamento. Coleta com `IUserReviewsService/GetAppReviews`, locale `brazilian`, múltiplos appids, paginação, retry/backoff 429, rastreio e revisitação diária planejada. `timestamp_created` e `timestamp_updated` não equivalem à data em que foi observada cada review. Deltas de votos e comentários exigem dois snapshots realmente observados. Não inferir geolocalização do idioma. Bronze imutável bruto, Silver limpo com histórico, Gold analítico versionado.

Fonte normativa adicional: `docs/fontes/regras_python_originais.txt` e `docs/fontes/escopo_steam_v32.md`.
