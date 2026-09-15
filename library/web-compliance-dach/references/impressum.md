# Modul A — Impressum

Rechtsgrundlage Deutschland: **§ 5 DDG** (Digitale-Dienste-Gesetz, seit 14.05.2024 an Stelle des § 5 TMG). Bei journalistisch-redaktionellen Inhalten zusätzlich **§ 18 Abs. 2 MStV**.

## Platzierungsregeln (gelten immer)

- Von **jeder** Seite mit maximal zwei Klicks erreichbar → permanenter Footer-Link.
- Verlinkung wörtlich als **„Impressum"** (in DE) — „Kontakt", „Legal", „About" genügen nicht.
- Muss ohne JavaScript-Interaktion lesbar sein (kein Modal-only, kein Accordion, das ohne JS zubleibt).
- Eigene URL, indexierbar, kein `noindex`.

## Pflichtangaben nach Rechtsform (DE)

Aufsteigend — jede Stufe enthält die vorherige.

**Alle:** Name/Firmierung · ladungsfähige Anschrift (kein Postfach) · E-Mail · zweiter schneller Kontaktweg (Telefon **oder** Kontaktformular mit Antwortzusage)

| Rechtsform | Zusätzlich |
|---|---|
| Einzelunternehmen / Kleingewerbe | Vor- und Nachname der natürlichen Person |
| GbR | alle Gesellschafter mit Vor- und Nachnamen |
| e.K. | Registergericht + HRA-Nummer |
| OHG / KG | Registergericht + HRA-Nummer, vertretungsberechtigte Gesellschafter |
| UG (haftungsbeschränkt) / GmbH | Registergericht + HRB-Nummer, alle Geschäftsführer, Firmierung inkl. Rechtsformzusatz |
| AG | Registergericht + HRB, Vorstand, Aufsichtsratsvorsitzender |
| Verein | Registergericht + VR-Nummer, Vorstand nach § 26 BGB |

**Wenn vorhanden:** USt-IdNr. nach § 27a UStG. Ist keine vorhanden, Zeile **weglassen** — niemals die Steuernummer angeben (die gehört nicht ins Impressum).

**Bei reglementierten Berufen** zusätzlich: gesetzliche Berufsbezeichnung, Staat der Verleihung, zuständige Kammer mit Anschrift/URL, berufsrechtliche Regelungen mit Fundstelle.

**Bei Blog/News/redaktionellen Inhalten:** „Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV: Name, Anschrift".

## Verbraucherschlichtung — WICHTIG, Stand 2026

Die **EU-Online-Streitbeilegungsplattform wurde zum 20.07.2025 eingestellt.** Der früher übliche Textbaustein mit dem Link auf `ec.europa.eu/consumers/odr` ist **veraltet und gehört entfernt** — ein toter Pflichtlink ist schlimmer als keiner.

Verbleibt nur der Hinweis nach § 36 VSBG (Pflicht bei B2C und mehr als 10 Beschäftigten, sonst freiwillig):

```
Verbraucherstreitbeilegung
Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer
Verbraucherschlichtungsstelle teilzunehmen.
```

## Vorlage — statisches HTML

