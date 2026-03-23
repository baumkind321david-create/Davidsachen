import pandas as pd
from matplotlib import pyplot as plt
de = pd.read_csv("C:/Users/David/Downloads/AmesHousing.csv", sep=";")
de.columns #die Spalten
#print(de.head()) #ersten Zeilen
print(de.to_string()) #den kompletten Dataframe

print(de.loc[0]) #durch die Zeile mit Index
print(de.loc[0, "Street"]) # durch Index Zeile und dann die Spalte
print(de.loc[0] ["Street"]) #alternative Schreibweise Index Zeile und dann die Spalte
print(de["Street"][0]) #erst Spalte und dann Zeile
print(de["Street"]) #nur die Spalte
#mehrere Spalten
print(de.loc[0:2, ["Street", "Year Built"]]) #inklusive!!!
print(de.iloc[0:2, 0:2]) #eklusive und nur mit Positionen!!!

#Duplikate entfernen!
de = de.drop_duplicates()
print(de)
#Nur Zeilen filtern, die normale Verkaufskondition besitzen
#wenn ich nur bestimmte Zeilen möchte und dann
#de = de.loc[1:3]
de = de.loc[de["Sale Condition"] == "Normal"]

print(de)

#das Alter als sie verkauft wurden
de["Age"] = de["Yr Sold"] - de["Year Built"]
#Durchschnittlichen Verkaufspreis abhängig von Nachbarschaft und Gebäudetyp
durchschnittspreisVerkauNei = de.groupby(["Neighborhood", "Bldg Type"])["SalePrice"].mean()
print(durchschnittspreisVerkauNei)
print(de.to_string())
#Daten vorbereiten und Kreisdiagramm von Häusertypen
anteileBild = de["Bldg Type"].value_counts()
print(anteileBild)
plt.figure(figsize = (10,10))
plt.title("Anteile der Häusertypen")
plt.pie(anteileBild.values, labels = anteileBild.index.values)
plt.show()

