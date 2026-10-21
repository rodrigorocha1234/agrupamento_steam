# SPEC 00 — visão geral e critérios

**Problema**: descobrir perfis comportamentais em avaliações Steam classificadas `brazilian`, sem analisar linguagem natural. Unidade de modelagem: review por jogo, um usuário pode aparecer em diversos jogos. **Não é classificação supervisionada**.

**Jogos iniciais**: Factorio 427520; Satisfactory 526870; Dyson Sphere Program 1366540. Qualquer quantidade de appids habilitados via YAML.

**Experimentos**: A experiência (playtime, num_reviews), B engajamento (votes_up, votes_funny, comment_count, weighted_vote_score), C conjunto. Excluir `voted_up` da entrada inicial e usar para interpretar. Comparar modelos por jogo e modelo conjunto (não usar appid como input inicial).

**Critérios**: reproduzível com seed; sem PLN; sem conteúdo textual em features; demonstrar fonte do dado e data de coleta; artefatos MLflow/MinIO; dashboard Grafana; testes e aprovação humana.

**Não prometer** dados reais a partir dos resultados simulados: 30.000 coletadas, 28.500 válidas, cinco clusters e scores citados na conversa foram EXEMPLO FICTÍCIO.
