from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter
import os

from app.api.endpoints import graph, ml, trips
from app.database import get_session
from app.services.graph_builder import build_graph
from app.services.graph_cache import GraphCache

ml_models = {}

REQUEST_COUNT = Counter(
    "app_request_count",
    "Nombre de requêtes par endpoint et status code",
    ["method", "endpoint", "status_code"]
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    model_path = "app/ml_assets/emission_model.joblib"
    if os.path.exists(model_path):
        print("Modèle ML chargé.")
    else:
        print("Aucun modèle ML trouvé — utilisez POST /api/ml/train pour l'entraîner.")

    session = next(get_session())
    try:
        G = build_graph(session)
        GraphCache.set(G)
    finally:
        session.close()

    yield

    ml_models.clear()
    GraphCache.invalidate()

app = FastAPI(
    title="OB Rail — CO₂ Optimizer",
    lifespan=lifespan,
)

@app.middleware("http")
async def count_requests(request: Request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=str(response.status_code)
    ).inc()
    return response

Instrumentator().instrument(app).expose(app)

app.include_router(trips.router, prefix="/api")
app.include_router(graph.router, prefix="/api")
app.include_router(ml.router, prefix="/api")