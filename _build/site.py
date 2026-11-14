# mjoar.com: Startseiten DE (/ und /de/) und EN (/en/) aus den Vorlagen _build/vorlagen/startseite-de.html (Entwurf v70,
# von Thorsten abgenommen 13.11.2026, Referenz _build/entwurf/startseite-v70.html) und _build/vorlagen/startseite-en.html
# (britisch-englische Fassung derselben Seite, gleicher Aufbau, 14.11.2026). Impressum und Datenschutz im Design der
# Startseite (gleicher Kopf, Fuß, Stil); der Rechtstext selbst wird unverändert aus den bisherigen Dateien (_build/alt/)
# übernommen. Die alten Unterseiten bleiben als schlanke Weiterleitungen auf den passenden Anker.
#   python _build/site.py        (aus dem Worktree)
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texte_v4 import ALT, EN_HINWEIS, RECHT_TITEL, T  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://mjoar.com"

# ---------------------------------------------------------------------------------------------------------------
# Kaufen: die eine zentrale Konstante. DE auf amazon.de, EN auf amazon.co.uk (UK kaufbar seit 08.10.2026),
# gleiche ASIN je Farbe; DE-Links mit Amazon-Attribution-Tag (Kampagne Website mjoar.com DE, 22.10.2026). Für UK gibt es
# kein Attribution-Tag im Repo, die UK-Links bleiben ohne Tag. "ohne" = Kanne ohne Farbwahl.
# UK-Eltern-ASIN ist B0HLWVCFC3 (nicht die DE-Eltern-ASIN B0H9ZS73SW: amazon.co.uk/dp/B0H9ZS73SW liefert 404, geprüft
# 14.11.2026 im Browser; B0HLWVCFC3 öffnet die LUN in Juniper mit allen vier Farben).
KAUFEN = {
    "de": {
        "juniper": "https://www.amazon.de/dp/B0HB116F83?maas=maas_adg_FEA56D9EA32C439D4BBBF6D72EA46D7A_afap_abs&ref_=aa_maas&tag=maas",
        "linen": "https://www.amazon.de/dp/B0HB16137F?maas=maas_adg_EF864ED8531FD89BDAEC4153DDB0C37A_afap_abs&ref_=aa_maas&tag=maas",
        "onyx": "https://www.amazon.de/dp/B0H9ZWMGWR?maas=maas_adg_B3CBB3AD96387F4F2894A9EF3F220F14_afap_abs&ref_=aa_maas&tag=maas",
        "steel": "https://www.amazon.de/dp/B0HB15MCKJ?maas=maas_adg_00DEC5090B791208EBE9EBA077008C3E_afap_abs&ref_=aa_maas&tag=maas",
        "ohne": "https://www.amazon.de/dp/B0H9ZS73SW?maas=maas_adg_E3BE5165C9E1C96682CC16F557CAAF91_afap_abs&ref_=aa_maas&tag=maas",
    },
    "en": {
        "juniper": "https://www.amazon.co.uk/dp/B0HB116F83",
        "linen": "https://www.amazon.co.uk/dp/B0HB16137F",
        "onyx": "https://www.amazon.co.uk/dp/B0H9ZWMGWR",
        "steel": "https://www.amazon.co.uk/dp/B0HB15MCKJ",
        "ohne": "https://www.amazon.co.uk/dp/B0HLWVCFC3",
    },
}
FARBEN = ["juniper", "linen", "onyx", "steel"]
# Markenshop: amazon.de/mjoar (DE-Vorlage, fest). Auf amazon.co.uk gibt es keinen Markenshop (amazon.co.uk/mjoar = 404,
# die Marke verlinkt dort nur auf eine Suche, geprüft 14.11.2026): EN nimmt die UK-Eltern-ASIN.
SHOP = {"de": "https://www.amazon.de/mjoar", "en": KAUFEN["en"]["ohne"]}
PDF = "/assets/docs/MJOAR_LUN350_Sicherheitshinweise_GPSR.pdf"

