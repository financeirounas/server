@echo off
setlocal

echo 🔹 Iniciando ambiente de desenvolvimento (Windows)...

REM Vai para a pasta onde o script está
cd /d %~dp0

set VENV_DIR=venv

REM Cria venv se não existir
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo 📦 Criando virtualenv em .\%VENV_DIR% ...
    python -m venv %VENV_DIR%
)

REM Ativa venv
echo ✅ Ativando virtualenv...
call "%VENV_DIR%\Scripts\activate.bat"

REM Sobe a API
echo 🚀 Subindo FastAPI em http://127.0.0.1:8000 ...
uvicorn cmd.main:app --reload --host 0.0.0.0 --port 8000

endlocal
