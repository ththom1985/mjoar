# Prüfungen für den PR (mjoar.com v4, One-Pager, Auftrag Fable 08.10.2026):
#  1. Wortgleichheit Seite → Copy: jeder sichtbare Textblock aller erzeugten Seiten (One-Pager, Kopf und Fuß der
#     Rechtsseiten, Weiterleitungen) steht wortgleich in MJOAR_WEB_COPY_v4.md. Ausnahmen werden einzeln gelistet:
#     Alt-Texte und Bedienetiketten (texte_v4.ALT), NICHT_IN_COPY, Titel der Rechtsseiten.
#  2. Wortgleichheit Copy → Seite: jede Inhaltsstelle der Copy (DE und EN) steht auf dem One-Pager der Sprache.
#     Regie bleibt draußen: [J], [J*], Klammerhinweise nach [J*]-Zeilen, [BILD …], Bildschlüssel, Feldbezeichnungen.
#  3. Rechtstexte: Artikel von Impressum/Datenschutz byte-gleich mit den bisherigen Dateien.
#  4. Keine Überschrift (h1–h4) endet mit „.“.
#  5. Verbotsliste: Gedankenstriche, „Entworfen in“, Preis, sichtbares „LFGB“, Farb-Unterzeilen, satin, Tülle.
#  6. Links: interne Ziele existieren (Dateien und Anker), Kaufen DE → amazon.de, EN → amazon.co.uk; externe Ziele gelistet.
#   python _build/pruefen.py        (aus dem Worktree, nach site.py)
import html
import importlib.util
import os
import re
import sys
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texte_v4 import ALT, NICHT_IN_COPY, RECHT_TITEL  # noqa: E402

# _build/site.py heißt wie das Standardmodul „site“: über den Dateipfad laden.
_spec = importlib.util.spec_from_file_location("mjoar_site", os.path.join(os.path.dirname(os.path.abspath(__file__)), "site.py"))
_mjoar_site = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mjoar_site)
DATENSCHUTZ_ENTFAELLT = _mjoar_site.DATENSCHUTZ_ENTFAELLT
KAUFEN = _mjoar_site.KAUFEN
WEITERLEITUNGEN = _mjoar_site.WEITERLEITUNGEN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPY = r"C:/Users/ththomas/OneDrive/01_THOMAS_MERCANTILE_BUSINESS/01_Marke_MJOAR/03_Website_Landingpage/MJOAR_WEB_COPY_v4.md"
ONEPAGER = {"de": ["de/index.html", "index.html"], "en": ["en/index.html"]}
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

    alle = [s for l in ONEPAGER.values() for s in l] + list(RECHT) + UMLEITUNG
    geparst = {s: parse(s) for s in alle}

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
                              (r"€|EUR\b|£", "Preis"), (r"LFGB", "LFGB sichtbar"), (r"(?i)la marzocco", "Maschinen-Schriftzug genannt"),
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
    stellen = copy_stellen()
    fehlt = [(l, x) for l, x in stellen if x not in seitentext[l]]
    # Root "/" ist der deutsche One-Pager: gleicher Inhalt wie /de/
    if geparst["index.html"].bloecke != geparst["de/index.html"].bloecke:
        fehler.append(("index.html", "Startseite / weicht vom deutschen One-Pager ab", ""))

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
    for s in alle:
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
    for lang, links in KAUFEN.items():
        for farbe, url in links.items():
            if url.rsplit("/", 1)[1] != KAUFEN["de"][farbe].rsplit("/", 1)[1]:
                fehler.append(("site.py", f"ASIN {lang}/{farbe} weicht von DE ab", url))

    print(f"Copy → Seite: {len(stellen)} Copy-Stellen (DE {sum(1 for l, _ in stellen if l == 'de')}, EN {sum(1 for l, _ in stellen if l == 'en')}) verglichen, {len(fehlt)} nicht gefunden")
    for f in fehlt:
        print("  FEHLT", f)
    print(f"Seite → Copy: {gepruefte} Textblöcke auf {len(alle)} Seiten geprüft, {len(fehler)} Abweichungen")
    for f in fehler:
        print("  ABWEICHUNG", f)
    h_anzahl = sum(len(geparst[s].ueberschriften) for s in alle)
    print(f"Überschriften h1–h4: {h_anzahl} geprüft, keine endet mit Punkt" if not any("endet mit Punkt" in f[1] for f in fehler)
          else "Überschriften h1–h4: siehe Abweichungen")
    print(f"Bewusst nicht aus der Copy ({len(set((k, v) for _, k, v in ausnahmen))} verschiedene):")
    for k, v in sorted(set((k, v) for _, k, v in ausnahmen)):
        print(f"  {k}: {v}")
    print(f"Links: {len(alle)} Seiten, {len(kaputt)} kaputte interne Ziele oder Anker")
    for k in kaputt:
        print("  KAPUTT", k)
    print("Externe Ziele:")
    for x in sorted(extern):
        print("  " + x)
    return 1 if fehler or kaputt or fehlt else 0


if __name__ == "__main__":
    sys.exit(main())