# Brevo-Formular unverändert (Double-Opt-in, Datenschutz Abschnitt 3)
BREVO = ("https://d3c20ae3.sibforms.com/serve/MUIFAJzjIZxfPKrfySr11g9GS6FoIFy8Hf1FJUUtNteGWoC1pQTypKM_fGkiPmSmH3fNQt-"
         "S0QhFMnKht-sU9mNEjMYv96tRuEYFTdQdqRRnmTJgS5l1kR402BulG2FacudUzQDDTpNfegGB-z88HKXQK3AENdrkUadGALIvMKzcjBBD_Yo"
         "oeWVD9a7Mem3rWsTYv6KGRAxlMiuvXA==")

PFADE = {
    "start": {"de": "/de/", "en": "/en/"},
    "impressum": {"de": "/de/impressum/", "en": "/en/imprint/"},
    "datenschutz": {"de": "/de/datenschutz/", "en": "/en/privacy/"},
}

# Alte Unterseiten → Anker der neuen Startseiten. DE: #produkte, #lun, #details, #uns. EN: #products, #lun, #details,
# #about. Alte Anker der Produktseite werden mitgenommen. Milch und Latte Art gibt es auf den neuen Seiten nicht mehr;
# die alten Latte-Art-Adressen leiten auf die Startseite.
_LUN_ALT = {"de": {"#im-detail": "#details", "#daten": "#lun", "#box": "#details", "#fragen": "#lun",
                   "#entstehung": "#uns", "#kaufen": "#lun"},
            "en": {"#im-detail": "#details", "#daten": "#lun", "#box": "#details", "#fragen": "#lun",
                   "#entstehung": "#about", "#kaufen": "#lun"}}
for _l in _LUN_ALT:
    _LUN_ALT[_l].update({f"#{f}": "#lun" for f in FARBEN})
WEITERLEITUNGEN = [
    # (alter Pfad, Sprache, Ziel (Pfad + Anker), Titel aus der Navigation der Copy, Ankerzuordnung)
    ("/de/lun-350/", "de", "/de/#lun", T["de"]["nav"][0][1], _LUN_ALT["de"]),
    ("/de/milch-und-latte-art/", "de", "/de/", T["de"]["nav"][2][1], {}),
    ("/de/ueber-uns/", "de", "/de/#uns", T["de"]["nav"][3][1], {}),
    ("/en/lun-350/", "en", "/en/#lun", T["en"]["nav"][0][1], _LUN_ALT["en"]),
    ("/en/milk-and-latte-art/", "en", "/en/", T["en"]["nav"][2][1], {}),
    ("/en/about/", "en", "/en/#about", T["en"]["nav"][3][1], {}),
    # Latte-Art-Unterseite entfernt (Auftrag 13.11.): statische Weiterleitung auf die Startseite, kanonisch auf /
    ("/latte-art/", "de", "/", T["de"]["nav"][2][1], {}),
]

e = html.escape

LOGO = open(os.path.join(ROOT, "assets", "web", "logo.svg"), encoding="utf-8").read().strip()

# ---------------------------------------------------------------------------------------------------------------
# Startseiten DE und EN. Die Vorlagen enthalten Texte und Gestaltung; site.py setzt Kopf (Titel, Meta, OG, hreflang),
# Kauflinks, Brevo-Ziel, Rechtslinks und das Logo ein (Platzhalter {{…}}, leere svg[data-logo]).
# Begründung eigene Vorlagen statt texte_v4/Abschnittsfunktionen: Aufbau, Stil und Texte sind komplett neu und stammen
# nicht aus Copy v4. Die EN-Vorlage ist die DE-Vorlage mit übersetzten Texten (pruefen.py sichert gleichen Aufbau).

VORLAGE_START = {l: os.path.join(ROOT, "_build", "vorlagen", f"startseite-{l}.html") for l in ["de", "en"]}
# Titel und Beschreibung: nur Sätze aus dem Hero der Seite (DE: Thorsten 14.11.: LUN-Satz raus; EN: dieselben Sätze).
START_META = {
    "de": ("MJØÅR · Schöne Dinge für deine Kaffee-Ecke",
           "Schöne Dinge für deine Kaffee-Ecke. Klares Design, ruhige Farben, kunststofffrei verpackt."),
    "en": ("MJØÅR · Beautiful things for your coffee corner",
           "Beautiful things for your coffee corner. Clear lines, calm colours, plastic-free packaging."),
}
START_DE_META = START_META["de"]
OG_LOCALE = {"de": "de_DE", "en": "en_GB"}
# Teilen-Bild: vorhandenes Produktbild (Familie 0284, alle vier Farben), 1200 × 630
OG_BILD = ("/assets/web/og-familie.jpg", 1200, 630)
ZAEHLER = '<script data-goatcounter="https://mjoar.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>'

