"""Atribui alias após aprovação humana explícita."""
import argparse
import os
import yaml
from mlflow import MlflowClient, set_tracking_uri


def main() -> None:
    parser = argparse.ArgumentParser(description="Promover versão previamente validada")
    parser.add_argument("--versao", type=int, required=True)
    parser.add_argument("--aprovado", action="store_true", help="Confirma revisão humana da versão")
    argumentos = parser.parse_args()
    if not argumentos.aprovado:
        parser.error("Promoção requer --aprovado após revisão humana.")
    with open("configuracoes/serving_modelo.yaml", encoding="utf-8") as arquivo:
        cfg = yaml.safe_load(arquivo)
    set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://localhost:5000"))
    nome = str(cfg["mlflow"]["nome_modelo"])
    MlflowClient().set_registered_model_alias(nome, "champion", argumentos.versao)
    print(f"Alias champion definido: {nome} v{argumentos.versao}")


if __name__ == "__main__":
    main()
