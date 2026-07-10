#!/bin/bash
# Stop all Atlas services

echo "🛑 Stopping Atlas..."
echo ""

# Stop backend
if [ -f .backend.pid ]; then
    BACKEND_PID=$(cat .backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "[1/3] Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        rm .backend.pid
        echo "✅ Backend stopped"
    else
        echo "⚠️  Backend not running"
        rm .backend.pid
    fi
else
    echo "[1/3] Backend PID not found (may not be running)"
fi

# Stop frontend
echo ""
if [ -f .frontend.pid ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "[2/3] Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        rm .frontend.pid
        echo "✅ Frontend stopped"
    else
        echo "⚠️  Frontend not running"
        rm .frontend.pid
    fi
else
    echo "[2/3] Frontend PID not found (may not be running)"
fi

# Stop Docker services
echo ""
echo "[3/3] Stopping infrastructure..."
cd infra
docker compose down
cd ..
echo "✅ Infrastructure stopped"

echo ""
echo "========================================"
echo "✅ Atlas stopped"
echo "========================================"
echo ""
echo "To start again: ./start_all.sh"
echo ""
