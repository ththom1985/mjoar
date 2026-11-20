# mjoar.com SEO-Entwurf (20.11.2026, ENTWURF, nicht live): Produktseite /de/lun-350/ und Ratgeber /de/milch-und-latte-art/.
# Stil (<style>), Schattenlage, Kopf und Fuß werden wortgleich aus de/index.html geschnitten, damit sich beide Seiten
# nahtlos ins bestehende Design einfügen. Neu ist nur SEITEN_CSS (Bausteine mit denselben Farben, Schriften, Abständen).
#   python _build/seo_entwurf.py      (aus dem Worktree; schreibt de/lun-350/index.html, de/milch-und-latte-art/index.html)
# Hinweis: site.py kennt diese Seiten noch nicht und würde sie (wie die unsichtbaren SEO-Änderungen aus PR #50) beim
# nächsten Lauf mit Weiterleitungen überschreiben. Vor dem nächsten site.py-Lauf nachziehen.
import html
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://mjoar.com"
e = html.escape

START = open(os.path.join(ROOT, "de", "index.html"), encoding="utf-8").read()


def teil(start, ende, quelle=START):
    a = quelle.index(start)
    b = quelle.index(ende, a) + len(ende)
    return quelle[a:b]


STIL = teil("<style>", "</style>")
SCHATTEN = teil('<div class="schattenlage"', "</div>")
KOPF = teil('<header class="gut">', "</header>")
FUSS = teil('<footer class="fuss gut"', "</footer>")
ZAEHLER = '<script data-goatcounter="https://mjoar.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>'
LOGO_TEXT = re.search(r'<svg data-logo class="logo-text".*?</svg>', START, re.S).group(0)

# Kauflinks wortgleich aus der Startseite (Attribution-Tags), Preise DE laut STAND.md Abschnitt LUN (seit 20.11.2026 14:16)
KAUFEN = {f: html.unescape(re.search(rf'data-f="{f}"[^>]*data-kaufen="([^"]+)"', START).group(1)) for f in
          ["juniper", "linen", "onyx", "steel"]}
ASIN = {f: re.search(r"/dp/(\w+)", u).group(1) for f, u in KAUFEN.items()}
PREIS_STAND = "20.11.2026"
FARBEN = [
    # schlüssel, Name, Text auf der Seite (wie Startseite), Farbwort für Schema/Alt, Preis, SKU, Swatch, Dateiname
    ("juniper", "Juniper", "mattes Salbeigrün", "Grün matt", "22.90", "MJ-LUN-350-JUN", "#8FA382", "milchkaennchen-latte-art-matt-gruen-juniper"),
    ("linen", "Linen", "mattes Cremeweiß", "Cremeweiß matt", "22.90", "MJ-LUN-350-LIN", "#E9E1D2", "milchkaennchen-latte-art-matt-cremeweiss-linen"),
    ("onyx", "Onyx", "mattes Schwarz", "Schwarz matt", "19.90", "MJ-LUN-350-ONX", "#1D1E1D", "milchkaennchen-latte-art-matt-schwarz-onyx"),
    ("steel", "Steel", "gebürsteter Edelstahl", "Edelstahl gebürstet", "17.90", "MJ-LUN-350-STL", "linear-gradient(135deg,#E3E5E6,#9EA3A6)", "milchkaennchen-latte-art-edelstahl-gebuerstet-steel"),
]


def euro(p):
    return p.replace(".", ",") + " €"


# Bilder mit sprechenden Dateinamen (Google Bilder): Kopien der Freisteller der Startseite, Inhalt byte-gleich
BILDORDNER = os.path.join(ROOT, "assets", "lun-350")


def bilder_kopieren():
    os.makedirs(BILDORDNER, exist_ok=True)
    for f, *_rest in FARBEN:
        datei = _rest[-1]
        for g in ["800", "1600"]:
            shutil.copyfile(os.path.join(ROOT, "assets", "start", f"frei-{f}-{g}.webp"),
                            os.path.join(BILDORDNER, f"{datei}-{g}.webp"))


