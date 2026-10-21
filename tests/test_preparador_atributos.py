import pandas as pd
from app.gestao_dados.preparador_atributos import PreparadorAtributos

def test_features_vetorizadas() -> None:
    dataframe = pd.DataFrame({
        "playtime_forever": [120, 0], "playtime_at_review": [60, 5],
        "playtime_last_two_weeks": [30, 0], "votes_up": [2, 3],
        "votes_funny": [1, 1], "comment_count": [4, 0],
    })
    resultado = PreparadorAtributos().transformar(dataframe)
    assert resultado["horas_jogadas"].tolist() == [2.0, 0.0]
    assert resultado["engajamento_review"].tolist() == [7, 4]
    assert resultado["inconsistencia_tempo"].tolist() == [False, True]
