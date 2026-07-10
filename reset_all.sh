#!/bin/bash
# Reset all Atlas data (fresh start)

echo "⚠️  WARNING: This will delete all research data!"
echo ""
read -p "Are you sure? (type 'yes' to confirm): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "🔄 Resetting Atlas..."
echo ""

# Stop everything
echo "[1/4] Stopping services..."
./stop_all.sh

# Remove Docker volumes (contains all data)
echo ""
echo "[2/4] Removing Docker volumes..."
cd infra
docker compose down -v
cd ..
echo "✅ Volumes removed"

# Clean logs
echo ""
echo "[3/4] Cleaning logs..."
rm -f backend.log frontend.log
echo "✅ Logs cleaned"

# Restart infrastructure
echo ""
echo "[4/4] Restarting infrastructure..."
cd infra
docker compose up -d
cd ..
echo "✅ Infrastructure restarted"

echo ""
echo "========================================"
echo "✅ Atlas reset complete"
echo "========================================"
echo ""
echo "All data has been deleted. Fresh start!"
echo ""
echo "To start Atlas: ./start_all.sh"
echo ""
