---
name: engines
description: Implementar, testar e avaliar a seleção configurável PyCaret ou sklearn para clustering Steam.
---
# Skill: Engines de Clustering
1. Ler `specs/09-selecao-engine.md`, `.agents/rules/09-engines.md` e `configuracoes/projeto_base.yaml`.
2. Confirmar versões de PyCaret e sklearn compatíveis com Python 3.12.
3. Implementar a engine selecionada pelo YAML com ferramentas nativas, sem alterar os endpoints Steam.
4. Adicionar/expandir tuners, métricas, MLflow e testes de contrato.
5. Revalidar `pyfunc` e FastAPI usando um modelo registrado de cada engine; exigir `/ready` funcional.
