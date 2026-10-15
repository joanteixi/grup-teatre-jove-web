/**
 * Les obres del grup.
 * Afegir una obra = copiar un bloc i canviar les dades. Res més.
 * `estat` pot ser: "propera" | "en cartell" | "estrenada"
 */

export type Obra = {
  titol: string;
  any: string;
  autor: string;
  direccio: string;
  sinopsi: string;
  estat: "propera" | "en cartell" | "estrenada";
  imatge?: string;
};

export const obres: Obra[] = [
  {
    titol: "Els Pastorets",
    any: "2026",
    autor: "Text popular",
    direccio: "Direcció col·lectiva",
    sinopsi:
      "El clàssic de cada Nadal, amb els àngels, els dimonis i tot el poble a la platea. Una tradició que arrossega generacions i que cada any es renova.",
    estat: "propera",
  },
  {
    titol: "Gente bien",
    any: "2026",
    autor: "Text contemporani",
    direccio: "Grup de sènior",
    sinopsi:
      "Retrat d'una família que mira de mantenir les aparences mentre tot se li desmunta per dins. Comèdia amarga, amb el grup de sènior al capdavant.",
    estat: "estrenada",
  },
  {
    titol: "Engrunes: racons de Po(e)",
    any: "2026",
    autor: "Edgar Allan Poe (adaptació)",
    direccio: "Treball d'escenes curtes",
    sinopsi:
      "Sis relats de Poe convertits en sis escenes breus en sis espais diferents. El públic camina, i la por el segueix d'una sala a l'altra.",
    estat: "propera",
  },
  {
    titol: "La Companyia de la Fantasia",
    any: "2026",
    autor: "Creació pròpia",
    direccio: "Escola de teatre",
    sinopsi:
      "Un musical familiar amb cançons originals, projeccions i bestiari fantàstic. La gran cita de l'escola de teatre amb el públic de totes les edats.",
    estat: "estrenada",
  },
];
