#!/usr/bin/env bash
# compliance-audit.sh — Technik-Scan für den Skill web-compliance-dach
# Findet eingesetzte Dienste und typische DSGVO-/TDDDG-Fallstricke in einem Web-Projekt.
# Aufruf: ./compliance-audit.sh [projektpfad]
# Exit: 0 = keine Befunde, 1 = Befunde vorhanden, 2 = Aufrufproblem

set -uo pipefail

ROOT="${1:-.}"
[ -d "$ROOT" ] || { echo "Pfad nicht gefunden: $ROOT" >&2; exit 2; }
ROOT="$(cd "$ROOT" && pwd)"

EXCLUDES=(--exclude-dir=node_modules --exclude-dir=.git --exclude-dir=dist
          --exclude-dir=build --exclude-dir=.next --exclude-dir=.nuxt
          --exclude-dir=out --exclude-dir=vendor --exclude-dir=.venv
          --exclude-dir=coverage --exclude-dir=.cache --exclude-dir=public/fonts)
CODE=(--include=*.html --include=*.htm --include=*.js --include=*.jsx --include=*.ts
      --include=*.tsx --include=*.astro --include=*.vue --include=*.svelte
      --include=*.php --include=*.css --include=*.scss --include=*.mdx --include=*.liquid)

FINDINGS=0
SERVICES=()

c_hit()  { printf '\033[31m  ✗ %s\033[0m\n' "$1"; FINDINGS=$((FINDINGS+1)); }
c_warn() { printf '\033[33m  ! %s\033[0m\n' "$1"; FINDINGS=$((FINDINGS+1)); }
c_ok()   { printf '\033[32m  ✓ %s\033[0m\n' "$1"; }
c_info() { printf '    %s\n' "$1"; }
head2()  { printf '\n\033[1m%s\033[0m\n' "$1"; }

# scan <regex> -> Trefferzeilen (max 4), leer wenn nichts
scan() { grep -rInE "$1" "$ROOT" "${EXCLUDES[@]}" "${CODE[@]}" 2>/dev/null | head -4; }
has()  { grep -rIqE "$1" "$ROOT" "${EXCLUDES[@]}" "${CODE[@]}" 2>/dev/null; }
rel()  { printf '%s' "${1#$ROOT/}"; }

printf '\033[1m═══ Compliance-Audit ═══\033[0m\n%s\n' "$ROOT"

# ───────────────────────── 1. Stack & Dienste ─────────────────────────
head2 "1. Erkannte Dienste"

PKG="$ROOT/package.json"
CONFIGS=""
for f in package.json vercel.json netlify.toml firebase.json wrangler.toml \
         .firebaserc astro.config.mjs next.config.js next.config.mjs; do
  [ -f "$ROOT/$f" ] && CONFIGS="$CONFIGS$f
$(cat "$ROOT/$f" 2>/dev/null)
"
done
# Verzeichnisnamen mitliefern (z. B. netlify/functions, .vercel)
CONFIGS="$CONFIGS
$(ls -A "$ROOT" 2>/dev/null)"

detect() { # detect <label> <regex>
  if has "$2" || printf '%s' "$CONFIGS" | grep -qiE "$2" 2>/dev/null; then
    SERVICES+=("$1"); c_info "• $1"
  fi
}

detect "Vercel (Hosting)"                 'vercel\.(app|com)|@vercel/'
detect "Vercel Analytics / Speed Insights" '@vercel/(analytics|speed-insights)'
detect "Netlify (Hosting)"                'netlify\.(app|com)|@netlify/'
detect "Cloudflare (CDN/Pages/Workers)"   'cloudflare|wrangler\.toml'
detect "Firebase (Hosting/DB/Auth)"       'firebase|firestore|firebaseapp\.com'
detect "Supabase"                         'supabase'
detect "AWS"                              'aws-sdk|@aws-sdk/|amazonaws\.com'
detect "Google Analytics / GTM"           'googletagmanager\.com|gtag\(|G-[A-Z0-9]{8,}|UA-[0-9]{4,}'
detect "Meta Pixel"                       'connect\.facebook\.net|fbq\('
detect "TikTok Pixel"                     'analytics\.tiktok\.com|ttq\.'
detect "LinkedIn Insight"                 'snap\.licdn\.com|_linkedin_partner_id'
detect "Hotjar / Clarity / Matomo / Plausible" 'hotjar|clarity\.ms|matomo|plausible'
detect "Google Maps"                      'maps\.google|maps\.googleapis\.com|google\.com/maps'
detect "YouTube-Embed"                    'youtube\.com/embed|youtube-nocookie\.com'
detect "Vimeo-Embed"                      'player\.vimeo\.com'
detect "Stripe"                           'stripe|js\.stripe\.com'
detect "PayPal"                           'paypal'
detect "Resend"                           'resend'
detect "Brevo / Sendinblue"               'brevo|sendinblue'
detect "Mailchimp"                        'mailchimp|list-manage\.com'
detect "SendGrid / Postmark"              'sendgrid|postmarkapp'
detect "OpenAI API"                       'openai|api\.openai\.com'
detect "Anthropic API"                    'anthropic|api\.anthropic\.com'
detect "Google Gemini API"                'generativelanguage\.googleapis|@google/gene?rative'
detect "reCAPTCHA"                        'recaptcha'
detect "Turnstile"                        'turnstile'
detect "Clerk / Auth0 / NextAuth"         '@clerk/|auth0|next-auth'
detect "Sentry"                           '@sentry/|sentry\.io'
detect "Calendly"                         'calendly'

