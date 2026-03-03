// index.js
const btn = document.getElementById("listenansicht");

// Array mit allen li-IDs + Bildinfos
const items = [
  {
    id: "erste",
    img: "./assets/img/morning.png",
    alt: "Morning Briefing Logo",
  },
  { id: "zweite", img: "./assets/img/logo-byte.webp", alt: "Byte Logo" },
  {
    id: "dritte",
    img: "./assets/img/logo-quark-daily.webp",
    alt: "Quark Daily Logo",
  },
  {
    id: "vierte",
    img: "./assets/img/logo-sternstunde-philosophie.webp",
    alt: "Sternstunde Philosophie Logo",
  },
  {
    id: "fünfte",
    img: "./assets/img/logo-passwort.webp",
    alt: "Passwort Logo",
  },
];

// Speichere Original-Links beim Start
items.forEach((item) => {
  const li = document.getElementById(item.id);
  if (!li) return;

  const link = li.querySelector("a");
  if (!link) return;

  // Titel extrahieren
  item.title = link.textContent.trim();
  // Kopiere das Original-Link-Element
  item.originalLink = link.cloneNode(true);
});

function zeigeListenansicht() {
  items.forEach((item) => {
    const li = document.getElementById(item.id);
    if (!li) return;

    // Alle Kinder entfernen (ohne innerHTML)
    while (li.firstChild) {
      li.removeChild(li.firstChild);
    }

    // Original-Link zurückfügen
    li.appendChild(item.originalLink.cloneNode(true));
  });

  btn.textContent = "Zur Kachelansicht";
  isTileView = false;
}

function zeigeKachelansicht() {
  items.forEach((item) => {
    const li = document.getElementById(item.id);
    if (!li) return;

    // Alle Kinder entfernen
    while (li.firstChild) {
      li.removeChild(li.firstChild);
    }

    // Neues <a> erstellen
    const a = document.createElement("a");
    a.href = "#";

    // <figure> erstellen
    const figure = document.createElement("figure");

    // <img> erstellen
    const img = document.createElement("img");
    img.src = item.img;
    img.alt = item.alt;
    img.width = 150;
    img.height = 150;

    // <figcaption> erstellen
    const figcaption = document.createElement("figcaption");
    figcaption.textContent = item.title;

    // Alles zusammenbauen
    figure.appendChild(img);
    figure.appendChild(figcaption);
    a.appendChild(figure);

    // In das <li> einfügen
    li.appendChild(a);
  });

  btn.textContent = "Zur Listenansicht";
  isTileView = true;
}

btn.addEventListener("click", () => {
  if (isTileView) {
    zeigeListenansicht();
  } else {
    zeigeKachelansicht();
  }
});
// Startzustand: Listenansicht
zeigeListenansicht();
