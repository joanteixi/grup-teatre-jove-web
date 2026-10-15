import { useEffect, useState } from "react";

type Enllac = { text: string; href: string };

/**
 * Menú de navegació per a mòbil. És l'únic component que necessita JavaScript,
 * i per això va aïllat: la resta de la web és HTML pur.
 */
export default function MobileNav({ items, rutaActual }: { items: Enllac[]; rutaActual: string }) {
  const [obert, setObert] = useState(false);

  // Tanca el menú quan canvia la ruta o amb la tecla Escape
  useEffect(() => {
    setObert(false);
  }, [rutaActual]);

  useEffect(() => {
    if (!obert) return;
    const tancar = (e: KeyboardEvent) => {
      if (e.key === "Escape") setObert(false);
    };
    document.addEventListener("keydown", tancar);
    return () => document.removeEventListener("keydown", tancar);
  }, [obert]);

  return (
    <div className="menu-mobil">
      <button
        type="button"
        className="menu-mobil__boto"
        aria-expanded={obert}
        aria-controls="menu-mobil-panell"
        onClick={() => setObert((v) => !v)}
      >
        <span aria-hidden="true">{obert ? "✕" : "☰"}</span>
        {obert ? "Tanca" : "Menú"}
      </button>

      {obert && (
        <div className="menu-mobil__panell" id="menu-mobil-panell">
          <nav aria-label="Navegació principal (mòbil)">
            <ul>
              {items.map((e) => (
                <li key={e.href}>
                  <a
                    href={e.href}
                    aria-current={rutaActual === e.href ? "page" : undefined}
                  >
                    {e.text}
                  </a>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      )}
    </div>
  );
}
