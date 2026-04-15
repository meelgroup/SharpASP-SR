#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(pwd)"

echo "Building Compl..."
cd "$ROOT_DIR/Compl"
make
cp clark "$ROOT_DIR"


cd "$ROOT_DIR"
echo "Downloading ganak..."
wget https://github.com/meelgroup/ganak/releases/download/release%2Fv2.6.1/ganak-v2.6.1-linux-amd64.tar.gz
tar -xvzf ganak-v2.6.1-linux-amd64.tar.gz

echo "Done. Copied binaries to:"
echo "  $ROOT_DIR/scripts/hashcount"
echo "  $ROOT_DIR/scripts/td"
echo "  $ROOT_DIR/scripts/flow_cutter_pace17"