# Especificação: 01-coleta-lake

Coleta inicial/incremental/revisitação; cursor, retry 429, manifesto e execução_id; Bronze, Silver, Gold particionados por appid/data, integridade, versões, idempotência; snapshots e observações por recommendationid.

## Critérios de aceite
- Implementação rastreável às seções correspondentes de `docs/fontes/escopo_steam_v32.md`.
- Testes automatizados, evidência e documentação dos trade-offs.
- Não considerar concluída sem validação funcional.
