from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from search_engine.api.routes.benchmark import router as benchmark_router
from search_engine.api.routes.health import router as health_router
from search_engine.api.routes.ingestion import router as ingestion_router
from search_engine.api.routes.inspector import router as inspector_router
from search_engine.api.routes.search import router as search_router
from search_engine.api.routes.testing import router as testing_router
from search_engine.api.templates import FINTECH_UI_HTML

app = FastAPI(
    title="BFSI Sentinel — Financial Intelligence & Compliance Search Engine",
    version="1.0.0",
    description="""
### 🚀 **[CLICK HERE TO OPEN THE INTERACTIVE FRONTEND UI](/)**

High-performance financial search platform with compressed postings, zero-copy memory-mapped retrieval, live BM25 tuning, interactive testing suites, and structured regulatory filtering.
""",
)

app.include_router(health_router)
app.include_router(search_router)
app.include_router(benchmark_router)
app.include_router(inspector_router)
app.include_router(testing_router)
app.include_router(ingestion_router)


@app.get("/", response_class=HTMLResponse, tags=["ui"])
def root_ui() -> HTMLResponse:
    """Serve the interactive BFSI Sentinel Compliance & Risk Intelligence Terminal UI."""
    return HTMLResponse(content=FINTECH_UI_HTML, status_code=200)
