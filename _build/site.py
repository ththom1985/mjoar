# mjoar.com: DE-Startseite (/ und /de/) aus der Vorlage _build/vorlagen/startseite-de.html (Entwurf v70, von Thorsten
# abgenommen 13.11.2026, Referenz _build/entwurf/startseite-v70.html). EN-One-Pager (/en/) und die Rechtsseiten weiter v4:
# Texte wortgleich aus MJOAR_WEB_COPY_v4.md (_build/texte_v4.py).
# Aufbau nach Jonahs Feedback vom 08.10.2026 (One-Pager, Ankernavigation, Design-Feinschliff), Auftrag Fable 08.10.
# Impressum und Datenschutz inhaltlich unverändert aus den bisherigen Dateien (_build/alt/). Die alten Unterseiten
# bleiben als schlanke Weiterleitungen auf den passenden Anker. Bilder aus _build/bilder.py (assets/web/).
#   python _build/site.py        (aus dem Worktree)
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texte_v4 import ALT, EN_HINWEIS, NAV_RECHT_DE, RECHT_TITEL, T  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BILDER = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bilder.json"), encoding="utf-8"))
SITE = "https://mjoar.com"
VERSION = "12"  # site.css (PR #23 hat nur das CSS hochgezählt)
VERSION_JS = "11"

# ---------------------------------------------------------------------------------------------------------------
# Kaufen: die eine zentrale Konstante. DE auf amazon.de, EN auf amazon.co.uk (UK kaufbar seit 08.10.2026),
# gleiche ASIN je Farbe; DE-Links mit Amazon-Attribution-Tag (Kampagne Website mjoar.com DE, 22.10.2026). "ohne" = Kanne ohne Farbwahl (Knopf, solange keine Farbe gewählt ist).
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
        "ohne": "https://www.amazon.co.uk/dp/B0H9ZS73SW",
    },
}
FARBEN = ["juniper", "linen", "onyx", "steel"]

# Hero-Bild: "0284" Familie (Thorsten 07.10.), Alternative "0420" an der Maschine (MJOAR_HERO=0420 beim Bauen).
HERO_BILD = os.environ.get("MJOAR_HERO", "0284")
HERO_VARIANTEN = {"0420": ("hero-d", "hero-m", "hero"), "0284": ("familie-d", "familie-m", "hero_0284")}
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
# Anker der Abschnitte je Sprache (Copy v4)
ANKER = {
    "de": {"einstieg": "einstieg", "lun": "lun", "details": "details", "gut": "gut-zu-wissen", "latte": "latte-art", "ueber": "ueber-uns"},
    "en": {"einstieg": "intro", "lun": "lun", "details": "details", "gut": "good-to-know", "latte": "latte-art", "ueber": "about"},
}

# Alte Unterseiten → Anker auf dem One-Pager. Alte Anker der Produktseite werden mitgenommen (EN: Farbe wählt vor).
# DE zeigt seit der neuen Startseite (Entwurf v70) auf deren Anker: #produkte, #lun, #details, #uns. Milch und Latte Art
# gibt es dort nicht mehr; die alten Latte-Art-Adressen leiten auf die Startseite.
_LUN_ALT = {"de": {"#im-detail": "#details", "#daten": "#lun", "#box": "#details", "#fragen": "#lun",
                   "#entstehung": "#uns", "#kaufen": "#lun"},
            "en": {"#im-detail": "#details", "#daten": "#good-to-know", "#box": "#good-to-know", "#fragen": "#good-to-know",
                   "#entstehung": "#about", "#kaufen": "#lun"}}
_LUN_ALT["de"].update({f"#{f}": "#lun" for f in FARBEN})
_LUN_ALT["en"].update({f"#{f}": f"#{f}" for f in FARBEN})
WEITERLEITUNGEN = [
    # (alter Pfad, Sprache, Ziel (Pfad + Anker), Titel aus der Navigation der Copy, Ankerzuordnung)
    ("/de/lun-350/", "de", "/de/#lun", T["de"]["nav"][0][1], _LUN_ALT["de"]),
    ("/de/milch-und-latte-art/", "de", "/de/", T["de"]["nav"][2][1], {}),
    ("/de/ueber-uns/", "de", "/de/#uns", T["de"]["nav"][3][1], {}),
    ("/en/lun-350/", "en", "/en/#lun", T["en"]["nav"][0][1], _LUN_ALT["en"]),
    ("/en/milk-and-latte-art/", "en", "/en/#latte-art", T["en"]["nav"][2][1], {}),
    ("/en/about/", "en", "/en/#about", T["en"]["nav"][3][1], {}),
    # Latte-Art-Unterseite entfernt (Auftrag 13.11.): statische Weiterleitung auf die Startseite, kanonisch auf /
    ("/latte-art/", "de", "/", T["de"]["nav"][2][1], {}),
]