_LOGO_VIEWBOX = re.search(r'viewBox="([^"]+)"', LOGO).group(1)
_LOGO_INNEN = re.sub(r"^<svg[^>]*>|</svg>$", "", LOGO)


def logos_einbetten(seite_html):
    """Jedes leere svg[data-logo] der Vorlage bekommt das Logo eingebettet (statt fetch('logo.svg') im Entwurf).
    Farbe kommt über currentColor aus dem CSS (Kopf grün, sonst Schriftfarbe)."""
    def setzen(m):
        return (f'<svg data-logo{m.group(1)} viewBox="{_LOGO_VIEWBOX}" xmlns="http://www.w3.org/2000/svg" focusable="false">'
                f"{_LOGO_INNEN}</svg>")
    neu, n = re.subn(r'<svg data-logo([^>]*?) viewBox="0 0 10 2"></svg>', setzen, seite_html)
    if n == 0:
        raise SystemExit("Startseite: kein svg[data-logo] in der Vorlage gefunden")
    return neu


def kopf_meta(lang, key, titel, beschreibung, kanonisch):
    """<head>-Inhalt: Startseiten mit Beschreibung, OG und Twitter-Card; Rechtsseiten noindex ohne OG."""
    url = SITE + kanonisch
    alternates = "".join(f'\n  <link rel="alternate" hreflang="{l}" href="{SITE}{PFADE[key][l]}">' for l in ["de", "en"])
    x_default = f"{SITE}/" if key == "start" else f"{SITE}{PFADE[key]['de']}"
    if beschreibung:
        og_pfad, og_b, og_h = OG_BILD
        og_alt = ALT[lang]["hero_0284"]
        andere = "en" if lang == "de" else "de"
        meta = f"""
  <meta name="description" content="{e(beschreibung)}">
  <link rel="canonical" href="{url}">{alternates}
  <link rel="alternate" hreflang="x-default" href="{x_default}">
  <meta property="og:type" content="website">
  <meta name="p:domain_verify" content="a9879c5ef5fd9a2b14fa6ac4ca45da7b">
  <meta property="og:site_name" content="MJØÅR">
  <meta property="og:title" content="{e(titel)}">
  <meta property="og:description" content="{e(beschreibung)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}{og_pfad}">
  <meta property="og:image:width" content="{og_b}">
  <meta property="og:image:height" content="{og_h}">
  <meta property="og:image:alt" content="{e(og_alt)}">
  <meta property="og:locale" content="{OG_LOCALE[lang]}">
  <meta property="og:locale:alternate" content="{OG_LOCALE[andere]}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(titel)}">
  <meta name="twitter:description" content="{e(beschreibung)}">
  <meta name="twitter:image" content="{SITE}{og_pfad}">
  <meta name="twitter:image:alt" content="{e(og_alt)}">"""
    else:
        meta = f"""
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{url}">{alternates}
  <link rel="alternate" hreflang="x-default" href="{x_default}">"""
    return f"""  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(titel)}</title>{meta}
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/jost-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>"""


def vorlage_fuellen(lang, kopf_html):
    """Vorlage der Startseite mit allen Platzhaltern gefüllt (Logos noch leer)."""
    werte = {"KOPF": kopf_html, "ZAEHLER": ZAEHLER, "BREVO": e(BREVO), "PDF": PDF,
             "IMPRESSUM": PFADE["impressum"][lang], "DATENSCHUTZ": PFADE["datenschutz"][lang]}
    werte.update({f"KAUFEN_{f}": e(KAUFEN[lang][f]) for f in FARBEN})
    if lang != "de":
        werte["SHOP"] = e(SHOP[lang])  # DE-Vorlage hat den Markenshop fest im Text (Entwurf v70)
    seite_html = open(VORLAGE_START[lang], encoding="utf-8").read()
    for k, v in werte.items():
        if "{{" + k + "}}" not in seite_html:
            raise SystemExit(f"Startseite {lang}: Platzhalter {{{{{k}}}}} fehlt in der Vorlage")
        seite_html = seite_html.replace("{{" + k + "}}", v)
    if "{{" in seite_html:
        raise SystemExit(f"Startseite {lang}: offener Platzhalter " + re.search(r"\{\{[^}]*\}\}", seite_html).group(0))
    return seite_html


