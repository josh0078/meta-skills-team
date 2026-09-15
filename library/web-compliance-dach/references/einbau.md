# Modul D — Technischer Einbau

---

## D1 — Wohin die Dateien gehören

Stack aus dem Projekt erkennen, dann passend anlegen:

| Stack | Dateien | Footer-Link |
|---|---|---|
| Statisches HTML | `impressum.html`, `datenschutz.html` im Root | in jede `.html` einfügen |
| Next.js App Router | `app/impressum/page.tsx`, `app/datenschutz/page.tsx` | `components/Footer.tsx` |
| Next.js Pages Router | `pages/impressum.tsx`, `pages/datenschutz.tsx` | `components/Footer.tsx` |
| Astro | `src/pages/impressum.astro`, `src/pages/datenschutz.astro` | `src/layouts/*.astro` |
| Vite/React SPA | `src/pages/Impressum.tsx` + Routen | Layout-Komponente |
| WordPress | zwei Seiten + Footer-Menü | Customizer → Menüs |
| Webflow | zwei statische Seiten, HTML-Embed für den Text | globaler Footer-Symbolblock |

Immer prüfen: existiert schon eine Legal-Seite? Dann **aktualisieren**, nicht zweite Datei danebenlegen.

Next.js Beispiel-Metadaten:
```tsx
export const metadata = {
  title: "Impressum | {{SITE}}",
  robots: { index: true, follow: false },
};
```

## D2 — Footer-Link

```html
<footer class="site-footer">
  <nav class="footer-legal" aria-label="Rechtliches">
    <a href="/impressum">Impressum</a>
    <a href="/datenschutz">Datenschutzerklärung</a>
    <button type="button" data-cc-open>Cookie-Einstellungen</button>
  </nav>
</footer>
```
- Wörtlich „Impressum" und „Datenschutzerklärung".
- Auf **jeder** Seite, inklusive Landingpages, Danke-Seiten und 404.
- Der „Cookie-Einstellungen"-Button ist Pflicht, sobald ein Banner existiert — der Widerruf muss so einfach sein wie die Erteilung.

## D3 — Google Fonts lokalisieren

**Vorher (Problem):**
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
```

**Weg A — Next.js (eingebaut, überträgt nichts an Google zur Laufzeit):**
```tsx
import { Inter } from "next/font/google";
const inter = Inter({ subsets: ["latin"], display: "swap", variable: "--font-inter" });
// <html className={inter.variable}>
```

**Weg B — Fontsource (jeder Bundler):**
```bash
npm i @fontsource-variable/inter
```
```ts
import "@fontsource-variable/inter";
```

**Weg C — statisches HTML, Dateien selbst hosten:**
```bash
# woff2 herunterladen (z. B. via google-webfonts-helper), nach /fonts legen
```
```css
@font-face {
  font-family: "Inter";
  src: url("/fonts/inter-v13-latin-regular.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
```

Danach kontrollieren, dass **keine** Anfrage mehr rausgeht:
```bash
grep -rn "fonts.googleapis.com\|fonts.gstatic.com\|use.fontawesome.com\|kit.fontawesome.com" . \
  --include="*.html" --include="*.css" --include="*.tsx" --include="*.jsx" --include="*.js" --include="*.astro"
```
Gleiches Vorgehen für FontAwesome, Material Icons, `unpkg`, `cdn.jsdelivr.net`, extern verlinkte Bilder.

## D4 — Consent-Banner

**Anforderungen (§ 25 TDDDG + EDSA-Leitlinien):**
1. „Ablehnen" auf **erster Ebene**, optisch **gleichwertig** zu „Akzeptieren" — gleiche Größe, gleicher Kontrast. Grauer Ablehnen-Link neben grünem Akzeptieren-Button = unwirksam.
2. Keine Vorauswahl außer bei technisch notwendigen Diensten.
3. **Nichts lädt vor der Entscheidung** außer technisch Notwendigem.
4. Widerruf jederzeit, genauso einfach → dauerhafter Button im Footer.
5. Entscheidung protokollieren (Zeitpunkt, Version, Auswahl) — Nachweispflicht Art. 7 Abs. 1 DSGVO.
6. Kein Cookie-Wall bei Diensten, die keine Alternative bieten.

**Werkzeugwahl:**
| Tool | Wann |
|---|---|
| **Klaro!** (Open Source, self-hosted) | Standardwahl — kostenlos, kein weiterer Drittanbieter, blockiert Skripte wirklich |
| **CookieConsent v3 (Orest Bida)** | leichtgewichtig, keine Abhängigkeiten |
| Cookiebot / Usercentrics | wenn der Kunde Auto-Scan und Audit-Reports braucht (kostenpflichtig, selbst ein Drittanbieter → eigener Baustein in der Datenschutzerklärung) |
| **kein Banner** | wenn wirklich nur technisch notwendige Dienste laufen — das ist der sauberste Zustand. Dann keinen Banner bauen, nur den Abschnitt in der Datenschutzerklärung. |

**Skripte korrekt blockieren** — `type="text/plain"` verhindert die Ausführung, bis das Tool umschaltet:
```html
<script type="text/plain" data-name="google-analytics"
        src="https://www.googletagmanager.com/gtag/js?id=G-XXXX"></script>
```

**Google Consent Mode v2** ergänzen, wenn GA4/Ads laufen — vor dem Banner-Skript:
```html
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted',
    wait_for_update: 500
  });
