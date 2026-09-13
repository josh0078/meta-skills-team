import os
import json
import subprocess
import sys

MANIFEST_PATH = "skills-manifest.json"

def verify_skills():
    if not os.path.exists(MANIFEST_PATH):
        print("Fehler: skills-manifest.json nicht gefunden.")
        sys.exit(1)
        
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    print("Starte Überprüfung der Skills...\n")
    
    all_good = True
    for skill in manifest.get("skills", []):
        print(f"Prüfe Skill: {skill.get('name')} ({skill.get('id')})")
        
        # 1. Check entrypoint
        entrypoint = skill.get("entrypoint")
        if not os.path.exists(entrypoint):
            print(f"  [FEHLER] Entrypoint {entrypoint} nicht gefunden!")
            all_good = False
            
        # 2. Check dependencies
        deps = skill.get("dependencies", {})
        pip_packages = deps.get("python_packages", [])
        
        if pip_packages:
            print(f"  Installiere/Prüfe Python-Pakete: {', '.join(pip_packages)}")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", *pip_packages], 
                                      stdout=subprocess.DEVNULL)
                print("  [OK] Abhängigkeiten installiert.")
            except subprocess.CalledProcessError:
                print("  [FEHLER] Konnte Pakete nicht installieren.")
                all_good = False
        else:
            print("  [OK] Keine spezifischen Python-Abhängigkeiten.")
            
        print("---")
        
    if all_good:
        print("Ergebnis: Alle Skills sind einsatzbereit!")
    else:
        print("Ergebnis: Es gab Fehler bei der Einrichtung. Bitte prüfe die Logs.")
        sys.exit(1)

if __name__ == "__main__":
    verify_skills()

