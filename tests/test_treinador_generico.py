import pandas as pd
from app.nucleo_agrupamento.treinador_generico import ConfiguracaoAgrupamento, TreinadorGenerico


def test_treinamento_generico() -> None:
    dados = pd.DataFrame({"valor": [1., 2., 3., 100., 110., 120.], "grupo": ["a", "a", "b", "b", "a", "b"]})
    cfg = ConfiguracaoAgrupamento(("valor",), ("grupo",), 2, 42)
    modelo = TreinadorGenerico().treinar(dados, cfg)
    assert len(modelo.predict(dados)) == len(dados)
