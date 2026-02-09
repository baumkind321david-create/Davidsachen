# ------------------- OwnColumn -------------------

import statistics as stat
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

class LeererWert(Exception):
    def __str__(self):
        return "Leerer Wert wurde angegeben."

class NurZahlen(Exception):
    def __str__(self):
        return "Die Spalte enthält Buchstaben, numerische Operation nicht möglich."

class OwnColumn:
    def __init__(self, name):
        self.name = name
        self.spalte = []
        self.typ = None  # "zahl" oder "text"

    # ----- Hinzufügen von Werten -----
    def hinzufuegen(self, wert):
        if wert is None:
            raise LeererWert()
        if isinstance(wert, (int, float)):
            if self.typ is None:
                self.typ = "zahl"
            elif self.typ != "zahl":
                raise TypeError("Mischung aus Zahlen und Text nicht erlaubt")
            self.spalte.append(wert)
        elif isinstance(wert, str):
            if self.typ is None:
                self.typ = "text"
            elif self.typ != "text":
                raise TypeError("Mischung aus Zahlen und Text nicht erlaubt")
            self.spalte.append(wert)
        else:
            raise TypeError("Nur Zahlen oder Text erlaubt")

    # ----- Statistische Methoden -----
    def summe(self):
        if self.typ != "zahl":
            raise NurZahlen()
        return sum(self.spalte)

    def mittelwert(self):
        if self.typ != "zahl":
            raise NurZahlen()
        return stat.mean(self.spalte)

    def median(self):
        if self.typ != "zahl":
            raise NurZahlen()
        return stat.median(self.spalte)

    def varianz(self):
        if self.typ != "zahl":
            raise NurZahlen()
        return stat.variance(self.spalte) if len(self.spalte) > 1 else 0

    def standardabweichung(self):
        if self.typ != "zahl":
            raise NurZahlen()
        return stat.stdev(self.spalte) if len(self.spalte) > 1 else 0

    def range(self):
        if self.typ != "zahl":
            raise NurZahlen()
        return max(self.spalte) - min(self.spalte)

    def modalwert(self):
        try:
            return stat.mode(self.spalte)
        except stat.StatisticsError:
            return None

    # ----- Filterfunktionen -----
    def filter_groesser(self, wert):
        if self.typ != "zahl":
            raise NurZahlen()
        return [x for x in self.spalte if x > wert]

    def filter_kleiner(self, wert):
        if self.typ != "zahl":
            raise NurZahlen()
        return [x for x in self.spalte if x < wert]

    def filter_ist(self, wert):
        return [x for x in self.spalte if x == wert]

    # ----- Visualisierungen -----
    def plot_histogramm(self, bins=10):
        if self.typ != "zahl":
            raise NurZahlen()
        plt.hist(self.spalte, bins=bins, color='skyblue', edgecolor='black')
        plt.title(f"Histogramm von {self.name}")
        plt.xlabel(self.name)
        plt.ylabel("Häufigkeit")
        plt.show()

    def plot_balken(self):
        if self.typ != "text":
            raise TypeError("Balkendiagramm nur für Textspalten")
        counts = Counter(self.spalte)
        plt.bar(counts.keys(), counts.values(), color='orange')
        plt.title(f"Balkendiagramm von {self.name}")
        plt.xlabel(self.name)
        plt.ylabel("Häufigkeit")
        plt.show()

    def __str__(self):
        return f"{self.name} ({self.typ}): {self.spalte}"
