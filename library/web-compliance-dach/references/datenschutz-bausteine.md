# Modul B — Datenschutzerklärung: Bausteine

**Regel: nur einbauen, was der Technik-Scan tatsächlich gefunden hat.** Eine Datenschutzerklärung, die Dienste beschreibt, die gar nicht laufen, ist selbst ein Verstoß gegen den Grundsatz der Richtigkeit (Art. 5 Abs. 1 lit. d DSGVO).

Jeder Baustein liefert: Zweck · Daten · **Rechtsgrundlage** · Empfänger · Drittland · Speicherdauer · AVV.

---

## 1. Pflicht-Rahmen (immer)

### 1.1 Verantwortlicher

```
Verantwortlicher im Sinne der DSGVO ist:
{{FIRMIERUNG}}, {{STRASSE_NR}}, {{PLZ_ORT}}
E-Mail: {{EMAIL}}
```
Bei benanntem DSB dessen Kontaktdaten ergänzen (Art. 37 DSGVO).

### 1.2 Server-Logfiles (immer, auch ohne jedes Tracking)

```
Beim Aufruf dieser Website werden durch den Hosting-Anbieter automatisch Informationen in
sogenannten Server-Logfiles gespeichert, die Ihr Browser automatisch übermittelt:

- Browsertyp und Browserversion
- verwendetes Betriebssystem
- Referrer-URL
- Hostname des zugreifenden Rechners
- Uhrzeit der Serveranfrage
- IP-Adresse

Eine Zusammenführung dieser Daten mit anderen Datenquellen wird nicht vorgenommen.
Die Erfassung erfolgt auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO. Der Betreiber hat ein
berechtigtes Interesse an der technisch fehlerfreien Darstellung und der Sicherheit seiner
Website; hierfür müssen Server-Logfiles erfasst werden.
Die Daten werden nach {{SPEICHERDAUER, üblich 7–30}} Tagen gelöscht.
```

### 1.3 Betroffenenrechte (immer)

```
Ihre Rechte

Auskunft (Art. 15 DSGVO) · Berichtigung (Art. 16) · Löschung (Art. 17) ·
Einschränkung der Verarbeitung (Art. 18) · Datenübertragbarkeit (Art. 20) ·
Widerspruch gegen Verarbeitungen auf Grundlage berechtigter Interessen (Art. 21) ·
Widerruf erteilter Einwilligungen mit Wirkung für die Zukunft (Art. 7 Abs. 3)

Wenden Sie sich hierzu formlos an {{EMAIL}}.

Unabhängig davon steht Ihnen ein Beschwerderecht bei einer Aufsichtsbehörde zu
(Art. 77 DSGVO), insbesondere bei der Behörde Ihres gewöhnlichen Aufenthaltsorts oder
am Sitz des Verantwortlichen: {{AUFSICHTSBEHOERDE}}.
```

### 1.4 SSL/TLS + Hinweis Datenübertragung im Internet

```
Diese Seite nutzt aus Sicherheitsgründen eine SSL- bzw. TLS-Verschlüsselung. Eine
verschlüsselte Verbindung erkennen Sie an „https://" in der Adresszeile Ihres Browsers.
Wir weisen darauf hin, dass die Datenübertragung im Internet Sicherheitslücken aufweisen
kann; ein lückenloser Schutz vor Zugriff durch Dritte ist nicht möglich.
```

---

## 2. Hosting

> Immer als **Auftragsverarbeitung** (Art. 28 DSGVO) darstellen. AVV muss abgeschlossen sein — beim Anbieter im Dashboard prüfbar.

### Vercel
```
Diese Website wird bei Vercel Inc., 340 S Lemon Ave #4133, Walnut, CA 91789, USA, gehostet.
Vercel verarbeitet dabei Verbindungsdaten (IP-Adresse, Zeitpunkt, aufgerufene Ressource,
User-Agent) zur Auslieferung der Seite. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO
(berechtigtes Interesse an einer sicheren und performanten Bereitstellung).
Mit Vercel besteht ein Auftragsverarbeitungsvertrag nach Art. 28 DSGVO. Die Übermittlung in
die USA wird auf die EU-Standardvertragsklauseln sowie die Zertifizierung von Vercel unter
dem EU-U.S. Data Privacy Framework gestützt.
Details: https://vercel.com/legal/privacy-policy
```
Läuft die Auslieferung über eine EU-Region, ergänzen: „Die Verarbeitung erfolgt primär in der Region {{REGION}} innerhalb der EU."

