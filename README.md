# Steam Reviews Clustering Brasil — Google Antigravity

Pacote de **contexto multiagente + specs/rules + esqueleto executável mínimo**. Não é um pipeline de produção finalizado. As implementações completas são tarefas dos agentes e exigem aprovação nos gates.

## Uso
1. Extraia e abra a pasta raiz no Antigravity.
2. Leia `AGENTS.md`, `specs/00-visao-geral.md` e `docs/roteiro-implementacao.md`.
3. No chat do agente execute `/startcycle` (skill atual em `.agents/skills/startcycle/SKILL.md`).
4. Aprovar/revisar os artefatos de cada etapa em `production_artifacts/` antes de implementar.
5. Para testar o esqueleto: `python -m pip install -e '.[dev]' && pytest`.

## Nota de atualização (21/10/2026)
Artigo de Peterson Pereira demonstra personas, skills e workflows legados. A documentação oficial indica descontinuação de workflows em 19/10/2026: este projeto usa **Agent Skills** (`SKILL.md`) no lugar de `.agents/workflows/*.md`. O arquivo `.agents/agents.md` é um catálogo de papéis para a equipe; `AGENTS.md` na raiz contém instruções automaticamente reconhecidas. A definição de papéis **não instancia agentes por si só**; o orquestrador coordena conversas/subagentes conforme recursos da instalação.

## Segurança e escopo
- Sem PLN, embeddings ou processamento de texto de reviews.
- `brazilian` = idioma, não nacionalidade/residência. Não criar inferências geográficas.
- Sem salvar textos das reviews nem steamid nos artefatos Gold/MLflow/Grafana.
- Steam: Service API `GetAppReviews/v1/` com `input_json` (não enviar parâmetros de forma plana). `key` opcional, apenas se legitimamente autorizada.
- Persistência de produção no MinIO e rastreabilidade no MLflow; testes podem usar fixtures em memória.

Fontes: https://pt.linkedin.com/pulse/google-antigravity-na-pr%C3%A1tica-criando-um-pipeline-com-peterson-alves-nm7of ; https://www.antigravity.google/docs/rules/ ; https://www.antigravity.google/docs/skills/ ; https://www.antigravity.google/docs/migration/workflows-to-skills/ ; https://partner.steamgames.com/doc/webapi/IUserReviewsService

## Reutilização e Serving (incremento)
O motor experimental genérico está em `app/nucleo_agrupamento/` e independe de Steam. Consulte `specs/07-motor-generico.md`.
Um exemplo **sintético** de KMeans registrável via MLflow pyfunc foi incluído em `app/servico_modelo/`; consulte `specs/06-mlflow-serving.md` e `docs/serving-guia.md`.
O endpoint `/invocations` é disponibilizado por `mlflow models serve` sem FastAPI após criar bucket, treinar e aprovar a versão. Não é pipeline completo pronto para produção.

## FastAPI integrada ao MLflow
O serviço `api` expõe `http://localhost:8081/docs`, `POST /api/v1/predict`, `POST /api/v1/predict-batch`, `/health`, `/ready` e `/metrics`. O projeto precisa de um modelo registrado em `models:/agrupamento_steam_kmeans@champion` para inferências reais.

Execute `docker compose up -d --build api` (após configurar `.env` e criar infraestrutura e modelo); mantenha `serving` em perfil opcional. A API carrega modelos sob demanda. A versão do campeão permanece em cache até reiniciar o processo. Para demonstração sem modelo registrado, rode os testes com motor simulado.

Exemplo de formato: `{"atributos":{"playtime_forever":120, ...}}`, incluindo exatamente as colunas da configuração `configuracoes/api_servico.yaml`. Ajuste o YAML ao contrato real do modelo; o exemplo inicial inclui campos que podem ser excluídos do treinamento.

Monitoramento: dashboard Grafana **11 — Clustering API Observability**. Para produção: implementar autenticação, limitação de requisições e endurecimento de segurança.


## Ambiente isolado Steam (decisão arquitetural)
Esta implantação atende exclusivamente reviews Steam; os endpoints não incluem `{projeto}`. Para reutilizar o motor em YouTube/FIPE, crie outro ambiente com seu próprio Compose, configuração, MLflow e API. Veja `specs/08-fastapi.md`.


## Seleção PyCaret / sklearn no YAML

Ajustar `motor_agrupamento.engine` para `sklearn` (padrão) ou `pycaret`. Para PyCaret instalar `pip install -e ".[pycaret]"`. PyCaret 4 usa API OOP; `setup()` global é legado PyCaret 3. Ver `specs/09-selecao-engine.md`. O teste real do PyCaret requer instalar o extra e executar no contêiner.