SEITEN_CSS = """/* Unterseiten (SEO-Entwurf 20.11.2026): Kopf liegt wie auf der Startseite über dem ersten Abschnitt, Bausteine mit den Werten der Startseite */
.lun.seitenkopf{padding-block:112px 88px}
.lun h1{font-family:var(--display);font-weight:300;font-size:clamp(32px,4.2vw,54px);line-height:1.05;margin:10px 0 18px}
.lun .kauf{display:flex;gap:22px;align-items:center;flex-wrap:wrap}
.lun .preis{font:600 15px var(--body);color:var(--text)}
.preis-hinweis{margin:12px 0 0;font-size:12.5px;color:var(--taupe)}
/* Text mit Bild, Aufbau wie Über uns */
.tb{padding-block:88px}
.tb-in{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:56px;align-items:center}
.tb.gedreht .tb-bild{order:-1}
.tb.ratkopf{padding-block:112px 56px}
.tb h1{font-family:var(--display);font-weight:300;font-size:clamp(34px,4.2vw,54px);line-height:1.06;letter-spacing:-.01em;margin:10px 0 22px}
.tb h2,.blick h2,.rat h2{font-family:var(--display);font-weight:300;font-size:clamp(30px,3.6vw,46px);line-height:1.08;margin:8px 0 22px}
.tb-text p{margin:0 0 14px;max-width:46ch;color:#4A423B}
.tb-text .link{display:inline-block;margin-top:10px;font-size:14px}
.tb-bild{margin:0;aspect-ratio:4/5;overflow:hidden;box-shadow:inset 0 0 0 1px rgba(140,127,112,.3);background:rgba(239,229,214,.85)}
.tb-bild img{width:100%;height:100%;object-fit:cover;display:block}
/* Farben: Karten wie im Abschnitt Produkte */
.farbreihe{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;border-top:1px solid var(--linie);padding-top:30px}
.karte .preis{color:var(--text);font-weight:600}
/* Auf einen Blick: Begriffe wie die Merkmale der LUN-Bühne */
.blick{padding-block:88px 72px}
.daten{margin:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:26px 32px;border-top:1px solid var(--linie);padding-top:26px}
.daten div{min-width:0}
.daten dt{font-family:var(--display);font-weight:400;font-size:16px;color:var(--text)}
.daten dd{margin:3px 0 0;font-size:13px;color:var(--taupe);line-height:1.5}
.blick .klein{margin:22px 0 0;font-size:12.5px;color:var(--taupe)}
.blick .klein a{color:var(--taupe)}
/* Ratgeber: ruhige Textspalte wie die Rechtsseiten (max. 68 Zeichen), Abschnitte mit feiner Linie */
.rat{padding-block:24px 88px}
.rat-spalte{max-width:68ch}
.rat-block{border-top:1px solid var(--linie);padding-block:34px 18px}
.rat-block h2{font-size:clamp(26px,2.8vw,34px);margin:0 0 16px}
.rat-block h3{font-family:var(--display);font-weight:400;font-size:19px;letter-spacing:.01em;margin:22px 0 8px;color:var(--text)}
.rat-block p{margin:0 0 14px;color:#4A423B;line-height:1.7}
.rat-block ol{margin:0 0 14px;padding-left:1.3em;color:#4A423B;line-height:1.7}
.rat-block li{margin:0 0 12px;padding-left:.3em}
.rat-block li strong,.rat-block p strong{color:var(--text);font-weight:600}
.rat-bilder{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin:8px 0 34px;max-width:860px}
.rat-bilder figcaption span{max-width:40ch}
/* Hinweis auf die andere Seite: schmales Band */
.weiter{padding-block:56px}
.weiter-in{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:24px;align-items:center;border-top:1px solid var(--linie);border-bottom:1px solid var(--linie);padding-block:30px}
.weiter h2{font-family:var(--display);font-weight:300;font-size:clamp(24px,2.6vw,32px);line-height:1.1;margin:6px 0 8px}
.weiter p{margin:0;color:#4A423B;max-width:56ch}
/* ENTWURF: fehlende Fakten sichtbar markieren, vor dem Livegang entfernen */
.offen{display:inline-block;font-size:12px;letter-spacing:.04em;color:#8a4b2a;border:1px dashed #b98a6e;border-radius:6px;padding:2px 8px;background:rgba(255,255,255,.45)}
@media (max-width:1000px){.farbreihe{grid-template-columns:repeat(2,minmax(0,1fr))}.daten{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:760px){.tb-in{grid-template-columns:minmax(0,1fr);gap:32px}.tb.gedreht .tb-bild{order:0}.tb{padding-block:64px}.lun.seitenkopf{padding-block:84px 64px}.weiter-in{grid-template-columns:minmax(0,1fr)}.rat{padding-block:8px 72px}.tb.ratkopf{padding-block:84px 40px}}
@media (max-width:480px){.daten{grid-template-columns:minmax(0,1fr)}.rat-bilder{grid-template-columns:minmax(0,1fr)}}"""


def kopf_fuer(selbst, en_ziel):
    k = KOPF.replace('href="#produkte"', 'href="/de/#produkte"').replace('href="#uns"', 'href="/de/#uns"')
    alt_de = 'href="/de/" lang="de" hreflang="de" aria-current="page"'
    alt_en = 'href="/en/" lang="en" hreflang="en"'
    assert k.count(alt_de) == 1 and k.count(alt_en) == 1, "Sprachlinks im Kopf nicht gefunden"
    k = k.replace(alt_de, f'href="{selbst}" lang="de" hreflang="de" aria-current="page"')
    k = k.replace(alt_en, f'href="{en_ziel}" lang="en" hreflang="en"')
    assert 'href="#' not in k
    return k


