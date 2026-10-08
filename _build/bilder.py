# Bild-Export für mjoar.com v2 (Auftrag Website 07.10.2026). Liest die Originale aus dem Shooting Julia Schärdel
# (2026_10_02_*) und die Freisteller nur lesend, schreibt WebP nach assets/web/ (480/960/1600/2400, soweit die Quelle
# reicht). Ausschnitte für die Details wie A+ v4 (APlus_Build/v4/build_aplus4.py), Freisteller per Multiplizieren auf
# Creme #F4EFE6 (on_creme), keine weißen Kästen. Kein Text in Bildern.
#   python _build/bilder.py        (aus C:/dev/mjoar)
import json
import os

import numpy as np
from PIL import Image, ImageChops

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "web")
PB = r"C:/Users/ththomas/OneDrive/01_THOMAS_MERCANTILE_BUSINESS/01_Marke_MJOAR/02_Produkt_Milchkaennchen_350ml/Produktbilder/"
SHOOT = PB + "2026_10_02_{}.jpg"
FREI = PB + "Montage_Hauptbild_Box/logo/LUN350_{}_Hauptbild_Julia_2000_logo.png"
CREME = (0xF4, 0xEF, 0xE6)
BREITEN = [480, 960, 1600, 2400]
QUALI = 78


def quelle(name):
    return Image.open(SHOOT.format(name)).convert("RGB")


def crop_cover(img, w, h, cx=0.5, cy=0.5, zoom=1.0):
    """Wie build_aplus4.crop_cover, aber ohne Skalierung: Ausschnitt im Seitenverhältnis w:h um (cx, cy)."""
    W, H = img.size
    ar = w / h
    if W / H > ar:
        ch = H / zoom
        cw = ch * ar
    else:
        cw = W / zoom
        ch = cw / ar
    x0 = min(max(cx * W - cw / 2, 0), W - cw)
    y0 = min(max(cy * H - ch / 2, 0), H - ch)
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))


def on_creme(img):
    """Weißen Freisteller-Hintergrund per Multiplizieren in Creme überführen (Schatten bleiben)."""
    return ImageChops.multiply(img, Image.new("RGB", img.size, CREME))


def weiss_anheben(im, ab=244):
    """Nahezu weißen Studiohintergrund auf reines Weiß ziehen, damit er nach on_creme exakt die Seitenfarbe hat."""
    return im.point(lambda v: 255 if v >= ab else int(v * 255 / ab))


def freisteller(farbe):
    """Freisteller eng auf das Objekt, quadratisch auf Creme (wie A+ 04 Farben)."""
    im = weiss_anheben(Image.open(FREI.format(farbe)).convert("RGB"))
    g = np.asarray(im.convert("L"))
    ys, xs = np.where(g < 246)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    seite = int(max(x1 - x0, y1 - y0) * 1.3)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    box = (int(cx - seite / 2), int(cy - seite / 2), int(cx - seite / 2) + seite, int(cy - seite / 2) + seite)
    leer = Image.new("RGB", (seite, seite), (255, 255, 255))
    leer.paste(im.crop((max(box[0], 0), max(box[1], 0), min(box[2], im.width), min(box[3], im.height))),
               (max(-box[0], 0), max(-box[1], 0)))
    # Fable 07.10.: auf Weiß liefern, die Seite multipliziert per CSS (mix-blend-mode: multiply) auf Creme. Ein vorab
    # eingerechnetes Creme verschiebt sich beim WebP-Farbsubsampling um 1 bis 2 Stufen und zeichnet einen hellen Kasten.
    return leer


bilder = {}


def export(name, img):
    """Schreibt name-<breite>.webp für alle Breiten ≤ Quellbreite (mindestens eine), merkt Maße für das HTML."""
    os.makedirs(OUT, exist_ok=True)
    breiten = [b for b in BREITEN if b <= img.width] or [img.width]
    if img.width not in breiten and img.width < BREITEN[-1] and img.width > breiten[-1] * 1.15:
        breiten.append(img.width)
    for b in breiten:
        h = round(img.height * b / img.width)
        img.resize((b, h), Image.LANCZOS).save(os.path.join(OUT, f"{name}-{b}.webp"), "WEBP", quality=QUALI, method=6)
    bilder[name] = {"breiten": breiten, "w": img.width, "h": img.height}
    print(name, img.size, breiten)


