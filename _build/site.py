# mjoar.com v2: statischer Seitenbau DE/EN (Auftrag Website, Fable 07.10.2026, Go Thorsten 07.10.).
# Texte wortgleich aus MJOAR_WEB_COPY_v3.md (_build/texte_v3.py); Impressum und Datenschutz inhaltlich unverändert aus den
# bisherigen Dateien (_build/alt/). Aufbau nach MJOAR_WEB_GUIDANCE.md (2.1, 3, 4, 7), editorial (Fable 07.10.).
# Bilder aus _build/bilder.py (assets/web/), Maße aus _build/bilder.json.
#   python _build/site.py        (aus dem Worktree)
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texte_v3 import ALT, T  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BILDER = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bilder.json"), encoding="utf-8"))
SITE = "https://mjoar.com"
VERSION = "3"

# ---------------------------------------------------------------------------------------------------------------
# Kaufen: die eine zentrale Konstante. EN zeigt vorerst ebenfalls auf amazon.de (UK noch nicht kaufbar).
# Umstellen auf amazon.co.uk: die Zeile KAUFEN["en"] = … durch die UK-Links ersetzen.
KAUFEN = {
    "de": {
        "juniper": "https://www.amazon.de/dp/B0HB116F83",
        "linen": "https://www.amazon.de/dp/B0HB16137F",
        "onyx": "https://www.amazon.de/dp/B0H9ZWMGWR",
        "steel": "https://www.amazon.de/dp/B0HB15MCKJ",
        "ohne": "https://www.amazon.de/dp/B0H9ZS73SW",
    },
}
KAUFEN["en"] = KAUFEN["de"]
FARBEN = ["juniper", "linen", "onyx", "steel"]

# Hero-Bild der Startseite (Thorsten wählt nach Screenshot): "0420" an der Maschine (Standard) oder "0284" Familie.
# Zum Vergleich ohne Codeänderung: Umgebungsvariable MJOAR_HERO=0284 beim Bauen.
HERO_BILD = os.environ.get("MJOAR_HERO", "0420")
HERO_VARIANTEN = {"0420": ("hero-d", "hero-m", "hero"), "0284": ("familie-d", "familie-m", "hero_0284")}
PDF = "/assets/docs/MJOAR_LUN350_Sicherheitshinweise_GPSR.pdf"

# Brevo-Formular unverändert (Double-Opt-in, Datenschutz Abschnitt 3)
BREVO = ("https://d3c20ae3.sibforms.com/serve/MUIFAJzjIZxfPKrfySr11g9GS6FoIFy8Hf1FJUUtNteGWoC1pQTypKM_fGkiPmSmH3fNQt-"
         "S0QhFMnKht-sU9mNEjMYv96tRuEYFTdQdqRRnmTJgS5l1kR402BulG2FacudUzQDDTpNfegGB-z88HKXQK3AENdrkUadGALIvMKzcjBBD_Yo"
         "oeWVD9a7Mem3rWsTYv6KGRAxlMiuvXA==")

PFADE = {
    "start": {"de": "/de/", "en": "/en/"},
    "lun": {"de": "/de/lun-350/", "en": "/en/lun-350/"},
    "latte": {"de": "/de/milch-und-latte-art/", "en": "/en/milk-and-latte-art/"},
    "ueber": {"de": "/de/ueber-uns/", "en": "/en/about/"},
    "impressum": {"de": "/de/impressum/", "en": "/en/imprint/"},
    "datenschutz": {"de": "/de/datenschutz/", "en": "/en/privacy/"},
}
VERPACKUNG = [("0307", "Juniper"), ("0310", "Onyx"), ("0321", "Steel"), ("0332", "Linen")]

e = html.escape


def fett(text):
    """**…** aus der Copy als <strong>; info@mjoar.com als Link."""
    teile = text.split("**")
    out = "".join(f"<strong>{e(t)}</strong>" if i % 2 else e(t) for i, t in enumerate(teile))
    return out.replace("info@mjoar.com", '<a href="mailto:info@mjoar.com">info@mjoar.com</a>')


def srcset(name):
    b = BILDER[name]
    return ", ".join(f"/assets/web/{name}-{w}.webp {w}w" for w in b["breiten"])


