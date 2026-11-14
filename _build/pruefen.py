# Prüfungen für den PR (mjoar.com v4, One-Pager, Auftrag Fable 08.10.2026):
#  1. Wortgleichheit Seite → Copy: jeder sichtbare Textblock aller erzeugten Seiten (One-Pager, Kopf und Fuß der
#     Rechtsseiten, Weiterleitungen) steht wortgleich in MJOAR_WEB_COPY_v4.md. Ausnahmen werden einzeln gelistet:
#     Alt-Texte und Bedienetiketten (texte_v4.ALT), NICHT_IN_COPY, Titel der Rechtsseiten.
#  2. Wortgleichheit Copy → Seite: jede Inhaltsstelle der Copy (DE und EN) steht auf dem One-Pager der Sprache.
#     Regie bleibt draußen: [J], [J*], Klammerhinweise nach [J*]-Zeilen, [BILD …], Bildschlüssel, Feldbezeichnungen.
#  3. Rechtstexte: Artikel von Impressum/Datenschutz byte-gleich mit den bisherigen Dateien.
#  4. Keine Überschrift (h1–h4) endet mit „.“.
#  5. Verbotsliste: Gedankenstriche, „Entworfen in“, Preis, Farb-Unterzeilen, satin, Tülle.
#  6. Links: interne Ziele existieren (Dateien und Anker), Kaufen DE → amazon.de, EN → amazon.co.uk; externe Ziele gelistet.
# Seit der neuen DE-Startseite (Entwurf v70, Thorsten 13.11.2026) gelten 1, 2, 4 und 5 für EN, die Rechtsseiten und die
# Weiterleitungen. Die DE-Startseite (/ und /de/) prüft Abschnitt 7 gegen den abgenommenen Entwurf:
#  7. Wortgleichheit Startseite ↔ Entwurf (_build/entwurf/startseite-v70.html): sichtbarer Text in derselben Reihenfolge,
#     Alt-Texte, aria-label und Platzhalter gleich (Abweichungen nur laut ENTWURF_ATTR_ERLAUBT); Titel und Beschreibung
#     nur aus Sätzen des Entwurfs. Marke nie als geschriebenes Wort im sichtbaren Text (immer Logo), kein „Barista“.
#  8. Technik: kein Google-Fonts-Abruf, Schriften lokal vorhanden, jedes svg[data-logo] mit eingebettetem Logo (kein fetch),
#     DE-Kauflinks mit Amazon-Attribution, echtes Brevo-Formular, GoatCounter, Videos nur ohne reduzierte Bewegung und
#     mobil < 1,5 MB, Weiterleitung /latte-art/ → / und nicht in der Sitemap.
# Seit der EN-Startseite und den Rechtsseiten im neuen Design (14.11.2026) gelten 1, 2, 4 und 5 nur noch für die
# Weiterleitungen (Titel aus Copy v4). Neu:
#  9. EN-Startseite (/en/): gleicher Aufbau wie DE (Tags, Klassen, Bilder, Stil- und Skriptblock gleich, gleiche Zahl an
#     Textblöcken), Marke nur als Logo (Über uns höchstens dreimal), keine deutschen Reste, Negativliste Brand Voice (EN),
#     Kauflinks nur amazon.co.uk ohne DE-Attribution, canonical/hreflang/og:locale, „DE · EN“ auf beiden Seiten richtig,
#     Datenschutz-Link am Newsletter auf /en/privacy/, Titel und Beschreibung nur aus Sätzen der Seite.
# 10. Rechtsseiten: Kopf, Fuß und Stil wie die Startseite derselben Sprache (Ankerlinks auf die Startseite, Sprachumschalter
#     auf die Rechtsseite der anderen Sprache), noindex, hreflang; Rechtstext byte-gleich mit _build/alt/ (3.) und mit dem
#     bisherigen Stand auf origin/main.
#   python _build/pruefen.py        (aus dem Worktree, nach site.py)
import html
import importlib.util
import os
import re
import subprocess
import sys
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texte_v4 import ALT, EN_HINWEIS, NICHT_IN_COPY, RECHT_TITEL  # noqa: E402

