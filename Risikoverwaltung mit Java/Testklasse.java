package Praktikum7;

import java.io.FileNotFoundException;
import java.io.IOException;

import javax.swing.JOptionPane;

public class Testklasse {

	public static void main(String[] args) throws IOException, ClassNotFoundException   {
		
		Menü neu = new Menü();
		Risikoverwaltung ne = new Risikoverwaltung();
		while(true)
		{
		try {
			try {
				neu.starten(ne);
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			break;
		} catch (AbbruchException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println("Abbruch erkannt. Starte Menü neu...");
		}
		
	
	}
		System.out.println("Programm beendet");

}
}