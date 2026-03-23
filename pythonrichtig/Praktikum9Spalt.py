import json
import statistics as st
import numpy as np
class keineBuchstaben(Exception):
    """Wird ausgelöst, wenn statt Buchstaben eine Zahl eingegeben wird"""
    def __str__(self):
        return "Kein Buchstaben, sondern Zahlen"

class keineZahl(Exception):
    """Wird ausgelöst, wenn statt Zahl ein Buchstabe eingegeben wird"""
    def __str__(self):
        return "Keine Zahl, sondern Buchstaben"

class reserviertBuchstaben(Exception):
    """Wird ausgelöst, wenn die Spalte bereits Zahlen enthält und Buchstaben hinzugefügt werden sollen"""
    def __str__(self):
        return "Es ist schon für Buchstaben reserviert"

class reserviertZahlen(Exception):
    """Wird ausgelöst, wenn die Spalte bereits Buchstaben enthält und Zahlen hinzugefügt werden sollen"""
    def __str__(self):
        return "Es ist schon für Zahlen reserviert"
class keineRechenoperation(Exception):
    """Wird ausgelöst, wenn anstatt Zahlen Buchstaben sich befinden!"""
    def __str__(self):
        return "Es kann keine Rechenoperationen durchgeführt werden, wegen Buchstaben!"

class OwnColumn:
    """Spalte mit Zahlen oder Buchstaben"""

    def __init__(self, name):
        """Initialisiert eine leere Spalte"""
        self.name = name
        self.werteAlt = []
        self.werteNeu = np.array([])

    def fügeZahlNdarray(self, zahl):
        """Fügt eine Zahl im Ndarray ein und überpürft vorher, ob welcher Typ ist"""
        if np.issubdtype(self.werteNeu.dtype, str):
            raise keineZahl()
        if not isinstance(zahl, (int, float)):
            raise keineZahl()
        self.werteNeu = np.append(self.werteNeu, zahl)



    def fügeZahl(self, zahl):
        """Fügt eine Zahl hinzu.
        Prüft vorher:
        - Wenn die Spalte Buchstaben enthält → reserviertBuchstaben Exception
        - Wenn der Wert kein Zahltyp ist → keineBuchstaben Exception"""
        for i in self.werte:
            if isinstance(i, str):
                raise reserviertBuchstaben()
        if isinstance(zahl, str):
            raise keineBuchstaben()
        else:
            self.werte.append(zahl)

    def fügeBuchstaben(self, buchstaben):
        """Fügt Buchstaben hinzu.
        Prüft vorher:
        - Wenn die Spalte Zahlen enthält → reserviertZahlen Exception
        - Wenn der Wert kein String ist → keineZahl Exception"""
        for i in self.werte:
            if isinstance(i, (float, int)):
                raise reserviertZahlen()
        if not isinstance(buchstaben, str):
            raise keineZahl()
        else:
            self.werte.append(buchstaben)
    def fügeBuchstabenndArray(self, buchstaben):
        """Fügt Buchstaben im Ndarray undf überprüft vorher welcher Typ das Ndarray und der
        übergebene Parameter ist"""
        for i in self.werteNeu:
            if not isinstance(i, str):
                raise reserviertBuchstaben()
        if isinstance(buchstaben, (int, float)):
            raise keineZahl()
        self.werteNeu = np.append(self.werteNeu, buchstaben)

    def löscheBuchstabenmitNdArray(self, Buchstaben):
        """Löscht alle Buchstaben im Ndarray"""
        self.werteNeu = self.werteNeu [self.werteNeu != Buchstaben]
    def loescheBuchstabe(self, Buchstaben):
        """Löscht einen Buchstaben.
        Prüft vorher:
        - Wenn der Wert eine Zahl ist → keineZahl Exception"""
        if isinstance(Buchstaben, (int, float)):
            raise keineZahl()
        else:
            self.werte = [i for i in self.werte if i != Buchstaben]
    def loescheZahlNdarray(self, zahl):
        """Löscht alle Zahlen im Ndarray"""
        self.werteNeu = self.werteNeu[self.werteNeu != zahl]
    def loescheZahl(self, zahl):
        """Löscht eine Zahl.
        Prüft vorher:
        - Wenn der Wert ein String ist → keineBuchstaben Exception"""
        if isinstance(zahl, str):
            raise keineBuchstaben()
        else:
            self.werte = [i for i in self.werte if i != zahl]

    def berechneSummeNdarray(self):
        """Hier wird überprüft, ob das Ndarray aus zahlen besteht, wenn nein, wird keine Summe ausgeben und
        eine Exception ausgegeben, ansonsten wird die Summe ausgegeben!"""
        if not np.issubdtype(self.werteNeu.dtype, np.number):
            raise keineRechenoperation()

        return self.werteNeu.sum()


    def berechneSumme(self):
        """Berechnet die Summe aller Zahlen in der Spalte"""
        summe = 0
        for i in self.werte:
            if isinstance(i, str):
                raise keineRechenoperation()
            else:
                summe = summe + i
        return summe

    def berechneMittelwert(self):
        """Berechnet den Mittelwert aller Zahlen in der Spalte"""
        mittelwert = sum(self.werte)/len(self.werte)
        if mittelwert == 0:
            print("Es sind keine Zahlen angeben oder es sind nur Buchstaben vorhanden")
        return mittelwert
    def berechneMean(self):
        """
        Berechnet Median mithilfe von statisticsmodul
        :return:
        """
        mittelwert = st.mean(self.werte)
        return mittelwert
    def berechneMittelwertNd(self):
        """Hier wird der Mittelwert von Ndarray berechnet"""
        if not np.issubdtype(self.werteNeu.dtype, np.number):
            raise keineRechenoperation()
        return self.werteNeu.mean()

    def berechneModalwert(self):
        """
        Berechnet Modalwert mithilfe von statisticsmodul
        :return:
        """

        if self.werte and isinstance(self.werte[0], (float, int)):
         return st.mode(self.werte)
        else:
            keineBuchstaben()
    def berechneModalwertNd(self):
        """Es berechnet den Modalwert vom Ndarray und mindstens 2!! (Variante)"""
        if not np.issubdtype(self.werteNeu.dtype, np.number):
            raise keineRechenoperation()


        da = np.unique_counts(self.werteNeu)
        return da
    def berechneVariance(self):
        """
        Berechnet Variance mithilfe von statisticsmoduk
        :return:
        """
        return st.variance(self.werte)

    def berechneVarianceNd(self):
        """berechnet Variance mithilfe von Ndarray"""
        if not np.issubdtype(self.werteNeu.dtype, np.number):
            raise keineRechenoperation()
        return self.werteNeu.var()