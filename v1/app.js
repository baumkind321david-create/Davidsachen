const express = require("express");
const app = express();
const port = 8020;


//importieren von persistence in app.js
const persistence= require("./models/persistence");

// Body-Parser für POST-Daten (für Subscribe)
app.use(express.urlencoded({ extended: true }));

// EJS konfigurieren
app.set("view engine", "ejs");
app.set("views", "./views");

// Statische Dateien aus public
app.use(express.static("public"));




// Router anbinden
const router = require("./routes/routes");
app.use(router);

// 404-Fehlerseite (muss nach allen anderen Routes kommen!)
app.use((req, res) => {
  res.status(404).render("error", { 
    title: "Seite nicht gefunden",
    message: "Die angeforderte Seite existiert nicht."
  });
});

app.listen(port, function() {
  console.log(`Anwendung läuft auf http://localhost:${port}`);
});

