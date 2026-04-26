package Praktikum7;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
public class Risikoverwaltung {
	private List <Risiko> liste;
	
	//Iterator<Risiko> it = Liste.iterator();
	private int size = 0;
	private Iterator <Risiko> it;
	public Risikoverwaltung()
	{
		liste = new ArrayList <Risiko>();
}
	public void aufnehmen(Risiko r)
	{
		liste.add(r);
	}
	public void zeigeRisiken()
	{
		Collections.sort(liste);
		Iterator<Risiko> it = liste.iterator();
		while(it.hasNext())
		{
			Risiko r = it.next();
			if(r!=null)
			{
				r.druckeDaten();
			}
		}
	}
	public void zeigeRisikeninDatei(OutputStream stream)
	{
		Collections.sort(liste);
		Iterator<Risiko> it = liste.iterator();
		while(it.hasNext())
		{
			Risiko r = it.next();
			if(r !=null)
			{
				r.druckeDaten(stream);
			}
		}
	}
	public Risiko sucheRisikomitMaxRuckstellung()
	{
		Risiko ergebnis = null;
		for (Risiko a: liste)
		{
			if(a!=null)
			{
			if(ergebnis ==null || a.ermittleRuckstellung() > ergebnis.ermittleRuckstellung())
			{
				ergebnis = a;
				return ergebnis;
			}
		}
		}
		return ergebnis;
	}
	public float berechneSummeRueckstellungen()
	{
		float ergebnis = 0;
		Iterator<Risiko> it = liste.iterator();
		while(it.hasNext())
		{
			Risiko r = it.next();
			if(r != null)
			{
				ergebnis = ergebnis + r.ermittleRuckstellung();
			}
		}
		return ergebnis;
	}
	public void speichern (File to) throws FileNotFoundException, IOException
	{
		try(FileOutputStream fos = new FileOutputStream(to);
				ObjectOutputStream oos = new ObjectOutputStream(fos))
		{
			oos.writeObject(this.liste);
		}
	}
	public void laden(File from) throws IOException, ClassNotFoundException
	{
		try(FileInputStream fis = new FileInputStream(from);
				ObjectInputStream ois = new ObjectInputStream(fis))
		{
			this.liste = (ArrayList<Risiko>) ois.readObject();
		}
	}
}