# _build/site.py heißt wie das Standardmodul „site“: über den Dateipfad laden.
_spec = importlib.util.spec_from_file_location("mjoar_site", os.path.join(os.path.dirname(os.path.abspath(__file__)), "site.py"))
_mjoar_site = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mjoar_site)
DATENSCHUTZ_ENTFAELLT = _mjoar_site.DATENSCHUTZ_ENTFAELLT
KAUFEN = _mjoar_site.KAUFEN
WEITERLEITUNGEN = _mjoar_site.WEITERLEITUNGEN
BREVO = _mjoar_site.BREVO
PFADE = _mjoar_site.PFADE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPY = r"C:/Users/ththomas/OneDrive/01_THOMAS_MERCANTILE_BUSINESS/01_Marke_MJOAR/03_Website_Landingpage/MJOAR_WEB_COPY_v4.md"
ONEPAGER = {}  # EN-One-Pager v4 ersetzt durch die EN-Startseite (Abschnitt 9)
START_DE = ["index.html", "de/index.html"]
START_EN = "en/index.html"
START = START_DE + [START_EN]
UK_ASINS = {u.rsplit("/", 1)[1] for u in KAUFEN["en"].values()}
ENTWURF = os.path.join(ROOT, "_build", "entwurf", "startseite-v70.html")
# Bewusste Abweichungen der Attribute vom Entwurf (Zahl = Mehr (+) oder Weniger (−) auf der gebauten Seite):
# Kopf-Logo ist jetzt ein Link zur Startseite (aria-label am Link statt am Logo), das Menü hat eine Beschriftung.
ENTWURF_ATTR_ERLAUBT = {("aria-label", "MJØÅR"): -1, ("aria-label", "MJØÅR Startseite"): 1, ("aria-label", "Menü"): 1}
MOBIL_VIDEO_MAX = 1_500_000
RECHT = {"de/impressum/index.html": "impressum.html", "de/datenschutz/index.html": "datenschutz.html",
         "en/imprint/index.html": "impressum.html", "en/privacy/index.html": "datenschutz.html"}
UMLEITUNG = [w[0].strip("/") + "/index.html" for w in WEITERLEITUNGEN] + ["impressum.html", "datenschutz.html"]
BLOCK = {"p", "h1", "h2", "h3", "h4", "li", "dt", "dd", "th", "td", "legend", "figcaption", "button", "label", "title", "summary",
         "div", "section", "nav", "span", "table", "tr", "ol", "ul", "dl", "header", "footer", "main", "form"}


def norm(text):
    text = html.unescape(text).replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text).strip()


def lesen(rel):
    return open(os.path.join(ROOT, rel.replace("/", os.sep)), encoding="utf-8").read()


