package Praktikum7;

import java.io.OutputStream;
import java.io.PrintStream;
import java.time.LocalDate;

public class AkzeptablesRisiko extends Risiko {

	public AkzeptablesRisiko(String bezeichnung, float eintrittswahrscheinlichkeit,
			float kosten_im_schadensfall) {
		super(bezeichnung, eintrittswahrscheinlichkeit, kosten_im_schadensfall);
	
	}
	@Override
	public float ermittleRuckstellung()
	{
		return 0;
	}
	@Override
	public void druckeDaten()
	{
		System.out.printf("Id %d AktzeptablesRisiko %s aus %s; Risikowert %.2f; Rückstellung %.2f%n", this.getId(), this.getBezeichnung(), 
				this.geterstell(), this.berechneRiskowert(), this.ermittleRuckstellung());
	}
	@Override
	public int hashCode()
	{
		return super.hashCode();
	}
	@Override
	public int compareTo(Risiko o) {
		return (int) (this.berechneRiskowert() - o.berechneRiskowert());
	}
	@Override
	public void druckeDaten(OutputStream stream) {
		PrintStream os = new PrintStream(stream);
		os.printf("Id %d AktzeptablesRisiko %s aus %s; Risikowert %.2f; Rückstellung %.2f%n", this.getId(), this.getBezeichnung(), 
				this.geterstell(), this.berechneRiskowert(), this.ermittleRuckstellung());
		os.flush();
		
	}
	
}
