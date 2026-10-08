# mjoar.com v4 · Seitenbau (One-Pager)

Die Seiten unter `/`, `/de/` und `/en/` werden aus diesem Ordner erzeugt. GitHub Pages liefert `_build/` nicht aus.

| Datei | Zweck |
|---|---|
| `texte_v4.py` | Alle Seitentexte, wortgleich aus `MJOAR_WEB_COPY_v4.md`, dazu Alt-Texte und Bedienetiketten (`ALT`, aus v3 übernommen) |
| `site.py` | Seitenbau. Enthält die **eine Konstante `KAUFEN`** (Links je Farbe, DE amazon.de, EN amazon.co.uk) und `HERO_BILD` |
| `bilder.py` | Bildexport aus dem Shooting nach `assets/web/` (WebP 480/960/1600/2400). Die Originale werden nur gelesen |
| `pruefen.py` | Wortgleichheit in beiden Richtungen gegen Copy v4, Überschriften ohne Schlusspunkt, Rechtstexte, Verbotsliste, Links und Anker, Kaufen-Marktplatz |
| `alt/` | Bisherige `impressum.html` und `datenschutz.html`; ihr Inhalt wird unverändert übernommen |

**Reihenfolge:** `python _build/bilder.py` (nur bei neuen Bildern), dann `python _build/site.py`, dann `python _build/pruefen.py`.

**Aufbau:** je Sprache eine Seite mit Ankern: Hero, Einstieg (`#einstieg`/`#intro`), Produkt (`#lun`), Details (`#details`), Gut zu wissen (`#gut-zu-wissen`/`#good-to-know`), Milch und Latte Art (`#latte-art`), Über uns (`#ueber-uns`/`#about`). Die alten Unterseiten (`/de/lun-350/` usw.) sind Weiterleitungen auf den passenden Anker; Impressum und Datenschutz bleiben eigene Seiten.

**Hero-Bild:** Standard ist 0284 (Familienbild). `MJOAR_HERO=0420` beim Bauen zeigt die Alternative (an der Maschine). Dauerhaft umstellen: `HERO_BILD` in `site.py`.
