package Praktikum7;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Scanner;
import javax.swing.JOptionPane;
public class Menü {
	private int Limit = 1000;
	private int kostenlimit = 5000;

	public void starten(Risikoverwaltung risikoverwalt) throws AbbruchException, IOException, ClassNotFoundException
	{
		Scanner scanner = new Scanner (System.in);
		int variable = 0;
		do
		{
			System.out.println("Risikoverwaltung:");
			System.out.println("1. Risiko aufnehmen.");
			System.out.println("2. Zeige alle Risiken");
			System.out.println("3. Risikoliste in Datei schreiben");
			System.out.println("4. Zeige Risiko mit maximaler Rückstellung");
			System.out.println("5. Berechne Summe aller Rückstellungen");
			System.out.println("6. Speichern in einer Datei");
			System.out.println("7. Laden in einer Datei");
			System.out.println("8. Beenden");
			System.out.println("Bitte Auswahl eingeben:");
			variable = scanner.nextInt();
			scanner.nextLine();
			
			switch(variable)	
			{
			case 1:
				String bezeichnung = JOptionPane.showInputDialog(null, "Geben Sie die Bezeichnung des Risikos ein");
				if (bezeichnung == null)
				{
					
					throw new AbbruchException("Vorgang beendet - nocheinmal");
					
					
				}
				String eintrittswahrscheinlichkeit = JOptionPane.showInputDialog(null, "Geben Sie die Eintrittswahrscheinlichkeit ein");
				if(eintrittswahrscheinlichkeit == null)
				{
					throw new AbbruchException("Vorgang beendet - nocheinmal");
				}
				float eintr = 0.0f;
			    float kostenim = 0.0f;
			    float versich = 0.0f;
				try
				{
					eintr = Float.parseFloat(eintrittswahrscheinlichkeit);
				}
				catch(NumberFormatException e)
				{
					JOptionPane.showMessageDialog(null,"Bitte gültige Eintrittswahrscheinlichkeit (Float) eingeben");
					break;
				}
				String kosten = JOptionPane.showInputDialog(null, "Geben Sie die Kosten im Schadensfall an");
				if (kosten == null)
				{
					throw new AbbruchException("Vorgang beendet - nocheinmal");
				}
				try
				{
					kostenim = Float.parseFloat(kosten);
				}
				catch (NumberFormatException e)
				{
					JOptionPane.showInputDialog(null, "Bitte gültige Kosten_im_Schadensfall (Float) eingeben");
					break;
				}
				float Risikowert = eintr * kostenim;
				
				if(Risikowert < this.Limit)
				{
					AkzeptablesRisiko akzep = new AkzeptablesRisiko(bezeichnung, eintr, kostenim);
					risikoverwalt.aufnehmen(akzep);
				}
				else
				{
					String Massnahmen = JOptionPane.showInputDialog(null, "Geben Sie die Maßnahmen ein");
					if (Massnahmen == null)
					{
						throw new AbbruchException("Vorgang beendet - nocheinmal");
					}
					if(kostenim > this.kostenlimit)
					{
						String Versicherungsbeitrag = JOptionPane.showInputDialog(null, "Geben Sie den Versicherungsbeitrag an");
						if (Versicherungsbeitrag == null)
						{
							throw new AbbruchException("Vorgang beendet - nocheinmal");
						}
						try
						{
							versich = Float.parseFloat(Versicherungsbeitrag);
						}
						catch (NumberFormatException e)
						{
							JOptionPane.showMessageDialog(null, "Bitte gültigen Versicherungsbeitrag (Float) eingeben");
							break;
						}
						ExtremesRisiko extrem = new ExtremesRisiko(bezeichnung, eintr, kostenim, Massnahmen, versich);
						risikoverwalt.aufnehmen(extrem);
					}
					else
					{
						InakzeptablesRisiko inakze = new InakzeptablesRisiko (bezeichnung, eintr, kostenim, Massnahmen);
						risikoverwalt.aufnehmen(inakze);
					}
				}
				break;
			case 2:
				risikoverwalt.zeigeRisiken();
				break;
			case 3:
				String dateipfad = null;
				while(dateipfad == null)
				{
					dateipfad = JOptionPane.showInputDialog(null, "Geben Sie ein Pfad ein");
					if(dateipfad == null)
					{
						int result = JOptionPane.showConfirmDialog(null, "Dateiname ist Leer! Neuen Dateinamen wählen?", "Warnung", 
								JOptionPane.YES_NO_OPTION);
						if (result == JOptionPane.YES_NO_OPTION)
						{
							dateipfad = null;
						}
						else
						{
							JOptionPane.showMessageDialog(null, "Vorgang abbrechen");
							throw new AbbruchException("Vorgang beendet - nocheinmal");
						}
					}
				}
					FileOutputStream ziel  = new FileOutputStream("C:\\Users\\baumk\\Downloads\\" + dateipfad, true);
					risikoverwalt.zeigeRisikeninDatei(ziel);
					ziel.close();
				break;
			case 4:
				 risikoverwalt.sucheRisikomitMaxRuckstellung().druckeDaten();
				 break;
			case 5: 
				float ergebnis = risikoverwalt.berechneSummeRueckstellungen();
				System.out.printf("Die Summe aller Rueckstellungen sind %f", ergebnis);
				break;
			case 6:
				String dateipfad1 = null;
				while(dateipfad1 == null)
				{
					dateipfad1 = JOptionPane.showInputDialog(null, "Geben Sie ein Pfad ein");
					if(dateipfad1 == null)
					{
						int result = JOptionPane.showConfirmDialog(null, "Dateiname ist Leer! Neuen Dateinamen wählen?", "Warnung", 
								JOptionPane.YES_NO_OPTION);
						if (result == JOptionPane.YES_NO_OPTION)
						{
							dateipfad1 = null;
						}
						else
						{
							JOptionPane.showMessageDialog(null, "Vorgang abbrechen");
							throw new AbbruchException("Vorgang beendet - nocheinmal");
						}
					}
				}
				File ziel1  = new File ("C:\\Users\\baumk\\Downloads\\" + dateipfad1);
				risikoverwalt.speichern(ziel1);
				break;
			case 7:
				String dateipfad2 = null;
				while(dateipfad2 == null)
				{
					dateipfad2 = JOptionPane.showInputDialog(null, "Geben Sie ein Pfad ein");
					if(dateipfad2 == null)
					{
						int result = JOptionPane.showConfirmDialog(null, "Dateiname ist Leer! Neuen Dateinamen wählen?", "Warnung", 
								JOptionPane.YES_NO_OPTION);
						if (result == JOptionPane.YES_NO_OPTION)
						{
							dateipfad2 = null;
						}
						else
						{
							JOptionPane.showMessageDialog(null, "Vorgang abbrechen");
							throw new AbbruchException("Vorgang beendet - nocheinmal");
						}
					}
				}
				File ziel2  = new File ("C:\\Users\\baumk\\Downloads\\" + dateipfad2);
				risikoverwalt.laden(ziel2);
				break;
			case 8:
				System.out.println("Programm beendet");
				break;
			default: 
				System.out.println("Gib bitte nur gültige Zahlen von 1 bis 5 ein");	
			}
		}while(variable != 8);
		scanner.close();
	}
}