### Firebase Hosting / Google Cloud
```
Diese Website wird über Firebase Hosting bereitgestellt, einen Dienst der Google Ireland
Limited, Gordon House, Barrow Street, Dublin 4, Irland. Beim Aufruf werden Verbindungsdaten
einschließlich Ihrer IP-Adresse verarbeitet. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO.
Es besteht ein Auftragsverarbeitungsvertrag; für Übermittlungen in die USA gelten die
EU-Standardvertragsklauseln sowie die Zertifizierung von Google LLC unter dem
EU-U.S. Data Privacy Framework.
Details: https://firebase.google.com/support/privacy
```

### Hetzner / IONOS / All-Inkl / Strato (EU-Hoster)
```
Diese Website wird bei {{ANBIETER}}, {{ANSCHRIFT}}, gehostet. Die Server stehen in
Deutschland. Verarbeitet werden Verbindungsdaten zur technischen Bereitstellung.
Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Es besteht ein Auftragsverarbeitungsvertrag
nach Art. 28 DSGVO. Eine Übermittlung in Drittländer findet nicht statt.
```

### Netlify / Cloudflare Pages / AWS Amplify
Struktur wie Vercel, mit Sitz und Policy-Link des jeweiligen Anbieters; USA-Transfer immer über SCC + DPF begründen.

### Cloudflare als CDN/Proxy (zusätzlich zum Hosting)
```
Zur Absicherung und Beschleunigung nutzen wir das Content Delivery Network von Cloudflare,
Inc., 101 Townsend St., San Francisco, CA 94107, USA. Sämtlicher Datenverkehr wird über
Cloudflare-Server geleitet; dabei verarbeitet Cloudflare Verbindungsdaten inkl. IP-Adresse
zur Abwehr von Angriffen und zur Auslieferung von Inhalten. Rechtsgrundlage ist Art. 6
Abs. 1 lit. f DSGVO. Es besteht ein Auftragsverarbeitungsvertrag; die Übermittlung in die USA
ist durch EU-Standardvertragsklauseln abgesichert.
```

---

## 3. Schriftarten, Icons, Assets

### Google Fonts — LOKAL (Soll-Zustand)
```
Diese Seite nutzt zur einheitlichen Darstellung Schriftarten von Google (Google Fonts).
Die Schriftarten sind lokal auf unserem Server installiert. Eine Verbindung zu Servern von
Google findet dabei nicht statt.
```

### Google Fonts — CDN (Problem-Zustand)
> **Nicht als Textbaustein liefern, sondern beheben.** LG München I, 20.01.2022, 3 O 17493/20: Einbindung per CDN ohne Einwilligung verletzt das Persönlichkeitsrecht, Schadensersatz zugesprochen. Anleitung zur Lokalisierung: `einbau.md`.
> Ist die Lokalisierung ausnahmsweise unmöglich, ist die Einbindung **einwilligungspflichtig** (Art. 6 Abs. 1 lit. a) und muss hinter das Consent-Gate.

Gleiches gilt für **FontAwesome CDN**, **Google Material Icons**, **Adobe Typekit**, **unpkg/jsdelivr-Skripte** und extern eingebundene Bilder.

---

## 4. Analytics & Reichweitenmessung

### Google Analytics 4 — EINWILLIGUNGSPFLICHTIG
```
Diese Website nutzt Google Analytics 4, einen Webanalysedienst der Google Ireland Limited,
Gordon House, Barrow Street, Dublin 4, Irland.

Google Analytics verwendet Cookies und ähnliche Technologien, die eine Analyse Ihrer Nutzung
der Website ermöglichen. Erfasst werden unter anderem gekürzte IP-Adresse, Geräte- und
Browserinformationen, ungefährer Standort, aufgerufene Seiten, Verweildauer und
Interaktionen. Die IP-Anonymisierung ist in GA4 standardmäßig aktiviert.

Rechtsgrundlage ist ausschließlich Ihre Einwilligung nach Art. 6 Abs. 1 lit. a DSGVO in
Verbindung mit § 25 Abs. 1 TDDDG. Sie können Ihre Einwilligung jederzeit über die
Cookie-Einstellungen mit Wirkung für die Zukunft widerrufen.

Mit Google besteht ein Auftragsverarbeitungsvertrag. Eine Übermittlung von Daten in die USA
kann nicht ausgeschlossen werden; sie wird auf die EU-Standardvertragsklauseln und die
Zertifizierung von Google LLC unter dem EU-U.S. Data Privacy Framework gestützt.
Speicherdauer: {{2/14 Monate}}.
Details: https://policies.google.com/privacy
```

