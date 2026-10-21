# Guia demonstrativo — MLflow serving sem FastAPI

**Pré-requisitos:** Docker Compose, portas locais 5000 e 8080, credenciais .env válidas e bucket `mlflow-artifacts` existente no MinIO (criar manualmente ou provisionar).

1. `cp .env.example .env` e configurar credenciais.
2. `docker compose up -d postgres minio mlflow`.
3. Criar o bucket `mlflow-artifacts` no MinIO. A configuração não o cria automaticamente.
4. Executar o treino sintético dentro do container MLflow: `docker compose exec mlflow python -m app.servico_modelo.treinar_exemplo`. Confirmar no MLflow UI a versão criada.
5. Após revisão humana: `docker compose exec mlflow python -m app.servico_modelo.promover_modelo --versao 1 --aprovado` (substituir 1 pela versão real).
6. `docker compose --profile serving up -d serving`.
7. Exemplo:

```bash
curl -X POST http://localhost:8080/invocations \
 -H 'Content-Type: application/json' \
 -d '{"dataframe_records":[{"horas_jogadas":120.0,"votos_uteis":8.0,"recebido_gratis":"nao"}]}'
```

Servidor esperado: DataFrame serializado com colunas `cluster` e `perfil`.

**Escopo:** somente exemplo sintético KMeans, não coleta/treino Steam real. Versão no exemplo é ilustrativa; consultar Registry. Acesso via 127.0.0.1 somente. Para produção exigem-se autenticação, gestão de segredos, proxy de instrumentação, testes integrados e Quality Gates.
