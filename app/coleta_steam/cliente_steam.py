"""Adaptador demonstrativo da Service API Steam (não registra reviews em disco)."""
from __future__ import annotations
import json
from collections.abc import Iterator, Mapping
from datetime import datetime, timedelta, timezone
from typing import TypeAlias, final

import requests

ValorJson: TypeAlias = "str | int | float | bool | None | list[ValorJson] | dict[str, ValorJson]"


@final
class ClienteSteam:
    def __init__(self, url: str, sessao: requests.Session | None = None) -> None:
        self._url = url
        self._sessao = sessao if sessao is not None else requests.Session()

    def montar_consulta(self, appid: int, dias: int = 365, cursor: str = "*") -> dict[str, ValorJson]:
        agora = datetime.now(timezone.utc)
        inicio = agora - timedelta(days=dias)
        return {
            "appid": appid, "filter": 1, "languages": ["brazilian"],
            "review_type": 0, "purchase_type": 0, "num_per_page": 100,
            "cursor": cursor, "date_range_start": int(inicio.timestamp()),
            "date_range_end": int(agora.timestamp()),
            "filter_offtopic_activity": True,
        }

    def buscar_pagina(self, consulta: Mapping[str, ValorJson], timeout: float = 25.0) -> dict[str, object]:
        resposta = self._sessao.get(
            self._url,
            params={"input_json": json.dumps(dict(consulta), separators=(",", ":"))},
            timeout=timeout,
        )
        resposta.raise_for_status()
        documento: object = resposta.json()
        if not isinstance(documento, dict):
            raise ValueError("Resposta Steam não contém objeto JSON")
        return {str(chave): valor for chave, valor in documento.items()}

    def iterar_paginas(self, appid: int, maximo_paginas: int = 100) -> Iterator[dict[str, object]]:
        """Exemplo mínimo; retries, métricas e validação ficam para o agente de dados."""
        cursor = "*"
        vistos: set[str] = set()
        for _ in range(maximo_paginas):
            if cursor in vistos:
                break
            vistos.add(cursor)
            pagina = self.buscar_pagina(self.montar_consulta(appid, cursor=cursor))
            avaliacoes = pagina.get("reviews", [])
            if not isinstance(avaliacoes, list) or not avaliacoes:
                break
            yield pagina
            proximo = pagina.get("cursor", "")
            if not isinstance(proximo, str) or not proximo:
                break
            cursor = proximo
