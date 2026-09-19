import os
import json
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST_PATH = os.path.join(BASE_DIR, "skills-manifest.json")
LOG_PATH = os.path.join(BASE_DIR, "installation_log.json")

def verify_skills(pc_name):
    if not os.path.exists(MANIFEST_PATH):
        print(f"Fehler: {MANIFEST_PATH} nicht gefunden.")
        sys.exit(1)
        
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    log_data = {}
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            log_data = json.load(f)
            
    if pc_name not in log_data:
        log_data[pc_name] = []
        
    installed_skills = log_data[pc_name]
        
    print(f"Starte Überprüfung der Skills für PC: {pc_name}...\n")
    
    all_good = True
    new_installations = False
    
    for skill in manifest.get("skills", []):
        skill_id = skill.get("id")
        
        if skill_id in installed_skills:
            print(f"Skill '{skill.get('name')}' ist bereits auf '{pc_name}' installiert. (Übersprungen)")
            continue
            
        print(f"Prüfe neuen Skill: {skill.get('name')}")
        
        # 1. Check entrypoint
        entrypoint_rel = skill.get("entrypoint", "")
        entrypoint_abs = os.path.join(BASE_DIR, entrypoint_rel) if not os.path.isabs(entrypoint_rel) else entrypoint_rel
        if not os.path.exists(entrypoint_abs):
            print(f"  [FEHLER] Entrypoint {entrypoint_rel} nicht gefunden!")
            all_good = False
            continue
            
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
                continue
        else:
            print("  [OK] Keine spezifischen Python-Abhängigkeiten.")
            
        # Mark as installed
        installed_skills.append(skill_id)
        new_installations = True
        print("---")
        
    if new_installations:
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        print("\nDas Installation-Log wurde aktualisiert. Lade Update auf GitHub hoch...")
        try:
            subprocess.check_call(["git", "add", "installation_log.json"], cwd=BASE_DIR)
            subprocess.check_call(["git", "commit", "-m", f"Protokoll: {pc_name} hat neue Skills installiert"], cwd=BASE_DIR)
            subprocess.check_call(["git", "push"], cwd=BASE_DIR)
            print("Push erfolgreich.")
        except Exception as e:
            print(f"Warnung: Konnte das Log nicht auf GitHub pushen (möglicherweise wegen fehlender Berechtigung). Bitte manuell pushen.")
            
    # === IDE-Integration ===
    print("\nPrüfe IDE-Integrationen...")
    antigravity_config = os.path.expanduser("~/.gemini/config")
    if os.path.exists(antigravity_config):
        target = os.path.join(antigravity_config, "skills")
        src = os.path.join(BASE_DIR, "library")
        if not os.path.exists(target) and not os.path.islink(target):
            try:
                os.symlink(src, target)
                print("  [OK] Symlink für Antigravity IDE erstellt.")
            except Exception as e:
                print(f"  [WARNUNG] Konnte Symlink nicht erstellen: {e}")
        else:
            print("  [OK] Antigravity IDE ist bereits verknüpft.")

    if all_good:
        print("\nErgebnis: Der PC ist auf dem neuesten Stand und alle Skills sind einsatzbereit!")
    else:
        print("\nErgebnis: Es gab Fehler bei der Einrichtung einiger Skills.")
        sys.exit(1)

if __name__ == "__main__":
    pc_name = sys.argv[1] if len(sys.argv) > 1 else "Unbekannter PC"
    verify_skills(pc_name)
