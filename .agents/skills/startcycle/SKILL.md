---
name: startcycle
description: Inicia ciclo de especificação, implementação, validação e observabilidade do projeto Steam Reviews com agentes especializados e gates humanos.
---
# Ciclo multiagente

1. Leia `AGENTS.md`, `.agents/agents.md`, `specs/`, `.agents/rules/`, `docs/regras-python-originais.txt`.
2. Acione papel @pm (`/produto` ou equivalente) e crie `production_artifacts/01-produto.md` com escopo, backlog, limites Steam, critérios. **PARE para aprovação humana**.
3. Após aprovação, papel @ml_architect e @data_engineer definem contratos, desenho e esquema dos dados; produzem `02-arquitetura.md` e `03-dados.md`. **PARE**.
4. Após aprovação, papel @ml_engineer e @ml_validator apresentam planos de clustering, tuning e avaliação. **PARE**.
5. Após aprovação, @observability e @devops planejam Compose, dashboards e alertas. **PARE**.
6. Após aprovação, implementar incrementalmente, rodar pytest/checagem estrita, registrar evidências e handoff por etapa.
7. @qa e @tech_writer revisam, produzem `09-entrega.md`, relatam pendências reais e solicitam aceite final.

Não alegue agentes lançados automaticamente; as skills são instruções para a conversa/ambiente que as invoca. Não executar passos bloqueados sem aceite.
