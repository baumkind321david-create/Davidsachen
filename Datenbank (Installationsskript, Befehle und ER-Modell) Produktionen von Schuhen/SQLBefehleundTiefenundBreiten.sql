--Aufgabe 1
--Diese Abfrage zeigt alle Produktionsabteilungen, die direkt oder indirekt unter der
--Abteilung liegen, die das Material „Pappe“ benutzen
Select * From Produktionsabteilung
Start With Hauptabteilung_ID = (Select Abteilungs_ID
From Material Where Materialname = 'Pappe')
Connect by prior Abteilungs_ID = Hauptabteilung_ID
--Aufgabe 2
-- Diese Abfrage zeigt uns die Gesamtanzahl der Produktionsaufträge für jeden
--einzelnen Schuhmodell Typ und welche Kunden diese Aufträge erteilt haben. 
SELECT 
    sm.typ AS Schuhmodell_Typ, 
    k.vorname AS Kunden_Vorname, 
    k.nachname AS Kunden_Nachname, 
    COUNT(pa.auftrags_id) AS Gesamt_Anzahl_Auftraege
FROM produktionsauftrag pa
JOIN schuhmodell sm ON pa.modell_id = sm.modell_id
JOIN kunde k ON pa.kunden_id = k.kunden_id
JOIN bearbeitet_pp bpp ON pa.auftrags_id = bpp.auftrags_id --um zuverhindern, dass Auftrag gelöscht wird muss auch midestens einmal bearbeitet werden
GROUP BY sm.typ, k.vorname, k.nachname;
--aufgabe 3
 --Diese Abfrage liefert uns den Vornamen und Nachname aller Kunden, die
--Aufträge erstellt haben, in denen die Schuhgröße immer über 40 ist.
SELECT 
    k.vorname, 
    k.nachname
FROM Kunde k
WHERE 40 < ALL (
    SELECT pa.groesse
    FROM produktionsauftrag pa
    WHERE pa.kunden_id = k.kunden_id
)
AND EXISTS (
    SELECT 1 
    FROM produktionsauftrag pa 
    WHERE pa.kunden_id = k.kunden_id
);
--aufgabe 4
 --Diese Abfrage liefert uns die Standorte alphabetisch sortiert nach der Straße, die
--in der Stadt mit der PLZ 59368 wohnen aber nicht in der Brachtstrasse liegen.
SELECT s.strassennummer, s.strasse, s.postleitzahl, s.lieferant_id
FROM Standort S
WHERE postleitzahl = 59368
MINUS
SELECT strassennummer, strasse, postleitzahl, Lieferant_id
FROM Standort
WHERE Strasse = 'Roggenkamp' 
ORDER BY Strasse;

--aufgabe 5
--Diese Abfrage soll uns alle Abteilungen anzeigen, die noch kein Material geliefert
--bekommen haben. 
SELECT abteilungsname
FROM produktionsabteilung
WHERE abteilungs_id NOT IN (
    SELECT m.abteilungs_id
    FROM material m
    JOIN liefert l ON m.material_id = l.material_id
);

--Tiefensuche
CREATE OR REPLACE FUNCTION tiefensuche (
    p_start IN VARCHAR
) RETURN VARCHAR AS
    v_result VARCHAR(200) := '';
    CURSOR ergebnis_cursor IS
        SELECT *
        FROM produktionsabteilung
        START WITH hauptabteilung_id = (
            SELECT abteilungs_id
            FROM material
            WHERE materialname = p_start
        )
        CONNECT BY PRIOR abteilungs_id = hauptabteilung_id;
BEGIN
    FOR r IN ergebnis_cursor LOOP
        v_result := v_result || r.abteilungsname || ' ';
    END LOOP;
    RETURN v_result;
END tiefensuche;

--breitensuche
CREATE OR REPLACE FUNCTION breitensuche (
    p_start IN VARCHAR
) RETURN VARCHAR AS
    v_result VARCHAR(200) := '';
    CURSOR ergebnis_cursor IS
        SELECT *
        FROM produktionsabteilung
        START WITH hauptabteilung_id = (
            SELECT abteilungs_id
            FROM material
            WHERE materialname = p_start
        )
        CONNECT BY PRIOR abteilungs_id = hauptabteilung_id
        ORDER BY LEVEL, abteilungs_id;
BEGIN
    FOR r IN ergebnis_cursor LOOP
        v_result := v_result || r.abteilungsname || ' ';
    END LOOP;
    RETURN v_result;
END breitensuche;
--testen Tiefensuche;
Select
tiefensuche('Pappe') as abteilungs_pfad
from DUAL

--testen breitenscuhe
Select
breitensuche('Pappe') as abteilungs_pfad
from DUAL