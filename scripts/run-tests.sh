#!/bin/bash
# DVSwitch Test Runner Script

set -e

echo "🧪 DVSwitch Test Runner"
echo "========================"

# Check if we're in the right directory
if [[ ! -f "compose/docker-compose.ci.yaml" ]]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Install test dependencies if needed
if [[ ! -d "venv" ]]; then
    echo "📦 Setting up Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements-test.txt
else
    echo "🔧 Activating existing virtual environment..."
    source venv/bin/activate
fi

# Setup environment files
echo "⚙️  Setting up environment files..."
./compose/env/setup-env.sh

# Start services
echo "🚀 Starting DVSwitch services..."
docker compose -f compose/docker-compose.ci.yaml up -d --build

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
timeout=300
elapsed=0
while [ $elapsed -lt $timeout ]; do
    if docker compose -f compose/docker-compose.ci.yaml ps | grep -q "unhealthy\|starting"; then
        echo "⏳ Services still starting... ($elapsed/$timeout seconds)"
        sleep 15
        elapsed=$((elapsed + 15))
    else
        echo "✅ All services are healthy!"
        break
    fi
done

if [ $elapsed -ge $timeout ]; then
    echo "❌ Services did not become healthy in time"
    docker compose -f compose/docker-compose.ci.yaml logs
    docker compose -f compose/docker-compose.ci.yaml down -v
    exit 1
fi

# Run tests
echo "🧪 Running tests..."
mkdir -p test-results

# Run unit tests
echo "📋 Running unit tests..."
pytest tests/unit/ -v --tb=short --html=test-results/unit-report.html --self-contained-html

# Run integration tests
echo "🔗 Running integration tests..."
pytest tests/integration/ -v --tb=short --timeout=300 --html=test-results/integration-report.html --self-contained-html

echo "✅ Tests completed!"
echo "📊 Results saved to test-results/"

# Cleanup
echo "🧹 Cleaning up..."
docker compose -f compose/docker-compose.ci.yaml down -v

echo "🎉 All done!"
