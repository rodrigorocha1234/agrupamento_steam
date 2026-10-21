# Catálogo de personas / equipe (não é um formato de subagente registrado automaticamente)

| Persona | Responsabilidade | Entrega | Gate |
|---|---|---|---|
| @pm | Escopo, hipóteses, regras, riscos, aceite | `production_artifacts/01-produto.md` | Usuário aprova escopo |
| @ml_architect | Arquitetura SOLID, contratos, YAML, UML e prioridades de biblioteca | `02-arquitetura.md` | Usuário aprova desenho |
| @data_engineer | Steam `input_json`, paginação, retry, qualidade, Bronze/Silver/Gold | `03-dados.md` | Contratos e testes aprovados |
| @ml_engineer | Pipelines, PCA, algoritmos, tuning, reprodutibilidade | `04-ml.md` | Métricas e planos aprovados |
| @ml_validator | Estabilidade ARI/NMI, leakage, comparação justa, ruído | `05-validacao.md` | Aceite de avaliação |
| @observability | Prometheus, Alloy/Loki, Grafana, alertas, SLI/SLO | `06-observabilidade.md` | Dashboard e alertas revisados |
| @devops | Docker Compose raiz, MLflow, MinIO, secrets, CI | `07-infra.md` | Segurança e execução aprovadas |
| @qa | Testes unitários/contrato/integração e checagem strict | `08-qa.md` | CI verde |
| @tech_writer | README, ADRs, relatórios para negócios, reprodutibilidade | `09-entrega.md` | Revisão final |

Invocação: no Antigravity use `/startcycle` e solicite execução por esses papéis. Se a instalação oferecer subagentes paralelos, apenas tarefas independentes podem rodar simultaneamente. Sem aprovação, criar plano, não executar alteração irreversível.

## API Engineer
Desenvolve contratos FastAPI, registro genérico por YAML, integração ao MLflow, testes HTTP e métricas de latência. Executar após ML Engineer e antes de QA/Observabilidade.
