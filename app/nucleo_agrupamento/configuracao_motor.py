"""Configuração tipada do motor para experimentos reproduzíveis."""
from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True, slots=True)
class ConfiguracaoMotor:
    engine: Literal['sklearn', 'pycaret']
    algoritmo: str
    quantidade_clusters: int
    semente: int
    colunas_numericas: tuple[str, ...]
    colunas_categoricas: tuple[str, ...]
    parametros_modelo: dict[str, int | float | str | bool]
