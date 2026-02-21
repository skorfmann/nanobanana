#!/usr/bin/env bash
set -euo pipefail

CLAUDE_DIR="${CLAUDE_HOME:-${HOME}/.claude}"
SKILL_DIR="${CLAUDE_DIR}/skills/nanobanana"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_SRC="${SCRIPT_DIR}/skill/nanobanana"

usage() {
  echo "Usage: ./install.sh [--claude-dir <path>]"
  echo ""
  echo "Options:"
  echo "  --claude-dir <path>  Claude Code config directory (default: ~/.claude)"
  echo "                       Also settable via CLAUDE_HOME env var"
  exit 0
}

while [ $# -gt 0 ]; do
  case "$1" in
    --claude-dir) CLAUDE_DIR="$2"; SKILL_DIR="${CLAUDE_DIR}/skills/nanobanana"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

# Install or upgrade CLI
echo "Installing nanobanana CLI..."
if [ -f "${SCRIPT_DIR}/pyproject.toml" ]; then
  # Local install from source
  uv tool install --upgrade "${SCRIPT_DIR}" 2>/dev/null || uv tool install "${SCRIPT_DIR}"
else
  # Remote install from PyPI
  uv tool install nanobanana --upgrade 2>/dev/null || uv tool install nanobanana
fi

# Install Claude Code skill (only if Claude Code is set up)
if [ -d "$CLAUDE_DIR" ]; then
  if [ -d "$SKILL_SRC" ]; then
    echo "Installing Claude Code skill..."
    mkdir -p "$SKILL_DIR"
    cp -r "$SKILL_SRC"/* "$SKILL_DIR"/
    echo "Skill installed to ${SKILL_DIR}"
  else
    echo "Warning: skill source not found at ${SKILL_SRC}"
    echo "Run this script from the nanobanana repository root."
  fi
else
  echo "Skipping Claude Code skill (${CLAUDE_DIR} not found)."
  echo "Install Claude Code first, then re-run this script to add the skill."
fi

echo ""
echo "Done! Make sure GEMINI_API_KEY or OPENROUTER_API_KEY is set."
