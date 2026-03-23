import json
import pickle as pick
import logging as log
import numpy as np
from matplotlib import pyplot as plt

log.basicConfig(filename="fehler.log", level=log.INFO,
                style="{", format="{asctime} [{levelname:8}] {message}")
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
class nurZahlenSpalte(Exception):
    """Wird ausgelöst, wenn die Spalte nicht numerisch ist"""
    def __str__(self):
        return "Es darf kein Plot gezeichnet werden, weil nicht numerisch! Gibt eine numerische Spalte an!"
class gleicheGrößeSpalte(Exception):
    """Wird ausgelöst, wenn beide Spalte nicht die gleiche Größe haben! Wähle eine Spalte, die gleich greoß sind!"""
    def __str__(self):
        return "Geben Sie Spalten an, die die gleiche Größen haben"
class OwnTable:
    """Tabelle mit mehreren Spalten, die Zahlen oder Buchstaben enthalten können"""

    def __init__(self):
        """Initialisiert eine leere Tabelle"""
        self.table = {}
        self.index = 0

    def fügeSpalte(self, spalte):
        """Fügt eine Spalte hinzu"""
        self.table[spalte.name] = spalte

    def löscheSpalte(self, name):
        """Löscht eine Spalte nach Namen.
        Exception: KeyError wird abgefangen, wenn der Name nicht existiert"""
        try:
            del self.table[name]
        except KeyError:
            print("Gibt einen gültigen Namen ein")
            log.error("Es ist ein Fehler aufgetreten, wegen falscher Schlüssel beim Löschen")

    def zugreifenSpalte(self, name):
        """Gibt die Spalte zurück.
        Exception: KeyError wird abgefangen, wenn der Name nicht existiert"""
        try:
            return self.table[name]
        except KeyError:
            print("Gibt einen gültigen Namen ein")
            log.error("Es ist ein Fehler aufgetreten, wegen falscher Schlüssel beim Zugreifen")

    def speichernTabelle(self, text):
        """Speichert die Tabelle als JSON-Datei"""
        with open(text, "w") as f:
            temp = {name: column.werte for name, column in self.table.items()}
            json.dump(temp, f)

    def ladenTabelle(self, text):
        """Lädt die Tabelle aus einer JSON-Datei.
        Exception: FileNotFoundError wird abgefangen, wenn die Datei nicht existiert"""
        try:
            with open(text, "r") as f:
                da = json.load(f)
                for name, werte in da.items():
                    spalte = OwnColumn(name)
                    spalte.werte = werte
                    self.table[name] = spalte
        except FileNotFoundError:
            print("Die Datei existiert nicht, bitte gib einen gültigen Dateinamen an!")
            log.error("Es ist ein Fehler aufgetreten, wegen falscher Filename beim Laden der Tabelle mit json")

    def __iter__(self):
        """Iterator starten"""
        self.index = 0
        return self

    def __next__(self):
        """Gibt die nächste Zeile als Dictionary zurück, fehlende Werte werden None"""
        if not self.table:
            raise StopIteration
        nums_rows = max(len(col.werte) for col in self.table.values())  # längste Spalte
        if self.index >= nums_rows:
            raise StopIteration
        row_dict = {}
        for name, col in self.table.items():
            if self.index < len(col.werte):
                row_dict[name] = col.werte[self.index]
            else:
                row_dict[name] = None
        self.index += 1
        return row_dict

    def describe(self):
        tabelle = []
        """Gibt für jede Spalte den MIN, MAX und Mean, Mode und Variance an, aber nur für Zahlenspalten"""
        for own_column, column in self.table.items():
            try:
                if isinstance(column.werteAlt[0], (float, int)):
                    da = {own_column: {"Min": min(column.werteAlt), "Max": max(column.werteAlt),
                                       "Mean": column.berechnestaMean(), "Mode":
                                           column.berechnestaMode(), "berechnestaVaria": column.berechnestatVaria()}}
                    tabelle.append(da)
                    return tabelle
            except IndexError:
                print("Es befindet sich keine Zahl")
    def describeNd(self):
        tabelle = []
        """Gibt nur jede Zahlenspalte in Numpy Min, Max, Mean, Mode und Variance"""
        for own_column, column in self.table.items():
            if np.issubdtype(column.werteNeu.dtype, np.number):
                da = {own_column: {"Min": np.min(column.werteNeu), "Max": np.max(column.werteNeu),
                                   "Mean": column.berechneMittelwertNd(), "Mode": column.berechneModalwertNd(),
                                   "Varainz": column.berechneVarianceNd()}}
                tabelle.append(da)
        return tabelle
    def schreibPickle(self, name):
        """Ganzes Objekt speichern"""

        with open(name, "wb") as f:
             pick.dump(self, f)

    def ladenPickle(self, name):
        """Ganzes Objekt laden und wenn es nicht gibt, wird eine Exception ausgegeben"""
        try:
         with open(name, "rb") as f:
            re = pick.load(f)

         return re
        except FileNotFoundError:
            print("gibt einen gültigen Ordner ein!")
            log.error("Es ist ein Fehler aufgetreten, wegen falscher Filename beim Laden mit Pickle")
    def zeichnen(self):
        """zeichnet Diagramm mithilfe vom Columnobjekt und beide Spalten müssen die gleiche Länge und die Zweite muss numerisch!"""
        plt.figure(figsize=(10, 10))
        typ = input(
            "Was für ein Diagramm wollen Sie? Linien = li, Balken = bar(vertikal)/bar(horizontal), Kreis=pie, Histogramm = hist, Scatterplot = scat, Boxplot=box")
        title1 = input("Geben Sie einen passenden Titel an!")
        try:
            spalte1 = input("Wählen Sie eine Spalte(x) beliebig aus")
            spalte2 = input("Wählen Sie eine Spalte(y) und muss numerisch sein!")
            if not np.issubdtype(self.table[spalte2].werteNeu.dtype, np.number):
                raise nurZahlenSpalte()
            if self.table[spalte1].werteNeu.size != self.table[spalte2].werteNeu.size:
                raise gleicheGrößeSpalte("muss die gleiche Größe sein")

            if typ == "li":
                plt.plot(self.table[spalte1].werteNeu, self.table[spalte2].werteNeu, color="red", marker="o",
                         linewidth=2, markersize=12, title = title1)
                plt.show()
            elif typ == "bar":
                art = input("Was wollen wir Sie haben vertikal(ver) oder horizontal (hor)?")
                if art == "ver":
                    plt.bar(self.table[spalte1].werteNeu, height= self.table[spalte2].werteNeu)
                    plt.title(title1)
                    plt.show()
                elif art == "hor":
                    plt.barh(self.table[spalte1].werteNeu, width= self.table[spalte2].werteNeu)
                    plt.title(title1)
                    plt.show()
                else:
                    print("Wähle nur gültige Eingaben von bar (ver/hor) oder ein anderes Diagramm!")
            elif typ == "pie":
                plt.pie(x=self.table[spalte2].werteNeu, labels=self.table[spalte1].werteNeu)
                plt.title(title1)
                plt.show()
            elif typ == "hist":
                spalt = input("Welche Spalte wollen Sie verwenden? Erste(alsErstes) oder Zweite (alsZweites), die ausgewählt wurde?")
                if spalt == "alsErst":
                 if not np.issubdtype(self.table[spalte1].werteNeu.dtype, np.number):
                    raise nurZahlenSpalte()
                 else:
                     plt.hist(self.table[spalte1].werteNeu)
                     plt.title(title1)
                     plt.show()
                elif spalt == "alsZweites":
                    plt.hist(self.table[spalte2].werteNeu)
                    plt.title(title1)
                    plt.show()
                else:
                    print("Versuchen Sie es nocheinmal die richtige Spalte auszuwählen oder ein anderes Diagramm!")
            elif typ == "scat":
                plt.scatter(x=self.table[spalte1].werteNeu, y= self.table[spalte2].werteNeu)
                plt.title(title1)
                plt.show()
            elif typ == "box":
                spalt = input(
                    "Welche Spalte wollen Sie verwenden? Erste(alsErstes) oder Zweite (alsZweites), die ausgewählt wurde?")
                if spalt == "alsErstes":
                    if not np.issubdtype(self.table[spalte1].werteNeu.dtype, np.number):
                        raise nurZahlenSpalte()
                    else:
                        plt.boxplot(self.table[spalte1].werteNeu)
                        plt.title(title1)
                        plt.show()
                elif spalt == "alsZweites":
                    plt.boxplot(self.table[spalte2].werteNeu)
                    plt.title(title1)
                    plt.show()
                else:
                    print("Versuchen Sie es nocheinmal die richtige Spalte auszuwählen oder ein anderes Diagramm!")
            else:
                print("Gib eine passendes Diagramm nocheinmal an!")
        except KeyError:
            print("Geben Sie einen passenden Key (vorhandene Spaltennamen) an!")
        except nurZahlenSpalte:
            print("Die gewählte Spalte muss numerisch sein!")
        except gleicheGrößeSpalte as e:
            print(e)
