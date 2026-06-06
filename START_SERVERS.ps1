#!/usr/bin/env powershell
# START ALL SERVERS - QUICK LAUNCHER

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          🚀 UPCHILD - START ALL SERVERS                        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Define paths
$PROJECT_ROOT = "c:\Users\vbara\OneDrive\Desktop\upchild"
$FRONTEND_PATH = "$PROJECT_ROOT\upchild-frontend\upchild-frontend"
$PYTHON_EXE = "$PROJECT_ROOT\venv\Scripts\python.exe"
$NPM_PATH = "npm"

Write-Host "📁 Project Root: $PROJECT_ROOT" -ForegroundColor Yellow
Write-Host ""

# Check if paths exist
if (!(Test-Path $PYTHON_EXE)) {
    Write-Host "❌ Python not found at $PYTHON_EXE" -ForegroundColor Red
    exit 1
}

if (!(Test-Path $FRONTEND_PATH)) {
    Write-Host "❌ Frontend not found at $FRONTEND_PATH" -ForegroundColor Red
    exit 1
}

Write-Host "✅ All paths verified" -ForegroundColor Green
Write-Host ""

# Start Flask Backend
Write-Host "🐍 Starting Flask Backend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd $PROJECT_ROOT; & '$PYTHON_EXE' flask_app.py"
Write-Host "   ✅ Flask will start in new window (port 5000)" -ForegroundColor Green
Start-Sleep -Seconds 2

# Start React Frontend
Write-Host ""
Write-Host "⚛️  Starting React Frontend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd $FRONTEND_PATH; npm start"
Write-Host "   ✅ React will start in new window (port 3000)" -ForegroundColor Green
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                     🎉 SERVERS STARTING                        ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "📌 WHAT TO DO NEXT:" -ForegroundColor Yellow
Write-Host "   1. Wait 15-20 seconds for servers to start" -ForegroundColor White
Write-Host "   2. Open browser: http://localhost:3000" -ForegroundColor White
Write-Host "   3. Login with: parent@example.com" -ForegroundColor White
Write-Host "   4. Select child 'Alex'" -ForegroundColor White
Write-Host "   5. Go to 'Behavior' tab" -ForegroundColor White
Write-Host "   6. Fill form and click 'Submit Behavior Log'" -ForegroundColor White
Write-Host ""

Write-Host "⚠️  KEEP THIS WINDOW OPEN - It monitors the servers" -ForegroundColor Yellow
Write-Host ""

# Keep monitoring
while ($true) {
    Start-Sleep -Seconds 5
}
