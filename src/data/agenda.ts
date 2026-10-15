/**
 * Agenda: funcions, assajos oberts i activitats.
 * Les dates i els llocs surten del calendari del grup: no els endevinis mai.
 * Format de data: "AAAA-MM-DD" i hora "HH:MM". Mantingues les entrades ordenades per data.
 */

export type Activitat = {
  data: string;
  hora: string;
  titol: string;
  lloc: string;
  descripcio: string;
  tipus: "funció" | "assaig obert" | "activitat" | "assemblea";
  entrades?: string;
};

export const agenda: Activitat[] = [
  {
    data: "2026-10-30",
    hora: "22:00",
    titol: "Engrunes de Poe",
    lloc: "Biblioteca el Castell",
    descripcio:
      "Què s'amaga entre les prestatgeries quan s'apaguen els llums de la biblioteca? El silenci que coneixes de dia es transforma en un escenari on les ombres cobren vida. Una nit única i irrepetible: un recorregut immersiu de sis lectures dramatitzades d'Edgar Allan Poe, sis històries esgarrifoses i sis veus en la foscor. T'atreveixes a creuar la porta quan la biblioteca tanca? Recomanat a partir de 12 anys (1r d'ESO).",
    tipus: "activitat",
    entrades: "Entrada lliure",
  },
  {
    data: "2026-12-26",
    hora: "20:00",
    titol: "Els Pastorets",
    lloc: "Casal de Cultura",
    descripcio:
      "Primera funció dels Pastorets, a la sala Antolina Boada i Ferrer. Entrades a taquilla i en línia.",
    tipus: "funció",
    entrades: "8 € · 6 € per a menors de 8 anys i sòcies",
  },
  {
    data: "2026-12-27",
    hora: "19:00",
    titol: "Els Pastorets",
    lloc: "Casal de Cultura",
    descripcio: "Segona funció dels Pastorets, a la sala Antolina Boada i Ferrer.",
    tipus: "funció",
    entrades: "8 € · 6 € per a menors de 8 anys i sòcies",
  },
  {
    data: "2027-02-21",
    hora: "19:00",
    titol: "Lectura dramatitzada: Lorca i altres poetes",
    lloc: "Biblioteca",
    descripcio:
      "Lectura dramatitzada a càrrec del grup de sènior. Entrada lliure fins a completar aforament.",
    tipus: "activitat",
  },
  {
    data: "2027-04-03",
    hora: "21:00",
    titol: "Un enemic del poble",
    lloc: "Casal de Cultura",
    descripcio: "Estrena de la nova producció del grup.",
    tipus: "funció",
  },
];
