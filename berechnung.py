def modulnote(nachweise):
    """Berechnet die gewichtete Modulnote.

    Gibt None zurück, wenn noch eine Note offen ist oder die
    Gewichtungen zusammen nicht 100 % ergeben.
    """
    summe_gewicht = 0
    summe_noten = 0
    for n in nachweise:
        if n.note is None:
            return None
        summe_gewicht = summe_gewicht + n.gewicht
        summe_noten = summe_noten + n.note * n.gewicht

    if summe_gewicht != 100:
        return None
    return round(summe_noten / 100, 2)


def status(note):
    """Gibt den Status eines Moduls als Text zurück."""
    if note is None:
        return "offen"
    if note >= 4:
        return "bestanden"
    return "nicht bestanden"


def semesterschnitt(zeilen):
    """Berechnet den ECTS-gewichteten Schnitt aller Module mit Note.

    zeilen ist eine Liste von Dicts mit den Schlüsseln 'modul' und 'note'.
    """
    summe_ects = 0
    summe_noten = 0
    for z in zeilen:
        if z["note"] is not None:
            summe_ects = summe_ects + z["modul"].ects
            summe_noten = summe_noten + z["note"] * z["modul"].ects

    if summe_ects == 0:
        return None
    return round(summe_noten / summe_ects, 2)