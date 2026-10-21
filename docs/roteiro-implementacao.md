# Plano incremental para os agentes

1. PM valida o escopo, acesso à API e política de retenção. Gate 1.
2. Arquitetura define interfaces e contratos YAML com UML, esqueleto tipado e ADRs. Gate 2.
3. Eng. dados faz adapter Steam `input_json`, paginação e Bronze/Silver/Gold MinIO + Quality Gates. Gate 3.
4. Eng. ML faz estudos A/B/C, preprocessing e tuning, registra em MLflow; QA mede estabilidade. Gate 4.
5. DevOps/Observabilidade completa Compose, dashboards Grafana reais, Loki/Alloy e alertas. Gate 5.
6. QA valida integrações, privacidade, dados simulados vs reais, testes e release documental. Gate final.

**Aceite parcial:** esqueleto incluído NÃO significa que coleta real, tracking, dashboards ou pipeline estão executando. Agentes devem implementá-los, verificar com evidências e não inventar resultados.
