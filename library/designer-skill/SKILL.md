---
name: designer
description: "Use this skill when the user types /designer, wants to apply a visual style to a project, asks 'welches design', 'stil ändern', 'design auswählen', 'design anpassen', 'theme wechseln', wants to set up the visual identity of a project, or references any of the design styles by name (Globe Hero, Glass Button, Cinematic, etc.). Also use when user types '/designer watch', 'watch modus', 'auf feedback warten', or wants Claude to automatically react to browser annotations."
---

# Designer Skill

Du bist ein erfahrener UI/UX-Designer und Frontend-Entwickler. Du kennst einen Katalog von 18 visuellen Stilen von 21st.dev und kannst diese **komponentenbasiert kombinieren** und auf Projekte anwenden.

Der Kern dieses Skills: Du generierst eine **visuelle Picker-Seite** mit echten Mini-Live-Demos jedes Stils, öffnest sie im Browser, und der User wählt durch Klicken. Nach Bestätigung wird die Config gespeichert und alles temporäre gelöscht.

---

## Dein Ablauf

### Schritt 1: Config prüfen

```bash
cat .designer-config.json 2>/dev/null || echo "NO_CONFIG"
```

- **Config vorhanden** → Zeige aktuelle Konfiguration als Tabelle. Frage ob der User etwas ändern will. Falls ja: gehe zu Schritt 2.
- **Keine Config** → Direkt zu Schritt 2.

---

### Schritt 2: Projekt analysieren

```bash
find . -name "*.tsx" -o -name "*.jsx" -o -name "*.html" | grep -v node_modules | grep -v ".next" | head -30
ls -la
cat package.json 2>/dev/null | grep -E '"next"|"react"|"vite"' | head -5
```

Identifiziere:
- **Framework**: Next.js App Router, Next.js Pages, Vite/React, oder vanilla HTML
- Läuft bereits ein Dev-Server? (Port 3000, 5173, etc.)

---

### Schritt 3: Visuellen Picker generieren

#### Für Next.js App Router Projekte:

Erstelle **zwei temporäre Dateien**:

**1. API Route** — `app/api/designer-save/route.ts`

```typescript
import { NextResponse } from "next/server";
import { writeFileSync, rmSync, mkdirSync, existsSync } from "fs";
import { join } from "path";

export async function POST(request: Request) {
  const body = await request.json();
  const { styles, globalPalette, sourceLinks, assets, ...rest } = body;

  // Save uploaded assets (logo, references) to design-assets/
  const savedAssets: Array<{ name: string; type: string; path: string }> = [];
  if (Array.isArray(assets) && assets.length > 0) {
    const assetsDir = join(process.cwd(), "design-assets");
    if (!existsSync(assetsDir)) mkdirSync(assetsDir, { recursive: true });
    assets.forEach((asset: { name: string; data: string; type: "logo" | "reference" }, i: number) => {
      const ext = asset.name.split(".").pop()?.toLowerCase() ?? "png";
      const safe = asset.name.replace(/[^a-z0-9.]/gi, "-").toLowerCase();
      const filename = `${asset.type}-${safe}`;
      const base64Data = asset.data.replace(/^data:image\/[^;]+;base64,/, "");
      writeFileSync(join(assetsDir, filename), Buffer.from(base64Data, "base64"));
      savedAssets.push({ name: asset.name, type: asset.type, path: `design-assets/${filename}` });
    });
  }

  const config = { ...rest, styles, globalPalette, sourceLinks, assets: savedAssets };
  writeFileSync(join(process.cwd(), ".designer-config.json"), JSON.stringify(config, null, 2));

  setTimeout(() => {
    try {
      rmSync(join(process.cwd(), "app/designer-picker"), { recursive: true, force: true });
      rmSync(join(process.cwd(), "app/api/designer-save"), { recursive: true, force: true });
    } catch {}
  }, 1000);

  return NextResponse.json({ success: true });
}
```

**2. Picker Page** — `app/designer-picker/page.tsx`

Dies ist die Kernkomponente. Erstelle sie mit folgendem Code (passe den Projektnamen dynamisch an):

