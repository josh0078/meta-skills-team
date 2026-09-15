import os
import json
import shutil
import re
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_AGENTS_SKILLS = os.path.expanduser("~/.agents/skills")
TARGET_LIBRARY = os.path.join(BASE_DIR, "library")
MANIFEST_PATH = os.path.join(BASE_DIR, "skills-manifest.json")

def read_skill_meta(skill_path, default_name):
    candidates = ['SKILL.md', f'{default_name}.md', 'README.md', 'index.md']
    desc = "Automatisch gescannter Skill"
    for cand in candidates:
        p = os.path.join(skill_path, cand)
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    content = f.read()
                match = re.search(r'^description:\s*(.+)$', content, re.MULTILINE)
                if match:
                    desc = match.group(1).strip()
                    if desc.startswith('"') and desc.endswith('"'): desc = desc[1:-1]
                    break
            except:
                pass
    return desc

def main():
    if not os.path.exists(TARGET_LIBRARY): os.makedirs(TARGET_LIBRARY)
    if not os.path.exists(MANIFEST_PATH):
        print("Manifest nicht gefunden.")
        return

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    existing_ids = {s.get("id") for s in manifest.get("skills", [])}
    added_any = False
    
    print("Suche nach neuen lokalen Skills...")
    if os.path.exists(SOURCE_AGENTS_SKILLS):
        for name in os.listdir(SOURCE_AGENTS_SKILLS):
            src_path = os.path.join(SOURCE_AGENTS_SKILLS, name)
            if not os.path.isdir(src_path): continue
                
            skill_id = f"agent-skill-{name}"
            if skill_id not in existing_ids:
                print(f"-> Neuen Skill gefunden: {name}")
                dst_path = os.path.join(TARGET_LIBRARY, name)
                if not os.path.exists(dst_path):
                    shutil.copytree(src_path, dst_path)
                
                entrypoint = f"./library/{name}/SKILL.md"
                if not os.path.exists(os.path.join(dst_path, "SKILL.md")):
                    entrypoint = f"./library/{name}"
                    
                manifest["skills"].append({
                    "id": skill_id,
                    "name": name.replace("-", " ").title(),
                    "description": read_skill_meta(src_path, name),
                    "entrypoint": entrypoint,
                    "dependencies": {"python_packages": [], "system_commands": []},
                    "adapters": {
                        "claude": {"invocation_style": "slash_command", "command": f"/{name}"},
                        "google": {"invocation_style": "function_calling"}
                    }
                })
                existing_ids.add(skill_id)
                added_any = True

    if added_any:
        with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
            
        print("Neue Skills wurden zum Register hinzugefügt. Lade auf GitHub hoch...")
        try:
            subprocess.check_call(["git", "add", "."], cwd=BASE_DIR)
            subprocess.check_call(["git", "commit", "-m", "Auto-sync lokale Skills"], cwd=BASE_DIR)
            subprocess.check_call(["git", "push"], cwd=BASE_DIR)
            print("Push erfolgreich! Die Skills sind nun für alle PCs verfügbar.")
        except Exception as e:
            print(f"Git Push fehlgeschlagen: {e}. Bitte pushe manuell.")
    else:
        print("Keine neuen lokalen Skills auf diesem PC gefunden.")

if __name__ == "__main__":
    main()
