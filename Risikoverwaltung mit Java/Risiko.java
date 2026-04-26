package Praktikum7;
import java.io.OutputStream;
import java.io.Serializable;
import java.time.LocalDate;
import java.util.Objects;

public abstract class Risiko implements Comparable<Risiko>, Serializable{
	private transient static int counter  = 0;
	private static final long serialVersionUID = 1L;
	private int id;
	private String bezeichnung;
	private float eintrittswahrscheinlichkeit;
	private float kosten_im_schadensfall;
	private LocalDate erstellungsdatum;
	public Risiko ( String bezeichnung, float eintrittswahrscheinlichkeit, float kosten_im_schadensfall ) {
		this.id = id;
		this.bezeichnung = bezeichnung;
		this.eintrittswahrscheinlichkeit = eintrittswahrscheinlichkeit;
		this.kosten_im_schadensfall = kosten_im_schadensfall;
		this.erstellungsdatum = LocalDate.now();
		this.id =counter++;
	}
	public int getId ()
	{
		return this.id;
	}
	public String getBezeichnung()
	{
		return this.bezeichnung;
	}
	public void setBezeichnung(String Bezeichnung)
	{
		this.bezeichnung = Bezeichnung;
	}
	public float getEintrittswahrscheinlichkeit()
	{
		return this.eintrittswahrscheinlichkeit;
	}
	public void setEintrittswahrscheinlichkeit(float eintritts)
	{
		this.eintrittswahrscheinlichkeit = eintritts;
	}
	public float getKosten()
	{
		return this.kosten_im_schadensfall;
	}
	public void setKosten(float kosten)
	{
		this.kosten_im_schadensfall= kosten;
	}
	public LocalDate geterstell()
	{
		return this.erstellungsdatum;
	}
	public float berechneRiskowert()
	{
		return this.eintrittswahrscheinlichkeit * this.kosten_im_schadensfall;
	}
	public abstract float ermittleRuckstellung();
	public abstract void druckeDaten();
	@Override
	public int hashCode()
	{
		return Objects.hash(this.id, this.bezeichnung, this.eintrittswahrscheinlichkeit, this.kosten_im_schadensfall, this.erstellungsdatum != null ? this.erstellungsdatum : 0);
	}
	@Override
	public boolean equals(Object obj)
	{
		if(this==obj) return true;
		if(obj== null || getClass() != obj.getClass()) return false;
		Risiko other = (Risiko) obj;
		
		return 
				Objects.equals(this.bezeichnung, other.bezeichnung) &&
				Float.compare(this.eintrittswahrscheinlichkeit, other.eintrittswahrscheinlichkeit) == 0&& 
				Float.compare(this.kosten_im_schadensfall, other.kosten_im_schadensfall) == 0&&
				Objects.equals(this.erstellungsdatum, other.erstellungsdatum);
		
	}
	public abstract int compareTo(Risiko andere);
	public abstract void druckeDaten(OutputStream stream);
}
