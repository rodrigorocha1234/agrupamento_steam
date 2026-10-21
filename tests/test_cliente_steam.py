import json
from app.coleta_steam.cliente_steam import ClienteSteam

class RespostaFalsa:
    def raise_for_status(self) -> None:
        pass
    def json(self) -> dict[str, object]:
        return {"cursor":"next", "reviews":[{"recommendationid":"12"}]}

class SessaoFalsa:
    def __init__(self) -> None:
        self.params: dict[str, str] = {}
    def get(self, url: str, *, params: dict[str, str], timeout: float) -> RespostaFalsa:
        self.params = params
        return RespostaFalsa()

def test_input_json_e_idioma() -> None:
    sessao = SessaoFalsa()
    cliente = ClienteSteam("https://example.test", sessao)  # type: ignore[arg-type]  # fake de contrato
    consulta = cliente.montar_consulta(427520)
    pagina = cliente.buscar_pagina(consulta)
    payload = json.loads(sessao.params["input_json"])
    assert payload["appid"] == 427520
    assert payload["languages"] == ["brazilian"]
    assert payload["filter"] == 1
    assert pagina["cursor"] == "next"
