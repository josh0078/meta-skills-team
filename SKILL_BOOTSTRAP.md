# Universal Agent Skill Bootstrap Protocol

Dieses Dokument dient als Einstiegspunkt für den Meta-Skill Orchestrator.

## Initialisierung für den Agenten
1. Identifiziere dein Modell (Claude, Google, Kimi etc.).
2. Finde heraus, auf welchem der 3 PCs du gerade läufst: **Joshua Mac**, **Joshua Mac mini**, oder **Mathis Mac**. (Frage den Nutzer, falls es unklar ist).
3. Lies `skills-manifest.json`, um verfügbare Skills und deren "adapter" zu finden.

## Befehl: "Update Skills" (Updates vom Team laden)
Wenn der Nutzer dich bittet, die Skills zu aktualisieren, führe folgende Befehle in diesem Verzeichnis aus:
1. `git pull` (um neue Skills vom Server zu laden)
2. `python3 sync_and_verify.py "PC_NAME"` (ersetze PC_NAME z.B. durch "Joshua Mac"). 
*Hinweis: Das Skript prüft das `installation_log.json`, überspringt bereits installierte Skills, lädt fehlende Pakete für neue Skills herunter und pusht das Log automatisch.*

## Befehl: "Sync Local Skills" (Lokale Skills ins Register laden)
Wenn der Nutzer diesen Befehl gibt:
1. Führe `python3 auto_sync_local.py` aus.
*Hinweis: Dieses Skript durchsucht den PC nach lokalen Skills, kopiert diese in die `library`, updatet das Manifest und pusht alles automatisch zu GitHub für das Team.*

## Einen manuellen neuen Skill hinzufügen
Wenn der Nutzer einen speziellen Ordner hochladen will:
Erstelle den Ordner unter `./library/<skill-name>/`, pass die `skills-manifest.json` an, führe `git add .`, `git commit` und `git push` aus.

## Ausführung
- Nutze den für dein Modell definierten "adapter" in der `skills-manifest.json`, um einen Skill auszuführen.
