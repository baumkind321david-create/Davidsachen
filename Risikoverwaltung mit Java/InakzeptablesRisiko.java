package Praktikum7;

import java.io.OutputStream;
import java.io.PrintStream;
import java.time.LocalDate;
import java.util.Objects;

public class InakzeptablesRisiko extends Risiko{
private String massnahme;
	
	public InakzeptablesRisiko (String bezeichnung, float eintrittswahrscheinlichkeit,
			float kosten_im_schadensfall,String massnahme)
	{
		super(bezeichnung, eintrittswahrscheinlichkeit, kosten_im_schadensfall);
		this.massnahme = massnahme;
	}
	public String getMassnahme()
	{
		return this.massnahme;
	}
	public void setMassnahme(String Massnahme)
	{
		this.massnahme = Massnahme;
	}
	@Override
	public float ermittleRuckstellung()
	{
		return this.berechneRiskowert();
	}
	@Override
	public void druckeDaten()
	{
		System.out.printf("Id %d Inakzeptables Risiko %s aus %s; Risikowert %.2f; Rückstellung %.2f, Massnahme %s%n", this.getId(), this.getBezeichnung(), 
				this.geterstell(), this.berechneRiskowert(), this.ermittleRuckstellung(), this.getMassnahme());
	}
	@Override
	public int hashCode()
	{
		return super.hashCode() + (massnahme !=null? this.massnahme.hashCode() : 0);
	}
	@Override
	public boolean equals(Object obj)
	{
		if(this==obj) return true;
		if(obj==null || getClass() != obj.getClass()) return false;
		if(!super.equals(obj)) return false;
		
		InakzeptablesRisiko other = (InakzeptablesRisiko) obj;
		return Objects.equals(this.massnahme, other.massnahme);
	}
	@Override
		public int compareTo(Risiko o) {
			return (int) (this.berechneRiskowert() - o.berechneRiskowert());
		}
	@Override
	public void druckeDaten(OutputStream stream) { //wohin
		PrintStream e = new PrintStream(stream);
		e.printf("Id %d Inakzeptables Risiko %s aus %s; Risikowert %.2f; Rückstellung %.2f, Massnahme %s%n", this.getId(), this.getBezeichnung(), 
				this.geterstell(), this.berechneRiskowert(), this.ermittleRuckstellung(), this.getMassnahme());
		e.flush();
	}
}
