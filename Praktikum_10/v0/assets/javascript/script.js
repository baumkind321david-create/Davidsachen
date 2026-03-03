const getViewportWidth = () => window.innerWidth ||
 document.documentElement.clientWidth;

 console.log(`Die Viewport-Breite beträgt: ${getViewportWidth()} Pixel.`);
const screenWidth = screen.width;
if (getViewportWidth() < 0.3 * screenWidth) {
    alert(`Warnung: Die Viewport-Breite (${getViewportWidth()} Pixel) ist weniger als 30% der Bildschirmbreite (${screenWidth} Pixel).`);
}
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

// EpisodeAudio
const audio1 = new EpisodeAudio("ep1.mp3", "10MB", "mp3");
const audio2 = new EpisodeAudio("ep2.mp3", "12MB", "mp3");

// Episoden
const ep1 = new Episode("Folge 1", "Intro", 90 * 60 * 1000, "2025-01-10", audio1);
const ep2 = new Episode("Folge 2", "Thema A", 45 * 60 * 1000, "2025-01-15", audio2);

const ep3 = new Episode("Episode A", "Start", 60 * 60 * 1000, "2024-12-01", audio1);
const ep4 = new Episode("Episode B", "Deep Dive", 30 * 60 * 1000, "2024-12-05", audio2);

// Podcasts
const podcast1 = new Podcast(
    "Tech Talk",
    "Technik Podcast",
    "Max",
    "max@mail.de",
    "bild1.png",
    "feed1.xml",
    ["Tech"],
    "2025-01-20"
);

const podcast2 = new Podcast(
    "History Cast",
    "Geschichte Podcast",
    "Anna",
    "anna@mail.de",
    "bild2.png",
    "feed2.xml",
    ["History"],
    "2024-12-10"
);

// Episoden hinzufügen
podcast1.addEpisode(ep1);
podcast1.addEpisode(ep2);

podcast2.addEpisode(ep3);
podcast2.addEpisode(ep4);

// Podcasts sammeln
const podcasts = [podcast1, podcast2];

for (const podcast of podcasts) {
    console.log(podcast.liste + ":");

    for (const episode of podcast.episoden) {
        console.log(
            "  " +
            episode.titel +
            " (" +
            episode.getDauerInStundenUndMinuten() +
            ")"
        );
    }
}
