@echo off
echo ========================================
echo Twilio Calling Dashboard
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if requirements.txt exists and is newer than last install
if exist "requirements.txt" (
    if not exist ".install_done" (
        echo Installing dependencies...
        pip install -r requirements.txt
        if errorlevel 1 (
            echo ERROR: Failed to install dependencies
            pause
            exit /b 1
        )
        echo. > .install_done
    )
)

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found
    echo Please run setup.py first or copy .env.template to .env
    echo.
    set /p choice="Continue anyway? (y/N): "
    if /i not "%choice%"=="y" (
        echo Exiting...
        pause
        exit /b 1
    )
)

REM Run the application
echo Starting Twilio Calling Dashboard...
echo.
python main.py

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Application exited with an error
    pause
)

REM Deactivate virtual environment
deactivate
