"""Atlas FastAPI application."""

import sys
import os

# Make Atlas's internal packages (orchestrator, agents, synthesis, schemas)
# importable. Several files in this project try to add the wrong folder to
# sys.path; adding the shared "packages" parent directory here, before
# anything else is imported, fixes all of those imports at once.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'packages'))

# Load the .env file. python-dotenv was listed as a dependency but never
# actually invoked anywhere in the project, so keys in .env (Tavily, Groq,
# GitHub, etc.) were never reaching the agents. Point explicitly at the
# project-root .env, since this file runs with apps/api as the working
# directory, not the project root.
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

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