```tsx
"use client";
import { useState, useRef } from "react";

// ── STYLE DEFINITIONS ──────────────────────────────────────────────────────
const STYLE_CATALOG = {
  hero: [
    {
      id: "shape-hero",
      name: "Shape Hero",
      desc: "Geometrische Shapes, Badge + Split-Title, Framer Motion",
      preview: `
        <div style="background:linear-gradient(135deg,#fefcff,#f0e8ff);height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:16px;position:relative;overflow:hidden">
          <div style="position:absolute;top:-20px;right:-20px;width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,rgba(124,58,237,0.4),rgba(244,114,182,0.3))"></div>
          <div style="position:absolute;bottom:-10px;left:-10px;width:50px;height:50px;border-radius:50%;background:linear-gradient(135deg,rgba(167,139,250,0.5),rgba(173,216,230,0.4))"></div>
          <div style="position:absolute;top:20px;left:16px;width:12px;height:12px;border-radius:3px;background:linear-gradient(135deg,#7c3aed,#a78bfa);transform:rotate(12deg)"></div>
          <div style="background:rgba(255,255,255,0.5);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.7);border-radius:20px;padding:3px 10px;font-size:10px;color:#7c3aed;font-weight:600;margin-bottom:8px">✦ Social Media Agency</div>
          <div style="font-size:18px;font-weight:900;color:#1a1a2e;text-align:center;line-height:1.1;margin-bottom:4px">Mehr Kunden durch</div>
          <div style="font-size:18px;font-weight:900;background:linear-gradient(135deg,#7c3aed,#f472b6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-align:center;margin-bottom:8px">Social Media.</div>
          <div style="font-size:9px;color:#64748b;text-align:center;margin-bottom:10px">Wir übernehmen LinkedIn & Instagram</div>
          <div style="display:flex;gap:6px">
            <div style="background:linear-gradient(135deg,rgba(124,58,237,0.85),rgba(167,139,250,0.85));backdrop-filter:blur(8px);border:1px solid rgba(167,139,250,0.4);color:white;padding:5px 10px;border-radius:10px;font-size:9px;font-weight:600">Starten →</div>
            <div style="background:rgba(255,255,255,0.4);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.6);color:#7c3aed;padding:5px 10px;border-radius:10px;font-size:9px;font-weight:600">Mehr erfahren</div>
          </div>
        </div>`
    },
    {
      id: "cinematic",
      name: "Cinematic Landing",
      desc: "Dramatisch, full-screen, kinoartige GSAP-Transitions",
      preview: `
        <div style="background:#0a0a0f;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:16px;position:relative;overflow:hidden">
          <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,rgba(124,58,237,0.15),transparent 70%)"></div>
          <div style="position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(124,58,237,0.5),transparent)"></div>
          <div style="font-size:8px;letter-spacing:0.3em;color:rgba(167,139,250,0.8);text-transform:uppercase;margin-bottom:12px">— NextGen Growth —</div>
          <div style="font-size:22px;font-weight:900;color:white;text-align:center;line-height:1;margin-bottom:6px;letter-spacing:-0.02em">DOMINATE<br/>SOCIAL MEDIA</div>
          <div style="width:40px;height:1px;background:linear-gradient(90deg,transparent,#a78bfa,transparent);margin:8px auto"></div>
          <div style="font-size:9px;color:rgba(255,255,255,0.4);text-align:center;margin-bottom:12px">LinkedIn & Instagram Marketing</div>
          <div style="border:1px solid rgba(124,58,237,0.5);color:rgba(167,139,250,0.9);padding:5px 14px;font-size:9px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase">DISCOVER</div>
        </div>`
    },
    {
      id: "gallery-scroll",
      name: "Gallery Scroll",
      desc: "Bento Grid, Scroll-Animationen, Indigo/Slate",
      preview: `
        <div style="background:#0f172a;height:100%;padding:10px;overflow:hidden">
          <div style="font-size:14px;font-weight:800;color:white;margin-bottom:6px">Your Animated Hero</div>
          <div style="font-size:8px;color:#94a3b8;margin-bottom:8px">Social Media Marketing</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;grid-template-rows:auto auto;gap:4px">
            <div style="background:linear-gradient(135deg,#312e81,#4f46e5);border-radius:8px;padding:8px;aspect-ratio:1">
              <div style="font-size:8px;color:white;font-weight:700">LinkedIn</div>
              <div style="font-size:7px;color:rgba(255,255,255,0.6);margin-top:2px">+240%</div>
            </div>
            <div style="background:linear-gradient(135deg,#1e1b4b,#3730a3);border-radius:8px;padding:8px;aspect-ratio:1">
              <div style="font-size:8px;color:white;font-weight:700">Instagram</div>
              <div style="font-size:7px;color:rgba(255,255,255,0.6);margin-top:2px">10K Reach</div>
            </div>
            <div style="background:linear-gradient(135deg,#4c1d95,#6d28d9);border-radius:8px;padding:8px;grid-column:span 2">
              <div style="font-size:8px;color:white;font-weight:700">Content Strategy</div>
            </div>
          </div>
        </div>`
    },
    {
      id: "container-scroll",
      name: "Container Scroll",
      desc: "3D Rotation beim Scrollen, minimalistisch (Aceternity)",
      preview: `
        <div style="background:#fff;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:12px;font-family:system-ui">
          <div style="font-size:11px;font-weight:600;color:#64748b;margin-bottom:4px;text-align:center">Die Zukunft deines</div>
          <div style="font-size:18px;font-weight:800;color:#0f172a;text-align:center;line-height:1;margin-bottom:10px">Social Marketings</div>
          <div style="width:100%;background:#0f172a;border-radius:10px;padding:10px;transform:perspective(400px) rotateX(8deg);transform-origin:bottom;box-shadow:0 20px 40px rgba(0,0,0,0.2)">
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px">
              <div style="background:#1e293b;border-radius:5px;height:30px"></div>
              <div style="background:#1e293b;border-radius:5px;height:30px"></div>
              <div style="background:#4f46e5;border-radius:5px;height:30px"></div>
              <div style="background:#1e293b;border-radius:5px;height:20px;grid-column:span 2"></div>
              <div style="background:#1e293b;border-radius:5px;height:20px"></div>
            </div>
          </div>
        </div>`
    },
    {
      id: "globe-hero",
      name: "Globe Hero",
      desc: "Dark SaaS, 3D Globe, Glow-Effekte, Bold Typography",
      preview: `
        <div style="background:#060612;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:12px;position:relative;overflow:hidden">
          <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 70%,rgba(99,102,241,0.2),transparent 60%)"></div>
          <div style="width:80px;height:80px;border-radius:50%;border:1px solid rgba(99,102,241,0.3);position:relative;margin-bottom:12px">
            <div style="position:absolute;inset:8px;border-radius:50%;border:1px solid rgba(99,102,241,0.2)"></div>
            <div style="position:absolute;inset:0;border-radius:50%;background:radial-gradient(ellipse at 40% 40%,rgba(99,102,241,0.4),rgba(6,6,18,0.8))"></div>
            <div style="position:absolute;top:50%;left:0;right:0;height:1px;background:rgba(99,102,241,0.3);transform:translateY(-50%)"></div>
          </div>
          <div style="font-size:7px;letter-spacing:0.2em;color:rgba(99,102,241,0.8);text-transform:uppercase;margin-bottom:6px">GLOBAL NETWORK</div>
          <div style="font-size:16px;font-weight:900;color:white;text-align:center;letter-spacing:-0.03em;line-height:1;margin-bottom:8px">Connect<br/><span style="background:linear-gradient(135deg,#818cf8,#c084fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent">Everything.</span></div>
          <div style="display:flex;gap:5px">
            <div style="background:rgba(99,102,241,0.85);backdrop-filter:blur(8px);color:white;padding:4px 10px;border-radius:8px;font-size:8px;font-weight:600">Get Started</div>
            <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:rgba(255,255,255,0.7);padding:4px 10px;border-radius:8px;font-size:8px">Learn more</div>
          </div>
        </div>`
    },
  ],
  background: [
    {
      id: "dream-sky",
      name: "Dream Sky Glow",
      desc: "Light Mode, Cream #fefcff, sanfte Rosa+Blau-Gradienten",
      preview: `
        <div style="height:100%;position:relative;background:#fefcff">
          <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 30% 70%,rgba(173,216,230,0.5),transparent 60%)"></div>
          <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 70% 30%,rgba(255,182,193,0.55),transparent 60%)"></div>
          <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:12px">
            <div style="font-size:10px;font-weight:700;color:#1a1a2e;margin-bottom:4px">Soft & Ethereal</div>
            <div style="font-size:8px;color:#64748b">Light Mode · Baby-Blau · Rosa</div>
          </div>
        </div>`
    },
    {
      id: "grid-glow",
      name: "Grid Glow BG",
      desc: "Dark Mode, Canvas-animierte Glow-Blobs, futuristisch",
      preview: `
        <div style="height:100%;position:relative;background:#080814;overflow:hidden">
          <div style="position:absolute;top:20%;left:30%;width:60px;height:60px;border-radius:50%;background:rgba(124,58,237,0.3);filter:blur(20px);animation:pulse 3s ease-in-out infinite"></div>
          <div style="position:absolute;bottom:20%;right:20%;width:80px;height:80px;border-radius:50%;background:rgba(167,139,250,0.2);filter:blur(25px);animation:pulse 4s ease-in-out infinite reverse"></div>
          <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:12px">
            <div style="font-size:10px;font-weight:700;color:rgba(255,255,255,0.9);margin-bottom:4px">Grid Glow</div>
            <div style="font-size:8px;color:rgba(255,255,255,0.4)">Dark · Driftende Blobs</div>
          </div>
          <style>@keyframes pulse{0%,100%{opacity:0.6;transform:scale(1)}50%{opacity:1;transform:scale(1.2)}}</style>
        </div>`
    },
    {
      id: "webgl-shader",
      name: "WebGL Shader",
      desc: "Three.js Wave Distortion, Charcoal + Green",
      preview: `
        <div style="height:100%;position:relative;background:#27272a;overflow:hidden">
          <div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(34,197,94,0.03) 2px,rgba(34,197,94,0.03) 4px)"></div>
          <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,rgba(34,197,94,0.12),transparent 60%)"></div>
          <svg style="position:absolute;inset:0;width:100%;height:100%;opacity:0.15" viewBox="0 0 200 200">
            <path d="M0,100 Q50,60 100,100 Q150,140 200,100" stroke="#22c55e" stroke-width="1.5" fill="none"/>
            <path d="M0,110 Q50,70 100,110 Q150,150 200,110" stroke="#22c55e" stroke-width="1" fill="none"/>
            <path d="M0,90 Q50,50 100,90 Q150,130 200,90" stroke="#22c55e" stroke-width="0.8" fill="none"/>
          </svg>
          <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:12px">
            <div style="font-size:10px;font-weight:800;color:white;letter-spacing:-0.03em">Wave Shader</div>
            <div style="font-size:8px;color:rgba(34,197,94,0.8);margin-top:2px">Three.js · WebGL</div>
          </div>
        </div>`
    },
    {
      id: "shader-lines",
      name: "Shader Lines",
      desc: "WebGL Mosaic-Linien, bunt & colorful, text overlay",
      preview: `
        <div style="height:100%;position:relative;background:#111;overflow:hidden;border-radius:inherit">
          <div style="position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 50% 50%,#f472b620 0deg,#7c3aed20 30deg,#06b6d420 60deg,#f59e0b20 90deg,#f472b620 120deg);opacity:0.8"></div>
          <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:12px">
            <div style="font-size:13px;font-weight:700;color:white;letter-spacing:-0.04em;text-align:center">Colorful<br/>Mosaic</div>
            <div style="font-size:7px;color:rgba(255,255,255,0.5);margin-top:4px">WebGL · Three.js</div>
          </div>
        </div>`
    },
  ],
  buttons: [
    {
      id: "liquid-glass",
      name: "Liquid Glass",
      desc: "macOS Dock-inspiriert, flüssiger Glaseffekt, dynamisch",
      preview: `
        <div style="height:100%;background:linear-gradient(135deg,#e0e7ff,#fce7f3);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;padding:12px">
          <div style="background:rgba(255,255,255,0.3);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.6);box-shadow:0 4px 16px rgba(124,58,237,0.1),inset 0 1px 0 rgba(255,255,255,0.7);color:#7c3aed;padding:7px 16px;border-radius:12px;font-size:10px;font-weight:600">Mehr erfahren</div>
          <div style="background:linear-gradient(135deg,rgba(124,58,237,0.85),rgba(167,139,250,0.85));backdrop-filter:blur(12px);border:1px solid rgba(167,139,250,0.4);box-shadow:0 4px 16px rgba(124,58,237,0.3);color:white;padding:7px 16px;border-radius:12px;font-size:10px;font-weight:600">Jetzt starten →</div>
          <div style="background:rgba(255,255,255,0.2);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.5);color:#374151;padding:5px 12px;border-radius:20px;font-size:9px;font-weight:500">Ghost Button</div>
        </div>`
    },
    {
      id: "glass-button",
      name: "Glass Button",
      desc: "Glassmorphism + Dotted Grid, OKLCH, CVA-Varianten",
      preview: `
        <div style="height:100%;position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;padding:12px;background:#f8fafc">
          <svg style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none;opacity:0.4" xmlns="http://www.w3.org/2000/svg">
            <defs><pattern id="dots" x="0" y="0" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="0.8" fill="rgba(100,116,139,0.4)"/></pattern></defs>
            <rect width="100%" height="100%" fill="url(#dots)"/>
          </svg>
          <div style="position:relative;background:rgba(255,255,255,0.6);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.8);box-shadow:0 2px 8px rgba(0,0,0,0.08);color:#334155;padding:5px 12px;border-radius:10px;font-size:9px;font-weight:600">Small</div>
          <div style="position:relative;background:rgba(255,255,255,0.6);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.8);box-shadow:0 2px 8px rgba(0,0,0,0.08);color:#334155;padding:7px 16px;border-radius:10px;font-size:10px;font-weight:600">Default</div>
          <div style="position:relative;background:rgba(255,255,255,0.6);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.8);box-shadow:0 2px 8px rgba(0,0,0,0.08);color:#334155;padding:9px 20px;border-radius:12px;font-size:11px;font-weight:600">Large</div>
        </div>`
    },
  ],
  cards: [
    {
      id: "glassy-pricing",
      name: "Glassy Pricing",
      desc: "Glassmorphism Cards, Cyan/Violet Akzente, 3-Tier",
      preview: `
        <div style="height:100%;background:linear-gradient(135deg,#fefcff,#f3e8ff);padding:8px;display:flex;gap:5px;align-items:center">
          <div style="flex:1;background:rgba(255,255,255,0.55);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.8);border-radius:12px;padding:8px">
            <div style="font-size:8px;font-weight:700;color:#1a1a2e;margin-bottom:2px">Starter</div>
            <div style="font-size:12px;font-weight:900;color:#1a1a2e">890€</div>
            <div style="font-size:7px;color:#64748b">/Monat</div>
          </div>
          <div style="flex:1;background:linear-gradient(135deg,rgba(124,58,237,0.08),rgba(244,114,182,0.06));backdrop-filter:blur(12px);border:1.5px solid rgba(124,58,237,0.28);border-radius:12px;padding:8px;transform:scale(1.05)">
            <div style="font-size:6px;color:#7c3aed;font-weight:700;text-transform:uppercase;margin-bottom:1px">Beliebt</div>
            <div style="font-size:8px;font-weight:700;color:#1a1a2e;margin-bottom:2px">Growth</div>
            <div style="font-size:12px;font-weight:900;color:#7c3aed">1.490€</div>
            <div style="font-size:7px;color:#64748b">/Monat</div>
          </div>
          <div style="flex:1;background:rgba(255,255,255,0.55);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.8);border-radius:12px;padding:8px">
            <div style="font-size:8px;font-weight:700;color:#1a1a2e;margin-bottom:2px">Pro</div>
            <div style="font-size:12px;font-weight:900;color:#1a1a2e">2.490€</div>
            <div style="font-size:7px;color:#64748b">/Monat</div>
          </div>
        </div>`
    },
    {
      id: "gradient-bold-card",
      name: "Gradient Bold Card",
      desc: "Animierter Glow-Border, Glassmorphism, premium",
      preview: `
        <div style="height:100%;background:#f8fafc;display:flex;align-items:center;justify-content:center;padding:12px">
          <div style="position:relative;border-radius:16px;padding:2px;background:linear-gradient(135deg,#7c3aed,#f472b6,#7c3aed,#06b6d4);background-size:300% 300%;animation:borderspin 3s linear infinite;width:100%">
            <div style="background:rgba(255,255,255,0.9);backdrop-filter:blur(16px);border-radius:14px;padding:12px">
              <div style="font-size:8px;font-weight:700;color:#7c3aed;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px">Featured</div>
              <div style="font-size:11px;font-weight:800;color:#0f172a;margin-bottom:4px">LinkedIn Strategie</div>
              <div style="font-size:8px;color:#64748b">Professionelle Positionierung</div>
            </div>
          </div>
          <style>@keyframes borderspin{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}</style>
        </div>`
    },
  ],
};

type CategoryKey = keyof typeof STYLE_CATALOG;
const CATEGORIES: { key: CategoryKey; label: string; icon: string }[] = [
  { key: "hero", label: "Hero Section", icon: "🎯" },
  { key: "background", label: "Hintergrund", icon: "🌅" },
  { key: "buttons", label: "Buttons", icon: "🔘" },
  { key: "cards", label: "Cards & Pricing", icon: "💳" },
];

interface UploadedAsset { name: string; data: string; type: "logo" | "reference"; }

export default function DesignerPicker() {
  const [selected, setSelected] = useState<Record<string, string>>({});
  const [activeCategory, setActiveCategory] = useState<CategoryKey>("hero");
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [assets, setAssets] = useState<UploadedAsset[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploadType, setUploadType] = useState<"logo" | "reference">("reference");

  const allSelected = CATEGORIES.every((c) => selected[c.key]);

  // Resolve selected IDs → display names for the config
  function resolveStyleName(category: CategoryKey, id: string): string {
    return STYLE_CATALOG[category].find(s => s.id === id)?.name ?? id;
  }

  async function handleSave() {
    if (!allSelected) return;
    setSaving(true);
    const config = {
      version: "1.0",
      lastUpdated: new Date().toISOString().split("T")[0],
      styles: {
        hero: resolveStyleName("hero", selected.hero),
        background: resolveStyleName("background", selected.background),
        buttons: resolveStyleName("buttons", selected.buttons),
        cards: resolveStyleName("cards", selected.cards),
      },
      globalPalette: {
        mode: selected.background === "dream-sky" || selected.background === "grid-glow" ? "light" : "dark",
        primaryAccent: "violet-600",
        secondaryAccent: "pink-400",
      },
      sourceLinks: {
        "Shape Hero": "https://21st.dev/community/components/kokonutd/shape-landing-hero/default",
        "Globe Hero": "https://21st.dev/community/components/chow-stack/globe-hero/default",
        "Cinematic Landing": "https://21st.dev/community/components/easemize/cinematic-landing-hero/default",
        "Gallery Scroll": "https://21st.dev/community/components/YoucefBnm/hero-gallery-scroll-animation/default",
        "Container Scroll": "https://21st.dev/community/components/aceternity/container-scroll-animation/default",
        "Dream Sky Glow": "https://21st.dev/community/components/meghtrix/background-gradient-glow/dream-sky-pink-glow",
        "Grid Glow BG": "https://21st.dev/community/components/dhiluxui/grid-glow-background/default",
        "WebGL Shader": "https://21st.dev/community/components/aliimam/web-gl-shader/default",
        "Shader Lines": "https://21st.dev/community/components/aliimam/shader-lines/default",
        "Liquid Glass": "https://21st.dev/community/components/suraj-xd/liquid-glass/default",
        "Glass Button": "https://21st.dev/community/components/easemize/glass-button/default",
        "Glassy Pricing": "https://21st.dev/community/components/easemize/animated-glassy-pricing/default",
        "Gradient Bold Card": "https://21st.dev/community/components/ruixenui/gradient-bold-card/default",
      },
    };
    await fetch("/api/designer-save", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...config, assets }),
    });
    setSaving(false);
    setSaved(true);
  }

  const currentStyles = STYLE_CATALOG[activeCategory];

  return (
    <div style={{ minHeight: "100vh", background: "#fafafa", fontFamily: "system-ui, -apple-system, sans-serif" }}>
      {/* Header */}
      <div style={{ background: "white", borderBottom: "1px solid #e2e8f0", padding: "16px 24px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "2px" }}>
            <div style={{ width: "24px", height: "24px", borderRadius: "6px", background: "linear-gradient(135deg,#7c3aed,#f472b6)", display: "flex", alignItems: "center", justifyContent: "center", color: "white", fontSize: "12px", fontWeight: "900" }}>N</div>
            <span style={{ fontWeight: "800", fontSize: "16px", color: "#0f172a" }}>Designer</span>
            <span style={{ fontSize: "10px", background: "#f3e8ff", color: "#7c3aed", padding: "2px 8px", borderRadius: "20px", fontWeight: "600" }}>VISUAL PICKER</span>
          </div>
          <div style={{ fontSize: "12px", color: "#64748b" }}>Wähle einen Stil pro Kategorie — klicke zum Auswählen, dann bestätige unten.</div>
        </div>
        <button
          onClick={handleSave}
          disabled={!allSelected || saving || saved}
          style={{
            background: allSelected && !saved ? "linear-gradient(135deg,#7c3aed,#a855f7)" : saved ? "#10b981" : "#e2e8f0",
            color: allSelected || saved ? "white" : "#94a3b8",
            border: "none",
            padding: "10px 24px",
            borderRadius: "12px",
            fontWeight: "700",
            fontSize: "13px",
            cursor: allSelected && !saved ? "pointer" : "default",
            transition: "all 0.2s",
            boxShadow: allSelected && !saved ? "0 4px 16px rgba(124,58,237,0.3)" : "none",
          }}
        >
          {saved ? "✓ Design gespeichert!" : saving ? "Speichern..." : allSelected ? "Design anwenden →" : `Noch ${CATEGORIES.filter(c => !selected[c.key]).length} ausstehend`}
        </button>
      </div>

      {saved ? (
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: "60vh", gap: "16px" }}>
          <div style={{ fontSize: "64px" }}>🎨</div>
          <div style={{ fontSize: "24px", fontWeight: "800", color: "#0f172a" }}>Design gespeichert!</div>
          <div style={{ fontSize: "14px", color: "#64748b", textAlign: "center", maxWidth: "400px" }}>
            Deine Auswahl wurde in <code style={{ background: "#f1f5f9", padding: "2px 6px", borderRadius: "4px" }}>.designer-config.json</code> gespeichert.<br />
            Claude wendet die Stile jetzt auf dein Projekt an.
          </div>
          <div style={{ background: "#f0fdf4", border: "1px solid #bbf7d0", borderRadius: "12px", padding: "12px 20px", marginTop: "8px" }}>
            <div style={{ fontSize: "12px", color: "#166534", fontWeight: "600" }}>Du kannst diesen Tab schließen — Claude übernimmt ab hier.</div>
          </div>
        </div>
      ) : (
        <div style={{ display: "flex", height: "calc(100vh - 73px)" }}>
          {/* Left: Category nav + selection summary */}
          <div style={{ width: "220px", borderRight: "1px solid #e2e8f0", background: "white", padding: "16px", display: "flex", flexDirection: "column", gap: "6px", flexShrink: 0 }}>
            <div style={{ fontSize: "10px", fontWeight: "700", color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "4px" }}>Kategorien</div>
            {CATEGORIES.map((cat) => (
              <button
                key={cat.key}
                onClick={() => setActiveCategory(cat.key)}
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  gap: "8px",
                  padding: "10px 12px",
                  borderRadius: "10px",
                  border: "none",
                  background: activeCategory === cat.key ? "#f3e8ff" : "transparent",
                  color: activeCategory === cat.key ? "#7c3aed" : "#374151",
                  fontWeight: activeCategory === cat.key ? "700" : "500",
                  fontSize: "13px",
                  cursor: "pointer",
                  textAlign: "left",
                  transition: "all 0.15s",
                }}
              >
                <span>{cat.icon} {cat.label}</span>
                {selected[cat.key] && <span style={{ fontSize: "14px" }}>✓</span>}
              </button>
            ))}

            {/* Summary */}
            {Object.keys(selected).length > 0 && (
              <div style={{ marginTop: "16px", padding: "12px", background: "#f8fafc", borderRadius: "10px", border: "1px solid #e2e8f0" }}>
                <div style={{ fontSize: "10px", fontWeight: "700", color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "8px" }}>Auswahl</div>
                {Object.entries(selected).map(([key, val]) => {
                  const cat = CATEGORIES.find(c => c.key === key);
                  const styles = STYLE_CATALOG[key as CategoryKey];
                  const style = styles?.find(s => s.id === val);
                  return (
                    <div key={key} style={{ marginBottom: "6px" }}>
                      <div style={{ fontSize: "9px", color: "#94a3b8" }}>{cat?.label}</div>
                      <div style={{ fontSize: "11px", fontWeight: "600", color: "#0f172a" }}>{style?.name}</div>
                    </div>
                  );
                })}
              </div>
            )}

            {/* Asset Upload */}
            <div style={{ marginTop: "16px" }}>
              <div style={{ fontSize: "10px", fontWeight: "700", color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "8px" }}>📎 Assets</div>
              <input ref={fileInputRef} type="file" accept="image/*" multiple style={{ display: "none" }}
                onChange={(e) => {
                  Array.from(e.target.files ?? []).slice(0, 6 - assets.length).forEach((file) => {
                    const reader = new FileReader();
                    reader.onload = (ev) => setAssets(prev => [...prev, { name: file.name, data: ev.target?.result as string, type: uploadType }]);
                    reader.readAsDataURL(file);
                  });
                  e.target.value = "";
                }}
              />
              <div style={{ display: "flex", gap: "6px", marginBottom: "8px" }}>
                {(["logo", "reference"] as const).map((t) => (
                  <button key={t} onClick={() => setUploadType(t)} style={{
                    flex: 1, padding: "5px 0", borderRadius: "7px", border: "none", cursor: "pointer", fontSize: "10px", fontWeight: "600",
                    background: uploadType === t ? "#ede9fe" : "#f1f5f9", color: uploadType === t ? "#7c3aed" : "#64748b",
                  }}>{t === "logo" ? "🏷 Logo" : "🖼 Referenz"}</button>
                ))}
              </div>
              <button onClick={() => fileInputRef.current?.click()} style={{
                width: "100%", padding: "10px", borderRadius: "10px", border: "2px dashed #e2e8f0",
                background: "#fafafa", color: "#94a3b8", fontSize: "11px", cursor: "pointer", fontWeight: "500",
              }}>+ Bild hochladen</button>
              {assets.length > 0 && (
                <div style={{ display: "flex", flexWrap: "wrap", gap: "6px", marginTop: "8px" }}>
                  {assets.map((a, i) => (
                    <div key={i} style={{ position: "relative" }}>
                      <img src={a.data} alt={a.name} style={{ width: "48px", height: "48px", objectFit: "cover", borderRadius: "8px", border: a.type === "logo" ? "2px solid #7c3aed" : "2px solid #e2e8f0" }} />
                      <div style={{ position: "absolute", top: "-4px", left: "-4px", fontSize: "8px", background: a.type === "logo" ? "#7c3aed" : "#64748b", color: "white", borderRadius: "4px", padding: "1px 3px" }}>{a.type === "logo" ? "L" : "R"}</div>
                      <button onClick={() => setAssets(prev => prev.filter((_, j) => j !== i))} style={{ position: "absolute", top: "-5px", right: "-5px", width: "14px", height: "14px", borderRadius: "50%", background: "#ef4444", border: "none", color: "white", fontSize: "9px", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center" }}>×</button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Right: Style grid */}
          <div style={{ flex: 1, padding: "20px", overflowY: "auto" }}>
            <div style={{ marginBottom: "16px" }}>
              <div style={{ fontSize: "18px", fontWeight: "800", color: "#0f172a" }}>
                {CATEGORIES.find(c => c.key === activeCategory)?.icon} {CATEGORIES.find(c => c.key === activeCategory)?.label}
              </div>
              <div style={{ fontSize: "12px", color: "#64748b", marginTop: "2px" }}>Klicke auf einen Stil um ihn auszuwählen</div>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: "14px" }}>
              {currentStyles.map((style) => {
                const isSelected = selected[activeCategory] === style.id;
                return (
                  <div
                    key={style.id}
                    onClick={() => setSelected(prev => ({ ...prev, [activeCategory]: style.id }))}
                    style={{
                      border: isSelected ? "2.5px solid #7c3aed" : "2px solid #e2e8f0",
                      borderRadius: "16px",
                      overflow: "hidden",
                      cursor: "pointer",
                      transition: "all 0.2s cubic-bezier(0.34,1.56,0.64,1)",
                      transform: isSelected ? "scale(1.02)" : "scale(1)",
                      boxShadow: isSelected ? "0 8px 24px rgba(124,58,237,0.2)" : "0 2px 8px rgba(0,0,0,0.06)",
                      background: "white",
                    }}
                  >
                    {/* Live Preview */}
                    <div
                      style={{ height: "180px", overflow: "hidden" }}
                      dangerouslySetInnerHTML={{ __html: style.preview }}
                    />
                    {/* Label */}
                    <div style={{ padding: "10px 12px", borderTop: isSelected ? "1px solid rgba(124,58,237,0.15)" : "1px solid #f1f5f9", background: isSelected ? "#faf5ff" : "white" }}>
                      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                        <div style={{ fontWeight: "700", fontSize: "13px", color: isSelected ? "#7c3aed" : "#0f172a" }}>{style.name}</div>
                        {isSelected && <div style={{ width: "18px", height: "18px", borderRadius: "50%", background: "#7c3aed", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "10px", color: "white" }}>✓</div>}
                      </div>
                      <div style={{ fontSize: "11px", color: "#64748b", marginTop: "2px", lineHeight: "1.4" }}>{style.desc}</div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

#### Für andere Projekte (Vite, vanilla):

Generiere eine `designer-picker.html` Datei mit identischer Logik als self-contained HTML. Starte einen lokalen Python-Server:
```bash
python3 -m http.server 3001 &
open http://localhost:3001/designer-picker.html
```

---

### Schritt 4: Browser öffnen und aktiv pollen

```bash
open http://localhost:[PORT]/designer-picker
```

**WICHTIG: Direkt danach diesen Poll-Loop ausführen und warten bis CONFIG_FOUND erscheint:**

```bash
echo "Warte auf Design-Auswahl im Browser..." && \
for i in $(seq 1 60); do
  if [ -f .designer-config.json ]; then
    echo "CONFIG_FOUND"
    cat .designer-config.json
    break
  fi
  echo "Warte... ($i/60)"
  sleep 5
