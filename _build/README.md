# mjoar.com · Seitenbau

Die Seiten unter `/`, `/de/` und `/en/` werden aus diesem Ordner erzeugt. GitHub Pages liefert `_build/` nicht aus.

| Datei | Zweck |
|---|---|
| `vorlagen/startseite-de.html` | **DE-Startseite** (`/` und `/de/`), Vorlage aus dem von Thorsten abgenommenen Entwurf v70 (13.11.2026). Texte und Gestaltung stehen hier; `site.py` setzt Kopf (Titel, Meta, OG, hreflang), Kauflinks, Brevo-Ziel, Rechtslinks und das Logo ein (Platzhalter `{{…}}`, leere `svg[data-logo]`) |
| `entwurf/startseite-v70.html` | Der abgenommene Entwurf unverändert, nur als Referenz für `pruefen.py` (Wortgleichheit) |
| `texte_v4.py` | Texte des EN-One-Pagers, der Rechtsseiten und der Weiterleitungen, wortgleich aus `MJOAR_WEB_COPY_v4.md`, dazu Alt-Texte und Bedienetiketten (`ALT`) |
| `site.py` | Seitenbau. Enthält die **eine Konstante `KAUFEN`** (Links je Farbe, DE amazon.de mit Attribution-Tag, EN amazon.co.uk), `BREVO`, `HERO_BILD` (EN), `START_DE_META` |
| `bilder.py` | Bildexport aus dem Shooting nach `assets/web/` (WebP 480/960/1600/2400). Die Originale werden nur gelesen |
| `pruefen.py` | EN/Rechtsseiten: Wortgleichheit gegen Copy v4, Überschriften, Verbotsliste. DE-Startseite: Wortgleichheit gegen den Entwurf, Marke nur als Logo. Alle: Rechtstexte, Links und Anker, Kaufen-Marktplatz und Attribution, Brevo, GoatCounter, keine Google Fonts, Videos |
| `alt/` | Bisherige `impressum.html` und `datenschutz.html`; ihr Inhalt wird unverändert übernommen |

**Reihenfolge:** `python _build/bilder.py` (nur bei neuen Bildern), dann `python _build/site.py`, dann `python _build/pruefen.py`.

**Aufbau DE:** Startseite mit Ankern Produkte (`#produkte`), LUN 350 (`#lun`), Im Detail (`#details`), Über uns (`#uns`). Die alten DE-Unterseiten leiten dorthin (`/de/lun-350/` → `#lun`, `/de/ueber-uns/` → `#uns`); `/de/milch-und-latte-art/` und `/latte-art/` leiten auf die Startseite (statische Seite mit `meta refresh` und `rel=canonical`, GitHub Pages kann keine Server-Weiterleitung).

**Aufbau EN (unverändert v4):** One-Pager mit Hero, Intro (`#intro`), Produkt (`#lun`), Details (`#details`), Good to know (`#good-to-know`), Milk and latte art (`#latte-art`), About (`#about`); alte EN-Unterseiten sind Weiterleitungen auf den passenden Anker.

**Assets der DE-Startseite:** neue Dateien in `assets/start/` (Freisteller, Skizzen, Zeichnung AORA, Schattenvideos), bereits vorhandene Bilder aus `assets/web/` (byte-gleich mit dem Entwurf).
- Videos: `schatten.mp4` (Startbild) und `schatten_blaetter.mp4` (fester Hintergrund) wie im Entwurf; mobil (≤ 760 px) `*_mobil.mp4`, erzeugt mit ffmpeg: `-an -vf scale=1120:-2:flags=lanczos -c:v libx264 -preset slow -crf 28 -profile:v high -pix_fmt yuv420p -movflags +faststart` (Ziel < 1,5 MB). Die Auswahl läuft über `<source media>`; bei `prefers-reduced-motion: reduce` passt keine Quelle, es wird kein Video geladen und das Standbild bleibt stehen.
- Schriften: Jost (300–500) und Manrope (400–600) selbst gehostet in `assets/fonts/` (`jost-latin.woff2`, `manrope-latin.woff2`). Quelle: variable WOFF2 von Google Fonts (Subset latin), Gewichtsachse mit fontTools `varLib.instancer` auf die genutzten Schnitte gekürzt. Lizenz SIL OFL 1.1 (`assets/fonts/OFL.txt`).

**Hero-Bild EN:** Standard ist 0284 (Familienbild). `MJOAR_HERO=0420` beim Bauen zeigt die Alternative (an der Maschine). Dauerhaft umstellen: `HERO_BILD` in `site.py`.
