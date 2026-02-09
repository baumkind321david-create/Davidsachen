package fachlogik;

import java.io.OutputStream;
import java.io.PrintStream;
import java.util.Objects;

public class inakze extends Risiko1 {

    private static final long serialVersionUID = 1L;
    private String massnahme;

    public inakze() { super(); }

    public inakze(String bezeichnung, float wkeit, float kosten, String massnahme) {
        super(bezeichnung, wkeit, kosten);
        this.massnahme = massnahme;
    }

    public inakze(Risiko1 r) {
        super(r.getBezeichnung(), r.getEintrittswahrscheinlichkeit(), r.getKostenImSchadensfall());
    }

    @Override
    public float ermittleRueckstellung() { return berechneRisikowert(); }

    @Override
    public void druckeDaten() { druckeDaten(System.out); }

    @Override
    public void druckeDaten(OutputStream out) {
        PrintStream ps = new PrintStream(out, true);
        ps.printf("Id: %d\tInakzeptables Risiko: %s\taus %s\tRisikowert: %.2f\tRückstellung: %.2f\tMassnahme: %s%n",
                getId(), getBezeichnung(), getDatum(), berechneRisikowert(), ermittleRueckstellung(), massnahme);
    }

    @Override
    public void setMassnahme(String m) { this.massnahme = m; }
    @Override
    public String getMassnahme() { return massnahme; }

    @Override
    public int hashCode() { return Objects.hash(super.hashCode(), massnahme); }

    @Override
    public boolean equals(Object obj) {
        if(!super.equals(obj)) return false;
        if(obj == null || getClass() != obj.getClass()) return false;
        inakze other = (inakze) obj;
        return Objects.equals(massnahme, other.massnahme);
    }
}