# Hero 0420 1 an der Maschine (Thorsten 07.10.): Desktop 5:4, mobil 4:5 eigener Ausschnitt
h = quelle("MJOAR0420 1")
export("hero-d", crop_cover(h, 3, 2, cx=0.5, cy=0.52))
export("hero-m", crop_cover(h, 4, 5, cx=0.6, cy=0.5))

# Farben: Freisteller je Farbe auf Creme
for farbe in ["Juniper", "Linen", "Onyx", "Steel"]:
    export(f"farbe-{farbe.lower()}", freisteller(farbe))

# Details (Fable 08.10., Nachbesserung PR #4): kein eingerechnetes Creme mehr. Nahaufnahmen auf Weiß werden auf Weiß
# geliefert, die Seite multipliziert sie per CSS (mix-blend-mode) randlos ins Creme, wie die Farb-Freisteller.
# Ausguss und Skala: 0215 ist das einzige Nahfoto von Ausguss und Skala im Shooting, das Original hat nur 1284 px;
# die Ausschnitte bleiben deshalb unter 1600 px (kein Hochrechnen). Wand und Griff aus Originalen mit 1600 x 2000.
d = weiss_anheben(quelle("MJOAR0215"))
export("detail-ausguss", d.crop((0, 100, 680, 950)))
export("detail-skala", d.crop((500, 90, 1284, 1070)))
export("detail-wand", crop_cover(quelle("MJOAR0307"), 4, 5, cx=0.30, cy=0.523, zoom=3779 / 2000))
# Griff 0182 (Juniper, Freisteller auf Weiß): ganzer Griff mit beiden Ansätzen am Korpus, 1600 x 2000.
export("detail-griff", weiss_anheben(quelle("MJOAR0182")).crop((150, 380, 1750, 2380)))

# Größe 0021 1 (Hand), 4:5 wie A+ 06
export("groesse", crop_cover(quelle("Mjoar_0021 1"), 4, 5, cx=0.42, cy=0.45))

# Gebrauch 0428 1, 0455 1, 0026 2 (4:5, Mittelpunkte wie A+ 05)
export("gebrauch-aufschaeumen", crop_cover(quelle("MJOAR0428 1"), 4, 5, cx=0.52, cy=0.5))
export("gebrauch-giessen", crop_cover(quelle("MJOAR0455 1"), 4, 5, cx=0.47, cy=0.5))
export("gebrauch-tasse", crop_cover(quelle("Mjoar_0026 2"), 4, 5, cx=0.465, cy=0.5))

# Verpackung 0307, 0310, 0321, 0332 (1:1, etwas enger auf Karton und Beutel)
for nr in ["0307", "0310", "0321", "0332"]:
    export(f"verpackung-{nr}", crop_cover(quelle(f"MJOAR{nr}"), 1, 1, cx=0.5, cy=0.6, zoom=1.25))

# Über uns 0284 (Familie): Desktop 3:2, mobil 4:5
f = quelle("MJOAR0284")
export("familie-d", crop_cover(f, 3, 2, cx=0.55, cy=0.58))
export("familie-m", crop_cover(f, 4, 5, cx=0.5, cy=0.55))
# Hero Desktop (Fable 08.10., Nachbesserung PR #4): ganzes Original 1:1, keine Kanne angeschnitten. Ein 3:2- oder
# 4:5-Ausschnitt schneidet unten bzw. seitlich an (die Kannen reichen von x 0,12 bis 0,91 und y 0,12 bis 0,93).
export("familie-q", f)

# „Wer dahinter steht“ (Thorsten 07.10.): Hero ist jetzt 0284, hier deshalb 0239 (Steel auf Karton mit Beutel), keine Dopplung
w = quelle("MJOAR0239")
export("wer-d", crop_cover(w, 4, 3, cx=0.5, cy=0.55))
export("wer-m", crop_cover(w, 4, 5, cx=0.5, cy=0.55))

# Zeichnungen Jonah (Latte Art), vorhanden in assets/latte/ (nur gelesen)
for motiv in ["heart", "rosetta", "tulip", "swan"]:
    export(f"latte-{motiv}", Image.open(os.path.join(ROOT, "assets", "latte", f"{motiv}.jpg")).convert("RGB"))

# Teilen-Vorschau (Open Graph) 1200x630 aus 0284, JPEG (WebP wird nicht überall gelesen)
crop_cover(f, 1200, 630, cx=0.55, cy=0.58).resize((1200, 630), Image.LANCZOS).save(os.path.join(OUT, "og-familie.jpg"), quality=82)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bilder.json"), "w", encoding="utf-8") as datei:
    json.dump(bilder, datei, indent=1)
print("fertig:", len(bilder), "Motive")
