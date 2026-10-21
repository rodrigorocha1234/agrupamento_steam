"""Modelo único por ambiente; motor pode ser reutilizado em outros deployments."""
from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass(frozen=True, slots=True)
class ProjetoModelo:
    nome: str
    modelo_mlflow: str
    alias: str
    colunas: tuple[str, ...]
    perfis: dict[int, str]

class RegistroModelos:
    def __init__(self, caminho: str | Path) -> None:
        with Path(caminho).open(encoding="utf-8") as arquivo:
            conteudo: object = yaml.safe_load(arquivo)
        if not isinstance(conteudo, dict):
            raise ValueError("Configuração YAML inválida")
        api = conteudo.get("api")
        if not isinstance(api, dict):
            raise ValueError("Seção api ausente")
        dados = api.get("modelo")
        if not isinstance(dados, dict):
            raise ValueError("Seção api.modelo ausente: esta instância requer um único modelo")
        colunas = dados.get("colunas")
        if not isinstance(colunas, list) or not colunas or not all(isinstance(c, str) for c in colunas):
            raise ValueError("Colunas inválidas para o modelo")
        if len(set(colunas)) != len(colunas):
            raise ValueError("Colunas duplicadas")
        perfis_brutos = dados.get("perfis", {})
        if not isinstance(perfis_brutos, dict):
            raise ValueError("Perfis inválidos")
        perfis = {int(chave): str(valor) for chave, valor in perfis_brutos.items()}
        self._modelo = ProjetoModelo(
            nome=str(dados.get("nome", "steam_reviews")),
            modelo_mlflow=str(dados["modelo_mlflow"]),
            alias=str(dados["alias"]),
            colunas=tuple(colunas),
            perfis=perfis,
        )
        inferencia = api.get("inferencia", {})
        if not isinstance(inferencia, dict):
            raise ValueError("Seção api.inferencia inválida")
        self.tamanho_maximo_lote = int(inferencia.get("tamanho_maximo_lote", 1000))
        if self.tamanho_maximo_lote < 1:
            raise ValueError("Limite de lote precisa ser positivo")

    def obter(self) -> ProjetoModelo:
        return self._modelo
