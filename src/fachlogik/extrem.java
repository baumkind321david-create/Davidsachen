package fachlogik;

import java.io.OutputStream;
import java.io.PrintStream;
import java.util.Objects;

public class extrem extends inakze {

    private static final long serialVersionUID = 1L;
    private float versicherungsbeitrag;

    public extrem(Risiko1 r) {
        super(r.getBezeichnung(), r.getEintrittswahrscheinlichkeit(), r.getKostenImSchadensfall(), "");
    }

    public extrem(String bezeichnung, float wkeit, float kosten, String massnahme, float beitrag) {
        super(bezeichnung, wkeit, kosten, massnahme);
        this.versicherungsbeitrag = beitrag;
    }

    @Override
    public float ermittleRueckstellung() { return versicherungsbeitrag; }

    public float getVersicherungsbeitrag() { return versicherungsbeitrag; }
    @Override
    public void setVersicherungsbeitrag(float beitrag) { this.versicherungsbeitrag = beitrag; }

    @Override
    public void druckeDaten() { druckeDaten(System.out); }

    @Override
    public void druckeDaten(OutputStream out) {
        PrintStream ps = new PrintStream(out, true);
        ps.printf("Id: %d\tExtremes Risiko: %s\taus %s\tVersicherungsbeitrag: %.2f\tMassnahme: %s%n",
                getId(), getBezeichnung(), getDatum(), versicherungsbeitrag, getMassnahme());
    }

    @Override
    public int hashCode() { return Objects.hash(super.hashCode(), versicherungsbeitrag); }

    @Override
    public boolean equals(Object obj) {
        if(!super.equals(obj)) return false;
        extrem other = (extrem) obj;
        return Float.compare(versicherungsbeitrag, other.versicherungsbeitrag) == 0;
    }
}