def startseite(lang, kanonisch):
    titel, beschreibung = START_META[lang]
    return logos_einbetten(vorlage_fuellen(lang, kopf_meta(lang, "start", titel, beschreibung, kanonisch)))


def startseite_de(kanonisch):
    return startseite("de", kanonisch)


# ---------------------------------------------------------------------------------------------------------------
# Rechtsseiten: Kopf, Fuß und Stil aus der Startseite derselben Sprache, Rechtstext unverändert.

def recht_aus_altdatei(datei):
    """Inhalt der bisherigen Rechtsseite (article.legal-card) unverändert übernehmen."""
    roh = open(os.path.join(ROOT, "_build", "alt", datei), encoding="utf-8").read()
    a = roh.index('<article class="legal-card">')
    b = roh.index("</article>", a) + len("</article>")
    return roh[a:b]


# Inhaltliche Änderung am Datenschutz seit v2 (Fable 07.10.): Die Seite speichert keine Sprachwahl im Browser
# (eigene URLs je Sprache), der Absatz zu mjoar_lang entfällt. Sonst unverändert.
DATENSCHUTZ_ENTFAELLT = re.compile(r"\s*<p>\s*Für die Sprachwahl zwischen Deutsch und Englisch speichert diese Website den Eintrag "
                                   r"<em>mjoar_lang</em>.*?</p>", re.S)

# Nur Gestaltung der Textspalte; Farben, Schriften und Abstände aus der Startseite.
RECHT_CSS = """/* Rechtsseiten: Kopf im Fluss statt über dem Startbild, ruhige Textspalte (max. 68 Zeichen) */
body.recht header{position:relative}
.recht-haupt{padding-block:24px 96px}
.recht-spalte{max-width:68ch}
.recht-hinweis{margin:16px 0 0}
.legal-card h1{font-family:var(--display);font-weight:300;font-size:clamp(34px,4.2vw,54px);line-height:1.06;letter-spacing:-.01em;margin:28px 0 36px}
.legal-block{border-top:1px solid var(--linie);padding-block:26px 12px}
.legal-block:last-child{border-bottom:1px solid var(--linie)}
.legal-block h2{font-family:var(--display);font-weight:400;font-size:20px;line-height:1.3;letter-spacing:.01em;margin:0 0 12px;color:var(--text)}
.legal-block p{margin:0 0 14px;color:#4A423B;line-height:1.7;overflow-wrap:break-word}
.legal-card a{color:var(--text);text-decoration-color:var(--taupe);text-underline-offset:3px}
.legal-note p{font-size:14px;color:var(--taupe)}
@media (max-width:760px){.recht-haupt{padding-block:8px 72px}.legal-block{padding-block:22px 8px}}"""


def _teil(seite_html, start, ende):
    a = seite_html.index(start)
    b = seite_html.index(ende, a) + len(ende)
    return seite_html[a:b]


def rechtsseite(lang, key, datei):
    inhalt = recht_aus_altdatei(datei)
    if datei == "datenschutz.html":
        inhalt, n = DATENSCHUTZ_ENTFAELLT.subn("", inhalt)
        if n != 1:
            raise SystemExit("Datenschutz: Absatz mjoar_lang nicht genau einmal gefunden")
    hinweis = ""
    if lang == "en":
        # Rechtstext gibt es nur auf Deutsch; unverändert, als deutscher Abschnitt ausgezeichnet, mit Hinweis oben.
        inhalt = inhalt.replace('<article class="legal-card">', '<article class="legal-card" lang="de">', 1)
        hinweis = f'<p class="eyebrow recht-hinweis">{e(EN_HINWEIS)}</p>\n'
    start = vorlage_fuellen(lang, "")
    stil = _teil(start, "<style>", "</style>").replace("</style>", RECHT_CSS + "\n</style>")
    kopf = _teil(start, '<header class="gut">', "</header>")
    fuss = _teil(start, '<footer class="fuss gut"', "</footer>")
    # Ankerlinks des Kopfs zeigen auf die Startseite der Sprache, der Sprachumschalter auf die Rechtsseite der anderen.
    kopf = kopf.replace('href="#', f'href="{PFADE["start"][lang]}#')
    for l in ["de", "en"]:
        alt = f'href="{PFADE["start"][l]}" lang="{l}"'
        if kopf.count(alt) != 1:
            raise SystemExit(f"Rechtsseite: Sprachlink {l} nicht genau einmal im Kopf")
        kopf = kopf.replace(alt, f'href="{PFADE[key][l]}" lang="{l}"')
    if 'href="#' in fuss:
        raise SystemExit("Rechtsseite: Ankerlink im Fuß")
    titel = RECHT_TITEL[lang][key]
    seite_html = f"""<!doctype html>
<html lang="{lang}">
<head>
{kopf_meta(lang, key, titel, None, PFADE[key][lang])}
{stil}
{ZAEHLER}
</head>
<body id="top" class="recht">

{kopf}

<main class="recht-haupt gut" id="inhalt">
  <div class="wrap recht-spalte">
{hinweis}{inhalt}
  </div>
</main>

{fuss}
</body>
</html>
"""
    return logos_einbetten(seite_html)


