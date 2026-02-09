# ------------------- OwnTable-------------------

from Spalte import OwnColumn
import matplotlib.pyplot as plt
from collections import defaultdict

class OwnTable:
    def __init__(self):
        self.dic = {}

    # ----- Spalten -----
    def hinzufuegeSpalte(self, col: OwnColumn):
        self.dic[col.name] = col.spalte

    def loescheSpalte(self, name):
        if name in self.dic:
            del self.dic[name]

    # ----- Zeilen -----
    def hinzufuegeZeile(self, werte: list):
        if len(werte) != len(self.dic):
            raise ValueError("Zeilenlänge stimmt nicht mit Spaltenanzahl überein")
        for i, key in enumerate(self.dic):
            self.dic[key].append(werte[i])

    def loescheZeile(self, index):
        for key in self.dic:
            del self.dic[key][index]

    # ----- Zugriff -----
    def head(self, n=5):
        return {k: v[:n] for k, v in self.dic.items()}

    def tail(self, n=5):
        return {k: v[-n:] for k, v in self.dic.items()}

    def select_rows(self, condition_function):
        result = defaultdict(list)
        n = len(next(iter(self.dic.values())))
        for i in range(n):
            row = {k: self.dic[k][i] for k in self.dic}
            if condition_function(row):
                for k in self.dic:
                    result[k].append(row[k])
        return dict(result)

    # ----- Gruppieren -----
    def groupby(self, spaltenname):
        result = defaultdict(list)
        n = len(next(iter(self.dic.values())))
        for i in range(n):
            key = self.dic[spaltenname][i]
            for k in self.dic:
                result[(key, k)].append(self.dic[k][i])
        grouped = defaultdict(list)
        for (key, col), values in result.items():
            grouped[key].append(values)
        return dict(grouped)

    # ----- Tabellen zusammenführen -----
    def merge(self, andere, on):
        merged = OwnTable()
        keys = list(self.dic.keys()) + [k for k in andere.dic if k != on]
        for k in keys:
            merged.dic[k] = []

        n_self = len(next(iter(self.dic.values())))
        n_andere = len(next(iter(andere.dic.values())))
        map_andere = {andere.dic[on][i]: i for i in range(n_andere)}

        for i in range(n_self):
            row_key = self.dic[on][i]
            for k in self.dic:
                merged.dic[k].append(self.dic[k][i])
            if row_key in map_andere:
                idx = map_andere[row_key]
                for k in andere.dic:
                    if k != on:
                        merged.dic[k].append(andere.dic[k][idx])
        return merged

    # ----- Plotting -----
    def plot_box(self, spaltenname):
        plt.boxplot(self.dic[spaltenname])
        plt.title(f"Boxplot von {spaltenname}")
        plt.show()

    def plot_histogram(self, spaltenname, bins=10):
        plt.hist(self.dic[spaltenname], bins=bins, color='lightgreen', edgecolor='black')
        plt.title(f"Histogramm von {spaltenname}")
        plt.show()

    def scatterplot(self, x, y):
        plt.scatter(self.dic[x], self.dic[y])
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

    def punktdiagramm(self, x, y):
        plt.plot(self.dic[x], self.dic[y], color='blue', marker='o', linestyle='dashed')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

    def describe(self):
        beschreibung = {}
        for key, values in self.dic.items():
            col = OwnColumn(key)
            for v in values:
                col.hinzufuegen(v)
            if col.typ == "zahl":
                beschreibung[key] = {
                    "Mittelwert": col.mittelwert(),
                    "Median": col.median(),
                    "Varianz": col.varianz(),
                    "Standardabweichung": col.standardabweichung(),
                    "Range": col.range()
                }
            else:
                beschreibung[key] = {
                    "Häufigkeit": dict((v, col.spalte.count(v)) for v in set(col.spalte))
                }
        return beschreibung

    def __str__(self):
        return str(self.dic)
