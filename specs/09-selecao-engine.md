# SPEC 09 — Seleção de engine de clustering

## Objetivo
A mesma solução Steam deverá aceitar `motor_agrupamento.engine: sklearn` ou `pycaret` no YAML, sem mudar o código da API, da coleta ou da persistência. Cada implantação Steam terá somente uma configuração de engine ativa por execução.

## Contratos
- Strategy para engine, Factory para resolução por nome.
- `sklearn`: adaptador inicial de KMeans que conserva preprocessamento já existente.
- `pycaret`: usar **PyCaret 4**, API OOP nativa (`ClusteringExperiment(...).fit(...).create_model(...)`). Nunca confundir com `setup()` global da versão 3.
- Resultado de treinamento: `sklearn.pipeline.Pipeline` treinado, consumível pelo encapsulamento MLflow `pyfunc`.
- Somente publicar no serving modelos que aceitam predição em novas observações; DBSCAN/Agglomerative exigem política explícita.
- A engine deve ser registrada como parâmetro/tag no MLflow e monitorada no Grafana, sem criar cardinalidade excessiva.
- Não inferir residência brasileira pela língua da avaliação.

## Critérios de aceite
1. Alterar somente `engine: sklearn` para `engine: pycaret` troca o adaptador usado, desde que extra instalado.
2. Ausência de PyCaret apresenta erro explícito; não executa sklearn silenciosamente.
3. Configuração inválida recebe erro explícito.
4. Teste automatizado demonstra o dispatch da fábrica, treinamento sklearn e caminho PyCaret com mock de dependência.
5. Contratos FastAPI Steam continuam invariáveis.

## Limitação
PyCaret 4 teve versões pré-lançamento em 2026. Executar prova de instalação e treino em container antes de produção; fixar versão efetivamente validada em lockfile. O MVP PyCaret inicial cobre KMeans e delega criação do modelo à API nativa. Tuning/avaliação comparativa completo e end-to-end MLflow exigem integração adicional.
