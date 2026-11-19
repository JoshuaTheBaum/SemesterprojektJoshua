from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Float

# Datenbank-Verbindung herstellen
engine = create_engine("sqlite:///gradeview.db")

# Basisklasse für die Datenklassen
Base = declarative_base()

# Session erstellen
Session = sessionmaker(bind=engine)


class Semester(Base):
    """Datenklasse für die Tabelle 'semester'."""
    __tablename__ = "semester"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Modul(Base):
    """Datenklasse für die Tabelle 'module'."""
    __tablename__ = "module"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ects = Column(Integer)
    semester_id = Column(Integer)


class Leistungsnachweis(Base):
    """Datenklasse für die Tabelle 'leistungsnachweise'. Die Note ist leer, solange offen."""
    __tablename__ = "leistungsnachweise"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    gewicht = Column(Integer)
    note = Column(Float)
    modul_id = Column(Integer)


# Tabellen erzeugen, falls sie noch nicht existieren
Base.metadata.create_all(engine)