def bild(name, alt, sizes, klasse="", lazy=True, attr=""):
    b = BILDER[name]
    mitte = min(b["breiten"], key=lambda w: abs(w - 960))
    h = round(b["h"] * 960 / b["w"])
    laden = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    k = f' class="{klasse}"' if klasse else ""
    return (f'<img{k} src="/assets/web/{name}-{mitte}.webp" srcset="{srcset(name)}" sizes="{sizes}" '
            f'width="960" height="{h}" alt="{e(alt)}" {laden}{attr}>')


def bild_mobil(name_d, name_m, alt, sizes, lazy=True, klasse=""):
    """Eigener 4:5-Ausschnitt für schmale Bildschirme (Guidance 3)."""
    hm = round(BILDER[name_m]["h"] * 960 / BILDER[name_m]["w"])
    return (f'<picture><source media="(max-width: 720px)" srcset="{srcset(name_m)}" sizes="100vw" width="960" height="{hm}">'
            f'{bild(name_d, alt, sizes, klasse=klasse, lazy=lazy)}</picture>')


LOGO = open(os.path.join(ROOT, "assets", "web", "logo.svg"), encoding="utf-8").read().strip()


def aktuell(bedingung, wert="page"):
    return f' aria-current="{wert}"' if bedingung else ""


def kopf(lang, seite):
    t, a = T[lang], ALT[lang]
    menu = "".join(f'<a href="{PFADE[k][lang]}"{aktuell(k == seite)}>{e(n)}</a>' for k, n in zip(["lun", "latte", "ueber"], t["menu"]))
    sprachen = (f'<nav class="sprachen" aria-label="{e(a["sprache"])}">'
                f'<a href="{PFADE[seite]["de"]}" lang="de" hreflang="de"{aktuell(lang == "de", "true")}>{t["sprachen"][0]}</a>'
                f'<span aria-hidden="true">|</span>'
                f'<a href="{PFADE[seite]["en"]}" lang="en" hreflang="en"{aktuell(lang == "en", "true")}>{t["sprachen"][1]}</a></nav>')
    return f"""<header class="kopf">
  <div class="kopf-innen">
    <a class="logo" href="{PFADE['start'][lang]}" aria-label="{e(a['start'])}">{LOGO}</a>
    <nav class="menu-desktop" aria-label="{e(a['menu'])}">{menu}</nav>
    <div class="kopf-rechts">
      {sprachen}
      <a class="knopf knopf-klein" href="{KAUFEN[lang]['ohne']}" rel="noopener">{e(t['kaufen'])}</a>
      <details class="menu-mobil"><summary aria-label="{e(a['menu'])}"><span></span><span></span><span></span></summary><nav aria-label="{e(a['menu'])}">{menu}</nav></details>
    </div>
  </div>
</header>"""


def newsletter(lang, nr):
    t = T[lang]
    vor, link, nach = t["nl_klein"]
    return f"""<div class="newsletter">
  <p>{fett(t['nl'])}</p>
  <form method="POST" action="{BREVO}">
    <label class="unsichtbar" for="nl-{nr}">{e(t['nl_feld'])}</label>
    <input id="nl-{nr}" type="email" name="EMAIL" required placeholder="{e(t['nl_feld'])}" autocomplete="email">
    <input type="text" name="email_address_check" value="" style="position:absolute;left:-9999px;height:0;width:0;border:0;padding:0" tabindex="-1" aria-hidden="true" autocomplete="off">
    <input type="hidden" name="locale" value="de">
    <button class="knopf" type="submit">{e(t['nl_knopf'])}</button>
  </form>
  <p class="klein">{e(vor)}<a href="{PFADE['datenschutz'][lang]}">{e(link)}</a>{e(nach)}</p>
</div>"""


def fuss(lang):
    t = T[lang]
    u = t["unten"]
    return f"""<footer class="fuss">
  <div class="fuss-innen">
    <div class="fuss-spalte fuss-marke"><p>{fett(t['fuss_links'])}</p></div>
    <div class="fuss-spalte"><p>{fett(t['fuss_mitte'])}</p></div>
    <div class="fuss-spalte">{newsletter(lang, 'fuss')}</div>
    <p class="recht"><a href="{PFADE['impressum'][lang]}">{e(u[0])}</a> · <a href="{PFADE['datenschutz'][lang]}">{e(u[1])}</a> · <a href="{PDF}">{e(u[2])}</a></p>
  </div>
</footer>"""


def kaufen(lang, farbe="ohne", lang_zeile=False, id_=""):
    t = T[lang]
    i = f' id="{id_}"' if id_ else ""
    zeile = t["kaufzeile_lang"] if lang_zeile else t["kaufzeile"]
    return (f'<div class="kaufen"><a class="knopf"{i} href="{KAUFEN[lang][farbe]}" rel="noopener">{e(t["kaufen"])}</a>'
            f'<p class="klein">{e(zeile)}</p></div>')


