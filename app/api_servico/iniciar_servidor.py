"""Entrada ASGI para uvicorn."""
import os
from app.api_servico.aplicacao_api import criar_aplicacao
from app.api_servico.registro_modelos import RegistroModelos

app = criar_aplicacao(RegistroModelos(os.getenv("CLUSTERING_API_CONFIG", "configuracoes/api_servico.yaml")))
