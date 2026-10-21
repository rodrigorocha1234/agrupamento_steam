# Regra de reuso e serving
1. O núcleo não importa módulos de fontes específicas (Steam, YouTube, FIPE, SPTrans).
2. Cada projeto declara esquema e features próprios em YAML e pode ter adaptadores de origem independentes.
3. Deploy de clustering apenas quando há inferência definida; KMeans suporta predict, DBSCAN não.
4. MLflow pyfunc + MLflow Model Registry + MLflow nativo `/invocations`; proibido FastAPI neste projeto.
5. Promoção de alias somente com aprovação humana após testes, validação e auditoria.
6. Dados e métricas sintéticos nunca devem ser reportados como observação real.
