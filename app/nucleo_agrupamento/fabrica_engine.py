"""Factory com registro explícito e sem condicionais por domínio."""
from typing import final
from app.nucleo_agrupamento.contrato_engine import ContratoEngine
from app.nucleo_agrupamento.engine_sklearn import EngineSklearn
from app.nucleo_agrupamento.engine_pycaret import EnginePycaret

@final
class FabricaEngine:
    def __init__(self) -> None:
        self._registro: dict[str, type[EngineSklearn] | type[EnginePycaret]] = {
            'sklearn': EngineSklearn,
            'pycaret': EnginePycaret,
        }

    def criar(self, nome: str) -> ContratoEngine:
        try:
            return self._registro[nome]()
        except KeyError as erro:
            raise ValueError(f'Engine não suportada: {nome}') from erro