def head(titel, beschreibung, pfad, og_typ, og_alt, jsonld):
    assert len(titel) <= 60, (titel, len(titel))
    assert len(beschreibung) <= 160, (beschreibung, len(beschreibung))
    url = SITE + pfad
    return f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(titel)}</title>
  <meta name="description" content="{e(beschreibung)}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="{og_typ}">
  <meta property="og:site_name" content="MJØÅR">
  <meta property="og:title" content="{e(titel)}">
  <meta property="og:description" content="{e(beschreibung)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/web/og-familie.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{e(og_alt)}">
  <meta property="og:locale" content="de_DE">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(titel)}">
  <meta name="twitter:description" content="{e(beschreibung)}">
  <meta name="twitter:image" content="{SITE}/assets/web/og-familie.jpg">
  <script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/jost-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
{STIL.replace("</style>", SEITEN_CSS + chr(10) + "</style>")}
{ZAEHLER}
</head>"""


def bild(src, alt, eager=False):
    lazy = "" if eager else ' loading="lazy"'
    return f'<img src="{src}" decoding="async" alt="{e(alt)}"{lazy}>'


# ---------------------------------------------------------------------------------------------------------------
# Produktseite /de/lun-350/

LUN_TITEL = "LUN 350 Milchkännchen für Latte Art | MJØÅR (MJOAR)"
LUN_BESCHR = ("LUN 350 von MJØÅR (MJOAR): Milchkännchen für Latte Art aus 1 mm Edelstahl 304, 350 ml, Skala innen. "
              "Matt grün, schwarz, cremeweiß oder Edelstahl.")


def lun_jsonld():
    varianten = []
    for f, name, text, farbwort, preis, sku, _sw, datei in FARBEN:
        varianten.append({
            "@type": "Product",
            "@id": f"{SITE}/de/lun-350/#{f}",
            "name": f"LUN 350 Milchkännchen {name} ({farbwort})",
            "sku": sku,
            "color": f"{farbwort} ({name})",
            "image": f"{SITE}/assets/lun-350/{datei}-1600.webp",
            "offers": {"@type": "Offer", "url": f"https://www.amazon.de/dp/{ASIN[f]}", "price": preis,
                       "priceCurrency": "EUR", "itemCondition": "https://schema.org/NewCondition"},
        })
    return {"@context": "https://schema.org", "@graph": [{
        "@type": "ProductGroup",
        "@id": f"{SITE}/de/lun-350/#lun",
        "name": "LUN 350 Milchkännchen",
        "description": ("Milchkännchen für Latte Art, 350 ml, aus 1 mm Edelstahl 304 (ganze Kanne einschließlich Griff), "
                        "Skala innen in ml und oz, spülmaschinengeeignet. Vier Farben: Juniper (Grün matt), "
                        "Linen (Cremeweiß matt), Onyx (Schwarz matt), Steel (Edelstahl gebürstet)."),
        "url": f"{SITE}/de/lun-350/",
        "brand": {"@type": "Brand", "name": "MJØÅR", "alternateName": "MJOAR"},
        "manufacturer": {"@id": f"{SITE}/#org"},
        "productGroupID": "MJ-LUN-350",
        "variesBy": ["https://schema.org/color"],
        "material": "Edelstahl 304",
        "weight": {"@type": "QuantitativeValue", "value": 198, "unitCode": "GRM"},
        "image": [f"{SITE}/assets/lun-350/{d}-1600.webp" for *_x, d in FARBEN]
                 + [f"{SITE}/assets/web/detail-ausguss-960.webp", f"{SITE}/assets/web/detail-skala-784.webp"],
        "hasVariant": varianten,
    }]}


def lun_seite():
    j, jn, jt, jw, jp, *_r = FARBEN[0]
    knoepfe = "\n".join(
        f'        <button type="button" aria-pressed="{"true" if i == 0 else "false"}" data-f="{f}" data-n="{name} · {text}" '
        f'data-preis="{euro(preis)}" data-bild="/assets/lun-350/{datei}-1600.webp" data-alt="LUN Milchkännchen 350 ml {farbwort.lower()} ({name})" '
        f'data-kaufen="{e(KAUFEN[f])}" style="--c:{sw}" aria-label="{name}"></button>'
        for i, (f, name, text, farbwort, preis, sku, sw, datei) in enumerate(FARBEN))
    karten = "\n".join(
        f'''      <article class="karte da" id="farbe-{f}">
        <div class="bild">{bild(f"/assets/lun-350/{datei}-800.webp", f"LUN Milchkännchen 350 ml für Latte Art, {farbwort.lower()} ({name})")}</div>
        <div class="info"><h3>{name}</h3><p>{text[0].upper() + text[1:]} · <span class="preis">{euro(preis)}</span></p><a class="link" href="{e(KAUFEN[f])}" target="_blank" rel="noopener">Bei Amazon</a></div>
      </article>''' for f, name, text, farbwort, preis, sku, sw, datei in FARBEN)
    j_datei = FARBEN[0][7]
    return f"""{head(LUN_TITEL, LUN_BESCHR, "/de/lun-350/", "product", "Die LUN in vier Farben", lun_jsonld())}
