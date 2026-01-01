"""
SEO Sentinel - FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import config

app = FastAPI(
    title="SEO Sentinel API",
    description="B2B SaaS for Website Health Monitoring",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.API['cors_origins'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "SEO Sentinel API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Import routers (uncomment as you build them)
# from app.api import auth, scans, websites, reports
# app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
# app.include_router(scans.router, prefix="/api/scans", tags=["scans"])
# app.include_router(websites.router, prefix="/api/websites", tags=["websites"])
# app.include_router(reports.router, prefix="/api/reports", tags=["reports"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)