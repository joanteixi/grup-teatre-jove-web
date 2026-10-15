import { useState } from "react";

/**
 * Formulari de contacte sense servidor.
 *
 * No hi ha backend: el botó obre el client de correu de qui escriu amb les dades
 * ja posades. És el més senzill i el més segur (ningú no ha de mantenir cap
 * servei ni cap base de dades de contactes).
 *
 * Si algun dia voleu un formulari "de veritat" que envie sol, es pot connectar
 * a un servei extern o a una funció d'Azure: el lloc on tocar-ho és aquest fitxer.
 */
export default function ContactForm({ email }: { email: string }) {
  const [assumpte, setAssumpte] = useState("Vull informació del grup");
  const [missatge, setMissatge] = useState("");
  const [nom, setNom] = useState("");

  const enviar = (e: React.FormEvent) => {
    e.preventDefault();
    const cos = `Nom: ${nom}\n\n${missatge}`;
    window.location.href = `mailto:${email}?subject=${encodeURIComponent(
      assumpte,
    )}&body=${encodeURIComponent(cos)}`;
  };

  return (
    <form className="formulari" onSubmit={enviar}>
      <p>
        <label htmlFor="nom">El teu nom</label>
        <input
          id="nom"
          name="nom"
          type="text"
          required
          value={nom}
          onChange={(e) => setNom(e.target.value)}
        />
      </p>

      <p>
        <label htmlFor="assumpte">Assumpte</label>
        <select
          id="assumpte"
          name="assumpte"
          value={assumpte}
          onChange={(e) => setAssumpte(e.target.value)}
        >
          <option>Vull informació del grup</option>
          <option>Vull apuntar-me a l'escola de teatre</option>
          <option>Vull fer-me soci/a</option>
          <option>Us vull contractar una funció</option>
          <option>Premsa i comunicació</option>
          <option>Altres</option>
        </select>
      </p>

      <p>
        <label htmlFor="missatge">Missatge</label>
        <textarea
          id="missatge"
          name="missatge"
          rows={6}
          required
          value={missatge}
          onChange={(e) => setMissatge(e.target.value)}
        />
      </p>

      <button type="submit" className="btn btn--vi">
        Obre el correu i envia
      </button>
      <p className="formulari__nota">
        El botó obre el teu programa de correu amb el missatge a punt d'enviar.
        No guardem cap dada en aquesta web.
      </p>
    </form>
  );
}
