# mjoar.com · Seitenbau

Die Seiten unter `/`, `/de/` und `/en/` werden aus diesem Ordner erzeugt. GitHub Pages liefert `_build/` nicht aus.

| Datei | Zweck |
|---|---|
| `vorlagen/startseite-de.html` | **DE-Startseite** (`/` und `/de/`), Vorlage aus dem von Thorsten abgenommenen Entwurf v70 (13.11.2026). Texte und Gestaltung stehen hier; `site.py` setzt Kopf (Titel, Meta, OG, hreflang), Kauflinks, Brevo-Ziel, Rechtslinks und das Logo ein (Platzhalter `{{…}}`, leere `svg[data-logo]`) |
| `vorlagen/startseite-en.html` | **EN-Startseite** (`/en/`): die DE-Vorlage mit britisch-englischen Texten (14.11.2026), gleicher Aufbau, gleicher Stil. Platzhalter wie DE, dazu `{{SHOP}}` (UK hat keinen Markenshop: UK-Eltern-ASIN) |
| `entwurf/startseite-v70.html` | Der abgenommene Entwurf unverändert, nur als Referenz für `pruefen.py` (Wortgleichheit) |
| `texte_v4.py` | Nur noch: Titel der Weiterleitungen (Copy v4), Titel der Rechtsseiten, EN-Hinweis „Legal text in German.“, Alt-Text des Teilen-Bilds. Der EN-One-Pager v4 ist durch die EN-Startseite ersetzt |
| `site.py` | Seitenbau. Enthält die **eine Konstante `KAUFEN`** (Links je Farbe, DE amazon.de mit Attribution-Tag, EN amazon.co.uk ohne Tag, UK-Eltern-ASIN B0HLWVCFC3), `SHOP`, `BREVO`, `START_META` (DE/EN), `RECHT_CSS` |
| `bilder.py` | Bildexport aus dem Shooting nach `assets/web/` (WebP 480/960/1600/2400). Die Originale werden nur gelesen |
| `pruefen.py` | DE-Startseite: Wortgleichheit gegen den Entwurf, Marke nur als Logo. EN-Startseite: gleicher Aufbau/Stil wie DE, Marke nur als Logo, keine deutschen Reste, Negativliste, nur amazon.co.uk ohne Tag, canonical/hreflang, DE · EN. Rechtsseiten: Kopf/Fuß/Stil wie die Startseite, Rechtstext byte-gleich mit `alt/` und origin/main. Weiterleitungen: Titel aus Copy v4. Alle: Links und Anker, Brevo, GoatCounter, keine Google Fonts, Videos |
| `alt/` | Bisherige `impressum.html` und `datenschutz.html`; ihr Inhalt wird unverändert übernommen |

**Reihenfolge:** `python _build/bilder.py` (nur bei neuen Bildern), dann `python _build/site.py`, dann `python _build/pruefen.py`.

**Aufbau DE:** Startseite mit Ankern Produkte (`#produkte`), LUN 350 (`#lun`), Im Detail (`#details`), Über uns (`#uns`). Die alten DE-Unterseiten leiten dorthin (`/de/lun-350/` → `#lun`, `/de/ueber-uns/` → `#uns`); `/de/milch-und-latte-art/` und `/latte-art/` leiten auf die Startseite (statische Seite mit `meta refresh` und `rel=canonical`, GitHub Pages kann keine Server-Weiterleitung).

**Aufbau EN:** wie DE, Anker Products (`#products`), LUN 350 (`#lun`), In detail (`#details`), About us (`#about`). Alte EN-Unterseiten leiten weiter: `/en/lun-350/` → `#lun`, `/en/about/` → `#about`, `/en/milk-and-latte-art/` → `/en/`.

**Rechtsseiten** (`/de/impressum/`, `/de/datenschutz/`, `/en/imprint/`, `/en/privacy/`): Kopf, Fuß und Stil aus der Startseite derselben Sprache (`site.py` schneidet sie aus der gefüllten Vorlage), dazu `RECHT_CSS` für die Textspalte. Der Rechtstext (`article.legal-card`) kommt unverändert aus `alt/`; EN zeigt den deutschen Text mit `lang="de"` und dem Hinweis „Legal text in German.“. `/impressum.html` und `/datenschutz.html` sind Weiterleitungen auf die DE-Seiten.

**Assets der DE-Startseite:** neue Dateien in `assets/start/` (Freisteller, Skizzen, Zeichnung AORA, Schattenvideos), bereits vorhandene Bilder aus `assets/web/` (byte-gleich mit dem Entwurf).
- Videos: `schatten.mp4` (Startbild) und `schatten_blaetter.mp4` (fester Hintergrund) wie im Entwurf; mobil (≤ 760 px) `*_mobil.mp4`, erzeugt mit ffmpeg: `-an -vf scale=1120:-2:flags=lanczos -c:v libx264 -preset slow -crf 28 -profile:v high -pix_fmt yuv420p -movflags +faststart` (Ziel < 1,5 MB). Die Auswahl läuft über `<source media>`; bei `prefers-reduced-motion: reduce` passt keine Quelle, es wird kein Video geladen und das Standbild bleibt stehen.
- Schriften: Jost (300–500) und Manrope (400–600) selbst gehostet in `assets/fonts/` (`jost-latin.woff2`, `manrope-latin.woff2`). Quelle: variable WOFF2 von Google Fonts (Subset latin), Gewichtsachse mit fontTools `varLib.instancer` auf die genutzten Schnitte gekürzt. Lizenz SIL OFL 1.1 (`assets/fonts/OFL.txt`).

