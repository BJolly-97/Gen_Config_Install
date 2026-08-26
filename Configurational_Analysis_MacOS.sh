#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "Installing Gen_Config and required Python modules..."
python3 -m pip install --quiet --no-warn-script-location -e .
if [ $? -ne 0 ]; then
  echo "Dependency install failed. Check Python installation."
  echo "Press any key to continue..."
  read -n 1 -s
  exit 1
fi
echo "All required modules installed."

echo ""

python3 -m gen_config.cli
