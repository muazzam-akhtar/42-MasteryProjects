#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="${VENV_DIR:-.venv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
REQ_FILE="${REQ_FILE:-requirements.txt}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "Error: '${PYTHON_BIN}' not found. Install Python 3 or set PYTHON_BIN=python3.x" >&2
  exit 1
fi

if [ ! -f "${REQ_FILE}" ]; then
  echo "Error: '${REQ_FILE}' not found in $(pwd)." >&2
  echo "Create it first, then re-run:" >&2
  echo "  touch ${REQ_FILE}" >&2
  exit 1
fi

if [ ! -d "${VENV_DIR}" ]; then
  echo "Creating virtual environment in '${VENV_DIR}'..."
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
else
  echo "Virtual environment already exists at '${VENV_DIR}'."
fi

echo "Activating '${VENV_DIR}'..."
# shellcheck disable=SC1090
source "${VENV_DIR}/bin/activate"

echo "Upgrading pip/setuptools/wheel..."
python -m pip install --upgrade pip setuptools wheel

echo "Installing dependencies from '${REQ_FILE}'..."
python -m pip install -r "${REQ_FILE}"

echo "Done."
echo "To activate later, run:"
echo "  source ${VENV_DIR}/bin/activate"
