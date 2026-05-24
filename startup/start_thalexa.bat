@echo off
REM Thalexa Windows startup launcher
REM Run this from the startup folder to launch Thalexa in the workspace root.
pushd "%~dp0.."
if exist ".venv\Scripts\python.exe" (
    echo Using virtual environment Python...
    ".venv\Scripts\python.exe" main.py
) else (
    echo Virtual environment not found, using system Python...
    python main.py
)
popd
pause
