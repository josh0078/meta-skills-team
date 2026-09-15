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

## Einen neuen Skill hinzufügen (Für den Agenten)
Wenn der Nutzer dich bittet, einen neuen Skill zum Register hinzuzufügen, musst du **komplett selbstständig** folgende Schritte ausführen:
1. **Ordner erstellen:** Erstelle einen neuen Ordner unter `./library/<skill-name>/` und lege dort die Skripte oder `SKILL.md` des neuen Skills ab.
2. **Manifest updaten:** Öffne die `skills-manifest.json` und füge ein neues JSON-Objekt in das Array `"skills"` ein (inkl. `id`, `name`, `description`, `entrypoint` und `adapters`).
3. **Commit & Push:** Führe im Hauptordner (`.skills` bzw. `.meta-skills`) folgende Befehle im Terminal aus, um den neuen Skill für das gesamte Team hochzuladen:
   - `git add .`
   - `git commit -m "Neuen Skill hinzugefügt: <skill-name>"`
   - `git push`
(Achte darauf, den Sandbox Bypass zu nutzen, falls das Terminal danach fragt).
