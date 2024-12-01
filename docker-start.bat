@echo off

REM Build and start the containers
docker-compose up --build -d

REM Wait for services to be ready
echo Waiting for services to be ready...
timeout /t 10 /nobreak

REM Check if services are running
echo Checking service status...
docker-compose ps

echo.
echo Services should now be available at:
echo - API: http://localhost:8000
echo - Dashboard: http://localhost:8000/static/dashboard.html
echo - Prometheus: http://localhost:9091
echo.
echo To view logs: docker-compose logs -f
echo To stop: docker-compose down
