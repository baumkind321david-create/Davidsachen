package datenhaltung;

public class PersistenzException extends Exception {

    public PersistenzException() {
        super();
    }

    public PersistenzException(String message) {
        super(message);
    }

    public PersistenzException(String message, Throwable cause) {
        super(message, cause);
    }
}