</script>
```
> Consent Mode ersetzt **kein** Consent-Tool — es ist nur die Signalisierung an Google.

**Minimal-Banner ohne Abhängigkeiten** (wenn genau ein optionaler Dienst existiert):
```html
<div id="cc" class="cc" role="dialog" aria-modal="false"
     aria-labelledby="cc-t" aria-describedby="cc-d" hidden>
  <h2 id="cc-t">Cookies &amp; Datenschutz</h2>
  <p id="cc-d">
    Wir verwenden technisch notwendige Cookies. Zusätzlich möchten wir {{DIENST}} einsetzen,
    um {{ZWECK}}. Dabei werden Daten an {{ANBIETER}} übertragen. Die Einwilligung ist
    freiwillig und jederzeit im Footer widerrufbar.
    <a href="/datenschutz">Mehr in der Datenschutzerklärung</a>
  </p>
  <div class="cc-actions">
    <button type="button" data-cc="deny">Ablehnen</button>
    <button type="button" data-cc="allow">Akzeptieren</button>
  </div>
</div>

<style>
  .cc{position:fixed;inset:auto 1rem 1rem 1rem;max-width:34rem;margin-inline:auto;z-index:9999;
      background:#fff;color:#18181b;border:1px solid #e4e4e7;border-radius:12px;padding:1.25rem;
      box-shadow:0 10px 40px rgb(0 0 0 / .18);font-size:.9375rem;line-height:1.5}
  .cc h2{font-size:1rem;margin:0 0 .5rem}
  .cc-actions{display:flex;gap:.75rem;margin-top:1rem}
  /* Gleichwertigkeit: identische Fläche und Gewichtung für beide Buttons */
  .cc-actions button{flex:1;padding:.7rem 1rem;font:inherit;font-weight:600;cursor:pointer;
      border-radius:8px;border:1px solid #18181b;background:#fff;color:#18181b}
  .cc-actions button[data-cc="allow"]{background:#18181b;color:#fff}
  @media (prefers-color-scheme: dark){
    .cc{background:#18181b;color:#fafafa;border-color:#3f3f46}
    .cc-actions button{border-color:#fafafa;background:#18181b;color:#fafafa}
    .cc-actions button[data-cc="allow"]{background:#fafafa;color:#18181b}
  }
</style>

<script>
(function () {
  var KEY = 'consent.v1';
  var el = document.getElementById('cc');

  function save(value) {
    localStorage.setItem(KEY, JSON.stringify({
      value: value, at: new Date().toISOString(), version: 1
    }));
  }
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { return null; }
  }
  function activate() {
    document.querySelectorAll('script[type="text/plain"][data-cc-src]').forEach(function (s) {
      var n = document.createElement('script');
      n.src = s.dataset.ccSrc;
      n.async = true;
      document.head.appendChild(n);
    });
    if (window.gtag) {
      gtag('consent', 'update', { analytics_storage: 'granted' });
    }
  }

  var stored = load();
  if (!stored) { el.hidden = false; }
  else if (stored.value === 'allow') { activate(); }

  el.addEventListener('click', function (e) {
    var choice = e.target.dataset.cc;
    if (!choice) return;
    save(choice);
    el.hidden = true;
    if (choice === 'allow') activate();
  });

  document.querySelectorAll('[data-cc-open]').forEach(function (b) {
    b.addEventListener('click', function () { el.hidden = false; });
  });
})();
</script>
```
> Der Banner speichert die Entscheidung in `localStorage` — das ist nach § 25 Abs. 2 Nr. 2 TDDDG einwilligungsfrei zulässig, weil er zur Erfüllung des vom Nutzer ausgedrückten Wunsches unbedingt erforderlich ist.

## D5 — Zwei-Klick-Lösung für Embeds

Statt YouTube/Maps direkt zu laden:
```html
<div class="embed-consent" data-embed="youtube">
  <p>
    Hier ist ein Video von YouTube eingebettet. Beim Laden werden Daten — unter anderem Ihre
    IP-Adresse — an Google übertragen.
    <a href="/datenschutz#youtube">Datenschutzhinweise</a>
  </p>
  <button type="button" data-embed-load
          data-src="https://www.youtube-nocookie.com/embed/{{ID}}">
    Video laden
  </button>
</div>

<script>
document.querySelectorAll('[data-embed-load]').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var f = document.createElement('iframe');
    f.src = btn.dataset.src;
    f.width = 560; f.height = 315; f.loading = 'lazy';
    f.title = 'Eingebettetes Video';
    f.allow = 'accelerometer; clipboard-write; encrypted-media; picture-in-picture';
    f.referrerPolicy = 'strict-origin-when-cross-origin';
    f.allowFullscreen = true;
    btn.closest('.embed-consent').replaceWith(f);
  });
});
</script>
```
Für Karten die datensparsamere Variante vorschlagen: statisches Bild + Link „In Google Maps öffnen" — braucht gar keine Einwilligung.

## D6 — Formulare

- Neben dem Absende-Button: `Mit dem Absenden stimmen Sie der Verarbeitung Ihrer Angaben gemäß unserer <a href="/datenschutz">Datenschutzerklärung</a> zu.` — **ohne** Pflicht-Checkbox, wenn die Rechtsgrundlage lit. b oder f ist.
- Newsletter dagegen **braucht** eine aktive, nicht vorausgewählte Checkbox + Double-Opt-in.
- Nur Felder abfragen, die gebraucht werden (Datenminimierung, Art. 5 Abs. 1 lit. c) — Pflichtfelder als solche markieren.
- Serverseitig validieren; Formulardaten nicht in Logs oder Analytics-Events spiegeln.

## D7 — Security-Header (unterstützen die Rechenschaftspflicht)

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=(), interest-cohort=()
Content-Security-Policy: {{projektspezifisch}}
```

## D8 — Abschluss-Checkliste vor dem Livegang

- [ ] Impressum und Datenschutzerklärung erreichbar, von jeder Seite, wörtlich benannt
- [ ] Keine Platzhalter (`{{`, `<AUSFÜLLEN>`, „Musterstraße") mehr im Text
- [ ] Nur tatsächlich eingesetzte Dienste beschrieben — und alle davon
- [ ] Keine Fonts/Icons/Skripte von fremden CDNs
- [ ] Kein Tracking vor Einwilligung; Ablehnen gleichwertig; Widerruf im Footer
- [ ] Embeds hinter Zwei-Klick oder Consent-Gate
- [ ] KI-Chatbot gekennzeichnet, KI-Medien mit Disclaimer
- [ ] AVVs abgeschlossen (Hosting, Mail, Analytics, KI-API)
- [ ] Keine API-Keys im Client-Bundle
- [ ] `scripts/compliance-audit.sh` läuft ohne Befund durch
