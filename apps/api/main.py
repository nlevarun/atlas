"""Atlas FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import research, websocket
import uvicorn

app = FastAPI(
    title="Atlas API",
    version="0.1.0",
    description="AI Operating System for Company Intelligence"
)

# CORS for Next.js dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(research.router, prefix="/api/research", tags=["research"])
app.include_router(websocket.router, tags=["websocket"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Atlas API",
        "version": "0.1.0",
        "status": "operational"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
