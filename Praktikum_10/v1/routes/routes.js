const express = require("express");
// [TODO]
// Include other required modules
const router = express.Router();

const persistence = require("../models/persistence");

router.get("/", function (req, res) {
  // [TODO]
  // Implement: Display list of subscribed podcasts
  // res.send("./assets/index.html", (req, res, next))
  const podcasts = persistence.podcasts;
  res.render("index", { 
    title: "Meine Podcasts", 
    podcasts: podcasts 
  });
 
});

router.get("/podcast", function (req, res) {
  // [TODO]
  // Implement: Show detail page for the podcast with the given
  // index (index is provided as a request/query parameter,
  // access with: req.query.pc)
  const pcIndex= parseInt(req.query.pc, 10);
  const podcasts = persistence.podcasts;

  if(isNaN(pcIndex) || pcIndex<0 || pcIndex >= podcasts.length){
    return res.status(404).render("error", {
      title:"Fehler", 
      messege: " Podcast nicht gefunden"});

  }
  const podcast = podcasts[pcIndex];
  res.render("podcast", { 
    title: podcast.liste, 
    podcast:podcast, 
    pcIndex: pcIndex});
  
});

router.get("/episode", function (req, res) {
  // [TODO]
  // Implement: Show detail page for the episode (indices
  // are provided as request/query parameters, access with:
  // req.query.pc and req.query.ep)
  const pcIndex= parseInt(req.query.pc, 10);
  const epIndex= parseInt(req.query.ep, 10);
  const podcasts=persistence.podcasts;

    if (
    isNaN(pcIndex) || pcIndex < 0 || pcIndex >= podcasts.length ||
    isNaN(epIndex) || epIndex < 0 || epIndex >= podcasts[pcIndex].episoden.length
  ) {
    return res.status(404).render("error", { 
      title: "Fehler", 
      message: "Episode nicht gefunden." });
  }

  const podcast = podcasts[pcIndex];
  const episode = podcast.episoden[epIndex];
  res.render("episode", { 
    title: episode.titel, 
    podcast: podcast, 
    episode:episode, 
    pcIndex:pcIndex, 
    epIndex:epIndex });

});

router.post("/subscribe", function (req, res) {
  // [TODO]
  // Implement: Subscribe to a podcast
  const feedUrl = req.body.feedUrl?.trim();
  if (!feedUrl) {
    return res.status(400).render("error", { 
      title: "Fehler", 
      message: "Keine Feed-URL angegeben." });
  }

  persistence.subscribe(feedUrl, (err) => {
    if (err) {
      console.error('Fehler beim Abonnieren:', err);
      return res.status(500).render('error', {
        title: 'Fehler',
        message: 'Podcast konnte nicht abonniert werden.'
      });
    }
    res.redirect("/"); // Nach Abonnieren zurück zur Liste
  });
});

module.exports = router;
