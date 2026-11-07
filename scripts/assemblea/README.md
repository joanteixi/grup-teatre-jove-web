# Presentació de l'assemblea (codi)

Aquí hi ha el codi que genera la presentació de l'assemblea del 2026. **No es
publica a la web**: la pàgina `/assemblea/` es va esborrar el 7 de novembre de
2026, un cop passada l'assemblea. El codi es queda per si es torna a necessitar.

## Fitxers

- `fes_presentacio.py` — genera la presentació (18 diapositives) a partir de
  `fitxa.json`. Escriu l'HTML i el PDF a `~/Documents/teatre/`.
- `fes_pressupost.py` — genera el pressupost 2027 (el bo és el Google Sheet de
  la carpeta Comptabilitat del Drive).
- `fitxa.json` — les xifres del cicle (comptes, obres, entrades, opinions).

## Com es torna a publicar

```bash
python3 scripts/assemblea/fes_presentacio.py
cp ~/Documents/teatre/Assemblea_2026_presentacio.html public/assemblea/index.html
# afegir-hi <meta name="robots" content="noindex, nofollow, noarchive">
./publica.sh "Assemblea: pagina interna temporal"
```

Quan s'acabi, esborrar `public/assemblea/` i tornar a publicar.

## Coses a recordar

- La lletra és gran i el fons blanc a posta: es projecta en una sala.
- Si s'hi afegeix contingut, comprovar que cap diapositiva desborda (alçada i
  amplada) abans de publicar.
- Les 2.000 € són **sortides de teatre**, i 1.000 € de la subvenció municipal
  van a compte del Teatre Sènior.
