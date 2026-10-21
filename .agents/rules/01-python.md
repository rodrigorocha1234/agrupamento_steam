---
trigger: always_on
description: Regras persistentes 01-python.md
---
# 01-python.md

Python 3.12+; sem `Any` nem `typing.Any`; type checker strict; imports explícitos. Nomes próprios em português; uma classe principal por arquivo; módulos e pacotes próprios exatamente duas palavras com `_`, exceções técnicas necessárias. `@override`, `@abstractmethod`, `@final`, `@property` conforme semântica. Exceções próprias, chaining, não suprimir erros. Testes pytest de unidade, contrato, integração e parametrizados. Prioridade: nativo → biblioteca padrão → operações vetorizadas → solução idiomática → abstração própria → implementação manual. Leia integralmente `docs/regras-python-originais.txt`.
