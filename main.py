from flask import Flask, render_template
import daten

app = Flask(__name__)


@app.route("/")
def index():
    """Startseite von GradeView."""
    return render_template("index.html", semester=daten.semester)


@app.route("/semester/<int:id>")
def semester_ansicht(id):
    """Zeigt alle Module eines Semesters."""
    
    # Semester mit der passenden id suchen
    gefunden = None
    for s in daten.semester:
        if s["id"] == id:
            gefunden = s

    # Alle Module dieses Semesters sammeln
    module_liste = []
    for m in daten.module:
        if m["semester_id"] == id:
            module_liste.append(m)

    return render_template("semester.html", semester=gefunden, module=module_liste)


if __name__ == "__main__":
    app.run(debug=True)