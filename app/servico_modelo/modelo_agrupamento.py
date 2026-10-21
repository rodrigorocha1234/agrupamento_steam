"""Modelo MLflow pyfunc; depende de MLflow instalado no ambiente de serving."""
from __future__ import annotations

import pandas as pd
import mlflow.pyfunc
from sklearn.pipeline import Pipeline


class ModeloAgrupamento(mlflow.pyfunc.PythonModel):
    """Prediz somente com um pipeline pré-ajustado; não reexecuta clustering."""

    def __init__(self, modelo: Pipeline, perfis: dict[int, str], colunas: tuple[str, ...]) -> None:
        super().__init__()
        self._modelo = modelo
        self._perfis = perfis
        self._colunas = colunas

    def predict(self, context: mlflow.pyfunc.PythonModelContext, model_input: pd.DataFrame, params: dict[str, object] | None = None) -> pd.DataFrame:
        ausentes = set(self._colunas).difference(model_input.columns)
        if ausentes:
            raise ValueError(f"Atributos obrigatórios ausentes: {sorted(ausentes)}")
        grupos = self._modelo.predict(model_input.loc[:, list(self._colunas)])
        saida = pd.DataFrame({"cluster": grupos.astype(int)})
        saida["perfil"] = saida["cluster"].map(self._perfis).fillna("Perfil não definido")
        return saida
