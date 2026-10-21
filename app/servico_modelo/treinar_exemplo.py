"""Exemplo explícito com dados SINTÉTICOS para testar o fluxo de Registry."""
from __future__ import annotations

import os
import yaml
import pandas as pd
import mlflow
from mlflow.models import infer_signature
from app.nucleo_agrupamento.treinador_generico import ConfiguracaoAgrupamento, TreinadorGenerico
from app.servico_modelo.modelo_agrupamento import ModeloAgrupamento


def main() -> None:
    with open("configuracoes/serving_modelo.yaml", encoding="utf-8") as arquivo:
        cfg = yaml.safe_load(arquivo)
    colunas_numericas = tuple(cfg["atributos"]["numericos"])
    colunas_categoricas = tuple(cfg["atributos"]["categoricos"])
    dados = pd.DataFrame({
        "horas_jogadas": [2., 4., 7., 12., 35., 80., 120., 200., 460., 700., 1100., 1800.],
        "votos_uteis": [0., 0., 1., 0., 2., 4., 8., 15., 19., 38., 45., 70.],
        "recebido_gratis": ["nao", "sim", "nao", "nao", "sim", "nao", "sim", "nao", "nao", "sim", "nao", "nao"],
    })
    configuracao = ConfiguracaoAgrupamento(
        colunas_numericas=colunas_numericas,
        colunas_categoricas=colunas_categoricas,
        quantidade_clusters=int(cfg["modelo"]["quantidade_clusters"]),
        semente=int(cfg["modelo"]["semente"]),
    )
    modelo = TreinadorGenerico().treinar(dados, configuracao)
    colunas = colunas_numericas + colunas_categoricas
    python_model = ModeloAgrupamento(modelo, {}, colunas)
    amostra = dados.loc[:, list(colunas)].head(2)
    assinatura = infer_signature(amostra, python_model.predict(None, amostra))
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://localhost:5000"))
    mlflow.set_experiment(str(cfg["mlflow"]["experimento_demo"]))
    with mlflow.start_run(run_name="DEMONSTRACAO_DADOS_SINTETICOS"):
        mlflow.log_param("fonte", "DADOS_SINTETICOS_NAO_PRODUCAO")
        mlflow.log_param("algoritmo", "KMeans")
        info = mlflow.pyfunc.log_model(
            name="modelo_agrupamento",
            python_model=python_model,
            signature=assinatura,
            input_example=amostra,
            registered_model_name=str(cfg["mlflow"]["nome_modelo"]),
            pip_requirements=["mlflow==3.4.0", "pandas>=2.2", "scikit-learn>=1.5"],
        )
    print(f"Modelo de DEMONSTRAÇÃO registrado: {info.model_uri}")
    print("A promoção para @champion é MANUAL e requer aprovação.")


if __name__ == "__main__":
    main()