### Plausible / Matomo (self-hosted, cookielos) — meist einwilligungsfrei
```
Zur Reichweitenmessung nutzen wir {{Plausible Analytics / Matomo}}. Der Dienst arbeitet
cookiefrei und ohne Zugriff auf Informationen in Ihrem Endgerät im Sinne des § 25 TDDDG.
Es werden keine personenbezogenen Profile gebildet; IP-Adressen werden ausschließlich
gekürzt bzw. als nicht rückführbarer Hashwert verarbeitet und nicht gespeichert.
Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO — berechtigtes Interesse an einer
datensparsamen statistischen Auswertung der Websitenutzung.
{{Bei Plausible Cloud:}} Die Verarbeitung erfolgt auf Servern innerhalb der EU
(Plausible Insights OÜ, Estland); es besteht ein Auftragsverarbeitungsvertrag.
```
> Voraussetzung für „einwilligungsfrei": kein Cookie, kein localStorage, kein Fingerprinting. Prüfen, nicht behaupten.

### Vercel Web Analytics / Speed Insights
```
Wir nutzen Vercel Web Analytics bzw. Speed Insights der Vercel Inc. Der Dienst misst
Seitenaufrufe und Performancewerte ohne Cookies und ohne Erstellung geräteübergreifender
Profile; Besucher werden über einen täglich wechselnden, nicht umkehrbaren Hashwert
gezählt. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO.
```

### Meta Pixel / TikTok Pixel / LinkedIn Insight — IMMER einwilligungspflichtig
```
Nach Ihrer Einwilligung setzen wir den {{DIENST}} der {{ANBIETER + ANSCHRIFT}} ein. Damit
werden Ihre Interaktionen auf dieser Website erfasst und an {{ANBIETER}} übermittelt, um die
Wirksamkeit unserer Werbung zu messen und Ihnen interessenbasierte Werbung auszuspielen.
Dabei kann eine Zuordnung zu Ihrem Nutzerkonto bei {{PLATTFORM}} erfolgen.
Rechtsgrundlage ist Art. 6 Abs. 1 lit. a DSGVO i. V. m. § 25 Abs. 1 TDDDG. Der Widerruf ist
jederzeit über die Cookie-Einstellungen möglich. Wir sind mit {{ANBIETER}} gemeinsam
Verantwortliche im Sinne des Art. 26 DSGVO; die wesentlichen Inhalte der Vereinbarung sind
unter {{LINK}} abrufbar. Datenübermittlungen in die USA erfolgen auf Grundlage der
EU-Standardvertragsklauseln.
```

---

## 5. Backend, Datenbank, Auth

### Firebase (Firestore / Auth / Storage / Functions)
```
Für Datenhaltung{{, Nutzerkonten}} und Dateispeicherung nutzen wir Firebase, einen Dienst der
Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland.

Verarbeitet werden {{AUFZÄHLUNG: z. B. Name, E-Mail-Adresse, Buchungsdaten, hochgeladene
Dateien}} sowie technische Metadaten der Zugriffe.
{{Bei Firebase Authentication:}} Zur Anmeldung werden E-Mail-Adresse und ein
kryptografischer Hash des Passworts sowie Anmeldezeitpunkte gespeichert.

Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO, soweit die Verarbeitung zur Erfüllung eines
Vertrags oder vorvertraglicher Maßnahmen erforderlich ist, im Übrigen Art. 6 Abs. 1 lit. f
DSGVO (berechtigtes Interesse am sicheren Betrieb der Anwendung).

Mit Google besteht ein Auftragsverarbeitungsvertrag nach Art. 28 DSGVO. Die Speicherung
erfolgt in der Region {{REGION}}. Soweit Daten in die USA übermittelt werden, geschieht dies
auf Basis der EU-Standardvertragsklauseln sowie der Zertifizierung von Google LLC unter dem
EU-U.S. Data Privacy Framework.
Speicherdauer: {{ANGABE}}.
```
> Firebase legt für Auth/Analytics Werte im Endgerät ab → sofern nicht strikt für den vom Nutzer angeforderten Dienst erforderlich, ist § 25 TDDDG einschlägig und eine Einwilligung nötig.

