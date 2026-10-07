# Prüfungen für den PR (Auftrag Website 07.10.2026):
#  1. Wortgleichheit: jeder sichtbare Textblock der 8 Inhaltsseiten steht wortgleich in MJOAR_WEB_COPY_v3.md.
#     Ausnahmen (bewusst nicht aus der Copy) werden einzeln gelistet: Alt-Texte, Bedienetiketten, NICHT_IN_COPY.
#  2. Rechtstexte: Artikel von Impressum/Datenschutz byte-gleich mit den bisherigen Dateien.
#  3. Keine Gedankenstriche, kein „Entworfen in“/„Designed in“, kein Preis, kein sichtbares „LFGB“.
#  4. Links: alle internen Ziele (href/src/srcset) existieren als Datei; externe Ziele werden gelistet.
#   python _build/pruefen.py        (aus dem Worktree, nach site.py)
import html
import os
import re
import sys
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texte_v3 import ALT, NICHT_IN_COPY  # noqa: E402
import importlib.util  # noqa: E402

# _build/site.py heißt wie das Standardmodul „site“: über den Dateipfad laden.
_spec = importlib.util.spec_from_file_location("mjoar_site", os.path.join(os.path.dirname(os.path.abspath(__file__)), "site.py"))
_mjoar_site = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mjoar_site)
DATENSCHUTZ_ENTFAELLT = _mjoar_site.DATENSCHUTZ_ENTFAELLT

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPY = r"C:/Users/ththomas/OneDrive/01_THOMAS_MERCANTILE_BUSINESS/01_Marke_MJOAR/03_Website_Landingpage/MJOAR_WEB_COPY_v3.md"
INHALT = {"de": ["de/", "de/lun-350/", "de/milch-und-latte-art/", "de/ueber-uns/"],
          "en": ["en/", "en/lun-350/", "en/milk-and-latte-art/", "en/about/"]}
RECHT = {"de/impressum/": "impressum.html", "de/datenschutz/": "datenschutz.html", "en/imprint/": "impressum.html", "en/privacy/": "datenschutz.html"}
BLOCK = {"p", "h1", "h2", "h3", "li", "dt", "dd", "th", "td", "legend", "figcaption", "button", "label", "title", "summary", "div", "section", "nav", "span"}
INLINE = {"strong", "em", "a", "b", "i"}


def norm(text):
    text = html.unescape(text).replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text).strip()


def korpus():
    roh = open(COPY, encoding="utf-8").read().replace("**", "")
    # Zeilen ohne Aufzählungszeichen und Nummern, Tabellenzellen einzeln
    teile = []
    for zeile in roh.splitlines():
        z = re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", zeile)
        teile.append(z)
        if "|" in z:
            teile.extend(c.strip() for c in z.split("|"))
    return norm(" \n ".join(teile)), roh


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.bloecke, self.puffer, self.attrs, self.ignorieren = [], [], [], 0

    def flush(self):
        t = norm("".join(self.puffer))
        if t:
            self.bloecke.append(t)
        self.puffer = []

    nav = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "head"):
            self.ignorieren += 1
        if tag == "nav":
            self.nav += 1
        if tag in BLOCK or (tag == "a" and self.nav):
            self.flush()
        for k in ("alt", "placeholder", "aria-label"):
            if a.get(k):
                self.attrs.append((k, norm(a[k])))
        if tag == "meta" and a.get("name") == "description":
            self.attrs.append(("description", norm(a.get("content", ""))))
        if tag == "title":
            self.ignorieren -= 0

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head"):
            self.ignorieren -= 1
        if tag == "nav":
            self.nav -= 1
        if tag in BLOCK or (tag == "a" and self.nav):
            self.flush()

    def handle_data(self, data):
        if not self.ignorieren:
            self.puffer.append(data)


def titel(seite_html):
    m = re.search(r"<title>(.*?)</title>", seite_html, re.S)
    return norm(m.group(1)) if m else ""