<body id="top" class="unterseite">

{SCHATTEN}

{kopf_fuer("/de/lun-350/", "/en/#lun")}

<main id="inhalt">
<!-- 1 · Kopf: LUN-Bühne der Startseite, hier mit H1 -->
<section class="lun seitenkopf gut" id="lun" aria-label="LUN 350">
  <div class="wrap in">
    <div class="bildspalte">
    <figure class="buehne" id="buehne">
      <span class="riesig" id="riesig" aria-hidden="true">LUN</span>
      <i class="bodenschatten" aria-hidden="true"></i>
      <div class="kanne"><img id="lun-bild" src="/assets/lun-350/{j_datei}-1600.webp" decoding="async" fetchpriority="high" alt="LUN Milchkännchen 350 ml grün matt (Juniper)"></div>
    </figure>
    </div>
    <div class="text">
      <p class="eyebrow">LUN 350 · Milchkännchen</p>
      <h1>LUN 350, das Milchkännchen für Latte&nbsp;Art</h1>
      <p>Die LUN macht nicht nur beim Milchaufschäumen eine gute Figur. In jeder der vier Farben macht sie deine Kaffee-Ecke ein Stück schöner. Durch den Korpus aus 1 mm dickem Edelstahl 304 liegt sie gut in der Hand und fühlt sich richtig wertig an. Der präzise Ausguss ist für Latte Art gemacht, damit Herz und Rosetta gelingen.</p>
      <div class="farben" role="group" aria-label="Farbe wählen">
{knoepfe}
      </div>
      <p class="farbname" id="lun-name">{jn} · {jt}</p>
      <dl class="merkmale">
        <div><dt>350 ml</dt><dd>Genug Milch für zwei Flat White oder einen Cappuccino.</dd></div>
        <div><dt>Maße</dt><dd>93&nbsp;mm hoch, Ø&nbsp;75&nbsp;mm.</dd></div>
        <div><dt>Spülmaschinengeeignet</dt><dd>Von Hand gespült bleibt sie am längsten schön.</dd></div>
      </dl>
      <div class="kauf"><a class="knopf" id="lun-kauf" href="{e(KAUFEN["juniper"])}" target="_blank" rel="noopener">Bei Amazon kaufen</a><span class="preis" id="lun-preis">{euro(jp)}</span></div>
      <p class="preis-hinweis">Preis inkl. MwSt. bei Amazon, Stand {PREIS_STAND}. Bestellung und Versand über Amazon.</p>
    </div>
  </div>
</section>

<!-- 2 · Ausguss -->
<section class="tb gut durch" id="ausguss" aria-label="Ausguss">
  <div class="wrap tb-in">
    <div class="tb-text">
      <p class="eyebrow">Der Ausguss</p>
      <h2>Für Herz, Tulpe und Rosetta</h2>
      <p>Der Ausguss der LUN ist für Latte Art geformt. Er ist nicht zu breit, damit du den Milchstrahl genau führen kannst.</p>
      <p>Am Anfang gießt du aus etwas Höhe in die Mitte der Tasse, damit sich Milch und Espresso verbinden. Ist die Tasse etwa halb voll, gehst du mit dem Ausguss ganz nah an die Oberfläche. Jetzt bleibt die Milch oben, und das Muster entsteht.</p>
      <a class="link" href="/de/milch-und-latte-art/#aufschaeumen">Milch aufschäumen, Schritt für Schritt</a>
    </div>
    <figure class="tb-bild">{bild("/assets/web/detail-ausguss-960.webp", "Latte-Art-Ausguss des Milchkännchens LUN in Schwarz matt, gefüllt mit aufgeschäumter Milch")}</figure>
  </div>
</section>

<!-- 3 · Korpus -->
<section class="tb gedreht gut durch" id="korpus" aria-label="Korpus">
  <div class="wrap tb-in">
    <div class="tb-text">
      <p class="eyebrow">Der Korpus</p>
      <h2>Ein ganzer Millimeter Edelstahl</h2>
      <p>Die LUN ist aus einem Millimeter Edelstahl 304 gefertigt, die ganze Kanne einschließlich Griff. Das gibt ihr Stabilität: Sie ist robust, fühlt sich wertig an, verformt sich nicht und hält dadurch länger.</p>
      <p>Innen ist sie blanker, unbeschichteter Edelstahl. Die matte Farbe sitzt nur außen.</p>
      <p>Der Griff geht ohne Schweißpunkt in den Korpus über. Da bleiben keine Milchreste hängen, und die Kanne ist schnell wieder sauber.</p>
    </div>
    <figure class="tb-bild">{bild("/assets/web/gebrauch-tasse-960.webp", "Milchkännchen LUN aus 1 mm Edelstahl in Schwarz matt (Onyx) neben einem Cappuccino mit Latte Art Herz")}</figure>
  </div>
</section>

