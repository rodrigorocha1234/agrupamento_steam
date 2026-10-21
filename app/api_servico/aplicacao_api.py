"""API dedicada à Steam, usando um motor de inferência reutilizável."""
from time import perf_counter
from fastapi import FastAPI, HTTPException
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.responses import Response
from app.api_servico.contratos_api import EntradaAgrupamento, LoteAgrupamento, SaidaAgrupamento
from app.api_servico.registro_modelos import RegistroModelos
from app.api_servico.gerenciador_inferencia import GerenciadorInferencia

REQUISICOES = Counter("clustering_api_requests_total", "Requisições de inferência", ["status"])
DURACAO = Histogram("clustering_api_request_duration_seconds", "Latência de inferência")
FALHAS = Counter("clustering_api_inference_errors_total", "Falhas de inferência")

def criar_aplicacao(registro: RegistroModelos, gerenciador: GerenciadorInferencia | None = None) -> FastAPI:
    api = FastAPI(title="Steam Reviews Clustering API", version="1.1.0")
    motor = gerenciador if gerenciador is not None else GerenciadorInferencia()

    def executar(registros: list[EntradaAgrupamento]) -> list[SaidaAgrupamento]:
        projeto = registro.obter()
        if len(registros) > registro.tamanho_maximo_lote:
            raise HTTPException(status_code=413, detail="Lote excede limite configurado")
        esperadas = set(projeto.colunas)
        if any(set(item.atributos) != esperadas for item in registros):
            raise HTTPException(status_code=422, detail="Atributos não correspondem ao contrato do modelo")
        inicio = perf_counter()
        try:
            versao, clusters = motor.predizer(projeto, [item.atributos for item in registros])
            REQUISICOES.labels("sucesso").inc()
            return [SaidaAgrupamento(projeto=projeto.nome, modelo=projeto.modelo_mlflow, versao=versao, cluster=cluster, perfil=projeto.perfis.get(cluster)) for cluster in clusters]
        except Exception as erro:
            FALHAS.inc()
            REQUISICOES.labels("erro").inc()
            raise HTTPException(status_code=503, detail="Modelo indisponível ou falha na inferência") from erro
        finally:
            DURACAO.observe(perf_counter() - inicio)

    @api.get("/health")
    def saude() -> dict[str, str]:
        return {"status": "ativo"}

    @api.get("/ready")
    def prontidao() -> dict[str, str]:
        try:
            versao, _ = motor.carregar(registro.obter())
        except Exception as erro:
            raise HTTPException(status_code=503, detail="Modelo ainda não está disponível") from erro
        return {"status": "pronto", "versao": versao}

    @api.get("/metrics", include_in_schema=False)
    def metricas() -> Response:
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    @api.get("/api/v1/model")
    def metadados() -> dict[str, object]:
        dados = registro.obter()
        return {"modelo": dados.modelo_mlflow, "alias": dados.alias, "colunas": list(dados.colunas)}

    @api.get("/api/v1/clusters")
    def clusters() -> dict[str, object]:
        return {"clusters": [{"cluster_id": indice, "perfil": nome} for indice, nome in sorted(registro.obter().perfis.items())]}

    @api.get("/api/v1/clusters/{cluster_id}")
    def consultar_cluster(cluster_id: int) -> dict[str, object]:
        perfil = registro.obter().perfis.get(cluster_id)
        if perfil is None:
            raise HTTPException(status_code=404, detail="Cluster sem perfil publicado")
        return {"cluster_id": cluster_id, "perfil": perfil}

    @api.post("/api/v1/predict", response_model=SaidaAgrupamento)
    def predicao(entrada: EntradaAgrupamento) -> SaidaAgrupamento:
        return executar([entrada])[0]

    @api.post("/api/v1/predict-batch", response_model=list[SaidaAgrupamento])
    def lote(entrada: LoteAgrupamento) -> list[SaidaAgrupamento]:
        return executar(entrada.registros)

    return api
