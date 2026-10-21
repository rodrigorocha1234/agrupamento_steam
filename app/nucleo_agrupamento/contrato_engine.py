"""Contrato das implementações de agrupamento."""
from typing import Protocol
import pandas as pd
from sklearn.pipeline import Pipeline

class ContratoEngine(Protocol):
    def treinar(self, dados: pd.DataFrame, configuracao: "ConfiguracaoMotor") -> Pipeline: ...

from app.nucleo_agrupamento.configuracao_motor import ConfiguracaoMotor