### Supabase / Neon / PlanetScale / MongoDB Atlas
Struktur wie Firebase; Region angeben (EU-Region bevorzugen und dann explizit nennen — das erspart die gesamte Drittlandbegründung).

### Clerk / Auth0 / NextAuth
```
Zur Verwaltung von Benutzerkonten nutzen wir {{DIENST}} der {{ANBIETER + ANSCHRIFT}}.
Verarbeitet werden E-Mail-Adresse, {{ggf. Name, Profilbild}}, Anmeldezeitpunkte, IP-Adresse
und Geräteinformationen zur Absicherung des Kontos. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b
DSGVO (Bereitstellung des Nutzerkontos). Es besteht ein Auftragsverarbeitungsvertrag.
```

---

## 6. Kontakt, Formulare, Mailversand

### Kontakt- / Buchungsformular
```
Kontaktformular

Wenn Sie uns per Kontaktformular Anfragen zukommen lassen, werden Ihre Angaben aus dem
Anfrageformular einschließlich der dort angegebenen Kontaktdaten zwecks Bearbeitung der
Anfrage und für den Fall von Anschlussfragen bei uns gespeichert. Diese Daten geben wir nicht
ohne Ihre Einwilligung weiter.

Verarbeitet werden: {{FELDER EXAKT AUFZÄHLEN — Name, E-Mail, Telefon, Nachricht, Datum, ...}}

Die Verarbeitung erfolgt auf Grundlage von Art. 6 Abs. 1 lit. b DSGVO, sofern Ihre Anfrage
mit der Erfüllung eines Vertrags zusammenhängt oder zur Durchführung vorvertraglicher
Maßnahmen erforderlich ist. In allen übrigen Fällen beruht die Verarbeitung auf unserem
berechtigten Interesse an der effektiven Bearbeitung der an uns gerichteten Anfragen
(Art. 6 Abs. 1 lit. f DSGVO).

Die Daten verbleiben bei uns, bis Sie uns zur Löschung auffordern, Ihre Einwilligung
widerrufen oder der Zweck entfällt — spätestens nach {{FRIST}}. Zwingende gesetzliche
Bestimmungen, insbesondere handels- und steuerrechtliche Aufbewahrungsfristen, bleiben
unberührt.
```
> Im Formular selbst braucht es: Link auf die Datenschutzerklärung neben dem Absende-Button. Eine **Checkbox ist bei lit. b/f nicht nötig** und suggeriert fälschlich eine Einwilligung — nur bei Newsletter oder echter Einwilligung setzen.

### Resend / Brevo / Postmark / SendGrid (transaktionaler Mailversand)
```
Für den Versand von {{Bestätigungs- und Benachrichtigungs-E-Mails}} nutzen wir {{DIENST}}
der {{ANBIETER + ANSCHRIFT}}. Übermittelt werden die E-Mail-Adresse des Empfängers sowie der
Inhalt der Nachricht; der Anbieter verarbeitet zusätzlich Metadaten zum Versandstatus.
Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO bzw. Art. 6 Abs. 1 lit. f DSGVO
(zuverlässige Zustellung). Es besteht ein Auftragsverarbeitungsvertrag nach Art. 28 DSGVO.
{{Bei US-Anbietern:}} Die Übermittlung in die USA wird auf die EU-Standardvertragsklauseln
gestützt.
```

### Newsletter (Mailchimp / Brevo / CleverReach)
```
Newsletter

Für den Newsletterversand nutzen wir {{DIENST}} der {{ANBIETER + ANSCHRIFT}}. Wenn Sie den
Newsletter abonnieren möchten, benötigen wir Ihre E-Mail-Adresse sowie eine Bestätigung, dass
Sie mit dem Empfang einverstanden sind (Double-Opt-in). Zur Dokumentation der Einwilligung
speichern wir Anmeldezeitpunkt, Bestätigungszeitpunkt und IP-Adresse.

Rechtsgrundlage ist ausschließlich Ihre Einwilligung nach Art. 6 Abs. 1 lit. a DSGVO. Sie
können diese jederzeit über den Abmeldelink in jedem Newsletter widerrufen; die Rechtmäßigkeit
der bis zum Widerruf erfolgten Verarbeitung bleibt unberührt.

{{Bei Erfolgsmessung:}} Der Newsletter enthält ein Zählpixel, das Öffnungen und Klicks
erfasst und mit Ihrer E-Mail-Adresse verknüpft. Diese Auswertung ist Teil der Einwilligung.
```
> Erfolgsmessung braucht eine **eigene, separat erteilte** Einwilligung — nicht mit der Anmelde-Checkbox bündeln.

