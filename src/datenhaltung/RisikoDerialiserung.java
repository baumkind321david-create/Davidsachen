package datenhaltung;

import java.io.*;
import java.util.ArrayList;
import java.util.List;
import fachlogik.Risiko1;

public class RisikoDerialiserung implements IDao {

    private String dateipfad;

    public RisikoDerialiserung(String dateipfad) {
        this.dateipfad = dateipfad;
    }

    @Override
    public void speichern(List<Risiko1> liste) throws PersistenzException {
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(dateipfad))) {
            oos.writeObject(liste);
        } catch (IOException e) {
            throw new PersistenzException("Fehler beim Speichern der Datei: " + dateipfad, e);
        }
    }

    @Override
    @SuppressWarnings("unchecked")
    public List<Risiko1> laden() throws PersistenzException {
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(dateipfad))) {
            return new ArrayList<>((List<Risiko1>) ois.readObject());
        } catch (IOException | ClassNotFoundException e) {
            throw new PersistenzException("Fehler beim Laden der Datei: " + dateipfad, e);
        }
    }
}
