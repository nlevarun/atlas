#!/bin/bash
# Check Atlas service status

echo "========================================"
echo "Atlas Status"
echo "========================================"
echo ""

# Check Docker services
echo "[1/4] Docker Services:"
cd infra
docker compose ps
cd ..
echo ""

# Check backend
echo "[2/4] Backend API:"
if [ -f .backend.pid ]; then
    BACKEND_PID=$(cat .backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "✅ Running (PID: $BACKEND_PID)"
        # Test health endpoint
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            echo "✅ Health check passed"
        else
            echo "⚠️  Health check failed"
        fi
    else
        echo "❌ Not running"
    fi
else
    echo "❌ Not running (no PID file)"
fi
echo ""

# Check frontend
echo "[3/4] Frontend:"
if [ -f .frontend.pid ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "✅ Running (PID: $FRONTEND_PID)"
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            echo "✅ Responding on port 3000"
        else
            echo "⚠️  Not responding yet (may be starting)"
        fi
    else
        echo "❌ Not running"
    fi
else
    echo "❌ Not running (no PID file)"
fi
echo ""

# Check ports
echo "[4/4] Port Status:"
lsof -ti:8000 > /dev/null 2>&1 && echo "✅ Port 8000 (backend) in use" || echo "❌ Port 8000 (backend) free"
lsof -ti:3000 > /dev/null 2>&1 && echo "✅ Port 3000 (frontend) in use" || echo "❌ Port 3000 (frontend) free"
lsof -ti:5432 > /dev/null 2>&1 && echo "✅ Port 5432 (postgres) in use" || echo "❌ Port 5432 (postgres) free"
lsof -ti:6379 > /dev/null 2>&1 && echo "✅ Port 6379 (redis) in use" || echo "❌ Port 6379 (redis) free"

echo ""
echo "========================================"
echo ""
echo "If all services are running:"
echo "🌐 Open: http://localhost:3000"
echo ""