e = html.escape


def fett(text):
    """**…** als <strong>; info@mjoar.com als Link."""
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
    """Eigener 4:5-Ausschnitt für schmale Bildschirme."""
    hm = round(BILDER[name_m]["h"] * 960 / BILDER[name_m]["w"])
    return (f'<picture><source media="(max-width: 720px)" srcset="{srcset(name_m)}" sizes="100vw" width="960" height="{hm}">'
            f'{bild(name_d, alt, sizes, klasse=klasse, lazy=lazy)}</picture>')


LOGO = open(os.path.join(ROOT, "assets", "web", "logo.svg"), encoding="utf-8").read().strip()


def kopf(lang, seite):
    """Sticky-Leiste: Ankerlinks laut Copy, Sprachumschalter, Kaufen (springt zu #lun). Auf den Rechtsseiten zeigen die
    Anker auf den One-Pager der Sprache."""
    t, a = T[lang], ALT[lang]
    basis = "" if seite == "start" else PFADE["start"][lang]
    # DE: Rechtsseiten zeigen auf die Anker der neuen Startseite (NAV_RECHT_DE), EN unverändert (Copy v4)
    nav = NAV_RECHT_DE if lang == "de" else t["nav"]
    menu = "".join(f'<a href="{basis}#{k}">{e(n)}</a>' for k, n in nav)
    sprachen = (f'<nav class="sprachen" aria-label="{e(a["sprache"])}">'
                f'<a href="{PFADE[seite]["de"]}" lang="de" hreflang="de"{" aria-current=\"true\"" if lang == "de" else ""}>{t["sprachen"][0]}</a>'
                f'<span aria-hidden="true">|</span>'
                f'<a href="{PFADE[seite]["en"]}" lang="en" hreflang="en"{" aria-current=\"true\"" if lang == "en" else ""}>{t["sprachen"][1]}</a></nav>')
    logo_ziel = "#top" if seite == "start" else PFADE["start"][lang]
    return f"""<header class="kopf">
  <div class="kopf-innen">
    <a class="logo" href="{logo_ziel}" aria-label="{e(a['start'])}">{LOGO}</a>
    <nav class="menu-desktop" aria-label="{e(a['menu'])}">{menu}</nav>
    <div class="kopf-rechts">
      {sprachen}
      <a class="knopf knopf-klein" href="{basis}#lun">{e(t['kaufen'])}</a>
      <details class="menu-mobil"><summary aria-label="{e(a['menu'])}"><span></span><span></span><span></span></summary><nav aria-label="{e(a['menu'])}">{menu}</nav></details>
    </div>
  </div>
</header>"""


def newsletter(lang):
    f = T[lang]["fuss"]
    vor, link, nach = f["nl_klein"]
    return f"""<div class="newsletter">
      <p>{e(f['nl'])}</p>
      <form method="POST" action="{BREVO}">
        <label class="unsichtbar" for="nl-fuss">{e(f['nl_feld'])}</label>
        <input id="nl-fuss" type="email" name="EMAIL" required placeholder="{e(f['nl_feld'])}" autocomplete="email">
        <input type="text" name="email_address_check" value="" style="position:absolute;left:-9999px;height:0;width:0;border:0;padding:0" tabindex="-1" aria-hidden="true" autocomplete="off">
        <input type="hidden" name="locale" value="de">
        <button class="knopf" type="submit">{e(f['nl_knopf'])}</button>
      </form>
      <p class="klein">{e(vor)}<a href="{PFADE['datenschutz'][lang]}">{e(link)}</a>{e(nach)}</p>
    </div>"""


def fuss(lang):
    f = T[lang]["fuss"]
    u = f["unten"]
    _, satz = f["links"]
    return f"""<footer class="fuss">
  <div class="innen raster fuss-innen">
    <div class="fuss-links">
      <div class="fuss-logo" role="img" aria-label="{e(ALT[lang]['marke'])}">{LOGO}</div>
      <p class="fuss-marke">{e(satz)}</p>
      <p class="fuss-kontakt">{e(f['kontakt'])} <a href="mailto:info@mjoar.com">info@mjoar.com</a></p>
      <p class="fuss-b2b">{e(f['b2b'][0])}<a href="mailto:info@mjoar.com?subject={f['b2b'][1]}">info@mjoar.com</a></p>
    </div>
    {newsletter(lang)}
    <p class="recht"><a href="{PFADE['impressum'][lang]}">{e(u[0])}</a> · <a href="{PFADE['datenschutz'][lang]}">{e(u[1])}</a> · <a href="{PDF}">{e(u[2])}</a></p>
  </div>
</footer>"""


