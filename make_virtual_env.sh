#!/usr/bin/env bash
set -e

PYTHON_BIN=${1:-/usr/bin/python3.7}
REQUIREMENTS=${2:-requirements.txt}

#Force regeneration
if [ -n "$3" ]; then
    rm -rf .env
fi

if [ ! -d ".env" ]; then
    virtualenv --python=$PYTHON_BIN .env
    source .env/bin/activate
    pip install -r $REQUIREMENTS
fi
source .env/bin/activate
