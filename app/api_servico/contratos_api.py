"""Contratos validados da API de agrupamento."""
from pydantic import BaseModel, ConfigDict, Field

class EntradaAgrupamento(BaseModel):
    model_config = ConfigDict(extra="forbid")
    atributos: dict[str, int | float | bool | str | None] = Field(min_length=1)

class LoteAgrupamento(BaseModel):
    model_config = ConfigDict(extra="forbid")
    registros: list[EntradaAgrupamento] = Field(min_length=1)

class SaidaAgrupamento(BaseModel):
    projeto: str
    modelo: str
    versao: str
    cluster: int
    perfil: str | None = None
    status: str = "SUCESSO"