def seite(lang, key, titel, beschreibung, inhalt, kanonisch=None):
    pfad = PFADE[key][lang]
    alternates = "".join(f'\n  <link rel="alternate" hreflang="{l}" href="{SITE}{PFADE[key][l]}">' for l in ["de", "en"])
    x_default = f"{SITE}/" if key == "start" else f"{SITE}{PFADE[key]['de']}"
    meta = f'\n  <meta name="description" content="{e(beschreibung)}">' if beschreibung else '\n  <meta name="robots" content="noindex">'
    og = (f'\n  <meta property="og:title" content="{e(titel)}">\n  <meta property="og:description" content="{e(beschreibung)}">'
          f'\n  <meta property="og:type" content="website">\n  <meta property="og:url" content="{SITE}{kanonisch or pfad}">'
          f'\n  <meta property="og:image" content="{SITE}/assets/web/og-familie.jpg">\n  <meta property="og:locale" content="{"de_DE" if lang == "de" else "en_GB"}">') if beschreibung else ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(titel)}</title>{meta}
  <link rel="canonical" href="{SITE}{kanonisch or pfad}">{alternates}
  <link rel="alternate" hreflang="x-default" href="{x_default}">{og}
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/cormorant-garamond-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/web/site.css?v={VERSION}">
  <script>document.documentElement.classList.add('js');</script>
  <script data-goatcounter="https://mjoar.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</head>
<body id="top">
{kopf(lang, key)}
<main id="inhalt">
{inhalt}
</main>
{fuss(lang)}
<script src="/assets/web/site.js?v={VERSION_JS}" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------------------------------------------------------
# Abschnitte des One-Pagers

def kopfzeile(dach, h, intro):
    """Abschnittskopf: Dach und Überschrift links (Spalten 1–6), Einleitung rechts (7–12)."""
    d = f'<p class="dach">{e(dach)}</p>' if dach else ""
    i = f'<p class="k-text">{e(intro)}</p>' if intro else ""
    return f'<div class="raster kopfzeile" data-reveal><div class="k-titel">{d}<h2>{e(h)}</h2></div>{i}</div>'


def paar(i, bild_html, text_html, klasse=""):
    """Bild/Text-Paar 4:5. Muster je Abschnitt: erstes Paar Bild rechts, dann abwechselnd."""
    seite_ = "bild-links" if i % 2 else "bild-rechts"
    k = f" {klasse}" if klasse else ""
    return (f'<div class="raster paar {seite_}{k}" data-reveal>'
            f'<div class="paar-bild">{bild_html}</div><div class="paar-text">{text_html}</div></div>')


def hero_bild(name_d, name_m, alt):
    """Hero: bis 720 px eigener 4:5-Ausschnitt, bis 860 px 3:2 (beides wie bisher), darüber das ganze Original 1:1."""
    if HERO_BILD != "0284":
        return bild_mobil(name_d, name_m, alt, "100vw", lazy=False)
    hm = round(BILDER[name_m]["h"] * 960 / BILDER[name_m]["w"])
    hd = round(BILDER[name_d]["h"] * 960 / BILDER[name_d]["w"])
    return (f'<picture><source media="(max-width: 720px)" srcset="{srcset(name_m)}" sizes="100vw" width="960" height="{hm}">'
            f'<source media="(max-width: 860px)" srcset="{srcset(name_d)}" sizes="100vw" width="960" height="{hd}">'
            f'{bild("familie-q", alt, "640px", lazy=False)}</picture>')


def hero(lang):
    t, a = T[lang]["hero"], ALT[lang]
    hd, hm, halt = HERO_VARIANTEN[HERO_BILD]
    # Desktop: Text links (Spalten 1–5), Familienbild rechts (7–12, ganzes Original 1:1), beides im ersten Schirm.
    # Mobil wie bisher: Bild randlos (4:5) über dem Text.
    return f"""<section class="hero innen raster">
  <div class="hero-bild">{hero_bild(hd, hm, a[halt])}</div>
  <div class="hero-text">
    <div class="hero-zeile">
      <p class="dach">{e(t['dach'])}</p>
      <h1>{e(t['h'])}</h1>
    </div>
    <div class="hero-neben">
      <p class="gross">{e(t['satz'])}</p>
      <p><a class="weiter" href="#lun">{e(t['link'])}</a></p>
    </div>
  </div>
</section>"""


