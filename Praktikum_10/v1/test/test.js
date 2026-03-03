const http = require("http");
const db = require("../models/persistence"); // Pfad ggf. anpassen

/* =========================
   Testdaten importieren
========================= */



// Einen Podcast abonnieren
// Importiert nacheinander die Feeds der Podcasts
// "Syntax" und "Working Draft"
db.subscribe("https://feeds.megaphone.fm/FSI1483080183", () => {
 db.subscribe("https://workingdraft.de/feed/", () => {
 console.log("Podcasts importiert.");
 });
})



/* =========================
   HTML-Erzeugung
========================= */

function generateHTML() {
  return `
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <title>Podcast Test Server</title>
</head>
<body>
  <h1>Importierte Podcasts</h1>

  ${db.podcasts.map(podcast => `
    <section>
      <h2>${podcast.liste}</h2>
      <p>${podcast.beschreibung}</p>

      ${podcast.bildUrl ? `<img src="${podcast.bildUrl}" width="200">` : ""}

      <h3>Episoden</h3>
      <ul>
        ${podcast.episoden.map(ep => `
          <li>${ep.titel}</li>
        `).join("")} 
      </ul>
      <hr>
    </section>
  `).join("")}

</body>
</html>
`;
/*join wegen der Liste Kommaweg*/
}

/* =========================
   Web-Server
========================= */

const server = http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
  res.end(generateHTML());
});

server.listen(8844, () => {
  console.log("Test-Server läuft unter http://localhost:8844");
});
