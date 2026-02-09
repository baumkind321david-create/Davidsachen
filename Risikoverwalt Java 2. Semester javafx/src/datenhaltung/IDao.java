package datenhaltung;

import java.util.List;
import fachlogik.Risiko1;

public interface IDao {
    void speichern(List<Risiko1> liste) throws PersistenzException;
    List<Risiko1> laden() throws PersistenzException;
}