def einstieg(lang):
    t = T[lang]["einstieg"]
    erst, *rest = t["text"]
    return f"""<section class="abschnitt innen raster einstieg" id="{t['id']}">
  <p class="e-lead" data-reveal>{e(erst)}</p>
  <div class="e-text" data-reveal>{''.join(f'<p>{e(p)}</p>' for p in rest)}{f'<p class="abgesetzt">{e(t["abgesetzt"])}</p>' if t['abgesetzt'] else ''}</div>
</section>"""


def produkt(lang):
    """Produktansicht wie im Live-Stand: großes Produktbild links, Infos, Farbwahl und Kaufen rechts."""
    t, a = T[lang]["produkt"], ALT[lang]
    k = KAUFEN[lang]
    haupt = "".join(
        bild(f"farbe-{f}", a["farbe"].format(t["farben"][f]), "(max-width: 860px) 100vw, 740px",
             klasse="farbbild" + (" aktiv" if f == "juniper" else ""), attr=f' data-farbe="{f}"')
        for f in FARBEN)
    wahl = "".join(
        f'<label class="wahl"><input type="radio" name="farbe" value="{f}" data-kaufen="{k[f]}">'
        f'<span>{bild("farbe-" + f, "", "88px", klasse="wahl-bild")}<span class="wahl-name">{e(t["farben"][f])}</span></span></label>'
        for f in FARBEN)
    punkte = "".join(f"<li>{e(p)}</li>" for p in t["punkte"])
    return f"""<section class="abschnitt innen raster produkt" id="lun">
  <div class="galerie-haupt">{haupt}</div>
  <div class="kaufbox">
    <p class="dach">{e(t['dach'])}</p>
    <h2 class="titel">{e(t['titel'])}</h2>
    <p>{e(t['absatz'])}</p>
    <ul class="punkte">{punkte}</ul>
    <fieldset class="farbwahl"><legend>{e(t['farbe'])}</legend>{wahl}</fieldset>
    <div class="kaufen"><a class="knopf" id="kaufen" href="{k['ohne']}" rel="noopener">{e(t['knopf'])}</a><p class="klein">{e(t['klein'])}</p></div>
  </div>
</section>"""


def details(lang):
    t, a = T[lang]["details"], ALT[lang]
    zeilen = "".join(
        paar(i, bild(name, a[name], "(max-width: 860px) 100vw, 520px", klasse="b45"), f"<h3>{e(titel)}</h3><p>{e(text)}</p>")
        for i, (titel, text, name) in enumerate(t["punkte"]))
    return f"""<section class="abschnitt innen" id="details">
  {kopfzeile(t['dach'], t['h'], t['intro'])}
  {zeilen}
</section>"""


def gut(lang):
    t = T[lang]["gut"]
    punkte = "".join(f"<p><strong>{e(n)}</strong> {e(x)}</p>" for n, x in t["punkte"])
    zeilen = "".join(
        f'<tr><th scope="row">{e(n)}</th><td>{e(v) if v is not None else "<!-- [LFGB] Platzhalter: erst nach bestandenem Eurofins-Bericht freischalten -->" + e(t["lfgb_platzhalter"])}</td></tr>'
        for n, v in t["daten"])
    fragen = "".join(f'<div class="frage"><dt>{e(f)}</dt><dd>{e(x)}</dd></div>' for f, x in t["fragen"])
    fragen = f'\n  <dl class="fragen" data-reveal>{fragen}</dl>' if fragen else ""
    return f"""<section class="abschnitt innen" id="{t['id']}">
  {kopfzeile(None, t['h'], None)}
  <div class="raster gzw">
    <div class="gzw-text" data-reveal>{punkte}</div>
    <div class="gzw-daten" data-reveal>
      <table class="daten"><tbody>{zeilen}</tbody></table>
      <p class="klein">{e(t['klein'])}</p>
      <p><a class="weiter" href="{PDF}">{e(t['pdf'])}</a></p>
    </div>
  </div>{fragen}
</section>"""


