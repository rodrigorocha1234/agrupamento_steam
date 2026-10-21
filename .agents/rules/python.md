---
trigger: model_decision
description: Regras para a área python no projeto Steam Reviews Clustering.
---
# Regras de python

Código próprio Python 3.12+; tipagem forte explícita, **proibido Any**, checker strict; nomes de classes, métodos, funções e atributos em português; módulos/pacotes importáveis próprios de exatamente duas palavras unidas por `_` (ressalvadas exigências das ferramentas). Uma classe principal por arquivo, SOLID e composição preferencial. `@override` em sobrescritas; `@final`, `@abstractmethod`, `@property` só quando apropriados. Exceções próprias e `raise ... from erro`. Priorizar biblioteca padrão e nativos. Testar com pytest e CI strict.

Fonte normativa adicional: `docs/fontes/regras_python_originais.txt` e `docs/fontes/escopo_steam_v32.md`.
