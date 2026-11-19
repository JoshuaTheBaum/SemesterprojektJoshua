from flask import Flask, render_template
from models import Session, Semester, Modul
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


if __name__ == "__main__":
    app.run(debug=True)