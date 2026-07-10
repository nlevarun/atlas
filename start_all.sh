#!/bin/bash
# Start all Atlas services

echo "🚀 Starting Atlas..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    echo "Please start Docker Desktop and try again"
    echo ""
    echo "To start Docker:"
    echo "  open -a Docker"
    exit 1
fi

# Start infrastructure
echo "[1/3] Starting infrastructure services..."
cd infra
docker compose up -d
cd ..

# Wait for services to be healthy
echo "    Waiting for services to initialize (30 seconds)..."
sleep 30

# Activate venv and start backend
echo ""
echo "[2/3] Starting backend API..."
source venv/bin/activate
cd apps/api

# Start backend in background
python main.py > ../../backend.log 2>&1 &
BACKEND_PID=$!
echo "    Backend started (PID: $BACKEND_PID)"
echo "    Logs: tail -f backend.log"

cd ../..

# Start frontend
echo ""
echo "[3/3] Starting frontend..."
cd apps/web

# Start frontend in background
npm run dev > ../../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "    Frontend started (PID: $FRONTEND_PID)"
echo "    Logs: tail -f frontend.log"

cd ../..

# Save PIDs for stop script
echo "$BACKEND_PID" > .backend.pid
echo "$FRONTEND_PID" > .frontend.pid

echo ""
echo "========================================"
echo "✅ Atlas is running!"
echo "========================================"
echo ""
echo "🌐 Open: http://localhost:3000"
echo ""
echo "📊 Backend: http://localhost:8000"
echo "📝 Frontend: http://localhost:3000"
echo ""
echo "To stop: ./stop_all.sh"
echo "To check status: ./status.sh"
echo "To view logs: tail -f backend.log frontend.log"
echo ""
echo "Opening Atlas in browser..."
sleep 3
open http://localhost:3000
