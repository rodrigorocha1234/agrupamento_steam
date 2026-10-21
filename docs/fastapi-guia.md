# FastAPI — instância dedicada a Steam Reviews

Esta API hospeda apenas o modelo de clustering de reviews Steam. Para YouTube, FIPE ou SPTrans, crie outro ambiente e reutilize o motor sem compartilhar esta API.

## Implantação inicial
1. Configure `.env` sem versionar credenciais.
2. Execute `docker compose up -d --build postgres minio mlflow prometheus loki alloy grafana`.
3. Crie o bucket MinIO de artefatos previsto no Compose.
4. Treine e registre o modelo Steam real no MLflow; após aprovação, atribua o alias `champion`.
5. Confira as colunas e os tipos em `configuracoes/api_servico.yaml`.
6. Execute `docker compose up -d --build api`.
7. Swagger: `http://localhost:8081/docs`; Prometheus: `GET /metrics`.
8. Após alterar o alias do modelo, reinicie a API para invalidar o cache em memória.

## Rotas
- `GET /health`, `GET /ready`, `GET /metrics`
- `GET /api/v1/model`
- `GET /api/v1/clusters`, `GET /api/v1/clusters/{cluster_id}`
- `POST /api/v1/predict`, `POST /api/v1/predict-batch`

## Exemplo
```bash
curl -X POST http://localhost:8081/api/v1/predict \
  -H 'Content-Type: application/json' \
  -d '{"atributos":{"playtime_forever":120,"playtime_at_review":60,"playtime_last_two_weeks":10,"num_reviews":2,"votes_up":1,"votes_funny":0,"weighted_vote_score":0.5,"comment_count":0,"voted_up":true,"steam_purchase":true,"received_for_free":false,"written_during_early_access":false}}'
```

Observação: rótulos dos clusters exigem interpretação e aprovação humana. `/health` não equivale a `/ready`.
