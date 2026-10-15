#!/usr/bin/env python3
"""Genera la imatge de previsualització (public/og.png, 1200x630).

És la imatge que surt quan algú comparteix l'enllaç de la web per WhatsApp,
Instagram o xarxes socials. Si canvieu el nom o l'eslògan, torneu a executar:

    python3 scripts/genera-og.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

AMPLADA, ALCADA = 1200, 630
FOSC = (20, 21, 42)
VI = (139, 30, 63)
OR = (224, 179, 74)
BLANC = (255, 255, 255)
GRIS = (215, 219, 235)

ARREL = Path(__file__).resolve().parent.parent
EIXIDA = ARREL / "public" / "og.png"

CANDIDATS_TIPUS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/TTF/DejaVuSerif-Bold.ttf",
]
CANDIDATS_COS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def tipus(candidats, mida):
    for cami in candidats:
        if Path(cami).exists():
            return ImageFont.truetype(cami, mida)
    return ImageFont.load_default()


img = Image.new("RGB", (AMPLADA, ALCADA), FOSC)
d = ImageDraw.Draw(img)

# Franges verticals subtils, com un teló
for x in range(0, AMPLADA, 34):
    d.rectangle([x, 0, x + 2, ALCADA], fill=(30, 32, 56))

# Franja de color de fons
d.rectangle([0, 0, AMPLADA, 14], fill=VI)

# Cercle amb les sigles
d.ellipse([70, 90, 190, 210], fill=VI)
f_sigles = tipus(CANDIDATS_TIPUS, 46)
d.text((130, 150), "TJ", font=f_sigles, fill=OR, anchor="mm")

# Text
f_titol = tipus(CANDIDATS_TIPUS, 62)
f_sub = tipus(CANDIDATS_COS, 30)
f_peu = tipus(CANDIDATS_COS, 26)

d.text((70, 300), "Grup de Teatre Jove", font=f_titol, fill=BLANC)
d.text((70, 380), "de Vacarisses", font=f_titol, fill=BLANC)
d.text((72, 480), "Teatre fet al poble, per a tothom", font=f_sub, fill=OR)

d.rectangle([70, 550, 76, 596], fill=VI)
d.text((100, 556), "Obres  ·  Escola de teatre  ·  Agenda  ·  Contacte", font=f_peu, fill=GRIS)

img.save(EIXIDA, "PNG", optimize=True)
print(f"Fet: {EIXIDA} ({EIXIDA.stat().st_size / 1024:.0f} KB)")
