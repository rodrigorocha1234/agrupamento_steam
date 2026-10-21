# Steam Reviews Clustering — instruções principais

Projeto Python 3.12+ de clustering **sem PLN** para reviews Steam em português brasileiro; idioma `brazilian` não prova residência no Brasil. Siga as specs e regras versionadas em `.agents/specs/` e `.agents/rules/`.

## Governança
- Antes de qualquer alteração, ler `README.md`, `.agents/specs/00-visao-geral.md`, specs da área e rules relevantes, além dos documentos de referência em `docs/fontes/`.
- Preservar integralmente requisitos, registrar discrepâncias e solicitar aprovação da especificação antes de alterar infraestrutura, API pública, persistência ou publicar modelos.
- A equipe é descrita em `.agents/agents/`; delegar tarefas especializadas aos subagentes disponíveis na superfície usada, sem pressupor que todos os IDEs permitem `invoke_subagent`.
- Nunca iniciar Docker Compose alternativo: identificar `compose.yaml`/`docker-compose.yml` existente e reutilizar rede, serviços e volumes; sem arquivo acessível, bloquear alterações de infraestrutura e solicitar sua inspeção no workspace.
- Não armazenar resultados analíticos ou modelos de modo persistente local: Data Lake MinIO e artefatos MLflow. Arquivos de trabalho e specs são versionados no repositório.
- Nunca afirmar que métrica, endpoint, execução, validação ou dashboard funciona sem teste/evidência.

## Sequência sugerida
@pm → aprovação humana → @arquiteto_ml + @engenheiro_dados → @engenheiro_ml + @engenheiro_api + @observabilidade → @qa → aprovação de publicação → @devops.
Os nomes @ são **papéis descritivos**, não comandos nativos garantidos. Para executar, solicitar delegação ao subagente identificado ou usar skills (`/planejar-steam`, `/implementar-steam`, `/auditar-steam`).
