#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=src python -m gbt_thebrain_bridge info
PYTHONPATH=src python -m gbt_thebrain_bridge check --payload '{}'
PYTHONPATH=src python -m gbt_thebrain_bridge run   --payload '{}'
