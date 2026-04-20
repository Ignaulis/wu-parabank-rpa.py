@echo off
setlocal

cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON_CMD=py -3"
) else (
    set "PYTHON_CMD=python"
)

echo [1/5] Creating virtual environment...
%PYTHON_CMD% -m venv venv
if errorlevel 1 goto :fail

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 goto :fail

echo [3/5] Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 goto :fail

echo [4/5] Installing requirements...
pip install -r requirements.txt
if errorlevel 1 goto :fail

echo [5/5] Installing Playwright browsers...
playwright install
if errorlevel 1 goto :fail

echo.
echo Setup completed successfully.
echo You can now run: run_windows.bat
exit /b 0

:fail
echo.
echo Setup failed. Please check errors above.
pause
exit /b 1