done
```

**Sobald CONFIG_FOUND erscheint:** Config lesen, sofort mit Schritt 5 weitermachen — NICHT auf weitere User-Eingabe warten. Der User hat im Browser bestätigt, das ist sein Signal zum Weitermachen.

Falls die Config ein `"assets"` Array enthält: jedes Asset mit dem Read-Tool öffnen bevor mit der Implementation begonnen wird. `type: "logo"` → im Projekt als Logo verwenden (Navbar, Favicon etc.); `type: "reference"` → als Design-Referenz für Farben, Stil, Layout nutzen.

---

### Schritt 5: Temporäre Dateien aufräumen

```bash
rm -rf app/designer-picker app/api/designer-save
```

---

### Schritt 6: Kohärenz-Check & Implementation

Identische Logik wie vorher: Dependencies installieren, Komponenten bauen, Stile anwenden.

---

## Stil-Katalog (vollständige Referenz)

### 1. Globe Hero
- **URL:** https://21st.dev/community/components/chow-stack/globe-hero/default
- **Aesthetic:** Dark SaaS, 3D Globe als Centerpiece, Glow-Effekte, text-8xl bis text-9xl font-black
- **Tech:** Framer Motion, React Three Fiber

### 2. Glowing Search Bar
- **URL:** https://21st.dev/community/components/thanh/animated-glowing-search-bar/default
- **Aesthetic:** Animierter Glow auf Inputs, clean minimal

### 3. Cinematic Landing
- **URL:** https://21st.dev/community/components/easemize/cinematic-landing-hero/default
- **Aesthetic:** Dramatisch, full-screen, GSAP-Transitions
- **Tech:** GSAP

### 4. Gallery Scroll
- **URL:** https://21st.dev/community/components/YoucefBnm/hero-gallery-scroll-animation/default
- **Aesthetic:** Bento Grid, Indigo/Slate, Scroll-triggered
- **Tech:** Framer Motion, ContainerScroll, BentoGrid

### 5. Expand Map
- **URL:** https://21st.dev/community/components/jatin-yadav05/expand-map/default
- **Aesthetic:** Minimalistisch, Emerald, tracking-[0.2em] uppercase

### 6. Glass Calendar
- **URL:** https://21st.dev/community/components/ravikatiyar/glass-calendar/default
- **Aesthetic:** Glassmorphism Kalender, Slate-900
- **Tech:** Framer Motion, date-fns

### 7. Liquid Glass
- **URL:** https://21st.dev/community/components/suraj-xd/liquid-glass/default
- **Aesthetic:** macOS Dock, flüssiger Glaseffekt, Backdrop-Filter

### 8. Glass Button
- **URL:** https://21st.dev/community/components/easemize/glass-button/default
- **Aesthetic:** Dotted SVG Grid, OKLCH, CVA-Varianten sm/default/lg/icon

### 9. Glassy Pricing
- **URL:** https://21st.dev/community/components/easemize/animated-glassy-pricing/default
- **Aesthetic:** Glassmorphism Cards, Cyan-400, Dark Base

### 10. Grid Glow BG
- **URL:** https://21st.dev/community/components/dhiluxui/grid-glow-background/default
- **Aesthetic:** Canvas-animierte Glow-Blobs, Dark/White, Framer Motion Stagger

### 11. Shader Lines
- **URL:** https://21st.dev/community/components/aliimam/shader-lines/default
- **Aesthetic:** WebGL Mosaic-Linien, colorful, Three.js

### 12. Dream Sky Glow
- **URL:** https://21st.dev/community/components/meghtrix/background-gradient-glow/dream-sky-pink-glow
- **Aesthetic:** Light #fefcff, Baby-Blau rgba(173,216,230,0.35) + Rosa rgba(255,182,193,0.4)

### 13. Glowing Bar Chart
- **URL:** https://21st.dev/community/components/svg-ui/bar-chart/glowing-bar-chart
- **Aesthetic:** Recharts + SVG feGaussianBlur stdDeviation="10"

### 14. WebGL Shader
- **URL:** https://21st.dev/community/components/aliimam/web-gl-shader/default
- **Aesthetic:** Three.js Wave, #27272a + #22c55e, animate-ping

### 15. Gradient Bold Card
- **URL:** https://21st.dev/community/components/ruixenui/gradient-bold-card/default
- **Aesthetic:** Animierter Gradient-Border, CSS background-size:300% animation

### 16. Warp Dialog
- **URL:** https://21st.dev/community/components/molecule-ui/warp-dialog/default
- **Aesthetic:** 3D Warp, Spring Physics, WarpDialog/WarpDialogTrigger/WarpDialogContent

### 17. Container Scroll
- **URL:** https://21st.dev/community/components/aceternity/container-scroll-animation/default
- **Aesthetic:** 3D rotate on scroll, ContainerScroll wrapper, Aceternity

### 18. Shape Hero
- **URL:** https://21st.dev/community/components/kokonutd/shape-landing-hero/default
- **Aesthetic:** Geometrische Shapes, Badge + Split-Title, HeroGeometric props: badge/title1/title2

---

---

## Annotation-Tool (Design-Feedback lesen)

Der User kann mit einem Zeichenstift direkt im Localhost auf der Seite markieren und einen Kommentar schicken. Claude liest diese Annotationen automatisch — entweder einmalig oder im aktiven Watch-Modus.

---

### Watch-Modus — automatisch auf Feedback warten (`/designer watch`)

Wenn der User `/designer watch` tippt oder sagt er will nicht mehr gefragt werden: **Starte den Watch-Modus.**

#### Schritt 1: Watcher-Script im Hintergrund starten

```bash
mkdir -p design-feedback/done
```

Dann dieses Script mit `run_in_background: true` starten:

```bash
mkdir -p design-feedback/done
while true; do
  for f in design-feedback/*.json; do
    [ -f "$f" ] || continue
    slug=$(basename "$f" .json)
    if [ ! -f "design-feedback/done/${slug}.json" ]; then
      echo "NEW_FEEDBACK:${f}"
      sleep 1
    fi
  done
  sleep 3
done
```

#### Schritt 2: Monitor-Tool auf den Prozess richten

Überwache den Background-Prozess mit dem **Monitor**-Tool (es streamt jede stdout-Zeile als Notification).

Sage dem User sofort:
> ✏️ **Watch-Modus aktiv.** Zeichne direkt im Browser und klicke „An Claude senden" — ich reagiere sofort.

#### Schritt 3: Bei `NEW_FEEDBACK:` sofort reagieren

Sobald Monitor die Zeile `NEW_FEEDBACK:design-feedback/XXXX.json` zeigt:

**a) JSON lesen:**
```bash
cat design-feedback/XXXX.json
```

**b) Screenshot-PNG lesen** — Read-Tool mit dem Pfad aus `"screenshot"` im JSON. Das Bild zeigt die Seite + Zeichnungen des Users direkt.

**c) Änderungen sofort umsetzen** — kein Rückfragen, direkt die markierten Stellen bearbeiten.

**d) Als erledigt markieren** (damit der Watcher sie nicht nochmal meldet):
```bash
slug="XXXX"  # den echten Slug einsetzen
cp "design-feedback/${slug}.json" "design-feedback/done/${slug}.json"
```

**e) Kurze Bestätigung** was geändert wurde — 1-2 Sätze.

**f) Weiter watchen** — der Background-Prozess läuft, Monitor überwacht weiter. Kein Neustart nötig.

---

### Einmaliges Feedback prüfen (ohne Watch-Modus)

```bash
ls design-feedback/*.json 2>/dev/null | grep -v "/done/" | sort -r | head -5
```

Falls Dateien vorhanden:
```bash
cat $(ls design-feedback/*.json 2>/dev/null | grep -v "/done/" | sort -r | head -1)
```

Dann die zugehörige PNG-Datei lesen (Pfad steht im JSON unter `"screenshot"`). Claude sieht das Bild mit den Zeichnungen direkt als multimodales Bild.

**Was tun mit dem Feedback:**
1. Screenshot-Bild ansehen (Read-Tool mit dem PNG-Pfad aus `"screenshot"`)
2. Kommentar aus JSON lesen
3. **Referenz-Bilder lesen** — falls `"references"` im JSON vorhanden (Array mit `{ name, path }`): jedes Bild mit dem Read-Tool öffnen. Diese Bilder sind Logos, Design-Referenzen oder Assets die der User hochgeladen hat
4. Die markierten/kommentierten Stellen + Referenz-Bilder zusammen interpretieren
5. Änderungen sofort umsetzen ohne weitere Rückfragen
6. Datei nach `design-feedback/done/` verschieben

### Annotation-Widget in neue Projekte injizieren

Wenn ein neues Projekt in Next.js App Router aufgebaut wird, diese drei Dinge immer hinzufügen:

**1. html2canvas installieren:**
```bash
npm install html2canvas
```

**2. API Route** — `app/api/design-feedback/route.ts` erstellen:
```typescript
import { NextResponse } from "next/server";
import { writeFileSync, mkdirSync, existsSync } from "fs";
import { join } from "path";

export async function POST(request: Request) {
  const { screenshot, comment, page, timestamp } = await request.json();
  const dir = join(process.cwd(), "design-feedback");
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  const slug = new Date(timestamp).toISOString().replace(/[:.]/g, "-").slice(0, 19);
  if (screenshot) {
    const base64Data = screenshot.replace(/^data:image\/png;base64,/, "");
    writeFileSync(join(dir, `${slug}.png`), Buffer.from(base64Data, "base64"));
  }
  writeFileSync(join(dir, `${slug}.json`),
    JSON.stringify({ timestamp, page, comment, screenshot: `design-feedback/${slug}.png` }, null, 2));
  return NextResponse.json({ success: true, slug });
}
```

**3. Widget-Komponente** — `components/design-feedback.tsx` mit vollem Canvas-Tool erstellen (Stift, Radierer, 5 Farben, 3 Strichstärken, Textarea-Kommentar, Screenshot via html2canvas, POST an API).

**4. In `app/layout.tsx`** einbinden:
```tsx
import { DesignFeedback } from "@/components/design-feedback";
// In <body>: <DesignFeedback />
```

---

## Wichtige Regeln

- **Niemals AskUserQuestion für Design-Entscheidungen** — immer den visuellen Picker generieren
- **Picker zuerst öffnen, dann warten** — nicht weiter machen bis Config gespeichert ist
- **Picker-Dateien nach Auswahl löschen** — `app/designer-picker/` und `app/api/designer-save/` entfernen
- **Source-Code von 21st.dev** — immer per WebFetch holen wenn verfügbar
- **Stil ist bindend** — bis `/designer` erneut aufgerufen wird
- **Design-Feedback immer prüfen** — beim Start jeder Design-Session `design-feedback/` auf neue Annotationen prüfen
