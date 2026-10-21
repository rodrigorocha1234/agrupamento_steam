# SPEC 01 — contrato Steam

Documentação: https://partner.steamgames.com/doc/webapi/IUserReviewsService

- Endpoint GET `https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/`; parâmetros de método dentro de `input_json` serializado. Chave publisher opcional, NUNCA registrar a chave.
- Campos solicitados: `appid`, `filter` enum (Recent=1), `languages` array (`brazilian`), `review_type` enum, `purchase_type` enum, `num_per_page`<=100, `cursor`, `date_range_start` e `date_range_end`, `filter_offtopic_activity` (true filtra outliers off-topic), `display_language`.
- `day_range` somente aplica a filtro Helpful, não implementar como equivalente a intervalo Recent.
- Cursor iniciar em '*', parar em lista vazia, limite de registros ou cursor repetido; não alegar paginação infinita.
- 429: aguardar Retry-After quando presente, backoff exponencial+jitter com tentativas limitadas; timeouts e erros transitórios; logs e métricas de todas as tentativas.
- Resposta: `reviews`, `cursor`, `total_matching`, `query_summary`; campos do autor num_reviews/playtime_*; dados booleanos voted_up/steam_purchase/received_for_free/early_access/refunded, votos e comentários.
- `language=brazilian` indica idioma, não geolocalização.
- Primeira entrega: contrato mockado, teste de input_json e sanitização de logs. Validar resposta real somente com conectividade/autorizações.