def latte(lang):
    t, a = T[lang]["latte"], ALT[lang]

    def liste(eintraege):
        return "".join(f"<li><strong>{e(s)}</strong> {e(x)}</li>" for s, x in eintraege)

    s = t["schritte"]
    erste = paar(0, bild("gebrauch-aufschaeumen", a["gebrauch-aufschaeumen"], "(max-width: 860px) 100vw, 520px", klasse="b45"),
                 f'<ol class="schritte">{liste(s[:3])}</ol>', klasse="la-paar")
    zweite = paar(1, bild("gebrauch-giessen", a["gebrauch-giessen"], "(max-width: 860px) 100vw, 520px", klasse="b45"),
                  f'<ol class="schritte" start="4">{liste(s[3:])}</ol>', klasse="la-paar")
    # Latte-Art-Motive vorerst ausgeblendet, bis eigene Fotos da sind (Thorsten 08.10.).
    return f"""<section class="abschnitt innen" id="latte-art">
  {kopfzeile(t['dach'], t['h'], t['intro'])}
  {erste}
  {zweite}
  <div class="raster la-unten">
    <div class="la-fehler" data-reveal>
      <h3>{e(t['fehler_h'])}</h3>
      <ul class="liste">{liste(t['fehler'])}</ul>
    </div>
    <div class="la-passt" data-reveal>
      <h3>{e(t['passt_h'])}</h3>
      <p>{e(t['passt_p'])}</p>
    </div>
  </div>
</section>"""


def ueber(lang):
    t, a = T[lang]["ueber"], ALT[lang]
    absaetze = "".join(f"<p>{e(p)}</p>" for p in t["text"])
    # Marke in prominenter Stellung als Logo statt Schriftzug (Thorsten 11.10.), im Fließtext bleibt MJØÅR als Text.
    vor = t["unterschrift"].removesuffix("MJØÅR")
    unterschrift = (f'{e(vor)}<span class="logo-inline" role="img" aria-label="{e(a["marke"])}">{LOGO}</span>'
                    if vor != t["unterschrift"] else e(t["unterschrift"]))
    text = (f"<h2>{e(t['h'])}</h2>{absaetze}<p class=\"unterschrift\">{unterschrift}</p>"
            f"<p>{fett(t['kontakt'])}</p>" + (f"<p class=\"ausblick\">{e(t['ausblick'])}</p>" if t.get("ausblick") else ""))
    return f"""<section class="abschnitt innen" id="{t['id']}">
  {paar(0, bild('wer-m', a['wer'], '(max-width: 860px) 100vw, 520px', klasse='b45'), text, klasse='ueber')}
</section>"""


def onepager(lang):
    return "\n\n".join([hero(lang), einstieg(lang), produkt(lang), details(lang), gut(lang), latte(lang), ueber(lang)])


# ---------------------------------------------------------------------------------------------------------------
# Neue DE-Startseite (Entwurf v70). Die Vorlage ist der abgenommene Entwurf mit Technik-Anpassungen (Asset-Pfade,
# Attribution-Links, Brevo, Videos mobil/ruhig, eigene Schriften); Texte und Gestaltung stehen dort unverändert.
# Begründung eigene Vorlage statt texte_v4/Abschnittsfunktionen: Aufbau, Stil und Texte sind komplett neu und stammen
# nicht aus Copy v4; ein Port in die v4-Funktionen hätte jeden Abschnitt neu geschrieben, ohne Gewinn für EN.

VORLAGE_START_DE = os.path.join(ROOT, "_build", "vorlagen", "startseite-de.html")
# Titel und Beschreibung: nur Sätze aus dem Hero des Entwurfs (Thorsten 14.11.: LUN-Satz raus).
START_DE_META = ("MJØÅR · Schöne Dinge für deine Kaffee-Ecke",
                 "Schöne Dinge für deine Kaffee-Ecke. Klares Design, ruhige Farben, kunststofffrei verpackt.")
# Teilen-Bild: vorhandenes Produktbild (Familie 0284, alle vier Farben), 1200 × 630
OG_BILD = ("/assets/web/og-familie.jpg", 1200, 630, ALT["de"]["hero_0284"])
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


