from flask import Flask, render_template, request, redirect, url_for
from models import Session, Semester, Modul, Leistungsnachweis
import daten
import berechnung

app = Flask(__name__)
daten.beispieldaten_einfuegen()


def zeilen_erstellen(session, module_liste):
    """Berechnet für jedes Modul die Note und den Status.

    Gibt eine Liste von Dicts mit den Schlüsseln 'modul', 'note' und 'status' zurück.
    """
    zeilen = []
    for m in module_liste:
        nachweise = session.query(Leistungsnachweis).filter(
            Leistungsnachweis.modul_id == m.id).all()
        note = berechnung.modulnote(nachweise)
        zeilen.append({"modul": m, "note": note, "status": berechnung.status(note)})
    return zeilen


def modul_pruefen(name, ects_text):
    """Prüft die Eingaben des Modul-Formulars (Sanitizing).

    Gibt eine Fehlermeldung zurück oder None, wenn alles in Ordnung ist.
    """
    if name == "":
        return "Bitte einen Namen eingeben."
    if ects_text == "":
        return "Bitte die ECTS eingeben."
    if int(ects_text) <= 0:
        return "Die ECTS müssen grösser als 0 sein."
    return None


@app.route("/")
def index():
    """Dashboard mit Kennzahlen und Liste aller Semester."""
    with Session() as session:
        alle_semester = session.query(Semester).order_by(Semester.id).all()
        alle_module = session.query(Modul).all()

        zeilen = zeilen_erstellen(session, alle_module)
        k = berechnung.kennzahlen(zeilen)
        return render_template("index.html", semester=alle_semester, k=k)


@app.route("/semester/<int:id>")
def semester_ansicht(id):
    """Zeigt alle Module eines Semesters mit Note, Status und Semesterschnitt."""
    with Session() as session:
        gefunden = session.query(Semester).filter(Semester.id == id).first()
        if gefunden is None:
            return "Semester nicht gefunden", 404

        module_liste = session.query(Modul).filter(Modul.semester_id == id).all()
        zeilen = zeilen_erstellen(session, module_liste)
        schnitt = berechnung.semesterschnitt(zeilen)
        return render_template("semester.html", semester=gefunden,
                               zeilen=zeilen, schnitt=schnitt)


@app.route("/modul/<int:id>")
def modul_ansicht(id):
    """Zeigt ein Modul mit allen Leistungsnachweisen und der Modulnote."""
    with Session() as session:
        modul = session.query(Modul).filter(Modul.id == id).first()
        if modul is None:
            return "Modul nicht gefunden", 404

        nachweise = session.query(Leistungsnachweis).filter(
            Leistungsnachweis.modul_id == id).all()
        note = berechnung.modulnote(nachweise)
        return render_template("modul.html", modul=modul, nachweise=nachweise,
                               note=note, status=berechnung.status(note))


@app.route("/semester/<int:id>/modul/neu")
def modul_neu(id):
    """Zeigt das leere Formular für ein neues Modul."""
    return render_template("modul_formular.html", titel="Neues Modul",
                           aktion=url_for("modul_neu_speichern", id=id),
                           name="", ects=4, fehler=None)


@app.route("/semester/<int:id>/modul/neu", methods=["POST"])
def modul_neu_speichern(id):
    """Speichert ein neues Modul im Semester."""
    name = request.form["name"].strip()
    ects_text = request.form["ects"].strip()

    fehler = modul_pruefen(name, ects_text)
    if fehler is not None:
        return render_template("modul_formular.html", titel="Neues Modul",
                               aktion=url_for("modul_neu_speichern", id=id),
                               name=name, ects=ects_text, fehler=fehler)

    with Session() as session:
        session.add_all([Modul(name=name, ects=int(ects_text), semester_id=id)])
        session.commit()
    return redirect(url_for("semester_ansicht", id=id))


@app.route("/modul/<int:id>/bearbeiten")
def modul_bearbeiten(id):
    """Zeigt das Formular mit den Daten eines bestehenden Moduls."""
    with Session() as session:
        modul = session.query(Modul).filter(Modul.id == id).first()
        if modul is None:
            return "Modul nicht gefunden", 404
        return render_template("modul_formular.html", titel="Modul bearbeiten",
                               aktion=url_for("modul_bearbeiten_speichern", id=id),
                               name=modul.name, ects=modul.ects, fehler=None)


@app.route("/modul/<int:id>/bearbeiten", methods=["POST"])
def modul_bearbeiten_speichern(id):
    """Speichert die Änderungen an einem Modul."""
    name = request.form["name"].strip()
    ects_text = request.form["ects"].strip()

    fehler = modul_pruefen(name, ects_text)
    if fehler is not None:
        return render_template("modul_formular.html", titel="Modul bearbeiten",
                               aktion=url_for("modul_bearbeiten_speichern", id=id),
                               name=name, ects=ects_text, fehler=fehler)

    with Session() as session:
        session.query(Modul).filter(Modul.id == id).update(
            {"name": name, "ects": int(ects_text)})
        session.commit()
    return redirect(url_for("modul_ansicht", id=id))


@app.route("/modul/<int:id>/loeschen", methods=["POST"])
def modul_loeschen(id):
    """Löscht ein Modul mitsamt seinen Leistungsnachweisen."""
    with Session() as session:
        modul = session.query(Modul).filter(Modul.id == id).first()
        if modul is None:
            return "Modul nicht gefunden", 404
        semester_id = modul.semester_id

        session.query(Leistungsnachweis).filter(
            Leistungsnachweis.modul_id == id).delete()
        session.query(Modul).filter(Modul.id == id).delete()
        session.commit()
    return redirect(url_for("semester_ansicht", id=semester_id))


@app.errorhandler(404)
def not_found(error):
    """Fehlerseite für unbekannte Adressen."""
    return "Seite nicht gefunden", 404


if __name__ == "__main__":
    app.run(debug=True)