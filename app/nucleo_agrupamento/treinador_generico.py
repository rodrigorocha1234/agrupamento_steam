"""Estratégia inicial genérica para agrupamento de dados tabulares."""
from dataclasses import dataclass

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler


@dataclass(frozen=True, slots=True)
class ConfiguracaoAgrupamento:
    colunas_numericas: tuple[str, ...]
    colunas_categoricas: tuple[str, ...]
    quantidade_clusters: int
    semente: int


class TreinadorGenerico:
    """Instancia modelo sem dependência de API, domínio ou fonte."""

    def criar_pipeline(self, configuracao: ConfiguracaoAgrupamento) -> Pipeline:
        numerico = Pipeline(steps=[
            ("imputador", SimpleImputer(strategy="median")),
            ("escalonador", RobustScaler()),
        ])
        categorico = Pipeline(steps=[
            ("imputador", SimpleImputer(strategy="most_frequent")),
            ("codificador", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ])
        transformador = ColumnTransformer(transformers=[
            ("numericas", numerico, list(configuracao.colunas_numericas)),
            ("categoricas", categorico, list(configuracao.colunas_categoricas)),
        ])
        return Pipeline(steps=[
            ("preparador", transformador),
            ("agrupador", KMeans(
                n_clusters=configuracao.quantidade_clusters,
                random_state=configuracao.semente,
                n_init=20,
            )),
        ])

    def treinar(self, dados: pd.DataFrame, configuracao: ConfiguracaoAgrupamento) -> Pipeline:
        esperado = set(configuracao.colunas_numericas + configuracao.colunas_categoricas)
        ausentes = esperado.difference(dados.columns)
        if ausentes:
            raise ValueError(f"Colunas ausentes: {sorted(ausentes)}")
        modelo = self.criar_pipeline(configuracao)
        modelo.fit(dados)
        return modelo
