"""Executa engine selecionada em YAML; devolve pipeline pronto para MLflow."""
from pathlib import Path
from typing import Literal, cast
import pandas as pd
import yaml
from sklearn.pipeline import Pipeline
from app.nucleo_agrupamento.configuracao_motor import ConfiguracaoMotor
from app.nucleo_agrupamento.fabrica_engine import FabricaEngine

class ExecutorEngine:
    def carregar_configuracao(self, caminho: Path) -> ConfiguracaoMotor:
        bruto: object = yaml.safe_load(caminho.read_text(encoding='utf-8'))
        if not isinstance(bruto, dict):
            raise ValueError('YAML raiz deve ser um mapa.')
        motor = bruto['motor_agrupamento']
        if not isinstance(motor, dict):
            raise ValueError('motor_agrupamento deve ser um mapa.')
        engine = str(motor['engine'])
        if engine not in ("sklearn", "pycaret"):
            raise ValueError(f"Engine inválida: {engine}")
        configuracao_especifica = motor.get(engine, {})
        if not isinstance(configuracao_especifica, dict):
            raise ValueError('Configuração da engine deve ser um mapa.')
        parametros = configuracao_especifica.get('parametros_modelo', {})
        if not isinstance(parametros, dict):
            raise ValueError('parametros_modelo deve ser um mapa.')
        return ConfiguracaoMotor(
            engine=cast(Literal['sklearn', 'pycaret'], engine),
            algoritmo=str(motor['algoritmo']),
            quantidade_clusters=int(motor['quantidade_clusters']),
            semente=int(motor['semente']),
            colunas_numericas=tuple(str(c) for c in motor['colunas_numericas']),
            colunas_categoricas=tuple(str(c) for c in motor['colunas_categoricas']),
            parametros_modelo={str(k): v for k, v in parametros.items()},
        )

    def treinar(self, dados: pd.DataFrame, caminho_yaml: Path) -> Pipeline:
        configuracao = self.carregar_configuracao(caminho_yaml)
        return FabricaEngine().criar(configuracao.engine).treinar(dados, configuracao)
