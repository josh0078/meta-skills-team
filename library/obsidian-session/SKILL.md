---
name: obsidian-session
description: "Use this skill when the user types /session-save or /session-load, or wants to save their current work progress before stopping, or wants to load context from a previous session. Also use when someone is starting fresh and wants to know what a colleague or previous Claude instance last worked on — especially phrases like 'fortschritt speichern', 'session speichern', 'was hat mein kollege gemacht', 'wo haben wir aufgehört', 'kontext laden', 'was wurde zuletzt gemacht', or asking about the last known state of a project from Obsidian session logs. Core use cases: saving work summaries to Obsidian, loading session context at the start of work, cross-developer handoffs, and picking up where another person left off. ALWAYS trigger for /session-save and /session-load."
---

# Obsidian Session Skill

Dieser Skill ermöglicht es mehreren Mitarbeitern und Claude-Instanzen, effektiv zusammenzuarbeiten, indem jede Session strukturiert im gemeinsamen Obsidian Vault dokumentiert wird.

## Vault-Konfiguration

**Standard-Vault-Pfad:** `/Users/joshuaerdol/Library/Mobile Documents/com~apple~CloudDocs/Obsidian daten`

Falls der Vault-Pfad in der CLAUDE.md des Projekts als `OBSIDIAN_VAULT` definiert ist, verwende diesen stattdessen.

---

## Befehl: /session-save

### Was tun

Erstelle eine strukturierte Session-Dokumentation im Obsidian Vault — **vollständig automatisch**, ohne dass der User alles selbst beschreiben muss. Analysiere dazu das Projekt und die Konversation eigenständig. Diese Note soll es einem anderen Menschen oder einer anderen Claude-Instanz ermöglichen, sofort zu verstehen was in dieser Session passiert ist — ohne die gesamte Konversation lesen zu müssen.

### Schritt-für-Schritt

1. **Zwei Fragen stellen** — kurz hintereinander, keine weiteren:
   - `"Dein Name? (z.B. Joshua)"`
   - `"Projektname für diese Session? (z.B. Obsidian Standardisierung, Jarvis, 24/7 ON)"` — der User gibt den Namen selbst an, damit er später gezielt danach suchen und laden kann.

2. **Kontext automatisch analysieren** — Führe diese Analyse selbstständig durch:

   **a) Arbeitsverzeichnis & Git-Status prüfen:**
   ```bash
   git status
   git diff --stat
   git log --oneline -10
   ```
   Wenn kein Git-Repo: suche nach kürzlich geänderten relevanten Dateien.

   **b) Konversation analysieren** — extrahiere:
   - Was wurde besprochen / gebaut / entschieden?
   - Welche Probleme wurden gelöst?
   - Was blieb ungelöst oder wurde explizit als TODO erwähnt?
   - Welche Architekturentscheidungen oder Trade-offs wurden diskutiert?

   **c) Relevante geänderte Dateien kurz lesen** — um zu verstehen was sich geändert hat.

3. **Speicherort — immer gleich, egal welches Projekt:**
   ```
   /Users/joshuaerdol/Library/Mobile Documents/com~apple~CloudDocs/Obsidian daten/Projekte/_Sessions/
   ```
   Alle Sessions landen im selben Ordner — so hat man eine zentrale Übersicht über alle Projekte und Claude kann beim `/session-load` einfach nach Projektname filtern.

4. **Dateiname generieren** nach Schema:
   ```
   YYYY-MM-DD_[Autor]_[Projektname].md
   ```
   Beispiel: `2026-05-24_Joshua_Obsidian-Standardisierung.md`
   — Leerzeichen im Projektnamen durch Bindestriche ersetzen.

5. **Note erstellen** mit dem unten definierten Template — befüllt aus der Analyse, nicht aus User-Input.

6. **Bestätigung geben:** `"Session gespeichert: [relativer Pfad]"` und zeige die wichtigsten extrahierten TODOs als kurze Preview.

### Note-Template

```markdown
---
type: session-log
date: YYYY-MM-DD
time: HH:MM
author: [Name]
project: [Projektname]
tags:
  - session-log
  - [projekt-tag]
related_sessions: []
---

# Session [DATUM] — [Autor] — [Projekt]

## Was wurde gemacht

[2-5 Sätze: Was war der Fokus dieser Session? Was wurde erreicht?]

## Geänderte & erstellte Dateien

| Datei | Aktion | Beschreibung |
|-------|--------|--------------|
| `pfad/zur/datei.ext` | erstellt/geändert/gelöscht | Kurze Beschreibung was geändert wurde |

*Wenn keine Dateien geändert wurden: "Keine Dateien geändert (Analyse/Planung-Session)"*

## Entscheidungen & Begründungen

- **[Entscheidung]:** [Warum wurde das so gemacht? Welche Alternativen wurden verworfen?]

*Nur echte Entscheidungen mit Begründung — keine Trivialitäten.*

## Offene TODOs & nächste Schritte

- [ ] [Was muss als nächstes gemacht werden]
- [ ] [Offenes Problem oder nächster Schritt]

## Kontext für die nächste Session

[1-3 Sätze: Was muss die nächste Person / Claude-Instanz unbedingt wissen?]

---
*Generiert von Claude · [[_Sessions/README|Session-Index]]*
```

### Wichtig beim Befüllen

- **Summary:** Schreibe für jemanden der diese Konversation nie gesehen hat.
- **Dateien:** Nur real existierende Dateien eintragen — niemals halluzinieren.
- **Entscheidungen:** Das "Warum", nicht nur das "Was".
- **TODOs:** Konkret und actionable.
- **Wikilinks:** Verlinke auf relevante Obsidian-Notes mit `[[Notename]]` wenn sie existieren.

---

## Befehl: /session-load

### Was tun

Lade den Kontext der letzten Sessions und bringe die aktuelle Claude-Instanz auf den aktuellen Stand.

### Schritt-für-Schritt

1. **Projektname erfragen** — `"Für welches Projekt? (z.B. Obsidian Standardisierung)"` — oder aus dem aktuellen Arbeitsverzeichnis ableiten wenn eindeutig.

2. **Sessions finden** — Suche in `/Users/joshuaerdol/Library/Mobile Documents/com~apple~CloudDocs/Obsidian daten/Projekte/_Sessions/` nach `.md` Dateien die den Projektnamen im Dateinamen enthalten, sortiert nach Datum (neueste zuerst).

3. **Letzten 1-3 Sessions lesen** — letzte Session immer vollständig, ältere nur bei offenen TODOs.

4. **Kompakten Kontext ausgeben:**

```
## Session-Kontext geladen

**Letzter Stand:** [Datum] von [Autor]
**Projekt:** [Projektname]

### Was bisher passiert ist
[2-4 Sätze Zusammenfassung]

### Offene TODOs
- [ ] ...

### Wichtige Entscheidungen
- **[Entscheidung]:** [Begründung]

### Empfohlener nächster Schritt
[Konkrete Empfehlung]
```

5. **Rückfrage:** `"Soll ich mit [nächster Schritt] weitermachen, oder gibt es eine andere Priorität?"`

### Wenn keine Sessions gefunden

`"Keine Sessions für [Projekt] gefunden. Soll ich nach /session-save eine erste Dokumentation anlegen?"`

---

## Hinweise für andere Claude-Instanzen

Wenn du `/session-load` ausführst und Sessions findest, behandle die dokumentierten Entscheidungen und TODOs als verlässliche Fakten über den Projektstand.
