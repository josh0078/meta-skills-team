# Claude Designer Skill

Ein visueller Style-Picker für Claude Code. Generiert eine Live-Demo-Seite mit 13+ Stilen aus [21st.dev](https://21st.dev), du klickst was dir gefällt — Claude baut die Website dazu.

## Was der Skill macht

1. Öffnet einen **visuellen Picker** im Browser mit Mini-Live-Previews jedes Stils
2. Du wählst pro Kategorie (Hero, Background, Buttons, Cards)
3. Speichert deine Wahl in `.designer-config.json`
4. Claude implementiert die gewählten Stile im Projekt

## Stile im Katalog

| Kategorie | Stile |
|-----------|-------|
| Hero | Shape Hero, Cinematic Landing, Gallery Scroll, Container Scroll, Globe Hero |
| Hintergrund | Dream Sky Glow, Grid Glow BG, WebGL Shader, Shader Lines |
| Buttons | Liquid Glass, Glass Button |
| Cards | Glassy Pricing, Gradient Bold Card |

## Installation

```bash
git clone https://github.com/josh0078/claude-designer-skill
cd claude-designer-skill
chmod +x install.sh
./install.sh
```

Oder als Einzeiler:

```bash
git clone https://github.com/josh0078/claude-designer-skill ~/.claude/skills/designer
```

## Benutzung

In Claude Code einfach tippen:

```
/designer
```

Claude öffnet den Picker automatisch im Browser.

### Weitere Befehle

- `/designer` — Neues Design auswählen
- `/designer watch` — Watch-Modus: Claude reagiert automatisch auf Browser-Annotationen (Zeichenstift-Feedback)

## Voraussetzungen

- [Claude Code](https://claude.ai/code) installiert
- Next.js App Router Projekt (oder Vite/vanilla HTML)
