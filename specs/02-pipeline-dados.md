# SPEC 02 — pipeline Bronze / Silver / Gold

Bronze: payload de coleta em MinIO com retenção controlada e exclusão do texto de reviews por padrão; metadados de proveniência (appid, capturado_em, query sem segredo, cursor hash).
Silver: schema tipado, conversão temporal, flatten de author, dedupe `(appid,recommendationid)`, nullability e campos numéricos. Quality Gate com report quantitativo. Gold: features para ML e relatórios agregados, sem steamid nem texto. Usar `assign`, `where`, `mask`, groupby, join; não `iterrows`/`itertuples`/`apply(axis=1)`.

Features derivadas: horas_jogadas, horas_ate_review, horas_apos_review com `clip(lower=0)` e marcador de inconsistência, atividade_recente=playtime_last_two_weeks/max(playtime_forever,1), engajamento= votes_up+votes_funny+comment_count (indicador exploratório). Temporalidade: `playtime_forever` é snapshot no momento de extração.

Quality Gate e métricas: % inválidas, duplicadas, nulos por campo, cobertura por jogo, frescor, taxa 429; critérios no YAML e registrar decisão de descarte.
