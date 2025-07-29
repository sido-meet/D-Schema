#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Run all tests
echo "--- RUNNING ALL TESTS ---"
uv run python -m unittest discover tests

echo "\n--- ALL TESTS COMPLETED SUCCESSFULLY ---"