# ------------------- test_script.py -------------------

from  Spalte import OwnColumn
from Tabelle import OwnTable

# ---- OwnColumn testen ----
print("=== OwnColumn Test ===")
col_zahlen = OwnColumn("Zahlen")
col_text = OwnColumn("Buchstaben")

# Werte hinzufügen
for i in range(1, 6):
    col_zahlen.hinzufuegen(i)  # 1,2,3,4,5

for buchstabe in ["a", "b", "a", "c", "b"]:
    col_text.hinzufuegen(buchstabe)

print("Zahlen-Spalte:", col_zahlen)
print("Text-Spalte:", col_text)

# Statistik
print("Summe:", col_zahlen.summe())
print("Mittelwert:", col_zahlen.mittelwert())
print("Median:", col_zahlen.median())
print("Varianz:", col_zahlen.varianz())
print("Standardabweichung:", col_zahlen.standardabweichung())
print("Range:", col_zahlen.range())
print("Modalwert (Text):", col_text.modalwert())

# Filter
print("Zahlen > 3:", col_zahlen.filter_groesser(3))
print("Zahlen < 3:", col_zahlen.filter_kleiner(3))
print("Buchstabe 'a':", col_text.filter_ist("a"))

# Plot
# col_zahlen.plot_histogramm()
# col_text.plot_balken()


# ---- OwnTable testen ----
print("\n=== OwnTable Test ===")
table = OwnTable()

# Spalten hinzufügen
table.hinzufuegeSpalte(col_zahlen)
table.hinzufuegeSpalte(col_text)

# Zeilen hinzufügen
table.hinzufuegeZeile([6, "d"])
table.hinzufuegeZeile([7, "a"])

print("Head:", table.head(3))
print("Tail:", table.tail(2))

# Zeilen filtern
rows_gt_4 = table.select_rows(lambda row: row["Zahlen"] > 4)
print("Zeilen mit Zahlen > 4:", rows_gt_4)

# Statistik beschreiben
print("Describe:", table.describe())

# Plot
# table.scatterplot("Zahlen", "Zahlen")  # Beispiel
# table.plot_box("Zahlen")
# table.plot_histogram("Zahlen")
