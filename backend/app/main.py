import os
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.demo_seed import seed_demo_data
from app.api.routes_escrow import router as escrow_router
from app.api.routes_proof import router as proof_router
from app.api.routes_ledger import router as ledger_router
from app.api.routes_webhooks import router as webhooks_router
from app.api.routes_disputes import router as disputes_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB, Genesis Block, & Seed Data
    seed_demo_data()
    print("[ProofLedger] Database initialized with Genesis block and demo milestones.")
    yield
    print("[ProofLedger] Application shutdown.")

app = FastAPI(
    title="ProofLedger API",
    description="Autonomous AI Escrow & Milestone Verification Platform powered by PayPal",
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory for static deliverable preview
Path(settings.UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_FOLDER), name="uploads")

# Include Routers
app.include_router(escrow_router, prefix=settings.API_V1_PREFIX)
app.include_router(proof_router, prefix=settings.API_V1_PREFIX)
app.include_router(ledger_router, prefix=settings.API_V1_PREFIX)
app.include_router(webhooks_router, prefix=settings.API_V1_PREFIX)
app.include_router(disputes_router, prefix=settings.API_V1_PREFIX)

@app.get("/api/info")
def get_info():
    return {
        "project": "ProofLedger",
        "tagline": "Autonomous AI Escrow & Milestone Verification via PayPal",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "paypal_mode": settings.PAYPAL_MODE,
        "paypal_has_live_credentials": bool(settings.PAYPAL_CLIENT_ID and settings.PAYPAL_CLIENT_SECRET)
    }

@app.get("/api/health")
def health_check():
    has_paypal = bool(settings.PAYPAL_CLIENT_ID and settings.PAYPAL_CLIENT_SECRET)
    return {
        "status": "HEALTHY",
        "service": "ProofLedger Backend",
        "database": "CONNECTED",
        "ai_oracle": "ACTIVE",
        "paypal": has_paypal,
        "aiMock": not bool(settings.GEMINI_API_KEY or settings.OPENAI_API_KEY),
        "version": settings.VERSION
    }

@app.get("/api/samples")
def get_sample_deliverables():
    """Returns pre-loaded sample images so judges can instantly test verification without finding local files."""
    return [
        {
            "id": "sample-pass",
            "name": "HVAC Dual-Run Capacitor & Gauge (Compliant)",
            "filename": "sample_hvac_pass.jpg",
            "url": "/uploads/sample_hvac_pass.jpg",
            "expected_outcome": "PASS (96% Confidence)",
            "description": "High resolution image showing verified capacitor unit and manifold gauge calibrated at 68.4 PSI."
        },
        {
            "id": "sample-fail",
            "name": "Deficient Wiring & Missing Gauge (Violation)",
            "filename": "sample_hvac_fail.jpg",
            "url": "/uploads/sample_hvac_fail.jpg",
            "expected_outcome": "FAIL (Autonomous Void Triggered)",
            "description": "Non-compliant work with missing manifold gauge and exposed copper wiring."
        }
    ]

# Mount Frontend static build if available at the very end
FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    from fastapi.responses import FileResponse
    @app.get("/escrow/approved")
    @app.get("/escrow/cancelled")
    def serve_escrow_redirect():
        index_path = FRONTEND_DIST / "index.html"
        return FileResponse(str(index_path))

    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="frontend")
else:
    @app.get("/")
    def root():
        return {
            "project": "ProofLedger",
            "tagline": "Autonomous AI Escrow & Milestone Verification via PayPal",
            "version": settings.VERSION,
            "docs_url": "/docs",
            "paypal_mode": settings.PAYPAL_MODE,
            "paypal_has_live_credentials": bool(settings.PAYPAL_CLIENT_ID and settings.PAYPAL_CLIENT_SECRET)
        }