<!-- 4 · Skala und Temperatur -->
<section class="tb gut durch" id="skala" aria-label="Skala und Temperatur">
  <div class="wrap tb-in">
    <div class="tb-text">
      <p class="eyebrow">Skala und Temperatur</p>
      <h2>Skala innen, Wärme am Korpus</h2>
      <p>Innen ist eine Skala in Milliliter und Unzen lasergraviert. So nimmst du jeden Morgen die gleiche Menge Milch, ohne zu schätzen. Weil sie im Stahl sitzt, hält sie auch in der Spülmaschine.</p>
      <p>Edelstahl leitet Wärme gut. Beim Aufschäumen fühlst du deshalb am Korpus, wie warm die Milch gerade ist. Mit etwas Übung bekommst du dafür schnell ein Gefühl. Der Griff bleibt dabei angenehm.</p>
      <p>Mit ihren 350 Millilitern reicht die aufgeschäumte Milch für zwei Flat White oder einen Cappuccino.</p>
    </div>
    <figure class="tb-bild">{bild("/assets/web/gebrauch-aufschaeumen-960.webp", "Milch aufschäumen im Milchkännchen LUN in Grün matt (Juniper) an der Dampflanze")}</figure>
  </div>
</section>

<!-- 5 · Vier Farben -->
<section class="kollektion gut durch" id="farben" aria-label="Vier Farben">
  <div class="wrap">
    <div class="kopf">
      <h2>Vier Farben</h2>
      <p>Drei matte Farben und gebürsteter Edelstahl. Alle vier dürfen in die Spülmaschine.</p>
    </div>
    <div class="farbreihe">
{karten}
    </div>
    <p class="preis-hinweis">Preise inkl. MwSt. bei Amazon, Stand {PREIS_STAND}.</p>
  </div>
</section>

<!-- 6 · Auf einen Blick -->
<section class="blick gut durch" id="auf-einen-blick" aria-label="Die LUN auf einen Blick">
  <div class="wrap">
    <p class="eyebrow">LUN 350</p>
    <h2>Die LUN auf einen Blick</h2>
    <dl class="daten">
      <div><dt>Inhalt</dt><dd>350 ml. Aufgeschäumt reicht das für zwei Flat White oder einen Cappuccino.</dd></div>
      <div><dt>Material</dt><dd>Edelstahl 304, die ganze Kanne einschließlich Griff.</dd></div>
      <div><dt>Wandstärke</dt><dd>1 mm.</dd></div>
      <div><dt>Oberfläche</dt><dd>Juniper, Linen und Onyx außen matt beschichtet, Steel gebürstet. Innen blanker Edelstahl.</dd></div>
      <div><dt>Skala</dt><dd>Innen, lasergraviert, in ml und oz.</dd></div>
      <div><dt>Maße</dt><dd>9,3&nbsp;cm hoch, Ø oben 6,4&nbsp;cm, Ø unten 7,5&nbsp;cm.</dd></div>
      <div><dt>Gewicht</dt><dd>198 g.</dd></div>
      <div><dt>Spülmaschine</dt><dd>Ja, alle vier Farben.</dd></div>
      <div><dt>Herd, Induktion, Mikrowelle</dt><dd>Nein.</dd></div>
      <div><dt>Lebensmittelkontakt</dt><dd><span class="offen">[OFFEN] Zeile „geprüft nach LFGB (Eurofins, Oktober 2026)“ erst nach Eintrag im Faktenblatt</span></dd></div>
    </dl>
    <p class="klein">Von Hand gemessen, kleine Abweichungen sind möglich. <a href="/assets/docs/MJOAR_LUN350_Sicherheitshinweise_GPSR.pdf">Sicherheitshinweise (PDF)</a></p>
  </div>
</section>

<!-- 7 · Pflege und Verpackung -->
<section class="tb gedreht gut durch" id="verpackung" aria-label="Pflege und Verpackung">
  <div class="wrap tb-in">
    <div class="tb-text">
      <p class="eyebrow">Pflege und Verpackung</p>
      <h2>Kunststofffrei verpackt</h2>
      <p>Die LUN darf in allen vier Farben in die Spülmaschine, wenn es schnell gehen muss. Von Hand mit einem weichen Schwamm gespült und kurz abgetrocknet, bleibt die Oberfläche am längsten ohne Wasserflecken. Bitte keine Scheuermittel und keine Stahlwolle.</p>
      <p>Sie kommt in einem Baumwollbeutel und einem Naturkarton, ganz ohne Plastik. Den Beutel kannst du danach weiter benutzen. So verpackt eignet sie sich auch gut als Geschenk.</p>
    </div>
    <figure class="tb-bild">{bild("/assets/web/verpackung-0307-960.webp", "Milchkännchen LUN in Grün matt im Baumwollbeutel neben dem Naturkarton")}</figure>
  </div>
</section>

