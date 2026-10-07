# mjoar.com v2 · Seitenbau

Die Seiten unter `/`, `/de/` und `/en/` werden aus diesem Ordner erzeugt. GitHub Pages liefert `_build/` nicht aus.

| Datei | Zweck |
|---|---|
| `texte_v3.py` | Alle Seitentexte, wortgleich aus `MJOAR_WEB_COPY_v3.md`, dazu Alt-Texte und Bedienetiketten |
| `site.py` | Seitenbau. Enthält die **eine Konstante `KAUFEN`** (Links je Farbe) und `HERO_BILD` |
| `bilder.py` | Bildexport aus dem Shooting nach `assets/web/` (WebP 480/960/1600/2400). Die Originale werden nur gelesen |
| `pruefen.py` | Wortgleichheit in beiden Richtungen, Rechtstexte, Verbotsliste, Links |
| `alt/` | Bisherige `impressum.html` und `datenschutz.html`; ihr Inhalt wird unverändert übernommen |

**Reihenfolge:** `python _build/bilder.py` (nur bei neuen Bildern), dann `python _build/site.py`, dann `python _build/pruefen.py`.

**EN auf amazon.co.uk umstellen:** In `site.py` die Zeile `KAUFEN["en"] = KAUFEN["de"]` durch die UK-Links ersetzen und neu bauen.

**Hero-Bild:** Standard ist 0420 1 (an der Maschine). `MJOAR_HERO=0284` beim Bauen zeigt die Alternative (Familienbild). Dauerhaft umstellen: `HERO_BILD` in `site.py`.
