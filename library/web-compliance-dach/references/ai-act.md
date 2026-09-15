# Modul C — EU AI Act: Transparenz-Komponenten

Verordnung (EU) 2024/1689. **Art. 50 (Transparenzpflichten) gilt seit dem 02.08.2026** — also aktuell anwendbar. Stand dieser Referenz: August 2026; bei kritischen Projekten den aktuellen Anwendungsstand kurz gegenprüfen, da es zu Art. 50 Leitlinien und Anpassungsdiskussionen der Kommission gibt.

Zeitschiene zur Einordnung:
| Datum | Wirksam |
|---|---|
| 01.08.2024 | Inkrafttreten |
| 02.02.2025 | Verbotene Praktiken (Art. 5), KI-Kompetenz (Art. 4) |
| 02.08.2025 | Pflichten für GPAI-Modelle, Governance, Sanktionen |
| **02.08.2026** | **Art. 50 Transparenz**, Hochrisiko nach Anhang III |
| 02.08.2027 | Hochrisiko in regulierten Produkten (Anhang I) |

---

## Wer ist betroffen?

Wer einen Chatbot oder ein KI-Feature auf der eigenen Website betreibt, ist **Betreiber** („deployer") — die Transparenzpflicht trifft dich, nicht nur den Modellanbieter.

| Situation | Pflicht | Art. |
|---|---|---|
| Chatbot / KI-Assistent, mit dem Menschen interagieren | Offenlegen, dass es KI ist — **vor oder bei der ersten Interaktion** | 50 Abs. 1 |
| KI erzeugt Bild/Audio/Video/Text-Ausgaben | Maschinenlesbare Kennzeichnung der Ausgabe (Anbieterpflicht) | 50 Abs. 2 |
| Emotionserkennung / biometrische Kategorisierung | Betroffene informieren | 50 Abs. 3 |
| **Deepfakes** (realistische generierte/manipulierte Bild-, Ton-, Videoinhalte) | Sichtbar offenlegen, dass künstlich erzeugt/manipuliert | 50 Abs. 4 |
| KI-generierter **Text zu Angelegenheiten von öffentlichem Interesse**, veröffentlicht zur Information der Öffentlichkeit | Offenlegen — **entfällt** bei menschlicher Überprüfung/redaktioneller Verantwortung | 50 Abs. 4 |
| Reine Marketing-/Produktbilder ohne Deepfake-Charakter | Keine strikte Art.-50-Pflicht, freiwilliger Hinweis empfohlen (UWG-Irreführung vermeiden) | — |

**Ausnahme Art. 50 Abs. 1:** Die Kennzeichnung entfällt, wenn es „aus Sicht einer angemessen aufmerksamen Person offensichtlich" ist, dass es sich um KI handelt. Verlass dich nicht darauf — kennzeichne.

---

## C1 — Chatbot / Live-KI: Kennzeichnung im Interface

Der Hinweis muss **vor der ersten Interaktion** sichtbar sein, nicht erst in der Datenschutzerklärung.

```html
<div class="chat-widget" role="region" aria-label="KI-Assistent">
  <div class="chat-header">
    <span class="chat-title">{{ASSISTENT_NAME}}</span>
    <span class="chat-ai-badge" aria-hidden="true">KI</span>
  </div>

  <!-- Pflichthinweis nach Art. 50 Abs. 1 EU AI Act -->
  <p class="chat-disclosure">
    Sie chatten mit einem KI-gestützten Assistenten, nicht mit einem Menschen.
    Antworten können fehlerhaft sein und stellen keine {{Rechts-/Gesundheits-/Finanz-}}beratung dar.
    Bitte geben Sie keine sensiblen personenbezogenen Daten ein.
    <a href="/datenschutz#ki">Hinweise zur Datenverarbeitung</a>
  </p>

  <div class="chat-messages" aria-live="polite"></div>
  …
</div>
```

```css
.chat-disclosure {
  font-size: 0.8125rem;
  line-height: 1.45;
  padding: 0.75rem 1rem;
  color: var(--fg-muted, #555);
  background: var(--surface-subtle, #f4f4f5);
  border-bottom: 1px solid var(--border, #e4e4e7);
}
.chat-ai-badge {
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  background: var(--accent-subtle, #e0e7ff);
  color: var(--accent-strong, #3730a3);
}
```

**Anforderungen:**
- Dauerhaft sichtbar oder mindestens beim Öffnen — nicht wegklickbar ohne Wiederkehr.
- Kein Dark Pattern: der Assistent darf sich nicht mit menschlichem Namen + Foto als Mitarbeiter ausgeben.
- Bei Sprachassistenten: **hörbarer** Hinweis in der Begrüßung.
- Barrierefrei: ausreichender Kontrast, im DOM vor dem Eingabefeld, Screenreader-lesbar.

## C2 — Übergabe an einen Menschen

Ist ein Wechsel zu einem Menschen möglich, muss der Wechsel erkennbar sein:
```
── Sie sprechen ab jetzt mit {{NAME}} aus unserem Team. ──
```

## C3 — KI-generierte Medien: sichtbarer Disclaimer

**Einzelnes Bild** (Caption direkt am Asset):
```html
<figure>
  <img src="/img/visual.webp" alt="{{ALT}}" width="1200" height="675">
  <figcaption>
    <span class="ai-tag">KI-generiert</span>
    Diese Visualisierung wurde mittels generativer KI erstellt und zeigt keine reale
    {{Person / Örtlichkeit / Produktausführung}}.
  </figcaption>
</figure>
```

**Seitenweit** (Footer oder eigener Abschnitt in der Datenschutz-/Transparenzseite):
```
Hinweis zu KI-generierten Inhalten

Teile der auf dieser Website verwendeten {{Bilder / Texte / Videos}} wurden mithilfe
generativer KI-Systeme erstellt ({{TOOLS, z. B. Midjourney, ChatGPT, Claude}}).
KI-generierte Abbildungen dienen der Veranschaulichung und bilden keine realen Personen,
Räumlichkeiten oder Produktausführungen ab. Maßgeblich für den Leistungsumfang sind
ausschließlich die vertraglichen Vereinbarungen.
Alle Inhalte werden vor der Veröffentlichung redaktionell geprüft.
```

**Deepfake-Fall** (realistische Darstellung von Personen/Ereignissen) — Hinweis muss **spätestens bei der ersten Wahrnehmung** klar und deutlich erkennbar sein: sichtbares Overlay im Bild/Video, nicht nur eine Bildunterschrift.

## C4 — Maschinenlesbare Kennzeichnung

Art. 50 Abs. 2 adressiert primär die Anbieter der Generatoren; als Betreiber solltest du vorhandene Kennzeichnungen aber **nicht zerstören**:

- **C2PA / Content Credentials** beim Export erhalten — viele Bildoptimierungs-Pipelines (`sharp`, `imagemin`, Next.js Image Optimization) strippen Metadaten. Bewusst entscheiden.
- IPTC-Feld `DigitalSourceType` auf `trainedAlgorithmicMedia` setzen, wo möglich.
- Ergänzend im HTML:
```html
<meta name="ai-generated" content="true">
<meta name="ai-generator" content="{{TOOL}}">
```
(kein Rechtsstandard, aber gängige Praxis und schadet nicht)

## C5 — Urheberrechtlicher Zusatz

Bei rein KI-generierten Assets besteht mangels menschlicher Schöpfungshöhe **kein Urheberrechtsschutz** (§ 2 Abs. 2 UrhG). Der pauschale Urheberrechts-Absatz im Impressum darf sie deshalb nicht mit einschließen:

```
An rein KI-generierten Inhalten dieser Website besteht kein Urheberrechtsschutz im Sinne des
§ 2 Abs. 2 UrhG. Von der Nutzung ausgenommen bleiben Marken-, Namens- und Kennzeichenrechte
sowie sämtliche menschlich geschaffenen Inhalte, insbesondere {{Texte, Logo, Fotografien}},
die dem urheber- bzw. kennzeichenrechtlichen Schutz unterliegen.
```

Zusätzlich: **niemals** dem Kunden Urheberrechte an KI-Assets zusichern. Bei Kundenprojekten in Angebot/Vertrag klarstellen, dass an KI-generierten Bildern nur ein tatsächliches Nutzungsverhältnis, kein ausschließliches Recht übertragen werden kann.

## C6 — KI-Kompetenz (Art. 4)

Gilt seit 02.02.2025 für Anbieter **und** Betreiber: Beschäftigte, die mit dem KI-System arbeiten, müssen ein ausreichendes Maß an KI-Kompetenz haben. Bei Kundenprojekten mit Chatbot einen Satz in die Übergabedokumentation aufnehmen: wer das System bedient, wie Fehlausgaben gemeldet werden, wer den Not-Aus kennt.

## C7 — Wann es über Transparenz hinausgeht

Melde dem User aktiv, wenn eine dieser Konstellationen auftaucht — dann ist es **kein** reiner Transparenzfall mehr, sondern potenziell Hochrisiko (Anhang III) oder verbotene Praxis (Art. 5):

- KI filtert **Bewerbungen** oder bewertet Kandidaten
- KI entscheidet über **Kreditwürdigkeit**, Versicherungstarife, Preise pro Person
- **Emotionserkennung** am Arbeitsplatz oder in Bildungseinrichtungen (verboten, Art. 5)
- **Biometrische Kategorisierung** nach sensiblen Merkmalen
- **Social Scoring**
- KI im Zugang zu Bildung, Sozialleistungen, Notfalldiensten

In diesen Fällen: nicht einfach Texte generieren, sondern klar sagen, dass eine Konformitätsbewertung, Risikomanagement und fachanwaltliche Prüfung nötig sind.
