import pytest
import pandas as pd

mlflow = pytest.importorskip("mlflow")
from app.nucleo_agrupamento.treinador_generico import ConfiguracaoAgrupamento, TreinadorGenerico
from app.servico_modelo.modelo_agrupamento import ModeloAgrupamento


def test_pyfunc_prediz_sem_retreinar() -> None:
    dados = pd.DataFrame({"valor": [1., 2., 100., 110.], "grupo": ["a", "a", "b", "b"]})
    cfg = ConfiguracaoAgrupamento(("valor",), ("grupo",), 2, 42)
    modelo = TreinadorGenerico().treinar(dados, cfg)
    resultado = ModeloAgrupamento(modelo, {}, ("valor", "grupo")).predict(None, dados)
    assert len(resultado) == 4
    assert list(resultado.columns) == ["cluster", "perfil"]
