"""Carregamento sob demanda de modelos versionados MLflow."""
from threading import RLock
import mlflow.pyfunc
import numpy as np
import pandas as pd
from app.api_servico.registro_modelos import ProjetoModelo

class GerenciadorInferencia:
    def __init__(self) -> None:
        self._cache: dict[str, tuple[str, mlflow.pyfunc.PyFuncModel]] = {}
        self._bloqueio = RLock()

    def carregar(self, projeto: ProjetoModelo) -> tuple[str, mlflow.pyfunc.PyFuncModel]:
        from mlflow import MlflowClient
        with self._bloqueio:
            # Versionamento explícito; troca do alias só entra após reinicialização/reload deliberado.
            if projeto.nome in self._cache:
                return self._cache[projeto.nome]
            versao = str(MlflowClient().get_model_version_by_alias(projeto.modelo_mlflow, projeto.alias).version)
            modelo = mlflow.pyfunc.load_model(f"models:/{projeto.modelo_mlflow}/{versao}")
            self._cache[projeto.nome] = (versao, modelo)
            return versao, modelo

    def predizer(self, projeto: ProjetoModelo, linhas: list[dict[str, int | float | bool | str | None]]) -> tuple[str,list[int]]:
        versao, modelo = self.carregar(projeto)
        quadro = pd.DataFrame(linhas, columns=list(projeto.colunas))
        saida = np.asarray(modelo.predict(quadro)).reshape(-1)
        if len(saida) != len(linhas):
            raise ValueError("Modelo retornou número inválido de predições")
        return versao, [int(indice) for indice in saida]
