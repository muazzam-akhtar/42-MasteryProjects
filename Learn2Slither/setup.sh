#!/usr/bin/env bash
set -euo pipefail

# Configuration
VENV_DIR="${VENV_DIR:-.venv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
REQ_FILE="${REQ_FILE:-requirements.txt}"
PYPI_INDEX_URL="https://pypi.org/simple"

echo "Using Python: ${PYTHON_BIN}"

# Verify Python exists
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
    echo "ERROR: '${PYTHON_BIN}' not found."
    echo "Install Python 3 or set PYTHON_BIN to the correct executable."
    exit 1
fi

# Verify requirements file exists
if [ ! -f "${REQ_FILE}" ]; then
    echo "ERROR: '${REQ_FILE}' not found in $(pwd)"
    exit 1
fi

# Create virtual environment if needed
if [ ! -d "${VENV_DIR}" ]; then
    echo "Creating virtual environment: ${VENV_DIR}"
    "${PYTHON_BIN}" -m venv "${VENV_DIR}"
else
    echo "Virtual environment already exists: ${VENV_DIR}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
# shellcheck disable=SC1090
source "${VENV_DIR}/bin/activate"

# Upgrade packaging tools
echo "Upgrading pip, setuptools, and wheel..."
python -m pip install \
    --upgrade \
    pip \
    setuptools \
    wheel \
    --index-url "${PYPI_INDEX_URL}"

# Install requirements from PyPI
echo "Installing dependencies from ${REQ_FILE}..."
python -m pip install \
    --no-cache-dir \
    --index-url "${PYPI_INDEX_URL}" \
    -r "${REQ_FILE}"

# Verify installation of common packages
echo "Installed packages:"
python -m pip list

# Optional validation
if python -m pip show flake8 >/dev/null 2>&1; then
    echo "✓ flake8 installed"
fi

if python -m pip show pygame >/dev/null 2>&1; then
    echo "✓ pygame installed"
fi

echo
echo "Setup completed successfully."
echo
echo "To activate the environment later:"
echo "source ${VENV_DIR}/bin/activate"