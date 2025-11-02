# Run Django (via uvicorn) and Vue frontend at the same time
Start-Process powershell -ArgumentList "cd backend; uv run uvicorn config.asgi:application --reload --host 127.0.0.1 --port 8000"
Start-Process powershell -ArgumentList "cd frontend; npm run dev"
Write-Host "Backend and frontend are now running..."
