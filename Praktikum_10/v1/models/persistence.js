const parser = require("./podcastParser");

function EpisodeAudio(url, groesse, typ)
{
    this.url = url;
    this.groesse = groesse;
    this.typ = typ;
}
function Episode(titel, beschreibung, dauer, datum, episodeAudio)
{
    this.titel = titel,
    this.beschreibung = beschreibung,
    this.dauer= dauer,
    this.datum = new Date(datum)
    this.EpisodeAudio = episodeAudio;
    this.getDauerInStundenUndMinuten = function(){
        let zwischenergebnis = this.dauer / 1000 / 60;
        let kopie = Math.floor(zwischenergebnis)
        let stunden = 0;
        while (kopie >= 60)
        {
            kopie = kopie - 60;
            stunden = stunden + 1;
        }
        let minuten = kopie;
        let ergebnis = stunden.toString() + "h" + " " + minuten.toString()+ "min";
        return ergebnis;
    }

}
function Podcast(liste, beschreibung, autor, besitzerEmail, bildUrl, feedUrl, kategorien, letztesUpdate)
{
    this.liste= liste,
    this.beschreibung= beschreibung,
    this.autor= autor,
    this.besitzerEmail=besitzerEmail,
    this.bildUrl = bildUrl,
    this.feedUrl = feedUrl,
    this.kategorien = kategorien,
    this.letztesUpdate = new Date(letztesUpdate)
    this.episoden = [];
    this.addEpisode = function(Episode){
        this.episoden.push(Episode)
        this.episoden.sort((a,b)=> b.datum - a.datum)
    }
}

const podcasts = [];

/**
 * Subscribes to a podcast by importing the data from the given feed URL.
 * The import itself is asynchronous, so a callback function is needed for subsequent actions.
 *
 * @param {String} url The feed URL of the podcast to subscribe to.
 * @param {Function} callback Callback function to be called after the import is complete.
 */
function subscribe(url, callback) {
  parser.parseFeed(url, (feed) => {
    podcasts.push(convert(url, feed));
    if (callback) callback();
  });
}

/**
 * Converts the feed data imported from a URL into data objects (Podcast, Episode, EpisodeAudio)
 * suitable for this web application.
 *
 * @param {String} url The feed URL of the podcast from which it was imported.
 * @param {Object} feed Feed object according to https://www.npmjs.com/package/podcast-feed-parser#default
 */
function convert(url, feed) {
  
  // Podcast aus Meta-Daten erzeugen
  const podcast = new Podcast(
    feed.meta.title,
    feed.meta.description,
    feed.meta.author,
    feed.meta.owner.email,
    feed.meta.imageURL,
    url,
    feed.meta.categories,
    feed.meta.lastUpdated
  );

  // Episoden durchlaufen
  const episodes1 = feed.episodes;
  episodes1.forEach(ep => {
    const audio = new EpisodeAudio(
      ep.enclosure.url,
      ep.enclosure.length,
      ep.enclosure.type
    );

    const episode = new Episode(
      ep.title,
      ep.description,
      ep.duration,
      ep.pubDate,
      audio
    );

    podcast.addEpisode(episode);
  });

  return podcast;
}

module.exports = {
  podcasts,
  subscribe
};