<!-- 8 · Weiter zum Ratgeber -->
<section class="weiter gut durch" aria-label="Kleine Kaffeekunde">
  <div class="wrap weiter-in">
    <div>
      <p class="eyebrow">Kleine Kaffeekunde</p>
      <h2>Welches Milchkännchen für Latte Art?</h2>
      <p>Größe, Ausguss, Milchmenge und Temperatur. Und wie du Milch Schritt für Schritt aufschäumst.</p>
    </div>
    <a class="link" href="/de/milch-und-latte-art/">Weiterlesen</a>
  </div>
</section>
</main>

{FUSS}

<script>
// Bühne wie auf der Startseite: großes LUN mit Parallaxe, Farbwahl tauscht Bild, Name, Preis und Kauflink
const bu=document.getElementById('buehne'), rz=document.getElementById('riesig');
const ruhig=matchMedia('(prefers-reduced-motion: reduce)').matches;
if(!ruhig) addEventListener('scroll',()=>{{const r=bu.getBoundingClientRect(); const off=(r.top+r.height/2-innerHeight/2)*0.18; rz.style.transform='translate(-50%,calc(-50% + '+off.toFixed(1)+'px))';}},{{passive:true}});
const lb=document.getElementById('lun-bild'), knoepfe=document.querySelectorAll('.lun .farben button');
function farbe(b,sofort){{
  knoepfe.forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
  const tausch=()=>{{lb.src=b.dataset.bild; lb.alt=b.dataset.alt; lb.style.opacity=1;}};
  if(sofort) tausch(); else {{lb.style.opacity=0; setTimeout(tausch,220);}}
  document.getElementById('lun-name').textContent=b.dataset.n;
  document.getElementById('lun-preis').textContent=b.dataset.preis;
  document.getElementById('lun-kauf').href=b.dataset.kaufen;
}}
knoepfe.forEach(b=>b.addEventListener('click',()=>farbe(b)));
// Alte Anker der früheren Produktseite weiter bedienen: #juniper/#linen/#onyx/#steel wählen die Farbe,
// #im-detail/#daten/#box/#fragen/#kaufen springen in den passenden Abschnitt, #entstehung geht zu Über uns.
(function(){{
  const h=location.hash, alt={{"#im-detail":"#ausguss","#daten":"#auf-einen-blick","#box":"#verpackung","#fragen":"#auf-einen-blick","#kaufen":"#lun"}};
  if(h==="#entstehung"){{location.replace("/de/#uns");return;}}
  const b=document.querySelector('.lun .farben button[data-f="'+h.slice(1)+'"]');
  if(b){{farbe(b,true);return;}}
  if(alt[h]){{history.replaceState(null,"",alt[h]);const z=document.querySelector(alt[h]);if(z)z.scrollIntoView();}}
}})();
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------------------------------------------
# Ratgeber /de/milch-und-latte-art/

RAT_TITEL = "Welches Milchkännchen für Latte Art? | MJØÅR (MJOAR)"
RAT_BESCHR = ("Größe, Ausguss, Material, Milchmenge und Temperatur: worauf es beim Milchkännchen für Latte Art ankommt. "
              "Mit Anleitung zum Aufschäumen.")


def rat_jsonld():
    return {"@context": "https://schema.org", "@graph": [{
        "@type": "Article",
        "@id": f"{SITE}/de/milch-und-latte-art/#artikel",
        "headline": "Welches Milchkännchen für Latte Art?",
        "description": RAT_BESCHR,
        "inLanguage": "de",
        "mainEntityOfPage": f"{SITE}/de/milch-und-latte-art/",
        "image": [f"{SITE}/assets/web/gebrauch-giessen-960.webp", f"{SITE}/assets/web/detail-ausguss-960.webp"],
        "datePublished": "2026-11-20",
        "author": {"@type": "Organization", "@id": f"{SITE}/#org", "name": "MJØÅR", "alternateName": "MJOAR", "url": f"{SITE}/"},
        "publisher": {"@id": f"{SITE}/#org"},
        "about": {"@id": f"{SITE}/de/lun-350/#lun"},
    }]}