### Google reCAPTCHA
```
Zum Schutz vor automatisierten Anfragen setzen wir reCAPTCHA der Google Ireland Limited ein.
Dabei werden IP-Adresse, Verweildauer, Mausbewegungen und Geräteinformationen an Google
übermittelt und dort ausgewertet. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO
(Missbrauchsabwehr); soweit dabei auf Informationen in Ihrem Endgerät zugegriffen wird,
zusätzlich Ihre Einwilligung nach § 25 Abs. 1 TDDDG.
```
> Datensparsamere Alternativen ohne Consent-Bedarf: Cloudflare Turnstile, Friendly Captcha, Honeypot-Feld.

---

## 7. Zahlungsdienste

### Stripe
```
Zahlungen wickeln wir über Stripe Payments Europe Ltd., 1 Grand Canal Street Lower, Dublin 2,
Irland, ab. Bei einer Zahlung werden die von Ihnen eingegebenen Zahlungsdaten unmittelbar an
Stripe übermittelt; wir selbst erhalten keine vollständigen Kartendaten. Verarbeitet werden
Name, E-Mail-Adresse, Rechnungs- und Zahlungsdaten, Betrag, IP-Adresse sowie Angaben zur
Betrugsprävention.
Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung); für die
Betrugsprävention Art. 6 Abs. 1 lit. f DSGVO. Übermittlungen an die Stripe Inc. in den USA
erfolgen auf Grundlage der EU-Standardvertragsklauseln.
Details: https://stripe.com/de/privacy
```

### PayPal
```
Bei Zahlung über PayPal werden Ihre Zahlungsdaten an die PayPal (Europe) S.à r.l. et Cie,
S.C.A., 22-24 Boulevard Royal, 2449 Luxemburg, übermittelt. Rechtsgrundlage ist Art. 6 Abs. 1
lit. b DSGVO; zur Betrugsprävention und Bonitätsprüfung zusätzlich Art. 6 Abs. 1 lit. f
DSGVO. PayPal kann Daten an Auskunfteien übermitteln.
Details: https://www.paypal.com/de/webapps/mpp/ua/privacy-full
```

---

## 8. Eingebettete Inhalte (iframes)

> **Alle einwilligungspflichtig** — der Aufruf lädt beim Rendern bereits Daten zum Drittanbieter. Lösung: 2-Klick / Shariff-Prinzip oder Consent-Gate. Siehe `einbau.md`.

### YouTube (erweiterter Datenschutzmodus)
```
Diese Website bindet Videos der YouTube-Plattform ein. Betreiber ist die Google Ireland
Limited. Wir nutzen YouTube im erweiterten Datenschutzmodus (youtube-nocookie.com), der nach
Angaben von YouTube dazu führt, dass keine Cookies für personalisierte Werbung gesetzt
werden, bevor Sie ein Video starten. Beim Start eines Videos wird eine Verbindung zu den
Servern von YouTube hergestellt und Ihre IP-Adresse übermittelt; sind Sie in Ihrem
YouTube-Konto eingeloggt, kann YouTube Ihr Surfverhalten Ihrem Profil zuordnen.
Die Einbettung erfolgt erst nach Ihrer Einwilligung, Art. 6 Abs. 1 lit. a DSGVO i. V. m.
§ 25 Abs. 1 TDDDG.
```

### Google Maps
```
Diese Seite bindet Kartenmaterial von Google Maps ein (Google Ireland Limited). Zur Nutzung
ist die Speicherung und Übermittlung Ihrer IP-Adresse an Google erforderlich; die
Verarbeitung kann auch auf Servern in den USA erfolgen. Die Einbindung erfolgt erst nach
Ihrer Einwilligung, Art. 6 Abs. 1 lit. a DSGVO i. V. m. § 25 Abs. 1 TDDDG.
```
> Datensparsame Alternative ohne Consent: statisches Kartenbild + Link „Route in Google Maps öffnen", oder OpenStreetMap self-hosted.

### Vimeo, Spotify, SoundCloud, Instagram-Embeds, Calendly
Gleiche Struktur, Anbieter und Anschrift austauschen; immer Art. 6 Abs. 1 lit. a + § 25 TDDDG.

