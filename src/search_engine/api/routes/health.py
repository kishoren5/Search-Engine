from fastapi import APIRouter

from search_engine.api.dependencies import get_global_index
from search_engine.api.schemas import HealthStatus

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live", response_model=HealthStatus)
def liveness() -> HealthStatus:
    return HealthStatus(status="alive", version="0.1.0")


@router.get("/ready", response_model=HealthStatus)
def readiness() -> HealthStatus:
    index = get_global_index()
    if index is None or index.corpus_size == 0:
        return HealthStatus(
            status="not_ready",
            version="0.1.0",
            corpus_size=0,
            reason="No index loaded or index empty",
        )
    return HealthStatus(
        status="ready",
        version="0.1.0",
        corpus_size=index.corpus_size,
    )
