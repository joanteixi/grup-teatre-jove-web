"""Genera el pressupost 2027 en Excel (model amb hipòtesis i fórmules)."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

DESTI = "/home/nex/Documents/teatre/Pressupost_2027.xlsx"

FOSC = "14152A"
VI = "8B1E3F"
OR = "E0B34A"
CREMA = "FBF7EF"
GROC = "FDF3D0"
GRIS = "5C6076"

EUR = '#,##0.00\\ "€"'
EUR0 = '#,##0\\ "€"'

wb = Workbook()

titol = Font(name="Georgia", size=20, bold=True, color=FOSC)
subtitol = Font(name="Calibri", size=10, color=GRIS)
capçalera = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
seccio = Font(name="Calibri", size=12, bold=True, color=VI)
normal = Font(name="Calibri", size=10.5, color="1A1A1A")
negreta = Font(name="Calibri", size=10.5, bold=True, color="1A1A1A")
nota = Font(name="Calibri", size=9, italic=True, color=GRIS)

fons_cap = PatternFill("solid", fgColor=FOSC)
fons_vi = PatternFill("solid", fgColor=VI)
fons_or = PatternFill("solid", fgColor=OR)
fons_input = PatternFill("solid", fgColor=GROC)
fons_total = PatternFill("solid", fgColor="EFE9DC")

fi = Side(style="thin", color="D8D2C4")
marc = Border(left=fi, right=fi, top=fi, bottom=fi)


def capçalera_fila(ws, fila, valors, ample=True):
    for j, v in enumerate(valors, start=1):
        c = ws.cell(row=fila, column=j, value=v)
        c.font = capçalera
        c.fill = fons_cap
        c.alignment = Alignment(horizontal="left" if j == 1 else "right", vertical="center")
        c.border = marc
    ws.row_dimensions[fila].height = 22


# ============================================================ RESUM
ws = wb.active
ws.title = "Resum"
ws.sheet_view.showGridLines = False
ample = {"A": 44, "B": 16, "C": 9, "D": 52}
for k, v in ample.items():
    ws.column_dimensions[k].width = v

ws["A1"] = "PRESSUPOST 2027"
ws["A1"].font = titol
ws["A2"] = "Associació Grup de Teatre Jove de Vacarisses · cicle novembre de 2026 – octubre de 2027"
ws["A2"].font = subtitol
ws["A3"] = ("Esborrany per a l'Assemblea General del 7 de novembre de 2026. Les caselles en groc són "
            "hipòtesis: es poden canviar i la resta es recalcula.")
ws["A3"].font = nota

# --- ingressos
ws["A5"] = "INGRESSOS"
ws["A5"].font = seccio
capçalera_fila(ws, 6, ["Concepte", "Import", "% total", "Base de la previsió"])

ingressos = [
    ("Escola de Teatre 2027", "=Escola!$B$12", "2 grups: petits (dilluns) i mitjans (dissabtes), tots dos de musical"),
    ("Pastorets 2026", "=Obres!F6", "320 espectadors × 7 € de mitjana"),
    ("Lectura de Lorca (Sènior)", "=Obres!F7", "180 espectadors × 6 € (preu reduït)"),
    ("Enemic del poble", "=Obres!F8", "220 espectadors × 7 €"),
    ("Jocs Florals", "=Obres!F9", "240 espectadors × 7 €"),
    ("Somnis d'institut", "=Obres!F10", "400 espectadors × 7 €"),
    ("Engrunes 2027", "=Obres!F11", "Accés gratuït amb reserva"),
    ("Subvenció de l'Ajuntament", 3696, "Import sol·licitat per al 2026; es manté"),
    ("Subvenció sènior", 250, "Com al 2026"),
    ("Altres (bar, donacions, federació)", 300, "Estimació prudent"),
]
fila = 7
for nom, valor, base in ingressos:
    ws.cell(row=fila, column=1, value=nom).font = normal
    c = ws.cell(row=fila, column=2, value=valor)
    c.font = normal
    c.number_format = EUR
    c.alignment = Alignment(horizontal="right")
    if isinstance(valor, (int, float)):
        c.fill = fons_input
    ws.cell(row=fila, column=3, value=f"=IF($B$17=0,0,B{fila}/$B$17)").number_format = "0.0%"
    ws.cell(row=fila, column=3).alignment = Alignment(horizontal="right")
    ws.cell(row=fila, column=3).font = normal
    ws.cell(row=fila, column=4, value=base).font = nota
    for j in range(1, 5):
        ws.cell(row=fila, column=j).border = marc
    fila += 1

ws.cell(row=17, column=1, value="TOTAL INGRESSOS").font = negreta
ws.cell(row=17, column=2, value="=SUM(B7:B16)").number_format = EUR
ws.cell(row=17, column=3, value="=IF($B$17=0,0,1)").number_format = "0.0%"
for j in range(1, 5):
    ws.cell(row=17, column=j).fill = fons_total
    ws.cell(row=17, column=j).border = marc
    ws.cell(row=17, column=j).font = negreta
    ws.cell(row=17, column=j).alignment = Alignment(horizontal="left" if j == 1 else "right")

# --- despeses
ws["A19"] = "DESPESES"
ws["A19"].font = seccio
capçalera_fila(ws, 20, ["Concepte", "Import", "% total", "Base de la previsió"])

despeses = [
    ("Escola de Teatre 2027", "=-Escola!$E$18", "Professorat dels dos grups i direcció del Sènior"),
    ("Pastorets 2026", "=Obres!G6", "Referència 2026: 1.677,83 €"),
    ("Lectura de Lorca (Sènior)", "=Obres!G7", "Lectura dramatitzada: menys escenografia"),
    ("Enemic del poble", "=Obres!G8", "Referència 2026 (Pervertimento): 1.322,65 €"),
    ("Jocs Florals", "=Obres!G9", "Referència 2026 (Criatures): 2.425,53 €"),
    ("Somnis d'institut", "=Obres!G10", "Musical: música, vestuari i escenografia"),
    ("Engrunes 2027", "=Obres!G11", "Referència 2026: 238,58 €"),
    ("Costes administratius", -1530, "Gestoria, telèfon, domini, assegurança (2026: 1.487,36 €)"),
    ("Hisenda (models 111 i 190)", -850, "2026: 811,08 € en tres pagaments"),
    ("Formació interna", -300, "Monogràfics trimestrals"),
    ("Sortides de teatre", -2000, "Sortides de teatre de tot el grup, pendent de concretar"),
]
fila = 21
for nom, valor, base in despeses:
    ws.cell(row=fila, column=1, value=nom).font = normal
    c = ws.cell(row=fila, column=2, value=valor)
    c.font = normal
    c.number_format = EUR
    c.alignment = Alignment(horizontal="right")
    if isinstance(valor, (int, float)):
        c.fill = fons_input
    ws.cell(row=fila, column=3, value=f"=IF($B$33=0,0,B{fila}/$B$33)").number_format = "0.0%"
    ws.cell(row=fila, column=3).alignment = Alignment(horizontal="right")
    ws.cell(row=fila, column=3).font = normal
    ws.cell(row=fila, column=4, value=base).font = nota
    for j in range(1, 5):
        ws.cell(row=fila, column=j).border = marc
    fila += 1

# imprevistos
ws.cell(row=32, column=1, value="Imprevistos (5 %)").font = normal
ws.cell(row=32, column=2, value="=0.05*SUM(B21:B31)").number_format = EUR
ws.cell(row=32, column=2).alignment = Alignment(horizontal="right")
ws.cell(row=32, column=4, value="Cinquè per cent sobre el total de despeses").font = nota
for j in range(1, 5):
    ws.cell(row=32, column=j).border = marc

ws.cell(row=33, column=1, value="TOTAL DESPESES").font = negreta
ws.cell(row=33, column=2, value="=SUM(B21:B32)").number_format = EUR
ws.cell(row=33, column=3, value="=IF($B$33=0,0,1)").number_format = "0.0%"
for j in range(1, 5):
    ws.cell(row=33, column=j).fill = fons_total
    ws.cell(row=33, column=j).border = marc
    ws.cell(row=33, column=j).font = negreta
    ws.cell(row=33, column=j).alignment = Alignment(horizontal="left" if j == 1 else "right")

# --- resultat
ws.cell(row=35, column=1, value="RESULTAT DE L'EXERCICI").font = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
ws.cell(row=35, column=2, value="=B17+B33").number_format = EUR
ws.cell(row=35, column=2).font = Font(name="Calibri", size=12, bold=True, color=FOSC)
ws.cell(row=35, column=2).alignment = Alignment(horizontal="right")
ws.cell(row=35, column=4, value="Ingressos menys despeses ordinàries").font = nota
for j in range(1, 5):
    ws.cell(row=35, column=j).fill = fons_or
    ws.cell(row=35, column=j).border = marc

# --- inversions
ws["A38"] = "INVERSIONS 2027"
ws["A38"].font = seccio
capçalera_fila(ws, 39, ["Concepte", "Import", "", "Nota"])
ws.cell(row=40, column=1, value="Ordinador").font = normal
ws.cell(row=40, column=2, value=600).number_format = EUR
ws.cell(row=40, column=2).fill = fons_input
ws.cell(row=40, column=2).alignment = Alignment(horizontal="right")
ws.cell(row=40, column=4, value="Equip per a la gestió del grup").font = nota
ws.cell(row=41, column=1, value="Mobles per guardar el material").font = normal
ws.cell(row=41, column=2, value=1500).number_format = EUR
ws.cell(row=41, column=2).fill = fons_input
ws.cell(row=41, column=2).alignment = Alignment(horizontal="right")
ws.cell(row=41, column=4, value="Nou espai d'emmagatzematge").font = nota
ws.cell(row=42, column=1, value="TOTAL INVERSIONS").font = negreta
ws.cell(row=42, column=2, value="=SUM(B40:B41)").number_format = EUR
for r in (40, 41, 42):
    for j in range(1, 5):
        ws.cell(row=r, column=j).border = marc
    ws.cell(row=r, column=2).alignment = Alignment(horizontal="right")
for j in range(1, 5):
    ws.cell(row=42, column=j).fill = fons_total
ws.cell(row=42, column=1).font = negreta
ws.cell(row=42, column=2).font = negreta

# --- tresoreria
ws["A45"] = "TRESORERIA"
ws["A45"].font = seccio
files_tres = [
    ("Saldo a 1 de novembre de 2026", 6968.39, "Banc 6.087,17 € + caixa 880,40 €"),
    ("+ Resultat de l'exercici", "=B35", "Segons el quadre de dalt"),
    ("− Inversions", "=-B42", "Ordinador i mobles"),
]
fila = 46
for nom, valor, base in files_tres:
    ws.cell(row=fila, column=1, value=nom).font = normal
    c = ws.cell(row=fila, column=2, value=valor)
    c.number_format = EUR
    c.alignment = Alignment(horizontal="right")
    if isinstance(valor, float):
        c.fill = fons_input
    ws.cell(row=fila, column=4, value=base).font = nota
    for j in range(1, 5):
        ws.cell(row=fila, column=j).border = marc
    fila += 1
ws.cell(row=49, column=1, value="SALDO PREVIST A 31 D'OCTUBRE DE 2027").font = negreta
ws.cell(row=49, column=2, value="=SUM(B46:B48)").number_format = EUR
for j in range(1, 5):
    ws.cell(row=49, column=j).fill = fons_or
    ws.cell(row=49, column=j).border = marc
ws.cell(row=49, column=1).font = Font(name="Calibri", size=11, bold=True, color=FOSC)
ws.cell(row=49, column=2).font = Font(name="Calibri", size=12, bold=True, color=FOSC)
ws.cell(row=49, column=2).alignment = Alignment(horizontal="right")

# ============================================================ OBRES
ob = wb.create_sheet("Obres")
ob.sheet_view.showGridLines = False
for k, v in {"A": 30, "B": 30, "C": 10, "D": 13, "E": 13, "F": 14, "G": 14, "H": 14, "I": 16, "J": 16}.items():
    ob.column_dimensions[k].width = v
ob["A1"] = "OBRES PREVISTES 2027"
ob["A1"].font = titol
ob["A2"] = "Espectadors i despesa són hipòtesis (groc). Ingressos = espectadors × preu mitjà."
ob["A2"].font = nota
capçalera_fila(ob, 4, ["Obra", "Dates", "Funcions", "Espectadors", "Preu mitjà", "Ingressos", "Despesa", "Resultat", "2026: ingressos", "2026: despesa"])

obres = [
    ("Pastorets 2026", "26 i 27 de desembre de 2026", 2, 320, 7.00, 1750, 2183.00, 1677.83),
    ("Lectura de Lorca (Sènior)", "20 i 21 de febrer de 2027", 2, 180, 6.00, 1100, 1886.72, 3009.08),
    ("Enemic del poble", "3 i 4 d'abril de 2027", 2, 220, 7.00, 1700, 988.00, 1322.65),
    ("Jocs Florals", "5 i 6 de juny de 2027", 2, 240, 7.00, 1350, 2292.49, 2425.53),
    ("Somnis d'institut", "juny de 2027", 3, 400, 7.00, 3200, 0.00, 182.90),
    ("Engrunes 2027", "octubre de 2027", 1, 0, 0.00, 350, 0.00, 238.58),
]
fila = 6
for nom, dates, funcions, esp, preu, desp, ing26, desp26 in obres:
    ob.cell(row=fila, column=1, value=nom).font = normal
    ob.cell(row=fila, column=2, value=dates).font = nota
    ob.cell(row=fila, column=3, value=funcions).alignment = Alignment(horizontal="center")
    c = ob.cell(row=fila, column=4, value=esp)
    c.fill = fons_input
    c.alignment = Alignment(horizontal="center")
    c = ob.cell(row=fila, column=5, value=preu)
    c.fill = fons_input
    c.number_format = EUR
    ob.cell(row=fila, column=6, value=f"=D{fila}*E{fila}").number_format = EUR
    c = ob.cell(row=fila, column=7, value=-desp)
    c.fill = fons_input
    c.number_format = EUR
    ob.cell(row=fila, column=8, value=f"=F{fila}+G{fila}").number_format = EUR
    ob.cell(row=fila, column=9, value=ing26).number_format = EUR
    ob.cell(row=fila, column=10, value=-desp26).number_format = EUR
    for j in range(1, 11):
        ob.cell(row=fila, column=j).border = marc
        if j >= 6:
            ob.cell(row=fila, column=j).alignment = Alignment(horizontal="right")
    fila += 1

ob.cell(row=12, column=1, value="TOTAL").font = negreta
ob.cell(row=12, column=3, value="=SUM(C6:C11)").font = negreta
ob.cell(row=12, column=4, value="=SUM(D6:D11)").font = negreta
for col in ("F", "G", "H", "I", "J"):
    c = ob[f"{col}12"]
    c.value = f"=SUM({col}6:{col}11)"
    c.number_format = EUR
    c.font = negreta
    c.alignment = Alignment(horizontal="right")
for j in range(1, 11):
    ob.cell(row=12, column=j).fill = fons_total
    ob.cell(row=12, column=j).border = marc

ob.cell(row=14, column=1, value="Nota: la columna «2026» és la liquidació real per obras del cicle anterior, "
        "per comparar. La despesa del 2027 és una estimació.").font = nota

# ============================================================ ESCOLA
esc = wb.create_sheet("Escola")
esc.sheet_view.showGridLines = False
for k, v in {"A": 34, "B": 22, "C": 10, "D": 13, "E": 9, "F": 14}.items():
    esc.column_dimensions[k].width = v
esc["A1"] = "ESCOLA DE TEATRE 2027"
esc["A1"].font = titol
esc["A2"] = "Alumnes, quota i mesos són hipòtesis (groc). Ingressos = alumnes × quota × mesos."
esc["A2"].font = nota
capçalera_fila(esc, 4, ["Grup", "Dia i hora", "Alumnes", "Quota / mes", "Mesos", "Ingrés"])

grups = [
    ("Grup de petits (musical)", "dilluns", 6, 35, 7),
    ("Grup de mitjans (musical)", "dissabtes", 7, 75, 7),
]
fila = 5
for nom, quan, alumnes, quota, mesos in grups:
    esc.cell(row=fila, column=1, value=nom).font = normal
    esc.cell(row=fila, column=2, value=quan).font = nota
    for col, val in (("C", alumnes), ("D", quota), ("E", mesos)):
        c = esc[f"{col}{fila}"]
        c.value = val
        c.fill = fons_input
        c.alignment = Alignment(horizontal="center")
    esc.cell(row=fila, column=4).number_format = EUR
    esc.cell(row=fila, column=6, value=f"=C{fila}*D{fila}*E{fila}").number_format = EUR
    esc.cell(row=fila, column=6).alignment = Alignment(horizontal="right")
    for j in range(1, 7):
        esc.cell(row=fila, column=j).border = marc
    fila += 1

# total alumnes: fila 9 → la fila 12 és text; ajustem: grups ocupen 5-8
esc.cell(row=7, column=1, value="TOTAL").font = negreta
esc.cell(row=7, column=3, value="=SUM(C5:C6)").font = negreta
esc.cell(row=7, column=3).alignment = Alignment(horizontal="center")
esc.cell(row=7, column=6, value="=SUM(F5:F6)").number_format = EUR
esc.cell(row=7, column=6).font = negreta
esc.cell(row=7, column=6).alignment = Alignment(horizontal="right")
for j in range(1, 7):
    esc.cell(row=7, column=j).fill = fons_total
    esc.cell(row=7, column=j).border = marc

# ingressos escola a la fila 12 (referenciada des del Resum)
esc.cell(row=11, column=1, value="INGRESSOS DE L'ESCOLA").font = seccio
esc.cell(row=12, column=1, value="Total quotes del curs").font = normal
esc.cell(row=12, column=2, value="=F7").number_format = EUR
esc.cell(row=12, column=2).font = negreta
esc.cell(row=12, column=2).alignment = Alignment(horizontal="right")
for j in range(1, 4):
    esc.cell(row=12, column=j).border = marc

esc.cell(row=14, column=1, value="DESPESES").font = seccio
capçalera_fila(esc, 15, ["Concepte", "", "Cost / mes", "Mesos", "Total"])
files = [("Professorat (2 grups)", 630, 7), ("Direcció Escola Sènior", 45, 7)]
fila = 16
for nom, cost, mesos in files:
    esc.cell(row=fila, column=1, value=nom).font = normal
    c = esc.cell(row=fila, column=3, value=cost)
    c.fill = fons_input
    c.number_format = EUR
    c.alignment = Alignment(horizontal="right")
    c = esc.cell(row=fila, column=4, value=mesos)
    c.fill = fons_input
    c.alignment = Alignment(horizontal="center")
    esc.cell(row=fila, column=5, value=f"=C{fila}*D{fila}").number_format = EUR
    esc.cell(row=fila, column=5).alignment = Alignment(horizontal="right")
    for j in range(1, 6):
        esc.cell(row=fila, column=j).border = marc
    fila += 1
esc.cell(row=18, column=1, value="TOTAL DESPESES ESCOLA").font = negreta
esc.cell(row=18, column=5, value="=SUM(E16:E17)").number_format = EUR
esc.cell(row=18, column=5).font = negreta
esc.cell(row=18, column=5).alignment = Alignment(horizontal="right")
for j in range(1, 6):
    esc.cell(row=18, column=j).fill = fons_total
    esc.cell(row=18, column=j).border = marc

esc.cell(row=20, column=1, value="Resultat de l'escola").font = normal
esc.cell(row=20, column=2, value="=B12-E18").number_format = EUR
esc.cell(row=20, column=2).alignment = Alignment(horizontal="right")
esc.cell(row=20, column=2).font = negreta

# ============================================================ HIPÒTESIS
hip = wb.create_sheet("Hipòtesis")
hip.sheet_view.showGridLines = False
hip.column_dimensions["A"].width = 30
hip.column_dimensions["B"].width = 90
hip["A1"] = "HIPÒTESIS I FONTS"
hip["A1"].font = titol
hip["A2"] = "Tot el que no és un número pres de la comptabilitat del 2026 és una hipòtesi, i aquí està explicada."
hip["A2"].font = nota

files_hip = [
    ("Base de partida", "Liquidació del cicle 2025-2026: 17.745,51 € d'ingressos, 16.250,29 € de despeses i 1.483,22 € de resultat, amb 6.968,39 € de tresoreria a 6/11/2026."),
    ("Cicle", "De l'1 de novembre de 2026 al 31 d'octubre de 2027. Els Pastorets de desembre de 2026 ja compten en aquest pressupost."),
    ("Obres previstes", "Segons la memòria d'activitats: Enemic del poble (3-4 abril), lectura de Lorca amb el Sènior (20-21 febrer), Jocs Florals (5-6 juny), Somnis d'institut (juny) i Engrunes (octubre)."),
    ("Espectadors", "S'estimen a partir de les entrades reals del 2026: Pastorets 317, Criatures 357, Gente Bien 224, Pervertimento 131, Companyia 155."),
    ("Preu mitjà", "7 € per entrada, barreja de 8 € general i 6 € reduïda; 6 € a la lectura de Lorca pel perfil de públic."),
    ("Despesa de les obres", "Es parteix de la despesa real del 2026 de l'obra equivalent i s'hi aplica un 5-10 % per inflació i materials; el musical de Somnis s'estima més car per música i vestuari."),
    ("Escola", "Dos grups, tots dos de musical: petits els dilluns (6 alumnes, 35 €/mes) i mitjans els dissabtes (7 alumnes, 75 €/mes). Set mesos de curs."),
    ("Professorat", "630 €/mes pels dos grups, set mesos; el 2026 es pagaven 628,58 €/mes per dos grups (factura de PuceDuca), així que la xifra es manté."),
    ("Subvencions", "3.696 € de l'Ajuntament (import sol·licitat) i 250 € del Sènior. Si la subvenció surt més baixa, el resultat baixa en la mateixa quantia."),
    ("Inversions", "600 € d'ordinador i 1.500 € de mobles per al nou espai. No són despesa de l'exercici: van a tresoreria."),
    ("Imprevistos", "5 % sobre el total de despeses ordinàries."),
    ("Què no hi és", "No hi ha despeses de la Federació (160 €/any) ni de publicitat impresa; si es volen, s'afecten als costes administratius."),
]
fila = 4
for tema, text in files_hip:
    c = hip.cell(row=fila, column=1, value=tema)
    c.font = Font(name="Calibri", size=10.5, bold=True, color=VI)
    c.alignment = Alignment(vertical="top")
    c2 = hip.cell(row=fila, column=2, value=text)
    c2.font = normal
    c2.alignment = Alignment(wrap_text=True, vertical="top")
    hip.row_dimensions[fila].height = 44
    fila += 1

wb.save(DESTI)
print("fet:", DESTI)
