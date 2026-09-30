# GradeView – Persönliche Notenübersicht für Studierende

## Ausgangslage
Als Student belege ich pro Semester mehrere Module an der FHGR, die jeweils aus verschiedenen Leistungsnachweisen mit unterschiedlicher Gewichtung bestehen (Prüfungen, Projekte, Präsentationen). Manchmal sind es 4 Leistungsnachweise und teilweise nur 1. Die Noten sind auf verschiedene Plattformen verteilt, und ich habe keine Übersicht darüber, wie mein aktueller Notenschnitt ist, wie viele ECTS ich bereits gesammelt habe oder welche Note ich in der nächsten Prüfung noch brauche, um ein Modul zu bestehen oder eine bestimmte Wunschnote zu erreichen.

## Projektidee
Die Webapp heistt GradeView. Sie ist eine Flask-Webapplikation, mit der Studierende ihre Semester, Module und Teilnoten erfassen. Die App berechnet automatisch gewichtete Modulnoten, den ECTS-gewichteten Durchschnitt pro Semester und über das ganze Studium und zeigt die Entwicklung in Diagrammen. Ein Zielnoten-Rechner zeigt, welche Note in den noch offenen Leistungsnachweisen nötig ist, um eine gewünschte Modulnote zu erreichen.

## Ansichten
1. **Dashboard**: Gesamtschnitt, gesammelte ECTS, Anzahl bestandener/offener Module und ein Diagramm zur Notenentwicklung über die Semester
2. **Semesterübersicht**: Alle Module eines Semesters mit Modulnote, ECTS, Status (bestanden, nicht bestanden, offen) und Semesterschnitt
3. **Moduldetail**: Alle Leistungsnachweise mit Gewichtung und Note sowie die berechnete Modulnote
4. **Formular Modul erfassen/bearbeiten**: Name, ECTS, Semester
5. **Formular Leistungsnachweis erfassen/bearbeiten**: Bezeichnung, Gewichtung in Prozent, Datum, Note (optional, falls noch offen)
6. **Zielnoten-Rechner**: Wunschnote für ein Modul eingeben, benötigte Note für die offenen Leistungsnachweise wird berechnet
7. **Auswertungen**: Diagramme, z. B. Modulnoten im Vergleich und Notenverteilung

## Daten
Die Daten werden mit SQLAlchemy in einer Datenbank gespeichert:
- **Semester**: Bezeichnung (z. B. HS26), Startdatum
- **Module**: Name, ECTS, Zuordnung zu einem Semester
- **Leistungsnachweise**: Bezeichnung, Gewichtung, Datum, Note (1–6), Zuordnung zu einem Modul

Ausgegeben werden die Daten als HTML-Tabellen, Kennzahlen und Diagramme. Optional falls Zeit bleibt ist ein CSV-Export der Notenübersicht möglich.

## Funktionen
- Semester, Module und Leistungsnachweise erfassen, bearbeiten und löschen
- Automatische Berechnung der gewichteten Modulnote (nur bei vollständigen Gewichtungen von 100 %)
- ECTS-gewichteter Durchschnitt pro Semester und gesamt
- Statusanzeige pro Modul (bestanden ab 4.0)
- Zielnoten-Rechner für offene Leistungsnachweise
- Diagramme zur Notenentwicklung und zum Modulvergleich
- Validierung der Eingaben (Note zwischen 1 und 6, Gewichtungen ergeben 100 %)

## Quellen
Es werden keine externen Datenquellen genutzt. Die Daten gibt der Nutzer selbst ein. Zum Testen werden eigene Beispieldaten erstellt.

## Technologien
Python, Flask, Jinja2, SQLAlchemy, SQLite, HTML/CSS (Bootstrap), Plotly oder Matplotlib für Diagramme