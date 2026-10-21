# Contexto multiagente para Google Antigravity — Steam Reviews Clustering

Pacote **de governança, não aplicação implementada**. Adaptado do artigo de Peterson Pereira (03/04/2026) e atualizado para o formato oficial de Antigravity em 21/10/2026.

## Como instalar
1. Extraia na **raiz** do repositório existente; preserve o Compose e código atual (backup e diff antes de mesclar).
2. Leia `AGENTS.md`, `.agents/specs/` e os documentos integrais `docs/fontes/`.
3. Abra o workspace no Antigravity App/CLI/IDE; rules e skills são descobertas automaticamente; subagentes `.agents/agents/*.md` documentados para App/CLI (ver compatibilidade da versão).
4. Peça: `Use a skill /planejar-steam para revisar as specs e produzir a especificação aprovada. Antes de infraestrutura, inspecione o Docker Compose existente.`
5. Depois de aprovar: `/implementar-steam`. Para revisão: `/auditar-steam`. Observabilidade: `/observar-steam`.

## Avisos
- O artigo usa `.agents/agents.md`, arquivos de skill soltos e `.agents/workflows/*.md` como padrão de 2026-04. A documentação atual usa subagentes em `.agents/agents/*.md`, skills em `.agents/skills/<nome>/SKILL.md` e regras em `.agents/rules/*.md`. Workflows legados deixam de funcionar a partir de 19/10/2026.
- Referências a `@pm` são papéis para delegação, não garantia de slash commands nativos. Skills podem ser chamadas por `/nome-da-skill` nas superfícies compatíveis.
- **Não há compose.yaml neste pacote**: o original deve ser lido no workspace antes de qualquer edição, conforme pedido do usuário.
- Os fontes originais foram preservados integralmente em `docs/fontes` e são autoridade para regras e escopo.

## Fontes
- https://pt.linkedin.com/pulse/google-antigravity-na-pr%C3%A1tica-criando-um-pipeline-com-peterson-alves-nm7of
- https://www.antigravity.google/docs/rules/
- https://www.antigravity.google/docs/skills/
- https://www.antigravity.google/docs/subagents/
- https://www.antigravity.google/docs/migration/workflows-to-skills/