---

## 9. KI-Dienste — Datenschutzteil

> Der Transparenz-/Kennzeichnungsteil steht in `ai-act.md`. Hier geht es nur um die **Datenverarbeitung**.

### Nutzereingaben gehen an eine KI-API (OpenAI / Anthropic / Google / Mistral)
```
Einsatz von KI-Diensten

{{BESCHREIBUNG DER FUNKTION, z. B. „Unser Chat-Assistent beantwortet Fragen zu unserem
Angebot."}} Zur Beantwortung werden Ihre Eingaben an {{ANBIETER, z. B. Anthropic PBC,
548 Market St, San Francisco, CA 94104, USA}} übermittelt und dort verarbeitet.

Übermittelt werden: der von Ihnen eingegebene Text{{, hochgeladene Dateien}} sowie
technische Metadaten der Anfrage. Bitte geben Sie in dieses Feld keine besonderen Kategorien
personenbezogener Daten im Sinne des Art. 9 DSGVO (etwa Gesundheitsdaten) und keine
Zugangsdaten ein.

Rechtsgrundlage ist {{Art. 6 Abs. 1 lit. b DSGVO, soweit die Funktion zur Erbringung der von
Ihnen angeforderten Leistung erforderlich ist / Art. 6 Abs. 1 lit. a DSGVO — Ihre
Einwilligung, die Sie vor der ersten Nutzung erteilen}}.

Mit {{ANBIETER}} besteht ein Auftragsverarbeitungsvertrag nach Art. 28 DSGVO. Der Anbieter
verwendet die über die Schnittstelle übermittelten Daten vertraglich nicht zum Training
seiner Modelle. Die Übermittlung in die USA erfolgt auf Grundlage der
EU-Standardvertragsklauseln{{ sowie der Zertifizierung des Anbieters unter dem EU-U.S. Data
Privacy Framework}}. Die Speicherdauer beim Anbieter beträgt {{ANGABE, z. B. bis zu 30 Tage
zur Missbrauchskontrolle}}.

Eine automatisierte Entscheidungsfindung mit rechtlicher Wirkung Ihnen gegenüber im Sinne
des Art. 22 DSGVO findet nicht statt.
```

**Vor dem Generieren prüfen und beim User nachfragen:**
1. Ist der **AVV** beim Anbieter tatsächlich abgeschlossen? (OpenAI/Anthropic: DPA im Dashboard aktivieren — passiert nicht automatisch.)
2. Ist **Zero Data Retention** oder eine verkürzte Aufbewahrung vereinbart? Sonst korrekte Frist angeben.
3. Läuft der Call **serverseitig**? Ein API-Key im Client-Bundle ist ein Sicherheitsvorfall, kein Datenschutztext-Problem — sofort melden.
4. Trifft die KI Entscheidungen über Personen (Bewerbung, Bonität, Preis)? Dann Art. 22 DSGVO prüfen und ggf. AI-Act-Hochrisiko-Einstufung ansprechen.

### KI nur beim Bauen der Seite verwendet (kein Live-System)
Kein Datenschutz-Baustein nötig — das ist reine Transparenz, siehe `ai-act.md`.

---

## 10. Cookies & lokale Speicherung — Übersichtstabelle

Die Erklärung braucht eine konkrete Auflistung, keine Pauschalfloskel:

```
| Name | Anbieter | Zweck | Speicherdauer | Typ |
|---|---|---|---|---|
| {{name}} | {{wir/Dritter}} | {{Zweck}} | {{Dauer}} | {{notwendig / Statistik / Marketing}} |
```

```
Technisch notwendige Cookies werden auf Grundlage von § 25 Abs. 2 Nr. 2 TDDDG ohne
Einwilligung gesetzt, da sie für den von Ihnen ausdrücklich gewünschten Dienst unbedingt
erforderlich sind. Alle übrigen Cookies und vergleichbaren Technologien setzen wir nur nach
Ihrer Einwilligung ein (§ 25 Abs. 1 TDDDG, Art. 6 Abs. 1 lit. a DSGVO). Sie können Ihre
Auswahl jederzeit über die Cookie-Einstellungen ändern.
```
> `localStorage`, `sessionStorage`, IndexedDB und Fingerprinting fallen genauso unter § 25 TDDDG wie Cookies. „Wir nutzen keine Cookies, nur localStorage" ist **kein** Argument.