def seite(lang, key, inhalt, extra_head=""):
    t = T[lang]
    titel, beschreibung = t["meta"][key]
    pfad = PFADE[key][lang]
    alternates = "".join(f'\n  <link rel="alternate" hreflang="{l}" href="{SITE}{PFADE[key][l]}">' for l in ["de", "en"])
    x_default = f"{SITE}/" if key == "start" else f"{SITE}{PFADE[key]['de']}"
    meta = f'\n  <meta name="description" content="{e(beschreibung)}">' if beschreibung else '\n  <meta name="robots" content="noindex">'
    og = (f'\n  <meta property="og:title" content="{e(titel)}">\n  <meta property="og:description" content="{e(beschreibung)}">'
          f'\n  <meta property="og:type" content="website">\n  <meta property="og:url" content="{SITE}{pfad}">'
          f'\n  <meta property="og:image" content="{SITE}/assets/web/og-familie.jpg">\n  <meta property="og:locale" content="{"de_DE" if lang == "de" else "en_GB"}">') if beschreibung else ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(titel)}</title>{meta}
  <link rel="canonical" href="{SITE}{pfad}">{alternates}
  <link rel="alternate" hreflang="x-default" href="{x_default}">{og}
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/cormorant-garamond-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/web/site.css?v={VERSION}">
  <script>document.documentElement.classList.add('js');</script>{extra_head}
</head>
<body>
{kopf(lang, key)}
<main id="inhalt">
{inhalt}
</main>
{fuss(lang)}
<script src="/assets/web/site.js?v={VERSION}" defer></script>
</body>
</html>
"""


def farb_kacheln(lang, link=True):
    """Große Freisteller auf Creme, Name und Art darunter, je Farbe ein Link (Copy v3 B2)."""
    t, a = T[lang], ALT[lang]
    out = []
    for i, f in enumerate(FARBEN):
        name, art = t["farben"][f]
        kopf_ = (f'{bild("farbe-" + f, a["farbe"].format(name), "(max-width: 720px) 72vw, 25vw")}'
                 f'<p class="farbname"><strong>{e(name)}</strong>: {e(art)}</p>')
        weiter = f'<a class="weiter" href="{PFADE["lun"][lang]}#{f}">{e(t["farbe_link"].format(name))}</a>' if link else ""
        out.append(f'<div class="farbe" data-reveal style="--i:{i}">{kopf_}{weiter}</div>')
    return f'<div class="farben">{"".join(out)}</div>'


def vier_dinge(lang):
    """Detail-Close-ups 4:5 als eigene Bildstrecke, versetzt."""
    a = ALT[lang]
    return '<div class="nahstrecke">' + "".join(
        f'<figure class="nah nah-{i + 1}" data-reveal>{bild(name, a[name], "(max-width: 720px) 100vw, 40vw")}'
        f'<figcaption><h3>{e(titel)}</h3><p>{e(text)}</p></figcaption></figure>'
        for i, (titel, text, name) in enumerate(T[lang]["vier"])) + "</div>"


def start(lang):
    t, a = T[lang], ALT[lang]
    v = [bild(f"verpackung-{nr}", a["verpackung"].format(farbe), "(max-width: 720px) 100vw, 58vw" if i == 0 else "(max-width: 720px) 33vw, 12vw")
         for i, (nr, farbe) in enumerate(VERPACKUNG)]
    hd, hm, halt = HERO_VARIANTEN[HERO_BILD]
    return f"""<section class="hero">
  <div class="hero-bild">{bild_mobil(hd, hm, a[halt], '100vw', lazy=False)}</div>
  <div class="hero-text raster">
    <div class="hero-zeile">
      <p class="dach">{e(t['hero_dach'])}</p>
      <h1>{e(t['hero_h'])}</h1>
    </div>
    <div class="hero-neben">
      <p class="gross">{e(t['hero_p'])}</p>
      {kaufen(lang)}
      <p><a class="weiter" href="{PFADE['lun'][lang]}">{e(t['hero_link'])}</a></p>
    </div>
  </div>
</section>

<section class="block" id="farben">
  <div class="raster kopfzeile">
    <div class="weit" data-reveal>
      <h2>{e(t['farben_h'])}</h2>
      <p class="unterzeile">{e(t['farben_unter'])}</p>
    </div>
    <p class="neben" data-reveal>{e(t['farben_p'])}</p>
  </div>
  {farb_kacheln(lang)}
