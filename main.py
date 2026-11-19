from flask import Flask, render_template
from models import Session, Semester, Modul, Leistungsnachweis
import daten

app = Flask(__name__)
daten.beispieldaten_einfuegen()


@app.route("/")
def index():
    """Startseite von GradeView."""
    with Session() as session:
        alle_semester = session.query(Semester).order_by(Semester.id).all()
        return render_template("index.html", semester=alle_semester)


@app.route("/semester/<int:id>")
def semester_ansicht(id):
    """Zeigt alle Module eines Semesters."""
    with Session() as session:
        gefunden = session.query(Semester).filter(Semester.id == id).first()
        if gefunden is None:
            return "Semester nicht gefunden", 404

        module_liste = session.query(Modul).filter(Modul.semester_id == id).all()
        return render_template("semester.html", semester=gefunden, module=module_liste)

    
@app.route("/modul/<int:id>")
def modul_ansicht(id):
    """Zeigt ein Modul mit allen Leistungsnachweisen."""
    with Session() as session:
        modul = session.query(Modul).filter(Modul.id == id).first()
        if modul is None:
            return "Modul nicht gefunden", 404

        nachweise = session.query(Leistungsnachweis).filter(
            Leistungsnachweis.modul_id == id).all()
        return render_template("modul.html", modul=modul, nachweise=nachweise)

@app.errorhandler(404)
def not_found(error):
    """Fehlerseite für unbekannte Adressen."""
    return "Seite nicht gefunden", 404


if __name__ == "__main__":
    app.run(debug=True)