def main():
    korp, roh = korpus()
    fehler, ausnahmen = [], []
    erlaubt_alt = set()
    for lang in ALT:
        for k, v in ALT[lang].items():
            if isinstance(v, dict):
                erlaubt_alt.update(v.values())
            else:
                erlaubt_alt.add(v)
    erlaubt_text = {s for l in NICHT_IN_COPY.values() for s in l}
    alt_formate = [ALT[l]["farbe"] for l in ALT] + [ALT[l]["verpackung"] for l in ALT]

    def ist_alt(s):
        if s in erlaubt_alt:
            return True
        return any(re.fullmatch(re.escape(f).replace(re.escape("{}"), r"\w+"), s) for f in alt_formate)

    gepruefte = 0
    for lang, seiten in INHALT.items():
        for s in seiten:
            pfad = os.path.join(ROOT, s.replace("/", os.sep), "index.html")
            quelle = open(pfad, encoding="utf-8").read()
            p = Text()
            p.feed(quelle)
            p.flush()
            for b in p.bloecke + [titel(quelle)]:
                gepruefte += 1
                if b in korp or b in {"|", "·", "·  ·"} or re.fullmatch(r"[·| ]+", b):
                    continue
                teile = [x.strip() for x in re.split(r"\s·\s", b) if x.strip()]
                if len(teile) > 1 and all(x in korp for x in teile):
                    continue
                # „Bezeichnung: Link“, wenn die Copy für den Link [Link] setzt und der Linktext aus der Copy stammt
                kopf_, _, rest = b.partition(": ")
                if rest and f"{kopf_}: [" in korp and rest in korp:
                    continue
                if b in erlaubt_text:
                    ausnahmen.append((s, "Text", b))
                    continue
                fehler.append((s, "nicht in Copy v3", b))
            for k, v in p.attrs:
                if k == "description":
                    gepruefte += 1
                    if v not in korp:
                        fehler.append((s, "Meta-Beschreibung nicht in Copy v3", v))
                elif k in ("placeholder",):
                    if v not in korp:
                        fehler.append((s, k, v))
                elif ist_alt(v):
                    ausnahmen.append((s, k, v))
                else:
                    fehler.append((s, f"{k} unbekannt", v))
            sichtbar = " ".join(p.bloecke)
            for muster, grund in [(r"[\u2013\u2014]|\s-\s", "Gedankenstrich"), (r"Entworfen in|Designed in", "Entworfen/Designed in"),
                                  (r"€|EUR\b", "Preis"), (r"LFGB", "LFGB sichtbar"), (r"(?i)la marzocco", "Maschinen-Schriftzug genannt"),
                                  (r"(?i)satin|seidenmatt|soft matt", "satiniert/satin/seidenmatt (Thorsten 07.10.: nicht mehr)"),
                                  (r"Tülle", "Tülle (Thorsten 07.10.: überall Ausguss)")]:
                if re.search(muster, sichtbar):
                    fehler.append((s, grund, re.search(muster, sichtbar).group(0)))
    # Rechtstexte byte-gleich
    for s, alt in RECHT.items():
        neu = open(os.path.join(ROOT, s.replace("/", os.sep), "index.html"), encoding="utf-8").read()
        a = open(os.path.join(ROOT, "_build", "alt", alt), encoding="utf-8").read()
        art = a[a.index('<article class="legal-card">'):a.index("</article>") + 10]
        if alt == "datenschutz.html":
            # Einzige inhaltliche Änderung (Fable 07.10., im PR ausgewiesen): Absatz zu mjoar_lang entfällt.
            art, n = DATENSCHUTZ_ENTFAELLT.subn("", art)
            if n != 1:
                fehler.append((s, "Datenschutz: Absatz mjoar_lang nicht genau einmal im Original", alt))
        if art not in neu.replace('<article class="legal-card" lang="de">', '<article class="legal-card">'):
            fehler.append((s, "Rechtstext weicht ab", alt))
        if "mjoar_lang" in neu:
            fehler.append((s, "mjoar_lang steht noch im Datenschutz", alt))
    # Links
    extern, kaputt, seiten_alle = set(), [], []
    for wurzel, _, dateien in os.walk(ROOT):
        if any(x in wurzel for x in (".git", "_build", "node_modules")):
            continue
        for d in dateien:
            if d.endswith(".html"):
                seiten_alle.append(os.path.join(wurzel, d))
    neue = [os.path.join(ROOT, x.replace("/", os.sep), "index.html") for l in INHALT.values() for x in l] + \
           [os.path.join(ROOT, x.replace("/", os.sep), "index.html") for x in RECHT] + \
           [os.path.join(ROOT, "index.html"), os.path.join(ROOT, "impressum.html"), os.path.join(ROOT, "datenschutz.html"), os.path.join(ROOT, "latte-art", "index.html")]
    for f in neue:
        q = open(f, encoding="utf-8").read()
        ziele = re.findall(r'(?:href|src|content|action|data-kaufen)="([^"]+)"', q) + [u.split(" ")[0] for s_ in re.findall(r'srcset="([^"]+)"', q) for u in s_.split(", ")]
        ziele += re.findall(r'url=([^"]+)"', q)
        for z in ziele:
            z = html.unescape(z)
            if z.startswith(("http://", "https://", "mailto:")):
                if not z.startswith("https://mjoar.com"):
                    extern.add(z.split("?")[0][:80])
                    continue
                z = z[len("https://mjoar.com"):] or "/"
            if not z.startswith("/"):
                continue
            pfad = z.split("#")[0].split("?")[0]
            datei = os.path.join(ROOT, pfad.strip("/").replace("/", os.sep))
            if pfad.endswith("/"):
                datei = os.path.join(datei, "index.html")
            if not os.path.exists(datei):
                kaputt.append((os.path.relpath(f, ROOT), z))
    # Gegenrichtung: jeder Inhaltssatz der Copy (Abschnitte A bis F) steht auf einer Seite der passenden Sprache.
    seitentext = {}
    for lang, seiten in INHALT.items():
        alles = []
        for s in seiten:
            q = open(os.path.join(ROOT, s.replace("/", os.sep), "index.html"), encoding="utf-8").read()
            p = Text()
            p.feed(q)
            p.flush()
            alles += p.bloecke + [v for _, v in p.attrs] + [titel(q)]
        seitentext[lang] = norm(" \n ".join(alles))
    fehlt, verglichen = [], 0
    abschnitt, sprache = "", None
    # Bezeichnungen der Copy vor dem Inhalt („Überschrift:“, „Absatz 1:“, „klein:“ …), Regieanweisungen ohne Seitentext
    label = re.compile(r"^(?:Überschrift|Heading|Unterzeile|Subline|Dachzeile|Eyebrow|Zeile \(groß\)|Line \(large\)|Satz|Sentence|Text|Link|Zweitlink|Second link|"
                       r"Absatz(?: \d)?|Paragraph(?: \d)?|Einleitung|Intro|Schluss|Close|Titel|Title|klein|Klein|small|Small|Zeile darunter, klein|Small line|"
                       r"Kopf|Header|Fuß, links|Fuß, Mitte|Fuß, rechts|Footer left|Footer middle|Footer right|Ganz unten|Bottom|"
                       r"Link je Farbe|Link per colour|Farbe|Colour):\s*")
    regie = ("Unter den Kannen", "Under the jugs", "Drei Punkte", "Three points", "Häufige Fehler", "Common mistakes",
             "Newsletter wie", "Newsletter as", "BILD", "Logo")
    for zeile in open(COPY, encoding="utf-8").read().splitlines():
        if zeile.startswith("## "):
            abschnitt, sprache = zeile[3:4], None
            continue
        if zeile.startswith("#"):
            continue
        if zeile.strip() in ("**DE**", "**EN**"):
            sprache = zeile.strip()[2:4].lower()
            continue
        if abschnitt not in "ABCDE" or abschnitt == "":
            continue
        stuecke = []
        if zeile.startswith("|"):
            zellen = [z.strip() for z in zeile.strip("|").split("|")]
            if len(zellen) == 4 and not set("".join(zellen)) <= set("-") and zellen[0] != "DE":
                stuecke = [("de", zellen[0]), ("de", zellen[1]), ("en", zellen[2]), ("en", zellen[3])]
        else:
            m = re.match(r"^\*\*(DE|EN):\*\*\s*(.+)$", zeile.strip())
            if m:
                sprache, zeile = m.group(1).lower(), m.group(2)
            if not sprache:
                continue
            inhalt = re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", zeile).replace("**", "").strip()
            if " / " in inhalt and abschnitt == "C" and inhalt.startswith(("Darunter", "Von Hand")):
                inhalt = inhalt.split(":", 1)[-1]
                de_, en_ = inhalt.split(" / ", 1)
                stuecke = [("de", de_), ("en", en_)]
            else:
                inhalt = label.sub("", inhalt)
                stuecke = [(sprache, s) for s in re.split(r"\s·\s|\s\|\s|\[[^\]]*\]|\(Name groß[^)]*\)", inhalt)]
        for sp, stueck in stuecke:
            stueck = label.sub("", norm(stueck)).strip(" .:")
            if len(stueck) < 4 or stueck.startswith(regie) or stueck.endswith(":") or stueck in ("[LFGB]",):
                continue
            verglichen += 1
            # „**Juniper**: Grün, matt“ ist Listenschreibweise der Copy (Name, darunter die Beschreibung). Auf der Seite
            # stehen beide ohne Doppelpunkt untereinander (Fable 07.10.): beide Teile einzeln prüfen.
            farbe = re.match(r"^(Juniper|Linen|Onyx|Steel): (.+)$", stueck)
            if farbe and all(x in seitentext[sp] for x in farbe.groups()):
                continue
            if stueck.rstrip(".") not in seitentext[sp]:
                fehlt.append((abschnitt, sp, stueck))
    print(f"Gegenrichtung Copy → Seiten: {verglichen} Copy-Stellen verglichen, {len(fehlt)} nicht gefunden")
    for f in fehlt:
        print("  FEHLT", f)
    print(f"Wortgleichheit: {gepruefte} Textblöcke auf 8 Inhaltsseiten geprüft, {len(fehler)} Abweichungen")
    for f in fehler:
        print("  ABWEICHUNG", f)
    print(f"Bewusst nicht aus der Copy ({len(set((k, v) for _, k, v in ausnahmen))} verschiedene):")
    for k, v in sorted(set((k, v) for _, k, v in ausnahmen)):
        print(f"  {k}: {v}")
    print(f"Links: {len(neue)} Seiten, {len(kaputt)} kaputte interne Ziele")
    for k in kaputt:
        print("  KAPUTT", k)
    print("Externe Ziele:")
    for x in sorted(extern):
        print("  " + x)
    return 1 if fehler or kaputt else 0


if __name__ == "__main__":
    sys.exit(main())
