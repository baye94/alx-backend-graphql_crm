#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Change to the project directory
cd "$PROJECT_DIR" || exit 1

# Set Python path to include the project directory
export PYTHONPATH="${PROJECT_DIR}:${PYTHONPATH}"
export DJANGO_SETTINGS_MODULE=alx_backend_graphql.settings

# Log CWD for test verification if needed
echo "cwd=$(pwd)"

# If in test mode, use a fixed date
if [ "$TEST_MODE" = "1" ]; then
    python manage.py cleanup_inactive_customers --reference-date="2024-01-01"
else
    python manage.py cleanup_inactive_customers
fi
