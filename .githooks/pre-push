#!/usr/bin/env bash
set -uo pipefail

if ! command -v trivy >/dev/null 2>&1; then
  echo "pre-push: trivy not found on PATH; see .claude/skills/trivy-scan/setup.md for setup instructions." >&2
  exit 1
fi

if ! trivy fs . --scanners vuln --severity CRITICAL --exit-code 1 --ignore-unfixed --quiet; then
  exit 1
fi

exit 0
