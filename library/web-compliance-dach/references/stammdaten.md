# Stammdaten — einmalig ausfüllen

Diese Datei ist die Quelle für alle Impressen und Datenschutzerklärungen **eigener** Projekte.
Solange hier `<AUSFÜLLEN>` steht, fragt der Skill nach und trägt die Antwort hier ein.

> Für **Kundenprojekte** gilt diese Datei nicht — dort immer die Daten des Kunden abfragen und diese Datei nicht verändern.

---

## Verantwortlicher / Diensteanbieter

| Feld | Wert |
|---|---|
| Rechtsform | `<AUSFÜLLEN>` (Einzelunternehmen / Kleingewerbe / GbR / UG / GmbH / e.K. / AG) |
| Firmierung (exakt wie im Register) | `<AUSFÜLLEN>` |
| Vor- und Nachname (natürliche Person) | `<AUSFÜLLEN>` |
| Straße + Hausnummer | `<AUSFÜLLEN>` (kein Postfach — ladungsfähige Anschrift Pflicht) |
| PLZ + Ort | `<AUSFÜLLEN>` |
| Land | `<AUSFÜLLEN>` |
| E-Mail | `<AUSFÜLLEN>` |
| Telefon | `<AUSFÜLLEN>` (optional, wenn ein anderer schneller Kanal existiert) |
| Kontaktformular-URL (Alternative zum Telefon) | `<AUSFÜLLEN>` |

## Register & Steuer

| Feld | Wert |
|---|---|
| Registergericht | `<AUSFÜLLEN>` (nur bei GmbH/UG/AG/e.K./OHG/KG) |
| Registernummer | `<AUSFÜLLEN>` |
| Vertretungsberechtigte Geschäftsführer | `<AUSFÜLLEN>` |
| USt-IdNr. (§ 27a UStG) | `<AUSFÜLLEN>` — falls keine vorhanden: Feld ganz weglassen, **nie** die Steuernummer stattdessen nennen |
| Kleinunternehmer § 19 UStG? | `<AUSFÜLLEN>` (ja/nein) |
| Wirtschafts-ID | `<AUSFÜLLEN>` (optional) |

## Berufsrecht (nur bei reglementierten Berufen)

| Feld | Wert |
|---|---|
| Berufsbezeichnung | `<AUSFÜLLEN>` |
| Verleihender Staat | `<AUSFÜLLEN>` |
| Zuständige Kammer + URL | `<AUSFÜLLEN>` |
| Berufsrechtliche Regelungen + Fundstelle | `<AUSFÜLLEN>` |
| Berufshaftpflicht (Versicherer + Geltungsraum) | `<AUSFÜLLEN>` |

## Redaktion & Verbraucher

| Feld | Wert |
|---|---|
| Verantwortlich für den Inhalt (§ 18 Abs. 2 MStV) | `<AUSFÜLLEN>` — nur bei journalistisch-redaktionellen Inhalten (Blog, News) |
| Teilnahme an Verbraucherschlichtung (§ 36 VSBG) | `<AUSFÜLLEN>` (i. d. R. „nein, nicht verpflichtet und nicht bereit") |
| Datenschutzbeauftragter benannt? | `<AUSFÜLLEN>` (Pflicht ab 20 Personen ständig mit automatisierter Verarbeitung) |
| Zuständige Aufsichtsbehörde | `<AUSFÜLLEN>` (Landesdatenschutzbehörde nach Sitz) |

## Standard-Stack (Vorbelegung für den Technik-Scan)

Häufig verwendet — der Scan prüft trotzdem jedes Projekt einzeln:

| Bereich | Dienst |
|---|---|
| Hosting | `<AUSFÜLLEN>` (z. B. Vercel, Firebase Hosting, Hetzner) |
| Datenbank / Auth | `<AUSFÜLLEN>` (z. B. Firebase, Neon/Postgres) |
| Mailversand | `<AUSFÜLLEN>` (z. B. Resend) |
| Analytics | `<AUSFÜLLEN>` (z. B. keins / Vercel Analytics / Plausible) |
| KI-APIs | `<AUSFÜLLEN>` (z. B. Anthropic, OpenAI) |
