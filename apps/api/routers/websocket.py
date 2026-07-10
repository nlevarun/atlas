"""WebSocket endpoints for live streaming."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import json

router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections for research runs."""

    def __init__(self):
        # Map of run_id -> list of active WebSocket connections
        self.active_connections: Dict[str, list[WebSocket]] = {}

    async def connect(self, run_id: str, websocket: WebSocket):
        """Accept a new WebSocket connection for a run."""
        await websocket.accept()

        if run_id not in self.active_connections:
            self.active_connections[run_id] = []

        self.active_connections[run_id].append(websocket)

        # Send connection confirmation
        await websocket.send_json({
            "type": "connected",
            "run_id": run_id,
            "message": "Connected to Atlas research stream"
        })

    def disconnect(self, run_id: str, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if run_id in self.active_connections:
            self.active_connections[run_id].remove(websocket)

            # Clean up empty lists
            if not self.active_connections[run_id]:
                del self.active_connections[run_id]

    async def broadcast(self, run_id: str, message: dict):
        """Broadcast a message to all connections for a run."""
        if run_id not in self.active_connections:
            return

        # Send to all connected clients
        disconnected = []
        for websocket in self.active_connections[run_id]:
            try:
                await websocket.send_json(message)
            except Exception:
                # Mark for removal if sending fails
                disconnected.append(websocket)

        # Clean up disconnected clients
        for ws in disconnected:
            self.disconnect(run_id, ws)


# Global connection manager
manager = ConnectionManager()


@router.websocket("/ws/research/{run_id}")
async def websocket_endpoint(websocket: WebSocket, run_id: str):
    """
    WebSocket endpoint for real-time research updates.

    Connect to this endpoint to receive live events as agents
    execute and evidence is discovered.

    Events:
    - run_started: Research run initiated
    - agent_started: Individual agent started
    - evidence_found: New evidence discovered
    - agent_completed: Agent finished
    - synthesis_started: Narrative synthesis started
    - run_completed: Research complete
    """
    await manager.connect(run_id, websocket)

    try:
        # Keep connection alive and listen for client messages
        while True:
            # Wait for any client messages (mostly just keep-alive)
            data = await websocket.receive_text()

            # Echo back if client sends ping
            if data == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        manager.disconnect(run_id, websocket)