# ---------------------------------------------------------------------------------------------------------------
# Weiterleitungen

def weiterleitung(ziel, titel, lang="de", anker=None):
    """Alte Adresse → neues Ziel: Meta-Refresh, kanonisch auf die Zielseite, Link für alle ohne Weiterleitung.
    ziel kann einen Anker tragen (/de/#lun). anker ordnet alte Anker der Seite neuen zu (sonst gilt der Zielanker)."""
    basis, _, ziel_anker = ziel.partition("#")
    if anker:
        skript = (f"<script>(function(){{var m={json.dumps(anker)},h=location.hash;"
                  f"location.replace({json.dumps(basis)}+(m[h]||{json.dumps('#' + ziel_anker if ziel_anker else '')}));}})();</script>")
    elif ziel_anker:
        skript = f"<script>location.replace({json.dumps(ziel)});</script>"
    else:
        skript = f"<script>location.replace({json.dumps(ziel)} + location.hash);</script>"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(titel)}</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{SITE}{basis}">
  <meta http-equiv="refresh" content="0; url={ziel}">
  {skript}
</head>
<body>
  <p><a href="{ziel}">{e(titel)}</a></p>
</body>
</html>
"""


def schreiben(pfad, inhalt):
    ziel = os.path.join(ROOT, pfad.strip("/").replace("/", os.sep), "index.html") if pfad.endswith("/") else os.path.join(ROOT, pfad.strip("/"))
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    with open(ziel, "w", encoding="utf-8", newline="\n") as datei:
        datei.write(inhalt)
    return ziel


def main():
    geschrieben = []
    for lang in ["de", "en"]:
        geschrieben.append(schreiben(PFADE["start"][lang], startseite(lang, PFADE["start"][lang])))
        for key, datei in [("impressum", "impressum.html"), ("datenschutz", "datenschutz.html")]:
            geschrieben.append(schreiben(PFADE[key][lang], rechtsseite(lang, key, datei)))
    # "/" = deutsche Startseite ohne Weiterleitung (wie bisher), kanonisch auf "/".
    geschrieben.append(schreiben("/index.html", startseite("de", "/")))
    for alt, lang, ziel, titel_, zuordnung in WEITERLEITUNGEN:
        geschrieben.append(schreiben(alt, weiterleitung(ziel, titel_, lang, zuordnung)))
    geschrieben.append(schreiben("/impressum.html", weiterleitung("/de/impressum/", T["de"]["fuss"]["unten"][0])))
    geschrieben.append(schreiben("/datenschutz.html", weiterleitung("/de/datenschutz/", T["de"]["fuss"]["unten"][1])))
    # Sitemap: nur die Startseiten (Rechtsseiten noindex, Weiterleitungen nicht), je mit hreflang de/en/x-default wie im Seitenkopf.
    urls = "".join(
        f"  <url><loc>{SITE}{PFADE['start'][l]}</loc>"
        + "".join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{SITE}{PFADE["start"][x]}"/>' for x in ["de", "en"])
        + f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>'
        + "</url>\n"
        for l in ["de", "en"])
    schreiben("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n  <url><loc>{SITE}/</loc></url>\n{urls}</urlset>\n')
    for g in geschrieben:
        print(os.path.relpath(g, ROOT))


if __name__ == "__main__":
    main()
