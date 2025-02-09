#!/bin/bash

# Make script executable with: chmod +x scripts/run_tests.sh

# Activate virtual environment
source .venv/bin/activate

# Export environment variables
export PYTHONPATH=$PYTHONPATH:$(pwd)
export ENVIRONMENT=local
export LOG_LEVEL=INFO

# Run tests with proper configuration
pytest -v \
    -m integration \
    --log-cli-level=INFO \
    --log-cli-format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)" \
    --log-cli-date-format="%Y-%m-%d %H:%M:%S" \
    tests/integration/test_health_check.py 