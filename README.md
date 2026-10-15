# Web corporativa — Grup de Teatre Jove de Vacarisses

Web estàtica (HTML de debò, generat amb [Astro](https://astro.build)) per al grup.
En català, pensada per ser trobada a Google i perquè els enllaços es vegin bé quan
es comparteixen per WhatsApp o xarxes.

- **No hi ha servidor ni base de dades.** La web són fitxers HTML, CSS i imatges.
- **No hi ha cookies ni rastrejadors.** No cal avís de cookies.
- **El formulari de contacte no desa res:** obre el correu de qui l'omple.
- React s'usa només en dos punts (menú de mòbil i formulari); la resta és HTML pur.

---

## 1. Posar-la en marxa a l'ordinador

Cal Node 22 o superior.

```bash
npm install      # només el primer cop
npm run dev      # servidor de proves a http://localhost:4321
```

Per veure com quedarà de veritat (el que es publicarà):

```bash
npm run build    # genera la carpeta dist/
npm run preview  # serveix dist/ per comprovar-ho
```

---

## 2. On es canvia cada cosa

| Vull canviar...                   | Fitxer                                                     |
| --------------------------------- | ---------------------------------------------------------- |
| Nom, eslògan, correu, xarxes, adreça | `src/data/site.ts`                                      |
| Les obres (títol, any, sinopsi, estat) | `src/data/obres.ts`                                   |
| L'agenda (funcions, assajos, activitats) | `src/data/agenda.ts`                                |
| Els grups de l'escola de teatre   | `src/pages/escola.astro`                                   |
| La junta (noms i càrrecs)         | `src/pages/qui-som.astro`                                  |
| Els colors i la tipografia        | `src/styles/global.css` (les variables del principi)       |
| La imatge de previsualització     | `scripts/genera-og.py` → `python3 scripts/genera-og.py`    |

Per afegir una obra o una activitat **no cal saber programar**: es copia un bloc
i se'n canvia el text. Cada fitxer té comentaris que ho expliquen.

Les pàgines són a `src/pages/`: `index.astro` (portada), `qui-som`, `obres`,
`escola`, `agenda`, `contacte`, `avis-legal` i `404`.

---

## 3. Què falta omplir abans de publicar

Al codi hi ha les marques `PLACEHOLDER`. Són aquestes:

- [ ] **Domini definitiu** a `astro.config.mjs` (ara és `https://www.grupteatrejove.cat`).
- [ ] **Noms i càrrecs de la junta** (`src/pages/qui-som.astro`).
- [ ] **Telèfon**, si el voleu publicar (`src/data/site.ts`).
- [ ] **Enllaços reals** d'Instagram i Facebook (`src/data/site.ts`).
- [ ] **Adreça de la seu**, si n'hi ha (`src/data/site.ts`).
- [ ] **Any de fundació** del grup (`src/data/site.ts`).
- [ ] **Dates reals** de l'agenda de 2026-2027 (`src/data/agenda.ts`).
- [ ] **Horaris i quotes** de l'escola de teatre (`src/pages/escola.astro`).
- [ ] **NIF i número de registre** d'associacions, a l'avís legal.
- [ ] **Avís legal i privacitat**: reviseu-lo amb qui porti la comptabilitat.
- [ ] `public/robots.txt`: poseu-hi el domini de debò al sitemap.
- [ ] Les obres: ara hi ha quatre exemples amb textos genèrics.

> Els textos són genèrics a posta. No hi ha cap dada del grup que no sigui
> comprovable: el correu `info@grupteatrejove.cat` i el nom de l'entitat són els
> reals; la resta són exemples perquè els veieu en context.

---

## 4. Publicar-ho a Azure

La manera més senzilla i la més barata per a una web com aquesta és
**Azure Static Web Apps** (pla gratuït: HTTPS, domini propi i desplegament
automàtic). Dues opcions:

### Opció A — amb GitHub (recomanada, un cop i prou)

1. Pugeu aquest projecte a un repositori de GitHub.
2. Al portal d'Azure: **Create resource → Static Web App**.
   - Source: **GitHub**, trieu el repositori i la branca `main`.
   - Build presets: **Custom**.
   - **App location**: `/` — **Output location**: `dist`.
3. Azure us proposarà d'afegir un secret al repositori amb el testimoni de
   desplegament. El fitxer `.github/workflows/azure-static-web-apps.yml` ja hi és:
   accepteu-ho i a partir d'aquí **cada canvi que pugeu a `main` es publica sol**.
4. A **Custom domains**, afegiu el domini del grup i seguiu les instruccions
   (normalment un registre CNAME a qui us gestioni el domini).

### Opció B — a mà, sense GitHub

```bash
npm run build
# Amb l'eina de línia de comandes d'Azure (swa):
npx @azure/static-web-apps-cli deploy dist \
  --deployment-token <EL_TOKEN_DE_DESPLECTAMENT> --env production
```

El token el trobareu al portal: *Static Web App → Manage deployment token*.
També podeu pujar la carpeta `dist/` amb qualsevol altre servei d'estàtics
d'Azure (Storage amb "Static website", per exemple).

El fitxer `staticwebapp.config.json` ja configura les capçaleres de seguretat i
la pàgina 404; **no cal tocar-lo** perquè funcioni.

---

## 5. Detalls tècnics

- `dist/` és el que es publica: HTML a `/qui-som/index.html`, etc.
- Astro genera una carpeta per pàgina; els enllaços interns acaben en `/`.
- Els estils surten d'un sol fitxer CSS minificat.
- Els dos components de React (`MobileNav`, `ContactForm`) s'hidraten només quan
  cal; la resta de la web funciona sense JavaScript.
- Si algun dia voleu un formulari que envie sol, es pot connectar a una funció
  d'Azure: l'únic fitxer a tocar és `src/components/ContactForm.tsx`.

## 6. Comprovacions fetes

- `npm run build`: 8 pàgines generades, sense errors.
- 167 enllaços interns revisats: cap de trencat.
- Capçaleres `og:` i `twitter:card` presents a totes les pàgines (per a les
  previsualitzacions en compartir).
- `public/og.png` generada a 1200×630.
