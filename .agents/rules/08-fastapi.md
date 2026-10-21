# RULE 08 — API FastAPI reutilizável
- Endpoint genérico; evitar `if projeto == steam` e duplicações por fonte.
- Contratos Pydantic estritos. Validação explícita de atributos contra configuração YAML.
- `mlflow.pyfunc` a partir de Registry/alias; não embutir treinamento na API.
- Evitar `Any` em código próprio; manter strict, uma classe principal por arquivo e nomes em português.
- Não promover modelo automaticamente sem gate humano de qualidade.
- Não capturar exceções silenciosamente; respostas HTTP não devem conter detalhes internos.
- Métricas p50/p95/p99, volume, erros, duração; nunca usar IDs de review como labels Prometheus.
- Serving MLflow nativo opcional, FastAPI padrão para servir múltiplos projetos.
