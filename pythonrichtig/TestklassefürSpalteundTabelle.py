import Praktikum9Tabelle as Tabelle
import Praktikum9Spalt as Spalt

d = Spalt.OwnColumn("Da")

d.fügeZahlNdarray(2)
d.fügeZahlNdarray(5)
d.fügeZahlNdarray(2)
d.fügeZahlNdarray(2)

t = Spalt.OwnColumn("er")
t.fügeZahlNdarray(23)
t.fügeZahlNdarray(23)
t.fügeZahlNdarray(23)
t.fügeZahlNdarray(23)



w = Tabelle.OwnTable()
w.fügeSpalte(d)
w.fügeSpalte(t)

w.zeichnen()
