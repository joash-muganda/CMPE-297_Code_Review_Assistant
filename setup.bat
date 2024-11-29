@echo off
echo Setting up Code Review Assistant...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo Creating necessary directories...
if not exist logs mkdir logs

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    if exist .env.example (
        copy .env.example .env
    ) else (
        echo Warning: .env.example not found. Please configure .env manually.
    )
)

REM Initialize database
echo Initializing database...
python -c "from src.model_manager import ModelManager; ModelManager()"

echo Setup complete! You can now run the application with:
echo python run_server.py

REM Deactivate virtual environment
deactivate

echo.
echo Press any key to exit...
pause >nul
