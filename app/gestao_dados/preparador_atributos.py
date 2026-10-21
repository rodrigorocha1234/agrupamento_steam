"""Engenharia de atributos vetorizada de reviews sem PLN."""
from __future__ import annotations
from typing import final
import pandas as pd


@final
class PreparadorAtributos:
    def transformar(self, dados: pd.DataFrame) -> pd.DataFrame:
        total = dados["playtime_forever"].clip(lower=0)
        no_review = dados["playtime_at_review"].clip(lower=0)
        return dados.assign(
            horas_jogadas=total.div(60),
            horas_ate_review=no_review.div(60),
            horas_apos_review=total.sub(no_review).clip(lower=0).div(60),
            inconsistencia_tempo=no_review.gt(total),
            proporcao_atividade_recente=dados["playtime_last_two_weeks"].div(total.clip(lower=1)),
            engajamento_review=dados["votes_up"].add(dados["votes_funny"]).add(dados["comment_count"]),
        )
