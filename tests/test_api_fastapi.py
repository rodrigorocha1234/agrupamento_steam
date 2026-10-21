import pytest
pytest.importorskip("mlflow")
from fastapi.testclient import TestClient
from app.api_servico.registro_modelos import RegistroModelos
from app.api_servico.aplicacao_api import criar_aplicacao

class MotorSimulado:
    def carregar(self, projeto: object) -> tuple[str, object]:
        return "7", object()

    def predizer(self, projeto: object, linhas: list[dict[str, object]]) -> tuple[str, list[int]]:
        return "7", [2] * len(linhas)

def criar_cliente() -> TestClient:
    registro = RegistroModelos("configuracoes/api_servico.yaml")
    return TestClient(criar_aplicacao(registro, MotorSimulado()))  # type: ignore[arg-type]

def test_saude() -> None:
    assert criar_cliente().get("/health").status_code == 200

def test_prontidao() -> None:
    resposta = criar_cliente().get("/ready")
    assert resposta.status_code == 200
    assert resposta.json()["versao"] == "7"

def test_contrato_atributos() -> None:
    resposta = criar_cliente().post("/api/v1/predict", json={"atributos": {"x": 1}})
    assert resposta.status_code == 422

def test_inferencia_simulada() -> None:
    projeto = RegistroModelos("configuracoes/api_servico.yaml").obter()
    campos = {coluna: 1 for coluna in projeto.colunas}
    resposta = criar_cliente().post("/api/v1/predict", json={"atributos": campos})
    assert resposta.status_code == 200
    assert resposta.json()["cluster"] == 2
    assert resposta.json()["versao"] == "7"

def test_lote_simulado() -> None:
    projeto = RegistroModelos("configuracoes/api_servico.yaml").obter()
    campos = {coluna: 1 for coluna in projeto.colunas}
    resposta = criar_cliente().post("/api/v1/predict-batch", json={"registros": [{"atributos": campos}, {"atributos": campos}]})
    assert resposta.status_code == 200
    assert len(resposta.json()) == 2

def test_clusters_nao_publicados() -> None:
    assert criar_cliente().get("/api/v1/clusters").json() == {"clusters": []}
    assert criar_cliente().get("/api/v1/clusters/2").status_code == 404
