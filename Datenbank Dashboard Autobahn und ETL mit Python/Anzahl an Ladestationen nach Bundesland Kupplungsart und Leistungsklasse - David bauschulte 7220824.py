import requests #um die Daten von der API abzurufen https://mimo.org/glossary/python/requests-library
import pandas as pd
import reverse_geocode #https://pypi.org/project/reverse-geocode/ die Bibliothek um Bundesländer herrauszufinden
import sqlite3

db_path = r"C:\Users\baumk\OneDrive\Desktop\4. Semester\eer\ev_charging.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

#das ist die Hauptseite, wo sich alle Autobahnen befinden
hauptURL = "https://verkehr.autobahn.de/o/autobahn/"

#wir holen mit get requests und mithilfe von json die Autobahnen
response = requests.get(hauptURL)
#das ist Dictionary und mithilfe von roads
autobahnen = response.json()["roads"]

#hier speichern, wir alle Elektroladesäulen
alle_Elektro = []

#hier speichern wir erstmal alle Bundesländer, um später mithilfe von reverse_geocode vom Englischen ins Deutsche
#ähnlicher Code, wie Arthur (haben zusammen gemacht)
bundeslaender = [
    "Saarland", "Nordrhein-Westfalen", "Niedersachsen", "Berlin", "Thüringen",
    "Sachsen", "Sachsen-Anhalt", "Bremen", "Rheinland-Pfalz", "Hessen",
    "Hamburg", "Schleswig-Holstein", "Baden-Württemberg", "Bayern",
    "Brandenburg", "Mecklenburg-Vorpommern"
]

#hier erstellen wir eine Hilfsfunktion, die dann vergleicht, was für ein Bundesland ist und gibt es je nach if das jeweilige
#Bundesland. Ausland bedeutet, dass manche Ladestationen in Frankreich zugeordnet worden sind
def map_bundesland(bundesland):
    if bundesland == "North Rhine-Westphalia":
        bundesland = "Nordrhein-Westfalen"
    elif bundesland == "Lower Saxony":
        bundesland = "Niedersachsen"
    elif bundesland == "City state Bremen":
        bundesland = "Bremen"
    elif bundesland == "Saxony-Anhalt":
        bundesland = "Sachsen-Anhalt"
    elif bundesland == "Bavaria":
        bundesland = "Bayern"
    elif bundesland == "Hesse":
        bundesland = "Hessen"
    elif bundesland == "Thuringia":
        bundesland = "Thüringen"
    elif bundesland == "Saxony":
        bundesland = "Sachsen"
    elif bundesland == "Baden-Wurttemberg":
        bundesland = "Baden-Württemberg"
    elif bundesland == "State of Berlin":
        bundesland = "Berlin"
    if bundesland not in bundeslaender:
        bundesland = "Ausland"
    return bundesland

#mit dieser Hilfsfunktion extrahieren wir später bei "Description in der jeweiligen Ladestation die Ladeleistung (kW)
#und unterteilen es in jeweiligen Ladeleistungsklasse

def parse_leistung(leistung):
    #wenn nichts übergeben wurde oder nichts in leistung steht, soll nichts zurückgegeben werden
    if not leistung or "kW" not in leistung:
        return None
    zahlen = ""
    for c in leistung:
        if c.isdigit():
            zahlen += c
    if zahlen == "":
        return None
    kw = int(zahlen)
    if kw < 50:
        klasse = "langsam"
    elif kw < 150:
        klasse = "mittel"
    else:
        klasse = "schnell"
    return kw, klasse

