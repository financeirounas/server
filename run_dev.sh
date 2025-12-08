#!/usr/bin/env bash
set -e

echo "🔹 Iniciando ambiente de desenvolvimento (Linux/macOS)..."

# Vai para a raiz do projeto (onde está este script)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# Nome da venv
VENV_DIR="venv"

# Cria venv se não existir
if [ ! -d "$VENV_DIR" ]; then
  echo "📦 Criando virtualenv em ./$VENV_DIR ..."
  python3 -m venv "$VENV_DIR"
fi


echo "✅ Ativando virtualenv..."
source "$VENV_DIR/bin/activate"


echo "🚀 Subindo FastAPI em http://127.0.0.1:8000 ..."
uvicorn cmd.main:app --reload --host 0.0.0.0 --port 8000
å