</section>

<section class="block" id="details">
  <h2 class="kopf-schmal" data-reveal>{e(t['vier_h'])}</h2>
  {vier_dinge(lang)}
</section>

<section class="vollbreit geteilt" id="groesse">
  <div class="geteilt-bild" data-reveal>{bild('groesse', a['groesse'], '(max-width: 720px) 100vw, 50vw')}</div>
  <div class="geteilt-text" data-reveal>
    <h2>{e(t['groesse_h'])}</h2>
    <p>{e(t['groesse_p'])}</p>
  </div>
</section>

<section class="block" id="gebrauch">
  <div class="raster kopfzeile">
    <h2 class="weit" data-reveal>{e(t['gebrauch_h'])}</h2>
    <div class="neben" data-reveal>
      <p>{e(t['gebrauch_p'])}</p>
      <p><a class="weiter" href="{PFADE['latte'][lang]}">{e(t['gebrauch_link'])}</a></p>
    </div>
  </div>
  <div class="strecke">{''.join(f'<div data-reveal style="--i:{i}">{bild(n, a[n], "(max-width: 720px) 80vw, 33vw")}</div>' for i, n in enumerate(['gebrauch-aufschaeumen', 'gebrauch-giessen', 'gebrauch-tasse']))}</div>
</section>

<section class="block ruhezeile" id="pflege">
  <h2 data-reveal>{e(t['pflege_h'])}</h2>
  <p data-reveal>{e(t['pflege_p'])}</p>
</section>

<section class="vollbreit" id="wer">
  <div class="vollbild" data-reveal>{bild_mobil('familie-d', 'familie-m', a['familie'], '100vw')}</div>
  <div class="block raster kopfzeile wer-text">
    <div class="weit" data-reveal>
      <p class="dach">{e(t['wer_dach'])}</p>
      <h2>{e(t['wer_h'])}</h2>
    </div>
    <div class="neben" data-reveal>
      <p>{e(t['wer_p'])}</p>
      <p><a class="weiter" href="{PFADE['ueber'][lang]}">{e(t['wer_link'])}</a></p>
    </div>
  </div>
</section>

<section class="block" id="ausgepackt">
  <div class="verpackung-raster">
    <div class="v-gross" data-reveal>{v[0]}</div>
    <div class="v-text" data-reveal>
      <h2>{e(t['aus_h'])}</h2>
      <p>{e(t['aus_p'])}</p>
      {kaufen(lang)}
      <div class="v-reihe">{''.join(v[1:])}</div>
    </div>
  </div>
  <p class="ausblick klein" data-reveal>{e(t['ausblick'])}</p>
</section>"""


def produkt(lang):
    t, a = T[lang], ALT[lang]
    k = KAUFEN[lang]
    haupt = "".join(
        bild(f"farbe-{f}", a["farbe"].format(t["farben"][f][0]), "(max-width: 720px) 100vw, 55vw",
             klasse="farbbild" + (" aktiv" if f == "juniper" else ""), lazy=f != "juniper", attr=f' data-farbe="{f}"')
        for f in FARBEN)
    galerie = "".join(f'<div data-reveal>{bild(n, a[n] if n in a else a["verpackung"].format("Juniper"), "(max-width: 720px) 50vw, 25vw")}</div>'
                      for n in ["groesse", "gebrauch-tasse", "gebrauch-giessen", "detail-ausguss", "detail-skala", "detail-griff", "detail-wand", "verpackung-0307"])
    wahl = "".join(
        f'<label class="wahl"><input type="radio" name="farbe" value="{f}" data-kaufen="{k[f]}">'
        f'<span>{bild("farbe-" + f, "", "88px", klasse="wahl-bild")}<span class="wahl-name">{e(t["farben"][f][0])}</span>'
        f'<span class="wahl-art">{e(t["farben"][f][1])}</span></span></label>'
        for f in FARBEN)
    detail = "".join(
        f'<article class="im-detail{" links" if i % 2 else ""}" data-reveal>'
        f'<div class="im-bild">{bild(name, a[name], "(max-width: 720px) 100vw, 45vw")}</div>'
        f'<div class="im-text"><h2>{e(titel)}</h2><p>{e(text)}</p></div></article>'
        for i, (titel, text, name) in enumerate(t["detail"]))
    zeilen = "".join(
        f'<tr><th scope="row">{e(n)}</th><td>{e(v) if v is not None else "<!-- [LFGB] Platzhalter: erst nach bestandenem Eurofins-Bericht freischalten -->" + e(t["lfgb_platzhalter"])}</td></tr>'
        for n, v in t["daten"])
    box = "".join(f"<p><strong>{e(n)}</strong> {e(x)}</p>" for n, x in t["box"])
    fragen = "".join(f"<dt>{e(f)}</dt><dd>{e(x)}</dd>" for f, x in t["fragen"])
    punkte = "".join(f"<li>{e(p)}</li>" for p in t["punkte"])
    s1, s2 = t["schluss"]
    return f"""<section class="produkt">
  <div class="galerie-haupt">{haupt}</div>
  <div class="kaufbox">
    <p class="dach">{e(t['dach'])}</p>
    <h1>{e(t['titel'])}</h1>
    <p>{e(t['absatz'])}</p>
    <ul class="punkte">{punkte}</ul>
    <fieldset class="farbwahl"><legend>{e(t['farbwahl'])}</legend>{wahl}</fieldset>
    {kaufen(lang, 'ohne', lang_zeile=True, id_='kaufen')}
  </div>