#die Hilfsfunktion ist dafür zuständig in Description: ["DC Kupplung Combo, AC Kupplung Combo"] für
#einen Ladenpunkt in einer Array auszugeben, dass aus dem einen langen String: die verschiedene Kupplungsarten
#extrahiert und im neuen Array packt
def split_kupplung(kupplung_list):
    result = []
    for k in kupplung_list:
        #hier unterteilen, wir es durch das Komma
        parts = k.split(",")
        #dann wird jeden Teil, den wir getrennt haben, sich angeschaut
        for p in parts:
            #es kann sein, dass dadruch die Trennung vorne und hinten sich Leerzeichen finden - hiermit trennen wir es auf
            clean = p.strip()
            if clean:
                #wir fügen das dann in der endgültigen Liste ein
                result.append(clean)
    return result

#hier gehen wir alle Autobahnen durch mithilfe f String: HauptURL/diejeweilige Autobahn/und services.., dass uns die
#die Charging Station zurückgibt
for a in autobahnen:
    url = f"{hauptURL}{a}/services/electric_charging_station"
    r = requests.get(url).json()
    #wenn es nichts gibt für die jeweilige Autobahn, dann soll übersprungen werden
    if "electric_charging_station" not in r:
        continue
    #hier gehen wir alle station durch und fügen am Ende noch eine neue Spalte für die jeweilige Autobahn
    for station in r["electric_charging_station"]:
        station["autobahn"] = a
        alle_Elektro.append(station)

#am Ende erstellen wir ein DataFrame

df = pd.DataFrame(alle_Elektro)
#hier erstellen wir erstmal die zwischentabellen - eine für ladestation und dann eine andere Zwischen-
#tabelle, wo mithilfe der Ladestationtabelle die Daten für die jeweilige Ladestation hinzufügen können!
#wenn eine Ladestation mehrere Kupplungsarten hat, soll bei dieser Tabelle mehrere Zeilen für dieselbe Ladestation
#erstellt werden
cursor.execute("""
CREATE TABLE IF NOT EXISTS stations (
    station_id INTEGER PRIMARY KEY,
    station_identifier TEXT,
    autobahn TEXT,
    titel TEXT,
    lat REAL,
    lon REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS charging_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_id INTEGER,
    ladepunkt INTEGER,
    kupplung TEXT,
    leistung_kw INTEGER,
    leistung_klasse TEXT,
    lat REAL,
    lon REAL,
    bundesland TEXT
)
""")

#hier zählen wir für jede Station hoch
station_id_counter = 1

#mit itertupels, was schneller als itterrows(PK2) gehen wir jeden ladestation im Dataframe, was wir erstellt haben
#durch und transformieren, bevor wir die Daten in die Zwischentabellen und dann endgültig in der Haupttabelle hinzufügen
#können -> in jedes Objekt eine Zeile
for row in df.itertuples(index=False):

    #wir holen die Kordinaten für die jeweilige Ladestation
    coord = row.coordinate
    #wenn es keine coordinate gibt, oder kein lat/long -> überspringen wir zur nächsten Ladestation
    if not coord or "lat" not in coord or "long" not in coord:
        continue

    #hierfür stellen wir sicher, wie im Transformierschritten, dass wir die Koordinaten in float
    #sodass wir damit Bundesland herrausfinden kann
    lat = float(coord["lat"])
    lon = float(coord["long"])

    #wir holen hier das Bundesland und geben das in der Hilfsfunktion, was uns die Übersetzung gibt
    location = reverse_geocode.get((lat, lon)) #dictionary

    #"city": "Melbourne",
    #"latitude": -37.814,
    #"longitude": 144.96332,
    #"population": 4917750,
   # "state": "Victoria",
    #"country": "Australia"

    bundesland = map_bundesland(location["state"])

    #wenn es keine Beschreibung gibt, obwohl wir ein Bundesland haben, sollen wir zur nächsten
    #Station -> ergibt keinen Sinn, wenn es nichts in der Description ist, weil da Kupplungsarten und Ladeleistungen
    #stehen!
    if not row.description:
        continue

    #wir speichern die  deskription (was ein Array ist) in desc und gehen  mkit for schleife durch
    desc = row.description

    station_result = []
    current = None

