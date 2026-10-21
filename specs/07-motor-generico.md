# SPEC 07 — Motor genérico de clustering reutilizável

## Delimitação
Separar domínio de agrupamento da fonte. `app/nucleo_agrupamento` implementa protocolos, preparação e algoritmos; `app/coleta_steam` é somente um adaptador específico. Novos adapters: YouTube, SPTrans, FIPE, CSV, SQL, REST, sem modificar núcleo.

## YAML-driven
Cada domínio define fonte, schema, seleção de atributos, classificação nominal/ordinal/contínua/discreta, imputação, tratamento de outliers, modelos, espaços de busca, métricas e modo de serving, sem nomes fixos de Steam no núcleo.

## Pipeline
Adapter → Quality Gate → atributos tabulares vetorizados → Transformador (numerico/categorico) → PCA opcional → Estratégia de clustering → otimização/estabilidade → registro MLflow → visualização Grafana → inferência onde suportada.

## Segurança metodológica
- Clustering é não supervisionado; diferenciar labels conhecidos de atributos e não vazar alvos nas features.
- Com múltiplas fontes, não misturar amostras de unidades incompatíveis.
- Algoritmos baseados em densidade podem produzir ruído; avaliar cobertura, estabilidade, validade interna e tamanho mínimo.
- Persistir mapeamento descritivo de clusters por versão; IDs de clusters não permanecem semanticamente estáveis entre treinos.

## Critérios de aceite
Um novo domínio pode fornecer DataFrame tabular, YAML de schema/features e adaptador sem importar `app.coleta_steam` no núcleo; KMeans genérico aceita DataFrame numérico/categórico e retorna identificadores. Inclusão de novos algoritmos por Strategy.
