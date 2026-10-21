# SPEC 08 — FastAPI exclusiva do ambiente Steam

## Decisão
- Uma instalação Docker Compose por domínio de negócio. Esta instalação contém apenas Steam.
- O motor de clustering é reutilizável como biblioteca/código; **não** hospedar modelos YouTube/FIPE nesta API.
- Um único modelo MLflow configurado em `configuracoes/api_servico.yaml`, com alias `champion`.
- Não incluir `{projeto}` no caminho HTTP.

## Endpoints
- `GET /health`: liveness do processo.
- `GET /ready`: 200 apenas quando versão do modelo MLflow puder ser carregada, senão 503.
- `GET /metrics`: métricas Prometheus (restringir rede).
- `GET /api/v1/model`: nome, alias e contrato de atributos.
- `GET /api/v1/clusters`: perfis interpretados e aprovados; vazio antes da aprovação.
- `GET /api/v1/clusters/{cluster_id}`: perfil aprovado ou 404.
- `POST /api/v1/predict`: `{ "atributos": { ... } }`.
- `POST /api/v1/predict-batch`: `{ "registros": [{"atributos": {...}}] }`.
- Resposta de inferência inclui o cluster, nome do modelo, versão, perfil opcional e status.

## Regras
- A API não realiza treinamento; o modelo é encapsulado em MLflow pyfunc.
- Checar os campos esperados antes da inferência; ausentes/extras = 422; lote excessivo = 413; falha MLflow = 503.
- Perfis de clusters só devem ser publicados após avaliação real. Números de simulação não são resultados.
- Não expor atributos pessoais, segredos, nem detalhes internos de falhas.
- Autenticação e limitação de chamadas são necessárias antes de uso público.
- Outros projetos devem reutilizar os contratos e o motor em seus próprios ambientes e configurações.
