"""Testes iniciais da alternância de engines."""
from pathlib import Path
from unittest.mock import MagicMock, patch
import pandas as pd
import pytest
from app.nucleo_agrupamento.executor_engine import ExecutorEngine
from app.nucleo_agrupamento.fabrica_engine import FabricaEngine

def test_fabrica_sklearn() -> None:
    assert type(FabricaEngine().criar('sklearn')).__name__ == 'EngineSklearn'

def test_fabrica_pycaret() -> None:
    assert type(FabricaEngine().criar('pycaret')).__name__ == 'EnginePycaret'

def test_fabrica_rejeita_desconhecida() -> None:
    with pytest.raises(ValueError, match='Engine não suportada'):
        FabricaEngine().criar('outro')

def test_yaml_seleciona_engine() -> None:
    cfg = ExecutorEngine().carregar_configuracao(Path('configuracoes/projeto_base.yaml'))
    assert cfg.engine in ('pycaret', 'sklearn')
