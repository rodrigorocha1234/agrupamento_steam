# RULE 09 — Engines intercambiáveis
- Configuração `motor_agrupamento.engine` deve decidir a engine, não o nome do projeto.
- Usar Strategy/Factory; não adicionar ramificações Steam/YouTube/FIPE no núcleo.
- Preferir recursos nativos do PyCaret 4 e sklearn; não duplicar pipelines indevidamente.
- Isolar dependência opcional PyCaret para não prejudicar instalação sklearn.
- Nunca salvar artefatos de treinamento em disco de forma permanente; registrar via MLflow/MinIO.
- Modelos de clustering sem `predict` não podem ser publicados como inferência sem adapter aprovado.
- Respeitar Python 3.12+, tipagem forte e testes.
