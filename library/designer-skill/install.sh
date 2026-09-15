#!/bin/bash
# Claude Designer Skill — Installer
# Kopiert den Skill in das globale Claude-Skills-Verzeichnis (~/.claude/skills/designer/)

set -e

SKILL_DIR="$HOME/.claude/skills/designer"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🎨 Claude Designer Skill — Installation"
echo ""

# Zielordner anlegen falls nötig
mkdir -p "$SKILL_DIR"

# SKILL.md kopieren
cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"

echo "✅ Skill installiert unter: $SKILL_DIR"
echo ""
echo "Starte Claude Code und benutze /designer um loszulegen."