def startseite_de(kanonisch):
    titel, beschreibung = START_DE_META
    url = SITE + kanonisch
    og_pfad, og_b, og_h, og_alt = OG_BILD
    alternates = "".join(f'\n  <link rel="alternate" hreflang="{l}" href="{SITE}{PFADE["start"][l]}">' for l in ["de", "en"])
    kopf_html = f"""  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(titel)}</title>
  <meta name="description" content="{e(beschreibung)}">
  <link rel="canonical" href="{url}">{alternates}
  <link rel="alternate" hreflang="x-default" href="{SITE}/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="MJØÅR">
  <meta property="og:title" content="{e(titel)}">
  <meta property="og:description" content="{e(beschreibung)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}{og_pfad}">
  <meta property="og:image:width" content="{og_b}">
  <meta property="og:image:height" content="{og_h}">
  <meta property="og:image:alt" content="{e(og_alt)}">
  <meta property="og:locale" content="de_DE">
  <meta property="og:locale:alternate" content="en_GB">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(titel)}">
  <meta name="twitter:description" content="{e(beschreibung)}">
  <meta name="twitter:image" content="{SITE}{og_pfad}">
  <meta name="twitter:image:alt" content="{e(og_alt)}">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/jost-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>"""
    werte = {"KOPF": kopf_html, "ZAEHLER": ZAEHLER, "BREVO": e(BREVO), "PDF": PDF,
             "IMPRESSUM": PFADE["impressum"]["de"], "DATENSCHUTZ": PFADE["datenschutz"]["de"]}
    werte.update({f"KAUFEN_{f}": e(KAUFEN["de"][f]) for f in FARBEN})
    seite_html = open(VORLAGE_START_DE, encoding="utf-8").read()
    for k, v in werte.items():
        if "{{" + k + "}}" not in seite_html:
            raise SystemExit(f"Startseite: Platzhalter {{{{{k}}}}} fehlt in der Vorlage")
        seite_html = seite_html.replace("{{" + k + "}}", v)
    if "{{" in seite_html:
        raise SystemExit("Startseite: offener Platzhalter " + re.search(r"\{\{[^}]*\}\}", seite_html).group(0))
    return logos_einbetten(seite_html)


# ---------------------------------------------------------------------------------------------------------------
# Rechtsseiten (Inhalt unverändert)

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


def rechtsseite(lang, datei):
    inhalt = recht_aus_altdatei(datei)
    if datei == "datenschutz.html":
        inhalt, n = DATENSCHUTZ_ENTFAELLT.subn("", inhalt)
        if n != 1:
            raise SystemExit("Datenschutz: Absatz mjoar_lang nicht genau einmal gefunden")
    hinweis = ""
    if lang == "en":
        # Rechtstext gibt es nur auf Deutsch; unverändert, als deutscher Abschnitt ausgezeichnet, mit Hinweis oben.
        inhalt = inhalt.replace('<article class="legal-card">', '<article class="legal-card" lang="de">', 1)
        hinweis = f'<p class="klein recht-hinweis">{e(EN_HINWEIS)}</p>\n'
    return f'<section class="innen recht-text">\n{hinweis}{inhalt}\n</section>'


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
        if lang == "en":
            titel, beschreibung = T[lang]["meta"]
            geschrieben.append(schreiben(PFADE["start"][lang], seite(lang, "start", titel, beschreibung, onepager(lang))))
        else:
            geschrieben.append(schreiben(PFADE["start"][lang], startseite_de(PFADE["start"][lang])))
        for key, datei in [("impressum", "impressum.html"), ("datenschutz", "datenschutz.html")]:
            geschrieben.append(schreiben(PFADE[key][lang], seite(lang, key, RECHT_TITEL[lang][key], None, rechtsseite(lang, datei))))
    # "/" = deutsche Startseite ohne Weiterleitung (wie bisher), kanonisch auf "/".
    geschrieben.append(schreiben("/index.html", startseite_de("/")))
    for alt, lang, ziel, titel_, zuordnung in WEITERLEITUNGEN:
        geschrieben.append(schreiben(alt, weiterleitung(ziel, titel_, lang, zuordnung)))
    geschrieben.append(schreiben("/impressum.html", weiterleitung("/de/impressum/", T["de"]["fuss"]["unten"][0])))
    geschrieben.append(schreiben("/datenschutz.html", weiterleitung("/de/datenschutz/", T["de"]["fuss"]["unten"][1])))
    urls = "".join(
        f"  <url><loc>{SITE}{PFADE['start'][l]}</loc>"
        + "".join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{SITE}{PFADE["start"][x]}"/>' for x in ["de", "en"])
        + "</url>\n"
        for l in ["de", "en"])
    schreiben("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n  <url><loc>{SITE}/</loc></url>\n{urls}</urlset>\n')
    for g in geschrieben:
        print(os.path.relpath(g, ROOT))


if __name__ == "__main__":
    main()
