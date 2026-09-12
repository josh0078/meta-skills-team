# Universal Agent Skill Bootstrap Protocol

Dieses Dokument dient als Einstiegspunkt für den Meta-Skill Orchestrator.

## Initialisierung für den Agenten
1. Identifiziere dein Modell (Claude, Google, Kimi etc.).
2. Lies `skills-manifest.json`, um verfügbare Skills und deren "adapter" zu finden.
3. Wenn der Nutzer dich bittet, die Skills zu **aktualisieren** (z.B. durch "Update Skills", "Pull" oder ähnliches), führe folgende Befehle in diesem Verzeichnis aus:
   - `git pull` (um die neuesten Skills vom Server zu laden)
   - `python3 sync_and_verify.py` (um Abhängigkeiten zu installieren und Fehler zu prüfen)
4. Melde dem Nutzer nach der Aktualisierung das Ergebnis von `sync_and_verify.py`.

## Ausführung
- Nutze den für dein Modell definierten "adapter" in der `skills-manifest.json`, um einen Skill auszuführen.

