#!/bin/sh
# Install BrillianceLab git hooks. Run once after cloning.
# Works on Git Bash / WSL / macOS / Linux.
set -e
cd "$(git rev-parse --show-toplevel)"
HOOK_DIR=".git/hooks"
mkdir -p "$HOOK_DIR"
cp build/git-hooks/pre-commit "$HOOK_DIR/pre-commit"
chmod +x "$HOOK_DIR/pre-commit"
echo "✓ pre-commit hook installed at $HOOK_DIR/pre-commit"
echo "  it runs:  JSON-LD parse · canonical audit · check_js · punct dry-run"
echo "  bypass once with:  git commit --no-verify"
