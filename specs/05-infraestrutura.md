# SPEC 05 — Infra e testes

Docker Compose único na raiz: app job/worker sob demanda, MinIO armazenamento S3, MLflow tracking server com artifact store MinIO e metastore Postgres, Prometheus, Grafana, Loki, Alloy; serviços de sistema/exporters conforme limites da máquina. Evitar armazenamento persistente local para dados/artefatos operacionais: Docker volumes persistentes para serviços de infraestrutura são aceitáveis, não salvar datasets no filesystem da aplicação.

CI: `pytest`, `ruff`, verificação strict mypy ou pyright (escolher e documentar). Testes de contrato da API com payload sintético, retries, rate limiting, paginação e limite, schema, vetorização, scoring/ruído; smoke test Compose e provisionamento Grafana. Fixar versões/reprodutibilidade; `.env.example` sem segredos. Entregas verificadas por logs/evidências, sem alegar CI executado se não ocorreu.