</section>

<section class="block galerie">{galerie}</section>

<section class="block" id="im-detail">{detail}</section>

<section class="vollbreit geteilt" id="entstehung">
  <div class="geteilt-bild" data-reveal>{bild_mobil('familie-d', 'familie-m', a['familie'], '(max-width: 720px) 100vw, 50vw')}</div>
  <div class="geteilt-text" data-reveal>
    <h2>{e(t['entstehung_h'])}</h2>
    <p>{e(t['entstehung_p'])}</p>
  </div>
</section>

<section class="block raster zweispaltig">
  <div id="daten" data-reveal>
    <h2>{e(t['daten_h'])}</h2>
    <table class="daten"><tbody>{zeilen}</tbody></table>
    <p class="klein">{e(t['daten_klein'])}</p>
  </div>
  <div id="box" data-reveal>
    <h2>{e(t['box_h'])}</h2>
    {box}
    <p><strong>{e(t['pdf_zeile'])}</strong> <a href="{PDF}">{e(t['pdf_link'])}</a></p>
  </div>
</section>

<section class="block spalte" id="fragen">
  <h2 data-reveal>{e(t['fragen_h'])}</h2>
  <dl class="fragen" data-reveal>{fragen}</dl>
</section>

<section class="block schluss" data-reveal>
  <p class="schluss-zeile">{e(s1)}</p>
  <p class="schluss-name">{e(s2)}</p>
  {kaufen(lang)}
</section>"""


def latte(lang):
    t, a = T[lang], ALT[lang]
    schritte = "".join(f"<li><strong>{e(s)}</strong> {e(x)}</li>" for s, x in t["la_schritte"])
    fehler = "".join(f"<li><strong>{e(s)}</strong> {e(x)}</li>" for s, x in t["la_fehler"])
    drei = "".join(f"<li><strong>{e(s)}</strong> {e(x)}</li>" for s, x in t["la_drei"])
    bilder = "".join(f'<div data-reveal style="--i:{i}">{bild(f"latte-{m}", a["latte"][m], "(max-width: 720px) 50vw, 25vw")}</div>'
                     for i, m in enumerate(["heart", "rosetta", "tulip", "swan"]))
    return f"""<section class="block erste raster kopfzeile">
  <div class="weit">
    <p class="dach">{e(t['la_dach'])}</p>
    <h1>{e(t['la_h'])}</h1>
  </div>
  <p class="neben gross">{e(t['la_intro'])}</p>
</section>
<section class="block reihe vier">{bilder}</section>
<section class="block spalte">
  <ol class="schritte">{schritte}</ol>
  <h2 class="klein-h">{e(t['la_fehler_h'])}</h2>
  <ul class="fehler">{fehler}</ul>
  <p class="la-schluss">{e(t['la_schluss'])}</p>
</section>
<section class="block spalte" data-reveal>
  <h2>{e(t['la_drei_h'])}</h2>
  <ul class="drei">{drei}</ul>
</section>"""


def ueber(lang):
    t, a = T[lang], ALT[lang]
    absaetze = "".join(f"<p>{fett(p)}</p>" for p in t["ueber_p"])
    return f"""<section class="vollbreit erste">
  <div class="vollbild">{bild_mobil('familie-d', 'familie-m', a['familie'], '100vw', lazy=False)}</div>