#wir gehen alle Elemente im Array Desc durch
    for line in desc:
        #wenn im Array irgendwo Ladepunkt steht und Doppelpunkt ein Dictionaryobjekt current und dann in der Liste gespeichert

        if line.startswith("Ladepunkt") and ":" in line:
            nummer = line.split()[1].replace(":", "") #kein Doppelpunktnhju654543w33
            current = {
                "ladepunkt": nummer,
                "kupplung": [],
                "leistung": None
            }
            station_result.append(current)

        #wenn es kein ladepunkt aber schon das objekt current erstellt wird, dann kucken wir
        #mithilfe von kW in der jeweiligen Objekt in Description, die Ladeleistung und durch
        #AC und DC die Kupplungsart

        #wenn zum beispiel nun ladepunkt 2 kommt, überschreiben wir das current und kucken auch hier Ladeleistung/
        #und Kupplungsart -> das Ladepunkt 1 ist trotzdem in der Liste station_result drin
        elif current is not None:

            if "kW" in line:
                current["leistung"] = line

            if "AC" in line or "DC" in line:
                current["kupplung"].append(line)

#wenn in description keine ladeleistung ist, dann überspringen wir zu der nächsten Station
#es kann sein, dass die fehlen, aber Kupplungsart/Ladeleistung drin sind, aber das wollen trotzdem nicht berücksichtigen
    if len(station_result) == 0:
        continue

#wir erhöhen die ladestion ID um 1 für die nächste
    station_id = station_id_counter
    station_id_counter += 1

#wir komnoenieren autobahn title station_id für die Zwischentabelle Ladestation, finde ich schöner
    station_identifier = f"{row.autobahn} | {row.title} ; {station_id}"

#wir fügen alle Werte für die zwischentabelle Ladestation ein
    cursor.execute("""
    INSERT INTO stations (
        station_id,
        station_identifier,
        autobahn,
        titel,
        lat,
        lon
    ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        station_id,
        station_identifier,
        row.autobahn,
        row.title,
        lat,
        lon
    ))

#hier gehen wir alle Ladepunkte innerhalb der ladestation durch, wenn hier ein Wert fehlt, wie Kupplungsart
#oder die ladeleistung, dann überspringen zu der nächsten ladeleistung innerhalb der ladestation
    for lp in station_result:

        if not lp["kupplung"]:
            continue

        result = parse_leistung(lp["leistung"])
        if result is None:
            continue

        kw = result[0]
        klasse = result[1]

        clean_kupplungen = split_kupplung(lp["kupplung"])

        #am Ende fügen wir jede Kupplungsart für die jeweilige Ladeleistung einen Eintrag in der anderen
        #zwischentabelle
        for kupplung in clean_kupplungen:

            cursor.execute("""
            INSERT INTO charging_data (
                station_id,
                ladepunkt,
                kupplung,
                leistung_kw,
                leistung_klasse,
                lat,
                lon,
                bundesland
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                station_id,
                lp["ladepunkt"],
                kupplung,
                kw,
                klasse,
                lat,
                lon,
                bundesland
            ))

#wenn es die finale Tabelle schon gibt, soll gelöscht werden und wieder aufgesetzt werden
cursor.execute("""
DROP TABLE IF EXISTS charging_data_agg
""")

#hier wird die finale tabelle durch charging_data (zwischentabelle) erstellt
#wir gruppieren hier pro bundesland, kupplung, leistungsklasse
cursor.execute("""
CREATE TABLE charging_data_agg AS
SELECT
    bundesland,
    kupplung,
    leistung_klasse,
    COUNT(DISTINCT station_id) AS Anzahl_Ladestation
FROM charging_data
GROUP BY bundesland, kupplung, leistung_klasse
""")


#wir löschen hier die Zwischentabellen!
cursor.execute("""
DROP TABLE IF EXISTS charging_data
""")
cursor.execute("""
DROP TABLE IF EXISTS stations
""")
conn.commit()
conn.close()

print("Fertig: Daten gespeichert.")