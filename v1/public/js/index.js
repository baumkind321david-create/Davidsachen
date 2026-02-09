
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("listenansicht");
  const kachelListe = document.getElementById("abos-kachel");
  const listenListe = document.getElementById("abos-liste");

  let isTileView = true; // Startet mit Kachelansicht

  function toggleView() {
    if (isTileView) {
      // Zu Listenansicht wechseln
      kachelListe.style.display = "none";
      listenListe.style.display = "block";
      btn.textContent = "Kachelansicht";
    } else {
      // Zurück zu Kachelansicht
      kachelListe.style.display = "grid"; // oder "flex", je nach deinem CSS
      listenListe.style.display = "none";
      btn.textContent = "Listenansicht";
    }
    isTileView = !isTileView;
  }

  btn.addEventListener("click", toggleView);
});