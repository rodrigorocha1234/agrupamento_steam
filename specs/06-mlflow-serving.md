# SPEC 06 — MLflow Registry e Serving nativo

## Objetivo
Treinar, registrar, versionar e disponibilizar um pipeline de clustering **sem FastAPI** via `mlflow models serve` (`POST /invocations`). Tracking, registry e artifacts devem usar MLflow/PostgreSQL/MinIO.

## Contratos
- Um único artefato MLflow pyfunc encapsula imputação, transformação, codificação, PCA opcional e `KMeans.predict` (nunca treinar novamente no serving).
- Contrato de entrada é um pandas.DataFrame com colunas declaradas no YAML e schema de assinatura registrado. Não aceitar colunas desconhecidas como mudança silenciosa do contrato; validar ausências e tipos.
- Saída tabular: `cluster` (int), `perfil` (str); descrições de perfis são gerenciadas em YAML e versionadas com o modelo. O perfil não é garantia de satisfação individual.
- O modelo tem nome no registry, versão e alias `champion`. Promoção requer aprovação humana e validações automatizadas; é proibida promoção automática implícita.
- Serving somente após modelo registrado e alias configurado. Endpoint `/invocations` recebe JSON `dataframe_records` ou `dataframe_split` conforme contrato MLflow.
- Não publicar portas de serving fora do host local por padrão; autenticação/rede e limites exigidos antes de produção.
- Medir métricas de latência p50/p95/p99, vazão, falhas e disponibilidade por componente instrumentado (proxy/exporter), sem atribuir falsamente métricas à aplicação quando não instrumentadas.
- DBSCAN/Agglomerative e HDBSCAN requerem estratégias explícitas para novos dados; neste incremento serving implementa exclusivamente KMeans. Não usar `fit_predict` em produção.

## Critérios de aceitação
1. `python -m app.servico_modelo.treinar_exemplo` registra modelo demonstrativo com dados sintéticos **explicitamente identificados**.
2. `python -m app.servico_modelo.promover_modelo --versao N` define alias após aprovação manual.
3. `docker compose --profile serving up -d serving` expõe servidor MLflow nativo após promoção.
4. `curl -X POST http://localhost:8080/invocations ...` devolve colunas cluster/perfil para linhas válidas.
5. Testes unitários do pyfunc com pipeline previamente ajustado; nenhum import de FastAPI.

## Restrição de escopo
Implementação presente é uma prova de integração treinada com dados sintéticos, **não** substitui o pipeline Steam completo, validação, aprovação e registro do vencedor real.
