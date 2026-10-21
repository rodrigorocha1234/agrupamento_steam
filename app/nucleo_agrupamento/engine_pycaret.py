"""Engine PyCaret 4: usa a API OOP nativa, sem chamar funções legadas 3.x."""
from typing import final
import pandas as pd
from sklearn.pipeline import Pipeline
from app.nucleo_agrupamento.configuracao_motor import ConfiguracaoMotor

@final
class EnginePycaret:
    def treinar(self, dados: pd.DataFrame, configuracao: ConfiguracaoMotor) -> Pipeline:
        try:
            from pycaret.clustering import ClusteringExperiment
        except ImportError as erro:
            raise RuntimeError(
                'PyCaret não instalado. Instale o extra: pip install -e ".[pycaret]".'
            ) from erro
        colunas = list(configuracao.colunas_numericas + configuracao.colunas_categoricas)
        ausentes = sorted(set(colunas).difference(dados.columns))
        if ausentes:
            raise ValueError(f'Colunas ausentes: {ausentes}')
        experimento = ClusteringExperiment(session_id=configuracao.semente).fit(dados.loc[:, colunas])
        parametros = dict(configuracao.parametros_modelo)
        if configuracao.algoritmo == 'kmeans':
            parametros['n_clusters'] = configuracao.quantidade_clusters
        resultado = experimento.create_model(configuracao.algoritmo, **parametros)
        return resultado.pipeline
