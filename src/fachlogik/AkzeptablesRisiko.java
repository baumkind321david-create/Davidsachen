package fachlogik;

import java.io.OutputStream;
import java.io.PrintStream;
import java.util.Objects;

public class AkzeptablesRisiko extends Risiko1 {

    private static final long serialVersionUID = 1L;

    public AkzeptablesRisiko() { super(); }

    public AkzeptablesRisiko(String bezeichnung, float wkeit, float kosten) {
        super(bezeichnung, wkeit, kosten);
    }

    @Override
    public float ermittleRueckstellung() { return 0f; }

    @Override
    public void druckeDaten() { druckeDaten(System.out); }

    @Override
    public void druckeDaten(OutputStream out) {
        PrintStream ps = new PrintStream(out, true);
        ps.printf("Id: %d\tAkzeptables Risiko: %s\taus %s\tRisikowert: %.2f\tRückstellung: %.2f%n",
                getId(), getBezeichnung(), getDatum(), berechneRisikowert(), ermittleRueckstellung());
    }

    @Override
    public int hashCode() { return Objects.hash(super.hashCode()); }

    @Override
    public boolean equals(Object obj) { return super.equals(obj); }
}

