package fachlogik;

import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;

import datenhaltung.PersistenzException;
import datenhaltung.RisikoDerialiserung;

public class Risikoverwaltung implements Iterable<Risiko1> {

    private List<Risiko1> liste = new ArrayList<>();
    private RisikoDerialiserung dao;

    public Risikoverwaltung() {}
    public Risikoverwaltung(RisikoDerialiserung dao) { this.dao = dao; }
    public void setRisikoDerialiserung(RisikoDerialiserung dao) { this.dao = dao; }

    public void aufnehmen(Risiko1 risiko) { liste.add(risiko); }
    public void entfernen(Risiko1 r) { liste.remove(r); }
    public List<Risiko1> getRisikenListe() { return liste; }

    public void zeigeRisiken() {
        Collections.sort(liste);
        for(Risiko1 r : liste) r.druckeDaten();
    }

    public Risiko1 sucheRisikoMitMaxRueckstellung() {
        if(liste.isEmpty()) return null;
        Risiko1 max = liste.get(0);
        for(Risiko1 r : liste) if(r.ermittleRueckstellung() >= max.ermittleRueckstellung()) max = r;
        return max;
    }

    public double neuberechneSummeRueckstellungen() {
        return liste.stream()
                    .mapToDouble(Risiko1::ermittleRueckstellung)
                    .sum();
    }

    public void druckeRisiken(OutputStream out) {
        Collections.sort(liste);
        for(Risiko1 r : liste) r.druckeDaten(out);
    }

    @Override
    public Iterator<Risiko1> iterator() { return liste.iterator(); }

    public void speichernin() throws PersistenzException { dao.speichern(liste); }

    public void laden() throws PersistenzException {
        liste = new ArrayList<>(dao.laden());
    }
}
