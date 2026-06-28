#!/usr/bin/env bash
# Motif easy setup. No pip, no build. Wires three things, each optional and reversible:
#   1. a `motif` (and `ii`/`oii`) command on your PATH      -> use it in any terminal
#   2. a Claude Code skill at ~/.claude/skills/motif        -> type /motif in Claude Code
#   3. the Motif MCP server (read-only) registered with Claude Code -> motif.* tools everywhere
#
# Re-running is safe (idempotent). Uninstall: ./install.sh --uninstall
set -euo pipefail

REPO="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
BIN_DIR="${MOTIF_BIN_DIR:-$HOME/.local/bin}"
SKILL_DIR="$HOME/.claude/skills/motif"
PY="${MOTIF_PYTHON:-python3}"
ok(){ printf "  \033[32mok\033[0m   %s\n" "$1"; }
info(){ printf "  ->   %s\n" "$1"; }

uninstall(){
  echo "Uninstalling Motif setup..."
  for c in motif ii oii; do [ -L "$BIN_DIR/$c" ] && rm -f "$BIN_DIR/$c" && ok "removed $BIN_DIR/$c"; done
  [ -L "$SKILL_DIR" ] && rm -f "$SKILL_DIR" && ok "removed skill symlink $SKILL_DIR"
  command -v claude >/dev/null 2>&1 && claude mcp remove motif -s user >/dev/null 2>&1 && ok "removed motif MCP server" || true
  echo "Done."; exit 0
}
[ "${1:-}" = "--uninstall" ] && uninstall

echo "Installing Motif (dependency-free core; no pip required)..."
chmod +x "$REPO/bin/motif"

# 1. PATH command(s)
mkdir -p "$BIN_DIR"
for c in motif ii oii; do
  ln -sf "$REPO/bin/motif" "$BIN_DIR/$c"
done
ok "linked motif, ii, oii -> $BIN_DIR"
case ":$PATH:" in *":$BIN_DIR:"*) : ;; *) info "add to your shell profile: export PATH=\"$BIN_DIR:\$PATH\"";; esac

# 2. Claude Code skill (type /motif)
if [ -d "$HOME/.claude/skills" ] || mkdir -p "$HOME/.claude/skills" 2>/dev/null; then
  ln -sfn "$REPO" "$SKILL_DIR"
  ok "Claude Code skill linked -> $SKILL_DIR (type /motif)"
else
  info "skipped skill link (no ~/.claude/skills)"
fi

# 3. MCP server (read-only by default; motif.* tools in Claude Code)
if command -v claude >/dev/null 2>&1; then
  claude mcp remove motif -s user >/dev/null 2>&1 || true
  if claude mcp add motif -s user -- "$REPO/bin/motif" mcp serve >/dev/null 2>&1; then
    ok "MCP server registered (read-only): motif.* tools available in Claude Code"
  else
    info "MCP registration skipped (run manually: claude mcp add motif -s user -- $REPO/bin/motif mcp serve)"
  fi
else
  info "claude CLI not found; skipped MCP registration"
fi

# verify
echo "Verifying..."
"$REPO/bin/motif" --version
echo
echo "Done. Try:  motif doctor   |   motif evidence query --product-form dashboard   |   /motif (in Claude Code)"