class Text(HTMLParser):
    """Sichtbare Textblöcke, Attribute (alt, placeholder, aria-label, description), Überschriften, ids.
    Der Rechtstext (article.legal-card) wird übersprungen, er wird byte-genau gesondert geprüft."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.bloecke, self.puffer, self.attrs, self.ueberschriften, self.ids = [], [], [], [], set()
        self.ignorieren, self.nav, self.artikel, self.h = 0, 0, 0, None

    def flush(self):
        t = norm("".join(self.puffer))
        if t:
            self.bloecke.append(t)
        self.puffer = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if self.artikel:
            if tag == "article":
                self.artikel += 1
            return
        if tag == "article" and "legal-card" in (a.get("class") or ""):
            self.flush()
            self.artikel = 1
            return
        if tag in ("script", "style", "head"):
            self.ignorieren += 1
        if tag == "nav":
            self.nav += 1
        if tag in BLOCK or (tag == "a" and self.nav):
            self.flush()
        if tag in ("h1", "h2", "h3", "h4"):
            self.h = []
        for k in ("alt", "placeholder", "aria-label"):
            if a.get(k):
                self.attrs.append((k, norm(a[k])))
        if tag == "meta" and a.get("name") == "description":
            self.attrs.append(("description", norm(a.get("content", ""))))
        if tag == "title":
            self.ignorieren -= 1  # Titel zählt als Text, obwohl er im Kopf steht

    def handle_endtag(self, tag):
        if self.artikel:
            if tag == "article":
                self.artikel -= 1
            return
        if tag == "title":
            self.ignorieren += 1
        if tag in ("script", "style", "head"):
            self.ignorieren -= 1
        if tag == "nav":
            self.nav -= 1
        if tag in ("h1", "h2", "h3", "h4") and self.h is not None:
            self.ueberschriften.append((tag, norm("".join(self.h))))
            self.h = None
        if tag in BLOCK or (tag == "a" and self.nav):
            self.flush()

    def handle_data(self, data):
        if self.artikel or self.ignorieren:
            return
        self.puffer.append(data)
        if self.h is not None:
            self.h.append(data)


def parse(rel):
    p = Text()
    p.feed(lesen(rel))
    p.flush()
    return p


def parse_body(roh):
    """Nur der sichtbare Teil ab <body> (der Entwurf hat keinen <head>)."""
    i = roh.find("<body")
    if i < 0:
        i = roh.index("</style>") + len("</style>")
    p = Text()
    p.feed(roh[i:])
    p.flush()
    return p


def entwurf_parse():
    return parse_body(open(ENTWURF, encoding="utf-8").read())


def korpus():
    roh = open(COPY, encoding="utf-8").read().replace("**", "")
    teile = [re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", z) for z in roh.splitlines()]
    return norm(" \n ".join(teile))


# Feldbezeichnungen der Copy vor dem Inhalt (längere zuerst)
LABEL = re.compile(
    r"^(?:Überschrift klein|Zeile \(groß\)|Daten \(Tabelle\)|Dach|Satz|Links|Link|Text|Abgesetzt|Titel|Absatz|Punkte|Farbe|Knopf|Klein|"
    r"Überschrift|Einleitung|Fragen|Schluss|Unterschrift|Kontakt|Ausblick|Newsletter|Feld|Unten|Beschreibung|"
    r"Small heading|Kicker|Line|Sentence|Set apart|Title|Paragraph|Points|Colour|Button|Small|Heading|Intro|Specifications|"
    r"Questions|Closing|Signature|Contact|Coming next|Left|Field|Bottom|Description):\s*")
MARKE = re.compile(r"\s*\[(?:J\*?|BILD[^\]]*|IMAGE[^\]]*|detail-[a-z]+|gebrauch-[a-z]+)\]")
REGIE_KLAMMER = re.compile(r"\s*\((?:Jonah|Jonahs|nur die Namen)[^)]*\)\s*$")


def copy_stellen():
    """Inhaltsstellen der Copy je Sprache, ohne Regie."""
    stellen, sprache = [], None
    for zeile in open(COPY, encoding="utf-8").read().splitlines():
        if zeile.startswith("## "):
            sprache = {"## DE": "de", "## EN": "en"}.get(zeile.strip())
            continue
        z = zeile.strip()
        if not sprache or not z or z.startswith("#") or z == "---":
            continue
        z = re.sub(r"^(?:[-*]|\d+\.)\s+", "", z)
        if z.startswith("("):
            continue  # Regiehinweis als eigene Zeile
        kopf_rest = re.match(r"^\*\*(.+?)\*\*(.*)$", z)
        stuecke = [kopf_rest.group(1), kopf_rest.group(2)] if kopf_rest else [z]
        for s in stuecke:
            s = MARKE.sub("", s.replace("**", ""))
            s = re.sub(r"\[LFGB: ([^\]]+)\]", r"\1", s)
            s = REGIE_KLAMMER.sub("", s)
            s = re.sub(r"\s*\(#[a-z-]+\)", "", s)
            s = LABEL.sub("", s.strip())
            for teil in re.split(r"\s·\s", s):
                teil = LABEL.sub("", teil.strip()).strip()
                teil = re.sub(r"^:\s*", "", teil)
                if kopf_rest and teil.endswith(":") and s == MARKE.sub("", kopf_rest.group(1)):
                    teil = teil[:-1]
                if not teil or teil.endswith(":"):
                    continue
                if teil == "Deutsch/English":
                    stellen += [(sprache, "Deutsch"), (sprache, "English")]
                    continue
                stellen.append((sprache, teil))
    return stellen


class Gerippe(HTMLParser):
    """Aufbau einer Seite ab <body>: Tags mit Klassen, Bildquellen, Rollen usw., ohne Sprache (Text, Alt, Labels, Links, ids)."""
    OHNE = {"href", "id", "alt", "aria-label", "data-n", "data-kaufen", "placeholder", "aria-current", "lang", "hreflang"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, tuple(sorted((k, v) for k, v in attrs if k not in self.OHNE))))

    def handle_endtag(self, tag):
        self.tags.append(("/" + tag, ()))


def gerippe(roh):
    g = Gerippe()
    g.feed(roh[roh.index("<body"):])
    return g.tags


def block(roh, muster):
    m = re.search(muster, roh, re.S)
    return m.group(0) if m else ""


# Negativliste Brand Voice §4 und §9 (englisch), dazu Floskeln, die auf EN typisch wären
EN_NEGATIV = (r"(?i)\b(elevat\w*|redefin\w*|crafted|more than just|not just a|designed to inspire|designed for|made to\b|"
              r"must-have|game.changer|statement|perfected|revolutionary|unique|unparalleled|premium quality|attention to detail|"
              r"indulge|pamper|magic\w*|clean and|and precision|and functional|a single)\b")
DEUTSCH_RESTE = r"\b(und|der|die|das|mit|für|bei|nicht|ist|wir|deine?|Kanne|Milch|Tülle|Kaufen|Datenschutz|Impressum|Kaffee|Farben?|Gründer)\b"


def en_startseite(entwurf):
    """Abschnitt 9: EN-Startseite gegen den Aufbau der DE-Seite und die Regeln für EN."""
    f = []
    s, roh, de = START_EN, lesen(START_EN), lesen("de/index.html")
    p, p_de = parse_body(roh), parse_body(de)
    # Aufbau gleich (Tags, Klassen, Bildquellen, Stil, Skript)
    a, b = gerippe(de), gerippe(roh)
    if a != b:
        i = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
        f.append((s, "Aufbau weicht von DE ab", f"DE {a[i] if i < len(a) else '-'} / EN {b[i] if i < len(b) else '-'}"))
    if block(de, r"<style>.*?</style>") != block(roh, r"<style>.*?</style>"):
        f.append((s, "Stilblock weicht von DE ab", ""))
    if block(de, r"<script>\s*//.*?</script>") != block(roh, r"<script>\s*//.*?</script>"):
        f.append((s, "Seitenskript weicht von DE ab", ""))
    if len(p.bloecke) != len(p_de.bloecke):
        f.append((s, "Zahl der Textblöcke weicht von DE ab", f"DE {len(p_de.bloecke)} / EN {len(p.bloecke)}"))
    # Text: Marke nur als Logo, Verbote, keine deutschen Reste
    sichtbar = " ".join(p.bloecke)
    attrs = " ".join(v for _, v in p.attrs)
    for muster, grund in [(r"[–—]|\s-\s", "Gedankenstrich"), (r"€|EUR\b|£", "Preis"), (r"(?i)la marzocco", "Maschinen-Schriftzug genannt"),
                          (r"(?i)(?<![@\w.])MJ[ØO][ÅA]R(?![\w]|\.[a-z])", "Marke als Wort statt Logo"), (r"(?i)barista", "„barista“"),
                          (r"(?i)designed in|made in germany|entworfen in", "„Designed in“"), (EN_NEGATIV, "Negativliste Brand Voice")]:
        for t in sorted(set(m.group(0) for m in re.finditer(muster, sichtbar))):
            f.append((s, grund, t))
    for t in sorted(set(re.findall(r"\w*[äöüßÄÖÜ]\w*", sichtbar + " " + attrs)) - {"mjölk"}):
        f.append((s, "deutsches Wort/Umlaut", t))
    for t in sorted(set(re.findall(DEUTSCH_RESTE, sichtbar + " " + attrs))):
        f.append((s, "deutsches Wort", t))
    uns = block(roh, r'<section class="uns[^"]*" id="about".*?</section>')
    n_logo, n_logo_de = uns.count('class="logo-text"'), block(de, r'<section class="uns[^"]*" id="uns".*?</section>').count('class="logo-text"')
    if not uns or n_logo > 3 or n_logo != n_logo_de:
        f.append((s, "Über uns: Logo im Text nicht wie DE (höchstens dreimal)", f"EN {n_logo} / DE {n_logo_de}"))
    for pflicht in ["At home in Munich & Vienna", "350 ml · 12 oz"]:
        if pflicht not in p.bloecke:
            f.append((s, "Pflichtzeile fehlt", pflicht))
    # Titel und Beschreibung nur aus Sätzen der Seite
    seite_text = norm(" \n ".join(p.bloecke))
    titel = re.search(r"<title>(.*?)</title>", roh).group(1)
    beschreibung = re.search(r'<meta name="description" content="([^"]+)"', roh).group(1)
    for teil in norm(titel).split(" · "):
        if teil != "MJØÅR" and teil not in seite_text:
            f.append((s, "Titel nicht aus dem Seitentext", teil))
    for satz in re.findall(r"[^.]+\.", norm(beschreibung)):
        if satz.strip() not in seite_text:
            f.append((s, "Beschreibung nicht aus dem Seitentext", satz.strip()))
    # Kopf: canonical, hreflang wechselseitig, Sprache
    for k in ('<html lang="en">', '<link rel="canonical" href="https://mjoar.com/en/">',
              '<link rel="alternate" hreflang="de" href="https://mjoar.com/de/">', '<link rel="alternate" hreflang="en" href="https://mjoar.com/en/">',
              '<link rel="alternate" hreflang="x-default" href="https://mjoar.com/">', '<meta property="og:locale" content="en_GB">',
              '<meta property="og:url" content="https://mjoar.com/en/">', 'name="twitter:card"', 'property="og:image"'):
        if k not in roh:
            f.append((s, "Kopf unvollständig", k))
    for d in START_DE:
        if '<link rel="alternate" hreflang="en" href="https://mjoar.com/en/">' not in lesen(d):
            f.append((d, "hreflang en fehlt", ""))
    # „DE · EN“: beide Links richtig, aktuelle Sprache markiert
    for d, lang in [(START_DE[0], "de"), (START_DE[1], "de"), (START_EN, "en")]:
        q = block(lesen(d), r'<span class="sprache">.*?</span>')
        for l, txt in [("de", "DE"), ("en", "EN")]:
            cur = ' aria-current="page"' if l == lang else ""
            if f'<a class="sprache" href="/{l}/" lang="{l}" hreflang="{l}"{cur}>{txt}</a>' not in q:
                f.append((d, "Sprachumschalter DE · EN falsch", txt))
    # Rechtslinks und Newsletter-Hinweis auf die EN-Seiten
    for k in ('More in our <a href="/en/privacy/">privacy policy</a>', '<a href="/en/imprint/">Imprint</a>', '<a href="/en/privacy/">Privacy</a>'):
        if k not in roh:
            f.append((s, "Rechtslink fehlt", k))
    if "/de/datenschutz/" in roh or "/de/impressum/" in roh:
        f.append((s, "Link auf deutsche Rechtsseite", ""))
    return f


def rechtsseiten():
    """Abschnitt 10: Rechtsseiten im Design der Startseite; Rechtstext wie auf origin/main."""
    f = []
    for s, alt in RECHT.items():
        lang = s[:2]
        key = "impressum" if alt == "impressum.html" else "datenschutz"
        roh = lesen(s)
        start = _mjoar_site.vorlage_fuellen(lang, "")
        # Kopf und Fuß wie auf der Startseite (Logos eingebettet, Ankerlinks auf die Startseite, Sprachlinks auf die Rechtsseiten)
        kopf = _mjoar_site.logos_einbetten(block(start, r'<header class="gut">.*?</header>')).replace('href="#', f'href="/{lang}/#')
        for l in ["de", "en"]:
            kopf = kopf.replace(f'href="/{l}/" lang="{l}"', f'href="{PFADE[key][l]}" lang="{l}"')
        fuss = _mjoar_site.logos_einbetten(block(start, r'<footer class="fuss gut".*?</footer>'))
        if block(roh, r'<header class="gut">.*?</header>') != kopf:
            f.append((s, "Kopf weicht von der Startseite ab", ""))
        if block(roh, r'<footer class="fuss gut".*?</footer>') != fuss:
            f.append((s, "Fuß weicht von der Startseite ab", ""))
        if block(roh, r"<style>.*?</style>") != block(start, r"<style>.*?</style>").replace("</style>", _mjoar_site.RECHT_CSS + "\n</style>"):
            f.append((s, "Stil weicht von der Startseite ab", ""))
        for k in (f'<html lang="{lang}">', '<meta name="robots" content="noindex">', f'<link rel="canonical" href="https://mjoar.com{PFADE[key][lang]}">',
                  f'<link rel="alternate" hreflang="de" href="https://mjoar.com{PFADE[key]["de"]}">',
                  f'<link rel="alternate" hreflang="en" href="https://mjoar.com{PFADE[key]["en"]}">', f"<title>{html.escape(RECHT_TITEL[lang][key])}</title>"):
            if k not in roh:
                f.append((s, "Kopf unvollständig", k))
        if lang == "en" and ('<article class="legal-card" lang="de">' not in roh or html.escape(EN_HINWEIS) not in roh):
            f.append((s, "EN: Hinweis oder lang=de am Rechtstext fehlt", ""))
        # Rechtstext gleich dem bisherigen Stand auf origin/main (bis zum Merge: alte Seite im alten Design)
        try:
            vorher = subprocess.run(["git", "-C", ROOT, "show", f"origin/main:{s}"], capture_output=True, check=True).stdout.decode("utf-8")
        except (subprocess.CalledProcessError, FileNotFoundError):
            f.append((s, "origin/main nicht lesbar, Rechtstext nicht gegen den bisherigen Stand geprüft", ""))
            continue
        art = lambda t: block(t.replace("\r\n", "\n"), r'<article class="legal-card"[^>]*>.*?</article>')
        if not art(vorher) or art(vorher) != art(roh):
            f.append((s, "Rechtstext weicht vom Stand origin/main ab", ""))
    return f


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    korp = korpus()
    fehler, ausnahmen = [], []
    erlaubt_alt = set()
    for lang in ALT:
        for k, v in ALT[lang].items():
            erlaubt_alt.update(v.values() if isinstance(v, dict) else [v])
    erlaubt_text = {s for l in NICHT_IN_COPY.values() for s in l}
    recht_titel = {v for l in RECHT_TITEL.values() for v in l.values()}
    alt_formate = [ALT[l]["farbe"] for l in ALT]

    def ist_alt(s):
        return s in erlaubt_alt or any(re.fullmatch(re.escape(f).replace(re.escape("{}"), r"\w+"), s) for f in alt_formate)

    alle = [s for l in ONEPAGER.values() for s in l] + UMLEITUNG
    geparst = {s: parse(s) for s in alle + list(RECHT) + START}
    entwurf = entwurf_parse()
    entwurf_text = norm(" \n ".join(entwurf.bloecke))

    # 1. Seite → Copy
    gepruefte = 0
    for s in alle:
        p = geparst[s]
        for b in p.bloecke:
            gepruefte += 1
            if b in korp or re.fullmatch(r"[·| ]+", b):
                continue
            teile = [x.strip() for x in re.split(r"\s·\s", b) if x.strip()]
            if len(teile) > 1 and all(x in korp for x in teile):
                continue
            if b in erlaubt_text:
                ausnahmen.append((s, "Text", b))
                continue
            if b in recht_titel:
                ausnahmen.append((s, "Titel Rechtsseite", b))
                continue
            if not s.startswith("en/") and b in entwurf.bloecke:
                ausnahmen.append((s, "aus Entwurf v70 (Navigation DE)", b))
                continue
            fehler.append((s, "nicht in Copy v4", b))
        for k, v in p.attrs:
            if k == "description":
                gepruefte += 1
                if v not in korp:
                    fehler.append((s, "Meta-Beschreibung nicht in Copy v4", v))
            elif k == "placeholder":
                if v not in korp:
                    fehler.append((s, k, v))
            elif ist_alt(v):
                ausnahmen.append((s, k, v))
            else:
                fehler.append((s, f"{k} unbekannt", v))
        sichtbar = " ".join(p.bloecke)
        for muster, grund in [(r"[\u2013\u2014]|\s-\s", "Gedankenstrich"), (r"Entworfen in|Designed in", "Entworfen/Designed in"),
                              (r"€|EUR\b|£", "Preis"), (r"(?i)la marzocco", "Maschinen-Schriftzug genannt"),
                              (r"(?i)satin|seidenmatt|soft matt", "satiniert/satin/seidenmatt"), (r"Tülle", "Tülle (überall Ausguss)"),
                              (r"(?i)grün, matt|cremeweiß|schwarz, matt|edelstahl, gebürstet|green, matt|cream, matt|black, matt|brushed stainless steel",
                               "Farb-Unterzeile (Jonah 08.10.: nur Namen)")]:
            if re.search(muster, sichtbar):
                fehler.append((s, grund, re.search(muster, sichtbar).group(0)))
        # 4. Überschriften ohne Schlusspunkt
        for tag, text in p.ueberschriften:
            if text.endswith("."):
                fehler.append((s, f"{tag} endet mit Punkt", text))

    # 2. Copy → Seite
    seitentext = {}
    for lang, seiten in ONEPAGER.items():
        p = geparst[seiten[0]]
        seitentext[lang] = norm(" \n ".join(p.bloecke + [v for _, v in p.attrs]))
    # DE-Stellen der Copy v4 stehen seit der neuen Startseite nicht mehr auf /de/ (Inhalt jetzt Entwurf v70, Abschnitt 7).
    stellen = [(l, x) for l, x in copy_stellen() if l in ONEPAGER]
    fehlt = [(l, x) for l, x in stellen if x not in seitentext[l]]
    # Root "/" ist die deutsche Startseite: gleicher Inhalt wie /de/
    if geparst["index.html"].bloecke != geparst["de/index.html"].bloecke or geparst["index.html"].attrs != geparst["de/index.html"].attrs:
        fehler.append(("index.html", "Startseite / weicht von /de/ ab", ""))

    # 7. Startseite DE ↔ Entwurf v70
    hinweise = []
    for s in START_DE:
        roh = lesen(s)
        p = parse_body(roh)
        if norm(" ".join(p.bloecke)) != norm(" ".join(entwurf.bloecke)):
            a_, b_ = norm(" ".join(entwurf.bloecke)), norm(" ".join(p.bloecke))
            i = next((i for i, (x, y) in enumerate(zip(a_, b_)) if x != y), min(len(a_), len(b_)))
            fehler.append((s, "Text weicht vom Entwurf ab", f"Entwurf …{a_[max(0, i - 40):i + 40]}… / Seite …{b_[max(0, i - 40):i + 40]}…"))
        zaehl = {}
        for k, v in entwurf.attrs:
            zaehl[(k, v)] = zaehl.get((k, v), 0) - 1
        for k, v in p.attrs:
            zaehl[(k, v)] = zaehl.get((k, v), 0) + 1
        for kv, n in zaehl.items():
            if n and ENTWURF_ATTR_ERLAUBT.get(kv) != n:
                fehler.append((s, "Attribut weicht vom Entwurf ab", f"{kv[0]}={kv[1]!r} ({n:+d})"))
        for kv, n in ENTWURF_ATTR_ERLAUBT.items():
            if zaehl.get(kv, 0) == n:
                ausnahmen.append((s, f"{kv[0]} ({n:+d} ggü. Entwurf)", kv[1]))
        titel = re.search(r"<title>(.*?)</title>", roh).group(1)
        beschreibung = re.search(r'<meta name="description" content="([^"]+)"', roh).group(1)
        for teil in norm(titel).split(" · "):
            if teil != "MJØÅR" and teil not in entwurf_text:
                fehler.append((s, "Titel nicht aus dem Entwurf", teil))
        for satz in re.findall(r"[^.]+\.", norm(beschreibung)):
            if satz.strip() not in entwurf_text:
                fehler.append((s, "Beschreibung nicht aus dem Entwurf", satz.strip()))
        for k in ('<link rel="canonical"', 'hreflang="de"', 'hreflang="en"', 'hreflang="x-default"', 'property="og:image"',
                  'name="twitter:card"', '<html lang="de">'):
            if k not in roh:
                fehler.append((s, "Kopf unvollständig", k))
        sichtbar = " ".join(p.bloecke)
        for muster, grund in [(r"[–—]|\s-\s", "Gedankenstrich"), (r"€|EUR\b|£", "Preis"),
                              (r"(?i)la marzocco", "Maschinen-Schriftzug genannt"), (r"(?i)(?<![@\w.])MJ[ØO][ÅA]R(?![\w]|\.[a-z])", "Marke als Wort statt Logo"),
                              (r"(?i)barista", "„Barista“")]:
            if re.search(muster, sichtbar):
                fehler.append((s, grund, re.search(muster, sichtbar).group(0)))
        # Nach der Verbotsliste v4 gesperrt, im abgenommenen Entwurf aber so gewollt: nur melden, nicht ändern.
        if s == "index.html":
            for muster, grund in [(r"Tülle", "„Tülle“ (v4: überall Ausguss)"), (r"Designed in", "„Designed in“ (Thorsten 06.10.: kein „Entworfen in“)"),
                                  (r"mattes Cremeweiß|mattes Salbeigrün|mattes Schwarz|gebürsteter Edelstahl", "Farb-Unterzeile (Jonah 08.10.: nur Namen)")]:
                for treffer in sorted(set(re.findall(muster, sichtbar))):
                    hinweise.append((grund, treffer))
            for tag, text in p.ueberschriften:
                if text.endswith("."):
                    hinweise.append((f"{tag} endet mit Punkt (v4-Regel)", text))

    # 8. Technik
    for s in alle + list(RECHT) + START:
        q = lesen(s)
        if re.search(r"fonts\.(googleapis|gstatic)\.com", q):
            fehler.append((s, "Google Fonts eingebunden", ""))
        if re.search(r"<meta http-equiv=\"refresh\"", q):
            continue
        for amz in re.findall(r'https://www\.amazon\.de/dp/[^"\s]+', html.unescape(q)):
            if "maas=" not in amz:
                fehler.append((s, "DE-Kauflink ohne Amazon-Attribution", amz))
        if "gc.zgo.at/count.js" not in q:
            fehler.append((s, "GoatCounter fehlt", ""))
    for s in START + list(RECHT):
        q = lesen(s)
        if "/assets/web/site.css" in q or "inter-latin" in q or "cormorant" in q:
            fehler.append((s, "altes Design (site.css, Inter/Cormorant) eingebunden", ""))
        for url in re.findall(r"url\('(/[^']+)'\)", q):
            if not os.path.exists(os.path.join(ROOT, url.strip("/").replace("/", os.sep))):
                fehler.append((s, "Schrift/CSS-Datei fehlt", url))
        if "fetch(" in q:
            fehler.append((s, "fetch() im Skript (Logo muss eingebettet sein)", ""))
        for svg in re.findall(r"<svg data-logo[^>]*>(.*?)</svg>", q, re.S):
            if "<path" not in svg:
                fehler.append((s, "svg[data-logo] ohne eingebettetes Logo", svg[:40]))
        if f'action="{html.escape(BREVO)}"' not in q or 'name="EMAIL"' not in q or 'name="email_address_check"' not in q:
            fehler.append((s, "Brevo-Formular fehlt oder unvollständig", ""))
        if 'onsubmit="return false"' in q:
            fehler.append((s, "Newsletter-Formular abgeschaltet", ""))
        for video in re.findall(r"<video[^>]*>(.*?)</video>", q, re.S):
            quellen = re.findall(r'<source src="([^"]+)" type="video/mp4" media="([^"]+)"', video)
            if not quellen or len(quellen) != video.count("<source"):
                fehler.append((s, "Video ohne media-gesteuerte Quellen", video[:60]))
            for src, media in quellen:
                if "prefers-reduced-motion: no-preference" not in media:
                    fehler.append((s, "Video lädt auch bei reduzierter Bewegung", src))
                groesse = os.path.getsize(os.path.join(ROOT, src.strip("/").replace("/", os.sep)))
                if "max-width: 760px" in media and groesse >= MOBIL_VIDEO_MAX:
                    fehler.append((s, "Mobil-Video zu groß", f"{src} {groesse} B"))
        if not re.search(r"@media \(prefers-reduced-motion: reduce\)\{[^}]*video\{display:none\}", q):
            fehler.append((s, "CSS blendet Video bei reduzierter Bewegung nicht aus", ""))
    la = lesen("latte-art/index.html")
    if '<link rel="canonical" href="https://mjoar.com/">' not in la or 'content="0; url=/"' not in la:
        fehler.append(("latte-art/index.html", "Weiterleitung nicht auf die Startseite", ""))
    if "latte-art" in lesen("sitemap.xml"):
        fehler.append(("sitemap.xml", "latte-art steht in der Sitemap", ""))
    for s in START + list(RECHT):
        if re.search(r'href="[^"]*#latte-art"|href="/latte-art/|href="/en/milk-and-latte-art/', lesen(s)):
            fehler.append((s, "interner Link auf Latte Art", ""))

    # 3. Rechtstexte byte-gleich
    for s, alt in RECHT.items():
        neu = lesen(s)
        a = open(os.path.join(ROOT, "_build", "alt", alt), encoding="utf-8").read()
        art = a[a.index('<article class="legal-card">'):a.index("</article>") + 10]
        if alt == "datenschutz.html":
            # Einzige inhaltliche Änderung seit v2 (Fable 07.10.): Absatz zu mjoar_lang entfällt.
            art, n = DATENSCHUTZ_ENTFAELLT.subn("", art)
            if n != 1:
                fehler.append((s, "Datenschutz: Absatz mjoar_lang nicht genau einmal im Original", alt))
        if art not in neu.replace('<article class="legal-card" lang="de">', '<article class="legal-card">'):
            fehler.append((s, "Rechtstext weicht ab", alt))
        if "mjoar_lang" in neu:
            fehler.append((s, "mjoar_lang steht noch im Datenschutz", alt))

    # 6. Links, Anker, Kaufen
    extern, kaputt = set(), []
    for s in alle + list(RECHT) + START:
        q = lesen(s)
        ziele = re.findall(r'(?:href|src|content|action|data-kaufen)="([^"]+)"', q)
        ziele += [u.split(" ")[0] for s_ in re.findall(r'srcset="([^"]+)"', q) for u in s_.split(", ")]
        ziele += re.findall(r'url=([^"]+)"', q)
        for z in ziele:
            z = html.unescape(z)
            if z.startswith(("http://", "https://", "mailto:")):
                if not z.startswith("https://mjoar.com"):
                    extern.add(z.split("?")[0][:80])
                    continue
                z = z[len("https://mjoar.com"):] or "/"
            if z.startswith("#"):
                if z[1:] and z[1:] not in geparst[s].ids:
                    kaputt.append((s, z))
                continue
            if not z.startswith("/"):
                continue
            pfad, _, anker = z.split("?")[0].partition("#")
            datei = os.path.join(ROOT, pfad.strip("/").replace("/", os.sep))
            if pfad.endswith("/"):
                datei = os.path.join(datei, "index.html")
            if not os.path.exists(datei):
                kaputt.append((s, z))
            elif anker and datei.endswith(".html"):
                rel = os.path.relpath(datei, ROOT).replace(os.sep, "/")
                ids = (geparst[rel] if rel in geparst else parse(rel)).ids
                if anker not in ids:
                    kaputt.append((s, z))
        # Kaufen: DE (und /) amazon.de, EN amazon.co.uk
        amazon = set(re.findall(r'https://www\.amazon\.[a-z.]+/dp/[A-Z0-9]+', q))
        soll = "https://www.amazon.co.uk/dp/" if s.startswith("en/") else "https://www.amazon.de/dp/"
        falsch = sorted(x for x in amazon if not x.startswith(soll))
        if falsch:
            fehler.append((s, "Kaufen-Link auf falschem Marktplatz", ", ".join(falsch)))
        if s.startswith("en/"):
            for x in sorted(set(re.findall(r'https://www\.amazon\.[a-z.]+/[^"\s]*', html.unescape(q)))):
                if not x.startswith("https://www.amazon.co.uk/dp/") or "?" in x or "maas" in x or "tag=" in x:
                    fehler.append((s, "EN: Amazon-Link nicht amazon.co.uk/dp ohne Tag", x))
                elif x.rsplit("/", 1)[1] not in UK_ASINS:
                    fehler.append((s, "EN: unbekannte ASIN", x))
    for lang, links in KAUFEN.items():
        for farbe, url in links.items():
            if lang == "en" and farbe == "ohne":
                continue  # UK hat eine eigene Eltern-ASIN (B0HLWVCFC3), die DE-Eltern-ASIN gibt es auf amazon.co.uk nicht
            if url.rsplit("/", 1)[1].split("?")[0] != KAUFEN["de"][farbe].rsplit("/", 1)[1].split("?")[0]:
                fehler.append(("site.py", f"ASIN {lang}/{farbe} weicht von DE ab", url))

    fehler += en_startseite(entwurf) + rechtsseiten()
    print(f"Copy → Seite: {len(stellen)} Copy-Stellen verglichen (Copy v4 gilt nur noch für die Titel der Weiterleitungen), {len(fehlt)} nicht gefunden")
    for f in fehlt:
        print("  FEHLT", f)
    print(f"Seite → Copy: {gepruefte} Textblöcke auf {len(alle)} Weiterleitungen geprüft; Startseite DE ↔ Entwurf v70: {len(entwurf.bloecke)} Textblöcke, "
          f"{len(entwurf.attrs)} Attribute auf {len(START_DE)} Seiten; EN-Startseite ↔ DE-Aufbau; Rechtsseiten (Kopf/Fuß/Stil, Rechtstext "
          f"gegen _build/alt und origin/main); Technik geprüft. {len(fehler)} Abweichungen")
    for f in fehler:
        print("  ABWEICHUNG", f)
    h_anzahl = sum(len(geparst[s].ueberschriften) for s in alle)
    print(f"Überschriften h1–h4: {h_anzahl} geprüft, keine endet mit Punkt" if not any("endet mit Punkt" in f[1] for f in fehler)
          else "Überschriften h1–h4: siehe Abweichungen")
    print(f"Bewusst nicht aus der Copy ({len(set((k, v) for _, k, v in ausnahmen))} verschiedene):")
    for k, v in sorted(set((k, v) for _, k, v in ausnahmen)):
        print(f"  {k}: {v}")
    print(f"Hinweise Startseite (aus dem abgenommenen Entwurf übernommen, nach Regeln v4 gesperrt; nicht geändert, zur Freigabe):")
    for h in hinweise:
        print(f"  {h[0]}: {h[1]}")
    print(f"Links: {len(alle) + len(RECHT) + len(START)} Seiten, {len(kaputt)} kaputte interne Ziele oder Anker")
    for k in kaputt:
        print("  KAPUTT", k)
    print("Externe Ziele:")
    for x in sorted(extern):
        print("  " + x)
    return 1 if fehler or kaputt or fehlt else 0


if __name__ == "__main__":
    sys.exit(main())
