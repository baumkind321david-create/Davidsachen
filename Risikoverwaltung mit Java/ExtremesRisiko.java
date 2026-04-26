package Praktikum7;

import java.io.OutputStream;
import java.io.PrintStream;
import java.time.LocalDate;
import java.util.Objects;

public class ExtremesRisiko extends InakzeptablesRisiko{
	private float versicherungsbeitrag;
	public ExtremesRisiko(String bezeichnung, float eintrittswahrscheinlichkeit, float kosten_im_schadensfall,
	String massnahme, float versicherungsbeitrag) {
		super(bezeichnung, eintrittswahrscheinlichkeit, kosten_im_schadensfall, massnahme);
		this.versicherungsbeitrag=versicherungsbeitrag;
		
	}
	public void setVersicherungsbeitrag(float versicherungsbeitrag)
	{
		this.versicherungsbeitrag = versicherungsbeitrag;
	}
	public float getVersicherungsbeitrag()
	{
		return this.versicherungsbeitrag;
	}
	@Override
	public float ermittleRuckstellung()
	{
		return this.versicherungsbeitrag;
	}
	@Override
	public void druckeDaten()
	{
		System.out.printf("Id %d Extremes Risiko %s aus %s; Versicherungsbeitrag %.2f, Massnahme %s%n", this.getId(), this.getBezeichnung(), 
				this.geterstell(), this.getVersicherungsbeitrag(), this.getMassnahme());
	}
	@Override
	public int hashCode()
	{
		return super.hashCode() + Float.hashCode(this.versicherungsbeitrag);
	}
	@Override
	public boolean equals(Object obj)
	{
		if(this==obj) return true;
		if(obj==null || getClass() != obj.getClass()) return false;
		if(!super.equals(obj)) return false;
		
		ExtremesRisiko other = (ExtremesRisiko) obj;
		return Float.compare(this.versicherungsbeitrag, other.versicherungsbeitrag) == 0;
	}
	@Override
	public int compareTo(Risiko o) {
		return (int) (this.berechneRiskowert() - o.berechneRiskowert());
	}
	@Override
	public void druckeDaten(OutputStream stream) {
		PrintStream os = new PrintStream(stream);
		os.printf("Id %d Extremes Risiko %s aus %s; Versicherungsbeitrag %.2f, Massnahme %s%n", this.getId(), this.getBezeichnung(), 
				this.geterstell(), this.getVersicherungsbeitrag(), this.getMassnahme());
		os.flush();
		
	}
}
