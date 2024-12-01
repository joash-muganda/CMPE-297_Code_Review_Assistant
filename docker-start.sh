#!/bin/bash

# Build and start the containers
docker-compose up --build -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Check if services are running
echo "Checking service status..."
docker-compose ps

echo "
Services should now be available at:
- API: http://localhost:8000
- Dashboard: http://localhost:8000/static/dashboard.html
- Prometheus: http://localhost:9091

To view logs: docker-compose logs -f
To stop: docker-compose down
"