```html
<main class="legal">
  <h1>Impressum</h1>

  <h2>Angaben gemäß § 5 DDG</h2>
  <p>
    {{FIRMIERUNG}}<br>
    {{STRASSE_NR}}<br>
    {{PLZ_ORT}}<br>
    {{LAND}}
  </p>

  <!-- nur bei juristischen Personen -->
  <h2>Vertreten durch</h2>
  <p>{{GESCHAEFTSFUEHRER}}</p>

  <h2>Kontakt</h2>
  <p>
    Telefon: <a href="tel:{{TEL_RAW}}">{{TELEFON}}</a><br>
    E-Mail: <a href="mailto:{{EMAIL}}">{{EMAIL}}</a>
  </p>

  <!-- nur bei Registereintrag -->
  <h2>Registereintrag</h2>
  <p>
    Eintragung im {{REGISTERART}}<br>
    Registergericht: {{REGISTERGERICHT}}<br>
    Registernummer: {{REGISTERNUMMER}}
  </p>

  <!-- nur wenn vorhanden -->
  <h2>Umsatzsteuer-ID</h2>
  <p>
    Umsatzsteuer-Identifikationsnummer gemäß § 27a Umsatzsteuergesetz:<br>
    {{USTID}}
  </p>

  <!-- nur bei redaktionellen Inhalten -->
  <h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
  <p>{{NAME}}, {{STRASSE_NR}}, {{PLZ_ORT}}</p>

  <h2>Verbraucherstreitbeilegung</h2>
  <p>
    Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer
    Verbraucherschlichtungsstelle teilzunehmen.
  </p>

  <h2>Haftung für Inhalte</h2>
  <p>
    Als Diensteanbieter sind wir gemäß § 7 Abs. 1 DDG für eigene Inhalte auf diesen Seiten nach den
    allgemeinen Gesetzen verantwortlich. Nach §§ 8 bis 10 DDG sind wir als Diensteanbieter jedoch nicht
    verpflichtet, übermittelte oder gespeicherte fremde Informationen zu überwachen oder nach Umständen zu
    forschen, die auf eine rechtswidrige Tätigkeit hinweisen. Verpflichtungen zur Entfernung oder Sperrung
    der Nutzung von Informationen nach den allgemeinen Gesetzen bleiben hiervon unberührt. Eine
    diesbezügliche Haftung ist jedoch erst ab dem Zeitpunkt der Kenntnis einer konkreten Rechtsverletzung
    möglich. Bei Bekanntwerden von entsprechenden Rechtsverletzungen werden wir diese Inhalte umgehend
    entfernen.
  </p>

  <h2>Haftung für Links</h2>
  <p>
    Unser Angebot enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen Einfluss haben.
    Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte der
    verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der Seiten verantwortlich. Die
    verlinkten Seiten wurden zum Zeitpunkt der Verlinkung auf mögliche Rechtsverstöße überprüft.
    Rechtswidrige Inhalte waren zum Zeitpunkt der Verlinkung nicht erkennbar. Eine permanente inhaltliche
    Kontrolle der verlinkten Seiten ist ohne konkrete Anhaltspunkte einer Rechtsverletzung nicht zumutbar.
    Bei Bekanntwerden von Rechtsverletzungen werden wir derartige Links umgehend entfernen.
  </p>

  <h2>Urheberrecht</h2>
  <p>
    Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem deutschen
    Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der
    Grenzen des Urheberrechtes bedürfen der schriftlichen Zustimmung des jeweiligen Autors bzw. Erstellers.
    Downloads und Kopien dieser Seite sind nur für den privaten, nicht kommerziellen Gebrauch gestattet.
    Soweit die Inhalte auf dieser Seite nicht vom Betreiber erstellt wurden, werden die Urheberrechte
    Dritter beachtet. Insbesondere werden Inhalte Dritter als solche gekennzeichnet.
  </p>
</main>
```

> **KI-Assets:** Wurden Bilder oder Texte rein generativ erstellt, darf der Urheberrechts-Absatz sie nicht mit einschließen. Ergänze stattdessen den Hinweis aus `ai-act.md` (Abschnitt „Urheberrechtlicher Zusatz").

## Österreich

Grundlage: **§ 5 ECG** + **§ 25 MedienG** (Offenlegung). Zusätzlich zu den DE-Angaben:

- Firmenbuchnummer + Firmenbuchgericht
- Mitgliedschaft **WKO** (Wirtschaftskammer) + Fachgruppe
- **Gewerbeordnung** als anwendbare Rechtsvorschrift, abrufbar über `ris.bka.gv.at`
- Aufsichtsbehörde (Bezirksverwaltungsbehörde / Magistrat)
- **Blattlinie** und Angabe der grundlegenden Richtung bei redaktionellen Inhalten (§ 25 MedienG)

## Schweiz

Keine allgemeine Impressumspflicht wie in DE — aber:

- **Art. 3 Abs. 1 lit. s UWG**: bei elektronischem Geschäftsverkehr sind klare Angaben zu Identität und Kontaktadresse Pflicht (Firma, Adresse, E-Mail).
- **revDSG** (in Kraft seit 01.09.2023) verlangt eine Datenschutzerklärung mit Angabe des Verantwortlichen; bei Datenexport ins Ausland Nennung der Staaten.
- Handelsregister-Nummer (UID/CHE-Nummer) angeben, falls eingetragen.
- Richtet sich die Seite (auch) an EU-Nutzer, gilt die DSGVO parallel via Marktortprinzip → dann DE-Variante bauen.
