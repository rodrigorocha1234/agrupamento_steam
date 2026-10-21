# Contrato principal — Steam Reviews Brasil

Atue como equipe multidisciplinar descrita em `.agents/agents.md`; respeite `specs/`, `.agents/rules/` e as regras originais em `docs/regras-python-originais.txt`.

**Ordem obrigatória:** Product Manager → Arquitetura → Engenharia de Dados → Engenharia de ML → Validação/QA → Observabilidade/DevOps → revisão humana. Cada etapa produz artefatos revisáveis em `production_artifacts/` e não avança em decisões estruturais sem aprovação explícita do usuário.

Objetivo: comparar perfis de reviews em idioma `brazilian` da Steam, para múltiplos `appid`, **sem PLN**. Unidade = review, não jogador único. Estudos: por jogo, conjunto e comparação por jogo. Nunca reportar simulações como dados reais.

Requisitos: Python 3.12+, estrita tipagem sem `Any`, nomes próprios em português, pacotes/módulos próprios duas palavras separadas por `_` (exceto nomes impostos), uma classe principal por arquivo, Pandas vetorizado, YAML para configurações mutáveis, SOLID e padrões somente quando agregarem valor, testes e observabilidade completa Grafana.

Para fluxos novos use Agent Skills com `SKILL.md`; workflows legados estão descontinuados. Antes de escrever código, propor plano, critérios de aceitação e riscos. Não apagar arquivos existentes ou publicar serviços externos sem aprovação. O protótipo em `app/` é apenas ponto de partida.

**Ampliação obrigatória:** SPEC 06 (MLflow serving nativo, sem FastAPI), SPEC 07 (motor genérico desacoplado de Steam) e Rule 07. Skill `/serving` para registro/promoção/inferência.

**Etapa API:** API Engineer implementa `specs/08-fastapi.md` com gate QA antes da exposição externa. FastAPI é o serviço HTTP padrão; o MLflow Serving nativo fica disponível como alternativa em `profiles: [serving]`.


Antes de modificar algoritmos, ler `specs/09-selecao-engine.md` e `.agents/rules/09-engines.md`. Usar skill `engines`.