def rat_seite():
    return f"""{head(RAT_TITEL, RAT_BESCHR, "/de/milch-und-latte-art/", "article", "Die LUN in vier Farben", rat_jsonld())}
<body id="top" class="unterseite">

{SCHATTEN}

{kopf_fuer("/de/milch-und-latte-art/", "/en/")}

<main id="inhalt">
<!-- Kopf: Text mit Bild -->
<section class="tb ratkopf gut durch" aria-label="Einleitung">
  <div class="wrap tb-in">
    <div class="tb-text">
      <p class="eyebrow">Kleine Kaffeekunde</p>
      <h1>Welches Milchkännchen für Latte&nbsp;Art?</h1>
      <p>Für Latte Art brauchst du Milch mit sehr feinem Schaum und ein Kännchen, mit dem du sie genau eingießen kannst. Worauf es dabei ankommt, haben wir hier gesammelt: Größe, Ausguss, Material, Menge und Temperatur.</p>
      <p>Danach zeigen wir, wie wir die Milch aufschäumen.</p>
    </div>
    <figure class="tb-bild">{bild("/assets/web/gebrauch-giessen-960.webp", "Latte Art gießen mit dem Milchkännchen LUN in Schwarz matt (Onyx)", eager=True)}</figure>
  </div>
</section>

<section class="rat gut durch" aria-label="Ratgeber">
  <div class="wrap">
  <article class="rat-spalte">
    <section class="rat-block" id="groesse">
      <h2>Die Größe richtet sich nach deinen Tassen</h2>
      <p>Milch gewinnt beim Aufschäumen an Volumen. Ein Kännchen mit 350 ml reicht deshalb für zwei Flat White oder einen Cappuccino. Für ein bis zwei Tassen zu Hause ist das eine gute Größe.</p>
      <p>Machst du mehrere Getränke auf einmal, ist ein größeres Kännchen praktischer. Beim Test in einem Wiener Café war die LUN 350 dem Team für den Café-Alltag zu klein, dort wünschten sie sich 600 ml.</p>
      <p>Umgekehrt ist wenig Milch in einem großen Kännchen schwerer aufzuschäumen, weil die Dampflanze kaum unter die Oberfläche reicht. Die LUN gibt es heute mit 350 ml, größere Größen sind in Arbeit.</p>
    </section>
    <section class="rat-block" id="ausguss">
      <h2>Der Ausguss zeichnet das Muster</h2>
      <p>Ein schmaler, spitzer Ausguss zieht feine Linien, wie du sie für Tulpe und Rosetta brauchst. Ein breiter, runder Ausguss gibt mehr Milch auf einmal ab, damit gelingen große, runde Formen wie ein Herz leichter.</p>
      <p>Bei der LUN haben wir uns für einen Ausguss entschieden, der nicht zu breit ist. So kannst du den Milchstrahl genau führen, für Herz, Tulpe und Rosetta.</p>
    </section>
  </article>
  <div class="rat-bilder">
    <figure class="detail"><div class="bild">{bild("/assets/web/detail-ausguss-960.webp", "Ausguss für Latte Art am Milchkännchen LUN in Schwarz matt")}</div>
      <figcaption><strong>Ausguss</strong><span>Nicht zu breit, damit du den Milchstrahl genau führen kannst.</span></figcaption></figure>
    <figure class="detail"><div class="bild">{bild("/assets/web/detail-skala-784.webp", "Skala innen im Milchkännchen in ml und oz")}</div>
      <figcaption><strong>Skala innen</strong><span>In ml und oz graviert. Du siehst die Menge schon beim Einfüllen.</span></figcaption></figure>
  </div>
  <article class="rat-spalte">
    <section class="rat-block" id="material">
      <h2>Auf die Wandstärke achten</h2>
      <p>Milchkännchen aus Edelstahl leiten Wärme gut. Beim Aufschäumen fühlst du deshalb am Korpus, wie warm die Milch gerade ist.</p>
      <p>Dünne Bleche werden schneller warm. Dickeres Blech liegt angenehmer in der Hand und fühlt sich wertiger an. Die LUN ist aus einem ganzen Millimeter Edelstahl 304, einschließlich Griff. Das gibt ihr Stabilität: Sie ist robust und verformt sich nicht.</p>
      <p>Ob matt oder blank, ist Geschmackssache. Bei der LUN sitzt die matte Farbe nur außen, innen ist sie blanker Edelstahl.</p>
    </section>
    <section class="rat-block" id="menge">
      <h2>Die Milchmenge lieber messen</h2>
      <p>Füll das Kännchen nicht zu voll, denn die Milch braucht beim Aufschäumen nach oben Platz. Eine Skala innen hilft dir dabei: Du nimmst jeden Morgen die gleiche Menge und musst nicht schätzen. In der LUN ist sie in Milliliter und Unzen lasergraviert.</p>
      <p><span class="offen">[OFFEN] Richtwerte je Getränk (ml Milch für Flat White, Cappuccino, Latte) fehlen im Faktenblatt</span></p>
    </section>
    <section class="rat-block" id="temperatur">
      <h2>Die Temperatur fühlst du am Korpus</h2>
      <p>Nimm Milch direkt aus dem Kühlschrank. Je kälter sie ist, desto mehr Zeit hast du beim Aufschäumen, und desto feiner wird der Schaum.</p>
      <p>Leg beim Aufschäumen eine Hand an das Kännchen. Sobald es zu heiß zum Anfassen wird, ist die Milch fertig, und du drehst den Dampf ab. Der Griff der LUN bleibt dabei angenehm.</p>
      <p><span class="offen">[OFFEN] Richtwert in Grad (üblich genannt etwa 55 bis 65 °C) nur nach Freigabe</span></p>
    </section>
    <section class="rat-block" id="aufschaeumen">
      <h2>Milch aufschäumen, Schritt für Schritt</h2>
      <p>Für Latte Art brauchst du Milch mit sehr feinem Schaum. Sie glänzt, sieht fast aus wie flüssige Farbe und hat keine sichtbaren Blasen. So gehen wir dabei vor.</p>
      <ol>
        <li><strong>Kalt anfangen:</strong> Nimm Milch direkt aus dem Kühlschrank und füll das Kännchen nicht zu voll.</li>
        <li><strong>Luft einziehen:</strong> Halte die Dampflanze knapp unter die Oberfläche und dreh den Dampf auf. Jetzt kommt Luft in die Milch, und du hörst ein leises, gleichmäßiges Geräusch. Das dauert nur ein paar Sekunden. Wird es laut und spritzt die Milch, ist die Lanze zu weit oben.</li>
        <li><strong>Die Milch in Bewegung bringen:</strong> Schieb die Lanze danach etwas tiefer in die Milch und halte das Kännchen leicht schräg. Die Milch fängt an, sich im Kreis zu drehen. Baristas sagen dazu, die Milch rollt. Diese Bewegung verteilt den Schaum gleichmäßig und macht große Blasen klein. Sobald das Kännchen zu heiß zum Anfassen wird, drehst du den Dampf ab.</li>
        <li><strong>Klopfen und schwenken:</strong> Klopf das Kännchen einmal kurz auf die Arbeitsplatte, damit übrig gebliebene Blasen platzen. Danach schwenkst du die Milch ein paar Mal im Kreis, bis die Oberfläche gleichmäßig glänzt.</li>
        <li><strong>Eingießen:</strong> Gieß zuerst aus etwas Höhe in die Mitte der Tasse, damit sich Milch und Espresso verbinden. Wenn die Tasse etwa halb voll ist, gehst du mit dem Ausguss ganz nah an die Oberfläche. Jetzt bleibt die Milch oben, und das Muster entsteht. Zum Schluss hebst du das Kännchen etwas an und ziehst einmal durch das Muster.</li>
      </ol>
    </section>
  </article>
  <div class="rat-bilder">
    <figure class="detail"><div class="bild">{bild("/assets/web/gebrauch-aufschaeumen-960.webp", "Milch aufschäumen im Milchkännchen LUN in Grün matt an der Dampflanze")}</div>
      <figcaption><strong>Aufschäumen</strong><span>Am Korpus fühlst du, wie warm die Milch gerade ist.</span></figcaption></figure>
    <figure class="detail"><div class="bild">{bild("/assets/web/gebrauch-tasse-960.webp", "Latte Art Herz im Cappuccino neben dem Milchkännchen LUN in Schwarz matt")}</div>
      <figcaption><strong>Eingießen</strong><span>Nah an der Oberfläche bleibt die Milch oben, und das Muster entsteht.</span></figcaption></figure>
  </div>
  <article class="rat-spalte">
    <section class="rat-block" id="fehler">
      <h2>Wenn es noch nicht klappt</h2>
      <h3>Der Schaum hat große Blasen</h3>
      <p>Meist ist zu viel Luft in die Milch gekommen, oder die Lanze war zu lange an der Oberfläche. Schieb sie beim nächsten Mal etwas früher tiefer, damit sich die Milch dreht.</p>
      <h3>Die Milch geht in der Tasse unter</h3>
      <p>Dann ist der Ausguss beim Eingießen noch zu weit von der Oberfläche entfernt. Geh mit dem Kännchen näher an die Tasse heran.</p>
      <h3>Das Muster zerläuft</h3>
      <p>Die Milch war zu flüssig. Lass beim nächsten Mal etwas länger Luft hinein.</p>
    </section>
    <section class="rat-block" id="matcha">
      <h2>Auch für Matcha und Kakao</h2>
      <p>Für einen Matcha Latte rührst du Matcha mit wenig heißem Wasser glatt und gießt die aufgeschäumte Milch dazu. Mit Kakao geht es genauso.</p>
    </section>
  </article>
  </div>
</section>

<section class="weiter gut durch" aria-label="LUN 350">
  <div class="wrap weiter-in">
    <div>
      <p class="eyebrow">LUN 350 · Milchkännchen</p>
      <h2>Unser Milchkännchen für Latte Art</h2>
      <p>350 ml, ein Millimeter Edelstahl 304 und eine Skala innen. In drei matten Farben und gebürstetem Edelstahl.</p>
    </div>
    <a class="link" href="/de/lun-350/">Mehr zur LUN</a>
  </div>
</section>
</main>

{FUSS}
</body>
</html>
"""


def schreiben(pfad, inhalt):
    ziel = os.path.join(ROOT, pfad.strip("/").replace("/", os.sep), "index.html")
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    with open(ziel, "w", encoding="utf-8", newline="\n") as d:
        d.write(inhalt)
    print(os.path.relpath(ziel, ROOT))


if __name__ == "__main__":
    bilder_kopieren()
    schreiben("/de/lun-350/", lun_seite())
    schreiben("/de/milch-und-latte-art/", rat_seite())
