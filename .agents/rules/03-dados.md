---
trigger: always_on
description: Regras persistentes 03-dados.md
---
# 03-dados.md

API Steam `/IUserReviewsService/GetAppReviews/v1/` GET com parâmetro `input_json` JSON serializado. Idioma `brazilian` indica idioma, não país. Não usar PLN nem armazenar texto de reviews no Gold. Paginação cursor Recent (enum 1), até 100/page, deduplicar `(appid,recommendationid)`; HTTP 429 retry com backoff+jitter e limite; janela Unix start/end em pares; chave de publisher opcional apenas autorizada. Qualidade e lineage de Bronze/Silver/Gold; MinIO como persistência.
