package fachlogik;

import java.io.OutputStream;
import java.io.PrintStream;
import java.io.Serializable;
import java.time.LocalDate;
import java.util.Objects;

public abstract class Risiko1 implements Comparable<Risiko1>, Serializable {

    private static int count = 0;
    public static final long serialVersionUID = 1L;

    private final int id;
    private String bezeichnung;
    private float eintrittswahrscheinlichkeit;
    private float kostenImSchadensfall;
    private final LocalDate erstellungsdatum;

    public Risiko1() {
        this.id = count++;
        this.erstellungsdatum = LocalDate.now();
    }

    public Risiko1(String bezeichnung, float eintrittswahrscheinlichkeit, float kostenImSchadensfall) {
        this.id = count++;
        this.erstellungsdatum = LocalDate.now();
        this.bezeichnung = bezeichnung;
        this.eintrittswahrscheinlichkeit = eintrittswahrscheinlichkeit;
        this.kostenImSchadensfall = kostenImSchadensfall;
    }

    public int getId() { return id; }
    public String getBezeichnung() { return bezeichnung; }
    public void setBezeichnung(String bezeichnung) { this.bezeichnung = bezeichnung; }
    public float getEintrittswahrscheinlichkeit() { return eintrittswahrscheinlichkeit; }
    public void setEintrittswahrscheinlichkeit(float wkeit) { this.eintrittswahrscheinlichkeit = wkeit; }
    public float getKostenImSchadensfall() { return kostenImSchadensfall; }
    public void setKostenImSchadensfall(float kosten) { this.kostenImSchadensfall = kosten; }
    public LocalDate getDatum() { return erstellungsdatum; }

    public abstract float ermittleRueckstellung();
    public abstract void druckeDaten();
    public abstract void druckeDaten(OutputStream out);

    public void setMassnahme(String m) {}
    public void setVersicherungsbeitrag(float v) {}
    public String getMassnahme() { return ""; }

    public float berechneRisikowert() {
        return eintrittswahrscheinlichkeit * kostenImSchadensfall;
    }

    @Override
    public int compareTo(Risiko1 other) {
        return Float.compare(this.berechneRisikowert(), other.berechneRisikowert());
    }

    @Override
    public int hashCode() {
        return Objects.hash(bezeichnung, eintrittswahrscheinlichkeit, kostenImSchadensfall, erstellungsdatum);
    }

    @Override
    public boolean equals(Object obj) {
        if(this == obj) return true;
        if(obj == null || getClass() != obj.getClass()) return false;
        Risiko1 other = (Risiko1) obj;
        return Float.compare(eintrittswahrscheinlichkeit, other.eintrittswahrscheinlichkeit) == 0 &&
               Float.compare(kostenImSchadensfall, other.kostenImSchadensfall) == 0 &&
               Objects.equals(bezeichnung, other.bezeichnung) &&
               Objects.equals(erstellungsdatum, other.erstellungsdatum);
    }

    @Override
    public String toString() {
        return String.format("Id: %d, %s, Datum: %s, Risikowert: %.2f", id, bezeichnung, erstellungsdatum, berechneRisikowert());
    }
}
