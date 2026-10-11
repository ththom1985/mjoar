# Retusche zweier Detailfotos (Thorsten 11.10.2026): liest Julias Originale nur, schreibt nach Produktbilder/Retusche/.
# MJOAR0182 (Griff Juniper): dunkle Schattenfugen an beiden Griffansätzen per Inpainting angeglichen, Hintergrund und
#   Schatten unter dem Griff bleiben (Weiß wird aus der Maske ausgenommen).
# MJOAR0215 (Ausguss/Skala): Kante geglättet: entlang der starken Konturen Rauschen und helle Pünktchen per NLM entfernt,
#   Bürststruktur der Flächen bleibt.
import os
import cv2
import numpy as np

PB = r"C:/Users/ththomas/OneDrive/01_THOMAS_MERCANTILE_BUSINESS/01_Marke_MJOAR/02_Produkt_Milchkaennchen_350ml/Produktbilder/"
ORIG = PB + "2026_10_02_{}.jpg"
ZIEL = PB + "Retusche/2026_10_02_{}_retusche.png"


def fugen(img, rois, thr=20, rad=4):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    weiss = cv2.dilate(((gray > 215) & (hsv[..., 1] < 30)).astype(np.uint8), np.ones((7, 7), np.uint8))
    mask = np.zeros(gray.shape, np.uint8)
    for x0, y0, x1, y1 in rois:
        g = gray[y0:y1, x0:x1].astype(np.int16)
        med = cv2.medianBlur(gray[y0:y1, x0:x1], 31).astype(np.int16)
        m = (((med - g) > thr) & (weiss[y0:y1, x0:x1] == 0)).astype(np.uint8) * 255
        mask[y0:y1, x0:x1] = cv2.dilate(m, np.ones((5, 5), np.uint8))
    mask[weiss > 0] = 0
    return cv2.inpaint(img, mask, rad, cv2.INPAINT_TELEA)


def kante(img, roi):
    x0, y0, x1, y1 = roi
    out = img.copy()
    sub = out[y0:y1, x0:x1].copy()
    gray = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
    band = cv2.dilate(cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 70, 170), np.ones((7, 7), np.uint8))
    den = cv2.medianBlur(cv2.fastNlMeansDenoisingColored(sub, None, 9, 9, 7, 21), 3)
    w = cv2.GaussianBlur(band.astype(np.float32) / 255, (11, 11), 0)[..., None]
    out[y0:y1, x0:x1] = (den * w + sub * (1 - w)).astype(np.uint8)
    return out


if __name__ == "__main__":
    os.makedirs(PB + "Retusche", exist_ok=True)
    cv2.imwrite(ZIEL.format("MJOAR0182"), fugen(cv2.imread(ORIG.format("MJOAR0182")), [(895, 890, 965, 965), (865, 1945, 935, 2065)]))
    cv2.imwrite(ZIEL.format("MJOAR0215"), kante(cv2.imread(ORIG.format("MJOAR0215")), (120, 150, 1284, 560)))
    print("Retusche geschrieben:", PB + "Retusche/")
