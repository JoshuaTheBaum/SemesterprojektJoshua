from flask import Flask, render_template
import daten

app = Flask(__name__)


@app.route("/")
def index():
    """Startseite von GradeView."""
    return render_template("index.html", semester=daten.semester)


if __name__ == "__main__":
    app.run(debug=True)