#!/bin/bash

set -e

echo "🔍 Running Python linters & formatters using Poetry..."

# Function to run a tool and check for failure
run_tool() {
  local tool=$1
  local args=$2

  echo "▶ Running $tool $args"
  if ! poetry run $tool $args; then
    echo "❌ $tool failed. Fix the above issues and try again."
    exit 1
  else
    echo "✅ $tool passed"
  fi
}

# Run tools
run_tool black .
run_tool isort .
run_tool flake8 .
run_tool pylint app/

echo "🎉 All checks passed successfully!"