[ ${#SERVICES[@]} -eq 0 ] && c_info "(keine Drittanbieter gefunden — bitte manuell gegenprüfen)"

# ───────────────────── 2. Fremde CDNs für Assets ─────────────────────
head2 "2. Externe Assets (Fonts, Icons, Skripte)"

FONT_HITS="$(scan 'fonts\.(googleapis|gstatic)\.com')"
if [ -n "$FONT_HITS" ]; then
  c_hit "Google Fonts per CDN eingebunden — überträgt die IP ohne Einwilligung in die USA"
  c_info "LG München I, 3 O 17493/20. Lokalisieren, siehe references/einbau.md D3."
  echo "$FONT_HITS" | sed "s|$ROOT/||" | sed 's/^/      /'
else
  c_ok "Keine Google-Fonts-CDN-Einbindung"
fi

FA_HITS="$(scan '(use|kit)\.fontawesome\.com|fonts\.googleapis\.com/icon|cdnjs\.cloudflare\.com|unpkg\.com|cdn\.jsdelivr\.net')"
if [ -n "$FA_HITS" ]; then
  c_warn "Weitere externe CDNs eingebunden (FontAwesome/unpkg/jsdelivr/cdnjs)"
  echo "$FA_HITS" | sed "s|$ROOT/||" | sed 's/^/      /'
else
  c_ok "Keine weiteren Asset-CDNs"
fi

# ───────────────────── 3. Rechtstext-Seiten ─────────────────────
head2 "3. Rechtstexte vorhanden?"

find_page() { find "$ROOT" -iname "*$1*" \
    -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/.next/*" \
    -not -path "*/dist/*" -not -path "*/build/*" 2>/dev/null | head -3; }

LEGAL_FILES=()
while IFS= read -r f; do [ -n "$f" ] && LEGAL_FILES+=("$f"); done < <(find_page impressum; find_page datenschutz; find_page privacy)

IMP="$(find_page impressum)"
DAT="$(find_page datenschutz; find_page privacy)"

if [ -n "$IMP" ]; then c_ok "Impressum-Datei gefunden"; echo "$IMP" | sed "s|$ROOT/|      |"
else c_hit "Kein Impressum gefunden — Pflicht nach § 5 DDG"; fi

if [ -n "$DAT" ]; then c_ok "Datenschutz-Datei gefunden"; echo "$DAT" | sed "s|$ROOT/|      |"
else c_hit "Keine Datenschutzerklärung gefunden — Pflicht nach Art. 13 DSGVO"; fi

# Footer-Links
if has 'href=["'"'"'][^"'"'"']*impressum'; then c_ok "Footer-Link auf das Impressum vorhanden"
else c_hit "Kein Link auf das Impressum im Markup — muss von jeder Seite erreichbar sein"; fi

if has 'href=["'"'"'][^"'"'"']*(datenschutz|privacy)'; then c_ok "Link auf die Datenschutzerklärung vorhanden"
else c_hit "Kein Link auf die Datenschutzerklärung im Markup"; fi

# Platzhalter in bereits vorhandenen Texten
if [ ${#LEGAL_FILES[@]} -gt 0 ]; then
  PH="$(grep -InE 'Musterstra|Max Mustermann|\{\{[A-Z_]+\}\}|<AUSFÜLLEN>|LOREM|XXXXX' "${LEGAL_FILES[@]}" 2>/dev/null | head -4)"
  [ -n "$PH" ] && { c_hit "Platzhalter in den Rechtstexten — nicht live gehen lassen"; echo "$PH" | sed "s|$ROOT/||" | sed 's/^/      /'; }
fi

# ─────────────── 4. Consent & Tracking-Reihenfolge ───────────────
head2 "4. Consent-Management"

HAS_CONSENT=false
if has 'klaro|cookieconsent|CookieConsent|cookiebot|usercentrics|consentmanager|data-cc|__tcfapi'; then
  HAS_CONSENT=true; c_ok "Consent-Mechanismus im Code gefunden"
fi

NEEDS_CONSENT="$(scan 'googletagmanager\.com|connect\.facebook\.net|analytics\.tiktok\.com|snap\.licdn\.com|hotjar|clarity\.ms|youtube\.com/embed|maps\.googleapis\.com|measurementId|firebase/analytics|getAnalytics|logEvent\(')"

if [ -n "$NEEDS_CONSENT" ]; then
  if $HAS_CONSENT; then
    c_info "Einwilligungspflichtige Dienste + Consent-Tool vorhanden — Blockierung manuell verifizieren:"
    c_info "Netzwerk-Tab öffnen, Seite neu laden, VOR jeder Auswahl auf Requests zu Dritten prüfen."
  else
    c_hit "Einwilligungspflichtige Dienste ohne erkennbares Consent-Tool"
  fi
  echo "$NEEDS_CONSENT" | sed "s|$ROOT/||" | sed 's/^/      /'
else
  c_ok "Keine einwilligungspflichtigen Drittdienste gefunden"
fi

# Skripte, die offensichtlich ungeblockt laden
UNBLOCKED="$(grep -rInE '<script[^>]+src=["'"'"'][^"'"'"']*(googletagmanager|facebook\.net|hotjar|clarity\.ms|tiktok)' \
             "$ROOT" "${EXCLUDES[@]}" --include=*.html --include=*.tsx --include=*.jsx --include=*.astro 2>/dev/null \
             | grep -v 'text/plain' | head -4)"
[ -n "$UNBLOCKED" ] && { c_hit "Tracking-Skript lädt ohne type=\"text/plain\"-Blockade"; echo "$UNBLOCKED" | sed "s|$ROOT/||" | sed 's/^/      /'; }

# Widerrufs-Button
if $HAS_CONSENT && ! has 'Cookie-Einstellungen|Cookie Einstellungen|cookie-settings|data-cc-open|Datenschutz-Einstellungen'; then
  c_warn "Kein dauerhafter „Cookie-Einstellungen\"-Button — Widerruf muss so einfach sein wie die Zustimmung"
fi

# ─────────────── 5. Embeds ───────────────
head2 "5. Eingebettete Drittinhalte"
IFR="$(scan '<iframe[^>]+src=["'"'"']https?://')"
if [ -n "$IFR" ]; then
  c_warn "iframes mit externer Quelle — lädt beim Rendern bereits Daten zum Anbieter"
  c_info "Zwei-Klick-Lösung einbauen, siehe references/einbau.md D5."
  echo "$IFR" | sed "s|$ROOT/||" | sed 's/^/      /'
else
  c_ok "Keine direkt geladenen externen iframes"
fi

# ─────────────── 6. Formulare ───────────────
head2 "6. Formulare"
if has '<form|onSubmit|handleSubmit|<input|<textarea|type=["'"'"']email'; then
  c_info "Formular(e) gefunden"
  if has 'datenschutz|privacy'; then c_ok "Datenschutz-Verweis im Projekt vorhanden — Platzierung am Formular prüfen"
  else c_hit "Formular ohne jeden Datenschutz-Hinweis"; fi
  has 'type=["'"'"']checkbox' && c_info "Checkbox vorhanden — bei Art. 6 Abs. 1 lit. b/f ist eine Einwilligungs-Checkbox falsch (nur bei Newsletter nötig)"
else
  c_ok "Keine Formulare gefunden"
fi

# ─────────────── 7. KI-Transparenz ───────────────
head2 "7. KI-Transparenz (AI Act Art. 50, gilt seit 02.08.2026)"
AI_CODE=false
has 'api\.openai\.com|api\.anthropic\.com|generativelanguage\.googleapis|openai|anthropic' && AI_CODE=true
if $AI_CODE; then
  c_info "KI-API im Projekt gefunden"
  if has 'KI-gestützt|künstliche Intelligenz|KI-Assistent|AI-Assistent|KI-generiert|AI-generated'; then
    c_ok "KI-Hinweis im Text vorhanden — Platzierung vor der ersten Interaktion prüfen"
  else
    c_hit "Keine KI-Kennzeichnung gefunden — Art. 50 Abs. 1 verlangt Offenlegung vor der Interaktion"
  fi
else
  c_ok "Keine Live-KI im Code (KI-generierte Medien trotzdem manuell prüfen)"
fi

# ─────────────── 8. Secrets im Client ───────────────
head2 "8. Schlüssel im Client-Bundle"
SEC="$(grep -rInE '(NEXT_PUBLIC_|VITE_|REACT_APP_)[A-Z_]*(OPENAI|ANTHROPIC|SECRET|PRIVATE|SERVICE_ROLE|STRIPE_SK)|sk-(ant-)?[A-Za-z0-9_-]{20,}|sk_live_[A-Za-z0-9]{20,}' \
        "$ROOT" "${EXCLUDES[@]}" "${CODE[@]}" 2>/dev/null | head -4)"
if [ -n "$SEC" ]; then
  c_hit "Möglicher geheimer Schlüssel im Client-Code — sofort rotieren und serverseitig verlagern"
  echo "$SEC" | sed "s|$ROOT/||" | cut -c1-140 | sed 's/^/      /'
else
  c_ok "Keine offensichtlichen Secrets im Client-Code"
fi

# ─────────────── Ergebnis ───────────────
printf '\n\033[1m═══ Ergebnis ═══\033[0m\n'
if [ "$FINDINGS" -eq 0 ]; then
  printf '\033[32mKeine automatisch erkennbaren Befunde.\033[0m\n'
  echo "Manuell bleibt zu prüfen: AVVs, Vollständigkeit der Pflichtangaben, tatsächliche Skript-Blockade im Netzwerk-Tab."
  exit 0
else
  printf '\033[31m%s Befund(e).\033[0m Details oben; Behebung siehe references/einbau.md.\n' "$FINDINGS"
  exit 1
fi
