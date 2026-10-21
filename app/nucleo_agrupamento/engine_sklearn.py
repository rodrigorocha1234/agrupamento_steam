"""Adapter da implementação existente do scikit-learn."""
import pandas as pd
from sklearn.pipeline import Pipeline
from typing import final
from app.nucleo_agrupamento.configuracao_motor import ConfiguracaoMotor
from app.nucleo_agrupamento.treinador_generico import ConfiguracaoAgrupamento, TreinadorGenerico

@final
class EngineSklearn:
    def treinar(self, dados: pd.DataFrame, configuracao: ConfiguracaoMotor) -> Pipeline:
        if configuracao.algoritmo != 'kmeans':
            raise ValueError('O adaptador sklearn inicial implementa somente kmeans; outros modelos exigem extensão.')
        cfg = ConfiguracaoAgrupamento(
            colunas_numericas=configuracao.colunas_numericas,
            colunas_categoricas=configuracao.colunas_categoricas,
            quantidade_clusters=configuracao.quantidade_clusters,
            semente=configuracao.semente,
        )
        return TreinadorGenerico().treinar(dados, cfg)
