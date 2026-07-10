#!/bin/bash
# Restart just the backend

echo "🔄 Restarting backend..."
echo ""

# Stop backend
if [ -f .backend.pid ]; then
    BACKEND_PID=$(cat .backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        rm .backend.pid
        sleep 2
    fi
fi

# Start backend
echo "Starting backend..."
source venv/bin/activate
cd apps/api
python main.py > ../../backend.log 2>&1 &
BACKEND_PID=$!
echo "$BACKEND_PID" > ../../.backend.pid
cd ../..

echo ""
echo "✅ Backend restarted (PID: $BACKEND_PID)"
echo "📝 Logs: tail -f backend.log"
echo "🌐 Test: curl http://localhost:8000/health"
echo ""