</section>
<section class="block raster kopfzeile">
  <div class="weit">
    <p class="dach">{e(t['ueber_dach'])}</p>
    <h1>{e(t['ueber_h'])}</h1>
  </div>
  <div class="neben">{absaetze}</div>
</section>
<section class="block spalte">
  {newsletter(lang, 'ueber')}
</section>"""


def recht_aus_altdatei(datei):
    """Inhalt der bisherigen Rechtsseite (article.legal-card) unverändert übernehmen."""
    roh = open(os.path.join(ROOT, "_build", "alt", datei), encoding="utf-8").read()
    a = roh.index('<article class="legal-card">')
    b = roh.index("</article>", a) + len("</article>")
    return roh[a:b]


def rechtsseite(lang, datei):
    inhalt = recht_aus_altdatei(datei)
    if lang == "en":
        # Rechtstext gibt es nur auf Deutsch; unverändert, als deutscher Abschnitt ausgezeichnet.
        inhalt = inhalt.replace('<article class="legal-card">', '<article class="legal-card" lang="de">', 1)
    return f'<section class="block spalte erste recht-text">\n{inhalt}\n</section>'


# Alte Anker der One-Page-Seite. #farben gibt es auf der neuen Startseite wieder, dort genügt der Anker selbst.
ALTE_ANKER = {
    "#colour": "/de/lun-350/", "#colours": "/de/lun-350/", "#latte-art": "/de/milch-und-latte-art/",
    "#story": "/de/ueber-uns/", "#founders": "/de/ueber-uns/", "#name": "/de/ueber-uns/", "#craft": "/de/lun-350/#im-detail",
    "#object": "/de/lun-350/", "#honest": "/de/lun-350/#daten", "#early": "/de/ueber-uns/", "#partners": "/de/ueber-uns/",
    "#hero": "/de/", "#top": "/de/",
}


def weiterleitung(ziel, titel, lang="de"):
    """Für alte Adressen (impressum.html, datenschutz.html, /latte-art/): Meta-Refresh, JS mit Anker und Link."""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(titel)}</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{SITE}{ziel}">
  <meta http-equiv="refresh" content="0; url={ziel}">
  <script>location.replace({json.dumps(ziel)} + location.hash);</script>
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
        geschrieben.append(schreiben(PFADE["start"][lang], seite(lang, "start", start(lang))))
        geschrieben.append(schreiben(PFADE["lun"][lang], seite(lang, "lun", produkt(lang))))
        geschrieben.append(schreiben(PFADE["latte"][lang], seite(lang, "latte", latte(lang))))
        geschrieben.append(schreiben(PFADE["ueber"][lang], seite(lang, "ueber", ueber(lang))))
        geschrieben.append(schreiben(PFADE["impressum"][lang], seite(lang, "impressum", rechtsseite(lang, "impressum.html"))))
        geschrieben.append(schreiben(PFADE["datenschutz"][lang], seite(lang, "datenschutz", rechtsseite(lang, "datenschutz.html"))))
    # "/" = deutsche Startseite ohne Weiterleitung; alte Anker der One-Page führen auf die neuen Seiten.
    anker = f"\n  <script>(function(){{var z={json.dumps(ALTE_ANKER)}[location.hash];if(z)location.replace(z);}})();</script>"
    wurzel = seite("de", "start", start("de"), extra_head=anker)
    wurzel = wurzel.replace(f'<link rel="canonical" href="{SITE}/de/">', f'<link rel="canonical" href="{SITE}/">')
    geschrieben.append(schreiben("/index.html", wurzel))
    geschrieben.append(schreiben("/impressum.html", weiterleitung("/de/impressum/", "Impressum")))
    geschrieben.append(schreiben("/datenschutz.html", weiterleitung("/de/datenschutz/", "Datenschutz")))
    geschrieben.append(schreiben("/latte-art/", weiterleitung("/de/milch-und-latte-art/", "Milch und Latte Art")))
    urls = "".join(
        f"  <url><loc>{SITE}{PFADE[k][l]}</loc>"
        + "".join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{SITE}{PFADE[k][x]}"/>' for x in ["de", "en"])
        + "</url>\n"
        for k in ["start", "lun", "latte", "ueber"] for l in ["de", "en"])
    schreiben("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n  <url><loc>{SITE}/</loc></url>\n{urls}</urlset>\n')
    for g in geschrieben:
        print(os.path.relpath(g, ROOT))


if __name__ == "__main__":
    main()
